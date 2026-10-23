#!/usr/bin/env python
"""Compare TRE against the main-project detectors on *the same* traces.

Why this is worth doing: the project has two lines of work that never touched each
other. TRE is a single training-free score (sum of entropy over generated positions) from
the reproduction line; the main project trains LR/MLP on 6- or 10-dimensional entropy
summaries. They have always been evaluated on different data, so "TRE or a trained
detector?" was unanswerable.

A TRE trace carries the same trace-v1 arrays the main-project extractor expects, so the
features can be lifted off it directly. That makes the comparison exact: same generations,
same questions, same labels, only the scoring rule differs.

Fairness rules:
  * the detectors are fitted on a train split and tuned on validation, never on the test
    split that TRE is scored on;
  * TRE needs no fitting, so it is scored on its natural full set; the trained detectors
    are scored on the split they did not see. To keep the comparison like-for-like the
    report also gives TRE restricted to that same test split.
  * labels come from the run's own judged file (one label file, one judge).

Output: a JSON report plus a printed table.
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
from src.detectors import FEATURE_SETS, fit_source  # noqa: E402
from src.evaluation import binary_metrics, grouped_bootstrap  # noqa: E402
from src.trace_schema import extract_features, load_trace  # noqa: E402

SPLITS = ("train", "validation", "test")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def protocol_label(judgment: dict) -> str | None:
    """Frozen two-pass label for one judgment, or None when the sample is excluded.

    correct on the first pass -> kept as correct (no second call was made);
    incorrect then incorrect -> kept as incorrect;
    incorrect then correct -> a flip, and the frozen protocol *drops* it. Collapsing the
    flip to "the first verdict wins" would silently keep 14 samples on the LLaDA HotpotQA
    run and change the metric.
    """
    first = judgment.get("judge_first")
    second = judgment.get("judge_second")
    if first == "correct":
        return "correct"
    if first == "incorrect" and second == "incorrect":
        return "incorrect"
    return None


def build_frame(run: Path, questions: Path, judgments: Path) -> pd.DataFrame:
    """Attach main-project features to every judged-and-kept TRE trace."""
    qmeta = {row["question_id"]: row for row in read_jsonl(questions)}
    judged = {row["sample_id"]: row for row in read_jsonl(judgments) if row.get("status") == "done"}
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))

    rows = []
    for sample_id, record in manifest["samples"].items():
        judgment = judged.get(sample_id)
        if judgment is None:
            continue
        label = protocol_label(judgment)
        if label is None:
            continue
        meta, arrays = load_trace(run / record["path"])
        question = qmeta[meta["question_id"]]
        features = extract_features(meta, arrays)
        features.update(
            sample_id=sample_id,
            question_id=meta["question_id"],
            cluster_id=question["cluster_id"],
            split=question.get("split", "test"),
            dataset=meta.get("dataset", "triviaqa"),
            label=label,
        )
        rows.append(features)
    frame = pd.DataFrame(rows)
    frame["y"] = frame.label.eq("incorrect").astype(int)
    return frame


def cluster_folds(frame: pd.DataFrame, *, k: int, seed: int) -> list[tuple[np.ndarray, np.ndarray]]:
    """Return ``[(held_out_indices, train_indices), ...]`` splitting by question cluster.

    Whole clusters move together, matching the resampling unit used everywhere else in the
    project, so a near-duplicate question can never sit in both the fit and the score set.
    """
    rng = np.random.default_rng(seed)
    clusters = np.array(sorted(frame.cluster_id.unique()), dtype=object)
    order = rng.permutation(len(clusters))
    buckets: list[list] = [[] for _ in range(k)]
    for position, index in enumerate(order):
        buckets[position % k].append(clusters[index])
    folds = []
    for bucket in buckets:
        held = frame.index[frame.cluster_id.isin(bucket)].to_numpy()
        trained = frame.index[~frame.cluster_id.isin(bucket)].to_numpy()
        if len(held):
            folds.append((held, trained))
    return folds


def score(y: np.ndarray, score: np.ndarray, clusters: pd.Series, seed: int) -> dict:
    if len(set(y.tolist())) < 2:
        return {"n": int(len(y)), "auroc": None}
    entry = {"n": int(len(y)), "positive": int(y.sum()), "negative": int(len(y) - y.sum())}
    entry.update(binary_metrics(y, score))
    interval = grouped_bootstrap(y, score, clusters, repeats=1000, seed=seed)
    entry["auroc_low"] = interval.get("auroc_low")
    entry["auroc_high"] = interval.get("auroc_high")
    return entry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--questions", required=True)
    parser.add_argument("--judgments", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--feature-sets", nargs="+", default=["entropy_raw", "relative_normalized", "late_only"])
    parser.add_argument("--kinds", nargs="+", default=["lr", "mlp"])
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    frame = build_frame(Path(args.run), Path(args.questions), Path(args.judgments))
    if frame.empty:
        raise SystemExit("no kept traces with judgments")
    print(f"traces={len(frame)} splits={frame.split.value_counts().to_dict() if 'split' in frame else '-'}")

    have_split = set(frame.split.unique()) >= set(SPLITS)
    results = {"tre_training_free": {}, "trained": []}

    # --- TRE, scoring-free, on everything -----------------------------------
    # Both variants are reported: `tre` is the paper's definition (a sum over positions) and
    # `tre_length_normalized` removes the position-count scale, which matters whenever the two
    # runs being compared differ in answer length. See scale_artefact_analysis.md.
    for column in ("tre", "tre_length_normalized"):
        if column not in frame:
            continue
        results["tre_training_free"][column] = score(
            frame.y.to_numpy(), frame[column].to_numpy(), frame.question_id, args.seed)
        entry = results["tre_training_free"][column]
        print(f"TRE {column:24s} (all n={len(frame)}): AUROC {entry['auroc']:.4f}")

    test = frame[frame.split == "test"]
    if len(test) and test.y.nunique() > 1:
        results["tre_training_free"]["test"] = score(
            test.y.to_numpy(), test.tre.to_numpy(), test.question_id, args.seed)
        print(f"TRE (test n={len(test)}): AUROC {results['tre_training_free']['test']['auroc']:.4f}")

    # --- trained detectors ---------------------------------------------------
    # TRE question lists carry split="test" for every row by construction, so there is no
    # train/dev to fit on. Rather than skip the comparison, use question-clustered k-fold
    # cross-validation: every test prediction comes from a fold that never saw its cluster.
    if not have_split:
        results["note"] = ("run has no train/validation split; trained detectors are scored by "
                           "question-clustered 5-fold cross-validation instead")
        print(results["note"])
        folds = cluster_folds(frame, k=5, seed=args.seed)
        for feature_set in args.feature_sets:
            columns = FEATURE_SETS[feature_set]
            if set(columns) - set(frame.columns):
                print(f"skip {feature_set}: missing {sorted(set(columns) - set(frame.columns))}")
                continue
            for kind in args.kinds:
                predictions = np.full(len(frame), np.nan)
                for held_out, trained in folds:
                    fit_rows = frame.iloc[trained]
                    if fit_rows.y.nunique() < 2:
                        continue
                    # split the fitting rows 80/20 to give fit_source its dev set
                    inner = np.random.default_rng(args.seed).permutation(len(fit_rows))
                    cut = max(int(0.8 * len(fit_rows)), 2)
                    tr, dv = fit_rows.iloc[inner[:cut]], fit_rows.iloc[inner[cut:]]
                    if dv.y.nunique() < 2:
                        dv = tr
                    model, threshold, _ = fit_source(tr, dv, columns, kind, args.seed, True)
                    predictions[held_out] = model.predict_proba(frame.iloc[held_out][columns])[:, 1]
                mask = ~np.isnan(predictions)
                entry = {"feature_set": feature_set, "kind": kind,
                         "cv": "question-clustered 5-fold"}
                entry["test"] = score(frame.y.to_numpy()[mask], predictions[mask],
                                      frame.question_id.iloc[np.where(mask)[0]], args.seed)
                results["trained"].append(entry)
                print(f"{feature_set:20s} {kind:3s} CV AUROC {entry['test']['auroc']:.4f} "
                      f"[{entry['test'].get('auroc_low', float('nan')):.3f},"
                      f"{entry['test'].get('auroc_high', float('nan')):.3f}]")
    else:
        train = frame[frame.split == "train"]
        dev = frame[frame.split == "validation"]
        for feature_set in args.feature_sets:
            columns = FEATURE_SETS[feature_set]
            if set(columns) - set(frame.columns):
                missing = sorted(set(columns) - set(frame.columns))
                print(f"skip {feature_set}: missing {missing}")
                continue
            for kind in args.kinds:
                model, threshold, _ = fit_source(train, dev, columns, kind, args.seed, True)
                entry = {"feature_set": feature_set, "kind": kind, "threshold": float(threshold)}
                entry["test"] = score(test.y.to_numpy(),
                                      model.predict_proba(test[columns])[:, 1],
                                      test.question_id, args.seed)
                results["trained"].append(entry)
                print(f"{feature_set:20s} {kind:3s} test AUROC {entry['test']['auroc']:.4f}")

    results["run"] = str(args.run)
    results["n_traces"] = int(len(frame))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
