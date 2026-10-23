"""Guard against constant columns sneaking into the frozen feature sets.

`revealed_fraction` was found to be 1.0 for every non-degenerate sample -- a circular definition,
since the effective window is itself defined by where generation stopped. It cost a dimension in
relative_normalized for the whole project. This test watches for the same class of problem on any
available feature table, so a new dead feature cannot be added silently.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.detectors import FEATURE_SETS  # noqa: E402

FEATURES = REPO / "results/pool2000/features_combined.parquet"

#: Known-degenerate features, documented in reports/dead_feature_finding.md. They stay in the
#: frozen feature sets (removing them would change published outputs) but must not multiply.
KNOWN_CONSTANT = {"revealed_fraction"}


@pytest.mark.skipif(not FEATURES.exists(), reason="feature table not present")
def test_no_new_constant_features():
    frame = pd.read_parquet(FEATURES)
    frame = frame[frame.human_reviewed & frame.label.isin(["correct", "incorrect"])]
    columns = {c for cols in FEATURE_SETS.values() for c in cols if c in frame}
    degenerate = {
        c for c in columns
        if frame[c].dropna().nunique() <= 1
    }
    unexpected = degenerate - KNOWN_CONSTANT
    assert not unexpected, (
        f"constant feature(s) not documented: {sorted(unexpected)}; "
        "either add to KNOWN_CONSTANT with a report, or remove from the feature set"
    )


@pytest.mark.skipif(not FEATURES.exists(), reason="feature table not present")
def test_known_constant_feature_is_still_constant():
    """If revealed_fraction ever starts varying, the documented claim becomes wrong."""
    frame = pd.read_parquet(FEATURES)
    frame = frame[frame.human_reviewed & frame.label.isin(["correct", "incorrect"])]
    if "revealed_fraction" not in frame:
        pytest.skip("column absent")
    normals = frame[frame.effective_length > 0]
    assert normals.revealed_fraction.nunique() == 1
