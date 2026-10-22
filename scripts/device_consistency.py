#!/usr/bin/env python
"""Cross-device consistency audit for two collections of the SAME questions.

Motivation: pilot200 was collected on a 4080 SUPER (sm_89); the migration to a
5090 (sm_120) reruns the identical config. BF16 is not bit-reproducible across
architectures, so this script quantifies what that means for the study:

1. generation identity  -- final token IDs per question;
2. answer validity      -- effective length / termination;
3. label stability      -- re-run the project's rule labeler on the new text and
                           compare with the reviewed labels of the reference run;
4. feature drift        -- per-feature relative change of the trace statistics.

Read-only on both collections. Nothing here is used to pick a "nicer" run: the
reference collection stays the analysis input; this reports the risk explicitly.

Usage:
  .venv/bin/python scripts/device_consistency.py \
      --reference data/trajectories/bf16_pilot200 \
      --candidate /root/autodl-tmp/probe5090/pilot200_5090 \
      --questions data/raw_qa/subsets/pilot200.jsonl \
      --labels data/labels \
      --out reports/device_consistency_pilot200.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from src.labeling import extract_candidate, normalize_answer  # noqa: E402
from src.signoff_rule import signoff_verdict, to_project_vocabulary  # noqa: E402
from src.trace_schema import extract_features, load_trace  # noqa: E402

MODEL_DIR = {"llada": "llada", "dream": "dream"}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def index_run(root: Path) -> dict[str, dict]:
    manifest = json.loads((root / "manifest.json").read_text())
    return {rec["question_id"]: {"path": root / rec["path"], "sample_id": sid}
            for sid, rec in manifest["samples"].items()}


def index_generations(root: Path) -> dict[str, dict]:
    path = root / "generations.jsonl"
    if not path.exists():
        return {}
    return {row["question_id"]: row for row in read_jsonl(path)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True, help="reference collection root (has <model>/ manifest.json)")
    parser.add_argument("--candidate", required=True, help="candidate collection root")
    parser.add_argument("--questions", required=True)
    parser.add_argument("--labels", default=str(ROOT / "data/labels"),
                        help="directory with <run>_<model>.reviewed.jsonl")
    parser.add_argument("--reference-label-prefix", default="pilot200")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    ref_root, cand_root = Path(args.reference), Path(args.candidate)
    qa = {row["question_id"]: row for row in read_jsonl(Path(args.questions))}
    report: dict = {"reference": str(ref_root), "candidate": str(cand_root), "models": {}}

    for model in MODEL_DIR:
        ref, cand = index_run(ref_root / model), index_run(cand_root / model)
        common = sorted(set(ref) & set(cand))
        if not common:
            report["models"][model] = {"error": "no common questions"}
            continue

        label_path = Path(args.labels) / f"{args.reference_label_prefix}_{model}.reviewed.jsonl"
        reviewed = {row["question_id"]: row for row in read_jsonl(label_path)} if label_path.exists() else {}
        cand_generations = index_generations(cand_root / model)
        ref_generations = index_generations(ref_root / model)

        identical, lengths, text_changes, flips, feature_rel = 0, [], [], [], []
        rows = []
        for qid in common:
            ref_meta, ref_arrays = load_trace(ref[qid]["path"])
            cand_meta, cand_arrays = load_trace(cand[qid]["path"])
            same = bool(np.array_equal(ref_arrays["final_tokens"], cand_arrays["final_tokens"]))
            identical += int(same)

            ref_len, cand_len = ref_meta["effective_length"], cand_meta["effective_length"]
            lengths.append((ref_len, cand_len))

            row = {
                "question_id": qid,
                "tokens_identical": same,
                "n_token_diffs": int((ref_arrays["final_tokens"] != cand_arrays["final_tokens"]).sum()),
                "reference_effective_length": ref_len,
                "candidate_effective_length": cand_len,
                "reference_termination": ref_meta["termination"],
                "candidate_termination": cand_meta["termination"],
            }

            ref_features = extract_features(ref_meta, ref_arrays)
            cand_features = extract_features(cand_meta, cand_arrays)
            for name, value in ref_features.items():
                if isinstance(value, (int, float)) and abs(value) > 1e-9:
                    other = cand_features.get(name)
                    if isinstance(other, (int, float)):
                        feature_rel.append(abs(other - value) / abs(value))
            row["tre_reference"] = round(float(ref_features["tre"]), 6)
            row["tre_candidate"] = round(float(cand_features["tre"]), 6)

            if qid in reviewed and qid in cand_generations:
                question = qa[qid]
                generation = cand_generations[qid]
                reference_text = ref_generations.get(qid, {}).get("generated_text", "")
                ref_candidate = normalize_answer(extract_candidate(reference_text))
                cand_candidate = normalize_answer(extract_candidate(generation["generated_text"]))
                row["reference_text"] = reference_text
                row["candidate_text"] = generation["generated_text"]
                row["candidate_answer_identical"] = ref_candidate == cand_candidate
                row["reviewed_label"] = reviewed[qid]["label"]
                text_changes.append(not row["candidate_answer_identical"])

                # Label stability is the number that matters: score BOTH texts with the
                # frozen sign-off rule (never with the reviewed label alone), so a device
                # difference and a rule difference cannot be confused.
                ref_verdict, _ = signoff_verdict(
                    question["gold_answer"], question.get("gold_aliases"), reference_text,
                    bool(reviewed[qid].get("refusal_detected", False)), question["question"])
                cand_verdict, _ = signoff_verdict(
                    question["gold_answer"], question.get("gold_aliases"), generation["generated_text"],
                    bool(reviewed[qid].get("refusal_detected", False)), question["question"])
                row["signoff_label_reference_text"] = to_project_vocabulary(ref_verdict)
                row["signoff_label_candidate_text"] = to_project_vocabulary(cand_verdict)
                flips.append(row["signoff_label_reference_text"] != row["signoff_label_candidate_text"])
            rows.append(row)

        length_deltas = [c - r for r, c in lengths]
        report["models"][model] = {
            "questions": len(common),
            "final_tokens_identical": identical,
            "final_tokens_identical_rate": round(identical / len(common), 4),
            "effective_length_delta": {
                "mean": round(float(np.mean(length_deltas)), 3),
                "max_abs": int(np.max(np.abs(length_deltas))),
                "changed": int(sum(1 for d in length_deltas if d != 0)),
            },
            "answer_text": {
                "compared": len(text_changes),
                "changed": int(sum(text_changes)),
                "changed_rate": round(float(np.mean(text_changes)), 4) if text_changes else None,
            },
            "label_flips_signoff_rule": {
                "compared": len(flips),
                "changed": int(sum(flips)),
                "changed_rate": round(float(np.mean(flips)), 4) if flips else None,
            },
            "feature_relative_change": {
                "median": round(float(np.median(feature_rel)), 5) if feature_rel else None,
                "p90": round(float(np.percentile(feature_rel, 90)), 5) if feature_rel else None,
                "max": round(float(np.max(feature_rel)), 5) if feature_rel else None,
            },
            "rows": rows,
        }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for model, data in report["models"].items():
        if "error" in data:
            print(f"{model}: {data['error']}")
            continue
        print(f"{model}: n={data['questions']} identical={data['final_tokens_identical']} "
              f"({data['final_tokens_identical_rate']:.1%}) "
              f"len_changed={data['effective_length_delta']['changed']} "
              f"answer_text_changed={data['answer_text']['changed']}/{data['answer_text']['compared']} "
              f"label_flips={data['label_flips_signoff_rule']['changed']}/{data['label_flips_signoff_rule']['compared']} "
              f"feature_rel_median={data['feature_relative_change']['median']}")
    print(f"written {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
