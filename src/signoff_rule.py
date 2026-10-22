"""The sign-off rule that produced the reviewed pilot200 labels, in-repo.

History: the 2026-10-21 pilot200 draft pre-review lived only in
``/root/autodl-tmp/tools/pilot200_draft_review.py`` (outside the repository), and
the reviewed labels that every main-table number rests on were promoted from its
output by ``finalize_reviewed_labels.py``.  Expansion cannot reuse a rule that
only exists on one disk, so the rule is ported here verbatim and pinned by a
regression test that must reproduce all 400 reviewed labels bit for bit
(``tests/test_signoff_rule.py``).

The rule is deliberately *different* from ``src.labeling.classify_generation``:
that one is the tool's proposal (it returns ``needs_review`` for most misses) and
was never the labelling authority.  This one is what a human signed off, so it
assigns a decisive verdict to every row.

Vocabulary differs too: this rule emits ``empty`` where the project vocabulary
uses ``refusal_empty``.  ``to_project_vocabulary`` maps it, and the mapping is
asserted by the same regression test.
"""
from __future__ import annotations

from typing import Iterable, Sequence

PUNCT = str.maketrans({c: " " for c in ".,;:!?\"'()[]{}<>“”‘’、"})

FUNCTION_WORDS = {
    "the", "a", "an", "of", "to", "in", "on", "at", "for", "and", "or", "but", "is", "are",
    "was", "were", "be", "been", "am", "my", "your", "his", "her", "its", "our", "their",
    "this", "that", "these", "those", "with", "from", "by", "as", "if", "then", "than", "so",
    "such", "it", "he", "she", "they", "we", "you", "i", "do", "did", "does", "not",
    "sir", "off", "out", "up", "down", "over", "under", "into", "about", "after", "before",
}

#: rule verdict -> project label vocabulary used by offline.py / detectors
PROJECT_VOCABULARY = {"empty": "refusal_empty"}


def tokens(value: object) -> list[str]:
    return str(value).translate(PUNCT).lower().split()


def contains(hay: Sequence[str], needle: Sequence[str]) -> bool:
    n = len(needle)
    if n == 0 or n > len(hay):
        return False
    return any(list(hay[i:i + n]) == list(needle) for i in range(len(hay) - n + 1))


def to_project_vocabulary(verdict: str) -> str:
    return PROJECT_VOCABULARY.get(verdict, verdict)


def signoff_verdict(gold: object, aliases: Iterable[object], prediction: object,
                    refusal: bool, question: object) -> tuple[str, str]:
    """Return ``(verdict, reason)`` exactly as the signed-off pilot200 review did."""
    p, g, q = tokens(prediction), tokens(gold), tokens(question)
    alias_list = [tokens(a) for a in (aliases or []) if str(a).strip()]
    if not p:
        return "empty", "空输出"
    if refusal:
        return "format_failure", "规则检出拒答"
    if p == g or contains(p, g) or (len(p) >= 2 and contains(g, p)):
        return "correct", "gold 命中（含等价/别名）"
    for alias in alias_list:
        if alias and (contains(p, alias) or (len(p) >= 2 and contains(alias, p))):
            return "correct", "gold 别名命中"
    if len(p) == 1 and (p[0] in FUNCTION_WORDS or len(p[0]) <= 2):
        return "format_failure", f"单 token 函数词/碎片 {prediction!r}，无答案内容"
    if len(p) == 1:
        return "incorrect", f"单 token 短答 {prediction!r}（疑似错答，人工留意）"
    if len(p) >= 3 and contains(q, p):
        return "format_failure", "输出为问句回显，无答案内容"
    return "incorrect", "gold 未命中"
