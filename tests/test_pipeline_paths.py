"""Pipeline scripts must not reference paths or scripts that do not exist.

Tonight a queue waited on the wrong process name, matched nothing, and started a second 8B model
onto a full GPU. That failure was silent. Path mistakes fail the same way -- a script that points at
a nonexistent file exits later with a confusing error, or worse, silently skips a step.

This checks the shell scripts committed for scheduled runs: every `.py` they invoke exists.
"""

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"

# Shell entry points that are meant to be run unattended.
PIPELINES = [
    "run_llada_hotpot_ctx_l64.sh",
    "finish_last_cell.sh",
    "run_dream_triviaqa.sh",
    "run_hotpotqa_bare.sh",
    "run_overnight_gpu.sh",
]


def invoked_python(script: Path) -> set[str]:
    text = script.read_text(encoding="utf-8")
    # matches ".venv/bin/python scripts/foo.py" and ".venv-llada/bin/python scripts/foo.py"
    return set(re.findall(r"\.venv[\w-]*/bin/python\s+(scripts/[\w/]+\.py)", text))


@pytest.mark.parametrize("name", PIPELINES)
def test_invoked_scripts_exist(name):
    script = SCRIPTS / name
    if not script.exists():
        pytest.skip(f"{name} not present")
    missing = [p for p in invoked_python(script) if not (REPO / p).exists()]
    assert not missing, f"{name} invokes missing script(s): {missing}"


@pytest.mark.parametrize("name", PIPELINES)
def test_pipelines_are_syntactically_valid(name):
    script = SCRIPTS / name
    if not script.exists():
        pytest.skip(f"{name} not present")
    import subprocess
    result = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
