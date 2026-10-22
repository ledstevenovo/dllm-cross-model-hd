#!/usr/bin/env python
"""Project the AUROC interval width as a function of test-set size, from the pilot scores.

For each key cell this bootstraps the pilot target-test items (cluster = question) at several
test-set sizes and reports the 95% interval width of the AUROC estimate. This is the test-set
size uncertainty only (models are held fixed at their pilot fit); it is the part the pool
expansion buys, and it assumes the new questions behave like the pilot ones.

Output: reports/expansion_precision.json and a markdown table on stdout.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

KEY_CELLS = [
    ("anomaly: Dream->LLaDA rel+LR", "Dream-org/Dream-v0-Instruct-7B",
     "GSAI-ML/LLaDA-8B-Instruct", "relative_normalized", "lr"),
    ("reference: Dream->LLaDA ent+LR", "Dream-org/Dream-v0-Instruct-7B",
     "GSAI-ML/LLaDA-8B-Instruct", "entropy_raw", "lr"),
    ("LLaDA->Dream rel+LR", "GSAI-ML/LLaDA-8B-Instruct",
     "Dream-org/Dream-v0-Instruct-7B", "relative_normalized", "lr"),
]


def auroc(y: np.ndarray, s: np.ndarray) -> float | None:
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return None
    from scipy.stats import rankdata
    ranks = rankdata(np.concatenate([pos, neg]), method="average")
    rank_sum_pos = ranks[: len(pos)].sum()
    return (rank_sum_pos - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", default=str(ROOT / "results/stage7/main/predictions.csv"))
    parser.add_argument("--sizes", type=int, nargs="+", default=[48, 100, 150, 200, 300])
    parser.add_argument("--repeats", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20261022)
    parser.add_argument("--out", default=str(ROOT / "reports/expansion_precision.json"))
    args = parser.parse_args()

    frame = pd.read_csv(args.predictions)
    rng = np.random.default_rng(args.seed)
    payload = {"source": args.predictions, "repeats": args.repeats, "seed": args.seed,
               "method": "cluster bootstrap of pilot target-test items; models held at pilot fit",
               "cells": {}}
    rows_out = []
    for name, source, target, feature_set, kind in KEY_CELLS:
        cell = frame[(frame.source == source) & (frame.target == target)
                     & (frame.feature_set == feature_set) & (frame.kind == kind)]
        if cell.empty:
            print(f"warning: cell not found: {name}")
            continue
        items = cell[["question_id", "label", "score"]].copy().reset_index(drop=True)
        items["y"] = items.label.eq("incorrect").astype(int)
        y_all = items.y.to_numpy()
        s_all = items.score.to_numpy()
        groups = [g.index.to_numpy() for _, g in items.groupby("question_id")]
        first_item = np.array([g[0] for g in groups])
        singleton_share = sum(1 for g in groups if len(g) == 1) / len(groups)
        observed = auroc(y_all, s_all)
        entry = {"source": source, "target": target, "feature_set": feature_set, "kind": kind,
                 "n_pilot": int(len(items)), "n_clusters_pilot": int(len(groups)),
                 "singleton_cluster_share": singleton_share,
                 "observed_auroc": float(observed), "by_size": {}}
        if singleton_share < 0.95:
            print(f"note: {name}: only {singleton_share:.0%} singleton clusters; "
                  f"projection uses first item per sampled cluster")
        table_row = [name, f"{observed:.3f}", str(len(items))]
        for size in args.sizes:
            gid = rng.integers(0, len(groups), size=(args.repeats, size))
            item_idx = first_item[gid]
            draws = [value for row in item_idx if (value := auroc(y_all[row], s_all[row])) is not None]
            draws = np.array(draws)
            lo, hi = np.percentile(draws, [2.5, 97.5])
            entry["by_size"][str(size)] = {
                "mean": float(draws.mean()), "std": float(draws.std()),
                "p2_5": float(lo), "p97_5": float(hi), "width": float(hi - lo),
                "valid_draws": int(len(draws)),
            }
            table_row += [f"{hi - lo:.3f}"]
        payload["cells"][name] = entry
        rows_out.append(table_row)
    header = ["cell", "observed AUROC", "n pilot"] + [f"width @ n={s}" for s in args.sizes]
    out = Path(args.out)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join(["---"] * len(header)) + "|")
    for row in rows_out:
        print("| " + " | ".join(str(x) for x in row) + " |")
    print("\nwrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
