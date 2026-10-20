#!/usr/bin/env bash
# Canonical environment bootstrap for this project. Source it before running anything:
#
#     source scripts/env.sh
#     python scripts/build_dataset.py
#
# On a NORMAL machine, plain `python -m venv .venv && pip install -r requirements.txt`
# is enough and this file only needs to set PYTHONPATH for convenience.
#
# On THIS Windows machine the DSH workspace sandbox breaks CPython's tempfile
# (directories created with mode 0o700 are not writable), which kills pip/ensurepip.
# `_pyfix/sitecustomize.py` repairs that. See docs/ENVIRONMENT.md for the full story.
set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export REPO_ROOT

# --- sandbox workaround ------------------------------------------------------
export PYTHONPATH="$REPO_ROOT/_pyfix${PYTHONPATH:+:$PYTHONPATH}"
export TMPDIR="$REPO_ROOT/.tmp"
export PIP_CACHE_DIR="$REPO_ROOT/.pipcache"
export PYTHONNOUSERSITE=1
# The Windows console defaults to GBK and crashes on TriviaQA's non-ASCII answers.
export PYTHONIOENCODING="utf-8"
export PYTHONUTF8=1
mkdir -p "$TMPDIR" "$PIP_CACHE_DIR"

# uv cannot be used in this sandbox (piped subprocess capture is denied), so its
# cache dirs are pointed inside the workspace purely to keep stray writes contained.
export UV_CACHE_DIR="$REPO_ROOT/.uvcache"
export UV_PYTHON_INSTALL_DIR="$REPO_ROOT/.uvpython"
export UV_TOOL_DIR="$REPO_ROOT/.uvtools"
export UV_TOOL_BIN_DIR="$REPO_ROOT/.uvbin"

# --- interpreter -------------------------------------------------------------
if [ -x "$REPO_ROOT/.venv/Scripts/python.exe" ]; then
  export PY="$REPO_ROOT/.venv/Scripts/python.exe"
elif [ -x "$REPO_ROOT/.venv/bin/python" ]; then
  export PY="$REPO_ROOT/.venv/bin/python"
else
  export PY="$(command -v python)"
fi

# Run the project from the repo root so that relative data/ paths resolve.
cd "$REPO_ROOT" || return 1
echo "env.sh: PY=$PY"
echo "env.sh: cwd=$PWD"
