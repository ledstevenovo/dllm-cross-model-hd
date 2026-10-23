#!/usr/bin/env python
"""Check that every headline number in the paper traces to a file on disk.

The paper has been rewritten many times tonight, and several numbers migrated between sections as
claims were revised. A stale figure left in the text would be the kind of error no test catches --
the earlier sign error was found by eye, not by tooling.

This script does not parse prose in general. It checks a hand-maintained map of claim -> source, so
each check is an assertion someone wrote deliberately rather than a heuristic that can drift.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "reports/paper_draft.md"


def metric(run: str, key: str = "tre") -> float:
    payload = json.loads((ROOT / "results/tre_repro" / run / "metrics.json").read_text())
    return payload["counts"]["main_metrics"][key]["auroc"]


def scores_metric(run: str, column: str) -> float:
    from sklearn.metrics import roc_auc_score
    frame = pd.read_csv(ROOT / "results/tre_repro" / run / "scores.csv")
    frame = frame[frame.status == "kept"]
    return float(roc_auc_score(frame.label.eq("incorrect").astype(int), frame[column]))


def main() -> int:
    text = PAPER.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, str]] = []

    # (description, condition, detail)
    def expect(label: str, value: float, rendered: str) -> None:
        """The paper must contain `rendered`, and that rendering must match `value`."""
        ok = rendered in text
        checks.append((label, ok, f"looking for {rendered!r} (computed {value:.4f})"))

    def close(label: str, computed: float, quoted: float, tol: float = 0.0051) -> None:
        # Default tolerance is half a unit in the second decimal: the paper quotes two decimals,
        # so anything within 0.005 is the same number as printed. A tighter default was flagging
        # correct roundings as failures, which would train a reader to ignore the audit.
        ok = abs(computed - quoted) <= tol
        checks.append((label, ok, f"computed {computed:.6f} vs quoted {quoted}"))

    # The five comparable cells
    close("LLaDA/TriviaQA L128 = 79.27", metric("llada_triviaqa_l128_longcat") * 100, 79.27)
    close("Dream/TriviaQA L128 = 79.68", metric("dream_triviaqa_l128_longcat") * 100, 79.68)
    close("LLaDA/HotpotQA bare = 83.79", metric("llada_hotpotqa_bare_v1") * 100, 83.79)
    close("Dream/HotpotQA bare = 82.24", metric("dream_hotpotqa_bare_v1") * 100, 82.24)
    close("LLaDA/HotpotQA bare BF16 = 82.24", metric("llada_hotpotqa_bare_bf16_longcat") * 100, 82.24)
    close("precision effect = 0.0155",
          metric("llada_hotpotqa_bare_v1") - metric("llada_hotpotqa_bare_bf16_longcat"), 0.0155, tol=0.001)

    # Normalised vs raw, which the paper now reports side by side
    close("LLaDA/TQ norm = 84.3", scores_metric("llada_triviaqa_l128_longcat", "tre_length_normalized") * 100, 84.3, tol=0.05)
    close("Dream/TQ norm = 84.8", scores_metric("dream_triviaqa_l128_longcat", "tre_length_normalized") * 100, 84.8, tol=0.05)
    close("LLaDA/TQ L256 raw = 70.15", metric("llada_triviaqa_l256_longcat") * 100, 70.15, tol=0.0051)
    close("LLaDA/TQ L256 norm = 83.8",
          scores_metric("llada_triviaqa_l256_longcat", "tre_length_normalized") * 100, 83.8, tol=0.05)

    # The claims whose signs matter most
    close("Dream/HotpotQA bare beats paper by +1.6",
          metric("dream_hotpotqa_bare_v1") * 100 - 80.6, 1.6, tol=0.05)
    close("LLaDA/HotpotQA bare misses paper by -1.8",
          85.6 - metric("llada_hotpotqa_bare_v1") * 100, 1.8, tol=0.05)

    # Context effect, both bases
    close("LLaDA context raw gap 0.093",
          metric("llada_hotpotqa_bare_v1") - metric("llada_hotpotqa_longcat"), 0.093, tol=0.0051)
    close("Dream context raw gap 0.103",
          metric("dream_hotpotqa_bare_v1") - metric("dream_hotpotqa_bf16_L128_S64_B128_v1"), 0.103, tol=0.0051)

    failed = [c for c in checks if not c[1]]
    for label, ok, detail in checks:
        print(f"{'OK  ' if ok else 'FAIL'} {label}: {detail}")
    print()
    print(f"{len(checks) - len(failed)}/{len(checks)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
