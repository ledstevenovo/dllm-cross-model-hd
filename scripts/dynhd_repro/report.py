#!/usr/bin/env python
"""Aggregate DynHD per-ID labels/scores and partition counts (no retraining, no test tuning).

Scores are joined by sample id from a scores jsonl (sample_id + score) produced by the
detector evaluation; thresholds are never re-selected here.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR.parents[1] / "references/repos/DynHD"))
import common  # noqa: E402
from dynhd.data.io import load_trace  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--split")
    parser.add_argument("--index-map")
    parser.add_argument("--scores", help="jsonl with sample_id and score")
    parser.add_argument("--out", required=True)
    parser.add_argument("--experiment-id", default=None)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    files = sorted(data_dir.glob("*.pt"))
    scores = {}
    if args.scores:
        for line in Path(args.scores).read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                scores[str(row["sample_id"])] = float(row["score"])
    rows = []
    for position, path in enumerate(files):
        data = load_trace(str(path))
        meta = data.get("meta", {})
        sample_id = str(meta.get("id"))
        entry = {"position": position, "file": path.name, "sample_id": sample_id,
                 "question_id": meta.get("question_id"), "label": int(data.get("label", -1)),
                 "score": scores.get(sample_id), "answer_sha256": meta.get("answer_sha256"),
                 "generation_fingerprint": meta.get("generation_fingerprint", "").strip() or None}
        rows.append(entry)

    partitions = {}
    if args.split:
        split = json.loads(Path(args.split).read_text())
        for part, indices in split.items():
            parts = [rows[i] for i in indices if 0 <= i < len(rows)]
            counts = {0: sum(1 for r in parts if r["label"] == 0), 1: sum(1 for r in parts if r["label"] == 1)}
            entry = {"n": len(parts), "label0": counts[0], "label1": counts[1]}
            scored = [r for r in parts if r["score"] is not None]
            if scored and counts[0] and counts[1]:
                try:
                    from sklearn.metrics import average_precision_score, roc_auc_score
                    y = [r["label"] for r in scored]
                    s = [r["score"] for r in scored]
                    entry["auroc"] = round(float(roc_auc_score(y, s)), 6)
                    entry["average_precision"] = round(float(average_precision_score(y, s)), 6)
                    entry["scored"] = len(scored)
                except Exception as error:
                    entry["metric_error"] = str(error)
            partitions[part] = entry
    report = {"data_dir": str(data_dir), "files": len(rows), "experiment_id": args.experiment_id,
              "seed": args.seed, "scores_joined": sum(1 for r in rows if r["score"] is not None),
              "partitions": partitions,
              "fingerprints": sorted({r["generation_fingerprint"] for r in rows if r["generation_fingerprint"]}),
              "rows": rows}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2, ensure_ascii=False))
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
