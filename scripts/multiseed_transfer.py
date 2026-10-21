#!/usr/bin/env python
"""Multi-seed robustness of the main-project transfer matrix (CPU only).

The committed matrix uses one seed. This script re-runs every source/target/feature-set/kind
cell for several seeds and reports per-seed metrics plus mean [min,max], so the transfer gap
can be read with its seed variability instead of a single draw.

Outputs reports/main_project_multiseed.json (+ .csv) and writes nothing to the tracked matrix.
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
from src.detectors import evaluate_transfer  # noqa: E402

SEEDS = (42, 43, 44, 45, 46)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(REPO / "results/stage7/features_combined.parquet"))
    parser.add_argument("--out", default=str(REPO / "reports/main_project_multiseed.json"))
    parser.add_argument("--seeds", type=int, nargs="+", default=list(SEEDS))
    parser.add_argument("--bootstrap", type=int, default=500)
    parser.add_argument("--feature-sets", nargs="+", default=["entropy_raw", "relative_normalized"])
    parser.add_argument("--kinds", nargs="+", default=["lr", "mlp"])
    args = parser.parse_args()

    frame = pd.read_parquet(args.features)
    frames = []
    for seed in args.seeds:
        result = evaluate_transfer(frame, feature_sets=tuple(args.feature_sets), kinds=tuple(args.kinds),
                                   repeats=args.bootstrap, seed=seed, axis="model")
        table = result[0] if isinstance(result, tuple) else result
        table = table.copy()
        table["seed"] = seed
        frames.append(table)
        print(f"seed {seed}: {len(table)} cells", flush=True)
    all_rows = pd.concat(frames, ignore_index=True)

    keys = ["axis", "source", "target", "dataset", "feature_set", "kind"]
    grouped = all_rows.groupby(keys, dropna=False)
    metrics = ["auroc", "auprc", "f1", "brier", "ece", "transfer_cost_auroc"]
    summary = []
    for key, group in grouped:
        row = dict(zip(keys, key if isinstance(key, tuple) else (key,)))
        for metric in metrics:
            values = ([v for v in group[metric].tolist() if v is not None and not pd.isna(v)]
                      if metric in group.columns else [])
            if values:
                row[f"{metric}_mean"] = float(np.mean(values))
                row[f"{metric}_min"] = float(np.min(values))
                row[f"{metric}_max"] = float(np.max(values))
                row[f"{metric}_std"] = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
            else:
                row[f"{metric}_mean"] = None
        row["seeds"] = int(group["seed"].nunique())
        summary.append(row)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {"features": args.features, "seeds": args.seeds, "bootstrap": args.bootstrap,
               "cells": summary, "notes": [
                   "same feature file as the committed single-seed matrix; only the fitting seed changes",
                   "transfer_cost_auroc is the in-domain reference minus the transfer AUROC on the same target test set",
                   "seed spread is reported as mean/min/max/std; it is not a confidence interval",
               ]}
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    pd.DataFrame(summary).to_csv(out.with_suffix(".csv"), index=False)
    cross = [row for row in summary if row["source"] != row["target"] and row.get("auroc_mean") is not None]
    in_domain = [row for row in summary if row["source"] == row["target"] and row.get("auroc_mean") is not None]
    print(f"cells={len(summary)} in-domain={len(in_domain)} cross={len(cross)}")
    for row in sorted(in_domain + cross, key=lambda r: -(r.get("auroc_mean") or 0))[:8]:
        print(f"  {row['source'][:22]:22s}->{row['target'][:22]:22s} {row['feature_set']:20s} {row['kind']:3s} "
              f"AUROC {row['auroc_mean']:.4f} [{row['auroc_min']:.4f},{row['auroc_max']:.4f}] std {row['auroc_std']:.4f}")
    print("wrote", out, "and", out.with_suffix(".csv"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
