#!/usr/bin/env python
"""Assemble DynHD step-4 pilot200 evidence into reports/dynhd_pilot200_collect.json.

Covers: calibration runs, pilot runs (hash-verified), gap/failure counts, timing and memory
statistics, actual-T distribution, label distribution, merged snapshot provenance, and the
measured cost expression T = 200*t_llada + 200*t_dream + load/IO.
"""
from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO / "references/repos/DynHD"))
import common  # noqa: E402
import torch  # noqa: E402

OUT = REPO / "reports/dynhd_pilot200_collect.json"
SUBSET = REPO / "data/raw_qa/subsets/pilot200.jsonl"


def parse_ts(text: str):
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")


def run_summary(run_dir: Path, expected_ids=None) -> dict:
    manifest = json.loads((run_dir / "run_manifest.json").read_text())
    events = [json.loads(line) for line in (run_dir / "events.jsonl").read_text().splitlines() if line.strip()]
    saved_events = {row["sample_id"]: row for row in events if row["event"] == "saved"}
    started = parse_ts(events[0]["ts"]) if events else None
    finished = parse_ts(events[-1]["ts"]) if events else None
    elapsed, peaks, actual_t, labels = [], [], [], {}
    hash_ok, problems = 0, []
    for path in sorted(run_dir.glob("*.pt")):
        data = torch.load(path, map_location="cpu", weights_only=True)
        meta = data["meta"]
        sample_id = str(meta.get("id"))
        event = saved_events.get(sample_id)
        if event is None:
            problems.append(f"{sample_id}: no saved event")
        elif event.get("file") != path.name or event.get("file_sha256") != common.sha256_file(path):
            problems.append(f"{sample_id}: file hash does not match the saved event")
        else:
            hash_ok += 1
        elapsed.append(float(meta.get("elapsed_seconds", 0.0)))
        peaks.append(int((meta.get("peak_memory_bytes") or {}).get("allocated", 0)))
        actual_t.append(int(meta.get("actual_T") or 0))
        labels[int(data["label"])] = labels.get(int(data["label"]), 0) + 1
    gaps = json.loads((run_dir / "gaps.json").read_text())["gaps"] if (run_dir / "gaps.json").exists() else []
    missing = sorted(set(expected_ids) - set(saved_events))[:5] if expected_ids is not None else None
    return {
        "run_dir": str(run_dir), "run_id": manifest["run_id"],
        "load_seconds": manifest.get("load_seconds"),
        "device_memory_after_load": manifest.get("device_memory_after_load"),
        "generation_fingerprint": manifest["generation_fingerprint"],
        "task_list_sha256": manifest["task_list_sha256"],
        "saved_samples": len(saved_events), "files": len(list(run_dir.glob("*.pt"))),
        "hash_verified": hash_ok,
        "expected_ids": len(expected_ids) if expected_ids is not None else None,
        "missing_ids_sample": missing,
        "coverage": ("complete" if expected_ids is not None and not missing else
                     ("partial" if missing else None)),
        "gaps": len(gaps), "gap_states": sorted({g["state"] for g in gaps}),
        "labels": labels, "actual_T_values": sorted(set(actual_t)),
        "elapsed_seconds": {
            "mean": round(statistics.mean(elapsed), 4) if elapsed else None,
            "median": round(statistics.median(elapsed), 4) if elapsed else None,
            "p95": round(sorted(elapsed)[int(0.95 * (len(elapsed) - 1))], 4) if elapsed else None,
            "min": round(min(elapsed), 4) if elapsed else None,
            "max": round(max(elapsed), 4) if elapsed else None,
            "total": round(sum(elapsed), 1) if elapsed else None,
        },
        "peak_memory_bytes_max": max(peaks) if peaks else None,
        "sampling_wall_seconds": round((finished - started).total_seconds(), 1) if started and finished else None,
        "problems": problems,
    }


def main() -> int:
    expected = [json.loads(line)["sample_id"] for line in SUBSET.read_text(encoding="utf-8").splitlines() if line.strip()]
    evidence = {"date": common.utc_now(), "subset": str(SUBSET), "subset_size": len(expected),
                "models": {}, "cost": {}, "notes": [
                    "pilot200 = 120 train / 30 validation / 50 test (frozen pool order)",
                    "calibration runs stay outside the pilot tree and are never merged",
                    "raw files follow the pilot200.jsonl row order as {pilot_index:06d}.pt",
                ]}
    for model in ("llada", "dream"):
        root = common.REPRO_ROOT / f"traces/{model}/pilot200"
        evidence["models"][model] = {
            "calibration": run_summary(common.REPRO_ROOT / f"acceptance/{model}/raw/calibration5"),
            "pilot": run_summary(root / "raw/pilot200_v1", expected),
            "merged": (lambda merged: {
                "dir": str(merged),
                "files": len(list(merged.glob("*.pt"))),
                "merge_manifest": json.loads((merged / "merge_manifest.json").read_text())
                if (merged / "merge_manifest.json").exists() else None,
            })(root / "merged/pilot200_v1_merged"),
        }
        refill = root / "raw/pilot200_v1_refill1"
        if refill.exists():
            evidence["models"][model]["refill"] = run_summary(refill)
        calibration = evidence["models"][model]["calibration"]["elapsed_seconds"]["mean"]
        pilot = evidence["models"][model]["pilot"]["elapsed_seconds"]["mean"]
        load = evidence["models"][model]["pilot"]["load_seconds"]
        evidence["cost"][model] = {"mean_seconds_per_item": pilot, "load_seconds": load,
                                   "calibration_mean_seconds": calibration,
                                   "estimated_200_items_seconds": round(200 * pilot, 1)}
    estimate = sum(evidence["cost"][m]["estimated_200_items_seconds"] for m in ("llada", "dream"))
    evidence["cost"]["expression"] = "T = 200*t_llada + 200*t_dream + load/IO"
    evidence["cost"]["estimated_seconds"] = round(estimate, 1)
    evidence["cost"]["measured_sampling_wall_seconds"] = {
        model: evidence["models"][model]["pilot"]["sampling_wall_seconds"] for model in ("llada", "dream")}
    OUT.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({model: {"pilot_saved": evidence["models"][model]["pilot"]["saved_samples"],
                              "gaps": evidence["models"][model]["pilot"]["gaps"],
                              "mean_s": evidence["cost"][model]["mean_seconds_per_item"],
                              "wall_s": evidence["models"][model]["pilot"]["sampling_wall_seconds"],
                              "merged_files": evidence["models"][model]["merged"]["files"]}
                      for model in ("llada", "dream")}, indent=2, ensure_ascii=False))
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
