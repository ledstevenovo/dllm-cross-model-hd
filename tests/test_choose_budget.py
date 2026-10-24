"""Budget recommendations must refuse to trust a censored pilot.

Both of tonight's sizing mistakes trace to the same thing: reading a budget off a configuration whose
answers already hit the cap. The rule is that a pilot is censored when its *median* sits at the
maximum -- at least half the answers were cut, so the sample says nothing about true length.

A share threshold alone is wrong: a 20-question pilot naturally repeats its maximum a quarter of the
time while still spanning 5 to 20 tokens.
"""

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from choose_budget import recommend  # noqa: E402


def test_small_pilot_with_spread_is_not_censored():
    budget, at_cap, censored = recommend([5, 10, 15, 20], headroom=1.5)
    assert budget == 30
    assert at_cap == pytest.approx(0.25)
    assert censored is False, "a quarter of a 4-sample pilot hits the max by construction"


def test_rounds_up_to_a_block_multiple():
    budget, _, _ = recommend([5, 10, 20], headroom=1.5, block_multiple=64)
    assert budget == 64


def test_constant_lengths_are_censored():
    _, at_cap, censored = recommend([40, 40, 40, 40])
    assert at_cap == 1.0
    assert censored is True


def test_the_degenerate_context_cell_is_censored():
    # 97.6% of the real L64 context answers ended at 62 tokens
    _, at_cap, censored = recommend([62] * 98 + [30, 20])
    assert at_cap > 0.95
    assert censored is True


def test_a_healthy_pilot_suggests_a_budget_near_the_max():
    lengths = [2, 5, 6, 8, 10, 13, 17, 19, 19, 20, 22, 26, 32, 35, 44]
    budget, at_cap, censored = recommend(lengths, headroom=1.5)
    assert censored is False
    assert budget == 66
    assert at_cap < 0.10


def test_empty_input_is_rejected():
    with pytest.raises(ValueError):
        recommend([])
