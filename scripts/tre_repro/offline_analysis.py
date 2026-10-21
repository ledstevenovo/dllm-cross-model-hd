#!/usr/bin/env python
"""TRE offline analyses on the frozen 800-question run (CPU only, no new generation).

Computes, all from the existing trace-v1 arrays + committed judgments:
  1. score-family comparison (TRE variants, entropy aggregates, confidence, stability)
  2. space ablations (all / unrevealed / revealing / revealed evidence) per paper table 2/3 names
  3. time ablations (average / exponential / hard last-30% / linear)
  4. calibration (Brier / ECE) for the probability-shaped scores
  5. answer_type and termination breakdowns, plus tail diagnostics
  6. grouped bootstrap CIs for every score (question_id grouped, fixed seed)

Output: reports/tre_repro/offline_analysis.json (+ per-score CSV). Never changes the
pre-registered main metric; everything here is a declared secondary analysis.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(REPO))
from src.evaluation import binary_metrics, grouped_bootstrap  # noqa: E402

BOOTSTRAP = 1000
BOOTSTRAP_SEED = 20261021


def load_run(run: Path):
    manifest = json.loads((run / "manifest.json").read_text())
    rows = []
    for sample_id, record in manifest["samples"].items():
        with np.load(run / record["path"], allow_pickle=False) as z:
            arrays = {key: z[key] for key in z.files if key != "metadata"}
            meta = json.loads(z["metadata"].item())
        rows.append({"sample_id": sample_id, "meta": meta, "arrays": arrays})
    return rows


def score_families(row, vocab_size: int) -> dict:
    a = row["arrays"]
    entropy, revealed = a["entropy"].astype(np.float64), a["revealed"].astype(bool)
    prob = a["top1_probability"].astype(np.float64)
    length = int(row["meta"]["effective_length"])
    T = entropy.shape[0]
    weight = (np.arange(1, T + 1) / T)[:, None]
    log_vocab = np.log(vocab_size)
    vis = entropy[:, :length]
    vis_r = revealed[:, :length]
    tail = entropy[:, length + 1:] if length + 1 < T else np.zeros((T, 0))
    tail_r = revealed[:, length + 1:] if length + 1 < T else np.zeros((T, 0), dtype=bool)
    out = {
        "tre": float((weight * entropy * revealed).sum()),
        "tre_effective": float((weight * vis * vis_r).sum()),
        "tre_length_normalized": float((weight * vis * vis_r).sum() / max(length, 1)),
        "tre_vocab_normalized": float((weight * entropy * revealed).sum() / log_vocab),
        "mean_entropy": float(vis.mean()) if length else 0.0,
        "max_entropy": float(vis.max()) if length else 0.0,
        "late_entropy": float(vis[int(2 * T / 3):].mean()) if length else 0.0,
        "revealing_entropy": float(vis[vis_r].mean()) if vis_r.any() else 0.0,
        "mean_uncertainty": float(1.0 - prob[:, :length].mean()) if length else 0.0,
        "min_top1_probability": float(prob[:, :length].min()) if length else 0.0,
        "tail_tre": float((weight * tail * tail_r).sum()) if tail.size else 0.0,
        "effective_length": float(length),
    }
    tokens = a["top1_token"][:, :length]
    out["prediction_switch_rate"] = float((tokens[1:] != tokens[:-1]).mean()) if tokens.shape[0] > 1 and length else 0.0
    return out


def space_ablation(row) -> dict:
    """Paper table 2/3 space variants, computed on the same traces."""
    a = row["arrays"]
    entropy, revealed, mask_before = (a["entropy"].astype(np.float64), a["revealed"].astype(bool),
                                      a["mask_before"].astype(bool))
    T = entropy.shape[0]
    weight = (np.arange(1, T + 1) / T)[:, None]
    unrevealed = mask_before & ~revealed
    revealed_before = ~mask_before
    masks = {"space_all_tokens": np.ones_like(mask_before),
             "space_unrevealed": unrevealed,
             "space_revealing": revealed,
             "space_revealed_before": revealed_before}
    out = {}
    for name, mask in masks.items():
        out[name] = float((weight * entropy * mask).sum())
    # plain averages over each region (the paper's "Average" variant)
    for name, mask in masks.items():
        denom = max(int(mask.sum()), 1)
        out[name + "_average"] = float((entropy * mask).sum() / denom)
    return out


def time_ablation(row) -> dict:
    a = row["arrays"]
    entropy, revealed = a["entropy"].astype(np.float64), a["revealed"].astype(bool)
    T = entropy.shape[0]
    linear = (np.arange(1, T + 1) / T)[:, None]
    expo = np.exp(np.arange(T) / T)[:, None]
    expo = expo / expo.max()
    hard = (np.arange(T) >= int(0.7 * T))[:, None].astype(np.float64)
    uniform = np.ones((T, 1))
    out = {}
    for name, weight in (("time_linear", linear), ("time_exponential", expo),
                         ("time_hard_last_30", hard), ("time_average", uniform)):
        weighted = float((weight * entropy * revealed).sum())
        out[name] = weighted
        out[name + "_average"] = weighted / max(int(revealed.sum()), 1)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", default=str(REPO / "data/trajectories/tre_repro/llada_triviaqa_fp16_L128_S64_B128_v3"))
    parser.add_argument("--scores", default=str(REPO / "results/tre_repro/llada_triviaqa_fp16_L128_S64_B128_v3/scores.csv"))
    parser.add_argument("--out", default=str(REPO / "reports/tre_repro/offline_analysis.json"))
    parser.add_argument("--bootstrap", type=int, default=BOOTSTRAP)
    args = parser.parse_args()

    run = Path(args.run)
    rows = load_run(run)
    judged = {row["sample_id"]: row for row in csv.DictReader(open(args.scores))}
    vocab_size = int(rows[0]["meta"]["vocab_size"])

    per_sample, labels, question_ids, answer_types, terminations = [], [], [], [], []
    for row in rows:
        sid = row["sample_id"]
        record = judged.get(sid)
        if record is None or record["status"] != "kept":
            continue
        label = 1 if record["label"] == "incorrect" else 0
        families = {**score_families(row, vocab_size), **space_ablation(row), **time_ablation(row)}
        families["sample_id"] = sid
        families["question_id"] = row["meta"]["question_id"]
        families["label"] = label
        per_sample.append(families)
        labels.append(label)
        question_ids.append(row["meta"]["question_id"])
        answer_types.append(record.get("answer_type") or "unknown")
        terminations.append(row["meta"]["termination"])

    labels = np.asarray(labels)
    question_ids = np.asarray(question_ids)
    score_names = [key for key in per_sample[0] if key not in ("sample_id", "question_id", "label")]
    results = {}
    for name in score_names:
        scores = np.asarray([row[name] for row in per_sample], dtype=float)
        if not np.isfinite(scores).all() or np.unique(scores).size < 2:
            continue
        metrics = binary_metrics(labels, scores)
        metrics.update(grouped_bootstrap(labels, scores, question_ids, repeats=args.bootstrap, seed=BOOTSTRAP_SEED))
        results[name] = metrics

    # probability-shaped scores: calibration
    calibration = {}
    for name in ("min_top1_probability", "mean_uncertainty"):
        if name in results:
            calibration[name] = {"brier": results[name].get("brier"), "ece": results[name].get("ece")}

    # breakdowns
    by_answer_type, by_termination = {}, {}
    tre = np.asarray([row["tre"] for row in per_sample], dtype=float)
    for value in sorted(set(answer_types)):
        mask = np.asarray([a == value for a in answer_types])
        if mask.sum() and np.unique(labels[mask]).size == 2:
            by_answer_type[value] = binary_metrics(labels[mask], tre[mask])
        else:
            by_answer_type[value] = {"n": int(mask.sum()), "positive": int(labels[mask].sum()),
                                     "auroc": None, "note": "single class or too few"}
    for value in sorted(set(terminations)):
        mask = np.asarray([t == value for t in terminations])
        if mask.sum() and np.unique(labels[mask]).size == 2:
            by_termination[value] = binary_metrics(labels[mask], tre[mask])
        else:
            by_termination[value] = {"n": int(mask.sum()), "positive": int(labels[mask].sum()), "auroc": None}

    report = {
        "run": str(run), "scores_file": args.scores, "n": len(per_sample),
        "positive": int(labels.sum()), "negative": int((1 - labels).sum()),
        "bootstrap": {"repeats": args.bootstrap, "seed": BOOTSTRAP_SEED, "unit": "question_id"},
        "main_metric": "tre",
        "score_families": results,
        "calibration": calibration,
        "by_answer_type": by_answer_type,
        "by_termination": by_termination,
        "notes": [
            "all scores are secondary analyses; the pre-registered main metric stays tre",
            "space variants follow the paper table 2/3 names; exponential/hard windows are self-defined and declared",
            "bootstrap resamples question_id groups; single-class draws are skipped and counted",
        ],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    with open(out.with_suffix(".csv"), "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["score", "n", "positive", "negative", "auroc", "auprc",
                                                "auroc_low", "auroc_high", "auprc_low", "auprc_high",
                                                "bootstrap_valid"])
        writer.writeheader()
        for name, metrics in sorted(results.items(), key=lambda kv: -(kv[1].get("auroc") or 0)):
            writer.writerow({"score": name, **{key: metrics.get(key) for key in writer.fieldnames if key != "score"}})
    top = sorted(((name, m.get("auroc")) for name, m in results.items() if m.get("auroc") is not None),
                 key=lambda kv: -kv[1])
    print(f"n={len(per_sample)} positive={int(labels.sum())} | {len(results)} scores")
    for name, auroc in top[:12]:
        m = results[name]
        print(f"  {name:34s} AUROC {auroc:.4f} [{m['auroc_low']:.4f}, {m['auroc_high']:.4f}] AUPRC {m['auprc']:.4f}")
    print("wrote", out, "and", out.with_suffix(".csv"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
