#!/usr/bin/env python
"""Recommend a generation budget from a short pilot's answer-length distribution.

Written after making the same mistake twice in one night. The L64 context cell truncated 97.6% of
answers because I sized it from a *different* configuration's truncation rate, and the L256
prediction failed partly because a bigger block changes how early the model stops. Both would have
been avoided by measuring length first on a 20-question sample.

The recommendation is deliberately conservative: pick the smallest budget whose pilot maximum leaves
headroom, because a budget below the answer distribution silently corrupts every downstream metric
(there is no error, the numbers just quietly mean something else).

Usage:
  .venv/bin/python scripts/choose_budget.py --run /tmp/opencode/smoke256 --headroom 1.5
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def recommend(lengths: list[int], *, headroom: float = 1.5,
              block_multiple: int | None = None) -> tuple[int, float, bool]:
    """Return (suggested budget, fraction at cap, censored flag).

    ``censored`` means too many answers ended at the pilot's maximum, so the observed distribution is
    truncated and the recommendation is only a lower bound. A caller should treat that as a failure
    rather than a suggestion -- this is exactly the state the L64 context cell was in.
    """
    if not lengths:
        raise ValueError("no lengths")
    array = np.array(lengths)
    cap = int(array.max())
    at_cap = float((array >= cap).mean())
    suggestion = array.max() * headroom
    if block_multiple:
        suggestion = math.ceil(suggestion / block_multiple) * block_multiple
    # Censoring means many answers pile up at the maximum *and* the sample has spread elsewhere.
    # A small pilot naturally repeats its max, so a share test alone would flag healthy runs.
    # A pilot is censored if the median sits at the maximum: at least half the answers were cut off,
    # so the observed distribution says nothing about how long answers really get.
    censored = float(np.median(array)) == cap
    return int(suggestion), at_cap, bool(censored)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, help="a completed pilot run directory")
    parser.add_argument("--headroom", type=float, default=1.5,
                        help="multiply the pilot max by this before rounding up (default 1.5)")
    parser.add_argument("--block-multiple", type=int, default=None,
                        help="round the suggestion up to a multiple of this (usually block_size)")
    args = parser.parse_args()

    run = Path(args.run)
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    lengths = []
    for record in manifest["samples"].values():
        with np.load(run / record["path"], allow_pickle=False) as archive:
            meta = json.loads(archive["metadata"].item())
        lengths.append(meta["effective_length"])
    if not lengths:
        raise SystemExit("pilot run has no samples")

    array = np.array(lengths)
    suggestion, at_cap, censored = recommend(lengths, headroom=args.headroom,
                                             block_multiple=args.block_multiple)
    print(f"pilot n={len(array)}  median={np.median(array):.0f}  p95={np.percentile(array, 95):.0f}  "
          f"max={int(array.max())}  at_cap={at_cap:.1%}")
    print(f"recommended budget: {suggestion}  (max x {args.headroom}"
          + (f", rounded to {args.block_multiple}" if args.block_multiple else "") + ")")
    if censored:
        print(f"WARNING: {at_cap:.0%} of the pilot hit the cap, so the distribution is censored "
              "and the recommendation is a lower bound. Re-pilot with a larger budget.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
