"""TRE reproduction (v3) question contract, prompt style and label schema.

Why this module exists instead of reusing :mod:`src.schema`: the frozen
cross-model study contract pins *one* prompt template (v1, an explicit short-answer
instruction) and :meth:`src.schema.QARecord.problems` rejects any record whose
``prompt`` is not that template.  The TRE reproduction deliberately uses the
bare-question prompt (v3 decision ③: the question text alone, wrapped once by the
model's own chat template at collection time), so it needs its own -- much smaller
-- record contract.  Keeping it separate means the frozen mainline artifacts stay
byte-identical and cannot drift.

Contracts fixed here (see ``docs/TRE_4080SUPER_32GB_复现方案.md`` §4.2):

* ``sample_id == question_id + '__seed' + str(GENERATION_SEED)`` -- the collector
  derives sample IDs itself and ignores whatever the question file carries, so
  the file must already agree with :func:`sample_id_for`.
* ``prompt`` is exactly the trimmed question; nothing is prepended or appended.
* Provenance lives in ``provenance``: which pool file/row the question came from,
  that pool's SHA256, the selection seed and rank, and the upstream HF
  config/split (``rc.nocontext`` / ``validation``).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .prompts import answer_in_prompt
from .textnorm import normalize_question

__all__ = [
    "GENERATION_SEED",
    "QUESTION_FIELD_ORDER",
    "TRE_PROMPT_STYLE",
    "TRE_PROMPT_STYLE_CONTEXT",
    "TRE_PROMPT_VERSION",
    "TRE_PROMPT_VERSION_CONTEXT",
    "TRE_REPRO_SCHEMA_VERSION",
    "TreQuestion",
    "bare_prompt",
    "build_record",
    "context_prompt",
    "load_questions",
    "prompt_fingerprint",
    "render_context",
    "sample_id_for",
    "validate_questions",
]

TRE_REPRO_SCHEMA_VERSION = "tre-repro-question-v3"

#: Bare-question prompt style, recorded verbatim in every record and in the run
#: manifest.  Any future prompt experiment gets a new version string, never an
#: edit of this one.
TRE_PROMPT_VERSION = "v3-bare-question"
TRE_PROMPT_STYLE = (
    "bare question only; the model's own chat template is applied exactly once "
    "at collection time; no instruction prefix, no answer tags, no context"
)

#: HotpotQA prompt style for R2.  HotpotQA questions are unanswerable without the
#: distractor paragraphs, so the context has to be in the prompt; the instruction
#: says to use only that context, which is the standard HotpotQA protocol.  A new
#: version string, never an edit of v3 -- the R1 files must keep serialising
#: byte-identically.
TRE_PROMPT_VERSION_CONTEXT = "v4-hotpotqa-context"
TRE_PROMPT_STYLE_CONTEXT = (
    "context-grounded question: the distractor paragraphs are rendered as "
    "'Title: sentences' blocks, followed by the question; the model's own chat "
    "template is applied exactly once at collection time"
)

#: Generation seed for the TRE reproduction.  It fixes ``sample_id`` and is passed
#: explicitly to the collector (``--seed``); it is *not* the data sampling seed,
#: which lives in the questions manifest.
GENERATION_SEED = 20261021

QUESTION_FIELD_ORDER: tuple[str, ...] = (
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
    "provenance",
)

ALLOWED_SPLITS: tuple[str, ...] = ("test", "smoke")


def sample_id_for(question_id: str) -> str:
    """Return the collector-contract sample ID for one question."""
    if not isinstance(question_id, str) or not question_id.strip():
        raise ValueError("question_id must be a non-empty string")
    return f"{question_id}__seed{GENERATION_SEED}"


def bare_prompt(question: str) -> str:
    """Return the prompt ③ text for one question: the question, nothing else."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("bare_prompt requires a non-empty question string")
    return question.strip()


def render_context(titles: Iterable[str], sentences: Iterable[Iterable[str]]) -> str:
    """Render HotpotQA paragraphs as ``Title: s1 s2`` blocks separated by blank lines.

    The distractor paragraphs arrive as parallel lists of titles and per-title
    sentence lists.  A stable rendering matters more than a pretty one: the exact
    text is fingerprinted into every question record, so any change is a new
    prompt version rather than a silent drift.
    """
    titles = list(titles)
    sentences = list(sentences)
    if len(titles) != len(sentences):
        raise ValueError("context titles and sentences must have the same length")
    blocks = []
    for title, group in zip(titles, sentences):
        if not str(title).strip():
            raise ValueError("context paragraph has an empty title")
        blocks.append(f"{str(title).strip()}: {' '.join(str(s).strip() for s in group if str(s).strip())}")
    if not blocks:
        raise ValueError("context must have at least one paragraph")
    return "\n\n".join(blocks)


