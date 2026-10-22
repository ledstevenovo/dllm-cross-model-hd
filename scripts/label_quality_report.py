#!/usr/bin/env python
"""Consolidate the second-judge label-quality evidence into one page.

Reads the two consistency runs (main-project reviewed labels and DynHD rule labels), recomputes
per-model agreement and label marginals from their judged rows, and writes
reports/label_quality_evidence.md. Read-only with respect to the labels: this document is
supplementary evidence, the labels themselves stay the reviewed rule sign-off.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def load_rows(path: Path) -> list[dict]:
    try:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except Exception:  # noqa: BLE001
        return []


def kappa(rows: list[dict]):
    rows = [r for r in rows if r.get("judge_label") is not None]
    if not rows:
        return None
    n = len(rows)
    po = sum(1 for r in rows if r["agree"]) / n
    p_rule = sum(1 for r in rows if r["rule_label"] == 1) / n
    p_judge = sum(1 for r in rows if r["judge_label"] == 1) / n
    pe = p_rule * p_judge + (1 - p_rule) * (1 - p_judge)
    return (po - pe) / (1 - pe) if pe < 1 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dynhd", default=str(REPO / "reports/dynhd_label_consistency.json"))
    parser.add_argument("--main", dest="main_report",
                        default=str(REPO / "reports/main_label_consistency.json"))
    parser.add_argument("--out", default=str(REPO / "reports/label_quality_evidence.md"))
    args = parser.parse_args()

    sets = [("主项目（迁移矩阵/稳定性所用 reviewed 标签）",
             Path(args.main_report), Path(args.main_report).with_name(Path(args.main_report).stem + ".rows.jsonl")),
            ("DynHD 复现（规则标签）",
             Path(args.dynhd), Path(args.dynhd).with_name(Path(args.dynhd).stem + ".rows.jsonl"))]
    lines = ["# 标签质量证据：第二 judge 一致性（2026-10-22）", ""]
    summary = []
    for title, report_path, rows_path in sets:
        report, rows = load_json(report_path), load_rows(rows_path)
        if not report or not rows:
            lines += [f"## {title}", "", f"- ⚠️ 尚未完成或缺少数据：`{report_path.name}`", ""]
            continue
        resolved = [r for r in rows if r.get("judge_label") is not None]
        overall = sum(1 for r in resolved if r["agree"]) / len(resolved) if resolved else None
        k = kappa(rows)
        lines += [f"## {title}", "",
                  f"- judge：`{report.get('judge_model')}`，冻结提示词 `judge_prompt_v3` "
                  f"（sha256 {str(report.get('judge_prompt_sha256'))[:12]}…），温度 0",
                  f"- 抽样：{report.get('samples_requested')} 条，完成 {report.get('samples_resolved')} 条"
                  f"（seed {report.get('plan', {}).get('seed', report.get('seed', '?'))}）",
                  f"- **总体一致率 {overall:.3f}**，**Cohen's κ = "
                  f"{('%.3f' % k) if k is not None else 'n/a'}**", ""]
        lines += ["| 模型 | n | 一致率 | 规则标签 incorrect 占比 | judge incorrect 占比 |", "|---|---|---|---|---|"]
        for model in sorted({r["model"] for r in resolved}):
            sub = [r for r in resolved if r["model"] == model]
            lines.append(f"| {model} | {len(sub)} | "
                         f"{sum(1 for r in sub if r['agree']) / len(sub):.3f} | "
                         f"{sum(1 for r in sub if r['rule_label'] == 1) / len(sub):.2f} | "
                         f"{sum(1 for r in sub if r['judge_label'] == 1) / len(sub):.2f} |")
        lines += ["", f"- 不一致 {sum(1 for r in resolved if not r['agree'])} 条；明细见 "
                      f"`{report_path.name}`（disagreements 字段）与 `{rows_path.name}`，"
                      f"并已全部进入人工抽查表（`reports/label_spotcheck_sheet.md/.csv`）。", ""]
        dis_rows = [r for r in resolved if not r["agree"]][:5]
        if dis_rows:
            lines += ["### 分歧示例（最多 5 条，完整清单见 `label_spotcheck_sheet.md`）", "",
                      "| 模型 | 问题（截断） | 规则 | judge | judge 理由（截断） |", "|---|---|---|---|---|"]
            for r in dis_rows:
                q = " ".join(r["question"].split())[:90]
                reason = " ".join((r.get("judge_reason") or "").split())[:140]
                lines.append(f"| {r['model']} | {q} | {'incorrect' if r['rule_label'] else 'correct'} | "
                             f"{'incorrect' if r['judge_label'] else 'correct'} | {reason} |")
            lines.append("")
        summary.append((title, len(resolved), overall, k))

    lines += ["## 说明", "",
              "- 本证据是**补充**：正式指标仍使用 reviewed 规则签核标签，第二 judge 不改任何标签；",
              "- 两套判分使用同一冻结提示词与同一 judge 模型/端点，可与 TRE R1 的 judge 口径直接对照；",
              "- 人工抽查表按“全部不一致 + 一致中补齐至 ≥50 条”生成，供人工独立复核后填写判定。", ""]
    out = Path(args.out)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
