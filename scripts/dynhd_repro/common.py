"""Shared helpers for the DynHD reproduction adapter (step 0-1 contracts).

All formal runs must go through scripts/dynhd_repro/collect_local.py; this module only
holds deterministic helpers: paths, hashing, seed derivation, event logs, pool loading.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

REPO = Path(__file__).resolve().parents[2]
REPRO_ROOT = Path(os.environ.get("DYNHD_REPRO_ROOT", "/root/autodl-tmp/dynhd_repro"))
UPSTREAM = REPO / "references/repos/DynHD"
SEED_DERIVATION_VERSION = "sha256-first4be-v1"


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fingerprint(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def derive_item_seed(collection_seed: int, question_id: str) -> int:
    """item_seed = first 4 bytes of SHA256(str(seed) + ':' + question_id), big-endian."""
    digest = hashlib.sha256(f"{int(collection_seed)}:{question_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big")


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class EventLog:
    """Append-only JSONL event log with immediate flush (start/saved/failed/abort)."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = open(self.path, "a", encoding="utf-8")

    def write(self, event: str, **fields: Any) -> None:
        row = {"event": event, "ts": utc_now(), **fields}
        self._fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        self._fh.flush()
        os.fsync(self._fh.fileno())

    def close(self) -> None:
        self._fh.close()

    def read(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_pool(subset: Path, only_ids: Optional[Path] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Load a frozen local subset (id/question/answer/prompt) in file order.

    answer = [gold_answer] + gold_aliases (order preserved); prompt is the frozen prompt text.
    --only-question-ids filters first, then limit applies to the filtered ordered list.
    """
    rows = []
    for line in Path(subset).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        rows.append({
            "id": record["sample_id"],
            "question_id": record["question_id"],
            "question": record["question"],
            "answer": [record["gold_answer"], *(record.get("gold_aliases") or [])],
            "prompt": record.get("prompt") or record["question"],
            "dataset": record.get("dataset"),
            "split": record.get("split"),
        })
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("subset contains duplicate sample ids")
    if only_ids is not None:
        wanted = [line.strip() for line in Path(only_ids).read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(wanted) != len(set(wanted)):
            raise ValueError("only-question-ids contains duplicates")
        index = {r["id"]: r for r in rows}
        missing = [w for w in wanted if w not in index]
        if missing:
            raise ValueError(f"only-question-ids entries not present in subset: {missing[:5]}")
        rows = [index[w] for w in wanted]
    if limit is not None:
        if limit < 1:
            raise ValueError("limit must be positive")
        if limit > len(rows):
            raise ValueError(f"limit {limit} exceeds available items {len(rows)}")
        rows = rows[:limit]
    if not rows:
        raise ValueError("empty task list after filtering")
    return rows


def run_id_or_default(model: str, run_id: Optional[str]) -> str:
    return run_id or f"{time.strftime('%Y%m%d_%H%M%S')}_{model}"


def coerce_dream_logits_hook(model) -> None:
    """Upstream DynHD passes generation_logits_hook_func=None to Dream; the pinned Dream
    revision calls it unconditionally (generation_utils.py:307/415), which raises
    TypeError. Coerce None to the identity hook: no semantic change, documented deviation.
    Patched on the model wrapper instance, never in the upstream snapshot."""
    original = model.diffusion_generate

    def patched(*args, **kwargs):
        if kwargs.get("generation_logits_hook_func") is None:
            kwargs["generation_logits_hook_func"] = lambda step, x, logits: logits
        return original(*args, **kwargs)

    model.diffusion_generate = patched


def pilot_layout(output_dir: Path) -> Optional[Path]:
    """If output_dir looks like <root>/traces/<model>/pilot200/raw/<run_id>, return the failures dir."""
    parts = output_dir.parts
    if "pilot200" in parts and "raw" in parts:
        idx = parts.index("pilot200")
        return Path(*parts[: idx + 1]) / "failures"
    return None
