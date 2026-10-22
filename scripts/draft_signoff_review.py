#!/usr/bin/env python
"""Draft the sign-off review for any collected run, using the frozen rule.

This replaces the out-of-repo ``tools/pilot200_draft_review.py`` for new
collections. It writes two artefacts:

* ``<prefix>_<model>.draft_review.jsonl`` -- the tool-proposal fields kept from
  ``offline.py label`` plus the sign-off verdict, ``human_reviewed=false``;
  this is what ``finalize_reviewed_labels.py`` promotes after review;
* a Markdown table (``--sheet``) for the human to read.

The rule itself lives in ``src/signoff_rule.py`` and is pinned to reproduce the
400 reviewed pilot200 labels (``tests/test_signoff_rule.py``). Refuses to run if
that guarantee is broken, so expansion cannot silently use a drifted rule.

Usage:
  .venv/bin/python scripts/draft_signoff_review.py \
      --questions data/raw_qa/subsets/pool2000_v1_new.jsonl \
      --run-root data/trajectories/bf16_pool2000 \
      --prefix pool2000 \
      --sheet reports/pool2000_draft_review.md
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.signoff_rule import signoff_verdict, to_project_vocabulary  # noqa: E402

MODELS = ("llada", "dream")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def check_rule_against_pilot200() -> None:
    """Fail loudly if the in-repo rule no longer matches the signed-off labels."""
    questions = {row["question_id"]: row for row in read_jsonl(ROOT / "data/raw_qa/subsets/pilot200.jsonl")}
    checked = 0
    for model in MODELS:
        generations = {row["question_id"]: row for row in
                       read_jsonl(ROOT / f"data/trajectories/bf16_pilot200/{model}/generations.jsonl")}
        for row in read_jsonl(ROOT / f"data/labels/pilot200_{model}.reviewed.jsonl"):
            question = questions[row["question_id"]]
            verdict, _ = signoff_verdict(
                question["gold_answer"], question.get("gold_aliases"),
                generations[row["question_id"]]["generated_text"],
                row.get("refusal_detected", False), question["question"],
            )
            checked += 1
            if to_project_vocabulary(verdict) != row["label"]:
                raise SystemExit(
                    f"sign-off rule drifted: {model}/{row['question_id']} "
                    f"reviewed={row['label']} rule={verdict}; fix src/signoff_rule.py first"
                )
    if checked != 400:
        raise SystemExit(f"expected 400 reference labels, checked {checked}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--run-root", required=True, help="directory with <model>/generations.jsonl")
    parser.add_argument("--prefix", required=True, help="output label file prefix, e.g. pool2000")
    parser.add_argument("--proposals-prefix", default=None,
                        help="prefix of the existing <prefix>_<model>.proposals.jsonl (default: same as --prefix)")
    parser.add_argument("--labels-dir", default=str(ROOT / "data/labels"), help="where to write labels")
    parser.add_argument("--proposals-dir", default=str(ROOT / "data/labels"),
                        help="where to read <prefix>_<model>.proposals.jsonl from")
    parser.add_argument("--sheet", default=None, help="optional Markdown review sheet")
    parser.add_argument("--max-rows", type=int, default=0, help="limit sheet rows (0 = all)")
    args = parser.parse_args()

    check_rule_against_pilot200()

    questions = {row["question_id"]: row for row in read_jsonl(Path(args.questions))}
    labels_dir = Path(args.labels_dir)
    labels_dir.mkdir(parents=True, exist_ok=True)
    sheet = ["# 签核复核表（draft，human_reviewed=false）", "",
             f"规则：`src/signoff_rule.py`（已对 pilot200 400/400 复现）；题单：`{args.questions}`", ""]
    summary: dict = {"rule": "src/signoff_rule.py", "questions": args.questions, "models": {}}

    for model in MODELS:
        run = Path(args.run_root) / model
        generations = read_jsonl(run / "generations.jsonl")
        prefix = args.proposals_prefix or args.prefix
        proposals_path = Path(args.proposals_dir) / f"{prefix}_{model}.proposals.jsonl"
        proposals = {row["sample_id"]: row for row in read_jsonl(proposals_path)} if proposals_path.exists() else {}

        rows, counts = [], Counter()
        for generation in generations:
            question = questions[generation["question_id"]]
            proposal = proposals.get(generation["sample_id"], {})
            # The refusal flag comes from the tool proposal, not from the generation
            # record: the signed-off review used exactly that value.
            refusal = bool(proposal.get("refusal_detected", False))
            verdict, reason = signoff_verdict(
                question["gold_answer"], question.get("gold_aliases"),
                generation["generated_text"], refusal, question["question"],
            )
            label = to_project_vocabulary(verdict)
            counts[label] += 1
            rows.append({
                **proposal,
                "sample_id": generation["sample_id"],
                "question_id": generation["question_id"],
                "model_id": generation["model_id"],
                "label": label,
                "label_source": f"signoff-rule:{verdict}",
                "human_reviewed": False,
                "notes": reason,
                "signoff_reason": reason,
                "candidate": generation["generated_text"],
            })

        out = labels_dir / f"{args.prefix}_{model}.draft_review.jsonl"
        out.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
        summary["models"][model] = {"rows": len(rows), "labels": dict(counts), "out": str(out)}
        print(f"{model}: {len(rows)} rows {dict(counts)} -> {out}")

        if args.sheet:
            shown = rows[:args.max_rows] if args.max_rows else rows
            sheet += [f"## {model}（{len(rows)} 条；correct {counts.get('correct', 0)}）", "",
                      "| # | split | question | gold | prediction | 判定 | 说明 |", "|---|---|---|---|---|---|---|"]
            for index, row in enumerate(shown, 1):
                question = questions[row["question_id"]]
                sheet.append(
                    f"| {index} | {question['split']} | {question['question'][:60]} | "
                    f"{str(question['gold_answer'])[:24]} | {row['candidate'][:50]!r} | "
                    f"{row['label']} | {row['signoff_reason'][:30]} |"
                )
            sheet.append("")

    if args.sheet:
        path = Path(args.sheet)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(sheet), encoding="utf-8")
        print(f"sheet -> {path}")

    manifest_path = labels_dir / f"{args.prefix}_draft_manifest.json"
    manifest_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"manifest -> {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
