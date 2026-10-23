"""Every headline number in the paper must still match the file it came from.

The paper was rewritten repeatedly tonight as claims were revised, and a stale figure survived one
such rewrite: Dream/TriviaQA L128 read 79.72 when the run gives 79.683. That was caught by an audit
script written afterwards, not by any test, so the audit now runs as a test.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "scripts/audit_paper_numbers.py"
RUNS = REPO / "results/tre_repro"


@pytest.mark.skipif(not RUNS.exists(), reason="no TRE results present")
def test_paper_numbers_match_their_sources():
    result = subprocess.run([sys.executable, str(AUDIT)], capture_output=True, text=True, cwd=REPO)
    assert result.returncode == 0, result.stdout + result.stderr
