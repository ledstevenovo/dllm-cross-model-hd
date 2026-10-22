"""Contract tests for the TRE-reproduction question lists and the scoring entry point."""

import json

import numpy as np
import pytest

from src.trace_schema import REQUIRED, save_trace
from src.tre_repro import (
    GENERATION_SEED,
    TRE_PROMPT_VERSION_CONTEXT,
    TRE_REPRO_SCHEMA_VERSION,
    bare_prompt,
    build_record,
    context_prompt,
    load_questions,
    prompt_fingerprint,
    render_context,
    sample_id_for,
    validate_questions,
)
from scripts.score_tre_repro import collect_rows, summarize


def pool_row(question_id="triviaqa__q1", question="Which city hosts the Eiffel Tower?"):
    return {
        "question_id": question_id,
        "cluster_id": question_id,
        "dataset": "triviaqa",
        "question": question,
        "gold_answer": "Paris",
        "gold_aliases": ["Paris, France"],
        "gold_normalized_aliases": ["paris"],
        "answer_type": "WikipediaEntity",
        "answer_source_field": "answer.value",
        "source": {"hf_config": "rc.nocontext", "hf_split": "validation"},
    }


PROVENANCE = {
    "pool_file": "data/raw_qa/triviaqa/test.jsonl",
    "pool_sha256": "0" * 64,
    "selection_seed": 20261021,
    "selection_rank": 0,
    "source_split": "validation",
    "source_config": "rc.nocontext",
}


