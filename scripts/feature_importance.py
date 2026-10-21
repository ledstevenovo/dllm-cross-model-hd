#!/usr/bin/env python
"""Permutation importance + leave-one-feature-out ablations for the main-project detectors.

CPU only. For every source/target cell and feature set it reports
  - full-feature AUROC
  - leave-one-feature-out AUROC delta (which evidence actually carries the signal)
  - permutation importance (AUROC drop when one column is shuffled, 20 repeats)
  - a 200-draw bootstrap CI on the full-feature AUROC

Output: reports/main_project_importance.json (+ .csv). Secondary analysis only.
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
from src.detectors import FEATURE_SETS, eligible, fit_source  # noqa: E402
from src.evaluation import binary_metrics, grouped_bootstrap  # noqa: E402

PERMUTATIONS = 20
BOOTSTRAP = 200


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(REPO / "results/stage7/features_combined.parquet"))
    parser.add_argument("--out", default=str(REPO / "reports/main_project_importance.json"))
    parser.add_argument("--feature-sets", nargs="+", default=["entropy_raw", "relative_normalized"])
    parser.add_argument("--kind", default="lr")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    frame = pd.read_parquet(args.features)
    reviewed = eligible(frame)
    domains = sorted(frame.model_id.unique())
    rng = np.random.default_rng(args.seed)
    cells = []

    for source in domains:
        train = reviewed[(reviewed.model_id == source) & (reviewed.split == "train")]
        dev = reviewed[(reviewed.model_id == source) & (reviewed.split == "validation")]
        for feature_set in args.feature_sets:
            columns = FEATURE_SETS[feature_set]
            model, threshold, _ = fit_source(train, dev, columns, args.kind, args.seed, True)
            for target in domains:
                test = reviewed[(reviewed.model_id == target) & (reviewed.split == "test")]
                if test.empty:
                    continue
                y = test.label.eq("incorrect").astype(int).to_numpy()
                base_score = model.predict_proba(test[columns])[:, 1]
                base = binary_metrics(y, base_score, threshold, True)
                base.update(grouped_bootstrap(y, base_score, test.question_id, repeats=BOOTSTRAP, seed=args.seed))
                loo = {}
                for column in columns:
                    reduced = [c for c in columns if c != column]
                    if not reduced:
                        continue
                    m2, _, _ = fit_source(train, dev, reduced, args.kind, args.seed, True)
                    s2 = m2.predict_proba(test[reduced])[:, 1]
                    auroc = binary_metrics(y, s2)["auroc"]
                    loo[column] = {"auroc": auroc,
                                   "delta": (auroc - base["auroc"]) if auroc is not None and base["auroc"] is not None else None}
                perm = {}
                for column in columns:
                    drops = []
                    for _ in range(PERMUTATIONS):
                        shuffled = test[columns].copy()
                        shuffled[column] = rng.permutation(shuffled[column].to_numpy())
                        score = model.predict_proba(shuffled)[:, 1]
                        auroc = binary_metrics(y, score)["auroc"]
                        if auroc is not None and base["auroc"] is not None:
                            drops.append(base["auroc"] - auroc)
                    perm[column] = {"mean_drop": float(np.mean(drops)) if drops else None,
                                    "std_drop": float(np.std(drops)) if drops else None,
                                    "repeats": len(drops)}
                cells.append({"source": source, "target": target, "feature_set": feature_set,
                              "kind": args.kind, "n": base["n"], "base": base,
                              "leave_one_out": loo, "permutation": perm})
                print(f"{source.split('/')[-1][:14]} -> {target.split('/')[-1][:14]} {feature_set:20s} "
                      f"AUROC {base['auroc']:.4f} | top drop: "
                      f"{max(perm.items(), key=lambda kv: kv[1]['mean_drop'] or 0)[0] if perm else '-'}", flush=True)

    payload = {"features": args.features, "kind": args.kind, "seed": args.seed,
               "permutations": PERMUTATIONS, "bootstrap": BOOTSTRAP, "cells": cells,
               "notes": ["leave-one-out refits the detector without one feature",
                         "permutation shuffles one column in the target test set",
                         "both are secondary analyses; the committed matrix stays the main table"]}
    out = Path(args.out)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    rows = []
    for cell in cells:
        for column, values in cell["leave_one_out"].items():
            rows.append({"source": cell["source"], "target": cell["target"],
                         "feature_set": cell["feature_set"], "kind": cell["kind"],
                         "feature": column, "loo_auroc": values["auroc"], "loo_delta": values["delta"],
                         "perm_mean_drop": cell["permutation"].get(column, {}).get("mean_drop"),
                         "base_auroc": cell["base"]["auroc"]})
    pd.DataFrame(rows).to_csv(out.with_suffix(".csv"), index=False)
    print("wrote", out, "and", out.with_suffix(".csv"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
