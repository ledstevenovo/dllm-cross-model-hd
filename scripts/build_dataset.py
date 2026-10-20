#!/usr/bin/env python
"""Build the frozen question pool for the cross-model hallucination study.

Pipeline
--------
    raw parquet (sha256-verified)
      -> field extraction + light cleaning
      -> duplicate collapse and identifier-collision clustering
      -> engineering carve-out (smoke20, removed from the research pool)
      -> deterministic global split by cluster (train / validation / test)
      -> stratified small200 subset of test
      -> per-split JSONL + subset JSONL + id index + run manifest

What this script guarantees
---------------------------
* **Reproducibility.**  Same raw files + same config -> byte-identical outputs.
  Every input is verified against its recorded sha256 before a single row is
  read, and every output is hashed into the manifest.
* **No cross-split leakage.**  The split is assigned to a *cluster*, never to a
  row, and the script re-checks after building that no cluster and no identical
  question text appears in more than one split.
* **No prompt/answer leakage.**  Every record's prompt is validated against the
  frozen template and asserted not to contain its own gold answer.
* **Auditability.**  Every dropped row, every collapsed duplicate and every
  identifier collision is counted in the manifest.  Nothing is discarded
  silently.

Run:
    source scripts/env.sh && "$PY" scripts/build_dataset.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import tomllib
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from src.io_utils import (  # noqa: E402
    ensure_dir,
    read_json,
    sha256_file,
    write_json,
    write_jsonl,
)
from src.prompts import (  # noqa: E402
    PROMPT_TEMPLATE_VERSION,
    answer_in_prompt,
    describe as prompt_describe,
    prompt_fingerprint,
    render_prompt,
)
from src.schema import (  # noqa: E402
    RESEARCH_SPLITS,
    SCHEMA_VERSION,
    QARecord,
    validate_records,
)
from src.splitting import assign_splits, select_stratified  # noqa: E402
from src.dedup import cluster_mapping  # noqa: E402
from src.textnorm import (  # noqa: E402
    collapse_whitespace,
    normalize_question,
    normalized_variants,
)

MANIFEST_VERSION = "build-dataset-manifest-v1"
DEFAULT_CONFIG = "configs/datasets/build.toml"
RAW_INDEX = "data/raw_download/raw_index.json"
RAW_QA_DIR = "data/raw_qa"
MANIFEST_DIR = "data/manifests"

#: The carve-out split name; see configs/datasets/build.toml.
SMOKE_SPLIT = "smoke"


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def dig(record: Mapping[str, Any], dotted: str, default: Any = None) -> Any:
    """Read a dotted path out of a nested mapping, tolerating missing keys."""
    if not dotted:
        return default
    current: Any = record
    for part in dotted.split("."):
        if isinstance(current, Mapping) and part in current:
            current = current[part]
        else:
            return default
    return current


def as_list(value: Any) -> list[str]:
    """Coerce a parquet cell into a list of non-empty strings."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, (list, tuple, np.ndarray, pd.Series)):
        return [str(item) for item in list(value) if item is not None and str(item).strip()]
    return [str(value)] if str(value).strip() else []


def clean_text(value: Any) -> str:
    """Whitespace-normalise a string cell without touching its content."""
    if value is None:
        return ""
    return collapse_whitespace(str(value))


def count_by(items: Iterable[Any]) -> dict[str, int]:
    """Count items, returning a key-sorted plain dict for stable manifests."""
    return dict(sorted(Counter(str(item) for item in items).items()))


