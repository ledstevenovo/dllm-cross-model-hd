#!/usr/bin/env python
"""Learning curve: how the anomaly cell's AUROC behaves as the test set grows.

The pilot200 result said rel+LR Dream->LLaDA was at chance (0.494).  On 2000
questions the same cell is 0.752.  This script shows *why* by recomputing the cell at
a range of test-set sizes drawn from the same expanded pool, so the reader sees the
estimate wander rather than having to take "small sample" on faith.

Two panels, both on the same fitted detector (fit never changes, only the scoring
subset does -- refitting per size would conflate sample size with fit variance):

1. **Test-set size sweep**: score the first N test questions (by cluster, so a
   cluster is never split) for N in a geometric ladder up to the full set.  Reports
   the AUROC and its cluster-bootstrap CI at each N.
2. **The pilot200 draw**: 2000 resamples of 48 test questions, giving the distribution
   of the estimate at exactly the pilot200 test size.  Where does the observed 0.494
   sit in that distribution?  If the true value is ~0.75, ~0.494 should appear in the
   lower tail rather than being typical -- which is what "small sample" predicts.

Output: ``reports/pool2000_learning_curve.json``.
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
from src.detectors import FEATURE_SETS, fit_source  # noqa: E402
from src.evaluation import binary_metrics, grouped_bootstrap  # noqa: E402

DREAM = "Dream-org/Dream-v0-Instruct-7B"
LLADA = "GSAI-ML/LLaDA-8B-Instruct"
SIZES = (24, 48, 96, 192, 288, 384, 491)
PILOT_N = 48
PILOT_AUROC = 0.4941  # observed on pilot200, for reference


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(REPO / "results/pool2000/features_combined.parquet"))
    parser.add_argument("--feature-set", default="relative_normalized")
    parser.add_argument("--kind", default="lr")
    parser.add_argument("--source", default=DREAM)
    parser.add_argument("--target", default=LLADA)
    parser.add_argument("--resamples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default=str(REPO / "reports/pool2000_learning_curve.json"))
    args = parser.parse_args()

    frame = pd.read_parquet(args.features)
    frame = frame[frame.human_reviewed & frame.label.isin(["correct", "incorrect"])].copy()
    columns = FEATURE_SETS[args.feature_set]

    train = frame[(frame.model_id == args.source) & (frame.split == "train")]
    dev = frame[(frame.model_id == args.source) & (frame.split == "validation")]
    test = frame[(frame.model_id == args.target) & (frame.split == "test")].reset_index(drop=True)
    model, threshold, _ = fit_source(train, dev, columns, args.kind, args.seed, True)

    test["score"] = model.predict_proba(test[columns])[:, 1]
    test["y"] = test.label.eq("incorrect").astype(int)
    if test.y.nunique() < 2:
        raise SystemExit("target test set has a single class")

    full = binary_metrics(test.y.to_numpy(), test.score.to_numpy())["auroc"]
    print(f"full test n={len(test)} AUROC={full:.4f}")

    # --- panel 1: fixed detector, growing test subset -----------------------
    # Draw whole clusters so the subset never splits a cluster across sizes.
    clusters = sorted(test.cluster_id.unique())
    rng = np.random.default_rng(args.seed)
    order = list(rng.permutation(clusters))
    sweep = []
    for size in SIZES:
        if size > len(test):
            continue
        # cumulate clusters until at least `size` test rows are covered
        picked, rows = [], 0
        for cluster in order:
            picked.append(cluster)
            rows = int(test.cluster_id.isin(picked).sum())
            if rows >= size:
                break
        subset = test[test.cluster_id.isin(picked)]
        if subset.y.nunique() < 2:
            continue
        y = subset.y.to_numpy()
        score = subset.score.to_numpy()
        metrics = binary_metrics(y, score)
        interval = grouped_bootstrap(y, score, subset.question_id, repeats=1000, seed=args.seed)
        sweep.append({
            "requested": size, "n": int(len(subset)), "clusters": len(picked),
            "positive": int(y.sum()), "negative": int(len(y) - y.sum()),
            "auroc": float(metrics["auroc"]),
            "auroc_low": interval.get("auroc_low"), "auroc_high": interval.get("auroc_high"),
        })
        print(f"  n={len(subset):3d} AUROC {metrics['auroc']:.3f} "
              f"[{interval.get('auroc_low'):.2f},{interval.get('auroc_high'):.2f}] "
              f"pos={int(y.sum())} neg={int(len(y) - y.sum())}")

    # --- panel 2: the pilot200 test size ------------------------------------
    draws = []
    for _ in range(args.resamples):
        picked = rng.choice(len(test), size=min(PILOT_N, len(test)), replace=False)
        subset = test.iloc[picked]
        if subset.y.nunique() < 2:
            continue
        value = binary_metrics(subset.y.to_numpy(), subset.score.to_numpy())["auroc"]
        if value is not None:
            draws.append(value)
    draws = np.asarray(draws)
    percentile = float((draws <= PILOT_AUROC).mean())

    payload = {
        "features": str(args.features),
        "cell": {"source": args.source, "target": args.target,
                 "feature_set": args.feature_set, "kind": args.kind},
        "seed": args.seed,
        "full": {"n": int(len(test)), "auroc": float(full),
                 "positive": int(test.y.sum()), "negative": int(len(test) - test.y.sum())},
        "sweep": sweep,
        "pilot_size_distribution": {
            "n_per_draw": PILOT_N, "resamples": int(len(draws)),
            "mean": float(draws.mean()), "std": float(draws.std()),
            "p05": float(np.percentile(draws, 5)), "p25": float(np.percentile(draws, 25)),
            "median": float(np.percentile(draws, 50)),
            "p75": float(np.percentile(draws, 75)), "p95": float(np.percentile(draws, 95)),
            "min": float(draws.min()), "max": float(draws.max()),
            "observed_pilot200": PILOT_AUROC,
            "observed_percentile": percentile,
        },
        "notes": [
            "the detector is fitted once and never refitted, so only the scoring subset changes",
            "clusters are drawn whole, matching the resampling unit used everywhere else",
            "the pilot-size distribution answers: how often would a 48-question test set have shown 0.494?",
        ],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    d = payload["pilot_size_distribution"]
    print(f"\nat n={PILOT_N}: mean {d['mean']:.3f} sd {d['std']:.3f} "
          f"[p05 {d['p05']:.3f}, p95 {d['p95']:.3f}]")
    print(f"pilot200's 0.494 sits at percentile {d['observed_percentile']*100:.1f}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
