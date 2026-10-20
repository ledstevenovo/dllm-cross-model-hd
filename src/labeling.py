"""Conservative answer-match proposals, not factual adjudication.

Five factual/output categories plus needs_review. Only independently reviewed
incorrect is a hallucination positive. Exact short-answer matches are proposals;
unmatched prose, multiline explanations and matching truncated outputs require
review. See docs/LABEL_PROTOCOL.md for the primary metric inclusion rule.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence

from .textnorm import (
    collapse_whitespace,
    extract_number,
    first_line,
    is_yes_no,
    normalize_answer,
    normalize_text,
    remove_punctuation,
    strip_wrapping_quotes,
)

__all__ = [
    "EVAL_REGIMES",
    "HALLUCINATION_POSITIVE_LABEL",
    "LABELS",
    "LABEL_MEANINGS",
    "LabelResult",
    "classify_generation",
    "extract_candidate",
    "match_answer",
]

#: The five mutually exclusive classes of section 4.3.
LABELS: tuple[str, ...] = (
    "correct",
    "incorrect",
    "refusal_empty",
    "incomplete_truncated",
    "format_failure",
    "needs_review",
)

#: Only a parseable wrong answer counts as a factual error.
HALLUCINATION_POSITIVE_LABEL = "incorrect"

#: The abstaining classes, kept separate from the factual-error class.
ABSTAIN_LABELS: tuple[str, ...] = ("refusal_empty", "incomplete_truncated", "format_failure", "needs_review")

LABEL_MEANINGS: dict[str, str] = {
    "needs_review": "Unmatched or ambiguous output; requires independent factual review.",
    "correct": "The extracted answer matches the gold value or one of its aliases.",
    "incorrect": "An independently adjudicated factual error. The only positive class.",
    "refusal_empty": "Blank output or an explicit refusal to answer.",
    "incomplete_truncated": "Generation hit the length budget without producing a matching answer.",
    "format_failure": "Output was unusable as an answer (no answer content, or the question echoed).",
}

#: How to turn the five-way labels into a binary detection target.  Reporting
#: all three makes the abstention handling auditable instead of implicit.
EVAL_REGIMES: dict[str, dict[str, object]] = {
    "binary_exclude_abstain": {
        "positive": ["incorrect"],
        "negative": ["correct"],
        "dropped": list(ABSTAIN_LABELS),
        "note": "Cleanest factual-error signal; abstaining outputs are dropped, so report coverage.",
    },
    "binary_abstain_as_negative": {
        "positive": ["incorrect"],
        "negative": ["correct", "refusal_empty", "incomplete_truncated", "format_failure"],
        "dropped": ["needs_review"],
        "note": "Conventional accuracy view; an abstention counts as 'not a hallucination'.",
    },
    "all_statuses": {
        "classes": list(LABELS),
        "dropped": [],
        "note": "Full protocol; needed to show the detector is not just detecting truncation.",
    },
}

_ANSWER_CUE_RE = re.compile(r"answer\s*[:\uff1a]", flags=re.IGNORECASE)

# Patterns are written against *normalised* text, where punctuation has already
# become whitespace, so "don't" appears as "don t".
_REFUSAL_RE = re.compile(
    r"(?:\bi\s+(?:do\s+not|don\s*t|dont)\s+know\b)"
    r"|(?:\bi\s+am\s+not\s+sure\b)"
    r"|(?:\bi\s*'?\s*m\s+not\s+sure\b)"
    r"|(?:\bnot\s+sure\b)"
    r"|(?:\bno\s+idea\b)"
    r"|(?:\b(?:can\s*not|can\s*t|cannot)\s+(?:be\s+)?(?:answer|determin|say|tell|know))"
    r"|(?:\bunanswerable\b)"
    r"|(?:\bno\s+(?:definitive|known|clear)\s+answer\b)"
    r"|(?:\binsufficient\s+information\b)"
    r"|(?:\bi\s+(?:do\s+not|don\s*t|dont)\s+have\s+enough\s+information\b)"
    r"|(?:\bas\s+an\s+ai\b)"
    r"|(?:\bunknown\b)"
    r"|(?:不知道)"
    r"|(?:无法回答)"
    r"|(?:不确定)",
    flags=re.IGNORECASE,
)

_ALNUM_RE = re.compile(r"[^\W_]", flags=re.UNICODE)


@dataclass(frozen=True, slots=True)
class LabelResult:
    """The outcome of labelling one generation."""

    label: str
    label_source: str
    candidate: str
    candidate_normalized: str
    matched_answer: Optional[str] = None
    truncated: bool = False
    refusal_detected: bool = False
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-safe dict for ``data/labels/``."""
        return {
            "label": self.label,
            "label_source": self.label_source,
            "candidate": self.candidate,
            "candidate_normalized": self.candidate_normalized,
            "matched_answer": self.matched_answer,
            "truncated": self.truncated,
            "refusal_detected": self.refusal_detected,
            "notes": list(self.notes),
        }


def extract_candidate(text: object) -> str:
    """Pull the candidate answer out of a raw generation.

    Models frequently restate the prompt before answering, so everything up to
    the **last** ``Answer:`` cue is discarded.  Only the first non-empty line is
    kept: generative QA answers on line one and explains afterwards, and grading
    the explanation would reward verbosity.
    """
    if not isinstance(text, str):
        return ""
    body = text
    cues = list(_ANSWER_CUE_RE.finditer(body))
    if cues:
        body = body[cues[-1].end() :]
    return strip_wrapping_quotes(first_line(body))


