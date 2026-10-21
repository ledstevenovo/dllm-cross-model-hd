#!/usr/bin/env python
"""Turn an adopted draft pre-review into reviewed labels (human sign-off recorded).

The reviewer field records how the sign-off happened: a rule-level approval writes
``reviewer="<name>"`` and ``review_mode="rule-signoff"`` while keeping the per-item notes
and flags, so the audit trail shows what was approved and what was machine-proposed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import common  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft-labels", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--reviewer", required=True, help="human reviewer name, e.g. ledstevenovo")
    parser.add_argument("--review-mode", default="rule-signoff",
                        choices=["rule-signoff", "item-by-item"])
    parser.add_argument("--corrected-ids", help="optional json file: {pilot_index: {decision,label,note}}")
    parser.add_argument("--signed-off-at", default="2026-10-22")
    args = parser.parse_args()

    corrections = json.loads(Path(args.corrected_ids).read_text()) if args.corrected_ids else {}
    rows = [json.loads(line) for line in Path(args.draft_labels).read_text(encoding="utf-8").splitlines() if line.strip()]
    out_rows, counts = [], {}
    for row in rows:
        key = str(row["pilot_index"])
        if key in corrections:
            fix = corrections[key]
            row = {**row, **{k: v for k, v in fix.items() if k in ("decision", "label", "notes")}}
            row["correction"] = fix
        decision = row["decision"]
        label = row["label"]
        if decision not in ("include", "exclude"):
            raise SystemExit(f"row {row['sample_id']}: invalid decision {decision!r}")
        if decision == "include" and label not in ("0", "1", 0, 1):
            raise SystemExit(f"row {row['sample_id']}: include needs label 0/1")
        counts[decision if decision == "exclude" else f"include-{label}"] = \
            counts.get(decision if decision == "exclude" else f"include-{label}", 0) + 1
        out_rows.append({
            "sample_id": row["sample_id"], "question_id": row["question_id"],
            "decision": decision, "label": (int(label) if decision == "include" else None),
            "human_reviewed": True,
            "label_source": f"human:{args.reviewer}:{args.review_mode}:{args.signed_off_at}",
            "review_mode": args.review_mode,
            "reviewed_at": args.signed_off_at,
            "generated_text_sha256": row["generated_text_sha256"],
            "exclude_reason": row.get("exclude_reason") if decision == "exclude" else None,
            "notes": row.get("notes"), "flags": row.get("flags", []),
            "pilot_index": row["pilot_index"],
        })
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in out_rows) + "\n")
    print(json.dumps({"draft": args.draft_labels, "reviewed": args.out, "rows": len(out_rows),
                      "counts": counts, "reviewer": args.reviewer, "review_mode": args.review_mode},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
