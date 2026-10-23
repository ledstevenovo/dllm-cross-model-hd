#!/usr/bin/env python
"""Post-process Dream x HotpotQA once scoring is done: test the recitation hypothesis.

The hypothesis (fixed before this run's scores existed, in
reports/tre_repro/recitation_hypothesis.md) is that LLaDA's HotpotQA shortfall comes from its
long recitations diluting the TRE sum, not from the dataset being unfriendly to TRE.

Decision rule, also fixed in advance:
    Dream/HotpotQA AUROC >= 0.75  -> recitation is the main cause
    0.70 <= AUROC < 0.75          -> partial cause
    AUROC < 0.70                  -> recitation is secondary, look elsewhere

This script reports the verdict plus the supporting comparison across all five runs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    "llada_triviaqa": ROOT / "results/tre_repro/llada_triviaqa_fp16_L128_S64_B128_v3",
    "llada_triviaqa_l64": ROOT / "results/tre_repro/llada_triviaqa_fp16_L64_S64_B64_v1",
    # LongCat version, so both HotpotQA cells share one judge (see r2_same_judge_result.md)
    "llada_hotpotqa": ROOT / "results/tre_repro/llada_hotpotqa_longcat",
    "dream_triviaqa": ROOT / "results/tre_repro/dream_triviaqa_bf16_L128_S64_B128_v1",
    "dream_hotpotqa": ROOT / "results/tre_repro/dream_hotpotqa_bf16_L128_S64_B128_v1",
}
PAPER = {"llada_triviaqa": 82.2, "llada_triviaqa_l64": 86.5,
         "llada_hotpotqa": 85.6, "dream_triviaqa": 83.9, "dream_hotpotqa": 80.6}
# Judge provenance per cell: two TriviaQA cells used different vendors from each other, and
# the HotpotQA pair now shares LongCat so at least that comparison is judge-clean.
JUDGE = {"llada_triviaqa": "deepseek", "llada_triviaqa_l64": "deepseek",
         "llada_hotpotqa": "LongCat", "dream_triviaqa": "vankit", "dream_hotpotqa": "LongCat"}


def main() -> int:
    rows, missing = [], []
    for name, path in RUNS.items():
        metrics = path / "metrics.json"
        if not metrics.exists():
            missing.append(name)
            continue
        payload = json.loads(metrics.read_text(encoding="utf-8"))
        counts = payload["counts"]
        cell = counts["main_metrics"]["tre"]
        rows.append({
            "run": name,
            "auroc": cell["auroc"],
            "auroc_low": cell["auroc_low"],
            "auroc_high": cell["auroc_high"],
            "n": cell["n"],
            "positive": counts["positive_n"],
            "positive_rate": counts["positive_n"] / cell["n"],
            "precision": payload["decoding_config"]["precision"],
            "judge": JUDGE.get(name, "?"),
            "gen_length": payload["decoding_config"]["gen_length"],
            "paper_128": PAPER[name],
            "diff_vs_paper": (cell["auroc"] * 100) - PAPER[name],
        })

    verdict = None
    if "dream_hotpotqa" in [r["run"] for r in rows]:
        target = next(r for r in rows if r["run"] == "dream_hotpotqa")
        auroc = target["auroc"]
        # Thresholds revised at 15:58 after seeing the positive rate (9.2%, ~73 positives)
        # but before any AUROC existed: the original 0.70/0.75 cutoffs were 0.05 apart while
        # the 95% CI is ~0.13 wide, so they could not be distinguished. The revised cutoffs
        # are one CI half-width apart, and the middle band is reported as "cannot tell".
        if auroc >= 0.78:
            verdict = {"holds": True, "label": "recitation is the main cause", "auroc": auroc}
        elif auroc >= 0.65:
            verdict = {"holds": "undecided",
                       "label": "indistinguishable from LLaDA on the same judge (0.745); this run cannot separate the two mechanisms",
                       "auroc": auroc}
        else:
            verdict = {"holds": False, "label": "recitation is secondary; look elsewhere", "auroc": auroc}

    payload = {
        "cells": rows,
        "missing_runs": missing,
        "recitation_hypothesis_verdict": verdict,
        "rule_frozen_at": "reports/tre_repro/recitation_hypothesis.md (original cutoffs 0.70/0.75, "
                          "revised to 0.65/0.78 on positive-rate grounds before any AUROC existed)",
        "note": ("paper_128 is the paper's 128-step column; the L64 comparison is only meaningful against "
                 "the paper's 64 column, which is not listed here because our '64' differs (see budget_columns.md)"),
    }
    out = ROOT / "reports/tre_repro/five_cells.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"{'run':22s} {'AUROC':>6} {'CI':>16} {'n':>5} {'pos%':>6} {'prec':>8} {'judge':>9} {'vs paper':>9}")
    for r in rows:
        print(f"{r['run']:22s} {r['auroc']:6.3f} [{r['auroc_low']:.3f},{r['auroc_high']:.3f}] "
              f"{r['n']:5d} {r['positive_rate']:6.1%} {r['precision']:>8} {r['judge']:>9} {r['diff_vs_paper']:+9.1f}")
    if missing:
        print(f"missing: {missing}")
    if verdict:
        print(f"\nrecitation hypothesis: {verdict['label']} (Dream/HotpotQA {verdict['auroc']:.3f})")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
