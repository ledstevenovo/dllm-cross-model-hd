#!/usr/bin/env python
"""Step-5 label evidence: exclusion reasons and the three report views' question counts."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
import common  # noqa: E402
sys.path.insert(0, str(REPO / "references/repos/DynHD"))
from dynhd.data.io import load_trace  # noqa: E402

OUT = REPO / "reports/dynhd_labels.json"


def reason_bucket(text: str) -> str:
    text = str(text or "")
    if "空" in text:
        return "refusal_empty"
    if "回显" in text:
        return "format_failure_echo"
    if "函数词" in text or "碎片" in text:
        return "format_failure_fragment"
    return "other"


def main() -> int:
    evidence = {"date": common.utc_now(), "reviewer": "ledstevenovo",
                "review_mode": "rule-signoff:2026-10-22", "models": {}}
    test_ids = {}
    for model in ("llada", "dream"):
        root = common.REPRO_ROOT / f"traces/{model}/pilot200"
        split = json.loads((common.REPRO_ROOT / f"splits/{model}/pilot200.json").read_text())
        valid_files = sorted((root / "valid").glob("*.pt"))
        excluded = sorted((root / "excluded").glob("*.pt"))
        excluded_reasons = Counter()
        for path in excluded:
            data = load_trace(str(path))
            excluded_reasons[reason_bucket(data["meta"].get("excluded_reason"))] += 1
        partitions = {}
        for part in ("train", "val", "test"):
            rows = [valid_files[i] for i in split.get(part, [])]
            labels = [int(load_trace(str(path))["label"]) for path in rows]
            partitions[part] = {"n": len(rows), "correct": labels.count(0), "incorrect": labels.count(1)}
        test_ids[model] = {str(load_trace(str(valid_files[i]))["meta"]["id"]) for i in split["test"]}
        evidence["models"][model] = {
            "pilot_answers": 200,
            "valid": len(valid_files), "excluded": len(excluded),
            "excluded_reasons": dict(excluded_reasons),
            "partitions": partitions,
            "view1_failure_and_coverage": {
                "answers": 200, "valid": len(valid_files), "excluded": len(excluded),
                "coverage_of_valid": round(len(valid_files) / 200, 4),
                "excluded_rate": round(len(excluded) / 200, 4)},
            "view2_valid_metrics": "computed in reports/dynhd_eval_%s.json (step 6)" % model,
        }
    common_test = test_ids["llada"] & test_ids["dream"]
    evidence["view3_common_valid_test"] = {
        "llada_test_n": len(test_ids["llada"]), "dream_test_n": len(test_ids["dream"]),
        "common_n": len(common_test),
        "note": "common valid test set within the frozen test partition; metrics in the step-6 evidence",
    }
    OUT.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(evidence, indent=2, ensure_ascii=False))
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
