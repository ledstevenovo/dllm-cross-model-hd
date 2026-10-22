#!/usr/bin/env python
"""Concurrent second-judge consistency check for a label set (pool2000 / pilot200).

Why a second script: ``label_consistency_main.py`` calls the judge serially. On the
measured latency (3.75 s per call for this prompt) full coverage of a 3600-label
run would take ~3.75 h. This script keeps that script's contract -- same frozen
prompt, same request shape, same agreement/kappa arithmetic, same output fields --
but issues calls through a bounded thread pool and checkpoints every result, so an
interrupted run resumes instead of restarting.

It never edits labels. Coverage is reported explicitly: the main table must say
"judged N of M" rather than implying full coverage.

Usage:
  export LONGCAT_API_KEY=...            # or source /root/autodl-tmp/.env.longcat
  .venv/bin/python scripts/judge_consistency_parallel.py \
      --subset data/raw_qa/subsets/pool2000_v1.jsonl \
      --trajectories data/trajectories/bf16_pool2000 \
      --labels data/labels --prefix pool2000 \
      --out reports/pool2000_label_consistency.json \
      --workers 6 --samples-per-model 0        # 0 = every eligible label
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
PROMPT = REPO / "data/tre_repro/judge_prompt_v3.txt"
PROMPT_SHA256 = "2d125bea4f6a5d5a5f97cbb48666c1c872f093d9356a00b09283dc88e5bd46cd"

WRITE_LOCK = threading.Lock()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def cohen_kappa(rows: list[dict]) -> float | None:
    n = len(rows)
    if not n:
        return None
    po = sum(1 for r in rows if r["agree"]) / n
    p_rule = sum(1 for r in rows if r["rule_label"] == 1) / n
    p_judge = sum(1 for r in rows if r["judge_label"] == 1) / n
    pe = p_rule * p_judge + (1 - p_rule) * (1 - p_judge)
    return (po - pe) / (1 - pe) if pe < 1 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset", required=True)
    parser.add_argument("--trajectories", required=True)
    parser.add_argument("--labels", required=True)
    parser.add_argument("--prefix", required=True, help="label file prefix, e.g. pool2000")
    parser.add_argument("--samples-per-model", type=int, default=0, help="0 = all eligible")
    parser.add_argument("--seed", type=int, default=20261021)
    parser.add_argument("--out", required=True)
    parser.add_argument("--endpoint", default="https://api.longcat.chat/openai/v1/chat/completions")
    parser.add_argument("--model", default="LongCat-2.5-Preview")
    parser.add_argument("--api-key-env", default="LONGCAT_API_KEY")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--checkpoint", default=None)
    args = parser.parse_args()

    prompt_text = PROMPT.read_text(encoding="utf-8")
    if hashlib.sha256(prompt_text.encode()).hexdigest() != PROMPT_SHA256:
        raise SystemExit("frozen judge prompt hash mismatch")

    questions = {row["question_id"]: row for row in read_jsonl(Path(args.subset))}
    rng = random.Random(args.seed)
    plan, sampled = {"models": {}, "seed": args.seed,
                     "samples_per_model": args.samples_per_model or "all"}, []

    for model in ("llada", "dream"):
        answers = {row["sample_id"]: row.get("generated_text", "")
                   for row in read_jsonl(Path(args.trajectories) / model / "generations.jsonl")}
        labels = {row["sample_id"]: row for row in
                  read_jsonl(Path(args.labels) / f"{args.prefix}_{model}.reviewed.jsonl")}
        eligible = sorted(sid for sid, rec in labels.items()
                          if rec.get("human_reviewed") and rec.get("label") in ("correct", "incorrect")
                          and sid in answers and str(rec.get("question_id")) in questions)
        rng.shuffle(eligible)
        chosen = eligible if not args.samples_per_model else eligible[:args.samples_per_model]
        plan["models"][model] = {
            "eligible": len(eligible), "chosen": len(chosen),
            "reviewed_label_counts": {k: sum(1 for sid in chosen if labels[sid]["label"] == k)
                                      for k in ("correct", "incorrect")},
        }
        for sid in chosen:
            row = questions[str(labels[sid]["question_id"])]
            sampled.append({"model": model, "sample_id": sid, "question": row["question"],
                            "references": [x for x in [row.get("gold_answer"), *(row.get("gold_aliases") or [])] if x],
                            "answer": answers[sid],
                            "rule_label": 0 if labels[sid]["label"] == "correct" else 1,
                            "label_source": labels[sid].get("label_source", "")})

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        print(json.dumps({"plan": plan, "sampled": len(sampled),
                          "note": f"{args.api_key_env} not set: nothing called, nothing written"},
                         indent=2, ensure_ascii=False))
        return 0

    ckpt_path = Path(args.checkpoint) if args.checkpoint else Path(str(args.out) + ".partial.jsonl")
    judged: dict[tuple[str, str], dict] = {}
    if ckpt_path.exists():
        for record in read_jsonl(ckpt_path):
            judged[(record["model"], record["sample_id"])] = record
        print(f"resume: {len(judged)} already judged", flush=True)

    todo = [row for row in sampled if (row["model"], row["sample_id"]) not in judged]
    print(f"to judge: {len(todo)} / {len(sampled)} with {args.workers} workers", flush=True)

    def judge(row: dict) -> dict:
        payload = json.dumps({"question": row["question"], "reference_answers": row["references"],
                              "proposed_answer": row["answer"]}, ensure_ascii=False)
        body = json.dumps({"model": args.model, "temperature": 0, "max_tokens": 2048,
                           "response_format": {"type": "json_object"},
                           "messages": [{"role": "system", "content": prompt_text},
                                        {"role": "user", "content": payload}]}).encode()
        last_error = None
        for attempt in range(5):
            try:
                request = urllib.request.Request(
                    args.endpoint, data=body, method="POST",
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
                with urllib.request.urlopen(request, timeout=180) as response:
                    content = json.loads(response.read())["choices"][0]["message"]["content"]
                verdict = str(json.loads(content)["verdict"]).lower()
                label = 0 if verdict == "correct" else 1
                return {"model": row["model"], "sample_id": row["sample_id"],
                        "rule_label": row["rule_label"], "answer": row["answer"],
                        "question": row["question"], "judge_label": label,
                        "judge_verdict": verdict,
                        "judge_reason": str(json.loads(content).get("reason", ""))[:400],
                        "agree": label == row["rule_label"]}
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                time.sleep(2 ** (attempt + 1))
        print(f"  unresolved {row['model']}/{row['sample_id']}: {type(last_error).__name__}", flush=True)
        return {"model": row["model"], "sample_id": row["sample_id"],
                "rule_label": row["rule_label"], "answer": row["answer"],
                "question": row["question"], "judge_label": None,
                "judge_verdict": "unresolved", "judge_reason": "", "agree": False}

    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(judge, row): row for row in todo}
        for future in as_completed(futures):
            entry = future.result()
            judged[(entry["model"], entry["sample_id"])] = entry
            with WRITE_LOCK:
                with ckpt_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
            done += 1
            if done % 100 == 0:
                print(f"  judged {done}/{len(todo)}", flush=True)

    rows = [judged[(row["model"], row["sample_id"])] for row in sampled
            if (row["model"], row["sample_id"]) in judged]
    resolved = [row for row in rows if row["judge_label"] is not None]
    agreement = sum(1 for row in resolved if row["agree"]) / len(resolved) if resolved else None
    per_model = {}
    for model in ("llada", "dream"):
        subset = [r for r in resolved if r["model"] == model]
        if subset:
            per_model[model] = {
                "n": len(subset),
                "agreement": sum(1 for r in subset if r["agree"]) / len(subset),
                "rule_incorrect": sum(1 for r in subset if r["rule_label"] == 1) / len(subset),
                "judge_incorrect": sum(1 for r in subset if r["judge_label"] == 1) / len(subset),
            }

    payload = {"date": "2026-10-22", "scope": f"{args.prefix} reviewed labels",
               "judge_model": args.model, "judge_endpoint": args.endpoint,
               "judge_prompt_sha256": PROMPT_SHA256, "plan": plan,
               "samples_requested": len(sampled), "samples_resolved": len(resolved),
               "coverage": round(len(resolved) / len(sampled), 4) if sampled else None,
               "agreement": agreement, "cohens_kappa": cohen_kappa(resolved),
               "per_model": per_model,
               "disagreements": [r for r in resolved if not r["agree"]][:50],
               "note": "supplementary label-quality evidence; labels themselves stay the reviewed sign-off"}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out.with_name(out.stem + ".rows.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    if all(row["judge_label"] is not None for row in rows) and ckpt_path.exists():
        ckpt_path.unlink()
    print(json.dumps({k: payload[k] for k in ("samples_requested", "samples_resolved", "coverage",
                                              "agreement", "cohens_kappa", "per_model")},
                     indent=2, ensure_ascii=False))
    print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
