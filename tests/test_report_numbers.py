"""The numbers in the reports must agree in sign with the metrics they came from.

Tonight a sign error reached three documents: Dream's closed-book HotpotQA scored 82.24 against
a paper value of 80.6, which is +1.6, but the text said -1.6. It was caught by eye, not by any
test, and these figures are the paper's claims.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
CHECKER = REPO / "scripts/check_table_consistency.py"
CELLS = REPO / "reports/tre_repro/all_cells.json"
TARGET = REPO / "reports/tre_repro/context_effect_confirmed.md"


def run_checker():
    return subprocess.run([sys.executable, str(CHECKER)], capture_output=True, text=True, cwd=REPO)


@pytest.mark.skipif(not CELLS.exists(), reason="run scripts/tre_table.py first")
def test_reports_are_consistent():
    result = run_checker()
    assert result.returncode == 0, result.stderr


@pytest.mark.skipif(not (CELLS.exists() and TARGET.exists()), reason="inputs missing")
def test_checker_detects_a_flipped_sign(tmp_path):
    original = TARGET.read_text(encoding="utf-8")
    flipped = original.replace("| Dream | 0.8224 | 80.6 | **+1.6** |",
                               "| Dream | 0.8224 | 80.6 | **−1.6** |")
    if flipped == original:
        pytest.skip("the line under test changed; update this test")
    try:
        TARGET.write_text(flipped, encoding="utf-8")
        result = run_checker()
        assert result.returncode == 1, "checker failed to notice a flipped sign"
        assert "80.6" in result.stderr
    finally:
        TARGET.write_text(original, encoding="utf-8")
