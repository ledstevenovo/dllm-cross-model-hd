#!/usr/bin/env python
"""Formal entry checks for a reviewed pilot200 valid directory.

Rejects anything that is not human-reviewed, binds labels to answers, and verifies the
frozen split covers every valid file with both classes present in train and val.
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
    parser.add_argument("--model", required=True, choices=["llada", "dream"])
    parser.add_argument("--valid-dir", required=True)
    parser.add_argument("--split", required=True)
    parser.add_argument("--index-map")
    parser.add_argument("--out")
    args = parser.parse_args()

    valid_dir = Path(args.valid_dir).resolve()
    if "pilot200" not in valid_dir.parts or valid_dir.name != "valid":
        raise SystemExit("check_valid only accepts <...>/pilot200/valid")
    problems, labels, fingerprints = [], [], set()
    files = sorted(valid_dir.glob("*.pt"))
    if not files:
        problems.append("valid dir is empty")
    traces = []
    for path in files:
        stem = path.stem
        if len(stem) != 6 or not stem.isdigit():
            problems.append(f"{path.name}: not the {{pilot_index:06d}}.pt convention")
        try:
            data = load_trace(str(path))
        except Exception as error:
            problems.append(f"{path.name}: unloadable: {error}")
            continue
        meta, features, label = data.get("meta", {}), data.get("features"), int(data.get("label", -1))
        if meta.get("test_fixture"):
            problems.append(f"{path.name}: test_fixture data must not enter formal valid")
        if meta.get("human_reviewed") is not True:
            problems.append(f"{path.name}: human_reviewed is not true")
        if meta.get("provisional") is not False:
            problems.append(f"{path.name}: provisional flag not false")
        if not str(meta.get("label_source", "")).startswith("human:"):
            problems.append(f"{path.name}: label_source must be human:<reviewer/run>")
        if label not in (0, 1):
            problems.append(f"{path.name}: label {label} not in {{0,1}}")
        if str(meta.get("answer_sha256")) != common.sha256_text(str(meta.get("generated_text", ""))):
            problems.append(f"{path.name}: answer hash does not bind to generated_text")
        if features is None or features.dim() != 2 or not bool(features.isfinite().all()):
            problems.append(f"{path.name}: features missing/non-finite")
        prompt_emb = data.get("prompt_emb")
        if prompt_emb is not None and (prompt_emb.dim() != 1 or not bool(prompt_emb.isfinite().all())):
            problems.append(f"{path.name}: prompt_emb invalid")
        fingerprints.add(str(meta.get("generation_fingerprint")))
        labels.append(label)
        traces.append({"file": path.name, "label": label, "meta": meta})

    if len(fingerprints) > 1:
        problems.append(f"mixed generation fingerprints: {sorted(fingerprints)}")

    split = json.loads(Path(args.split).read_text())
    for part in ("train", "val", "test"):
        if part not in split:
            problems.append(f"split missing partition {part}")
    if not problems or all("split" not in p for p in problems):
        indices = {part: sorted(int(i) for i in split.get(part, [])) for part in ("train", "val", "test")}
        flat = indices["train"] + indices["val"] + indices["test"]
        if flat != list(range(len(files))):
            problems.append("split does not cover every valid file exactly once")
        for part in ("train", "val"):
            counts = {0: 0, 1: 0}
            for index in indices[part]:
                counts[labels[index]] += 1
            if counts[0] == 0 or counts[1] == 0:
                problems.append(f"partition {part} needs both classes, got {counts}")
        if any(not indices[part] for part in ("train", "val", "test")):
            problems.append("partitions must be non-empty")

    if args.index_map:
        index_map = json.loads(Path(args.index_map).read_text())
        if sorted(int(k) for k in index_map) != list(range(len(files))):
            problems.append("index_map does not cover every valid file")
        for key, row in index_map.items():
            position = int(key)
            if position < len(traces) and traces[position]["file"] != f"{int(row['pilot_index']):06d}.pt":
                problems.append(f"index_map position {key} does not match file name")

    counts = {"total": len(files)}
    for part in ("train", "val", "test"):
        if part in split:
            part_labels = [labels[i] for i in sorted(int(x) for x in split[part]) if i < len(labels)]
            counts[part] = {"n": len(part_labels), "label0": part_labels.count(0), "label1": part_labels.count(1)}
    summary = {"model": args.model, "valid_dir": str(valid_dir), "files": len(files),
               "counts": counts, "fingerprints": sorted(f for f in fingerprints if f != "None"),
               "problems": problems, "ok": not problems}
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "problems"}, indent=2, ensure_ascii=False))
    for problem in problems[:15]:
        print(" !", problem)
    print("check_valid:", "OK" if not problems else "FAILED")
    return 0 if not problems else 2


if __name__ == "__main__":
    raise SystemExit(main())
