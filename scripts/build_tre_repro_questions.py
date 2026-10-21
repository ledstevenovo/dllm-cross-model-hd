"""Build the TRE reproduction question lists (v3 decision B).

Decision B (2026-10-21): sample from the **test partition of the frozen pool**
(``data/raw_qa/triviaqa/test.jsonl``) rather than re-downloading the raw HF
validation split.  Rationale, measured in the same session:

* raw ``trivia_qa/rc.nocontext`` validation holds 9,960 unique questions; the
  frozen pool holds 9,915.  The 46-question difference (0.46%) is 12 questions
  carved out into the engineering ``smoke20`` plus 34 removed by the pool's own
  conservative cleaning, 31 of which are items whose gold answer is printed in
  the question (copyable).  An 800-question draw therefore differs from a
  raw-pool draw by ~3 questions, all of the easiest kind.
* the pool's test partition is cluster-disjoint from its train/validation
  partitions, so a later trained baseline (TraceDet / DynHD / TDGNet) can keep
  using train/validation without near-duplicate leakage into these 800 items.
* no network dependency and the pool's provenance is already audited.

The lists are deterministic: questions are sorted by ``question_id`` and drawn
with ``random.Random(SAMPLING_SEED)``; the draw of 820 is split into the first
800 (evaluation) and the last 20 (engineering smoke), which makes the two lists
disjoint by construction.  Overlaps with the pre-existing frozen subsets
(``pilot200``/``small200``/``smoke20``) are measured and recorded in the
manifest, not silently avoided.

Usage::

    uv run python scripts/build_tre_repro_questions.py            # writes files
    uv run python scripts/build_tre_repro_questions.py --check    # verify only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tre_repro import (  # noqa: E402
    GENERATION_SEED,
    TRE_PROMPT_STYLE,
    TRE_PROMPT_VERSION,
    TRE_REPRO_SCHEMA_VERSION,
    bare_prompt,
    build_record,
    prompt_fingerprint,
    sample_id_for,
    validate_questions,
)

POOL = ROOT / "data/raw_qa/triviaqa/test.jsonl"
OUT_DIR = ROOT / "data/tre_repro/questions"
MANIFEST = ROOT / "data/tre_repro/questions_manifest.json"
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


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def build() -> tuple[list[dict], list[dict], dict]:
    pool_rows = read_jsonl(POOL)
    if len({row["question_id"] for row in pool_rows}) != len(pool_rows):
        raise ValueError("pool question IDs are not unique")
    pool_sha = sha256(POOL)
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
            "source_config": (row.get("source") or {}).get("hf_config", "rc.nocontext"),
            "prompt_style": TRE_PROMPT_STYLE,
        }

    eval_records: list[dict] = []
    smoke_records: list[dict] = []
    for rank, index in enumerate(picked):
        row = ordered[index]
        if rank < EVAL_TOTAL:
            eval_records.append(build_record(row, split="test", provenance=provenance(row, rank)).to_dict())
        else:
            smoke_records.append(
                build_record(row, split="smoke", provenance=provenance(row, rank - EVAL_TOTAL)).to_dict()
            )

    report = {}
    for name, records in (("triviaqa_eval800", eval_records), ("smoke20", smoke_records)):
        loaded = [build_record_read(record) for record in records]
        report[name] = validate_questions(loaded)
    eval_ids = {row["question_id"] for row in eval_records}
    smoke_ids = {row["question_id"] for row in smoke_records}
    eval_clusters = {row["cluster_id"] for row in eval_records}
    train_clusters = {
        row["cluster_id"] for row in read_jsonl(POOL.parent / "train.jsonl")
    }
    validation_clusters = {
        row["cluster_id"] for row in read_jsonl(POOL.parent / "validation.jsonl")
    }
    overlaps = {}
    for path in sorted(SUBSETS.glob("*.jsonl")):
        other = {row["question_id"] for row in read_jsonl(path) if row["dataset"] == "triviaqa"}
        overlaps[path.name] = {
            "triviaqa_questions": len(other),
            "overlap_eval800": len(other & eval_ids),
            "overlap_smoke20": len(other & smoke_ids),
        }
    manifest = {
        "manifest_version": "tre-repro-questions-v1",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "schema_version": TRE_REPRO_SCHEMA_VERSION,
        "decision": "B: sample from the frozen pool's test partition; see docs/TRE_4080SUPER_32GB_复现方案.md §4.2",
        "generation_seed": GENERATION_SEED,
        "sampling_seed": SAMPLING_SEED,
        "selection_rule": SELECTION,
        "dataset": "triviaqa",
        "source_split": "validation",
        "source_config": "rc.nocontext",
        "source_split_note": (
            "the upstream rc.nocontext test split carries no usable gold answers, so the pool (and these "
            "lists) are drawn from the validation split; 'split=test' inside the file is an internal role only"
        ),
        "prompt": {
            "prompt_template_version": TRE_PROMPT_VERSION,
            "prompt_style": TRE_PROMPT_STYLE,
            "example_prompt": bare_prompt(eval_records[0]["question"]),
            "example_prompt_fingerprint": prompt_fingerprint(bare_prompt(eval_records[0]["question"])),
        },
        "pool": {
            "file": POOL.relative_to(ROOT).as_posix(),
            "sha256": pool_sha,
            "rows": len(pool_rows),
            "unique_questions": len({row["question_id"] for row in pool_rows}),
            "unique_clusters": len({row["cluster_id"] for row in pool_rows}),
        },
        "files": {
            "triviaqa_eval800": {
                "path": (OUT_DIR / "triviaqa_eval800.jsonl").relative_to(ROOT).as_posix(),
                "samples": len(eval_records),
                "unique_questions": len(eval_ids),
                "unique_clusters": len({row["cluster_id"] for row in eval_records}),
                "sha256": None,
                "first_sample_id": eval_records[0]["sample_id"],
            },
            "smoke20": {
                "path": (OUT_DIR / "smoke20.jsonl").relative_to(ROOT).as_posix(),
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


def build_record_read(row: dict):
    """Reconstruct a :class:`src.tre_repro.TreQuestion` from a serialised row."""
    from src.tre_repro import TreQuestion

    return TreQuestion(
        sample_id=row["sample_id"],
        question_id=row["question_id"],
        cluster_id=row["cluster_id"],
        dataset=row["dataset"],
        split=row["split"],
        question=row["question"],
        gold_answer=row["gold_answer"],
        gold_aliases=tuple(row.get("gold_aliases") or ()),
        gold_normalized_aliases=tuple(row.get("gold_normalized_aliases") or ()),
        answer_type=row.get("answer_type") or "",
        answer_source_field=row.get("answer_source_field") or "",
        source=row.get("source") or {},
        provenance=row.get("provenance") or {},
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--check", action="store_true", help="verify existing files against a fresh build without writing")
    args = parser.parse_args(argv)

    eval_records, smoke_records, manifest = build()
    for name, records in (("triviaqa_eval800", eval_records), ("smoke20", smoke_records)):
        path = OUT_DIR / f"{name}.jsonl"
        serialized = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records)
        digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        manifest["files"][name]["sha256"] = digest
        if args.check:
            if not path.exists() or path.read_bytes() != serialized.encode("utf-8"):
                raise SystemExit(f"{path} differs from a fresh build")
            print(f"[check] {path.relative_to(ROOT)} matches ({len(records)} records, sha256 {digest[:16]})")
        else:
            write_jsonl(path, records)
            print(f"[write] {path.relative_to(ROOT)} ({len(records)} records, sha256 {digest[:16]})")

    if not args.check:
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[write] {MANIFEST.relative_to(ROOT)}")
    print(json.dumps(manifest["validation"], ensure_ascii=False))
    print(json.dumps(manifest["overlap_with_frozen_subsets"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
