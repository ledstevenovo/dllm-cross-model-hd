#!/usr/bin/env python
"""Consistency check between the rule-based draft labels and an independent LLM judge path.

For the DynHD 400 answers we already have reviewed rule labels. This script samples a fixed
set, asks the SAME frozen prompt (judge_prompt_v3.txt) through the J2 endpoint, and reports
agreement, disagreement samples and Cohen's kappa. It never edits the main labels: it exists
to quantify how much the label source matters.

Requires MOMA_API_KEY. Without a key it prints the plan and exits 0 (nothing is written).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(REPO / "scripts/dynhd_repro"))
sys.path.insert(0, str(REPO / "references/repos/DynHD"))
from dynhd.data.io import load_trace  # noqa: E402

ENDPOINT = "https://zhenze-huhehaote.cme-cloud/v1/chat/completions".replace("cme-cloud", "cmecloud.cn")
MODEL = "deepseek-v4.1-flash"
PROMPT = REPO / "data/tre_repro/judge_prompt_v3.txt"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset", default=str(REPO / "data/raw_qa/subsets/pilot200.jsonl"))
    parser.add_argument("--samples-per-model", type=int, default=50)
    parser.add_argument("--seed", type=int, default=20261021)
    parser.add_argument("--out", default=str(REPO / "reports/dynhd_label_consistency.json"))
    parser.add_argument("--endpoint", default=ENDPOINT,
                        help="chat/completions URL or an OpenAI-compatible base URL")
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--api-key-env", default="MOMA_API_KEY",
                        help="environment variable holding the API key")
    parser.add_argument("--checkpoint", default=None,
                        help="per-item resume file (default <out>.partial.jsonl)")
    args = parser.parse_args()
    endpoint = args.endpoint if args.endpoint.endswith("/chat/completions") \
        else args.endpoint.rstrip("/") + "/chat/completions"
    if args.model != MODEL:
        print(f"note: judge model overridden: {MODEL} -> {args.model}")

    prompt_text = PROMPT.read_text(encoding="utf-8")
    if hashlib.sha256(prompt_text.encode()).hexdigest() != "2d125bea4f6a5d5a5f97cbb48666c1c872f093d9356a00b09283dc88e5bd46cd":
        raise SystemExit("frozen judge prompt hash mismatch")
    api_key = os.environ.get(args.api_key_env)
    questions = {json.loads(line)["sample_id"]: json.loads(line)
                 for line in Path(args.subset).read_text(encoding="utf-8").splitlines() if line.strip()}
    plan = {"models": {}, "seed": args.seed, "samples_per_model": args.samples_per_model}
    sampled = []
    rng = random.Random(args.seed)
    for model in ("llada", "dream"):
        root = Path("/root/autodl-tmp/dynhd_repro") / f"traces/{model}/pilot200/valid"
        traces = sorted(root.glob("*.pt"))
        rng.shuffle(traces)
        chosen = traces[: args.samples_per_model]
        plan["models"][model] = len(chosen)
        for path in chosen:
            data = load_trace(str(path))
            meta = data["meta"]
            row = questions.get(str(meta.get("id")))
            if row is None:
                continue
            sampled.append({"model": model, "sample_id": meta["id"], "question": row["question"],
                            "references": [row["gold_answer"], *(row.get("gold_aliases") or [])],
                            "answer": meta.get("generated_text", ""), "rule_label": int(data["label"])})

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
                reason = str(verdict_obj.get("reason", ""))[:400]
                return 0 if verdict == "correct" else 1, verdict, reason
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
            resolved_n = sum(1 for r in rows if r["judge_label"] is not None)
            print(f"  judged {index}/{len(sampled)} (resolved {resolved_n})", flush=True)
    resolved = [row for row in rows if row["judge_label"] is not None]
    agreement = sum(1 for row in resolved if row["agree"]) / len(resolved) if resolved else None
    # Cohen's kappa against the rule labels
    kappa = None
    if resolved:
        n = len(resolved)
        po = sum(1 for row in resolved if row["agree"]) / n
        p_rule = sum(1 for row in resolved if row["rule_label"] == 1) / n
        p_judge = sum(1 for row in resolved if row["judge_label"] == 1) / n
        pe = p_rule * p_judge + (1 - p_rule) * (1 - p_judge)
        kappa = (po - pe) / (1 - pe) if pe < 1 else None
    payload = {"date": "2026-10-22", "judge_model": args.model, "judge_endpoint": endpoint,
               "judge_prompt_sha256":
               hashlib.sha256(prompt_text.encode()).hexdigest(),
               "plan": plan, "seed": args.seed,
               "samples_requested": len(sampled), "samples_resolved": len(resolved),
               "agreement": agreement, "cohens_kappa": kappa,
               "disagreements": [row for row in resolved if not row["agree"]][:20],
               "note": "supplementary label-quality evidence; the main labels stay the reviewed rule sign-off"}
    out = Path(args.out)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    rows_out = out.with_name(out.stem + ".rows.jsonl")
    rows_out.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    if all(row["judge_label"] is not None for row in rows) and ckpt_path.exists():
        ckpt_path.unlink()
    print(json.dumps({k: payload[k] for k in ("samples_requested", "samples_resolved", "agreement", "cohens_kappa")},
                     indent=2, ensure_ascii=False))
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
