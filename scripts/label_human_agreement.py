#!/usr/bin/env python
"""Human spot-check analysis: human vs rule vs judge labels on the flagged 50 items.

Inputs
  reports/label_spotcheck_human_v1.csv   the human verdict (0=correct, 1=incorrect) + note
  reports/label_spotcheck_sheet.csv      the sheet the human reviewed (rule/judge labels)
Outputs
  reports/label_spotcheck_summary.json   agreements, kappas, disagreement resolution, error rates
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def kappa(pairs: list[tuple[int, int]]) -> float | None:
    n = len(pairs)
    if n == 0:
        return None
    po = sum(1 for a, b in pairs if a == b) / n
    pa = sum(1 for a, _ in pairs if a == 1) / n
    pb = sum(1 for _, b in pairs if b == 1) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe) if pe < 1 else None


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    spread = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return ((centre - spread) / denom, (centre + spread) / denom)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--human", default=str(ROOT / "reports/label_spotcheck_human_v1.csv"))
    parser.add_argument("--sheet", default=str(ROOT / "reports/label_spotcheck_sheet.csv"))
    parser.add_argument("--out", default=str(ROOT / "reports/label_spotcheck_summary.json"))
    args = parser.parse_args()

    human = {(r["source"], r["model"], r["sample_id"]): r for r in read_csv(Path(args.human))}
    sheet = read_csv(Path(args.sheet))
    flagged = [r for r in sheet if r["review_priority"]]
    joined, missing = [], []
    for row in flagged:
        key = (row["source"], row["model"], row["sample_id"])
        if key not in human:
            missing.append(key)
            continue
        entry = dict(row)
        entry["human_label"] = int(human[key]["human_label"])
        entry["human_note"] = human[key]["human_note"]
        entry["rule_label"] = int(row["rule_label"])
        entry["judge_label"] = int(row["judge_label"])
        joined.append(entry)
    if missing:
        print(f"warning: {len(missing)} flagged rows have no human verdict: {missing[:3]}")

    def pair_stats(rows, a, b):
        pairs = [(r[a], r[b]) for r in rows]
        agree = sum(1 for x, y in pairs if x == y)
        k = kappa(pairs)
        lo, hi = wilson(agree, len(pairs))
        return {"n": len(pairs), "agree": agree, "agreement": agree / len(pairs) if pairs else None,
                "kappa": k, "agreement_ci95": [lo, hi]}

    result = {
        "date": "2026-10-22",
        "items_reviewed": len(joined),
        "source_mix": dict(Counter(r["source"] for r in joined)),
        "human_vs_rule": pair_stats(joined, "human_label", "rule_label"),
        "human_vs_judge": pair_stats(joined, "human_label", "judge_label"),
        "rule_vs_judge": pair_stats(joined, "rule_label", "judge_label"),
        "rule_error_rate_vs_human": None, "judge_error_rate_vs_human": None,
        "disagreement_resolution": [],
    }
    for name, key in (("rule_error_rate_vs_human", "rule_label"),
                      ("judge_error_rate_vs_human", "judge_label")):
        errors = sum(1 for r in joined if r[key] != r["human_label"])
        lo, hi = wilson(errors, len(joined))
        result[name] = {"errors": errors, "n": len(joined), "rate": errors / len(joined),
                        "ci95": [lo, hi]}
    for r in joined:
        if r["rule_label"] != r["judge_label"]:
            sided = "rule" if r["human_label"] == r["rule_label"] else (
                "judge" if r["human_label"] == r["judge_label"] else "neither")
            result["disagreement_resolution"].append({
                "source": r["source"], "model": r["model"], "sample_id": r["sample_id"],
                "rule_label": r["rule_label"], "judge_label": r["judge_label"],
                "human_label": r["human_label"], "human_sides_with": sided,
                "human_note": r["human_note"]})
    result["disagreement_tally"] = dict(Counter(d["human_sides_with"]
                                                for d in result["disagreement_resolution"]))
    # per-source agreement
    result["per_source"] = {}
    for source in sorted({r["source"] for r in joined}):
        sub = [r for r in joined if r["source"] == source]
        result["per_source"][source] = {
            "n": len(sub),
            "human_vs_rule": pair_stats(sub, "human_label", "rule_label"),
            "human_vs_judge": pair_stats(sub, "human_label", "judge_label")}
    out = Path(args.out)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in
                      ("items_reviewed", "source_mix", "human_vs_rule", "human_vs_judge",
                       "rule_vs_judge", "rule_error_rate_vs_human", "judge_error_rate_vs_human",
                       "disagreement_tally")},
                     indent=2, ensure_ascii=False))
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
