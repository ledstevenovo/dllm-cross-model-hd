"""The length filter must degrade gracefully, not crash, when nothing survives.

On Dream/TriviaQA every one of the ten features correlates with effective_length at |r| > 0.25,
because the answers are a median of three tokens. The first version of the fair comparison crashed in
the fitter with an empty feature list; that is a legitimate outcome which should be reported, not an
exception.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from fair_detector_comparison import length_free_columns  # noqa: E402


def frame(seed_length_correlation: bool):
    rng = np.random.default_rng(0)
    n = 200
    length = rng.integers(1, 20, n).astype(float)
    rows = {"effective_length": length}
    for index in range(4):
        if seed_length_correlation:
            # strongly tied to length, as in the Dream/TriviaQA run
            rows[f"f{index}"] = length * (index + 1) + rng.normal(0, 0.1, n)
        else:
            rows[f"f{index}"] = rng.normal(0, 1, n)
    return pd.DataFrame(rows)


def test_length_correlated_features_are_dropped():
    kept, dropped = length_free_columns(frame(True), ["f0", "f1", "f2", "f3"], 0.25)
    assert kept == []
    assert set(dropped) == {"f0", "f1", "f2", "f3"}


def test_independent_features_are_kept():
    kept, dropped = length_free_columns(frame(False), ["f0", "f1", "f2", "f3"], 0.25)
    assert len(kept) == 4
    assert dropped == {}


def test_constant_feature_is_dropped_not_correlated():
    data = frame(False)
    data["dead"] = 1.0
    kept, dropped = length_free_columns(data, ["f0", "dead"], 0.25)
    assert "dead" not in kept
    assert dropped["dead"] == "constant"
