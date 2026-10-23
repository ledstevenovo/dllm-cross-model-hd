#!/usr/bin/env python
"""TRE vs detector with the length-correlated features removed.

The comparison reported so far is slightly unfair to TRE: normalised TRE has length divided out,
while the detector's ten features include six that correlate with effective_length at |r| > 0.25.
If the detector's advantage comes from that information, removing those features should close the
gap; if it survives, the advantage is genuinely about entropy structure rather than length.

This keeps the same traces, labels, folds and seed, and changes only the feature list.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from src.detectors import FEATURE_SETS, fit_source  # noqa: E402
from src.evaluation import binary_metrics, grouped_bootstrap  # noqa: E402
from tre_vs_detectors import build_frame, cluster_folds, score  # noqa: E402

CORR_LIMIT = 0.25


def length_free_columns(frame: pd.DataFrame, columns: list[str], limit: float) -> tuple[list[str], dict]:
    kept, dropped = [], {}
    for column in columns:
        if column not in frame:
            continue
        series = frame[column].dropna()
        if series.nunique() <= 1:
            dropped[column] = "constant"
            continue
        r = abs(float(np.corrcoef(series, frame.loc[series.index, "effective_length"])[0, 1]))
        if r > limit:
            dropped[column] = round(r, 3)
        else:
            kept.append(column)
    return kept, dropped


def cv_score(frame: pd.DataFrame, columns: list[str], seed: int) -> dict:
    predictions = np.full(len(frame), np.nan)
    for held, trained in cluster_folds(frame.reset_index(drop=True), k=5, seed=seed):
        fit_rows = frame.reset_index(drop=True).iloc[trained]
        if fit_rows.y.nunique() < 2:
            continue
        rng = np.random.default_rng(seed)
        order = rng.permutation(len(fit_rows))
        cut = max(int(0.8 * len(fit_rows)), 2)
        tr, dv = fit_rows.iloc[order[:cut]], fit_rows.iloc[order[cut:]]
        if dv.y.nunique() < 2:
            dv = tr
        model, _, _ = fit_source(tr, dv, columns, "lr", seed, True)
        predictions[held] = model.predict_proba(frame.reset_index(drop=True).iloc[held][columns])[:, 1]
    mask = ~np.isnan(predictions)
    return score(frame.y.to_numpy()[mask], predictions[mask],
                 frame.question_id.iloc[np.where(mask)[0]], seed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--questions", required=True)
    parser.add_argument("--judgments", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    frame = build_frame(Path(args.run), Path(args.questions), Path(args.judgments))
    full, dropped = length_free_columns(frame, FEATURE_SETS["relative_normalized"], CORR_LIMIT)
    print(f"dropped {len(dropped)} of {len(FEATURE_SETS['relative_normalized'])} features "
          f"(|r| with length > {CORR_LIMIT} or constant):")
    for column, why in sorted(dropped.items()):
        print(f"  {column:44s} {why}")
    print(f"kept {len(full)}: {full}")

    tre_norm = score(frame.y.to_numpy(), frame.tre_length_normalized.to_numpy(),
                     frame.question_id, args.seed)
    full_cv = cv_score(frame, FEATURE_SETS["relative_normalized"], args.seed)
    lean_cv = cv_score(frame, full, args.seed)

    payload = {
        "run": str(args.run),
        "dropped_for_length": dropped,
        "kept": full,
        "tre_length_normalized": tre_norm,
        "detector_full": full_cv,
        "detector_length_free": lean_cv,
        "gaps": {
            "full_vs_tre": full_cv["auroc"] - tre_norm["auroc"],
            "lean_vs_tre": lean_cv["auroc"] - tre_norm["auroc"],
        },
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nTRE(norm)            {tre_norm['auroc']:.4f}")
    print(f"detector full        {full_cv['auroc']:.4f}  (gap {payload['gaps']['full_vs_tre']:+.4f})")
    print(f"detector length-free {lean_cv['auroc']:.4f}  (gap {payload['gaps']['lean_vs_tre']:+.4f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
