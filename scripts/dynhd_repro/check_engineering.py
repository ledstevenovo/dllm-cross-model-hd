#!/usr/bin/env python
"""Engineering-only checks for DynHD traces (provisional/test_fixture allowed).

Never valid for formal metrics; formal data must pass check_valid.py instead.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR.parents[1] / "references/repos/DynHD"))
import common  # noqa: E402
from dynhd.data.io import load_trace  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    data_dir = Path(args.data_dir).resolve()
    engineering_root = (common.REPRO_ROOT / "engineering").resolve()
    if engineering_root not in data_dir.parents and data_dir != engineering_root:
        raise SystemExit(f"check_engineering only accepts paths under {engineering_root}")

    problems, rows = [], []
    labels, dtypes, fingerprints = {}, set(), set()
    for path in sorted(data_dir.glob("*.pt")):
        try:
            data = load_trace(str(path))
        except Exception as error:
            problems.append(f"{path.name}: unloadable: {error}")
            continue
        features = data.get("features")
        meta = data.get("meta", {})
        if features is None or features.dim() != 2 or features.shape[1] < 1:
            problems.append(f"{path.name}: bad features shape {getattr(features, 'shape', None)}")
        elif not bool(features.isfinite().all()):
            problems.append(f"{path.name}: non-finite features")
        label = int(data.get("label", -1))
        if label not in (0, 1):
            problems.append(f"{path.name}: label {label} not in {{0,1}}")
        else:
            labels[label] = labels.get(label, 0) + 1
        if not isinstance(meta, dict) or "labeling_method" not in meta:
            problems.append(f"{path.name}: missing meta.labeling_method")
        method = str(meta.get("labeling_method", ""))
        if method == "openai":
            problems.append(f"{path.name}: upstream placeholder labeling_method=openai was not rewritten")
        if meta.get("provisional") is False and method not in ("test_fixture", "human_reviewed"):
            problems.append(f"{path.name}: non-provisional trace must be test_fixture or human_reviewed")
        dtypes.add(tuple(features.shape) if features is not None else None)
        fingerprints.add(str(meta.get("generation_fingerprint")))
        rows.append({"file": path.name, "label": label, "method": method, "kind": meta.get("provisional_kind")})

    if len(dtypes) > 1:
        problems.append(f"inconsistent feature shapes: {sorted(str(d) for d in dtypes)}")
    summary = {"data_dir": str(data_dir), "files": len(rows), "labels": labels, "dtypes": sorted(str(d) for d in dtypes),
               "fingerprints": sorted(f for f in fingerprints if f and f != "None"),
               "problems": problems, "ok": not problems}
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "problems"}, indent=2, ensure_ascii=False))
    for problem in problems[:10]:
        print(" !", problem)
    print("check_engineering:", "OK" if not problems else "FAILED")
    return 0 if not problems else 2


if __name__ == "__main__":
    raise SystemExit(main())
