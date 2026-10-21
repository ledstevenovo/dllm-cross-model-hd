#!/usr/bin/env python
"""Draft pre-review for DynHD pilot200 answers (step-5 preparation).

Produces, per model: a review sheet, a draft labels file (human_reviewed=false) and a
count summary. Rules and flags follow the main project's smoke/pilot convention so the
same sign-off wording can be reused. This script never marks anything as human-reviewed.

  correct  -> label 0, include
  incorrect-> label 1, include
  refusals/echo/format failures -> exclude (abstain classes, kept out of the main metric)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO / "references/repos/DynHD"))
import common  # noqa: E402
import torch  # noqa: E402

PUNCT = str.maketrans({c: " " for c in ".,;:!?\"'()[]{}<>“”‘’、"})
FUNCTION_WORDS = {
    "the", "a", "an", "of", "to", "in", "on", "at", "for", "and", "or", "but", "is", "are",
    "was", "were", "be", "been", "am", "my", "your", "his", "her", "its", "our", "their",
    "this", "that", "these", "those", "with", "from", "by", "as", "if", "then", "than", "so",
    "such", "it", "he", "she", "they", "we", "you", "i", "do", "did", "does", "not", "sir",
    "off", "out", "up", "down", "over", "under", "into", "about", "after", "before",
}


def tokens(text) -> list[str]:
    return str(text).translate(PUNCT).lower().split()


def contains(hay: list[str], needle: list[str]) -> bool:
    n = len(needle)
    if n == 0 or n > len(hay):
        return False
    return any(hay[i:i + n] == needle for i in range(len(hay) - n + 1))


def propose(gold, aliases, prediction, question, model) -> tuple[str, str, str | None, list[str]]:
    """Return (decision, label_or_none, reason, flags)."""
    p, g, q = tokens(prediction), tokens(gold), tokens(question)
    alias_list = [tokens(a) for a in (aliases or []) if str(a).strip()]
    flags: list[str] = []
    if not p:
        return "exclude", None, "空输出（refusal_empty）", flags
    if p == g or contains(p, g) or (len(p) >= 2 and contains(g, p)):
        return "include", "0", "gold 命中（含等价/包含）", flags
    for alias in alias_list:
        if alias and (contains(p, alias) or (len(p) >= 2 and contains(alias, p))):
            return "include", "0", "gold 别名命中", flags
    if len(p) >= 3 and (contains(q, p) or (contains(p, q) and len(q) >= 3)):
        return "exclude", None, "输出为问句回显（format_failure）", flags
    if len(p) == 1:
        if p[0] in FUNCTION_WORDS or len(p[0]) <= 2:
            return "exclude", None, f"单 token 函数词/碎片 {prediction!r}（无答案内容）", flags
        return "include", "1", f"单 token 短答 {prediction!r}（疑似错答）", ["short-answer"]
    if len(p) == 2 and all(t in FUNCTION_WORDS for t in p):
        return "exclude", None, f"两 token 均为函数词 {prediction!r}", flags
    if model == "dream" and len(p) <= 2:
        flags.append("short-answer")
    return "include", "1", "gold 未命中（错答）", flags


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["llada", "dream"], required=True)
    parser.add_argument("--data-dir", required=True, help="merged or raw run directory")
    parser.add_argument("--subset", default=str(REPO / "data/raw_qa/subsets/pilot200.jsonl"))
    parser.add_argument("--out-sheet", required=True)
    parser.add_argument("--out-labels", required=True)
    parser.add_argument("--reviewer-note", default="assistant:pre-review:2026-10-22")
    args = parser.parse_args()

    rows = [json.loads(line) for line in Path(args.subset).read_text(encoding="utf-8").splitlines() if line.strip()]
    index = {row["sample_id"]: (position, row) for position, row in enumerate(rows)}
    data_dir = Path(args.data_dir)
    traces = []
    for path in sorted(data_dir.glob("*.pt")):
        data = torch.load(path, map_location="cpu", weights_only=True)
        meta = data["meta"]
        sample_id = str(meta.get("id"))
        if sample_id not in index:
            raise SystemExit(f"{path.name}: sample_id {sample_id} not in the subset")
        position, row = index[sample_id]
        decision, label, reason, flags = propose(row["gold_answer"], row.get("gold_aliases"),
                                                 meta.get("generated_text", ""), row["question"], args.model)
        traces.append({
            "pilot_index": position, "split": row.get("split"), "sample_id": sample_id,
            "question_id": row["question_id"], "question": row["question"], "gold": row["gold_answer"],
            "prediction": str(meta.get("generated_text", "")),
            "answer_sha256": meta.get("answer_sha256"), "decision": decision, "label": label,
            "reason": reason, "flags": flags,
            "provisional_label": int(data.get("label", -1)),
        })

    counts = {}
    for row in traces:
        key = "exclude" if row["decision"] == "exclude" else f"include-{row['label']}"
        counts[key] = counts.get(key, 0) + 1
    flagged = [row for row in traces if row["flags"]]

    sheet = [f"# DynHD pilot200 预复核草表（{args.model}，{len(traces)} 条，未人工签核）", "",
             "决策口径（事前固定）：correct→include/0；incorrect→include/1；空答、问句回显、函数词碎片→exclude（abstain，不进主指标）。",
             f"统计：{json.dumps(counts, ensure_ascii=False)}；需人工拍板的短答 {len(flagged)} 条。", "",
             "| # | split | question | gold | prediction | 提案 | 说明 |", "|---|---|---|---|---|---|---|"]
    for row in traces:
        mark = " ⚠" if row["flags"] else ""
        sheet.append(f"| {row['pilot_index']} | {row['split']} | {row['question'][:44]} | {str(row['gold'])[:20]} | "
                     f"{row['prediction'][:44]!r} | {row['decision']}/{row['label']}{mark} | {row['reason'][:40]} |")
    if flagged:
        sheet += ["", "## 需人工拍板的短答（建议逐条确认 include=1 还是 exclude）", ""]
        for row in flagged:
            sheet.append(f"- #{row['pilot_index']} [{row['split']}] {row['question'][:50]} | gold={row['gold']!r} | pred={row['prediction']!r}")
    Path(args.out_sheet).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_sheet).write_text("\n".join(sheet) + "\n")

    labels = [{
        "sample_id": row["sample_id"], "question_id": row["question_id"],
        "decision": row["decision"], "label": row["label"],
        "human_reviewed": False, "label_source": args.reviewer_note,
        "generated_text_sha256": row["answer_sha256"],
        "exclude_reason": row["reason"] if row["decision"] == "exclude" else None,
        "notes": row["reason"], "flags": row["flags"], "pilot_index": row["pilot_index"],
    } for row in traces]
    Path(args.out_labels).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_labels).write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in labels) + "\n")
    print(json.dumps({"model": args.model, "traces": len(traces), "counts": counts,
                      "flagged_short_answers": len(flagged),
                      "sheet": args.out_sheet, "labels_draft": args.out_labels}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
