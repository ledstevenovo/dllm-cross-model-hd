#!/usr/bin/env python
"""Merge same-config raw runs by sample id into a new directory (never overwrite).

Fingerprints must match exactly; per-item seeds must match; duplicates across runs fail
unless --prefer names a run that wins (same-config only). Provenance is recorded.
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
import torch  # noqa: E402
from dynhd.data.io import load_trace  # noqa: E402


def load_run(run_dir: Path):
    manifest_path = run_dir / "run_manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"{run_dir}: missing run_manifest.json")
    manifest = json.loads(manifest_path.read_text())
    fingerprint = manifest.get("generation_fingerprint")
    seeds = {row["sample_id"]: row["item_seed"] for row in manifest.get("task_list", [])}
    files = {}
    for path in sorted(run_dir.glob("*.pt")):
        data = load_trace(str(path))
        meta = data.get("meta", {})
        sample_id = str(meta.get("id"))
        if sample_id in files:
            raise SystemExit(f"{run_dir}: duplicate sample id inside run: {sample_id}")
        if str(meta.get("generation_fingerprint")) != str(fingerprint):
            raise SystemExit(f"{run_dir}/{path.name}: trace fingerprint differs from run manifest")
        files[sample_id] = {"path": path, "data": data,
                            "answer_sha256": common.sha256_text(str(meta.get("generated_text", "")))}
    return {"dir": run_dir, "manifest": manifest, "fingerprint": fingerprint, "seeds": seeds, "files": files}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--prefer", help="run_id that wins for same-config duplicates")
    args = parser.parse_args()

    runs = [load_run(Path(run).resolve()) for run in args.inputs]
    fingerprints = {run["fingerprint"] for run in runs}
    if len(fingerprints) != 1:
        raise SystemExit(f"refusing to merge different generation fingerprints: {sorted(fingerprints)}")
    out_dir = Path(args.out).resolve()
    if out_dir.exists():
        raise SystemExit(f"merge output already exists: {out_dir}")
    prefer = None
    if args.prefer:
        prefer = next((run for run in runs if run["manifest"]["run_id"] == args.prefer), None)
        if prefer is None:
            raise SystemExit(f"--prefer {args.prefer} does not match any input run_id")

    seen = {}
    provenance = []
    for run in runs:
        for sample_id, entry in run["files"].items():
            if sample_id in seen:
                previous = seen[sample_id]
                if prefer is None or entry is previous:
                    raise SystemExit(f"duplicate sample id {sample_id} across runs; use --prefer to choose")
                if run is prefer:
                    seen[sample_id] = entry
                continue
            seen[sample_id] = entry
        provenance.append({"run_id": run["manifest"]["run_id"], "dir": str(run["dir"]),
                           "files": len(run["files"]), "fingerprint": run["fingerprint"]})
    if not seen:
        raise SystemExit("nothing to merge")

    seeds = {}
    for run in runs:
        for sample_id, seed in run["seeds"].items():
            if sample_id in seen:
                if sample_id in seeds and seeds[sample_id] != seed:
                    raise SystemExit(f"item seed mismatch for {sample_id}")
                seeds[sample_id] = seed

    out_dir.mkdir(parents=True, exist_ok=False)
    for sample_id, entry in sorted(seen.items()):
        target = out_dir / f"{sample_id}.pt"
        data = entry["data"]
        data["meta"] = {**data["meta"], "merged_from": entry["path"].parent.name,
                        "merged_answer_sha256": entry["answer_sha256"]}
        torch.save(data, target)
        load_trace(str(target))
    manifest = {"merge_id": out_dir.name, "generation_fingerprint": runs[0]["fingerprint"],
                "inputs": provenance, "merged_samples": len(seen), "prefer": args.prefer,
                "item_seeds": seeds}
    (out_dir / "merge_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"merged {len(seen)} samples from {len(runs)} runs into {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
