#!/usr/bin/env python
"""Cross-artifact digest of the overnight no-GPU run (read-only, tolerant of missing inputs).

The queue's step 11 report is a log-tail excerpt. This digest instead reads the structured
artifacts (stage-7 matrix, multiseed, importance, stability, TRE, DynHD) and prints the numbers
that matter in one page, together with provenance (git HEAD, step markers) and explicit caveats
for partial runs.

Usage: .venv/bin/python scripts/morning_digest.py [--out reports/morning_digest.md]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
LOG = Path("/root/autodl-tmp/overnight_logs")
DONE = LOG / ".done"

SHORT = {
    "LLaDA": "LLaDA",
    "Dream": "Dream",
    "GSAI-ML/LLaDA-8B-Instruct": "LLaDA",
    "Dream-org/Dream-v0-Instruct-7B": "Dream",
}
STEPS = ["01_backup", "02_labels", "03_stage7", "04_tre_offline", "05_tre_permutation",
         "06_multiseed", "07_importance", "08_stability", "09_dynhd", "10_consistency",
         "11_report", "12_commit"]


def short(model: str) -> str:
    return SHORT.get(model, model.split("/")[-1][:14])


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def load_csv(path: Path):
    try:
        return pd.read_csv(path)
    except Exception:
        return None


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True,
                              text=True, timeout=30).stdout.strip()
    except Exception as e:  # noqa: BLE001
        return f"(git failed: {e})"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(REPO / "reports/morning_digest.md"))
    args = parser.parse_args()
    out_path = Path(args.out)
    lines: list[str] = []
    warn: list[str] = []

    def w(text: str = "") -> None:
        lines.append(text)

    def table(rows: list[list[str]], header: list[str]) -> None:
        w("| " + " | ".join(header) + " |")
        w("|" + "|".join(["---"] * len(header)) + "|")
        for r in rows:
            w("| " + " | ".join(str(c) for c in r) + " |")
        w()

    # ---------------------------------------------------------------- provenance
    done = sorted(p.name for p in DONE.glob("*")) if DONE.exists() else []
    pending = [s for s in STEPS if s not in done]
    w(f"# 隔夜无卡运行汇总（生成于 {time.strftime('%Y-%m-%d %H:%M')}）")
    w()
    w(f"- git HEAD: `{git('log', '-1', '--format=%h %s')}`")
    clean = git("status", "--porcelain")
    w(f"- 工作树: {'干净' if not clean else '有未提交改动（见 git status）'}")
    w(f"- 步骤标记: {len([s for s in STEPS if s in done])}/12 完成"
      + (f"，未完成: {' '.join(pending)}" if pending else "，全部完成"))
    w(f"- 队列结束标记: {'是' if LOG.joinpath('driver.log').exists() and 'overnight v4 done' in LOG.joinpath('driver.log').read_text() else '否（可能仍在运行）'}")
    w()

    # ---------------------------------------------------------------- 1 stage7
    tm = load_csv(REPO / "results/stage7/main/transfer_matrix.csv")
    if tm is None:
        warn.append("results/stage7/main/transfer_matrix.csv 缺失")
    else:
        sub = tm[(tm.axis == "model") & (tm.dataset == "all")]
        w("## 1. 主项目迁移矩阵（pilot200 reviewed，dataset=all）")
        w()
        rows = []
        for fs in ("relative_normalized", "entropy_raw"):
            for src, dst, label in (
                ("GSAI-ML/LLaDA-8B-Instruct", "GSAI-ML/LLaDA-8B-Instruct", "LLaDA 域内"),
                ("Dream-org/Dream-v0-Instruct-7B", "Dream-org/Dream-v0-Instruct-7B", "Dream 域内"),
                ("GSAI-ML/LLaDA-8B-Instruct", "Dream-org/Dream-v0-Instruct-7B", "LLaDA → Dream"),
                ("Dream-org/Dream-v0-Instruct-7B", "GSAI-ML/LLaDA-8B-Instruct", "Dream → LLaDA"),
            ):
                cells = {}
                for kind in ("lr", "mlp"):
                    hit = sub[(sub.feature_set == fs) & (sub.kind == kind)
                              & (sub.source == src) & (sub.target == dst)]
                    if len(hit):
                        r = hit.iloc[0]
                        cells[kind] = f"{r.auroc:.3f} [{r.auroc_low:.2f},{r.auroc_high:.2f}] n={int(r.n)}"
                    else:
                        cells[kind] = "-"
                rows.append([fs, label, cells["lr"], cells["mlp"]])
        table(rows, ["特征集", "方向", "LR（95% CI）", "MLP（95% CI）"])
        anomaly = sub[(sub.feature_set == "relative_normalized") & (sub.kind == "lr")
                      & (sub.source == "Dream-org/Dream-v0-Instruct-7B")
                      & (sub.target == "GSAI-ML/LLaDA-8B-Instruct")]
        if len(anomaly):
            r = anomaly.iloc[0]
            strat = tm[(tm.axis == "model") & (tm.feature_set == "relative_normalized")
                       & (tm.kind == "lr") & (tm.source == r.source) & (tm.target == r.target)
                       & (tm.dataset != "all")]
            parts = "；".join(f"{x.dataset} n={int(x.n)} AUROC {x.auroc:.3f}" for x in strat.itertuples())
            w(f"- 已知异常格 `relative_normalized+LR` Dream→LLaDA: AUROC {r.auroc:.3f} "
              f"[{r.auroc_low:.2f},{r.auroc_high:.2f}]；分层：{parts}（小样本层驱动，见 initial_observations）")
        w()

    # ---------------------------------------------------------------- 2 multiseed
    ms = load_json(REPO / "reports/main_project_multiseed.json")
    if ms is None:
        warn.append("reports/main_project_multiseed.json 缺失")
    else:
        w(f"## 2. 多种子稳健性（{len(ms.get('seeds', []))} seeds，bootstrap {ms.get('bootstrap')}）")
        w()
        cells = [c for c in ms["cells"] if c.get("dataset") == "all"]
        rows = []
        for src in ("GSAI-ML/LLaDA-8B-Instruct", "Dream-org/Dream-v0-Instruct-7B"):
            for dst in ("GSAI-ML/LLaDA-8B-Instruct", "Dream-org/Dream-v0-Instruct-7B"):
                label = f"{short(src)} → {short(dst)}"
                vals = []
                for fs, kind in (("relative_normalized", "lr"), ("entropy_raw", "lr"),
                                 ("relative_normalized", "mlp"), ("entropy_raw", "mlp")):
                    hit = [c for c in cells if c["source"] == src and c["target"] == dst
                           and c["feature_set"] == fs and c["kind"] == kind]
                    if hit:
                        c = hit[0]
                        vals.append(f"{c['auroc_mean']:.3f} (σ {c['auroc_std']:.3f})")
                    else:
                        vals.append("-")
                rows.append([label, *vals])
        table(rows, ["方向", "rel+LR", "ent+LR", "rel+MLP", "ent+MLP"])
        w("每一格为 5 个种子的 AUROC 均值（σ 为种子间标准差）。")
        w()

    # ---------------------------------------------------------------- 3 importance
    im = load_json(REPO / "reports/main_project_importance.json")
    if im is None:
        warn.append("reports/main_project_importance.json 缺失")
    else:
        w(f"## 3. 特征重要性（{im.get('kind', '?').upper()}，置换 {im.get('permutations')} 次，dataset=all）")
        w()
        rows = []
        for c in im["cells"]:
            perm = c.get("permutation", {})
            top_perm = sorted(perm.items(), key=lambda kv: -kv[1]["mean_drop"])[:2]
            loo = c.get("leave_one_out", {})
            top_loo = sorted(loo.items(), key=lambda kv: kv[1].get("delta", 0))[:1]
            rows.append([
                f"{short(c['source'])} → {short(c['target'])} {c['feature_set']}",
                f"{c['base']['auroc']:.3f}",
                "；".join(f"{k} ({v['mean_drop']:+.3f})" for k, v in top_perm),
                "；".join(f"{k} ({-v.get('delta', 0):+.3f})" for k, v in top_loo),
            ])
        table(rows, ["格", "base AUROC", "置换 top-2（正=重要）", "LOO top-1"])
        w()

    # ---------------------------------------------------------------- 4 stability
    st = load_json(REPO / "reports/main_project_stability.json")
    if st is None:
        warn.append("reports/main_project_stability.json 缺失")
    else:
        w(f"## 4. 稳定性重采样（{st.get('repeats')} repeats，簇级重采样）")
        w()
        if st.get("stopped_early"):
            warn.append(f"稳定性提前停止（max_seconds={st.get('max_seconds')}），"
                        f"missing_combos={st.get('missing_combos')}")
        partial = [c for c in st["cells"] if c.get("partial")]
        rows = []
        for c in sorted(st["cells"], key=lambda c: (c["feature_set"], c["kind"], c["source"], c["target"])):
            flag = "（partial）" if c.get("partial") else ""
            rows.append([
                f"{short(c['source'])} → {short(c['target'])} {c['feature_set']} {c['kind'].upper()}{flag}",
                f"{c['auroc_mean']:.3f} (σ {c['auroc_std']:.3f})",
                f"{c['auroc_p05']:.3f}–{c['auroc_p95']:.3f}",
                f"{c['p_above_0_5']:.2f}/{c['p_above_0_7']:.2f}/{c['p_above_0_8']:.2f}",
                f"{c['repeats_valid']}/{c['repeats_requested']}",
            ])
        table(rows, ["格", "AUROC 均值（σ）", "5–95% 分位", "P(>0.5/>0.7/>0.8)", "有效/请求"])
        key = [c for c in st["cells"] if c["feature_set"] == "relative_normalized"
               and c["kind"] == "lr" and short(c["source"]) == "Dream" and short(c["target"]) == "LLaDA"]
        if key:
            c = key[0]
            w(f"- **异常格 `relative_normalized+LR` Dream→LLaDA 在重采样下**：均值 {c['auroc_mean']:.3f}，"
              f"P(>0.5)={c['p_above_0_5']:.2f}（即 P(≤0.5)={1 - c['p_above_0_5']:.2f}），"
              f"5–95% 分位 {c['auroc_p05']:.3f}–{c['auroc_p95']:.3f}"
              + ("（partial）" if c.get("partial") else ""))
        w("分位是重采样离散度，不是总体置信区间；阈值未在稳定性循环中重新调优。")
        w()

    # ---------------------------------------------------------------- 5 TRE
    tre = load_json(REPO / "reports/tre_repro/offline_analysis.json")
    if tre is None:
        warn.append("reports/tre_repro/offline_analysis.json 缺失")
    else:
        w(f"## 5. TRE R1（judge 800 题：{tre.get('positive')} 正 / {tre.get('negative')} 负）")
        w()
        fams = tre.get("score_families", {})
        top = sorted(((k, v) for k, v in fams.items() if v.get("auroc") is not None),
                     key=lambda kv: -kv[1]["auroc"])[:5]
        rows = []
        for k, v in top:
            rng = ""
            if v.get("auroc_low") is not None:
                rng = f" [{v['auroc_low']:.3f},{v['auroc_high']:.3f}]"
            rows.append([k, f"{v['auroc']:.4f}{rng}"])
        table(rows, ["分数族（Top5）", "AUROC（95% CI）"])
        w(f"- 主口径 `{tre.get('main_metric')}`: AUROC {fams.get(tre.get('main_metric'), {}).get('auroc', float('nan')):.4f}")
        perm = load_json(REPO / "reports/tre_repro/permutation_test.json")
        if perm:
            perm_rows = []
            for k, v in perm["results"].items():
                perm_rows.append([f"置换检验 {k}",
                                  f"p={v['p_value_one_sided']:.2e}（null mean {v['null_mean']:.3f}）"])
            table(perm_rows, ["置换检验", "结果"])
        w()

    # ---------------------------------------------------------------- 6 DynHD
    dy = load_json(REPO / "reports/dynhd_reproduction_summary.json")
    if dy is None:
        warn.append("reports/dynhd_reproduction_summary.json 缺失")
    else:
        w("## 6. DynHD 复现交付")
        w()
        a = dy.get("cpu_acceptance_assertions", {})
        ev = dy.get("evaluation", {})
        common = dy.get("common_test_set", {})
        w(f"- CPU 验收断言: {a.get('passed')}/{a.get('total')}")
        def _mean(x):
            return x.get("mean") if isinstance(x, dict) else x
        if "llada" in ev:
            v = ev["llada"].get("aggregate", {}).get("test_auroc_fixed")
            w(f"- LLaDA test AUROC（3 seeds 均值）: {_mean(v):.4f}" if v else "- LLaDA test AUROC: n/a")
        if "dream" in ev:
            v = ev["dream"].get("aggregate", {}).get("test_auroc_fixed")
            w(f"- Dream test AUROC（3 seeds 均值）: {_mean(v):.4f}" if v else "- Dream test AUROC: n/a")
        if common:
            import statistics as _s
            w(f"- 共同测试集 n={common.get('common_n')}: LLaDA {_s.mean(common['llada_common_test_auroc']):.4f} / "
              f"Dream {_s.mean(common['dream_common_test_auroc']):.4f}")
        w(f"- 记录的偏差 {len(dy.get('deviations', []))} 条，限制 {len(dy.get('limits', []))} 条（见 "
          f"reports/dynhd_reproduction_summary.md）")
        w()

    # ---------------------------------------------------------------- 7 caveats
    w("## 7. 注意事项")
    w()
    w("- 单次矩阵不能用于检测器优劣结论；稳定性分位仅为重采样离散度。")
    w("- test 层每方向仅 18–48 条，跨模型多数格 CI 覆盖 0.5；结论以「是否出现稳定迁移缺口」为准。")
    w("- `data/labels/*.reviewed.jsonl` 为 gitignore 文件，只存在于工作区与夜间备份包。")
    for x in warn:
        w(f"- ⚠️ {x}")
    w()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    for line in lines:
        print(line)
    print(f"\nwrote {out_path}")
    if warn:
        print("WARNINGS:", *warn, sep="\n  ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
