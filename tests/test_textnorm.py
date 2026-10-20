"""Project normalization regression cases; not official benchmark equivalence."""

from __future__ import annotations

import pytest

from src.textnorm import (
    collapse_whitespace,
    extract_number,
    first_line,
    is_yes_no,
    normalize_answer,
    normalize_question,
    normalized_variants,
    remove_articles,
    remove_punctuation,
    strip_wrapping_quotes,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Paris", "paris"),
        ("  Paris  ", "paris"),
        ("The Battle of Hastings", "battle of hastings"),
        ("a cat", "cat"),
        ("An Apple", "apple"),
        ('"Paris"', "paris"),
        ("\u201cParis\u201d", "paris"),
        ("Paris.", "paris"),
        ("New   York", "new york"),
        ("\uff21\uff22\uff23", "abc"),
        ("", ""),
        (None, ""),
    ],
)
def test_normalize_answer(raw, expected):
    assert normalize_answer(raw) == expected


def test_normalize_answer_does_not_fold_accents():
    """Accent folding would merge two answers that are not the same answer."""
    assert normalize_answer("caf\u00e9") != normalize_answer("cafe")
    assert normalize_answer("caf\u00e9") == "caf\u00e9"


def test_normalize_question_uses_the_same_contract_as_answer_matching():
    raw = "The  Capital of France?"
    assert normalize_question(raw) == normalize_answer(raw)


def test_remove_punctuation_replaces_and_never_glues_tokens():
    """Deleting punctuation would turn "a-b" into the different token "ab"."""
    assert remove_punctuation("a-b") == "a b"


def test_remove_articles_only_drops_standalone_articles():
    assert remove_articles("the theory of an atheist") == "  theory of   atheist"


def test_strip_wrapping_quotes_peels_repeatedly_but_not_unpaired_marks():
    assert strip_wrapping_quotes("'\"Paris\"'") == "Paris"
    assert strip_wrapping_quotes("Paris") == "Paris"
    assert strip_wrapping_quotes("'Paris") == "'Paris"


def test_collapse_whitespace():
    assert collapse_whitespace("  a \n b  ") == "a b"


@pytest.mark.parametrize("raw", ["1,234", "1234", "12", "-3.5", "+7", "0.5"])
def test_extract_number_accepts_plain_numbers(raw):
    assert extract_number(raw) is not None


@pytest.mark.parametrize("raw", ["12%", "12kg", "1 000", "twelve", "", "1,23", "12."])
def test_extract_number_rejects_units_and_malformed_numbers(raw):
    """A silent partial parse would create false matches for range answers."""
    assert extract_number(raw) is None


def test_extract_number_values():
    assert extract_number("1,234") == 1234.0
    assert extract_number("-3.5") == -3.5


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("Yes", True), ("yes", True), ("True", True), ("No", True), ("maybe", False), ("", False)],
)
def test_is_yes_no(raw, expected):
    assert is_yes_no(raw) is expected


def test_first_line_skips_leading_blank_lines():
    assert first_line("\n\nAnswer: Paris\nbecause") == "Answer: Paris"
    assert first_line("   ") == ""


def test_normalized_variants_deduplicates_and_sorts():
    assert normalized_variants(["Paris", "paris ", "The Paris", ""]) == ["paris"]
    assert normalized_variants(["zebra", "bear"]) == ["bear", "zebra"]
