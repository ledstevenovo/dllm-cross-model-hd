#!/usr/bin/env python
"""Label-permutation null test for the TRE scores (CPU).

Answers: "could an AUROC this high arise by chance given 507/800 positives?" The labels are
shuffled within the frozen question set (question-clustered: whole clusters move together),
the score is held fixed, and AUROC is recomputed. Reports the empirical p-value and the null
quantiles. This is a significance check on the existing scores, not a new metric.

Output: reports/tre_repro/permutation_test.json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(REPO))
from src.evaluation import binary_metrics  # noqa: E402

PERMUTATIONS = 10000


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scores", default=str(REPO / "results/tre_repro/llada_triviaqa_fp16_L128_S64_B128_v3/scores.csv"))
    parser.add_argument("--out", default=str(REPO / "reports/tre_repro/permutation_test.json"))
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--seed", type=int, default=20261021)
    parser.add_argument("--scores-columns", nargs="+", default=["tre", "tre_effective", "tre_length_normalized"])
    args = parser.parse_args()

    rows = [row for row in csv.DictReader(open(args.scores)) if row["status"] == "kept"]
    labels = np.asarray([1 if row["label"] == "incorrect" else 0 for row in rows])
    clusters = np.asarray([row["cluster_id"] for row in rows])
    unique = sorted(set(clusters))
    cluster_index = {name: index for index, name in enumerate(unique)}
    cluster_ids = np.asarray([cluster_index[name] for name in clusters])
    cluster_labels = {}
    for cluster in unique:
        values = labels[clusters == cluster]
        cluster_labels[cluster_index[cluster]] = int(values[0]) if len(set(values)) == 1 else -1

    rng = np.random.default_rng(args.seed)
    results = {}
    for column in args.scores_columns:
        scores = np.asarray([float(row[column]) for row in rows])
        observed = binary_metrics(labels, scores)["auroc"]
        null = []
        pure = all(value >= 0 for value in cluster_labels.values()) and len(unique) < len(rows)
        for _ in range(args.permutations):
            if pure:
                shuffled = np.asarray([cluster_labels[i] for i in rng.permutation(len(unique))])
                permuted = shuffled[cluster_ids]
            else:
                permuted = rng.permutation(labels)
            if len(np.unique(permuted)) < 2:
                continue
            null.append(binary_metrics(permuted, scores)["auroc"])
        null = np.asarray(null)
        p_value = float((np.sum(null >= observed) + 1) / (len(null) + 1)) if observed is not None else None
        results[column] = {
            "observed_auroc": observed, "permutations_requested": args.permutations,
            "permutations_valid": int(len(null)), "permutation_mode": "cluster" if pure else "row",
            "p_value_one_sided": p_value,
            "null_mean": float(null.mean()), "null_p95": float(np.percentile(null, 95)),
            "null_p99": float(np.percentile(null, 99)), "null_max": float(null.max()),
        }
        print(f"{column:26s} AUROC {observed:.4f} | null mean {null.mean():.4f} p95 {np.percentile(null,95):.4f} "
              f"| p = {p_value:.4g}", flush=True)

    payload = {"scores": args.scores, "n": len(rows), "positive": int(labels.sum()),
               "seed": args.seed, "results": results,
               "notes": ["labels are permuted, scores are held fixed",
                         "cluster permutation is used when every cluster is label-pure",
                         "empirical p is one-sided (observed >= null)"]}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
