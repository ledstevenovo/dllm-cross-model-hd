#!/usr/bin/env python
"""Cross-judge consistency: does a second vendor's judge reproduce the frozen labels?

Why this exists: the TRE main table's labels were produced by J2 (moma
``deepseek-v4.1-flash``) and every R1 number rests on them.  A replacement credential
arrived on a *different* vendor's endpoint (vankit, same model id).  Same model name on
a different vendor is not the same judge -- different serving stack, quantization,
sampling defaults and possibly a different snapshot -- so the project rule "one label
file, one judge, one protocol" forbids silently splicing them.

This script measures the difference instead of assuming it.  It takes the rows already
judged by the reference judge, re-judges the *same text* with the candidate judge, and
reports agreement and Cohen's kappa under the frozen two-pass protocol (first verdict
correct -> keep; incorrect -> second real call; both incorrect -> keep; a flip
incorrect->correct drops the sample).

Two numbers matter and they answer different questions:

* first-pass agreement -- how often the two judges read the same answer the same way;
* final-label agreement -- what a downstream table would actually see, which also
  depends on how often the second pass flips.

Output: a JSON report with per-row detail so a disagreement can be inspected, not just
counted.  Read-only on the existing label file.

Usage:
  set -a; . /root/autodl-tmp/.env.judge; set +a
  .venv/bin/python scripts/judge_crosscheck.py \
      --reference data/tre_repro/labels/llada_triviaqa_fp16_L128_S64_B128_v3/paper_judgments.jsonl \
      --sample /tmp/opencode/judge_crosscheck_100.json \
      --out reports/tre_repro/judge_crosscheck.json --workers 8
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_PROMPT = ROOT / "data/tre_repro/judge_prompt_v3.txt"
PROMPT_SHA256 = "2d125bea4f6a5d5a5f97cbb48666c1c872f093d9356a00b09283dc88e5bd46cd"
VERDICTS = ("correct", "incorrect")
LOCK = threading.Lock()


def sha256_text(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_references(questions: Path) -> dict[str, dict]:
    refs = {}
    for row in read_jsonl(questions):
        answers = [row["gold_answer"], *(row.get("gold_aliases") or [])]
        seen, unique = set(), []
        for answer in answers:
            text = str(answer)
            if text.strip() and text not in seen:
                seen.add(text)
                unique.append(text)
        refs[row["question_id"]] = {"question": row["question"], "references": unique}
    return refs


def call(endpoint: str, model: str, prompt: str, entry: dict, answer: str,
         api_key: str, timeout: int, max_tokens: int) -> dict:
    payload = json.dumps({"question": entry["question"], "reference_answers": entry["references"],
                          "proposed_answer": answer}, ensure_ascii=False)
    body = json.dumps({"model": model, "temperature": 0, "response_format": {"type": "json_object"},
                       "max_tokens": max_tokens,
                       "messages": [{"role": "system", "content": prompt},
                                    {"role": "user", "content": payload}]}).encode("utf-8")
    request = urllib.request.Request(endpoint, data=body, method="POST",
                                     headers={"Content-Type": "application/json",
                                              "Authorization": f"Bearer {api_key}"})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", "replace")
            status = response.status
    except Exception as error:
        return {"ok": False, "error": f"{type(error).__name__}: {error}",
                "latency_s": round(time.perf_counter() - started, 3)}
    latency = round(time.perf_counter() - started, 3)
    try:
        message = json.loads(raw)["choices"][0]["message"]
        content = message.get("content")
        parsed = json.loads(content)
        verdict = str(parsed["verdict"]).strip().lower()
        if verdict not in VERDICTS:
            raise ValueError(f"verdict outside {VERDICTS}: {verdict!r}")
    except Exception as error:
        return {"ok": False, "error": f"{type(error).__name__}: {error}", "latency_s": latency,
                "raw": raw[:400]}
    return {"ok": True, "verdict": verdict, "reason": str(parsed.get("reason", ""))[:300],
            "latency_s": latency}


def kappa(pairs: list[tuple[str, str]]) -> tuple[float, float]:
    """Cohen's kappa for two raters over the binary verdict vocabulary."""
    total = len(pairs)
    if not total:
        return 0.0, 0.0
    agree = sum(1 for a, b in pairs if a == b) / total
    labels = sorted({v for pair in pairs for v in pair})
    expected = sum((sum(1 for a, _ in pairs if a == label) / total)
                   * (sum(1 for _, b in pairs if b == label) / total) for label in labels)
    if expected >= 1.0:
        return agree, 1.0 if agree >= 1.0 else 0.0
    return agree, (agree - expected) / (1.0 - expected)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True, help="label file judged by the reference judge")
    parser.add_argument("--sample", required=True,
                        help="JSON list of {sample_id, question_id, question, generated_text, moma_first, moma_second}")
    parser.add_argument("--questions", default=str(ROOT / "data/tre_repro/questions/triviaqa_eval800.jsonl"))
    parser.add_argument("--prompt", default=str(DEFAULT_PROMPT))
    parser.add_argument("--out", required=True)
    parser.add_argument("--endpoint", default=os.environ.get("JUDGE_ENDPOINT", ""))
    parser.add_argument("--model", default=os.environ.get("JUDGE_MODEL", "deepseek-v4.1-flash"))
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--retries", type=int, default=3)
    args = parser.parse_args()

    api_key = os.environ.get("MOMA_API_KEY")
    if not api_key:
        raise SystemExit("MOMA_API_KEY is not set")
    if not args.endpoint:
        raise SystemExit("--endpoint or JUDGE_ENDPOINT is required")

    prompt = Path(args.prompt).read_text(encoding="utf-8")
    digest = sha256_text(prompt)
    if digest != PROMPT_SHA256:
        raise SystemExit(f"judge prompt hash mismatch: {digest} != frozen {PROMPT_SHA256}")

    references = load_references(Path(args.questions))
    sample = json.loads(Path(args.sample).read_text(encoding="utf-8"))
    reference = {row["sample_id"]: row for row in read_jsonl(Path(args.reference))}

    def judge(row: dict) -> dict:
        entry = references[row["question_id"]]
        first = None
        for attempt in range(args.retries + 1):
            first = call(args.endpoint, args.model, prompt, entry, row["generated_text"],
                         api_key, args.timeout, args.max_tokens)
            if first.get("ok"):
                break
            time.sleep(2 ** attempt)
        if not first or not first.get("ok"):
            return {**row, "candidate_first": None, "candidate_second": None,
                    "status": "unresolved", "error": (first or {}).get("error")}
        result = {**row, "candidate_first": first["verdict"],
                  "candidate_first_reason": first.get("reason", ""), "status": "done"}
        if first["verdict"] == "correct":
            return result
        second = None
        for attempt in range(args.retries + 1):
            second = call(args.endpoint, args.model, prompt, entry, row["generated_text"],
                          api_key, args.timeout, args.max_tokens)
            if second.get("ok"):
                break
            time.sleep(2 ** attempt)
        if not second or not second.get("ok"):
            result.update(status="unresolved", candidate_second=None,
                          error=(second or {}).get("error"))
            return result
        result["candidate_second"] = second["verdict"]
        result["candidate_second_reason"] = second.get("reason", "")
        return result

    started = time.perf_counter()
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(judge, row): row for row in sample}
        for done, future in enumerate(as_completed(futures), 1):
            row = future.result()
            rows.append(row)
            with LOCK:
                print(f"[crosscheck] {done}/{len(sample)} {row['sample_id'][:30]} "
                      f"ref={row.get('moma_first')} cand={row.get('candidate_first')} "
                      f"{row.get('status')}", flush=True)
    elapsed = time.perf_counter() - started

    resolved = [r for r in rows if r["status"] == "done"]

    def final_label(row: dict, first_key: str, second_key: str) -> str:
        first = row.get(first_key)
        if first == "correct":
            return "correct"
        second = row.get(second_key)
        if second == "incorrect":
            return "incorrect"
        if second == "correct":
            return "flipped"
        return "unresolved"

    first_pairs = [(r["moma_first"], r["candidate_first"]) for r in resolved]
    final_pairs = []
    for r in resolved:
        a = final_label(r, "moma_first", "moma_second")
        b = final_label(r, "candidate_first", "candidate_second")
        if "unresolved" in (a, b):
            continue
        final_pairs.append((a, b))

    agree_first, kappa_first = kappa(first_pairs)
    agree_final, kappa_final = kappa(final_pairs)
    flips = [r for r in resolved if final_label(r, "moma_first", "moma_second") == "flipped"
             or final_label(r, "candidate_first", "candidate_second") == "flipped"]

    report = {
        "reference": str(args.reference),
        "endpoint": args.endpoint,
        "model": args.model,
        "judge_prompt_sha256": digest,
        "sampled": len(sample),
        "resolved": len(resolved),
        "unresolved": len(rows) - len(resolved),
        "elapsed_seconds": round(elapsed, 1),
        "first_pass": {"n": len(first_pairs), "agreement": agree_first, "kappa": kappa_first},
        "final_label": {"n": len(final_pairs), "agreement": agree_final, "kappa": kappa_final},
        "final_label_counts": {
            "reference": {k: sum(1 for a, _ in final_pairs if a == k) for k in ("correct", "incorrect")},
            "candidate": {k: sum(1 for _, b in final_pairs if b == k) for k in ("correct", "incorrect")},
        },
        "flip_rows": [r["sample_id"] for r in flips],
        "notes": [
            "same model id on a different vendor is not the same judge; this measures the gap",
            "first_pass agreement compares only the first verdict; final_label also folds in the second pass",
            "a flip (incorrect->correct on the second pass) drops the sample, so it shows up as a label difference",
        ],
        "rows": rows,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("sampled", "resolved", "unresolved",
                                             "first_pass", "final_label", "final_label_counts")},
                     indent=2, ensure_ascii=False))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
