#!/usr/bin/env python
"""Scale-alignment diagnostic for cross-model feature transfer.

Hypothesis (paper draft section 5.3): `relative_normalized` fails on Dream->LLaDA because the
source-fitted StandardScaler meets a shifted target feature distribution, not because the
features carry no signal. Three variants per cell:

  source-scale   the current pipeline: StandardScaler fit on the SOURCE train (reference)
  target-scale   every feature z-scored with the TARGET model's train mean/std, then the
                 source-fit model applied (diagnostic only: uses target-train statistics)
  quantile-map   every TARGET feature mapped through its own train CDF onto the source-train
                 quantiles (rank alignment), source rows left untouched

If the anomaly cell recovers under target-scale / quantile-map, the failure is a scale /
alignment problem. Diagnostic only: never used in the headline numbers.

Output: reports/alignment_diagnostic.json + a markdown table on stdout.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.detectors import FEATURE_SETS, fit_source  # noqa: E402
from src.evaluation import binary_metrics  # noqa: E402


def auroc_on(model, frame, columns) -> float | None:
    if frame.empty or frame.label.nunique() < 2:
        return None
    y = frame.label.eq("incorrect").astype(int).to_numpy()
    score = model.predict_proba(frame[columns])[:, 1]
    return binary_metrics(y, score)["auroc"]


def bootstrap_ci(model, frame, columns, rng, repeats: int = 500) -> tuple[float | None, float | None]:
    """Cluster bootstrap of the test AUROC with the model held fixed."""
    if frame.empty or frame.label.nunique() < 2:
        return None, None
    frame = frame.reset_index(drop=True)
    y = frame.label.eq("incorrect").astype(int).to_numpy()
    score = model.predict_proba(frame[columns])[:, 1]
    groups = [g.index.to_numpy() for _, g in frame.groupby("question_id")]
    first = np.array([g[0] for g in groups])
    draws = []
    for _ in range(repeats):
        picked = first[rng.integers(0, len(groups), size=len(groups))]
        value = binary_metrics(y[picked], score[picked])["auroc"]
        if value is not None:
            draws.append(value)
    if not draws:
        return None, None
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return float(lo), float(hi)


def zscore_with_target(frame, columns, source, target) -> pd.DataFrame:
    out = frame.copy()
    ref = out[(out.model_id == target) & (out.split == "train")]
    for column in columns:
        mu, sigma = ref[column].mean(), ref[column].std(ddof=0)
        if sigma and sigma > 0:
            out[column] = (out[column] - mu) / sigma
    return out


def quantile_map(frame, columns, source, target) -> pd.DataFrame:
    out = frame.copy()
    src_train = out[(out.model_id == source) & (out.split == "train")]
    tgt_train = out[(out.model_id == target) & (out.split == "train")]
    for column in columns:
        src_values = np.sort(src_train[column].to_numpy())
        tgt_values = np.sort(tgt_train[column].to_numpy())
        if len(src_values) < 5 or len(tgt_values) < 5:
            continue
        quantiles = np.linspace(0, 1, len(tgt_values))
        mapped = np.interp(out.loc[out.model_id == target, column],
                           tgt_values, np.quantile(src_values, quantiles))
        out.loc[out.model_id == target, column] = mapped
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(ROOT / "results/stage7/features_combined.parquet"))
    parser.add_argument("--feature-sets", nargs="+", default=["relative_normalized", "entropy_raw"])
    parser.add_argument("--kinds", nargs="+", default=["lr", "mlp"])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default=str(ROOT / "reports/alignment_diagnostic.json"))
    args = parser.parse_args()

    frame = pd.read_parquet(args.features)
    frame = frame[frame.human_reviewed & frame.label.isin(["correct", "incorrect"])].copy()
    domains = sorted(frame.model_id.unique())
    rng = np.random.default_rng(args.seed)
    results = []
    for feature_set in args.feature_sets:
        columns = FEATURE_SETS[feature_set]
        for kind in args.kinds:
            for source in domains:
                for target in domains:
                    if source == target:
                        continue
                    src_tr = frame[(frame.model_id == source) & (frame.split == "train")]
                    src_dev = frame[(frame.model_id == source) & (frame.split == "validation")]
                    tgt_te = frame[(frame.model_id == target) & (frame.split == "test")]

                    model_ref, _, _ = fit_source(src_tr, src_dev, columns, kind, args.seed, True)
                    ref = auroc_on(model_ref, tgt_te, columns)

                    ts_frame = zscore_with_target(frame, columns, source, target)
                    model_ts2, _, _ = fit_source(
                        ts_frame[(ts_frame.model_id == source) & (ts_frame.split == "train")],
                        ts_frame[(ts_frame.model_id == source) & (ts_frame.split == "validation")],
                        columns, kind, args.seed, False)
                    target_scale = auroc_on(model_ts2, ts_frame[(ts_frame.model_id == target)
                                                                & (ts_frame.split == "test")], columns)

                    qm_frame = quantile_map(frame, columns, source, target)
                    model_qm, _, _ = fit_source(
                        qm_frame[(qm_frame.model_id == source) & (qm_frame.split == "train")],
                        qm_frame[(qm_frame.model_id == source) & (qm_frame.split == "validation")],
                        columns, kind, args.seed, True)
                    qm = auroc_on(model_qm, qm_frame[(qm_frame.model_id == target)
                                                     & (qm_frame.split == "test")], columns)
                    results.append({"source": source, "target": target, "feature_set": feature_set,
                                    "kind": kind, "n_test": int(len(tgt_te)),
                                    "source_scale": ref, "target_scale": target_scale,
                                    "quantile_map": qm,
                                    "by_dataset": {
                                        str(ds): {
                                            "n": int(len(chunk)),
                                            "source_scale": auroc_on(
                                                model_ref, chunk, columns),
                                            "quantile_map": auroc_on(
                                                model_qm,
                                                qm_frame[(qm_frame.model_id == target)
                                                         & (qm_frame.split == "test")
                                                         & (qm_frame.dataset == ds)], columns)}
                                        for ds, chunk in tgt_te.groupby("dataset")},
                                    "ci": {
                                        "source_scale": bootstrap_ci(model_ref, tgt_te, columns, rng),
                                        "target_scale": bootstrap_ci(
                                            model_ts2, ts_frame[(ts_frame.model_id == target)
                                                                & (ts_frame.split == "test")],
                                            columns, rng),
                                        "quantile_map": bootstrap_ci(
                                            model_qm, qm_frame[(qm_frame.model_id == target)
                                                               & (qm_frame.split == "test")],
                                            columns, rng)}})

    payload = {"features": args.features, "seed": args.seed,
               "note": "diagnostic only; target-scale/quantile-map use target-train statistics "
                       "and are never used in headline numbers",
               "cells": results}
    out = Path(args.out)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    header = ["格", "n", "source-scale (现状)", "target-scale", "quantile-map", "恢复?"]
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join(["---"] * len(header)) + "|")

    def fmt(value):
        return f"{value:.3f}" if isinstance(value, float) else "—"

    for r in sorted(results, key=lambda r: (r["feature_set"], r["kind"], r["source"], r["target"])):
        tag = f"{r['source'].split('/')[-1][:10]}->{r['target'].split('/')[-1][:10]} {r['feature_set'][:8]} {r['kind']}"
        delta = (r["target_scale"] - r["source_scale"]) if (r["target_scale"] is not None
                                                           and r["source_scale"] is not None) else None
        verdict = "✅ 明显恢复" if (delta or 0) > 0.10 else ("~ 小幅" if (delta or 0) > 0.03 else "— 未恢复")
        qm_lo, qm_hi = r["ci"]["quantile_map"]
        qm_ci = f" [{qm_lo:.2f},{qm_hi:.2f}]" if qm_lo is not None else ""
        print(f"| {tag} | {r['n_test']} | {fmt(r['source_scale'])} | {fmt(r['target_scale'])} | "
              f"{fmt(r['quantile_map'])}{qm_ci} | {verdict} |")
    print("\nwrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
