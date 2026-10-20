"""Small, dependency-free file helpers shared by the build scripts.

Kept separate from the research modules so that the pipeline logic
(``src.textnorm``, ``src.splitting``, ...) stays pure and unit-testable without
touching the disk.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any, Iterable, Mapping

__all__ = [
    "ensure_dir",
    "read_json",
    "sha256_file",
    "write_json",
    "write_jsonl",
]


def ensure_dir(path: str) -> str:
    """Create a directory (and parents) if missing and return it."""
    os.makedirs(path, exist_ok=True)
    return path


def sha256_file(path: str, chunk_size: int = 1 << 20) -> str:
    """Return the hex sha256 of a file, read in bounded chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(chunk_size)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def read_json(path: str) -> Any:
    """Read a UTF-8 JSON document."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str, payload: Any, *, indent: int = 2) -> str:
    """Write UTF-8 JSON atomically (temp file + ``os.replace``) and return the path.

    Atomic replacement means an interrupted build can never leave a half-written
    manifest that a later stage would happily read as truth.
    """
    ensure_dir(os.path.dirname(os.path.abspath(path)))
    temporary = f"{path}.tmp"
    with open(temporary, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=indent, ensure_ascii=False, sort_keys=False)
        handle.write("\n")
    os.replace(temporary, path)
    return path


def write_jsonl(path: str, records: Iterable[Mapping[str, Any]]) -> int:
    """Write JSON Lines atomically, one compact object per line.  Returns the count.

    ``ensure_ascii=False`` keeps Chinese and accented text readable, and the
    records are expected to already be in a fixed key order (see
    ``src.schema.FIELD_ORDER``) so that diffs between builds stay reviewable.
    """
    ensure_dir(os.path.dirname(os.path.abspath(path)))
    temporary = f"{path}.tmp"
    count = 0
    with open(temporary, "w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=False))
            handle.write("\n")
            count += 1
    os.replace(temporary, path)
    return count
