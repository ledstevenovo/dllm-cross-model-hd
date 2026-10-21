#!/usr/bin/env python
"""Per-model acceptance subset: longest rendered prompt + shortest gold answer.

Selection uses each model's own tokenizer and chat template over the full pilot subset and
does not depend on file order (ties break by id). Output rows keep the frozen subset schema
so the collection wrapper can consume them directly.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import common  # noqa: E402

DEFAULT_MODEL_PATHS = {
    "llada": "/root/autodl-tmp/hf-cache/hub/models--GSAI-ML--LLaDA-8B-Instruct/snapshots/08b83a6feb34df1a6011b80c3c00c7563e963b07",
    "dream": "/root/autodl-tmp/hf-cache/hub/models--Dream-org--Dream-v0-Instruct-7B/snapshots/05334cb9faaf763692dcf9d8737c642be2b2a6ae",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset", required=True)
    parser.add_argument("--model", required=True, choices=["llada", "dream"])
    parser.add_argument("--out", required=True)
    parser.add_argument("--model-path", default=None)
    args = parser.parse_args()

    from transformers import AutoTokenizer

    model_path = args.model_path or DEFAULT_MODEL_PATHS[args.model]
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)
    rows = [json.loads(line) for line in Path(args.subset).read_text(encoding="utf-8").splitlines() if line.strip()]
    if len({row["sample_id"] for row in rows}) != len(rows):
        raise SystemExit("subset contains duplicate sample ids")

    lengths = []
    for row in rows:
        messages = [{"role": "user", "content": row.get("prompt") or row["question"]}]
        rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        ids = tokenizer(rendered).input_ids
        lengths.append({"sample_id": row["sample_id"], "tokens": len(ids), "row": row})
    longest = sorted(lengths, key=lambda entry: (-entry["tokens"], entry["sample_id"]))[0]
    others = [entry for entry in lengths if entry["sample_id"] != longest["sample_id"]]
    shortest = sorted(others, key=lambda entry: (len(str(entry["row"]["gold_answer"]).split()), entry["sample_id"]))[0]

    chosen = [longest, shortest]
    out = []
    for entry in chosen:
        row = dict(entry["row"])
        row["acceptance_role"] = "longest_prompt" if entry is longest else "shortest_gold"
        row["rendered_prompt_tokens"] = entry["tokens"]
        out.append(json.dumps(row, ensure_ascii=False))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(out) + "\n")
    print(f"{args.model}: longest={longest['sample_id']} ({longest['tokens']} tok), "
          f"shortest_gold={shortest['sample_id']} -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
