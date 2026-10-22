#!/usr/bin/env python
"""Pool the two stability-study seeds (300 + 300 cluster resamples per cell).

Means pool exactly (each repeat contributes one AUROC per cell); the population standard
deviation pools through the second moment. Quantiles and tail probabilities cannot be pooled
from summaries, so they are reported per seed and as their average, with the per-seed spread
shown to demonstrate seed-independence.

Output: reports/stability_two_seeds.json and a markdown table on stdout.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed1", default=str(ROOT / "reports/main_project_stability.json"))
    parser.add_argument("--seed2", default=str(ROOT / "reports/main_project_stability_seed2.json"))
    parser.add_argument("--out", default=str(ROOT / "reports/stability_two_seeds.json"))
    args = parser.parse_args()

    run1 = json.loads(Path(args.seed1).read_text())
    run2 = json.loads(Path(args.seed2).read_text())
    if run1.get("stopped_early") or run2.get("stopped_early"):
        print("warning: a run stopped early; pooling only completed cells")
    cells1 = {(c["source"], c["target"], c["feature_set"], c["kind"]): c
              for c in run1["cells"]}
    cells2 = {(c["source"], c["target"], c["feature_set"], c["kind"]): c
              for c in run2["cells"]}
    keys = sorted(set(cells1) & set(cells2))
    pooled, spread = [], []
    for key in keys:
        a, b = cells1[key], cells2[key]
        n1, n2 = a["repeats_valid"], b["repeats_valid"]
        n = n1 + n2
        mean = (n1 * a["auroc_mean"] + n2 * b["auroc_mean"]) / n
        second = (n1 * (a["auroc_std"] ** 2 + a["auroc_mean"] ** 2)
                  + n2 * (b["auroc_std"] ** 2 + b["auroc_mean"] ** 2)) / n
        std = max(second - mean ** 2, 0.0) ** 0.5
        entry = {
            "source": key[0], "target": key[1], "feature_set": key[2], "kind": key[3],
            "n_pooled": n, "mean_pooled": float(mean), "std_pooled": float(std),
            "mean_seed1": a["auroc_mean"], "mean_seed2": b["auroc_mean"],
            "std_seed1": a["auroc_std"], "std_seed2": b["auroc_std"],
            "p_above_0_5_seed1": a["p_above_0_5"], "p_above_0_5_seed2": b["p_above_0_5"],
            "p_above_0_7_seed1": a["p_above_0_7"], "p_above_0_7_seed2": b["p_above_0_7"],
            "p_above_0_8_seed1": a["p_above_0_8"], "p_above_0_8_seed2": b["p_above_0_8"],
            "p_above_0_5_mean": (a["p_above_0_5"] + b["p_above_0_5"]) / 2,
            "p_above_0_7_mean": (a["p_above_0_7"] + b["p_above_0_7"]) / 2,
            "p_above_0_8_mean": (a["p_above_0_8"] + b["p_above_0_8"]) / 2,
            "mean_abs_diff": abs(a["auroc_mean"] - b["auroc_mean"]),
            "p_above_0_7_abs_diff": abs(a["p_above_0_7"] - b["p_above_0_7"]),
        }
        pooled.append(entry)
        spread.append(entry["mean_abs_diff"])

    payload = {
        "date": "2026-10-22",
        "runs": [{"path": str(args.seed1), "seed": run1.get("seed"),
                  "repeats": run1.get("repeats"), "cells": len(run1["cells"])},
                 {"path": str(args.seed2), "seed": run2.get("seed"),
                  "repeats": run2.get("repeats"), "cells": len(run2["cells"])}],
        "cells": pooled,
        "seed_mean_abs_diff": {"max": max(spread) if spread else None,
                               "mean": sum(spread) / len(spread) if spread else None},
        "note": "means and std pooled exactly from per-seed summaries; quantiles/tail "
                "probabilities are per seed (pooling from summaries is not exact) and the "
                "average is shown for orientation",
    }
    out = Path(args.out)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    header = ["格", "均值(600)", "σ(600)", "均值 seed1/seed2", "P>0.5 s1/s2",
              "P>0.7 s1/s2", "P>0.8 s1/s2"]
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join(["---"] * len(header)) + "|")
    for c in sorted(pooled, key=lambda c: (c["feature_set"], c["kind"], c["source"], c["target"])):
        tag = f"{c['source'].split('/')[-1][:10]}->{c['target'].split('/')[-1][:10]}"
        print(f"| {tag} {c['feature_set'][:8]} {c['kind']} | {c['mean_pooled']:.3f} | "
              f"{c['std_pooled']:.3f} | {c['mean_seed1']:.3f}/{c['mean_seed2']:.3f} | "
              f"{c['p_above_0_5_seed1']:.2f}/{c['p_above_0_5_seed2']:.2f} | "
              f"{c['p_above_0_7_seed1']:.2f}/{c['p_above_0_7_seed2']:.2f} | "
              f"{c['p_above_0_8_seed1']:.2f}/{c['p_above_0_8_seed2']:.2f} |")
    print(f"\nseed |Δmean| max={payload['seed_mean_abs_diff']['max']:.4f} "
          f"mean={payload['seed_mean_abs_diff']['mean']:.4f}")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
