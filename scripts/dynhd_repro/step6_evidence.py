#!/usr/bin/env python
"""Step-6 evaluation evidence: per-seed metrics, per-ID scores, bootstrap CI and the
val-selected-threshold view, plus the common valid test set across models.

Thresholds: the main view is fixed at 0.5; the secondary view selects the threshold on
validation only (max F1) and applies it to test exactly once. Bootstrap resamples question
groups 1000 times with a fixed RNG seed; single-class resamples are skipped and counted.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO / "references/repos/DynHD"))
import common  # noqa: E402
import numpy as np  # noqa: E402
import torch  # noqa: E402
from dynhd.data import load_trace_dir  # noqa: E402
from dynhd.detectors import DetectorConfig, DynHDDetector  # noqa: E402
from sklearn.metrics import (accuracy_score, average_precision_score, f1_score,  # noqa: E402
                             precision_score, recall_score, roc_auc_score)

BOOTSTRAP = 1000
BOOTSTRAP_SEED = 20261021
MODELS = ("llada", "dream")


def load_detector(seed_dir: Path):
    checkpoint = torch.load(seed_dir / "detector.pt", map_location="cpu", weights_only=True)
    cfg = DetectorConfig(**checkpoint["cfg"])
    detector = DynHDDetector(cfg, device="cuda")
    return detector, checkpoint


def score_all(seed_dir: Path, data):
    detector, checkpoint = load_detector(seed_dir)
    detector.ensure_prompt_projector(data)
    detector.reference.load_state_dict(checkpoint["reference"])
    detector.deviation.load_state_dict(checkpoint["deviation"])
    if checkpoint.get("prompt_projector") is not None:
        detector.prompt_projector.load_state_dict(checkpoint["prompt_projector"])
    return np.asarray(detector.predict_proba(data), dtype=np.float64)


def metrics_at(y, scores, threshold):
    predictions = (scores >= threshold).astype(int)
    return {
        "n": int(len(y)), "positive": int(np.sum(y == 1)), "negative": int(np.sum(y == 0)),
        "auroc": float(roc_auc_score(y, scores)) if np.unique(y).size > 1 else None,
        "average_precision": float(average_precision_score(y, scores)) if np.unique(y).size > 1 else None,
        "accuracy": float(accuracy_score(y, predictions)),
        "precision": float(precision_score(y, predictions, zero_division=0)),
        "recall": float(recall_score(y, predictions, zero_division=0)),
        "f1": float(f1_score(y, predictions, zero_division=0)),
    }


def best_threshold(y, scores):
    candidates = sorted(set(float(s) for s in scores))
    best, best_f1 = 0.5, -1.0
    for threshold in candidates:
        f1 = f1_score(y, (scores >= threshold).astype(int), zero_division=0)
        if f1 > best_f1:
            best, best_f1 = float(threshold), float(f1)
    return best, best_f1


def grouped_bootstrap_auroc(y, scores, groups, seed):
    rng = np.random.default_rng(seed)
    unique = sorted(set(groups))
    by_group = {group: [i for i, g in enumerate(groups) if g == group] for group in unique}
    values = []
    for _ in range(BOOTSTRAP):
        chosen = rng.choice(unique, size=len(unique), replace=True)
        idx = [i for group in chosen for i in by_group[group]]
        yy, ss = y[idx], scores[idx]
        if np.unique(yy).size < 2:
            continue
        values.append(float(roc_auc_score(yy, ss)))
    if not values:
        return {"ci_low": None, "ci_high": None, "valid_resamples": 0, "requested": BOOTSTRAP}
    return {"ci_low": float(np.percentile(values, 2.5)), "ci_high": float(np.percentile(values, 97.5)),
            "valid_resamples": len(values), "requested": BOOTSTRAP,
            "mean": float(np.mean(values)), "median": float(np.median(values))}


def stats(values):
    values = [value for value in values if value is not None]
    if not values:
        return None
    return {"mean": float(np.mean(values)), "min": float(np.min(values)), "max": float(np.max(values)),
            "n": len(values)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-id", default="pilot200_v1")
    args = parser.parse_args()
    summary = {"date": common.utc_now(), "experiment_id": args.experiment_id,
               "threshold_main": 0.5, "bootstrap": {"resamples": BOOTSTRAP, "rng_seed": BOOTSTRAP_SEED,
                                                    "grouping": "question_id"},
               "models": {}}
    test_sets = {}
    for model in MODELS:
        root = common.REPRO_ROOT / f"traces/{model}/pilot200/valid"
        split = json.loads((common.REPRO_ROOT / f"splits/{model}/pilot200.json").read_text())
        data = load_trace_dir(str(root))
        sample_ids = [str(item["meta"]["id"]) for item in data]
        labels = np.asarray([int(item["label"]) for item in data], dtype=int)
        per_seed = []
        for seed in (42, 43, 44):
            seed_dir = common.REPRO_ROOT / f"results/{model}_pilot200/{args.experiment_id}/seed{seed}"
            scores = score_all(seed_dir, data)
            rows = {}
            for part in ("val", "test"):
                idx = split[part]
                y = labels[idx]
                s = scores[idx]
                fixed = metrics_at(y, s, 0.5)
                threshold, val_f1 = (best_threshold(labels[split["val"]], scores[split["val"]])
                                     if part == "test" else (None, None))
                rows[part] = {"fixed_threshold_0_5": fixed}
                if part == "test":
                    rows[part]["val_selected_threshold"] = {
                        "threshold": threshold, "val_f1": val_f1,
                        **metrics_at(y, s, threshold)}
                rows[part]["scores"] = {sample_ids[i]: float(scores[i]) for i in idx}
                rows[part]["labels"] = {sample_ids[i]: int(labels[i]) for i in idx}
            test_idx = split["test"]
            per_seed.append({
                "seed": seed, "val_fixed": rows["val"]["fixed_threshold_0_5"],
                "test_fixed": rows["test"]["fixed_threshold_0_5"],
                "test_val_selected": rows["test"]["val_selected_threshold"],
                "test_bootstrap": grouped_bootstrap_auroc(labels[test_idx], scores[test_idx],
                                                          [sample_ids[i] for i in test_idx],
                                                          BOOTSTRAP_SEED + seed),
                "scores_test": rows["test"]["scores"], "labels_test": rows["test"]["labels"],
            })
            test_sets.setdefault(model, set()).update(sample_ids[i] for i in test_idx)
        summary["models"][model] = {
            "valid_n": len(data),
            "per_seed": per_seed,
            "aggregate": {
                "test_auroc_fixed": stats([r["test_fixed"]["auroc"] for r in per_seed]),
                "test_ap_fixed": stats([r["test_fixed"]["average_precision"] for r in per_seed]),
                "test_f1_fixed": stats([r["test_fixed"]["f1"] for r in per_seed]),
                "test_auroc_val_selected": stats([r["test_val_selected"]["auroc"] for r in per_seed]),
                "val_auroc_fixed": stats([r["val_fixed"]["auroc"] for r in per_seed]),
                "test_bootstrap": [{"seed": r["seed"], **r["test_bootstrap"]} for r in per_seed],
            },
            "views": {"view1": "reports/dynhd_labels.json", "view2": "this file",
                      "view3": "common test set below"},
        }
        out = REPO / f"reports/dynhd_eval_{model}.json"
        out.write_text(json.dumps(summary["models"][model], indent=2, ensure_ascii=False) + "\n")
        print(f"{model}: test AUROC per seed "
              f"{[round(r['test_fixed']['auroc'], 4) if r['test_fixed']['auroc'] is not None else None for r in per_seed]} "
              f"F1 {[round(r['test_fixed']['f1'], 3) for r in per_seed]} -> {out}")

    common_ids = sorted(test_sets["llada"] & test_sets["dream"])
    summary["view3_common_test"] = {"llada_test_n": len(test_sets["llada"]),
                                    "dream_test_n": len(test_sets["dream"]), "common_n": len(common_ids)}
    for model in MODELS:
        per_seed_common = []
        for row in summary["models"][model]["per_seed"]:
            idx = [i for i in sorted(row["scores_test"]) if i in set(common_ids)]
            y = np.asarray([row["labels_test"][i] for i in idx], dtype=int)
            s = np.asarray([row["scores_test"][i] for i in idx], dtype=float)
            per_seed_common.append(metrics_at(y, s, 0.5)["auroc"])
        summary["view3_common_test"][f"{model}_common_test_auroc"] = per_seed_common
    combined = REPO / "reports/dynhd_step6_summary.json"
    combined.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(summary["view3_common_test"], ensure_ascii=False))
    print("wrote", combined)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