def config_fingerprint(config: Mapping[str, Any]) -> str:
    """Return ``sha256:<hex>`` over the canonically serialised config."""
    payload = json.dumps(config, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def git_commit(repo_root: str) -> str | None:
    """Read HEAD without spawning a subprocess.

    ``subprocess`` with ``capture_output=True`` needs a pipe, which locked-down
    hosts deny; reading ``.git`` directly always works and never fails a build.
    """
    git_dir = os.path.join(repo_root, ".git")
    head_path = os.path.join(git_dir, "HEAD")
    if not os.path.exists(head_path):
        return None
    try:
        with open(head_path, "r", encoding="utf-8") as handle:
            head = handle.read().strip()
    except OSError:
        return None
    if not head.startswith("ref:"):
        return head or None
    ref = head.split("ref:", 1)[1].strip()
    ref_path = os.path.join(git_dir, *ref.split("/"))
    if os.path.exists(ref_path):
        try:
            with open(ref_path, "r", encoding="utf-8") as handle:
                return handle.read().strip() or None
        except OSError:
            return None
    packed = os.path.join(git_dir, "packed-refs")
    if os.path.exists(packed):
        try:
            with open(packed, "r", encoding="utf-8") as handle:
                for line in handle:
                    if line.startswith(("#", "^")):
                        continue
                    parts = line.split()
                    if len(parts) == 2 and parts[1] == ref:
                        return parts[0]
        except OSError:
            return None
    return None


# ---------------------------------------------------------------------------
# raw -> intermediate records
# ---------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class RawQA:
    """One raw question, before deduplication and clustering."""

    dataset: str
    raw_id: str
    question: str
    gold_answer: str
    gold_aliases: tuple[str, ...]
    gold_norm_aliases: tuple[str, ...]
    answer_type: str
    stratum: str
    row_index: int
    source: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class BuiltRecord:
    """A deduplicated, clustered question, with its frozen split assigned."""

    record: QARecord
    stratum: str


def load_config(path: str) -> dict[str, Any]:
    """Read and sanity-check the TOML build config."""
    with open(path, "rb") as handle:
        config = tomllib.load(handle)
    if config.get("schema_version") != SCHEMA_VERSION:
        raise SystemExit(
            f"config schema_version {config.get('schema_version')!r} does not match "
            f"the code's {SCHEMA_VERSION!r}"
        )
    order = tuple(config["splits"]["order"])
    if order != RESEARCH_SPLITS:
        raise SystemExit(
            f"config splits.order {order!r} must equal src.schema.RESEARCH_SPLITS {RESEARCH_SPLITS!r}"
        )
    if config["subsets"]["smoke_name"] == config["subsets"]["small_name"]:
        raise SystemExit("smoke and small subset names must differ")
    return config


def verify_inputs(
    config: Mapping[str, Any], repo_root: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Verify every consumed raw file against its recorded sha256.

    Returns ``(consumed, index_files)``.  A mismatch is fatal: silently reading a
    different upstream revision would invalidate every downstream number.
    """
    index_path = os.path.join(repo_root, RAW_INDEX)
    if not os.path.exists(index_path):
        raise SystemExit(f"missing raw index {RAW_INDEX}; run scripts/download_raw.py first")
    index_files = read_json(index_path).get("files", {})
    lock_path = os.path.join(repo_root, 'configs/datasets/sources.lock.json')
    locked = {item['key']: item for item in read_json(lock_path)['files']}

    consumed: dict[str, Any] = {}
    for source in config["sources"]:
        key = source["raw_key"]
        if key not in index_files:
            raise SystemExit(f"raw_key {key!r} is not present in {RAW_INDEX}")
        entry = dict(index_files[key])
        for field in ('sha256','revision','repository','url'):
            if entry.get(field) != locked[key][field]:
                raise SystemExit(f'raw index differs from source lock: {key}/{field}')
        absolute = os.path.join(repo_root, entry["path"])
        if not os.path.exists(absolute):
            raise SystemExit(f"missing raw file {entry['path']}; run scripts/download_raw.py")
        digest = sha256_file(absolute)
        if digest != entry.get("sha256"):
            raise SystemExit(
                f"{entry['path']} sha256 mismatch: on-disk {digest} != recorded {entry.get('sha256')}"
            )
        entry["sha256_verified"] = True
        entry["absolute_path"] = absolute
        consumed[key] = entry
    return consumed, index_files


def read_source(
    source: Mapping[str, Any],
    entry: Mapping[str, Any],
    cleaning: Mapping[str, Any],
    stats: Counter,
    dropped: list[dict[str, Any]],
) -> list[RawQA]:
    """Extract cleaned :class:`RawQA` rows from one raw parquet file.

    ``dropped`` collects a bounded sample of the discarded copyable questions so
    the manifest can show *which* items the gold-in-prompt rule removed, rather
    than only how many.  Silently discarding a tenth of a dataset would be
    indefensible; a reviewer must be able to read the discarded items.
    """
    frame = pd.read_parquet(entry["absolute_path"])
    stats[f"{source['dataset']}:rows_read"] += len(frame)

    drop_copyable = bool(cleaning.get("drop_gold_in_prompt", True))
    rows: list[RawQA] = []
    for row_index, row in enumerate(frame.to_dict(orient="records")):
        raw_id = str(dig(row, source["id_field"], row_index)).strip()
        question = clean_text(dig(row, source["question_field"]))
        gold_value = clean_text(dig(row, source["answer_value"]))
        aliases = tuple(
            alias
            for alias in (clean_text(item) for item in as_list(dig(row, source["answer_aliases"])))
            if alias
        )
        norm_aliases = tuple(
            alias
            for alias in (clean_text(item) for item in as_list(dig(row, source["answer_norm_aliases"])))
            if alias
        )
        answer_type = clean_text(dig(row, source["answer_type_field"])) or str(
            source.get("answer_type_default", "unknown")
        )

        if len(question) < int(cleaning["min_question_chars"]):
            stats[f"{source['dataset']}:dropped_empty_question"] += 1
            continue
        if not (int(cleaning["min_gold_chars"]) <= len(gold_value) <= int(cleaning["max_gold_chars"])):
            stats[f"{source['dataset']}:dropped_unusable_gold"] += 1
            continue

        prompt = render_prompt(question)
        # A question that states its own canonical answer can be answered by
        # copying, which would inflate the correct-rate and weaken the label
        # signal behind the detector, so it is excluded by default.  The switch
        # exists so the decision is revisable from the config alone.
        if drop_copyable and answer_in_prompt(prompt, gold_value):
            stats[f"{source['dataset']}:dropped_gold_in_prompt"] += 1
            if len(dropped) < 40:
                dropped.append(
                    {
                        "dataset": source["dataset"],
                        "raw_id": raw_id,
                        "answer_type": answer_type,
                        "gold_answer": gold_value,
                        "question": question,
                    }
                )
            continue
        # An alias phrase in the question is *not* a drop reason: it is usually
        # the question's own wording (see prompts.assert_gold_not_in_prompt).
        # It is counted so the distinction stays visible in the manifest.
        if any(answer_in_prompt(prompt, alias) for alias in aliases):
            stats[f"{source['dataset']}:alias_phrase_in_prompt_kept"] += 1

        stratum = str(source["stratum"])
        stratum_field = source.get("stratum_field")
        if stratum_field:
            refined = clean_text(dig(row, stratum_field)).lower() or "unknown"
            stratum = f"{stratum}_{refined}"

        rows.append(
            RawQA(
                dataset=source["dataset"],
                raw_id=raw_id,
                question=question,
                gold_answer=gold_value,
                gold_aliases=aliases,
                gold_norm_aliases=norm_aliases,
                answer_type=answer_type,
                stratum=stratum,
                row_index=row_index,
                source={
                    "raw_key": source["raw_key"],
                    "repository": entry.get("repository"),
                    "revision": entry.get("revision"),
                    "hf_dataset": entry.get("dataset"),
                    "hf_config": source.get("hf_config"),
                    "hf_split": source.get("hf_split"),
                    "raw_file": entry["path"],
                    "raw_file_sha256": entry.get("sha256"),
                    "raw_row_index": row_index,
                    "raw_id": raw_id,
                    "raw_question_field": source["question_field"],
                },
            )
        )
    stats[f"{source['dataset']}:rows_kept"] += len(rows)
    return rows


def cluster_rows(rows: Sequence[RawQA], stats: Counter) -> list[BuiltRecord]:
    """Collapse duplicate rows and resolve identifier collisions into clusters.

    Two nested groupings, because they mean different things:

    * Rows sharing an identifier **but not** a normalised question are an
      upstream data defect (TriviaQA has exactly one: ``bb_956``).  Both
      questions are real, so both are kept with distinct ``question_id``
      suffixes, and they share a ``cluster_id`` so they can never be split apart.
    * Rows sharing an identifier **and** the normalised question are pure
      duplicate rows (TriviaQA validation has 7,984 such pairs).  One row is
      kept and every collapsed row index is recorded.

    If duplicate rows disagree about the answer, that is recorded as an
    inconsistency: the lowest row index wins, but the disagreement is visible in
    the manifest rather than hidden.
    """
    groups: dict[tuple[str, str], list[RawQA]] = defaultdict(list)
    for row in rows:
        groups[(row.dataset, row.raw_id)].append(row)

    built: list[BuiltRecord] = []
    for (dataset, raw_id), members in groups.items():
        base = f"{dataset}__{raw_id}"
        by_question: dict[str, list[RawQA]] = defaultdict(list)
        for member in members:
            by_question[normalize_question(member.question)].append(member)

        ordered = sorted(by_question.values(), key=lambda group: min(m.row_index for m in group))
        if len(ordered) > 1:
            stats["collisions:identifiers_with_multiple_questions"] += 1
            stats["collisions:extra_variants"] += len(ordered) - 1

        for variant_index, group in enumerate(ordered):
            # Variant 0 keeps the upstream identifier verbatim; extras get a
            # suffix so sample_id stays unique while cluster_id stays shared.
            question_id = base if variant_index == 0 else f"{base}__alt{variant_index}"
            if len(group) > 1:
                stats["dedup:duplicate_rows_collapsed"] += len(group) - 1
                distinct_answers = {
                    tuple(sorted(normalized_variants([m.gold_answer, *m.gold_aliases]))) for m in group
                }
                if len(distinct_answers) > 1:
                    stats["dedup:duplicate_rows_with_conflicting_answers"] += 1
            keeper = min(group, key=lambda m: m.row_index)
            provenance = dict(keeper.source)
            provenance["raw_row_indexes_collapsed"] = sorted(m.row_index for m in group)
            provenance["duplicate_row_count"] = len(group)
            built.append(
                BuiltRecord(
                    record=QARecord(
                        sample_id=question_id,
                        question_id=question_id,
                        cluster_id=base,
                        dataset=dataset,
                        split="",
                        question=keeper.question,
                        gold_answer=keeper.gold_answer,
                        gold_aliases=keeper.gold_aliases,
                        gold_normalized_aliases=keeper.gold_norm_aliases,
                        answer_type=keeper.answer_type,
                        # Filled in by main() once the dataset -> source-column
                        # mapping is known; kept empty here so cluster_rows stays
                        # independent of the config's field names.
                        answer_source_field="",
                        source=provenance,
                    ).finalize(),
                    stratum=keeper.stratum,
                )
            )
    built.sort(key=lambda item: item.record.sample_id)
    return built


# ---------------------------------------------------------------------------
# splitting and subset carving
# ---------------------------------------------------------------------------
def cluster_to_stratum(built: Sequence[BuiltRecord]) -> dict[str, str]:
    """Map each cluster id to its stratum, collapsing variant duplicates.

    A collision cluster contributes several records but only one cluster id, so
    the stratum mapping must be built per cluster; otherwise ``smoke20`` could
    select the same cluster twice and silently produce 19 questions.
    """
    mapping: dict[str, str] = {}
    for item in sorted(built, key=lambda entry: entry.record.cluster_id):
        mapping.setdefault(item.record.cluster_id, item.stratum)
    return mapping


def carve_and_split(
    built: Sequence[BuiltRecord],
    config: Mapping[str, Any],
) -> tuple[dict[str, str], dict[str, list[str]], dict[str, list[str]]]:
    """Assign smoke / train / validation / test and pick the small200 subset.

    Order matters: the smoke carve-out is removed **before** the split, so no
    smoke question can ever carry a research split label, and the small200
    subset is drawn **after** the split, so it is guaranteed to be part of test.

    Returns ``(cluster_split, smoke_selection, small_selection)`` where each
    selection is ``stratum -> [cluster_id, ...]``.
    """
    determinism = config["determinism"]
    base_seed = int(determinism["base_seed"])
    subsets = config["subsets"]

    strata: dict[str, list[str]] = defaultdict(list)
    for cluster_id, stratum in cluster_to_stratum(built).items():
        strata[stratum].append(cluster_id)

    smoke_selection = select_stratified(
        strata,
        int(subsets["smoke_total"]),
        seed=base_seed,
        salt=str(determinism["smoke_salt"]),
    )
    smoke_clusters = {cluster for ids in smoke_selection.values() for cluster in ids}

    remaining = sorted(
        cluster_id
        for cluster_id in cluster_to_stratum(built)
        if cluster_id not in smoke_clusters
    )
    ratios = [(name, float(config["splits"][name])) for name in config["splits"]["order"]]
    cluster_split = assign_splits(
        remaining,
        ratios,
        seed=base_seed,
        salt=str(determinism["split_salt"]),
    )
    for cluster_id in smoke_clusters:
        cluster_split[cluster_id] = SMOKE_SPLIT

    test_strata: dict[str, list[str]] = defaultdict(list)
    for cluster_id, stratum in cluster_to_stratum(built).items():
        if cluster_split.get(cluster_id) == "test":
            test_strata[stratum].append(cluster_id)
    small_selection = select_stratified(
        test_strata,
        int(subsets["small_total"]),
        seed=base_seed,
        salt=str(determinism["subset_salt"]),
    )
    return cluster_split, smoke_selection, small_selection


def flatten(selection: Mapping[str, Sequence[str]]) -> list[str]:
    """Flatten a ``stratum -> ids`` mapping into one sorted id list."""
    return sorted(cluster for ids in selection.values() for cluster in ids)


# ---------------------------------------------------------------------------
# leak checks
# ---------------------------------------------------------------------------
def leak_checks(
    built: Sequence[BuiltRecord],
    smoke_clusters: set[str],
    small_clusters: set[str],
) -> dict[str, Any]:
    """Re-verify, from the finished records, that no leakage exists.

    These checks run on the *output* records rather than on the split
    assignments, so a bug in the writing stage cannot pass unnoticed.
    """
    cluster_to_splits: dict[str, set[str]] = defaultdict(set)
    question_to_splits: dict[str, set[str]] = defaultdict(set)
    question_counts: Counter = Counter()
    sample_counts: Counter = Counter()
    research_samples: set[str] = set()
    test_clusters: set[str] = set()

    for item in built:
        record = item.record
        cluster_to_splits[record.cluster_id].add(record.split)
        question_to_splits[record.question_normalized].add(record.split)
        question_counts[record.question_normalized] += 1
        sample_counts[record.sample_id] += 1
        if record.split in RESEARCH_SPLITS:
            research_samples.add(record.sample_id)
        if record.split == "test":
            test_clusters.add(record.cluster_id)

    cluster_violations = sorted(c for c, s in cluster_to_splits.items() if len(s) > 1)
    cross_split_questions = sorted(q for q, s in question_to_splits.items() if len(s) > 1)
    same_split_duplicate_questions = sorted(
        q for q, s in question_to_splits.items() if len(s) == 1 and question_counts[q] > 1
    )
    duplicate_sample_ids = sorted(s for s, n in sample_counts.items() if n > 1)
    smoke_samples = {
        item.record.sample_id for item in built if item.record.cluster_id in smoke_clusters
    }
    smoke_overlap = sorted(smoke_samples & research_samples)
    small_not_in_test = sorted(small_clusters - test_clusters)
    smoke_not_flagged = sorted(
        item.record.sample_id
        for item in built
        if item.record.cluster_id in smoke_clusters and item.record.split != SMOKE_SPLIT
    )

    return {
        "cluster_split_violations_total": len(cluster_violations),
        "cluster_split_violations": cluster_violations[:20],
        "identical_question_cross_split_total": len(cross_split_questions),
        "identical_question_cross_split": cross_split_questions[:20],
        "identical_question_same_split_total": len(same_split_duplicate_questions),
        "duplicate_sample_ids_total": len(duplicate_sample_ids),
        "duplicate_sample_ids": duplicate_sample_ids[:20],
        "smoke_overlapping_research_pool_total": len(smoke_overlap),
        "smoke_records_with_wrong_split_total": len(smoke_not_flagged),
        "small200_clusters_not_in_test_total": len(small_not_in_test),
        "passed": not (
            cluster_violations
            or cross_split_questions
            or duplicate_sample_ids
            or smoke_overlap
            or small_not_in_test
            or smoke_not_flagged
        ),
    }


def answer_length_stats(records: Sequence[QARecord]) -> dict[str, Any]:
    """Summarise gold-answer lengths so later stages can set thresholds knowingly."""
    lengths = np.asarray([len(record.gold_answer) for record in records], dtype=np.int64)
    if lengths.size == 0:
        return {"count": 0}
    return {
        "count": int(lengths.size),
        "mean": round(float(lengths.mean()), 2),
        "p50": int(np.percentile(lengths, 50)),
        "p90": int(np.percentile(lengths, 90)),
        "p99": int(np.percentile(lengths, 99)),
        "max": int(lengths.max()),
        "over_40_chars": int((lengths > 40).sum()),
        "over_64_chars": int((lengths > 64).sum()),
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--repo-root", default=REPO_ROOT)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="run the whole pipeline and all checks but write no files",
    )
    args = parser.parse_args(argv)

    repo_root = os.path.abspath(args.repo_root)
    os.chdir(repo_root)

    config = load_config(args.config)
    cleaning = config["cleaning"]
    stats: Counter = Counter()

    consumed, index_files = verify_inputs(config, repo_root)

    # ---- extract -----------------------------------------------------------
    answer_value_fields: dict[str, str] = {}
    dropped_examples: list[dict[str, Any]] = []
    rows: list[RawQA] = []
    for source in config["sources"]:
        rows.extend(
            read_source(source, consumed[source["raw_key"]], cleaning, stats, dropped_examples)
        )
        answer_value_fields[source["dataset"]] = source["answer_value"]
    stats["pool:raw_rows_kept"] = len(rows)

    built = cluster_rows(rows, stats)
    mapping, near_duplicate_pairs = cluster_mapping(
        [item.record for item in built], config.get('dedup', {}).get('jaccard_threshold', 0.85))
    built = [replace(item, record=replace(item.record, cluster_id=mapping[item.record.cluster_id]))
             for item in built]
    stats['dedup:near_duplicate_pairs'] = len(near_duplicate_pairs)
    stats["pool:records"] = len(built)
    stats["pool:clusters"] = len({item.record.cluster_id for item in built})

    # Attach the real upstream answer field now that the dataset is known; the
    # field is provenance, so it must name the actual source column.
    built = [
        replace(
            item,
            record=replace(
                item.record,
                answer_source_field=answer_value_fields.get(item.record.dataset, "unknown"),
            ),
        )
        for item in built
    ]

    cluster_split, smoke_selection, small_selection = carve_and_split(built, config)
    smoke_clusters = set(flatten(smoke_selection))
    small_clusters = set(flatten(small_selection))

    for name, cluster_set, expected in (
        (config["subsets"]["smoke_name"], smoke_clusters, int(config["subsets"]["smoke_total"])),
        (config["subsets"]["small_name"], small_clusters, int(config["subsets"]["small_total"])),
    ):
        if len(cluster_set) != expected:
            raise SystemExit(
                f"subset {name}: expected {expected} clusters, selected {len(cluster_set)}"
            )

    finalised: list[BuiltRecord] = []
    for item in built:
        split = cluster_split.get(item.record.cluster_id)
        if not split:
            raise SystemExit(f"cluster {item.record.cluster_id!r} received no split")
        finalised.append(replace(item, record=replace(item.record, split=split)))

    # ---- validate before writing anything ---------------------------------
    validation = validate_records(item.record for item in finalised)
    if validation["problems"] or validation["duplicate_sample_ids"]:
        for problem in validation["problems"][:20]:
            print(f"SCHEMA PROBLEM: {problem}", file=sys.stderr)
        raise SystemExit(f"schema validation failed for {len(validation['problems'])} record(s)")

    checks = leak_checks(finalised, smoke_clusters, small_clusters)
    if not checks["passed"]:
        raise SystemExit(f"leak checks failed: {json.dumps(checks, ensure_ascii=False)[:2000]}")

    if args.dry_run:
        print(f"DRY RUN OK: {len(finalised)} records, no files written")
        print(f"  validation : {validation}")
        print(f"  leak checks: {checks['passed']}")
        for key in sorted(stats):
            print(f"  {key} = {stats[key]}")
        return 0

    # ---- write ------------------------------------------------------------
    created_at = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fingerprint = config_fingerprint(config)
    run_id = f"build_dataset_{created_at}_{fingerprint.split(':')[1][:8]}"

    outputs: list[dict[str, Any]] = []
    datasets = sorted({item.record.dataset for item in finalised})
    for dataset in datasets:
        for split in RESEARCH_SPLITS:
            subset = sorted(
                (item for item in finalised if item.record.dataset == dataset and item.record.split == split),
                key=lambda item: item.record.sample_id,
            )
            path = f"{RAW_QA_DIR}/{dataset}/{split}.jsonl"
            count = write_jsonl(path, (item.record.to_dict() for item in subset))
            outputs.append({"path": path, "records": count, "sha256": sha256_file(path)})

    subset_paths: dict[str, Any] = {}
    for name, cluster_set, expected in (
        (str(config["subsets"]["smoke_name"]), smoke_clusters, int(config["subsets"]["smoke_total"])),
        (str(config["subsets"]["small_name"]), small_clusters, int(config["subsets"]["small_total"])),
    ):
        subset = sorted(
            (item for item in finalised if item.record.cluster_id in cluster_set),
            key=lambda item: item.record.sample_id,
        )
        jsonl_path = f"{RAW_QA_DIR}/subsets/{name}.jsonl"
        count = write_jsonl(jsonl_path, (item.record.to_dict() for item in subset))
        outputs.append({"path": jsonl_path, "records": count, "sha256": sha256_file(jsonl_path)})

        ids_path = f"{RAW_QA_DIR}/subsets/{name}.ids.txt"
        ensure_dir(os.path.dirname(ids_path))
        with open(ids_path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(item.record.sample_id for item in subset) + "\n")
        outputs.append({"path": ids_path, "records": count, "sha256": sha256_file(ids_path)})

        subset_paths[name] = {
            "clusters": len(cluster_set),
            "records": count,
            "expected_clusters": expected,
            "split": subset[0].record.split if subset else None,
            "jsonl": jsonl_path,
            "ids_file": ids_path,
            "by_dataset": count_by(item.record.dataset for item in subset),
            "by_stratum": count_by(item.stratum for item in subset),
            "by_answer_type": count_by(item.record.answer_type for item in subset),
        }

    split_counts: dict[str, Any] = {}
    for split in (*RESEARCH_SPLITS, SMOKE_SPLIT):
        subset = [item for item in finalised if item.record.split == split]
        split_counts[split] = {
            "records": len(subset),
            "clusters": len({item.record.cluster_id for item in subset}),
            "by_dataset": count_by(item.record.dataset for item in subset),
            "by_stratum": count_by(item.stratum for item in subset),
            "by_answer_type": count_by(item.record.answer_type for item in subset),
        }

    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "run_id": run_id,
        "created_at_utc": created_at,
        "schema_version": SCHEMA_VERSION,
        "config_path": args.config,
        "config_fingerprint": fingerprint,
        "config": config,
        "prompt": prompt_describe(),
        "code": {
            "git_commit": git_commit(repo_root),
            "code_sha256": {name: sha256_file(os.path.join(REPO_ROOT, name)) for name in
                            ['scripts/build_dataset.py','src/dedup.py','src/schema.py','src/prompts.py','src/textnorm.py','src/splitting.py','src/io_utils.py']},
            "prompt_module_version": PROMPT_TEMPLATE_VERSION,
            "prompt_fingerprint": prompt_fingerprint(),
            "python": sys.version.split()[0],
            "pandas": pd.__version__,
            "numpy": np.__version__,
        },
        "inputs": [
            {key: value for key, value in consumed[key].items() if key != "absolute_path"}
            for key in sorted(consumed)
        ],
        "available_unused_inputs": {
            key: value for key, value in sorted(index_files.items()) if key not in consumed
        },
        "cleaning": dict(sorted(stats.items())),
        "near_duplicate_pairs": near_duplicate_pairs,
        "excluded_copyable_questions": {
            "rule": (
                "A question is excluded when its canonical gold answer value appears in the "
                "rendered prompt as a normalised token sequence with word boundaries. Such a "
                "question can be answered by copying the prompt."
            ),
            "config_key": "cleaning.drop_gold_in_prompt",
            "active": bool(cleaning.get("drop_gold_in_prompt", True)),
            "alias_policy": (
                "An alias phrase appearing in the question is NOT an exclusion reason and is "
                "only counted (cleaning.*:alias_phrase_in_prompt_kept). TriviaQA questions "
                "routinely reuse an alias phrase as their own wording, where the canonical "
                "answer differs and cannot be copied."
            ),
            "samples": dropped_examples,
        },
        "split_counts": split_counts,
        "subsets": subset_paths,
        "stratification": {
            "smoke_selection_by_stratum": count_by(
                cluster for ids in smoke_selection.values() for cluster in ids
            ),
            "small200_selection_by_stratum": count_by(
                cluster for ids in small_selection.values() for cluster in ids
            ),
        },
        "leak_checks": checks,
        "schema_validation": {
            "checked": validation["checked"],
            "problems": len(validation["problems"]),
            "duplicate_sample_ids": len(validation["duplicate_sample_ids"]),
        },
        "answer_length_distribution": answer_length_stats([item.record for item in finalised]),
        "outputs": outputs,
        "notes": [
            "Only held-out upstream splits are used; neither QA dataset's training corpus is touched.",
            "trivia_qa rc.nocontext/test is deliberately unused: its answer aliases are empty and value is '<unk>'.",
            "smoke20 is carved out before the split and carries split='smoke'; it must never be reported as a metric.",
            "small200 is a deterministic, stratified subset of the test split.",
            "The split is assigned per cluster_id, so identifier collisions and lexical near-duplicate clusters cannot straddle splits.",
            "Questions whose canonical gold answer appears in the prompt are dropped by default (cleaning.drop_gold_in_prompt): they can be answered by copying. Counts are in cleaning.*:dropped_gold_in_prompt and a sample is in excluded_copyable_questions.",
            "Alias phrases appearing in a question are kept and only counted; see excluded_copyable_questions.alias_policy.",
        ],
    }

    ensure_dir(os.path.join(repo_root, MANIFEST_DIR))
    manifest_path = f"{MANIFEST_DIR}/{run_id}.json"
    write_json(manifest_path, manifest)
    write_json(f"{MANIFEST_DIR}/build_dataset_latest.json", manifest)

    # ---- report -----------------------------------------------------------
    print(f"run_id             : {run_id}")
    print(f"prompt fingerprint : {prompt_fingerprint()}")
    print(f"config fingerprint : {fingerprint}")
    print()
    print(f"{'split':<12}{'clusters':>10}{'records':>9}{'triviaqa':>10}{'hotpotqa':>10}")
    for split in (*RESEARCH_SPLITS, SMOKE_SPLIT):
        info = split_counts[split]
        print(
            f"{split:<12}{info['clusters']:>10}{info['records']:>9}"
            f"{info['by_dataset'].get('triviaqa', 0):>10}"
            f"{info['by_dataset'].get('hotpotqa', 0):>10}"
        )
    print()
    for name, info in subset_paths.items():
        print(f"{name:<12} clusters={info['clusters']:<5} records={info['records']:<5} {info['by_stratum']}")
    print()
    print("cleaning / dedup counters:")
    for key in sorted(stats):
        print(f"  {key:<52}{stats[key]:>8}")
    print()
    print(f"leak checks passed : {checks['passed']}")
    print(f"manifest           : {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
