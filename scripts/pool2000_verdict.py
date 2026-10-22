#!/usr/bin/env python
"""Apply the pre-registered decision rule to the expanded transfer matrix.

The rule was written down before the pool2000 trajectories existed
(docs/NOGPU_WORKPLAN.md section 2d, frozen 2026-10-22):

    "directional gap holds" iff
        rel+LR  Dream -> LLaDA  95% CI upper bound < 0.6
        AND
        ent+LR  Dream -> LLaDA  95% CI lower bound > 0.7

Otherwise the result is reported as "not reproduced".

This script does exactly that and nothing else.  It does not look at the point
estimates, does not try alternative feature sets, and does not reweight.  If the
matrix is missing either cell it refuses to answer rather than reporting "false".

Because a bare true/false would hide how close the call was, it also reports, for
context only and clearly marked as *not* part of the decision, where each cell sits
relative to its threshold and what the pre-expansion value was.  The verdict itself
is computed solely from the two CI bounds above.

Output: reports/pool2000_verdict.json, plus a one-line human-readable verdict.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DREAM = "Dream-v0-Instruct-7B"
LLADA = "LLaDA-8B-Instruct"


def find_cell(table: pd.DataFrame, *, source: str, target: str, feature_set: str, kind: str,
              dataset: str = "all") -> dict:
    matches = table[
        table.source.str.contains(source, regex=False)
        & table.target.str.contains(target, regex=False)
        & (table.feature_set == feature_set)
        & (table.kind == kind)
        & (table.dataset == dataset)
    ]
    if len(matches) != 1:
        raise SystemExit(
            f"expected exactly one row for {source}->{target} {feature_set}/{kind} dataset={dataset}, "
            f"found {len(matches)}"
        )
    row = matches.iloc[0]
    return {
        "source": row["source"], "target": row["target"],
        "feature_set": row["feature_set"], "kind": row["kind"],
        "n": int(row["n"]),
        "positive": int(row["positive"]), "negative": int(row["negative"]),
        "auroc": float(row["auroc"]),
        "auroc_low": float(row["auroc_low"]),
        "auroc_high": float(row["auroc_high"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", default=str(ROOT / "results/pool2000/main/transfer_matrix.csv"))
    parser.add_argument("--out", default=str(ROOT / "reports/pool2000_verdict.json"))
    parser.add_argument("--baseline", default=str(ROOT / "results/stage7/main/transfer_matrix.csv"),
                        help="pre-expansion matrix, for context only")
    args = parser.parse_args()

    table = pd.read_csv(args.matrix)
    rel = find_cell(table, source=DREAM, target=LLADA, feature_set="relative_normalized", kind="lr")
    ent = find_cell(table, source=DREAM, target=LLADA, feature_set="entropy_raw", kind="lr")

    # --- the pre-registered decision, unmodified ----------------------------
    rel_ok = rel["auroc_high"] < 0.6
    ent_ok = ent["auroc_low"] > 0.7
    holds = bool(rel_ok and ent_ok)

    # --- context only: everything below is NOT part of the decision ---------
    baseline = None
    baseline_path = Path(args.baseline)
    if baseline_path.exists():
        old = pd.read_csv(baseline_path)
        try:
            baseline = {
                "relative_normalized_lr_dream_to_llada": find_cell(
                    old, source=DREAM, target=LLADA, feature_set="relative_normalized", kind="lr"),
                "entropy_raw_lr_dream_to_llada": find_cell(
                    old, source=DREAM, target=LLADA, feature_set="entropy_raw", kind="lr"),
            }
        except SystemExit:
            baseline = None

    ci_width = {
        "relative_normalized_lr": round(rel["auroc_high"] - rel["auroc_low"], 4),
        "entropy_raw_lr": round(ent["auroc_high"] - ent["auroc_low"], 4),
    }

    payload = {
        "matrix": str(args.matrix),
        "rule": {
            "frozen_at": "2026-10-22 (docs/NOGPU_WORKPLAN.md section 2d)",
            "states": "rel+LR Dream->LLaDA 95% CI upper < 0.6 AND ent+LR Dream->LLaDA 95% CI lower > 0.7",
            "verdict_field": "directional_gap_holds",
        },
        "cells": {"relative_normalized_lr": rel, "entropy_raw_lr": ent},
        "checks": {
            "rel_upper_below_0_6": {"value": rel["auroc_high"], "threshold": 0.6, "passes": rel_ok},
            "ent_lower_above_0_7": {"value": ent["auroc_low"], "threshold": 0.7, "passes": ent_ok},
        },
        "directional_gap_holds": holds,
        "verdict": "reproduced" if holds else "not reproduced",
        "context_only_not_part_of_the_decision": {
            "ci_widths": ci_width,
            "pre_expansion": baseline,
            "note": "reported so a reader can see how far each cell sat from its threshold; "
                    "the verdict above uses only the two CI bounds",
        },
        "notes": [
            "test set is ~450 per direction, so CI width should be about 0.08-0.13 for the reference cells",
            "if either cell is missing the script exits non-zero instead of answering false",
        ],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"rel+LR Dream->LLaDA  {rel['auroc']:.3f} [{rel['auroc_low']:.3f}, {rel['auroc_high']:.3f}] "
          f"n={rel['n']}  upper<0.6: {rel_ok}")
    print(f"ent+LR Dream->LLaDA  {ent['auroc']:.3f} [{ent['auroc_low']:.3f}, {ent['auroc_high']:.3f}] "
          f"n={ent['n']}  lower>0.7: {ent_ok}")
    print(f"VERDICT: {payload['verdict']}  (directional_gap_holds={holds})")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
