#!/usr/bin/env python
"""Paired comparison on the questions every direction shares (CPU).

The four cells of the transfer matrix do not have the same test set: LLaDA has 48
eligible test questions, Dream 45, because format_failure exclusions differ per
model.  Comparing their AUROCs directly therefore mixes a real effect with a
sample-composition difference.

This restricts all four directions to the questions that appear in every one of
them (44 of them) and recomputes each cell on that common set.  The detectors are
the already-fitted ones from the main run -- no refitting, so what changes is only
which rows are scored.

Output: ``reports/main_paired_comparison.json`` and a Markdown table on stdout.
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
from src.evaluation import binary_metrics, grouped_bootstrap  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", default=str(REPO / "results/stage7/main/predictions.csv"))
    parser.add_argument("--out", default=str(REPO / "reports/main_paired_comparison.json"))
    parser.add_argument("--bootstrap", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    frame = pd.read_csv(args.predictions)
    frame = frame[frame.label.isin(["correct", "incorrect"])].copy()
    frame["y"] = frame.label.eq("incorrect").astype(int)

    per_direction = {key: set(cell.question_id) for key, cell in frame.groupby(["source", "target"])}
    common = set.intersection(*per_direction.values())
    subset = frame[frame.question_id.isin(common)].copy()

    cells = []
    for (source, target, feature_set, kind), cell in subset.groupby(
            ["source", "target", "feature_set", "kind"], sort=True):
        y = cell.y.to_numpy()
        score = cell.score.to_numpy()
        metrics = binary_metrics(y, score)
        if metrics["auroc"] is None:
            continue
        interval = grouped_bootstrap(y, score, cell.question_id, repeats=args.bootstrap, seed=args.seed)
        cells.append({
            "source": source.split("/")[-1],
            "target": target.split("/")[-1],
            "feature_set": feature_set,
            "kind": kind,
            "n": int(len(cell)),
            "positive": int(y.sum()),
            "negative": int(len(y) - y.sum()),
            "auroc": float(metrics["auroc"]),
            "auroc_low": interval.get("auroc_low"),
            "auroc_high": interval.get("auroc_high"),
        })
        print(f"{source.split('/')[-1][:6]:>6} -> {target.split('/')[-1][:6]:<6} {feature_set:18s} {kind:3s} "
              f"AUROC {metrics['auroc']:.3f} [{interval.get('auroc_low'):.2f},{interval.get('auroc_high'):.2f}] "
              f"n={len(cell)} pos={int(y.sum())} neg={int(len(y) - y.sum())}", flush=True)

    payload = {
        "predictions": str(args.predictions),
        "seed": args.seed,
        "bootstrap_repeats": args.bootstrap,
        "common_questions": len(common),
        "direction_sizes": {f"{k[0].split('/')[-1]}->{k[1].split('/')[-1]}": len(v)
                            for k, v in per_direction.items()},
        "notes": [
            "all four directions restricted to the questions they all have in common",
            "detectors are the fitted ones from the main run; nothing is refitted",
            "reported n is per direction, so each direction sees the same questions but may label them differently (each model answers for itself)",
        ],
        "cells": cells,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
