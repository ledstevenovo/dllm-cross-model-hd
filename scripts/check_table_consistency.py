#!/usr/bin/env python
"""Cross-check every TRE figure quoted in the reports against the metrics files.

A sign error slipped into the write-up tonight: Dream's closed-book HotpotQA scored 82.24
against the paper's 80.6, which is +1.6, but three documents said -1.6. Nothing failed and no
test caught it -- it was found by eyeballing a generated summary table next to the prose. Since
these numbers are the paper's claims, they should be checked mechanically.

This walks the markdown reports for "AA.BB" style AUROC percentages and verifies that every
value matching a known run's AUROC (within 0.01) is quoted with the correct sign relative to
that run's paper reference. It is deliberately narrow: it only checks values it can attribute
to a run, and says nothing about numbers it cannot match.

Exit code is 1 when a contradiction is found, so it can gate a commit.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELLS = ROOT / "reports/tre_repro/all_cells.json"
REPORTS = [
    ROOT / "reports/paper_draft.md",
    ROOT / "reports/tre_repro/context_effect_confirmed.md",
    ROOT / "reports/tre_repro/five_cells.json",
]
DELTA = re.compile(r"([−+\-])\s*(\d+\.\d+)\s*(?:pp)?")
# Numbers may appear as AUROC decimals (0.8224) or percentages (82.24); the old pattern capped
# the fraction at two digits, which silently truncated 0.8224 to 0.82 and matched nothing.
NUMBER = re.compile(r"(\d+\.\d+)")


def main() -> int:
    if not CELLS.exists():
        print("no all_cells.json; run scripts/tre_table.py first", file=sys.stderr)
        return 1
    cells = json.loads(CELLS.read_text(encoding="utf-8"))["cells"]
    known = {(round(c["auroc"] * 100, 2), c["paper_128"]): c
             for c in cells if c["paper_128"] and c["comparable_to_paper"]}

    problems = []
    for path in REPORTS:
        if not path.exists() or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            # find "ours paper delta" triples: two percentages then a signed delta
            nums = NUMBER.findall(line)
            if len(nums) < 3:
                continue
            deltas = DELTA.findall(line)
            if not deltas:
                continue
            for ours_s, paper_s in zip(nums, nums[1:]):
                ours_raw, paper_raw = float(ours_s), float(paper_s)
                # accept either scale: 0.8224 vs 80.6, or 82.24 vs 80.6
                for scale in (100.0, 1.0):
                    ours, paper = round(ours_raw * scale, 2), round(paper_raw, 2)
                    cell = known.get((ours, paper))
                    if cell:
                        break
                if not cell:
                    continue
                expected = ours - paper
                for sign, mag in deltas:
                    value = float(mag)
                    if abs(value - abs(expected)) > 0.15:
                        continue
                    actual_sign = -1 if sign in "−-" else 1
                    if expected != 0 and actual_sign != (1 if expected > 0 else -1):
                        problems.append(
                            f"{path.relative_to(ROOT)}:{line_no} quotes {sign}{mag} for "
                            f"{ours} vs paper {paper}, but {ours} - {paper} = {expected:+.2f}")

    if problems:
        print("INCONSISTENT SIGNS:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1
    print(f"checked {len(known)} attributable cells across {len(REPORTS)} files: signs consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
