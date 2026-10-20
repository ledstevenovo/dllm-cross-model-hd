"""Unified QA-record schema for the cross-model hallucination study.

Every question that either model will ever be asked is represented by one
:class:`QARecord`.  The schema is the *contract* between the three stages of the
project:

* **data preparation** (this stage) fills the question-side fields;
* **trajectory collection** fills the generation-side fields defined in the
  experiment plan and stores them in the ``.npz`` payload, keyed by
  ``sample_id``;
* **feature extraction and detection** join on ``sample_id`` and must never need
  the raw parquet files again.

Because the split is frozen into the record, a model run cannot accidentally
evaluate on data the detector was fitted on: the analysis stage filters by the
``split`` field rather than re-deriving a split, which is the usual source of
train/test contamination in this kind of study.

``sample_id`` is stable and human-readable (``<dataset>__<raw_id>``), because it
becomes a filename in ``data/trajectories/{model}/{dataset}/{split}/{sample_id}.npz``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .prompts import (
    PROMPT_TEMPLATE_VERSION,
    assert_gold_not_in_prompt,
    prompt_fingerprint,
    render_prompt,
)
from .textnorm import normalize_question

__all__ = [
    "ALLOWED_SPLITS",
    "FIELD_ORDER",
    "RESEARCH_SPLITS",
    "SCHEMA_VERSION",
    "QARecord",
    "validate_records",
]

SCHEMA_VERSION = "qa-record-v1"

#: Splits used for the research itself.  ``train``/``validation`` fit the source
#: detector, ``test`` is the zero-shot transfer target.
RESEARCH_SPLITS: tuple[str, ...] = ("train", "validation", "test")

#: Every value the ``split`` field may take.  ``smoke`` is the engineering-only
#: carve-out (never used for any reported metric); ``unused`` marks an optional
#: archival pool that is deliberately excluded.
ALLOWED_SPLITS: tuple[str, ...] = RESEARCH_SPLITS + ("smoke", "unused")

#: Serialised field order.  Stable so that JSONL diffs stay readable.
FIELD_ORDER: tuple[str, ...] = (
    "schema_version",
    "sample_id",
    "question_id",
    "cluster_id",
    "dataset",
    "split",
    "question",
    "question_normalized",
    "gold_answer",
    "gold_aliases",
    "gold_normalized_aliases",
    "answer_type",
    "answer_source_field",
    "prompt",
    "prompt_template_version",
    "prompt_fingerprint",
    "source",
)


@dataclass(frozen=True, slots=True)
class QARecord:
    """One question, with its gold answer, frozen split and provenance."""

    sample_id: str
    question_id: str
    cluster_id: str
    dataset: str
    split: str
    question: str
    gold_answer: str
    gold_aliases: tuple[str, ...] = ()
    gold_normalized_aliases: tuple[str, ...] = ()
    answer_type: str = ""
    answer_source_field: str = ""
    source: Mapping[str, Any] = field(default_factory=dict)
    # Derived fields; filled by :meth:`finalize` when left empty.
    question_normalized: str = ""
    prompt: str = ""
    prompt_template_version: str = PROMPT_TEMPLATE_VERSION
    prompt_fingerprint: str = ""
    schema_version: str = SCHEMA_VERSION

    # -- construction -------------------------------------------------------
    def finalize(self) -> "QARecord":
        """Return a copy with every derived field filled in from the primitives.

        Deriving (never accepting) ``question_normalized``, ``prompt`` and
        ``prompt_fingerprint`` means a record can never describe a prompt other
        than the frozen one, so the record stays self-consistent even if the
        template is edited later -- at which point :meth:`problems` reports it.
        """
        from dataclasses import replace

        return replace(
            self,
            question_normalized=self.question_normalized or normalize_question(self.question),
            prompt=self.prompt or render_prompt(self.question),
            prompt_fingerprint=self.prompt_fingerprint or prompt_fingerprint(),
            prompt_template_version=self.prompt_template_version or PROMPT_TEMPLATE_VERSION,
        )

    # -- accessors ----------------------------------------------------------
    def gold_answers(self) -> tuple[str, ...]:
        """Return the gold value followed by every alias, de-duplicated.

        This is the full set the matcher may accept as "correct".  It is *not*
        normalised; the matcher normalises internally so that the stored
        strings stay human-readable.
        """
        seen: dict[str, None] = {}
        for value in (self.gold_answer, *self.gold_aliases):
            if value is not None and str(value).strip():
                seen.setdefault(str(value), None)
        return tuple(seen)

    # -- serialisation ------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-safe dict in :data:`FIELD_ORDER` order."""
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "sample_id": self.sample_id,
            "question_id": self.question_id,
            "cluster_id": self.cluster_id,
            "dataset": self.dataset,
            "split": self.split,
            "question": self.question,
            "question_normalized": self.question_normalized,
            "gold_answer": self.gold_answer,
            "gold_aliases": list(self.gold_aliases),
            "gold_normalized_aliases": list(self.gold_normalized_aliases),
            "answer_type": self.answer_type,
            "answer_source_field": self.answer_source_field,
            "prompt": self.prompt,
            "prompt_template_version": self.prompt_template_version,
            "prompt_fingerprint": self.prompt_fingerprint,
            "source": dict(self.source),
        }
        return {key: payload[key] for key in FIELD_ORDER}

    # -- validation ---------------------------------------------------------
    def problems(self, *, check_prompt: bool = True) -> list[str]:
        """Return a list of human-readable schema problems (empty means valid)."""
        issues: list[str] = []
        for name in ("sample_id", "question_id", "cluster_id", "dataset", "split", "question", "gold_answer"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                issues.append(f"{name} must be a non-empty string")
        if self.split not in ALLOWED_SPLITS:
            issues.append(f"split {self.split!r} is not one of {ALLOWED_SPLITS}")
        if self.schema_version != SCHEMA_VERSION:
            issues.append(f"schema_version {self.schema_version!r} != {SCHEMA_VERSION!r}")
        for index, alias in enumerate(self.gold_aliases):
            if not isinstance(alias, str) or not alias.strip():
                issues.append(f"gold_aliases[{index}] must be a non-empty string")
        if self.question_normalized != normalize_question(self.question):
            issues.append("question_normalized is not consistent with question")
        if check_prompt:
            if self.prompt != render_prompt(self.question):
                issues.append("prompt is not the frozen template rendered for this question")
            if self.prompt_fingerprint != prompt_fingerprint():
                issues.append("prompt_fingerprint does not match the frozen prompt")
            try:
                # Only the canonical value is guarded; an alias appearing in the
                # question is normally just the question's own wording and does
                # not make the item copyable.  See prompts.assert_gold_not_in_prompt.
                assert_gold_not_in_prompt(self.prompt, self.gold_answer)
            except AssertionError as exc:
                issues.append(str(exc))
        if not self.source:
            issues.append("source provenance must not be empty")
        return issues


def validate_records(
    records: Iterable[QARecord],
    *,
    check_prompt: bool = True,
    sample_id_uniqueness: bool = True,
) -> dict[str, Any]:
    """Validate a whole record stream and return a structured report.

    Returns a dict with ``checked``, ``problems`` (list of ``"<sample_id>: <issue>"``)
    and ``duplicate_sample_ids``.  The build script treats a non-empty problem
    list as a hard failure, so a schema drift cannot reach the artifacts.
    """
    problems: list[str] = []
    seen: set[str] = set()
    duplicates: list[str] = []
    checked = 0
    for record in records:
        checked += 1
        for issue in record.problems(check_prompt=check_prompt):
            problems.append(f"{record.sample_id or '<no id>'}: {issue}")
        if sample_id_uniqueness:
            if record.sample_id in seen:
                duplicates.append(record.sample_id)
            seen.add(record.sample_id)
    return {
        "checked": checked,
        "problems": problems,
        "duplicate_sample_ids": duplicates,
    }
