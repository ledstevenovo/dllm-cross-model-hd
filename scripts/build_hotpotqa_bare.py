#!/usr/bin/env python
"""Build a bare-question HotpotQA list: same 800 questions, context removed.

Purpose: test whether R2's HotpotQA shortfall comes from the context-grounded prompt rather
than from HotpotQA itself. The paper does not disclose whether its HotpotQA prompt includes
distractor paragraphs; the main project's prompt does not. Parsing the same 800 questions
without context lets the two be compared directly.

Frozen decisions:
  * identical question_ids and sample seeds, so the pairing with R2 is exact;
  * prompt style "v3-bare-question", i.e. literally the question and nothing else, matching
    both R1 and the main project's convention (the main project adds a short-answer
    instruction; this one stays bare so the only change from R2 is the removal of context);
  * written to a NEW file -- the R2 list is frozen and is never rewritten.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tre_repro import TRE_PROMPT_VERSION, bare_prompt, build_record, load_questions  # noqa: E402

SRC = ROOT / "data/tre_repro/questions/hotpotqa_eval800.jsonl"
OUT = ROOT / "data/tre_repro/questions/hotpotqa_bare800.jsonl"
MANIFEST = ROOT / "data/tre_repro/questions_manifest_hotpotqa_bare.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    records = load_questions(SRC)
    rows, pools = [], []
    for record in records:
        provenance = dict(record.provenance)
        provenance["derived_from"] = SRC.relative_to(ROOT).as_posix()
        provenance["derived_from_sha256"] = sha256(SRC)
        provenance["context"] = "removed for the bare-question control"
        provenance["prompt_style"] = TRE_PROMPT_VERSION
        row = build_record(
            {
                "question_id": record.question_id,
                "cluster_id": record.cluster_id,
                "dataset": record.dataset,
                "question": record.question,
                "gold_answer": record.gold_answer,
                "gold_aliases": record.gold_aliases,
                "gold_normalized_aliases": record.gold_normalized_aliases,
                "answer_type": record.answer_type,
                "answer_source_field": record.answer_source_field,
                "source": record.source,
            },
            split="test",
            provenance=provenance,
            context="",
        ).to_dict()
        rows.append(row)
        pools.append((row["question_id"], record.context))

    serialized = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    digest = hashlib.sha256(serialized.encode()).hexdigest()
    OUT.write_bytes(serialized.encode("utf-8"))

    manifest = {
        "manifest_version": "tre-hotpotqa-bare-v1",
        "purpose": ("control for R2: identical 800 HotpotQA questions with the distractor "
                    "context removed, to isolate the prompt as the source of R2's shortfall"),
        "derived_from": SRC.relative_to(ROOT).as_posix(),
        "derived_from_sha256": sha256(SRC),
        "questions": len(rows),
        "prompt_style": TRE_PROMPT_VERSION,
        "file": OUT.relative_to(ROOT).as_posix(),
        "file_sha256": digest,
        "context_removed": sum(1 for _, context in pools if context),
        "note": ("judge will see the same gold answers; expected positive rate is ~81% because "
                 "multi-hop questions are often unanswerable without context, so AUROC is not "
                 "directly comparable to the context-grounded run"),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} rows, sha256 {digest[:16]})")
    print(f"context removed from {manifest['context_removed']} of {len(rows)} questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
