#!/usr/bin/env python
"""One table for every TRE cell, with the protocol differences that make them comparable or not.

By now there are eight runs covering model x dataset x budget x prompt variant, and the
figures are only interpretable next to their protocol: judge vendor, precision, and whether
retrieval context was in the prompt. That last one turned out to move AUROC by ~0.09, more than
any other difference, so a table without it invites wrong comparisons.

The paper's reference values are read from a frozen dict rather than guessed per run. Cells
whose column definition differs from the paper (our L64 halves the positions TRE sums over) are
flagged rather than silently compared.

Output: reports/tre_repro/all_cells.json plus a printed table.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results/tre_repro"

# run directory -> (model, dataset, gen_length, prompt variant, judge, paper reference or None)
CELLS = {
    "llada_triviaqa_l128_longcat": ("LLaDA", "TriviaQA", 128, "bare", "LongCat", 82.2),
    "llada_triviaqa_l64_longcat": ("LLaDA", "TriviaQA", 64, "bare", "LongCat", None),
    "dream_triviaqa_l128_longcat": ("Dream", "TriviaQA", 128, "bare", "LongCat", 83.9),
    "dream_triviaqa_bf16_L64_S64_B64_v1": ("Dream", "TriviaQA", 64, "bare", "LongCat", None),
    "llada_hotpotqa_bare_v1": ("LLaDA", "HotpotQA", 128, "bare", "LongCat", 85.6),
    "llada_hotpotqa_bare_v1_L64": ("LLaDA", "HotpotQA", 64, "bare", "LongCat", None),
    "dream_hotpotqa_bare_v1": ("Dream", "HotpotQA", 128, "bare", "LongCat", 80.6),
    "llada_hotpotqa_longcat": ("LLaDA", "HotpotQA", 128, "context", "LongCat", 85.6),
    "llada_hotpotqa_fp16_L128_S64_B128_v1": ("LLaDA", "HotpotQA", 128, "context", "deepseek", 85.6),
    "dream_hotpotqa_bf16_L128_S64_B128_v1": ("Dream", "HotpotQA", 128, "context", "LongCat", 80.6),
    "dream_hotpotqa_bare_l64": ("Dream", "HotpotQA", 64, "bare", "LongCat", None),
    "dream_hotpotqa_ctx_l64": ("Dream", "HotpotQA", 64, "context", "LongCat", None),
}

# The paper's two columns are "total diffusion steps" 128 and 64; our runs are both single-block
# 64 steps and differ only in tokens per step, so a 64-vs-64 comparison is not apples to apples.
PAPER_64 = 86.5  # TriviaQA 64 column, deliberately unused for comparison


def main() -> int:
    rows = []
    for name, (model, dataset, gen, variant, judge, paper) in CELLS.items():
        path = RESULTS / name
        metrics_file = path / "metrics.json"
        if not metrics_file.exists():
            continue
        payload = json.loads(metrics_file.read_text(encoding="utf-8"))
        counts = payload["counts"]
        cell = counts["main_metrics"]["tre"]
        rows.append({
            "run": name,
            "model": model,
            "dataset": dataset,
            "gen_length": gen,
            "prompt": variant,
            "judge": judge,
            "precision": payload["decoding_config"]["precision"],
            "auroc": cell["auroc"],
            "auroc_low": cell["auroc_low"],
            "auroc_high": cell["auroc_high"],
            "n": cell["n"],
            "positive": counts["positive_n"],
            "positive_rate": counts["positive_n"] / cell["n"],
            "paper_128": paper,
            "delta_vs_paper": (cell["auroc"] * 100 - paper) if paper else None,
            "comparable_to_paper": bool(paper) and gen == 128,
        })

    rows.sort(key=lambda r: (r["model"], r["dataset"], r["prompt"], r["gen_length"]))
    out = ROOT / "reports/tre_repro/all_cells.json"
    out.write_text(json.dumps({"cells": rows, "note": (
        "comparable_to_paper is True only for gen_length=128 cells with a paper reference; "
        "our 64-token runs change the number of positions TRE sums over, not the step count, "
        "so they are not comparable with the paper's 64 column (see budget_columns.md)")},
        indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"{'model':6s} {'dataset':9s} {'prompt':8s} {'gen':>4} {'judge':>9} {'prec':>8} "
          f"{'AUROC':>6} {'CI':>14} {'pos%':>6} {'vs paper':>9}")
    for r in rows:
        delta = f"{r['delta_vs_paper']:+.1f}" if r["delta_vs_paper"] is not None else "—"
        flag = "" if r["comparable_to_paper"] else " *"
        print(f"{r['model']:6s} {r['dataset']:9s} {r['prompt']:8s} {r['gen_length']:4d} "
              f"{r['judge']:>9} {r['precision']:>8} {r['auroc']:6.3f} "
              f"[{r['auroc_low']:.3f},{r['auroc_high']:.3f}] {r['positive_rate']:6.1%} {delta:>9}{flag}")
    print("\n* not comparable with the paper's column (different definition of the budget)")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
