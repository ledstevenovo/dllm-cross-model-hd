#!/usr/bin/env python
"""Freeze the pool-expansion question list BEFORE any new results exist (main plan section 8).

Pre-registered rules (do not change after new results are seen):

1. Target size: 800 questions per model in total (train 480 / validation 120 / test 200,
   the same 60/15/25 proportions as pilot200). The 200 pilot questions keep their existing
   split; only new clusters are added, so nothing already collected is re-collected or
   re-split.
2. Pool: the per-split raw pools ``data/raw_qa/<dataset>/<split>.jsonl``; one representative
   row per cluster (lowest sample_id wins), exactly as in ``build_pilot.py``.
3. Strata: ``hotpotqa:<answer_type>`` and ``triviaqa`` (same as pilot200); allocation is
   proportional to the surviving pool (``src.splitting.select_stratified``).
4. Exclusions: every cluster already used by any existing experiment is removed from the pool
   -- pilot200 (which is also what the DynHD reproduction collected), small200, smoke20
   (main), and the TRE R1 eval800 + TRE smoke20 question lists.
5. Determinism: seed 20261022, salt ``<name>-<split>``; selection is hash-ranked, so it
   does not depend on labels, scores or any result.  ``--name`` is part of the salt, so a
   rerun must pass the same ``--name`` to reproduce a frozen list; a different name yields a
   different (not nested) selection.
6. Freeze artefacts: full list (pilot + new), the new-only collection list, and a manifest
   with counts, per-stratum tables, cluster-disjointness assertions and sha256 hashes.

Run: .venv/bin/python scripts/build_expansion_subset.py --total 2000 --name pool2000_v1
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.splitting import select_stratified  # noqa: E402

SEED = 20261022
EXCLUDE_FILES = [
    "data/raw_qa/subsets/pilot200.jsonl",
    "data/raw_qa/subsets/small200.jsonl",
    "data/raw_qa/subsets/smoke20.jsonl",
    "data/tre_repro/questions/triviaqa_eval800.jsonl",
    "data/tre_repro/questions/smoke20.jsonl",
]
SPLIT_SHARE = {"train": 0.60, "validation": 0.15, "test": 0.25}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def stratum_of(row: dict) -> str:
    return row["dataset"] + ":" + row["answer_type"] if row["dataset"] == "hotpotqa" else row["dataset"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--total", type=int, default=800)
    parser.add_argument("--name", default="pool800_v1")
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    pool: dict[str, list[dict]] = {}
    for split in SPLIT_SHARE:
        rows = []
        for path in sorted((ROOT / "data/raw_qa").glob(f"*/{split}.jsonl")):
            rows.extend(read_jsonl(path))
        pool[split] = rows

    used_questions, used_clusters = set(), set()
    qid_to_cluster = {row["question_id"]: row["cluster_id"]
                      for rows in pool.values() for row in rows}
    for rel in EXCLUDE_FILES:
        path = ROOT / rel
        if not path.exists():
            print(f"warning: exclusion file missing: {rel}")
            continue
        for row in read_jsonl(path):
            qid = str(row.get("question_id") or row.get("sample_id"))
            used_questions.add(qid)
            cluster = row.get("cluster_id") or qid_to_cluster.get(qid)
            if cluster:
                used_clusters.add(str(cluster))

    pilot = read_jsonl(ROOT / "data/raw_qa/subsets/pilot200.jsonl")
    excluded_cluster_count = len(used_clusters)
    kept_by_split = Counter(row["split"] for row in pilot)
    targets = {split: max(share * args.total, kept_by_split[split])
               for split, share in SPLIT_SHARE.items()}
    if sum(targets.values()) != args.total:
        raise SystemExit(f"target allocation {targets} does not sum to {args.total}")

    new_rows, selection_tables = [], {}
    for split in ("train", "validation", "test"):
        remaining = [row for row in pool[split] if str(row["cluster_id"]) not in used_clusters]
        by_cluster: dict[str, dict] = {}
        for row in sorted(remaining, key=lambda r: r["sample_id"]):
            by_cluster.setdefault(str(row["cluster_id"]), row)
        strata: dict[str, list[str]] = {}
        for cluster, row in by_cluster.items():
            strata.setdefault(stratum_of(row), []).append(cluster)
        need = int(targets[split]) - kept_by_split[split]
        picked = select_stratified(strata, need, seed=args.seed, salt=f"{args.name}-{split}")
        chosen = [by_cluster[cid] for ids in picked.values() for cid in ids]
        if len(chosen) != need:
            raise SystemExit(f"{split}: picked {len(chosen)} != needed {need}")
        pool_counts = Counter(stratum_of(by_cluster[c]) for c in by_cluster)
        selection_tables[split] = {
            "kept_pilot": int(kept_by_split[split]), "new": need, "total": int(targets[split]),
            "per_stratum": {name: {"pool_remaining": pool_counts.get(name, 0), "new": len(ids)}
                            for name, ids in sorted(picked.items())},
        }
        new_rows.extend(chosen)
        for row in chosen:
            used_clusters.add(str(row["cluster_id"]))

    full_rows = sorted(pilot + new_rows, key=lambda r: (r["split"], r["sample_id"]))
    new_sorted = sorted(new_rows, key=lambda r: (r["split"], r["sample_id"]))

    # ---- assertions: disjointness and coverage
    cluster_split: dict[str, set[str]] = {}
    for row in full_rows:
        cluster_split.setdefault(str(row["cluster_id"]), set()).add(row["split"])
    straddling = {c: s for c, s in cluster_split.items() if len(s) > 1}
    if straddling:
        raise SystemExit(f"cluster(s) straddle splits: {list(straddling)[:5]}")
    dup = [sid for sid, n in Counter(row["question_id"] for row in full_rows).items() if n > 1]
    if dup:
        raise SystemExit(f"duplicate question ids in the frozen list: {dup[:5]}")
    overlap = [row["question_id"] for row in new_rows if row["question_id"] in used_questions]
    if overlap:
        raise SystemExit(f"new selection overlaps an excluded set: {overlap[:5]}")

    full_path = ROOT / "data/raw_qa/subsets" / f"{args.name}.jsonl"
    new_path = ROOT / "data/raw_qa/subsets" / f"{args.name}_new.jsonl"
    for path, rows in ((full_path, full_rows), (new_path, new_sorted)):
        path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows),
                        encoding="utf-8", newline="\n")

    combined = Counter(row["split"] for row in full_rows)
    combined_by_stratum = Counter(f"{row['split']}/{stratum_of(row)}" for row in full_rows)
    manifest = {
        "name": args.name, "created": "2026-10-22", "seed": args.seed,
        "rules": {
            "target_total_per_model": args.total,
            "split_shares": SPLIT_SHARE,
            "pilot_kept": dict(kept_by_split),
            "one_representative_row_per_cluster": True,
            "strata": "hotpotqa:<answer_type>, triviaqa",
            "allocation": "proportional to surviving pool (src.splitting.select_stratified)",
            "exclusions": EXCLUDE_FILES,
            "result_independent": "selection uses hash-ranked cluster order only",
        },
        "counts": {"combined": dict(combined), "new": dict(Counter(r["split"] for r in new_rows))},
        "combined_by_split_and_stratum": dict(sorted(combined_by_stratum.items())),
        "selection_tables": selection_tables,
        "excluded_clusters_before_selection": excluded_cluster_count,
        "paths": {
            "full": str(full_path.relative_to(ROOT)).replace("\\", "/"),
            "new": str(new_path.relative_to(ROOT)).replace("\\", "/"),
        },
        "sha256": {
            "full": hashlib.sha256(full_path.read_bytes()).hexdigest(),
            "new": hashlib.sha256(new_path.read_bytes()).hexdigest(),
        },
        "question_ids": {"full": [r["question_id"] for r in full_rows],
                         "new": [r["question_id"] for r in new_sorted]},
        "note": "frozen BEFORE any new collection or results; the analysis set is pilot200 + new",
    }
    manifest_path = ROOT / "data/manifests" / f"{args.name}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"counts": manifest["counts"], "selection_tables": selection_tables,
                      "full": manifest["paths"]["full"], "new": manifest["paths"]["new"],
                      "sha256_new": manifest["sha256"]["new"][:16] + "…"}, indent=2, ensure_ascii=False))
    print("wrote", full_path, "and", new_path, "and", manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
