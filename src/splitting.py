"""Deterministic, cluster-aware splitting and subset carving.

Three properties matter here, and each rules out the obvious shortcut:

1. **Deterministic across machines and Python versions.**  We hash with
   :mod:`hashlib` (stable) and never with the built-in :func:`hash`, which is
   salted per process.  Rebuilding the dataset on another host must reproduce
   the same split byte for byte -- otherwise two models would silently be
   evaluated on different questions.

2. **Leakage clusters are split as a unit.**  TriviaQA contains a genuine
   ``question_id`` collision (two different questions sharing ``bb_956``) and
   the pipeline is designed for semantic near-duplicate clusters later.  Rows
   that belong to the same cluster always land in the same split, so a
   near-duplicate of a training question can never appear in test.

3. **Stratified subsets are drawn from one fixed hash order**, not from a
   shuffled list.  ``smoke20`` and ``small200`` therefore stay stable when new
   questions are added to the pool, which is what makes a 20-question pilot
   comparable with the 200-question run and with the full-scale run.
"""

from __future__ import annotations

import hashlib
import math
from typing import Iterable, Mapping, Sequence

__all__ = [
    "allocate_counts",
    "assign_splits",
    "hash_rank",
    "unit_hash",
]

_MASK64 = (1 << 64) - 1


def _digest(*parts: object) -> bytes:
    """Hash parts with an unambiguous separator.

    ``"\x1f"`` (unit separator) cannot occur in an id, so ``("ab", "c")`` and
    ``("a", "bc")`` hash differently.
    """
    payload = "\x1f".join(str(part) for part in parts).encode("utf-8")
    return hashlib.sha256(payload).digest()


def unit_hash(*parts: object) -> float:
    """Return a deterministic value in ``[0, 1)`` for the given parts."""
    return int.from_bytes(_digest(*parts)[:8], "big") / (1 << 64)


def hash_rank(*parts: object) -> int:
    """Return a deterministic 64-bit rank for ordering (stable tie-free sort)."""
    return int.from_bytes(_digest(*parts)[:8], "big") & _MASK64


def assign_splits(
    cluster_ids: Iterable[str],
    ratios: Sequence[tuple[str, float]],
    *,
    seed: int,
    salt: str,
) -> dict[str, str]:
    """Assign each cluster to exactly one split by hashing its id.

    ``ratios`` is an ordered sequence of ``(split_name, fraction)`` pairs; the
    order defines the cumulative thresholds and must therefore be fixed by the
    caller (we use :data:`src.schema.RESEARCH_SPLITS`).  Hashing -- rather than
    slicing a sorted list -- keeps existing assignments intact when the pool
    grows, which matters because the pool will grow from 200 to 2000 questions.

    Fractions are required to sum to 1 (within floating-point tolerance) so a
    typo in the config cannot silently leave questions unassigned.
    """
    total = sum(fraction for _, fraction in ratios)
    if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError(f"split ratios must sum to 1.0, got {total!r}")

    names = [name for name, _ in ratios]
    if len(set(names)) != len(names):
        raise ValueError("split names must be unique")

    cumulative: list[tuple[str, float]] = []
    running = 0.0
    for name, fraction in ratios:
        running += fraction
        cumulative.append((name, running))

    assignments: dict[str, str] = {}
    for cluster_id in cluster_ids:
        value = unit_hash(seed, salt, cluster_id)
        for name, upper in cumulative:
            if value < upper:
                assignments[cluster_id] = name
                break
        else:  # pragma: no cover - guarding against float rounding at 1.0
            assignments[cluster_id] = names[-1]
    return assignments


def allocate_counts(sizes: Mapping[str, int], total: int) -> dict[str, int]:
    """Allocate ``total`` slots across strata proportionally, by largest remainder.

    Rounding by largest remainder (with the stratum name as a deterministic
    tie-break) guarantees the allocation sums to exactly ``total``, so
    ``small200`` really contains 200 questions and not 198 or 203.
    """
    population = sum(sizes.values())
    if total < 0:
        raise ValueError("total must be non-negative")
    if total > population:
        raise ValueError(f"cannot allocate {total} slots from a population of {population}")
    if population == 0:
        return {name: 0 for name in sizes}

    exact = {name: total * size / population for name, size in sizes.items()}
    counts = {name: int(math.floor(value)) for name, value in exact.items()}
    remaining = total - sum(counts.values())
    if remaining:
        order = sorted(
            sizes,
            key=lambda name: (-(exact[name] - counts[name]), name),
        )
        for name in order[:remaining]:
            counts[name] += 1
    return counts


def select_stratified(
    strata: Mapping[str, Sequence[str]],
    total: int,
    *,
    seed: int,
    salt: str,
) -> dict[str, list[str]]:
    """Pick ``total`` cluster ids proportionally across strata, deterministically.

    Members of each stratum are ordered by :func:`hash_rank` and the first
    ``k`` are taken.  Because the order is a hash of the id alone, the selected
    set for a given ``total`` never changes when the surrounding pool changes.
    """
    counts = allocate_counts({name: len(ids) for name, ids in strata.items()}, total)
    chosen: dict[str, list[str]] = {}
    for name, ids in strata.items():
        ordered = sorted(ids, key=lambda cluster_id: hash_rank(seed, salt, cluster_id))
        chosen[name] = ordered[: counts[name]]
    return chosen
