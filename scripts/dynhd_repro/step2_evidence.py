#!/usr/bin/env python
"""Assemble step-2 single-question evidence into reports/dynhd_singleq.json.

Merges the wrapper acceptance runs (load time, per-item timing/VRAM, features) with the
alignment/non-interference/decode checks already written by acceptance_single.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO / "references/repos/DynHD"))
import common  # noqa: E402
import torch  # noqa: E402
from dynhd.data.io import load_trace  # noqa: E402

OUT = REPO / "reports/dynhd_singleq.json"


def run_evidence(model: str) -> dict:
    run = common.REPRO_ROOT / f"acceptance/{model}/raw/single"
    manifest = json.loads((run / "run_manifest.json").read_text())
    rendered_tokens = {row.get("sample_id"): row.get("rendered_prompt_tokens")
                       for row in (json.loads(line) for line in
                                   (common.REPRO_ROOT / f"subsets/{model}_acceptance.jsonl").read_text().splitlines()
                                   if line.strip())}
    items = []
    for path in sorted(run.glob("*.pt")):
        data = load_trace(str(path))
        meta = data["meta"]
        features = data["features"]
        items.append({
            "file": path.name,
            "sample_id": meta.get("id"),
            "question_id": meta.get("question_id"),
            "generated_text": meta.get("generated_text"),
            "provisional_label": int(data["label"]),
            "provisional_kind": meta.get("provisional_kind"),
            "elapsed_seconds": meta.get("elapsed_seconds"),
            "actual_T": meta.get("actual_T"),
            "peak_memory_bytes": meta.get("peak_memory_bytes"),
            "features_shape": list(features.shape),
            "features_finite": bool(features.isfinite().all()),
            "features_mean": round(float(features.mean()), 4),
            "features_max": round(float(features.max()), 4),
            "features_topk_mean_column": round(float(features[:, 2].mean()), 4),
            "prompt_emb_dim": int(data["prompt_emb"].numel()),
            "prompt_emb_finite": bool(data["prompt_emb"].isfinite().all()),
            "answer_sha256": meta.get("answer_sha256"),
            "item_seed": meta.get("item_seed"),
            "generation_fingerprint": meta.get("generation_fingerprint"),
            "raw_file_sha256": common.sha256_file(path),
            "rendered_prompt_tokens": rendered_tokens.get(meta.get("id")),
            "final_input_tokens": (rendered_tokens.get(meta.get("id")) or 0) + int(meta.get("actual_T") or 0),
        })
    return {"run_dir": str(run), "run_id": manifest["run_id"], "load_seconds": manifest.get("load_seconds"),
            "device": manifest["environment"], "saved": manifest["saved_count"],
            "failed": manifest["failed_count"], "not_started": manifest["not_started_count"], "items": items}


def main() -> int:
    evidence = json.loads(OUT.read_text()) if OUT.exists() else {}
    evidence["date"] = common.utc_now()
    evidence["single_runs"] = {model: run_evidence(model) for model in ("llada", "dream")}
    evidence["predefined_branches"] = {
        "T_equals_steps": "normal, main run",
        "systematic_T_lt_steps": "separate run_id and steps config, reported separately, never mixed with the main run",
        "sporadic_T_lt_steps": "sample marked invalid, investigated, no silent rewriting",
    }
    evidence["upstream_deviations"] = [{
        "item": "Dream generation_logits_hook_func=None",
        "detail": ("Upstream DynHD passes generation_logits_hook_func=None; the pinned Dream revision "
                   "(05334cb9) calls it unconditionally (generation_utils.py:307/415) and raises "
                   "TypeError. The wrapper coerces None to the identity hook on the model wrapper "
                   "instance (never in the upstream snapshot); first failed attempt archived at "
                   "acceptance/dream/raw/single_failed_logits_hook."),
        "effect": "none on sampling semantics; enables the Dream single-question run",
    }]
    evidence["main_config_alignment"] = {
        "steps": 64, "gen_length": 64, "temperature_llada": 0.0, "temperature_dream": 0.0,
        "dream_alg": "entropy", "dream_alg_temp": 0.0,
        "note": "paper default Dream steps 128 / temperature 0.2; main-table alignment recorded as deviation",
    }
    OUT.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({model: {"load_seconds": evidence["single_runs"][model]["load_seconds"],
                              "saved": evidence["single_runs"][model]["saved"],
                              "items": [{"id": item["sample_id"], "elapsed": item["elapsed_seconds"],
                                         "peak_alloc": item["peak_memory_bytes"]["allocated"] if item["peak_memory_bytes"] else None,
                                         "T": item["actual_T"], "prompt_emb": item["prompt_emb_dim"]}
                                        for item in evidence["single_runs"][model]["items"]]}
                        for model in ("llada", "dream")}, indent=2, ensure_ascii=False))
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
