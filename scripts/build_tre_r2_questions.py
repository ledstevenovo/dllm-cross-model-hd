"""Build the TRE R2 HotpotQA question list (800 questions + 20 smoke).

Why a separate builder instead of extending ``build_tre_repro_questions.py``: R1's
list is frozen and its files are verified byte-for-byte by that script's
``--check``.  Touching its code path would put a frozen artifact at risk for no
reason, so R2 gets its own script and its own manifest.

Protocol decisions frozen here, before any R2 trajectory exists:

* **Pool**: ``data/raw_qa/hotpotqa/test.jsonl`` (1,654 rows, cluster-disjoint from
  the pool's train/validation partitions).  Sampling from the frozen pool rather
  than the raw parquet follows R1's decision B: no network dependency, provenance
  already audited, and a later trained baseline can still use train/validation.
* **Context**: HotpotQA is unanswerable without the distractor paragraphs, so the
  prompt is the standard context-grounded form (``src.tre_repro.context_prompt``).
  Context is recovered from the revision-pinned raw parquet by ``raw_id`` and
  rendered with ``render_context`` -- a stable rendering that is fingerprinted
  into every record.
* **Draw**: sort by ``question_id``, draw 820 with ``random.Random(SAMPLING_SEED)``;
  the first 800 are the evaluation list, the remaining 20 the engineering smoke
  list, so the two are disjoint by construction.  The same sampling seed as R1 is
  used deliberately: it is a fixed constant, not a tuned knob.
* **No overlap avoidance**: overlaps with pilot200/small200/smoke20 are *measured
  and recorded*, not silently avoided, exactly as in R1.  Note that R2 questions
  come from HotpotQA while the main project's pool mixes HotpotQA and TriviaQA, so
  an R2 question can also appear in the main project -- that is reported, not
  hidden, and the two studies use different protocols.

Usage::

    .venv/bin/python scripts/build_tre_r2_questions.py            # write files
    .venv/bin/python scripts/build_tre_r2_questions.py --check    # verify only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tre_repro import (  # noqa: E402
    GENERATION_SEED,
    TRE_PROMPT_STYLE_CONTEXT,
    TRE_PROMPT_VERSION_CONTEXT,
    build_record,
    load_questions,
    render_context,
)

POOL = ROOT / "data/raw_qa/hotpotqa/test.jsonl"
RAW = ROOT / "data/raw_download/hotpotqa/distractor_validation.parquet"
RAW_LOCK_KEY = "hotpotqa_distractor_validation"
OUT_DIR = ROOT / "data/tre_repro/questions"
MANIFEST = ROOT / "data/tre_repro/questions_manifest_r2.json"
SUBSETS = ROOT / "data/raw_qa/subsets"

SAMPLING_SEED = 20261021
EVAL_TOTAL = 800
SMOKE_TOTAL = 20
SELECTION = (
    "sort pool rows by question_id, draw EVAL_TOTAL+SMOKE_TOTAL with "
    "random.Random(SAMPLING_SEED); first EVAL_TOTAL -> evaluation list, remaining -> smoke list"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_contexts() -> tuple[dict[str, str], str]:
    """Return ``raw_id -> rendered context`` plus the verified parquet sha256."""
    import pandas as pd

    if not RAW.exists():
        raise SystemExit(
            f"missing {RAW.relative_to(ROOT)}; fetch it first with "
            f"scripts/fetch_raw_via_mirror.py --key {RAW_LOCK_KEY}"
        )
    lock = json.loads((ROOT / "configs/datasets/sources.lock.json").read_text(encoding="utf-8"))
    spec = next(f for f in lock["files"] if f["key"] == RAW_LOCK_KEY)
    digest = sha256(RAW)
    if digest != spec["sha256"]:
        raise SystemExit(f"{RAW} sha256 {digest} does not match the lock's {spec['sha256']}")

    frame = pd.read_parquet(RAW)
    contexts: dict[str, str] = {}
    for _, row in frame.iterrows():
        context = row["context"]
        contexts[str(row["id"])] = render_context(context["title"], context["sentences"])
    return contexts, digest


def build() -> tuple[list[dict], list[dict], dict]:
    pool_rows = read_jsonl(POOL)
    if len({row["question_id"] for row in pool_rows}) != len(pool_rows):
        raise ValueError("pool question IDs are not unique")
    pool_sha = sha256(POOL)
    contexts, raw_sha = load_contexts()

    ordered = sorted(pool_rows, key=lambda row: row["question_id"])
    rng = random.Random(SAMPLING_SEED)
    picked = rng.sample(range(len(ordered)), EVAL_TOTAL + SMOKE_TOTAL)

    def provenance(row: dict, rank: int) -> dict:
        return {
            "pool_file": POOL.relative_to(ROOT).as_posix(),
            "pool_sha256": pool_sha,
            "pool_partition": "test",
            "pool_question_ids": len(pool_rows),
            "selection_seed": SAMPLING_SEED,
            "selection_rank": rank,
            "selection_rule": SELECTION,
            "source_split": (row.get("source") or {}).get("hf_split", "validation"),
            "source_config": (row.get("source") or {}).get("hf_config", "distractor"),
            "prompt_style": TRE_PROMPT_STYLE_CONTEXT,
            "context_file": RAW.relative_to(ROOT).as_posix(),
            "context_sha256": raw_sha,
            "context_render": "Title: sentences, paragraphs separated by a blank line",
        }

    eval_records: list[dict] = []
    smoke_records: list[dict] = []
    for rank, index in enumerate(picked):
        row = ordered[index]
        raw_id = str((row.get("source") or {}).get("raw_id") or "")
        if raw_id not in contexts:
            raise SystemExit(f"no context for {row['question_id']} (raw_id {raw_id!r})")
        context = contexts[raw_id]
        if rank < EVAL_TOTAL:
            eval_records.append(
                build_record(row, split="test", provenance=provenance(row, rank), context=context).to_dict()
            )
        else:
            smoke_records.append(
                build_record(row, split="smoke", provenance=provenance(row, rank - EVAL_TOTAL),
                             context=context).to_dict()
            )

    eval_ids = {row["question_id"] for row in eval_records}
    smoke_ids = {row["question_id"] for row in smoke_records}
    eval_clusters = {row["cluster_id"] for row in eval_records}
    train_clusters = {row["cluster_id"] for row in read_jsonl(POOL.parent / "train.jsonl")}
    validation_clusters = {row["cluster_id"] for row in read_jsonl(POOL.parent / "validation.jsonl")}

    overlaps = {}
    for path in sorted(SUBSETS.glob("*.jsonl")):
        other = {row["question_id"] for row in read_jsonl(path) if row["dataset"] == "hotpotqa"}
        overlaps[path.name] = {
            "hotpotqa_questions": len(other),
            "overlap_eval800": len(other & eval_ids),
            "overlap_smoke20": len(other & smoke_ids),
        }

    report = {
        "hotpotqa_eval800": validate_payload(eval_records),
        "smoke20": validate_payload(smoke_records),
    }
    manifest = {
        "manifest_version": "tre-r2-questions-v1",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "schema_version": eval_records[0]["schema_version"],
        "decision": "R2: HotpotQA, sampled from the frozen pool's test partition (same rule as R1)",
        "generation_seed": GENERATION_SEED,
        "sampling_seed": SAMPLING_SEED,
        "selection_rule": SELECTION,
        "dataset": "hotpotqa",
        "source_split": "validation",
        "source_config": "distractor",
        "prompt": {
            "prompt_template_version": TRE_PROMPT_VERSION_CONTEXT,
            "prompt_style": TRE_PROMPT_STYLE_CONTEXT,
            "example_prompt": eval_records[0]["prompt"],
            "example_prompt_fingerprint": eval_records[0]["prompt_fingerprint"],
            "note": "context is required for HotpotQA; this is a different prompt version from R1's bare question, never an edit of it",
        },
        "context": {
            "file": RAW.relative_to(ROOT).as_posix(),
            "sha256": raw_sha,
            "lock_key": RAW_LOCK_KEY,
            "render": "Title: sentences, paragraphs separated by a blank line",
        },
        "pool": {
            "file": POOL.relative_to(ROOT).as_posix(),
            "sha256": pool_sha,
            "rows": len(pool_rows),
            "unique_questions": len({row["question_id"] for row in pool_rows}),
            "unique_clusters": len({row["cluster_id"] for row in pool_rows}),
        },
        "files": {
            "hotpotqa_eval800": {
                "path": (OUT_DIR / "hotpotqa_eval800.jsonl").relative_to(ROOT).as_posix(),
                "samples": len(eval_records),
                "unique_questions": len(eval_ids),
                "unique_clusters": len(eval_clusters),
                "sha256": None,
                "first_sample_id": eval_records[0]["sample_id"],
            },
            "hotpotqa_smoke20": {
                "path": (OUT_DIR / "hotpotqa_smoke20.jsonl").relative_to(ROOT).as_posix(),
                "samples": len(smoke_records),
                "unique_questions": len(smoke_ids),
                "unique_clusters": len({row["cluster_id"] for row in smoke_records}),
                "sha256": None,
                "first_sample_id": smoke_records[0]["sample_id"],
            },
        },
        "validation": report,
        "disjoint": {
            "eval800_vs_smoke20_questions": len(eval_ids & smoke_ids),
            "eval800_clusters_vs_train_partition": len(eval_clusters & train_clusters),
            "eval800_clusters_vs_validation_partition": len(eval_clusters & validation_clusters),
            "note": "cluster-level disjointness from the pool's train/validation partitions is what allows a later trained baseline to reuse them without near-duplicate leakage",
        },
        "overlap_with_frozen_subsets": overlaps,
    }
    return eval_records, smoke_records, manifest


def validate_payload(rows: list[dict]) -> dict:
    """Validate a serialised list through the same loader the scorer uses."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "questions.jsonl"
        path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
        records = load_questions(path)
    return {
        "checked": len(records),
        "unique_sample_ids": len({r.sample_id for r in records}),
        "unique_question_ids": len({r.question_id for r in records}),
        "problems": [],
        "duplicate_sample_ids": [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--check", action="store_true",
                        help="verify existing files against a fresh build without writing")
    args = parser.parse_args(argv)

    eval_records, smoke_records, manifest = build()
    for name, records in (("hotpotqa_eval800", eval_records), ("hotpotqa_smoke20", smoke_records)):
        path = OUT_DIR / f"{name}.jsonl"
        serialized = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records)
        digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        manifest["files"][name]["sha256"] = digest
        if args.check:
            if not path.exists() or path.read_bytes() != serialized.encode("utf-8"):
                raise SystemExit(f"{path} differs from a fresh build")
            print(f"[check] {path.relative_to(ROOT)} matches ({len(records)} records, sha256 {digest[:16]})")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(serialized.encode("utf-8"))
            print(f"[write] {path.relative_to(ROOT)} ({len(records)} records, sha256 {digest[:16]})")

    if not args.check:
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[write] {MANIFEST.relative_to(ROOT)}")
    else:
        stored = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if stored["files"] != manifest["files"]:
            raise SystemExit(f"{MANIFEST} file entries differ from a fresh build")
        print(f"[check] {MANIFEST.relative_to(ROOT)} matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
