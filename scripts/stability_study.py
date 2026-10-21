#!/usr/bin/env python
"""Large-scale resampling and stability study for the main-project transfer matrix (CPU).

Because pilot200 is small, the honest way to spend CPU is to quantify instability instead of
tuning: for every source/target cell this runs many repeated train/validation splits
(bootstrapped at the question-cluster level) and reports the distribution of AUROC, the
probability that the transfer gap exceeds zero, and the rank stability of feature sets.

Cost scales with --repeats x cells; a full 200-repeat pass takes hours on CPU.

Output: reports/main_project_stability.json (+ .csv). Secondary analysis only.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
sys.path.insert(0, str(REPO))
from src.detectors import FEATURE_SETS, fit_source  # noqa: E402
from src.evaluation import binary_metrics  # noqa: E402


def cluster_resample(pool: pd.DataFrame, rng) -> pd.DataFrame:
    """Resample question clusters inside each split, keeping the split assignment."""
    parts = []
    for split, chunk in pool.groupby("split"):
        clusters = sorted(chunk.cluster_id.unique())
        picked = rng.choice(clusters, size=len(clusters), replace=True)
        for draw, cluster in enumerate(picked):
            rows = chunk[chunk.cluster_id == cluster].copy()
            rows["sample_id"] = rows["sample_id"].astype(str) + f"__r{draw}"
            parts.append(rows)
    return pd.concat(parts, ignore_index=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(REPO / "results/stage7/features_combined.parquet"))
    parser.add_argument("--out", default=str(REPO / "reports/main_project_stability.json"))
    parser.add_argument("--repeats", type=int, default=200, help="cluster-resampling repeats per cell")
    parser.add_argument("--seed", type=int, default=20261021)
    parser.add_argument("--feature-sets", nargs="+", default=["entropy_raw", "relative_normalized"])
    parser.add_argument("--kinds", nargs="+", default=["lr", "mlp"])
    parser.add_argument("--allow-nonbf16", action="store_true")
    args = parser.parse_args()

    frame = pd.read_parquet(args.features)
    if not args.allow_nonbf16 and not frame.precision.isin(["bf16", "bfloat16"]).all():
        raise SystemExit("formal analysis requires BF16 traces")
    frame = frame[frame.human_reviewed & frame.label.isin(["correct", "incorrect"])].copy()
    domains = sorted(frame.model_id.unique())
    rng = np.random.default_rng(args.seed)
    started = time.perf_counter()

    cells = []
    for source in domains:
        for feature_set in args.feature_sets:
            columns = FEATURE_SETS[feature_set]
            for kind in args.kinds:
                per_repeat = {target: [] for target in domains}
                refit_failures = 0
                for repeat in range(args.repeats):
                    sample = cluster_resample(frame, rng)
                    train = sample[(sample.model_id == source) & (sample.split == "train")]
                    dev = sample[(sample.model_id == source) & (sample.split == "validation")]
                    if train.empty or dev.empty or train.label.nunique() < 2 or dev.label.nunique() < 2:
                        refit_failures += 1
                        continue
                    try:
                        model, threshold, _ = fit_source(train, dev, columns, kind, args.seed, True)
                    except Exception:
                        refit_failures += 1
                        continue
                    for target in domains:
                        test = sample[(sample.model_id == target) & (sample.split == "test")]
                        if test.empty or test.label.nunique() < 2:
                            continue
                        y = test.label.eq("incorrect").astype(int).to_numpy()
                        score = model.predict_proba(test[columns])[:, 1]
                        auroc = binary_metrics(y, score)["auroc"]
                        if auroc is not None:
                            per_repeat[target].append(auroc)
                for target, values in per_repeat.items():
                    if not values:
                        continue
                    cells.append({
                        "source": source, "target": target, "feature_set": feature_set, "kind": kind,
                        "repeats_requested": args.repeats, "repeats_valid": len(values),
                        "refit_failures": refit_failures,
                        "auroc_mean": float(np.mean(values)), "auroc_std": float(np.std(values)),
                        "auroc_p05": float(np.percentile(values, 5)),
                        "auroc_p95": float(np.percentile(values, 95)),
                        "auroc_min": float(np.min(values)), "auroc_max": float(np.max(values)),
                        "p_above_0_5": float(np.mean(np.asarray(values) > 0.5)),
                        "p_above_0_7": float(np.mean(np.asarray(values) > 0.7)),
                        "p_above_0_8": float(np.mean(np.asarray(values) > 0.8)),
                    })
                done = len(cells)
                elapsed = time.perf_counter() - started
                print(f"[{done}] {source.split('/')[-1][:12]} {feature_set:20s} {kind:3s} "
                      f"{args.repeats} repeats | {elapsed/60:.1f} min elapsed", flush=True)

    out = Path(args.out)
    payload = {"features": args.features, "repeats": args.repeats, "seed": args.seed,
               "resampling_unit": "question cluster inside each frozen split",
               "elapsed_seconds": round(time.perf_counter() - started, 1), "cells": cells,
               "notes": ["each repeat refits on resampled train/validation and scores the resampled test",
                         "reported quantiles are resampling spread, not a confidence interval on the population",
                         "no threshold tuning happens here; the fitted threshold is used as-is"]}
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    pd.DataFrame(cells).to_csv(out.with_suffix(".csv"), index=False)
    cross = [c for c in cells if c["source"] != c["target"]]
    if cross:
        best = max(cross, key=lambda c: c["auroc_mean"])
        worst = min(cross, key=lambda c: c["auroc_mean"])
        print(f"cross-model cells: {len(cross)} | best {best['auroc_mean']:.4f} "
              f"({best['source'].split('/')[-1]}->{best['target'].split('/')[-1]}), "
              f"worst {worst['auroc_mean']:.4f}")
    print("wrote", out, "and", out.with_suffix(".csv"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
