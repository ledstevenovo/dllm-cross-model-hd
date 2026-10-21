#!/usr/bin/env python
"""Apply human-reviewed labels to read-only raw/merged traces -> valid/ (+ excluded/).

Raw files are never modified: hashes are verified unchanged before and after. Labels bind to
the judged answer through ``generated_text_sha256``; a mismatch fails the item.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR.parents[1] / "references/repos/DynHD"))
import common  # noqa: E402
import torch  # noqa: E402
from dynhd.data.io import load_trace  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset", required=True, help="frozen subset jsonl (pilot_index source)")
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--labels-file", required=True)
    parser.add_argument("--valid-dir", required=True)
    parser.add_argument("--excluded-dir", required=True)
    parser.add_argument("--report")
    args = parser.parse_args()

    rows = [json.loads(line) for line in Path(args.subset).read_text(encoding="utf-8").splitlines() if line.strip()]
    subset_index = {row["sample_id"]: (position, row) for position, row in enumerate(rows)}
    labels = {}
    for line in Path(args.labels_file).read_text(encoding="utf-8").splitlines():
        if line.strip():
            label = json.loads(line)
            key = label.get("sample_id") or label.get("question_id")
            labels[key] = label

    raw_dir = Path(args.raw_dir).resolve()
    valid_dir = Path(args.valid_dir); excluded_dir = Path(args.excluded_dir)
    valid_dir.mkdir(parents=True, exist_ok=True); excluded_dir.mkdir(parents=True, exist_ok=True)
    before = {path.name: common.sha256_file(path) for path in sorted(raw_dir.glob("*.pt"))}
    included, excluded, problems = [], [], []
    for name, raw_hash in before.items():
        path = raw_dir / name
        data = load_trace(str(path))
        meta = dict(data.get("meta", {}))
        sample_id = str(meta.get("id"))
        entry = subset_index.get(sample_id)
        if entry is None:
            problems.append(f"{name}: sample_id {sample_id} not in subset")
            continue
        pilot_index, row = entry
        label_row = labels.get(sample_id) or labels.get(row["question_id"])
        if label_row is None:
            problems.append(f"{name}: no reviewed label for {sample_id}")
            continue
        if label_row.get("human_reviewed") is not True:
            problems.append(f"{name}: reviewed label lacks human_reviewed=true")
            continue
        expected = label_row.get("generated_text_sha256")
        if expected and expected != common.sha256_text(str(meta.get("generated_text", ""))):
            problems.append(f"{name}: label/answer hash mismatch (refusing to apply)")
            continue
        decision = str(label_row.get("decision", "include"))
        meta["human_reviewed"] = True
        meta["provisional"] = False
        meta["label_source"] = str(label_row.get("label_source", "human:unknown"))
        meta["reviewed_at"] = label_row.get("reviewed_at", common.utc_now())
        meta["reviewed_answer_sha256"] = expected or common.sha256_text(str(meta.get("generated_text", "")))
        meta["source_raw_file"] = name
        meta["source_raw_sha256"] = raw_hash
        target_dir = valid_dir if decision == "include" else excluded_dir
        if decision == "include":
            label = int(label_row.get("label", -1))
            if label not in (0, 1):
                problems.append(f"{name}: include decision needs label 0/1")
                continue
            included.append(sample_id)
        else:
            label = int(data.get("label", 1))
            meta["excluded_reason"] = str(label_row.get("exclude_reason", "unspecified"))
            excluded.append(sample_id)
        target = target_dir / f"{pilot_index:06d}.pt"
        payload = {"features": data["features"], "label": label, "meta": meta, "prompt_emb": data.get("prompt_emb")}
        torch.save(payload, target)
        load_trace(str(target))  # reload validation

    after = {path.name: common.sha256_file(path) for path in sorted(raw_dir.glob("*.pt"))}
    raw_changed = [name for name in before if before[name] != after.get(name)] or [n for n in after if n not in before]
    if raw_changed:
        problems.append(f"raw files changed during relabel: {raw_changed[:5]}")
    report = {"raw_dir": str(raw_dir), "valid_dir": str(valid_dir), "excluded_dir": str(excluded_dir),
              "raw_files": len(before), "included": len(included), "excluded": len(excluded),
              "raw_unchanged": not raw_changed, "problems": problems, "ok": not problems}
    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "problems"}, indent=2, ensure_ascii=False))
    for problem in problems[:10]:
        print(" !", problem)
    print("relabel:", "OK" if not problems else "FAILED")
    return 0 if not problems else 2


if __name__ == "__main__":
    raise SystemExit(main())