def context_prompt(context: str, question: str) -> str:
    """Return the R2 prompt text: context-grounded question, context first."""
    if not isinstance(context, str) or not context.strip():
        raise ValueError("context_prompt requires a non-empty context")
    if not isinstance(question, str) or not question.strip():
        raise ValueError("context_prompt requires a non-empty question")
    return (
        "Answer the question using only the context below.\n\n"
        f"Context:\n{context.strip()}\n\n"
        f"Question: {question.strip()}\nAnswer:"
    )


def prompt_fingerprint(prompt: str, *, style: str = TRE_PROMPT_VERSION) -> str:
    """Return ``sha256:<hex>`` over the prompt style version and the prompt text.

    Hashing the version too means a style change is visible even when a single
    prompt string happens to repeat.
    """
    payload = f"{style}\x1f{prompt}".encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True, slots=True)
class TreQuestion:
    """One TRE-reproduction question with its prompt and provenance.

    ``context`` is empty for R1 (TriviaQA, bare-question prompt ③).  R2 adds
    HotpotQA, whose protocol needs the distractor paragraphs in the prompt, so the
    record carries them explicitly: the prompt is then *composed* and its style
    version differs.  Keeping ``context`` on the record rather than baking the
    text into ``question`` means the question stays comparable across protocols,
    and the frozen R1 files serialise exactly as before (no new keys, because the
    field order only gains an entry when a context is present).
    """

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
    provenance: Mapping[str, Any] = field(default_factory=dict)
    context: str = ""

    @property
    def prompt(self) -> str:
        """The exact text handed to the model (before its chat template)."""
        if self.context:
            return context_prompt(self.context, self.question)
        return bare_prompt(self.question)

    @property
    def prompt_style(self) -> str:
        return TRE_PROMPT_VERSION_CONTEXT if self.context else TRE_PROMPT_VERSION

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": TRE_REPRO_SCHEMA_VERSION,
            "sample_id": self.sample_id,
            "question_id": self.question_id,
            "cluster_id": self.cluster_id,
            "dataset": self.dataset,
            "split": self.split,
            "question": self.question,
            "question_normalized": normalize_question(self.question),
            "gold_answer": self.gold_answer,
            "gold_aliases": list(self.gold_aliases),
            "gold_normalized_aliases": list(self.gold_normalized_aliases),
            "answer_type": self.answer_type,
            "answer_source_field": self.answer_source_field,
            "prompt": self.prompt,
            "prompt_template_version": self.prompt_style,
            "prompt_fingerprint": prompt_fingerprint(self.prompt, style=self.prompt_style),
            "source": dict(self.source or {}),
            "provenance": dict(self.provenance or {}),
        }
        if self.context:
            payload["context"] = self.context
            order = QUESTION_FIELD_ORDER + ("context",)
        else:
            order = QUESTION_FIELD_ORDER
        return {key: payload[key] for key in order}

    def problems(self) -> list[str]:
        """Return schema problems for this record (empty list means valid)."""
        issues: list[str] = []
        for name in ("sample_id", "question_id", "cluster_id", "dataset", "split", "question", "gold_answer"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                issues.append(f"{name} must be a non-empty string")
        if self.split not in ALLOWED_SPLITS:
            issues.append(f"split {self.split!r} is not one of {ALLOWED_SPLITS}")
        if self.sample_id != sample_id_for(self.question_id):
            issues.append("sample_id does not follow the collector contract question_id__seed<GENERATION_SEED>")
        if self.context:
            if context_prompt(self.context, self.question) != self.prompt:
                issues.append("context prompt is not reproducible from context + question")
        elif bare_prompt(self.question) != self.question.strip():
            issues.append("prompt must be the bare question")
        if answer_in_prompt(self.question, self.gold_answer):
            # The pool was already filtered for copyable answers; this is a guard
            # against importing records from somewhere else.  Checked against the
            # *question* even when a context is present: a gold answer that is
            # copyable from the question is a broken item either way, while an
            # answer present in the context is exactly what HotpotQA is.
            issues.append("gold answer appears in the question (copyable item)")
        if not self.source:
            issues.append("source provenance must not be empty")
        for key in ("pool_file", "pool_sha256", "selection_seed", "selection_rank", "source_split", "source_config"):
            if key not in (self.provenance or {}):
                issues.append(f"provenance.{key} is required")
        return issues


def build_record(pool_row: Mapping[str, Any], *, split: str, provenance: Mapping[str, Any],
                 context: str = "") -> TreQuestion:
    """Build one :class:`TreQuestion` from a pool row (``data/raw_qa/...`` JSONL)."""
    if split not in ALLOWED_SPLITS:
        raise ValueError(f"split must be one of {ALLOWED_SPLITS}")
    question_id = pool_row["question_id"]
    return TreQuestion(
        sample_id=sample_id_for(question_id),
        question_id=question_id,
        cluster_id=pool_row["cluster_id"],
        dataset=pool_row["dataset"],
        split=split,
        question=pool_row["question"],
        gold_answer=pool_row["gold_answer"],
        gold_aliases=tuple(pool_row.get("gold_aliases") or ()),
        gold_normalized_aliases=tuple(pool_row.get("gold_normalized_aliases") or ()),
        answer_type=str(pool_row.get("answer_type") or ""),
        answer_source_field=str(pool_row.get("answer_source_field") or ""),
        source=dict(pool_row.get("source") or {}),
        provenance=dict(provenance),
        context=context,
    )


def validate_questions(records: Iterable[TreQuestion]) -> dict[str, Any]:
    """Validate a whole question stream; returns ``checked``/``problems``/``duplicates``."""
    problems: list[str] = []
    seen_sample: set[str] = set()
    seen_question: set[str] = set()
    duplicates: list[str] = []
    checked = 0
    for record in records:
        checked += 1
        for issue in record.problems():
            problems.append(f"{record.sample_id}: {issue}")
        if record.sample_id in seen_sample:
            duplicates.append(record.sample_id)
        seen_sample.add(record.sample_id)
        seen_question.add(record.question_id)
    return {
        "checked": checked,
        "unique_sample_ids": len(seen_sample),
        "unique_question_ids": len(seen_question),
        "problems": problems,
        "duplicate_sample_ids": duplicates,
    }


def load_questions(path: str | Path) -> list[TreQuestion]:
    """Load and validate a ``data/tre_repro/questions/*.jsonl`` file."""
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    records = [
        TreQuestion(
            sample_id=row["sample_id"],
            question_id=row["question_id"],
            cluster_id=row["cluster_id"],
            dataset=row["dataset"],
            split=row["split"],
            question=row["question"],
            gold_answer=row["gold_answer"],
            gold_aliases=tuple(row.get("gold_aliases") or ()),
            gold_normalized_aliases=tuple(row.get("gold_normalized_aliases") or ()),
            answer_type=str(row.get("answer_type") or ""),
            answer_source_field=str(row.get("answer_source_field") or ""),
            source=dict(row.get("source") or {}),
            provenance=dict(row.get("provenance") or {}),
            context=str(row.get("context") or ""),
        )
        for row in rows
    ]
    report = validate_questions(records)
    if report["problems"] or report["duplicate_sample_ids"]:
        raise ValueError("invalid question file: " + "; ".join((report["problems"] + report["duplicate_sample_ids"])[:5]))
    if [r.to_dict()["schema_version"] for r in records] != [TRE_REPRO_SCHEMA_VERSION] * len(records):
        raise ValueError("schema_version mismatch")
    # The prompt must round-trip: a file whose stored prompt disagrees with the
    # text rebuilt from question+context would collect something other than what
    # its fingerprint claims.
    for row, record in zip(rows, records):
        if row.get("prompt") != record.prompt:
            raise ValueError(f"prompt does not round-trip for {record.sample_id}")
        if row.get("prompt_template_version") != record.prompt_style:
            raise ValueError(f"prompt_template_version mismatch for {record.sample_id}")
        if row.get("prompt_fingerprint") != prompt_fingerprint(record.prompt, style=record.prompt_style):
            raise ValueError(f"prompt_fingerprint mismatch for {record.sample_id}")
    return records
