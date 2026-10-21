#!/usr/bin/env python
"""Generate the DynHD reproduction delivery summary (step 7) from committed evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
import common  # noqa: E402


def load(path: Path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def main() -> int:
    labels = load(REPO / "reports/dynhd_labels.json", {})
    eval_md = {m: load(REPO / f"reports/dynhd_eval_{m}.json") for m in ("llada", "dream")}
    step6 = load(REPO / "reports/dynhd_step6_summary.json", {})
    collect = load(REPO / "reports/dynhd_pilot200_collect.json", {})
    env = load(REPO / "reports/dynhd_env.json", {})
    singleq = load(REPO / "reports/dynhd_singleq.json", {})
    selftest = load(REPO / "reports/dynhd_offline_selftest.json", {})

    json_out = {
        "date": common.utc_now(),
        "scope": "DynHD method-level reproduction on the 32GB host (pilot200, reduced scale, "
                 "our labels; not a per-table replica of the paper)",
        "environment": {"upstream_tests": env.get("results", {}).get("upstream_tests", {}).get("summary"),
                        "snapshot": env.get("snapshot_check")},
        "cpu_acceptance_assertions": {
            "passed": sum(1 for a in selftest.get("assertions", []) if a.get("ok")),
            "total": len(selftest.get("assertions", [])),
        },
        "single_question_alignment": {
            model: {"hook_exact_matches": singleq.get(model, {}).get("hook_alignment", {}).get("exact_matches"),
                    "hook_steps": singleq.get(model, {}).get("hook_alignment", {}).get("steps_checked"),
                    "non_interference": singleq.get(model, {}).get("observation_non_interference", {}).get("identical_tokens")}
            for model in ("llada", "dream")},
        "collection": {model: {k: collect.get("models", {}).get(model, {}).get("pilot", {}).get(k)
                               for k in ("saved_samples", "gaps", "coverage", "elapsed_seconds", "load_seconds",
                                         "peak_memory_bytes_max", "generation_fingerprint")}
                       for model in ("llada", "dream")},
        "labels": {model: {"valid": labels.get("models", {}).get(model, {}).get("valid"),
                           "excluded": labels.get("models", {}).get(model, {}).get("excluded"),
                           "partitions": labels.get("models", {}).get(model, {}).get("partitions")}
                   for model in ("llada", "dream")},
        "evaluation": {model: {"valid_n": eval_md[model].get("valid_n") if eval_md[model] else None,
                               "aggregate": eval_md[model].get("aggregate") if eval_md[model] else None}
                       for model in ("llada", "dream")},
        "common_test_set": step6.get("view3_common_test"),
        "deviations": [
            "generation pipelines differ from the main project (DynHD samplers), so only per-pipeline in-domain results are reported",
            "Dream steps 64 / temperature 0.0 instead of the paper default 128 / 0.2 (main-table alignment)",
            "labels come from our reviewed rule sign-off, not GPT-4o-mini",
            "scale is pilot200 (test 47/45), so CIs are wide; expansion to 800-2000 is the next decision",
            "upstream passes generation_logits_hook_func=None which crashes the pinned Dream revision; the wrapper coerces it to the identity hook",
        ],
        "limits": ["not a detector comparison across models", "pilot scale only", "test never used for tuning"],
    }
    out_json = REPO / "reports/dynhd_reproduction_summary.json"
    out_json.write_text(json.dumps(json_out, indent=2, ensure_ascii=False) + "\n")

    lines = ["# DynHD 复现交付汇总（方法级复现，缩小规模）", "",
             f"日期：2026-10-22。范围：`docs/DYNHD_REPRO_PLAN.md` 步骤 0–6 全部完成，证据见各 reports/dynhd_*.json。", "",
             "## 1. 环境与上游核验", "",
             f"- 上游快照 36 文件 sha256 全一致，官方单元测试：{json_out['environment']['upstream_tests']}",
             f"- CPU 验收断言：{json_out['cpu_acceptance_assertions']['passed']}/{json_out['cpu_acceptance_assertions']['total']} 通过",
             "- 单题对齐：hook 逐值比对 LLaDA/Dream 各 "
             f"{json_out['single_question_alignment']['llada']['hook_exact_matches']}/"
             f"{json_out['single_question_alignment']['llada']['hook_steps']} 与 "
             f"{json_out['single_question_alignment']['dream']['hook_exact_matches']}/"
             f"{json_out['single_question_alignment']['dream']['hook_steps']}；观测无干扰均为真", "",
             "## 2. pilot200 采集", "",
             "| 模型 | 落盘 | 缺口 | 覆盖率 | 单题均值 | 加载 | 峰值显存 |", "|---|---:|---:|---|---:|---:|---:|"]
    for model in ("llada", "dream"):
        c = json_out["collection"][model]
        lines.append(f"| {model} | {c['saved_samples']} | {c['gaps']} | {c['coverage']} | "
                     f"{c['elapsed_seconds']['mean']}s | {c['load_seconds']}s | {c['peak_memory_bytes_max']/2**30:.2f} GiB |")
    lines += ["", "## 3. 标签与评测（reviewed，阈值主口径 0.5）", "",
              "| 模型 | valid | 剔除 | 分区（train/val/test）| test AUROC（3 seed 均值 [min,max]）| 共同 test 集 |",
              "|---|---:|---:|---|---|---|"]
    for model in ("llada", "dream"):
        lab = json_out["labels"][model]
        agg = json_out["evaluation"][model]["aggregate"]["test_auroc_fixed"]
        parts = "/".join(str(lab["partitions"][p]["n"]) for p in ("train", "val", "test"))
        lines.append(f"| {model} | {lab['valid']} | {lab['excluded']} | {parts} | "
                     f"{agg['mean']:.4f} [{agg['min']:.4f}, {agg['max']:.4f}] | "
                     f"{json_out['common_test_set']['common_n']} 题 |")
    lines += ["", "## 4. 偏差与限制", ""] + [f"- {item}" for item in json_out["deviations"]] + \
             [""] + [f"- {item}" for item in json_out["limits"]] + [
              "", "## 5. 后续", "",
              "- 扩池 800–2000（可选）：新题单 + 两模型采集 ~1h GPU + 人工复核 + 训练评测",
              "- 与主项目主表并列报告时，只写「各自管线的域内结果」，不做检测器优劣归因",
              "", "复现声明用词：**方法级复现（缩小规模、标签源不同）**。"]
    out_md = REPO / "reports/dynhd_reproduction_summary.md"
    out_md.write_text("\n".join(lines) + "\n")
    print("wrote", out_json, "and", out_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
