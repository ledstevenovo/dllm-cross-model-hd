"""The single frozen no-context prompt template for the whole study.

Design rules (these are research constraints, not style preferences):

1. **Exactly one template** is used for *both* models and *all* datasets.  A
   per-model or per-dataset prompt would confound the cross-model transfer
   comparison with prompt effects, and the study's whole point is that the only
   thing that changes between source and target is the model.
2. **No context passages.**  TriviaQA is used in its ``rc.nocontext`` variant and
   HotpotQA with its distractor paragraphs withheld, so both datasets ask the
   same kind of question: pure parametric recall.  This keeps the hallucination
   definition comparable across datasets.
3. **The gold answer never appears in the prompt.**  :func:`assert_gold_not_in_prompt`
   is the runtime guard; the build script calls it for every record, so a future
   template edit that leaks an answer fails loudly instead of silently
   inflating the correct-rate.
4. **Frozen and fingerprinted.**  Any edit to :data:`PROMPT_TEMPLATE` changes
   :func:`prompt_fingerprint`, which is stamped into every record and into the
   run manifest.  Two datasets built with different fingerprints are not
   comparable and the analysis stage can detect that.

The template text is the *user-content* part of the conversation.  Instruction-
tuned checkpoints (``LLaDA-8B-Instruct``, ``Dream-7B-Instruct``) wrap this string
in their own chat template at generation time; that wrapper belongs to the
inference configuration, not here, and must be recorded per model in
``configs/models/``.
"""

from __future__ import annotations

import hashlib
from typing import Final

from .textnorm import normalize_answer

__all__ = [
    "PROMPT_PLACEHOLDER",
    "PROMPT_TEMPLATE",
    "PROMPT_TEMPLATE_VERSION",
    "assert_gold_not_in_prompt",
    "describe",
    "prompt_fingerprint",
    "render_prompt",
]

PROMPT_PLACEHOLDER: Final[str] = "{question}"

PROMPT_TEMPLATE_VERSION: Final[str] = "v1"

#: v1 -- a minimal instruction plus the question.  Chosen over the bare
#: ``"Question: ...\nAnswer:"`` because both checkpoints are instruction-tuned
#: and a bare completion prompt makes them continue the *question* rather than
#: answer it; the one-clause instruction removes that failure mode without
#: hinting at the answer or its length.
PROMPT_TEMPLATE: Final[str] = (
    "Answer the question with a short factual answer.\n"
    "\n"
    "Question: {question}\n"
    "Answer:"
)


def _validate_template() -> None:
    """Fail at import time if the frozen template has been edited incorrectly."""
    if PROMPT_TEMPLATE.count(PROMPT_PLACEHOLDER) != 1:
        raise AssertionError(
            "PROMPT_TEMPLATE must contain exactly one {question} placeholder, "
            f"found {PROMPT_TEMPLATE.count(PROMPT_PLACEHOLDER)}"
        )
    if PROMPT_TEMPLATE.format(question="").count("{") or PROMPT_TEMPLATE.format(
        question=""
    ).count("}"):
        raise AssertionError("PROMPT_TEMPLATE must not contain other brace placeholders")


_validate_template()


def prompt_fingerprint() -> str:
    """Return ``sha256:<hex>`` over the version and the exact template text.

    The version string is hashed too, so bumping the version without touching
    the text still produces a new fingerprint -- an intentional change is always
    visible in the artifacts.
    """
    payload = f"{PROMPT_TEMPLATE_VERSION}\x1f{PROMPT_TEMPLATE}".encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def render_prompt(question: str) -> str:
    """Render the frozen template for one question."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("render_prompt requires a non-empty question string")
    return PROMPT_TEMPLATE.format(question=question.strip())


def assert_gold_not_in_prompt(prompt: str, gold_answers: list[str]) -> None:
    """Raise if any acceptable gold answer is visible in the rendered prompt.

    Matching is normalised *and* substring-based, because a leaked answer is
    still leaked if it appears inside a longer word (``"Kinect"`` inside
    ``"KinectShare"``).  Only non-trivial answers (>= 3 characters after
    normalisation) are checked, otherwise a gold answer like ``"a"`` would match
    every prompt.
    """
    haystack = normalize_answer(prompt)
    for gold in gold_answers:
        needle = normalize_answer(gold)
        if len(needle) >= 3 and needle in haystack:
            raise AssertionError(
                f"gold answer {gold!r} (normalised {needle!r}) leaks into the prompt"
            )


def describe() -> dict[str, object]:
    """Return the prompt description stamped into records and manifests."""
    return {
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "prompt_template": PROMPT_TEMPLATE,
        "prompt_fingerprint": prompt_fingerprint(),
        "prompt_placeholder": PROMPT_PLACEHOLDER,
        "prompt_style": "no-context, single-turn, answer-only",
    }
