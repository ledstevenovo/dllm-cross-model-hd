#!/usr/bin/env python
"""Build the human spot-check sheet for the DynHD label-quality evidence.

Reads the judged rows from the second-judge run (reports/dynhd_label_consistency.rows.jsonl) and
writes

  reports/label_spotcheck_sheet.md   readable sheet, all disagreements first
  reports/label_spotcheck_sheet.csv  same rows with empty your_verdict / your_notes columns

Review focus: every disagreement plus a deterministic fill of agreements until at least
--min-review items are marked, so the human review covers >= 50 questions by construction.
The sheet never edits the labels; it is evidence about them.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]

VERDICT_CHOICES = "agree | rule_ok_judge_wrong | judge_ok_rule_wrong | unsure"


def load_rows(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def load_references(subset: Path) -> dict[str, list[str]]:
    refs = {}
    for line in subset.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        refs[str(row["sample_id"])] = [row.get("gold_answer"), *(row.get("gold_aliases") or [])]
    return refs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", nargs="+",
                        default=[str(REPO / "reports/dynhd_label_consistency.rows.jsonl"),
                                 str(REPO / "reports/main_label_consistency.rows.jsonl")],
                        help="one or more judged-rows jsonl files (merged, deduplicated; "
                             "the source tag comes from the file-name prefix)")
    parser.add_argument("--subset", default=str(REPO / "data/raw_qa/subsets/pilot200.jsonl"))
    parser.add_argument("--min-review", type=int, default=50)
    parser.add_argument("--out-md", default=str(REPO / "reports/label_spotcheck_sheet.md"))
    parser.add_argument("--out-csv", default=str(REPO / "reports/label_spotcheck_sheet.csv"))
    args = parser.parse_args()

    rows, seen = [], set()
    for path in args.rows:
        tag = Path(path).stem.split("_")[0]
        for row in load_rows(Path(path)):
            row = dict(row)
            row["source"] = tag
            key = (tag, row["model"], row["sample_id"])
            if key in seen:
                continue
            seen.add(key)
            rows.append(row)
    refs = load_references(Path(args.subset))
    disagreements = [r for r in rows if not r["agree"]]
    by_source: dict[str, list[dict]] = {}
    for row in sorted((r for r in rows if r["agree"]), key=lambda r: (r["source"], r["model"], r["sample_id"])):
        by_source.setdefault(row["source"], []).append(row)
    needed = max(0, args.min_review - len(disagreements))
    sampled, index = [], 0
    while len(sampled) < needed:
        progressed = False
        for source in sorted(by_source):
            if len(sampled) >= needed:
                break
            if index < len(by_source[source]):
                sampled.append(by_source[source][index])
                progressed = True
        if not progressed:
            break
        index += 1
    dis_keys = {(r["source"], r["model"], r["sample_id"]) for r in disagreements}
    priority_keys = dis_keys | {(r["source"], r["model"], r["sample_id"]) for r in sampled}

    for row in rows:
        key = (row["source"], row["model"], row["sample_id"])
        row["review_priority"] = "disagreement" if key in dis_keys \
            else ("sample" if key in priority_keys else "")
        row["references"] = [x for x in refs.get(row["sample_id"].split("__seed")[0], []) if x]

    order = sorted(rows, key=lambda r: (r["review_priority"] != "disagreement",
                                        r["review_priority"] == "", r["source"], r["model"], r["sample_id"]))
    total = len(rows)
    per_set = {s: sum(1 for r in rows if r["source"] == s) for s in sorted({r["source"] for r in rows})}
    lines = [
        "# 标签人工抽查表（第二 judge 对照，主项目 + DynHD）",
        "",
        f"- 两套被判分条目共 {total}（{', '.join(f'{s} {n}' for s, n in per_set.items())}），"
        f"其中不一致 {len(disagreements)} 条；`review_priority` 标记：不一致全部 + 一致中抽 {len(sampled)} 条 "
        f"= {len(priority_keys)} 条建议人工复核（不少于 {args.min_review} 条）。",
        "- `source` 列：`main` = 主项目 reviewed 标签（迁移矩阵/稳定性所用）；`dynhd` = DynHD 复现规则标签。",
        "- 每行给出：规则标签（主表所用）vs 第二 judge 标签、判定理由。请只看题面与参考答案，独立判断后填 CSV 的 "
        f"`your_verdict`（{VERDICT_CHOICES}）与 `your_notes`。",
        "- 本表不改主标签，只作为标签质量证据留存。",
        "",
    ]
    for index, row in enumerate(order, 1):
        mark = "⚠️ 不一致" if not row["agree"] else "一致"
        reason = (row.get("judge_reason") or "").replace("\n", " ").strip()
        lines += [
            f"## {index}. [{row['review_priority'] or '-'}] {row['source']}/{row['model']} · {row['sample_id']} · {mark}",
            "",
            f"- **问题**：{row['question'].strip()}",
            f"- **参考答案**：{'；'.join(str(x) for x in row['references']) or '（无）'}",
            f"- **模型回答**：{row['answer'].strip() or '（空）'}",
            f"- **规则标签**：{'incorrect(1)' if row['rule_label'] == 1 else 'correct(0)'}"
            f" ｜ **judge 标签**：{'incorrect(1)' if row['judge_label'] == 1 else 'correct(0)'}",
            f"- **judge 理由**：{reason or '（无）'}",
            "",
        ]
    Path(args.out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")

    header = ["review_priority", "source", "model", "sample_id", "question",
              "reference_answers", "answer", "rule_label", "judge_label", "agree",
              "judge_reason", "your_verdict", "your_notes"]

    def csv_row(row):
        return [row["review_priority"], row["source"], row["model"], row["sample_id"],
                row["question"].strip(), " | ".join(str(x) for x in row["references"]),
                row["answer"].strip(), row["rule_label"], row["judge_label"],
                row["agree"], (row.get("judge_reason") or "").strip(), "", ""]

    with Path(args.out_csv).open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for row in order:
            writer.writerow(csv_row(row))
    review_out = Path(args.out_csv).with_name(Path(args.out_csv).stem + "_review50.csv")
    with review_out.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for row in order:
            if row["review_priority"]:
                writer.writerow(csv_row(row))
    print(json.dumps({"rows": total, "disagreements": len(disagreements),
                      "sampled_agreements": len(sampled), "review_priority": len(priority_keys),
                      "md": args.out_md, "csv": args.out_csv, "review_csv": str(review_out)},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
