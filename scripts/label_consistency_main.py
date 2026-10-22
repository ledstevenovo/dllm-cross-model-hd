#!/usr/bin/env python
"""Independent second-judge consistency check for the MAIN-project labels.

The transfer matrix and the stability study are built on the reviewed pilot200 labels
(correct/incorrect after the rule sign-off). This script samples a fixed set per model, asks an
independent judge the same frozen question/answer/reference prompt used for TRE (J2 prompt v3),
and reports agreement and Cohen's kappa against the reviewed labels. It never edits the labels.

Reads:  data/trajectories/bf16_pilot200/<model>/generations.jsonl   (answers)
        data/labels/pilot200_<model>.reviewed.jsonl                 (reviewed labels)
        data/raw_qa/subsets/pilot200.jsonl                          (questions, references)
Writes: reports/main_label_consistency.json (+ .rows.jsonl for the spot-check sheet)

Without the API key env var it prints the plan and writes nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent
PROMPT = REPO / "data/tre_repro/judge_prompt_v3.txt"
PROMPT_SHA256 = "2d125bea4f6a5d5a5f97cbb48666c1c872f093d9356a00b09283dc88e5bd46cd"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset", default=str(REPO / "data/raw_qa/subsets/pilot200.jsonl"))
    parser.add_argument("--trajectories", default=str(REPO / "data/trajectories/bf16_pilot200"))
    parser.add_argument("--labels", default=str(REPO / "data/labels"))
    parser.add_argument("--samples-per-model", type=int, default=50)
    parser.add_argument("--seed", type=int, default=20261021)
    parser.add_argument("--out", default=str(REPO / "reports/main_label_consistency.json"))
    parser.add_argument("--endpoint", required=True, help="chat/completions URL or base URL")
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key-env", default="MOMA_API_KEY")
    parser.add_argument("--checkpoint", default=None)
    args = parser.parse_args()
    endpoint = args.endpoint if args.endpoint.endswith("/chat/completions") \
        else args.endpoint.rstrip("/") + "/chat/completions"

    prompt_text = PROMPT.read_text(encoding="utf-8")
    if hashlib.sha256(prompt_text.encode()).hexdigest() != PROMPT_SHA256:
        raise SystemExit("frozen judge prompt hash mismatch")

    questions = {str(json.loads(line)["question_id"]): json.loads(line)
                 for line in Path(args.subset).read_text(encoding="utf-8").splitlines() if line.strip()}
    plan, sampled = {"models": {}, "seed": args.seed, "samples_per_model": args.samples_per_model}, []
    rng = random.Random(args.seed)
    for model in ("llada", "dream"):
        answers = {}
        for line in (Path(args.trajectories) / model / "generations.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                answers[str(record["sample_id"])] = record.get("generated_text", "")
        labels = {}
        for line in (Path(args.labels) / f"pilot200_{model}.reviewed.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                labels[str(record["sample_id"])] = record
        eligible = sorted(sid for sid, rec in labels.items()
                          if rec.get("human_reviewed") and rec.get("label") in ("correct", "incorrect")
                          and sid in answers and str(rec.get("question_id")) in questions)
        rng.shuffle(eligible)
        chosen = eligible[: args.samples_per_model]
        plan["models"][model] = {"eligible": len(eligible), "chosen": len(chosen),
                                 "reviewed_label_counts": {
                                     k: sum(1 for sid in chosen if labels[sid]["label"] == k)
                                     for k in ("correct", "incorrect")}}
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

    def judge(row):
        payload = json.dumps({"question": row["question"], "reference_answers": row["references"],
                              "proposed_answer": row["answer"]}, ensure_ascii=False)
        body = json.dumps({"model": args.model, "temperature": 0, "max_tokens": 2048,
                           "response_format": {"type": "json_object"},
                           "messages": [{"role": "system", "content": prompt_text},
                                        {"role": "user", "content": payload}]}).encode()
        request = urllib.request.Request(endpoint, data=body, method="POST",
                                         headers={"Content-Type": "application/json",
                                                  "Authorization": f"Bearer {api_key}"})
        last_error = None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(request, timeout=180) as response:
                    content = json.loads(response.read())["choices"][0]["message"]["content"]
                verdict_obj = json.loads(content)
                verdict = str(verdict_obj["verdict"]).lower()
                return 0 if verdict == "correct" else 1, verdict, str(verdict_obj.get("reason", ""))[:400]
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                import time
                time.sleep(2 ** (attempt + 1))
        print(f"  unresolved ({type(last_error).__name__}: {last_error})", flush=True)
        return None, "unresolved", ""

    ckpt_path = Path(args.checkpoint) if args.checkpoint else Path(str(args.out) + ".partial.jsonl")
    judged = {}
    if ckpt_path.exists():
        for line in ckpt_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                judged[(rec["model"], rec["sample_id"])] = rec
        print(f"resume: {len(judged)} items already judged in {ckpt_path}", flush=True)

    rows = []
    for index, row in enumerate(sampled, 1):
        key = (row["model"], row["sample_id"])
        if key in judged:
            rows.append(judged[key])
            continue
        label, verdict, reason = judge(row)
        entry = {**{k: row[k] for k in ("model", "sample_id", "rule_label", "answer", "question")},
                 "judge_label": label, "judge_verdict": verdict, "judge_reason": reason,
                 "agree": (label is not None and label == row["rule_label"])}
        rows.append(entry)
        judged[key] = entry
        with ckpt_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        if index % 10 == 0 or index == len(sampled):
            print(f"  judged {index}/{len(sampled)}", flush=True)

    resolved = [row for row in rows if row["judge_label"] is not None]
    agreement = sum(1 for row in resolved if row["agree"]) / len(resolved) if resolved else None
    kappa = None
    if resolved:
        n = len(resolved)
        po = sum(1 for row in resolved if row["agree"]) / n
        p_rule = sum(1 for row in resolved if row["rule_label"] == 1) / n
        p_judge = sum(1 for row in resolved if row["judge_label"] == 1) / n
        pe = p_rule * p_judge + (1 - p_rule) * (1 - p_judge)
        kappa = (po - pe) / (1 - pe) if pe < 1 else None
    per_model = {}
    for model in ("llada", "dream"):
        sub = [r for r in resolved if r["model"] == model]
        if sub:
            per_model[model] = {"n": len(sub),
                                "agreement": sum(1 for r in sub if r["agree"]) / len(sub),
                                "rule_incorrect": sum(1 for r in sub if r["rule_label"] == 1) / len(sub),
                                "judge_incorrect": sum(1 for r in sub if r["judge_label"] == 1) / len(sub)}
    payload = {"date": "2026-10-22", "scope": "main project reviewed pilot200 labels",
               "judge_model": args.model, "judge_endpoint": endpoint,
               "judge_prompt_sha256": PROMPT_SHA256, "plan": plan,
               "samples_requested": len(sampled), "samples_resolved": len(resolved),
               "agreement": agreement, "cohens_kappa": kappa, "per_model": per_model,
               "disagreements": [r for r in resolved if not r["agree"]][:25],
               "note": "supplementary label-quality evidence; the main labels stay the reviewed rule sign-off"}
    out = Path(args.out)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    rows_out = out.with_name(out.stem + ".rows.jsonl")
    rows_out.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    if all(row["judge_label"] is not None for row in rows) and ckpt_path.exists():
        ckpt_path.unlink()
    print(json.dumps({k: payload[k] for k in ("samples_requested", "samples_resolved",
                                              "agreement", "cohens_kappa", "per_model")},
                     indent=2, ensure_ascii=False))
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
