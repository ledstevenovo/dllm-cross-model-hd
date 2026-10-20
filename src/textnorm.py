"""Text normalisation shared by question deduplication and answer matching.

The answer-matching normaliser is deliberately the **SQuAD / HotpotQA official**
``normalize_answer`` (lowercase, strip punctuation, drop the articles
``a``/``an``/``the``, collapse whitespace).  Staying faithful to the published
metric makes our label agreement comparable with the TriviaQA and HotpotQA
literature instead of inventing a private notion of "same answer".

Documented deviation from the published function: we apply Unicode NFKC
normalisation first, so full-width and compatibility characters
(``"Ａ"`` -> ``"A"``, ligatures, non-breaking spaces) fold before matching.
This is required because the raw corpora contain such characters and NFKC is
the only step that is *safe* here -- it never merges two strings that are
semantically different, unlike accent folding, which we deliberately do **not**
do (``cafe`` must not match ``café``).

Question normalisation reuses the same function on purpose: deduplication should
not consider two questions different just because one says "the" and the other
does not.
"""

from __future__ import annotations

import re
import string
import unicodedata
from typing import Iterable, Iterator, Optional

__all__ = [
    "collapse_whitespace",
    "extract_number",
    "is_yes_no",
    "normalize_answer",
    "normalize_question",
    "normalize_text",
    "normalized_variants",
    "remove_articles",
    "remove_punctuation",
    "strip_wrapping_quotes",
]

_ARTICLES_RE = re.compile(r"\b(a|an|the)\b", flags=re.IGNORECASE)
_PUNCT_TABLE = str.maketrans({ch: " " for ch in string.punctuation})
_WS_RE = re.compile(r"\s+")
_NUMBER_RE = re.compile(r"^[+-]?(?:\d+(?:,\d{3})*|\d+)(?:\.\d+)?$")
_YES = frozenset({"yes", "yeah", "yep", "true", "correct"})
_NO = frozenset({"no", "nope", "false", "incorrect"})
_WRAPPING = ('"', "'", "`", "\u201c", "\u201d", "\u2018", "\u2019", "\u300c", "\u300d")


def normalize_text(value: object) -> str:
    """NFKC-fold, lowercase and collapse whitespace.  Never raises.

    ``None`` and non-strings normalise to ``""`` so that a malformed corpus row
    degrades into an empty string instead of crashing a long build.
    """
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)
    value = unicodedata.normalize("NFKC", value)
    return collapse_whitespace(value.lower())


def collapse_whitespace(value: str) -> str:
    """Collapse every run of whitespace into a single space and strip the ends."""
    return _WS_RE.sub(" ", value).strip()


def remove_punctuation(value: str) -> str:
    """Replace ASCII punctuation with spaces (SQuAD ``remove_punc``).

    Punctuation is replaced, not deleted, so ``"a-b"`` becomes ``"a b"`` and can
    never be glued into the different token ``"ab"``.  Unicode punctuation is
    left intact, matching the published metric.
    """
    return value.translate(_PUNCT_TABLE)


def remove_articles(value: str) -> str:
    """Drop standalone articles ``a`` / ``an`` / ``the``."""
    return _ARTICLES_RE.sub(" ", value)


def strip_wrapping_quotes(value: str) -> str:
    """Peel matching quotation marks off both ends, repeatedly.

    Generative models very often answer ``"Paris"`` with the quotes included;
    those quotes must not turn a correct answer into an incorrect one.
    """
    out = value.strip()
    changed = True
    while changed and len(out) >= 2:
        changed = False
        if out[0] in _WRAPPING and out[-1] in _WRAPPING:
            out = out[1:-1].strip()
            changed = True
    return out


def normalize_answer(value: object) -> str:
    """Normalise a gold answer, alias or generated answer for comparison.

    Order: NFKC + lowercase -> strip wrapping quotes -> punctuation to spaces ->
    drop articles -> collapse whitespace.  Quote stripping happens before
    punctuation removal because the punctuation table would otherwise turn the
    quotes into spaces and lose the pairing information.
    """
    text = strip_wrapping_quotes(normalize_text(value))
    return collapse_whitespace(remove_articles(remove_punctuation(text)))


def normalize_question(value: object) -> str:
    """Normalise a question into a stable deduplication key.

    Identical to :func:`normalize_answer` by design -- see the module docstring.
    """
    return normalize_answer(value)


def normalized_variants(values: Iterable[object]) -> list[str]:
    """Normalise a sequence, drop empties and return a de-duplicated sorted list."""
    seen: dict[str, None] = {}
    for value in values:
        norm = normalize_answer(value)
        if norm:
            seen.setdefault(norm, None)
    return sorted(seen)


def extract_number(value: object) -> Optional[float]:
    """Parse a plain number, or return ``None`` if the string is not one.

    Handles an optional sign, thousands separators (``"1,000"``) and decimals.
    Percent signs, units and spelled-out numbers are rejected on purpose: a
    silent partial parse would create false matches for range-type answers.
    """
    text = normalize_text(value)
    if not text or not _NUMBER_RE.match(text):
        return None
    try:
        return float(text.replace(",", ""))
    except ValueError:  # pragma: no cover - guarded by the regex above
        return None


def is_yes_no(value: object) -> bool:
    """Return whether a normalised answer is a yes/no decision word."""
    norm = normalize_answer(value)
    return norm in _YES or norm in _NO


def first_line(value: str) -> str:
    """Return the first non-empty line of a generation.

    Generative QA almost always puts the answer on the first line and then
    explains; the protocol only ever grades the first non-empty line.
    """
    for line in value.splitlines():
        if line.strip():
            return line.strip()
    return ""


def iter_tokens(value: str) -> Iterator[str]:
    """Yield normalised whitespace tokens, for diagnostics only."""
    yield from normalize_answer(value).split()
