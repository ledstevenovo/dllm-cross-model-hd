#!/usr/bin/env python
"""Promote assistant/draft label files to reviewed labels under an adopted rule.

Keeps every original field (candidate, matched_answer, notes, refusal flags, ...) and only
rewrites the provenance fields, so the audit trail shows what the human approved and what the
machine proposed. Labels must already use the project vocabulary.

  correct | incorrect                                    -> eligible factual labels
  refusal_empty | incomplete_truncated | format_failure   -> abstain (kept, not eligible)
  needs_review                                            -> kept for re-review only
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

VOCABULARY = ("correct", "incorrect", "refusal_empty", "incomplete_truncated", "format_failure", "needs_review")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--review-mode", default="rule-signoff", choices=["rule-signoff", "item-by-item"])
    parser.add_argument("--signed-off-at", default="2026-10-22")
    parser.add_argument("--notes-suffix", default="")
    args = parser.parse_args()

    rows = [json.loads(line) for line in Path(args.input).read_text(encoding="utf-8").splitlines() if line.strip()]
    out_rows, counts = [], Counter()
    for row in rows:
        label = str(row.get("label", ""))
        if label not in VOCABULARY:
            raise SystemExit(f"{row.get('sample_id')}: label {label!r} outside the project vocabulary")
        counts[label] += 1
        out = dict(row)
        out["human_reviewed"] = True
        out["label_source"] = f"human:{args.reviewer}:{args.review_mode}:{args.signed_off_at}"
        out["review_mode"] = args.review_mode
        out["reviewed_at"] = args.signed_off_at
        out["previous_label_source"] = row.get("label_source")
        if args.notes_suffix and out.get("notes"):
            out["notes"] = f"{out['notes']} | {args.notes_suffix}"
        out_rows.append(out)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in out_rows) + "\n")
    print(json.dumps({"input": args.input, "out": args.out, "rows": len(out_rows),
                      "labels": dict(counts), "reviewer": args.reviewer}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
