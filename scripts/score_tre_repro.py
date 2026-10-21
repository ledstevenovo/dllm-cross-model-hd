"""Score one TRE-reproduction run (plan v3.1 §7): single model, no detector training.

This is the sanctioned entry point for R1 -- ``scripts/offline.py evaluate`` cannot
serve as one: it demands exactly two backbones, human-reviewed labels, a
train/validation/test fit and BF16 features, none of which apply to a single-model
training-free metric.

What it enforces before any number is printed (all failures are hard errors):

* question file passes :func:`src.tre_repro.load_questions` (schema, bare prompt,
  ``sample_id`` contract, unique IDs);
* every trace matches the frozen question (id, prompt), carries the frozen
  generation seed and one single decoding configuration across the run, and is
  real FP16 unless ``--allow-synthetic`` is given;
* every judgment is bound to the *judged text* through ``generated_text_sha256``,
  so a re-generation cannot silently reuse stale labels;
* coverage of questions / traces / judgments is complete for the main table.
  Missing traces, unjudged samples or ``needs_review`` records block the main
  table (exit 2) unless ``--allow-partial`` asks for an explicitly labelled
  reported subset.

Outputs: ``scores.csv`` (per sample), ``metrics.json`` (counts, AUROC/AP with a
question-grouped bootstrap CI, decoding diagnostics and provenance hashes).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from src.evaluation import binary_metrics, grouped_bootstrap  # noqa: E402
from src.trace_schema import extract_features, load_trace  # noqa: E402
from src.tre_repro import GENERATION_SEED, load_questions  # noqa: E402

VALID_VERDICTS = ("correct", "incorrect")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_run_traces(run: Path, *, allow_synthetic: bool) -> tuple[dict[str, tuple[dict, dict]], dict]:
    """Load every trace, enforce per-run consistency, return rows and a config summary."""
    traces = sorted((run / "traces").glob("*.npz"))
    if not traces:
        raise ValueError(f"no traces under {run/'traces'}")
    loaded: dict[str, tuple[dict, dict]] = {}
    configs: set[tuple] = set()
    for path in traces:
        meta, arrays = load_trace(path)
        sample_id = meta["sample_id"]
        if sample_id in loaded:
            raise ValueError(f"duplicate trajectory for {sample_id}")
        if not allow_synthetic and meta.get("synthetic", False):
            raise ValueError(f"synthetic trajectory in a real run: {sample_id}")
        if not allow_synthetic and meta.get("precision") != "float16":
            raise ValueError(f"expected float16, found {meta.get('precision')!r}: {sample_id}")
        configs.add((meta.get("model_id"), meta.get("precision"), meta.get("gen_length"),
                     meta.get("steps"), meta.get("block_size"), meta.get("seed")))
        loaded[sample_id] = (meta, arrays)
    if len(configs) != 1:
        raise ValueError(f"run mixes decoding configurations: {sorted(configs)}")
    model_id, precision, gen_length, steps, block_size, seed = next(iter(configs))
    summary = {"model_id": model_id, "precision": precision, "gen_length": gen_length,
               "steps": steps, "block_size": block_size, "seed": seed, "traces": len(loaded)}
    return loaded, summary


def load_judgments(path: Path) -> dict[str, dict]:
    records = read_jsonl(path)
    by_id: dict[str, dict] = {}
    for record in records:
        sample_id = record.get("sample_id")
        if not sample_id:
            raise ValueError("judgment without sample_id")
        if sample_id in by_id:
            raise ValueError(f"duplicate judgment for {sample_id}")
        status = record.get("status", "done")
        if status not in ("done", "needs_review"):
            raise ValueError(f"unknown judgment status {status!r} for {sample_id}")
        if status == "done":
            first = record.get("judge_first")
            if first not in VALID_VERDICTS:
                raise ValueError(f"invalid judge_first for {sample_id}: {first!r}")
            if first == "incorrect" and record.get("judge_second") not in VALID_VERDICTS:
                raise ValueError(f"judge_second is required after an incorrect first verdict: {sample_id}")
        by_id[sample_id] = record
    return by_id


def collect_rows(run: Path, questions_path: Path, judgments_path: Path, *,
                 allow_synthetic: bool = False, allow_missing_answer_hash: bool = False) -> tuple[list[dict], dict]:
    """Validate and join questions x traces x judgments into per-sample rows."""
    questions = {q.sample_id: q for q in load_questions(questions_path)}
    expected_ids = set(questions)
    traces, config = load_run_traces(run, allow_synthetic=allow_synthetic)
    judgments = load_judgments(judgments_path)

    unknown = set(traces) - expected_ids
    if unknown:
        raise ValueError(f"trajectories outside the frozen question list: {sorted(unknown)[:3]}")
    unknown_judgments = set(judgments) - expected_ids
    if unknown_judgments:
        raise ValueError(f"judgments outside the frozen question list: {sorted(unknown_judgments)[:3]}")

    rows: list[dict] = []
    for sample_id, question in questions.items():
        row: dict = {
            "sample_id": sample_id,
            "question_id": question.question_id,
            "cluster_id": question.cluster_id,
            "split": question.split,
            "answer_type": question.answer_type,
            "status": "missing_trace",
            "exclusion": "",
        }
        trace = traces.get(sample_id)
        if trace is not None:
            meta, arrays = trace
            if meta["question_id"] != question.question_id:
                raise ValueError(f"question_id mismatch for {sample_id}")
            if meta.get("prompt") != question.question:
                raise ValueError(f"prompt mismatch for {sample_id}")
            if meta.get("seed") != GENERATION_SEED:
                raise ValueError(f"generation seed mismatch for {sample_id}: {meta.get('seed')!r}")
            features = extract_features(meta, arrays)
            row.update({
                "tre": features["tre"],
                "tre_effective": features["tre_effective"],
                "tre_length_normalized": features["tre_length_normalized"],
                "effective_length": meta["effective_length"],
                "generation_length": meta["gen_length"],
                "termination": meta["termination"],
                "tail_tre": features["tre"] - features["tre_effective"],
                "tail_share": ((features["tre"] - features["tre_effective"]) / features["tre"]
                               if features["tre"] else float("nan")),
                "generated_text_sha256": sha256_text(meta["generated_text"]),
                "generated_text": meta["generated_text"],
            })
            judgment = judgments.get(sample_id)
            if judgment is None:
                row["status"] = "unjudged"
            else:
                if not allow_missing_answer_hash:
                    claimed = judgment.get("generated_text_sha256")
                    if claimed != row["generated_text_sha256"]:
                        raise ValueError(
                            f"judgment is not bound to this generation for {sample_id}: "
                            f"{str(claimed)[:16]} != {row['generated_text_sha256'][:16]}"
                        )
                row["judge_first"] = judgment.get("judge_first")
                row["judge_second"] = judgment.get("judge_second")
                if judgment.get("status", "done") == "needs_review":
                    row["status"] = "needs_review"
                elif row["judge_first"] == "incorrect" and row.get("judge_second") == "correct":
                    row["status"] = "dropped"
                    row["exclusion"] = "judge disagreement (incorrect -> correct)"
                else:
                    row["status"] = "kept"
                    row["label"] = "incorrect" if row["judge_first"] == "incorrect" else "correct"
        rows.append(row)
    return rows, config


def _auroc(y: np.ndarray, score: np.ndarray) -> float | None:
    if len(set(y.tolist())) < 2:
        return None
    finite = np.isfinite(score)
    if not finite.all():
        return None
    return binary_metrics(y, score)["auroc"]


def summarize(rows: list[dict], *, bootstrap: int, bootstrap_seed: int) -> dict:
    """Counts, main metrics and the pre-declared diagnostics (direction is fixed: higher = riskier)."""
    counts = {name: sum(1 for row in rows if row["status"] == name)
              for name in ("kept", "dropped", "needs_review", "unjudged", "missing_trace")}
    kept = [row for row in rows if row["status"] == "kept"]
    summary: dict = {
        "initial_n": len(rows),
        "kept_n": counts["kept"],
        "dropped_n": counts["dropped"],
        "needs_review_n": counts["needs_review"],
        "unjudged_n": counts["unjudged"],
        "missing_trace_n": counts["missing_trace"],
        "judge_first_correct_n": sum(1 for row in rows if row.get("judge_first") == "correct"),
        "judge_first_incorrect_n": sum(1 for row in rows if row.get("judge_first") == "incorrect"),
        "judge_second_ran_n": sum(1 for row in rows if row.get("judge_second") in VALID_VERDICTS),
        "judge_flip_n": counts["dropped"],
        "main_table_eligible": not any(counts[name] for name in ("needs_review", "unjudged", "missing_trace")),
    }
    if not kept:
        summary["main_metrics"] = None
        return summary
    y = np.array([1 if row["label"] == "incorrect" else 0 for row in kept], dtype=int)
    qids = [row["question_id"] for row in kept]
    summary["positive_n"] = int(y.sum())
    summary["negative_n"] = int((1 - y).sum())
    metrics_for = {}
    for column in ("tre", "tre_effective"):
        scores = np.array([row[column] for row in kept], dtype=float)
        entry = {"n": len(y), "auroc": _auroc(y, scores)}
        if len(set(y.tolist())) == 2:
            entry.update(binary_metrics(y, scores))
            entry.update(grouped_bootstrap(y, scores, qids, repeats=bootstrap, seed=bootstrap_seed))
        metrics_for[column] = entry
    summary["main_metrics"] = metrics_for
    summary["main_metric"] = "tre"  # pre-registered in the plan; tre_effective is the robustness variant
    length_scores = np.array([float(row["effective_length"]) for row in kept])
    tail_scores = np.array([float(row["tail_tre"]) for row in kept])
    tail_share = np.array([float(row["tail_share"]) for row in kept])
    summary["diagnostic_auroc"] = {
        "effective_length": _auroc(y, length_scores),
        "tail_tre": _auroc(y, tail_scores),
        "tail_share": _auroc(y, tail_share),
        "note": "diagnostics only; direction not flipped, never used to pick the main metric",
    }
    terminations = {}
    for row in kept:
        terminations[row["termination"]] = terminations.get(row["termination"], 0) + 1
    lengths = np.array([row["effective_length"] for row in kept])
    summary["generation_diagnostics"] = {
        "termination_counts": terminations,
        "empty_answer_n": sum(1 for row in kept if row["effective_length"] == 0),
        "truncated_n": terminations.get("length_budget", 0),
        "effective_length_min": int(lengths.min()),
        "effective_length_median": float(np.median(lengths)),
        "effective_length_p95": float(np.quantile(lengths, 0.95)),
        "effective_length_max": int(lengths.max()),
        "tail_share_mean": float(np.nanmean(tail_share)) if np.isfinite(tail_share).any() else None,
        "tail_share_median": float(np.nanmedian(tail_share)) if np.isfinite(tail_share).any() else None,
    }
    return summary


def write_scores_csv(path: Path, rows: list[dict]) -> None:
    columns = ["sample_id", "question_id", "cluster_id", "split", "status", "label", "judge_first",
               "judge_second", "exclusion", "tre", "tre_effective", "tre_length_normalized", "tail_tre",
               "tail_share", "effective_length", "generation_length", "termination", "answer_type",
               "generated_text_sha256", "generated_text"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False, default=str) + "\n",
                    encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run", required=True, type=Path, help="trajectory run directory (traces/, manifest.json)")
    parser.add_argument("--questions", required=True, type=Path)
    parser.add_argument("--judgments", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--judge-prompt", type=Path, help="frozen judge prompt file; its SHA256 is recorded")
    parser.add_argument("--bootstrap", type=int, default=1000)
    parser.add_argument("--bootstrap-seed", type=int, default=GENERATION_SEED)
    parser.add_argument("--allow-synthetic", action="store_true", help="tests/fixtures only")
    parser.add_argument("--allow-partial", action="store_true",
                        help="do not fail when the main table is blocked; the reported subset is written explicitly")
    parser.add_argument("--allow-missing-answer-hash", action="store_true")
    args = parser.parse_args(argv)

    rows, config = collect_rows(args.run, args.questions, args.judgments,
                                allow_synthetic=args.allow_synthetic,
                                allow_missing_answer_hash=args.allow_missing_answer_hash)
    summary = summarize(rows, bootstrap=args.bootstrap, bootstrap_seed=args.bootstrap_seed)
    args.output.mkdir(parents=True, exist_ok=True)
    write_scores_csv(args.output / "scores.csv", rows)
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    payload = {
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "code_commit": git.stdout.strip() if git.returncode == 0 else None,
        "direction": "positive class = hallucinated/incorrect; higher score = higher risk",
        "pre_registered_main_metric": "tre (all generated positions); tre_effective is reported as a robustness variant",
        "run": str(args.run),
        "run_manifest_sha256": sha256_file(args.run / "manifest.json") if (args.run / "manifest.json").exists() else None,
        "questions": {"path": str(args.questions), "sha256": sha256_file(args.questions)},
        "judgments": {"path": str(args.judgments), "sha256": sha256_file(args.judgments),
                      "judge_prompt_sha256": sha256_file(args.judge_prompt) if args.judge_prompt else None},
        "decoding_config": config,
        "bootstrap": {"repeats": args.bootstrap, "seed": args.bootstrap_seed, "unit": "question_id"},
        "counts": summary,
    }
    write_json(args.output / "metrics.json", payload)
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
    if not summary["main_table_eligible"]:
        message = ("main table blocked: needs_review/unjudged/missing traces present "
                   f"({summary['needs_review_n']}/{summary['unjudged_n']}/{summary['missing_trace_n']}); "
                   "resolve or re-run the affected records, or use --allow-partial for an explicitly labelled subset")
        if not args.allow_partial:
            print("BLOCKED: " + message, file=sys.stderr)
            return 2
        print("PARTIAL: " + message, file=sys.stderr)
        payload["reported_subset"] = {"kept_n": summary["kept_n"], "main_metrics": summary["main_metrics"],
                                      "basis": "explicit user request (--allow-partial)"}
        write_json(args.output / "metrics.json", payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