def write_questions(tmp_path, records):
    path = tmp_path / "questions.jsonl"
    path.write_text("".join(json.dumps(r.to_dict(), ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    return path


def test_record_contract_and_bare_prompt(tmp_path):
    record = build_record(pool_row(), split="test", provenance=PROVENANCE)
    payload = record.to_dict()
    assert payload["schema_version"] == TRE_REPRO_SCHEMA_VERSION
    assert payload["sample_id"] == sample_id_for("triviaqa__q1") == "triviaqa__q1__seed20261021"
    assert payload["prompt"] == bare_prompt("Which city hosts the Eiffel Tower?") == payload["question"]
    assert payload["prompt_fingerprint"] == prompt_fingerprint(payload["prompt"])
    assert validate_questions([record])["problems"] == []
    loaded = load_questions(write_questions(tmp_path, [record]))
    assert loaded[0].to_dict() == payload


def test_record_rejects_copyable_gold_and_bad_sample_id():
    from dataclasses import replace

    record = build_record(pool_row(question="In which year did the War of 1812 start?"), split="test",
                          provenance=PROVENANCE)
    copyable = replace(record, gold_answer="1812")
    assert any("appears in the question" in issue for issue in copyable.problems())
    broken = replace(record, gold_answer="Paris", sample_id="triviaqa__q1__seed1")
    assert any("collector contract" in issue for issue in broken.problems())


CONTEXT = "Eliot Cutler: Eliot Cutler is an American lawyer.\n\nFarid Khavari: He ran for governor."


def test_context_record_uses_its_own_prompt_style_and_round_trips(tmp_path):
    record = build_record(pool_row(), split="test", provenance=PROVENANCE, context=CONTEXT)
    payload = record.to_dict()

    assert payload["context"] == CONTEXT
    assert payload["prompt_template_version"] == TRE_PROMPT_VERSION_CONTEXT
    assert payload["prompt"] == context_prompt(CONTEXT, payload["question"])
    assert payload["prompt"] != payload["question"]
    assert payload["prompt_fingerprint"] == prompt_fingerprint(payload["prompt"], style=TRE_PROMPT_VERSION_CONTEXT)
    assert validate_questions([record])["problems"] == []
    assert load_questions(write_questions(tmp_path, [record]))[0].to_dict() == payload


def test_context_record_does_not_reject_a_gold_answer_that_lives_in_the_context():
    # HotpotQA answers are *supposed* to be in the distractor paragraphs; only a
    # gold answer visible in the question itself means the item is copyable.
    record = build_record(pool_row(question="Which city hosts the Eiffel Tower?"), split="test",
                          provenance=PROVENANCE, context="Paris: Paris is the capital of France.")
    assert validate_questions([record])["problems"] == []


def test_loader_rejects_a_prompt_that_does_not_round_trip(tmp_path):
    record = build_record(pool_row(), split="test", provenance=PROVENANCE, context=CONTEXT)
    payload = record.to_dict()
    payload["prompt"] = payload["prompt"].replace("only", "ONLY")
    path = tmp_path / "questions.jsonl"
    path.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="prompt does not round-trip"):
        load_questions(path)


def test_loader_rejects_a_stale_prompt_fingerprint(tmp_path):
    record = build_record(pool_row(), split="test", provenance=PROVENANCE, context=CONTEXT)
    payload = record.to_dict()
    payload["prompt_fingerprint"] = "sha256:" + "0" * 64
    path = tmp_path / "questions.jsonl"
    path.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="prompt_fingerprint mismatch"):
        load_questions(path)


def test_render_context_is_stable_and_rejects_empty_input():
    rendered = render_context(["A", "B"], [["one.", "two."], ["three."]])
    assert rendered == "A: one. two.\n\nB: three."
    with pytest.raises(ValueError):
        render_context([], [])
    with pytest.raises(ValueError):
        render_context(["A"], [["x"], ["y"]])


def test_question_file_rejects_duplicates(tmp_path):
    record = build_record(pool_row(), split="test", provenance=PROVENANCE)
    path = write_questions(tmp_path, [record, record])
    with pytest.raises(ValueError, match="invalid question file"):
        load_questions(path)


def trace_meta(sample_id, question_id, question, *, effective_length, termination, seed=GENERATION_SEED):
    meta = {key: "fixture" for key in REQUIRED}
    meta.update(
        sample_id=sample_id,
        question_id=question_id,
        dataset="triviaqa",
        split="test",
        model_id="fixture-llada",
        checkpoint_revision="fixture-revision",
        tokenizer_revision="fixture-tokenizer",
        code_commit="fixture-commit",
        prompt=question,
        precision="float16",
        gen_length=4,
        steps=2,
        block_size=4,
        effective_length=effective_length,
        termination=termination,
        vocab_size=1000000,
        environment={"python": "fixture"},
        temperature=0.0,
        seed=seed,
        synthetic=True,
    )
    return meta


def trace_arrays(entropy_scale=1.0, effective_length=2):
    entropy = np.array([[2.0, 4.0, 1.0, 1.0], [1.0, 3.0, 2.0, 1.0]]) * entropy_scale
    return {
        "entropy": entropy,
        "top1_probability": np.full((2, 4), 0.5),
        "mask_before": np.array([[True, True, True, True], [False, True, True, True]]),
        "revealed": np.array([[True, False, False, False], [False, True, True, True]]),
        "final_tokens": np.array([10, 11, 12, 13]),
    }


def build_run(tmp_path, sample_ids, scales=None):
    run = tmp_path / "run"
    (run / "traces").mkdir(parents=True)
    for index, (sample_id, question_id, question) in enumerate(sample_ids):
        meta = trace_meta(sample_id, question_id, question, effective_length=2, termination="eot")
        scale = 1.0 if scales is None else float(scales[index])
        save_trace(run / "traces" / f"{index}.npz", meta, trace_arrays(entropy_scale=scale))
    (run / "manifest.json").write_text("{}\n", encoding="utf-8")
    return run


def judgment(sample_id, text_sha, first, second=None, status="done"):
    payload = {"sample_id": sample_id, "question_id": "triviaqa__q" + sample_id[-1], "status": status,
               "judge_first": first, "generated_text_sha256": text_sha}
    if second is not None:
        payload["judge_second"] = second
    return payload


def test_scoring_keeps_flips_and_reports_metrics(tmp_path):
    from scripts.score_tre_repro import sha256_text

    questions = [build_record(pool_row(f"triviaqa__q{i}", f"Question number {i}?"), split="test",
                              provenance={**PROVENANCE, "selection_rank": i}) for i in range(1, 5)]
    path = write_questions(tmp_path, questions)
    # q2 is judged incorrect and carries the largest TRE -> a perfect ranking is expected.
    run = build_run(tmp_path, [(q.sample_id, q.question_id, q.question) for q in questions],
                    scales=[1.0, 3.0, 2.0, 1.5])
    text_sha = sha256_text("fixture")
    judgments = tmp_path / "judgments.jsonl"
    rows = [
        judgment("triviaqa__q1__seed20261021", text_sha, "correct"),
        judgment("triviaqa__q2__seed20261021", text_sha, "incorrect", "incorrect"),
        judgment("triviaqa__q3__seed20261021", text_sha, "incorrect", "correct"),
        judgment("triviaqa__q4__seed20261021", text_sha, "correct"),
    ]
    judgments.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    table, config = collect_rows(run, path, judgments, allow_synthetic=True, allow_missing_answer_hash=True)
    summary = summarize(table, bootstrap=50, bootstrap_seed=1)
    assert config["gen_length"] == 4 and config["seed"] == GENERATION_SEED
    assert summary["initial_n"] == 4 and summary["kept_n"] == 3 and summary["dropped_n"] == 1
    assert summary["judge_flip_n"] == 1 and summary["main_table_eligible"] is True
    assert summary["positive_n"] == 1 and summary["negative_n"] == 2
    assert summary["main_metrics"]["tre"]["auroc"] == 1.0
    assert "diagnostic_auroc" in summary and "generation_diagnostics" in summary


def test_scoring_blocks_on_missing_or_unreviewed(tmp_path):
    from scripts.score_tre_repro import sha256_text

    questions = [build_record(pool_row(f"triviaqa__q{i}", f"Question number {i}?"), split="test",
                              provenance={**PROVENANCE, "selection_rank": i}) for i in range(1, 4)]
    path = write_questions(tmp_path, questions)
    run = build_run(tmp_path, [(q.sample_id, q.question_id, q.question) for q in questions])
    text_sha = sha256_text("fixture")
    judgments = tmp_path / "judgments.jsonl"
    rows = [
        judgment("triviaqa__q1__seed20261021", text_sha, "correct"),
        judgment("triviaqa__q2__seed20261021", text_sha, None, status="needs_review"),
    ]
    judgments.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    table, _ = collect_rows(run, path, judgments, allow_synthetic=True, allow_missing_answer_hash=True)
    summary = summarize(table, bootstrap=20, bootstrap_seed=1)
    assert summary["needs_review_n"] == 1 and summary["unjudged_n"] == 1
    assert summary["main_table_eligible"] is False
    assert summary["kept_n"] == 1


def test_scoring_rejects_unbound_judgment_and_wrong_prompt(tmp_path):
    questions = [build_record(pool_row("triviaqa__q1", "Question number 1?"), split="test", provenance=PROVENANCE)]
    path = write_questions(tmp_path, questions)
    run = build_run(tmp_path, [(questions[0].sample_id, questions[0].question_id, questions[0].question)])
    judgments = tmp_path / "judgments.jsonl"
    judgments.write_text(json.dumps(judgment("triviaqa__q1__seed20261021", "deadbeef", "correct")) + "\n",
                         encoding="utf-8")
    with pytest.raises(ValueError, match="not bound to this generation"):
        collect_rows(run, path, judgments, allow_synthetic=True)
    # wrong prompt in the trace is caught before any metric is computed
    (run / "traces" / "0.npz").unlink()
    meta = trace_meta(questions[0].sample_id, questions[0].question_id, "A different question?",
                      effective_length=2, termination="eot")
    save_trace(run / "traces" / "0.npz", meta, trace_arrays())
    with pytest.raises(ValueError, match="prompt mismatch"):
        collect_rows(run, path, judgments, allow_synthetic=True, allow_missing_answer_hash=True)
