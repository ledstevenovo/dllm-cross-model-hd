#!/usr/bin/env python
"""Cluster permutation test for the main-project transfer matrix (CPU).

The TRE reproduction has a permutation null (``scripts/tre_repro/permutation_test.py``,
p=1e-4) but the main transfer matrix never had one: its 16 cells were reported with
bootstrap CIs only.  A CI answers "how much would this AUROC move under resampling",
which is a different question from "could a number this far from 0.5 have arisen with
random labels".  This adds the second.

Method: for each (source, feature_set, kind, target) cell the fitted detector is held
fixed and the target test *labels* are permuted, whole question clusters moving
together (clusters are the resampling unit everywhere else in this project).  AUROC is
recomputed on each permutation; the empirical p-value is one-sided,
``(#{null >= observed} + 1) / (permutations + 1)``, matching the TRE script.

Permuting labels rather than refitting matters: refitting would confound "the signal
isn't there" with "the fit is unstable".  The detector that produced the observed
number is the one being tested.

Output: ``reports/main_project_permutation.json``.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
sys.path.insert(0, str(REPO))
from src.evaluation import binary_metrics  # noqa: E402

PERMUTATIONS = 10000


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", default=str(REPO / "results/stage7/main/predictions.csv"))
    parser.add_argument("--out", default=str(REPO / "reports/main_project_permutation.json"))
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    frame = pd.read_csv(args.predictions)
    frame = frame[frame.label.isin(["correct", "incorrect"])].copy()
    frame["y"] = frame.label.eq("incorrect").astype(int)
    rng = np.random.default_rng(args.seed)

    cells = []
    keys = ["source", "target", "feature_set", "kind"]
    for (source, target, feature_set, kind), cell in frame.groupby(keys, sort=True):
        y = cell.y.to_numpy()
        score = cell.score.to_numpy()
        observed = binary_metrics(y, score)["auroc"]
        if observed is None:
            continue

        # Cluster-level permutation: shuffle cluster labels, then expand back to rows.
        clusters = cell.question_id.to_numpy()
        unique = sorted(set(clusters))
        index = {name: i for i, name in enumerate(unique)}
        cluster_ids = np.asarray([index[name] for name in clusters])
        # A cluster is label-pure when all its rows share a label; only then can the
        # whole-cluster shuffle be done on one label per cluster.
        cluster_label = np.full(len(unique), -1, dtype=int)
        pure = True
        for name, i in index.items():
            values = y[clusters == name]
            if len(set(values.tolist())) == 1:
                cluster_label[i] = int(values[0])
            else:
                pure = False
                break

        null = []
        for _ in range(args.permutations):
            if pure:
                permuted = cluster_label[rng.permutation(len(unique))][cluster_ids]
            else:
                permuted = rng.permutation(y)
            if len(np.unique(permuted)) < 2:
                continue
            value = binary_metrics(permuted, score)["auroc"]
            if value is not None:
                null.append(value)
        null = np.asarray(null)
        p_value = float((np.sum(null >= observed) + 1) / (len(null) + 1))
        cells.append({
            "source": source.split("/")[-1],
            "target": target.split("/")[-1],
            "feature_set": feature_set,
            "kind": kind,
            "n": int(len(cell)),
            "positive": int(y.sum()),
            "negative": int(len(y) - y.sum()),
            "clusters": int(len(unique)),
            "observed_auroc": float(observed),
            "permutations_valid": int(len(null)),
            "permutation_mode": "cluster" if pure else "row",
            "null_mean": float(null.mean()),
            "null_p95": float(np.percentile(null, 95)),
            "null_max": float(null.max()),
            "p_value_one_sided": p_value,
        })
        print(f"{source.split('/')[-1][:6]:>6} -> {target.split('/')[-1][:6]:<6} {feature_set:18s} {kind:3s} "
              f"AUROC {observed:.3f} | null mean {null.mean():.3f} p95 {np.percentile(null,95):.3f} "
              f"| p = {p_value:.4g}", flush=True)

    payload = {
        "predictions": str(args.predictions),
        "seed": args.seed,
        "permutations_requested": args.permutations,
        "notes": [
            "the fitted detector is held fixed; only the target test labels are permuted",
            "cluster permutation is used when every question cluster is label-pure, row permutation otherwise",
            "empirical p is one-sided (observed >= null); p is bounded below by 1/(permutations+1)",
        ],
        "cells": cells,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(cells)} cells)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