def match_answer(
    candidate: object,
    gold_answer: object,
    gold_aliases: Iterable[object] = (),
) -> tuple[bool, Optional[str], Optional[str]]:
    """Match a candidate against the gold value and aliases.

    Returns ``(matched, matched_answer, rule)`` where ``rule`` names the rule
    that fired, so ``label_source`` can record *why* a label was assigned and
    the analysis stage can audit matches without re-running the matcher.

    Numeric values are compared before punctuation normalization so signs and
    decimal points cannot disappear. Other candidates use exact normalized
    equality, then yes/no equivalence. These remain label proposals.
    """
    candidate_norm = normalize_answer(candidate)
    if not candidate_norm:
        return False, None, None

    acceptable = [
        value
        for value in (gold_answer, *gold_aliases)
        if value is not None and str(value).strip()
    ]

    for value in acceptable:
        cn, gn = extract_number(candidate), extract_number(value)
        if cn is not None or gn is not None:
            if cn is not None and gn is not None and cn == gn:
                return True, str(value), "numeric_equality"
            continue
        if candidate_norm == normalize_answer(value):
            return True, str(value), "exact_normalized"

    candidate_number = extract_number(candidate)
    if candidate_number is not None:
        for value in acceptable:
            gold_number = extract_number(value)
            if gold_number is not None and candidate_number == gold_number:
                return True, str(value), "numeric_equality"

    if is_yes_no(candidate_norm):
        for value in acceptable:
            if is_yes_no(value) and _polarity(candidate_norm) == _polarity(normalize_answer(value)):
                return True, str(value), "yes_no_equivalence"

    return False, None, None


def _polarity(normalized: str) -> str:
    """Return ``'yes'`` or ``'no'`` for a normalised yes/no word."""
    negative = {"no", "nope", "false", "incorrect"}
    return "no" if normalized in negative else "yes"


def classify_generation(
    text: object,
    gold_answer: object,
    gold_aliases: Sequence[object] = (),
    *,
    question: Optional[str] = None,
    hit_max_length: bool = False,
) -> LabelResult:
    """Propose an output status; truncated matches remain needs_review."""
    notes: list[str] = []

    if not isinstance(text, str) or not text.strip():
        return LabelResult(
            label="refusal_empty" if isinstance(text, str) else "format_failure",
            label_source="refusal_empty:blank" if isinstance(text, str) else "format_failure:not_text",
            candidate="",
            candidate_normalized="",
            truncated=hit_max_length,
            notes=("generation was missing or not a string",),
        )

    candidate = extract_candidate(text)
    candidate_norm = normalize_answer(candidate)
    # The refusal patterns are written against punctuation-free text, where
    # "don't" has become "don t" and "can't" has become "can t".  Feeding them
    # plain normalize_text() -- which keeps punctuation -- silently missed the
    # single most common refusal phrasing and booked "I don't know." as a
    # factual error, i.e. into the positive class this module exists to protect.
    text_norm = collapse_whitespace(remove_punctuation(normalize_text(text)))
    refusal = bool(_REFUSAL_RE.search(text_norm))

    matched, matched_answer, rule = match_answer(candidate, gold_answer, gold_aliases)
    if matched and (hit_max_length or len(text.strip().splitlines()) > 1 or refusal):
        return LabelResult("needs_review", "needs_review:matched_but_ambiguous", candidate, candidate_norm, matched_answer, hit_max_length, refusal)
    if matched:
        return LabelResult(
            label="correct",
            label_source=f"correct:{rule}",
            candidate=candidate,
            candidate_normalized=candidate_norm,
            matched_answer=matched_answer,
            truncated=hit_max_length,
            refusal_detected=refusal,
            notes=tuple(notes),
        )

    if refusal:
        return LabelResult(
            label="refusal_empty",
            label_source="refusal_empty:refusal_phrase",
            candidate=candidate,
            candidate_normalized=candidate_norm,
            truncated=hit_max_length,
            refusal_detected=True,
            notes=tuple(notes),
        )

    if not candidate or not _ALNUM_RE.search(candidate):
        return LabelResult(
            label="refusal_empty" if not candidate_norm else "format_failure",
            label_source=(
                "refusal_empty:empty_output"
                if not candidate_norm
                else "format_failure:no_alphanumeric_answer_content"
            ),
            candidate=candidate,
            candidate_normalized=candidate_norm,
            truncated=hit_max_length,
            refusal_detected=refusal,
            notes=tuple(notes),
        )

    if question is not None and candidate_norm == normalize_answer(question):
        return LabelResult(
            label="format_failure",
            label_source="format_failure:question_echoed_verbatim",
            candidate=candidate,
            candidate_normalized=candidate_norm,
            truncated=hit_max_length,
            refusal_detected=refusal,
            notes=tuple(notes),
        )

    if hit_max_length:
        return LabelResult(
            label="incomplete_truncated",
            label_source="incomplete_truncated:hit_max_length",
            candidate=candidate,
            candidate_normalized=candidate_norm,
            truncated=True,
            refusal_detected=refusal,
            notes=tuple(notes),
        )

    return LabelResult(
        label="needs_review",
        label_source="needs_review:no_matching_rule",
        candidate=candidate,
        candidate_normalized=candidate_norm,
        truncated=False,
        refusal_detected=refusal,
        notes=tuple(notes),
    )
