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
3. **The gold answer value never appears in the prompt.**  :func:`answer_in_prompt`
   and :func:`assert_gold_not_in_prompt` are the runtime guards; the build script
   drops any question whose canonical answer is copyable from the prompt, so the
   correct-rate is never inflated by copying.  Alias phrases are deliberately
   *not* treated as leaks (see :func:`assert_gold_not_in_prompt`).
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
    "answer_in_prompt",
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


def answer_in_prompt(prompt: str, answer: str, *, min_chars: int = 3) -> bool:
    """Return whether ``answer`` is visible in ``prompt`` as a token sequence.

    Matching is normalised and **token-sequence** based, not substring based.
    Two consequences, both deliberate:

    * A leaked answer is still caught when the question merely wraps it in
      punctuation or articles (``"the battle of Hastings"`` vs ``"Battle"``),
      because normalisation strips those before the comparison.
    * A false positive is avoided when the answer is a fragment of a longer word
      (``"Bull"`` must not match ``"Bulldog"``), which a naive substring test
      would report and which would then silently discard good questions.

    Answers shorter than ``min_chars`` after normalisation are ignored: a gold
    answer like ``"a"`` or ``"no"`` would otherwise match almost every prompt.
    """
    needle = normalize_answer(answer)
    if len(needle) < min_chars:
        return False
    needle_tokens = needle.split()
    haystack_tokens = normalize_answer(prompt).split()
    width = len(needle_tokens)
    if width == 0 or width > len(haystack_tokens):
        return False
    for start in range(len(haystack_tokens) - width + 1):
        if haystack_tokens[start : start + width] == needle_tokens:
            return True
    return False


def assert_gold_not_in_prompt(prompt: str, gold_answer: str) -> None:
    """Raise if the canonical gold answer is visible in the rendered prompt.

    Only the **canonical answer value** is checked, not the alias list.  The
    distinction is load-bearing: TriviaQA questions routinely reuse an alias
    phrase as their own wording -- ``"Which volcano in Tanzania is the highest
    mountain in Africa?"`` has gold ``"Kilimanjaro"`` and alias ``"Highest
    mountain in Africa"`` -- and in those items the model cannot copy the answer
    it is asked for, so discarding them would destroy good questions.  When the
    *value* itself appears, by contrast, the model can answer by copying, which
    is exactly what this guard exists to prevent.
    """
    if answer_in_prompt(prompt, gold_answer):
        raise AssertionError(
            f"gold answer {gold_answer!r} (normalised {normalize_answer(gold_answer)!r}) "
            "appears in the prompt"
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
