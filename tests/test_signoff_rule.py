"""The in-repo sign-off rule must reproduce the 400 reviewed pilot200 labels.

This is the guard that makes pool expansion legitimate: the expansion labels will
be produced by ``src.signoff_rule`` and then promoted by the same
``finalize_reviewed_labels.py``. If this test fails, the ported rule has drifted
from the rule a human actually signed off, and expansion must stop.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.signoff_rule import signoff_verdict, to_project_vocabulary

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "data/raw_qa/subsets/pilot200.jsonl"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_rule_reproduces_both_reviewed_label_files():
    questions = {row["question_id"]: row for row in read_jsonl(QUESTIONS)}
    total, mismatches = 0, []
    for model in ("llada", "dream"):
        generations = {row["question_id"]: row for row in
                       read_jsonl(ROOT / f"data/trajectories/bf16_pilot200/{model}/generations.jsonl")}
        reviewed = read_jsonl(ROOT / f"data/labels/pilot200_{model}.reviewed.jsonl")
        assert len(reviewed) == 200, f"{model}: expected 200 reviewed labels"
        for row in reviewed:
            question = questions[row["question_id"]]
            generation = generations[row["question_id"]]
            verdict, _ = signoff_verdict(
                question["gold_answer"], question.get("gold_aliases"),
                generation["generated_text"], row.get("refusal_detected", False), question["question"],
            )
            total += 1
            if to_project_vocabulary(verdict) != row["label"]:
                mismatches.append((model, row["question_id"], row["label"], verdict))
    assert total == 400
    assert not mismatches, f"{len(mismatches)} label(s) no longer reproduce: {mismatches[:5]}"


def test_rule_vocabulary_maps_into_the_project_vocabulary():
    reviewed_vocabulary = {"correct", "incorrect", "refusal_empty", "incomplete_truncated",
                           "format_failure", "needs_review"}
    raw_vocabulary = {"correct", "incorrect", "empty", "incomplete_truncated", "format_failure"}
    for verdict in raw_vocabulary:
        assert to_project_vocabulary(verdict) in reviewed_vocabulary


def test_rule_is_decisive():
    """No branch of the sign-off rule may leave an item unresolved."""
    verdict, _ = signoff_verdict("Paris", [], "Lyon", False, "Capital of France?")
    assert verdict == "incorrect"
    verdict, _ = signoff_verdict("Paris", [], "", False, "Capital of France?")
    assert to_project_vocabulary(verdict) == "refusal_empty"
