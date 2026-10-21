#!/usr/bin/env python
"""Build upstream-format split.json + index_map.json for a valid trace directory.

Split assignment comes from the frozen subset's ``split`` column (train/validation/test);
positions are the sorted file positions in the valid directory, matching what the upstream
training/eval CLIs load. index_map records position -> {pilot_index, sample_id, question_id}.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import common  # noqa: E402

SPLIT_MAP = {"train": "train", "validation": "val", "val": "val", "test": "test"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset", required=True, help="frozen subset jsonl (pilot200)")
    parser.add_argument("--valid-dir", required=True, help="directory with {pilot_index:06d}.pt files")
    parser.add_argument("--out", required=True, help="upstream split.json path")
    parser.add_argument("--index-map", required=True)
    args = parser.parse_args()

    rows = [json.loads(line) for line in Path(args.subset).read_text(encoding="utf-8").splitlines() if line.strip()]
    valid = sorted(Path(args.valid_dir).glob("*.pt"))
    if not valid:
        raise SystemExit("no .pt files in valid dir")
    split = {"train": [], "val": [], "test": []}
    index_map = {}
    for position, path in enumerate(valid):
        stem = path.stem
        if len(stem) != 6 or not stem.isdigit():
            raise SystemExit(f"{path.name} does not follow the {{pilot_index:06d}}.pt convention")
        pilot_index = int(stem)
        if pilot_index >= len(rows):
            raise SystemExit(f"pilot_index {pilot_index} out of range")
        row = rows[pilot_index]
        part = SPLIT_MAP.get(str(row.get("split")))
        if part is None:
            raise SystemExit(f"unknown split value {row.get('split')!r}")
        split[part].append(position)
        index_map[str(position)] = {"pilot_index": pilot_index, "sample_id": row["sample_id"],
                                    "question_id": row["question_id"], "split": part}
    for part, indices in split.items():
        if not indices:
            raise SystemExit(f"partition {part} is empty")
    covered = sorted(split["train"] + split["val"] + split["test"])
    if covered != list(range(len(valid))):
        raise SystemExit("split does not cover every valid file exactly once")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(split, indent=2) + "\n")
    Path(args.index_map).write_text(json.dumps(index_map, indent=2, ensure_ascii=False) + "\n")
    print(f"valid files {len(valid)} -> train/val/test = "
          f"{len(split['train'])}/{len(split['val'])}/{len(split['test'])}")
    print("wrote", args.out, "and", args.index_map)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
