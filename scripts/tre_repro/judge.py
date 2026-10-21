#!/usr/bin/env python
"""J2 judge client for the TRE reproduction (R1): moma `deepseek-v4.1-flash`, frozen prompt v3.

Flow (frozen in docs/TRE_4080SUPER_32GB_复现方案.md §4.4):
  first verdict correct  -> keep (y=0), no second call
  first verdict incorrect -> second real call; both incorrect -> keep (y=1)
  incorrect -> correct     -> dropped (record both raw verdicts)
  API/schema/empty        -> needs_review (never silently incorrect, never dropped)

Every judgment is bound to the judged text through ``generated_text_sha256`` taken from the
trace metadata; the frozen prompt hash is verified before any call. Credentials come from the
``MOMA_API_KEY`` environment variable and are never written to any file.

Resume safety: stored rows are re-verified on startup (sample presence, answer hash, frozen
prompt hash, model/endpoint); rows that fail are moved to ``paper_judgments.jsonl.stale.jsonl``
and those samples are judged again instead of being reused. Rows with ``status=needs_review``
(rate limits, schema anomalies) block the main table and are re-judged with
``--retry-needs-review`` (previous attempts are appended to ``paper_judgments.jsonl.retry.jsonl``).

Retries: ``--retries N`` means N retries after the first call (N+1 calls max), waiting
2 s, 4 s, 8 s, ... between them.

Usage (smoke first, then the formal run):
  export MOMA_API_KEY=...
  .venv/bin/python scripts/tre_repro/judge.py --dry-run \
      --run data/trajectories/tre_repro/llada_v3_smoke20_L128_S64_B128 --limit 1
  .venv/bin/python scripts/tre_repro/judge.py \
      --run data/trajectories/tre_repro/llada_v3_smoke20_L128_S64_B128
  .venv/bin/python scripts/tre_repro/judge.py \
      --run data/trajectories/tre_repro/llada_triviaqa_fp16_L128_S64_B128_v3
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import random
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROMPT = ROOT / "data/tre_repro/judge_prompt_v3.txt"
PROMPT_SHA256 = "2d125bea4f6a5d5a5f97cbb48666c1c872f093d9356a00b09283dc88e5bd46cd"
ENDPOINT = "https://zhenze-huhehaote.cmecloud.cn/v1/chat/completions"
MODEL = "deepseek-v4.1-flash"
VERDICTS = ("correct", "incorrect")
LOCK = threading.Lock()
_RATE_LOCK = threading.Lock()
_LAST_CALL = [0.0]
_MIN_INTERVAL = 0.0


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_run_samples(run: Path) -> dict[str, dict]:
    """sample_id -> {question_id, generated_text, generated_text_sha256, trace_sha256_verified}."""
    manifest = json.loads((run / "manifest.json").read_text())
    samples = {}
    import numpy as np  # local import: project venv has numpy
    for sample_id, record in manifest["samples"].items():
        trace = run / record["path"]
        if sha256_file(trace) != record["sha256"]:
            raise SystemExit(f"trace hash mismatch for {sample_id}: {trace}")
        with np.load(trace, allow_pickle=False) as z:
            meta = json.loads(z["metadata"].item())
        samples[sample_id] = {
            "question_id": meta["question_id"],
            "generated_text": str(meta.get("generated_text", "")),
            "generated_text_sha256": sha256_text(str(meta.get("generated_text", ""))),
            "trace_sha256_verified": True,
        }
    return samples


def load_references(questions: Path) -> dict[str, dict]:
    refs = {}
    for line in questions.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        answers = [row["gold_answer"], *(row.get("gold_aliases") or [])]
        seen, unique = set(), []
        for answer in answers:
            text = str(answer)
            if text.strip() and text not in seen:
                seen.add(text)
                unique.append(text)
        refs[row["question_id"]] = {"question": row["question"], "references": unique}
    return refs


def build_request(prompt_text: str, question: str, references: list[str], answer: str,
                  max_tokens: int) -> dict:
    user_payload = json.dumps({"question": question, "reference_answers": references,
                               "proposed_answer": answer}, ensure_ascii=False)
    return {
        "model": MODEL,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": user_payload},
        ],
    }


def call_judge(request: dict, api_key: str, timeout: int) -> dict:
    if _MIN_INTERVAL > 0:
        with _RATE_LOCK:
            wait = _LAST_CALL[0] + _MIN_INTERVAL - time.perf_counter()
            if wait > 0:
                time.sleep(wait)
            _LAST_CALL[0] = time.perf_counter()
    data = json.dumps(request).encode("utf-8")
    http = urllib.request.Request(
        ENDPOINT, data=data, method="POST",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(http, timeout=timeout) as response:
            body = response.read().decode("utf-8", "replace")
            status = response.status
    except urllib.error.HTTPError as error:
        return {"http_status": error.code, "error": f"HTTPError: {error.reason}",
                "body": error.read().decode("utf-8", "replace")[:2000],
                "latency_s": round(time.perf_counter() - started, 3)}
    except Exception as error:
        return {"http_status": None, "error": f"{type(error).__name__}: {error}",
                "latency_s": round(time.perf_counter() - started, 3)}
    return {"http_status": status, "body": body, "latency_s": round(time.perf_counter() - started, 3)}


def parse_verdict(result: dict) -> tuple[str | None, str, dict]:
    """Return (verdict, reason, meta) or (None, error, meta). Only message.content is parsed."""
    if "error" in result or result.get("http_status") != 200:
        return None, result.get("error") or f"HTTP {result.get('http_status')}", {}
    try:
        payload = json.loads(result["body"])
    except Exception as error:
        return None, f"unparseable response body: {error}", {}
    try:
        message = payload["choices"][0]["message"]
        content = message.get("content")
    except Exception as error:
        return None, f"response missing choices/message/content: {error}", {}
    meta = {"response_id": payload.get("id"), "response_model": payload.get("model"),
            "usage": payload.get("usage"), "created": payload.get("created"),
            "reasoning_content_saved": "reasoning_content" in message}
    try:
        parsed = json.loads(content)
        verdict = str(parsed["verdict"]).strip().lower()
        reason = str(parsed.get("reason", ""))[:500]
    except Exception as error:
        return None, f"content is not the frozen JSON schema: {error}", meta
    if verdict not in VERDICTS:
        return None, f"verdict outside {VERDICTS}: {verdict!r}", meta
    return verdict, reason, meta


def judge_once(request: dict, api_key: str, timeout: int, retries: int, raw_log, sample_id: str,
               pass_name: str) -> tuple[str | None, str, list[dict]]:
    """One judgment pass: up to ``retries`` retries after the first call, waits 2/4/8 s."""
    attempts = []
    for retry in range(retries + 1):
        attempt_no = retry + 1
        result = call_judge(request, api_key, timeout)
        verdict, reason, meta = parse_verdict(result)
        attempts.append({"pass": pass_name, "attempt": attempt_no, "http_status": result.get("http_status"),
                         "latency_s": result.get("latency_s"), "verdict": verdict,
                         "parse_error": None if verdict else reason, **meta})
        with LOCK:
            raw_log.write(json.dumps({
                "sample_id": sample_id, "pass": pass_name, "attempt": attempt_no,
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "request": request,  # no headers, no credentials
                "response_body": result.get("body", "")[:8000],
                "error": result.get("error"), "parse_error": None if verdict else reason,
            }, ensure_ascii=False) + "\n")
            raw_log.flush()
        if verdict is not None:
            with LOCK:
                print(f"[judge] {sample_id[:34]} {pass_name} #{attempt_no} -> {verdict} "
                      f"({result.get('latency_s')}s)", flush=True)
            return verdict, reason, attempts
        with LOCK:
            print(f"[judge] {sample_id[:34]} {pass_name} #{attempt_no} -> {reason[:60]} "
                  f"({result.get('latency_s')}s)", flush=True)
        if retry < retries:
            time.sleep(2 ** attempt_no)  # after attempt 1 -> 2 s, 2 -> 4 s, 3 -> 8 s
    return None, attempts[-1]["parse_error"] if attempts else "no attempt", attempts


def judge_sample(sample_id: str, sample: dict, reference_entry: dict, prompt_text: str,
                 api_key: str, timeout: int, max_tokens: int, retries: int, raw_log) -> dict:
    question = reference_entry["question"]
    references = reference_entry["references"]
    answer = sample["generated_text"]
    request = build_request(prompt_text, question, references, answer, max_tokens)
    first, first_reason, first_attempts = judge_once(request, api_key, timeout, retries, raw_log,
                                                     sample_id, "first")
    row = {
        "sample_id": sample_id, "question_id": sample["question_id"],
        "question": reference_entry["question"],
        "generated_text_sha256": sample["generated_text_sha256"],
        "generated_text": answer,
        "model": MODEL, "endpoint": ENDPOINT, "judge_prompt_sha256": sha256_text(prompt_text),
        "params": {"temperature": 0, "response_format": {"type": "json_object"}, "max_tokens": max_tokens},
        "judged_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "attempts": {"first": first_attempts},
    }
    if first is None:
        row.update(status="needs_review", judge_first=None, judge_second=None,
                   note=f"first pass unresolved: {first_reason}")
        return row
    row["judge_first"] = first
    row["judge_first_reason"] = first_reason
    if first == "correct":
        row.update(status="done", judge_second=None)
        return row
    second, second_reason, second_attempts = judge_once(request, api_key, timeout, retries, raw_log,
                                                        sample_id, "second")
    row["attempts"]["second"] = second_attempts
    row["judge_second"] = second
    row["judge_second_reason"] = second_reason
    if second is None:
        row.update(status="needs_review", note=f"second pass unresolved: {second_reason}")
    else:
        row.update(status="done")
    return row


def validate_existing(rows: list[dict], samples: dict[str, dict], prompt_hash: str) -> tuple[list[dict], list[dict]]:
    """Re-verify stored judgments against the current run before allowing reuse.

    A row is stale when it cannot be bound to this run and prompt: missing/duplicate sample_id,
    sample not present, answer hash mismatch, judge prompt hash mismatch, or model/endpoint
    change. Stale rows are never reused.
    """
    valid, stale, seen = [], [], set()
    for row in rows:
        sample_id = row.get("sample_id")
        if not sample_id:
            reason = "missing sample_id"
        elif sample_id in seen:
            reason = "duplicate sample_id"
        elif sample_id not in samples:
            reason = "sample_id not in current run"
        elif row.get("generated_text_sha256") != samples[sample_id]["generated_text_sha256"]:
            reason = "answer hash does not match the current trace"
        elif row.get("judge_prompt_sha256") != prompt_hash:
            reason = "judge prompt hash does not match the frozen prompt"
        elif row.get("model") != MODEL or row.get("endpoint") != ENDPOINT:
            reason = "model or endpoint changed"
        else:
            reason = None
        if reason:
            stale.append({**row, "stale_reason": reason})
        else:
            valid.append(row)
            seen.add(sample_id)
    return valid, stale


def main() -> int:
    global MODEL, ENDPOINT, _MIN_INTERVAL
    parser = argparse.ArgumentParser(description="TRE J2 judge client (frozen prompt v3)")
    parser.add_argument("--run", required=True, help="trajectory run directory")
    parser.add_argument("--questions", default=str(ROOT / "data/tre_repro/questions/triviaqa_eval800.jsonl"))
    parser.add_argument("--prompt", default=str(DEFAULT_PROMPT))
    parser.add_argument("--output", default=None, help="default data/tre_repro/labels/<run>/paper_judgments.jsonl")
    parser.add_argument("--raw-output", default=None)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--retries", type=int, default=3,
                        help="retries after the first call per pass (default 3 -> up to 4 calls, backoff 2/4/8 s)")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--sample-ids", help="file with one sample_id per line (scope --retry-needs-review or a partial run)")
    parser.add_argument("--retry-needs-review", action="store_true",
                        help="re-judge rows whose status is needs_review (previous attempts are backed up)")
    parser.add_argument("--model", default=MODEL, help="judge model id (must stay one model per label file)")
    parser.add_argument("--endpoint", default=ENDPOINT, help="chat-completions endpoint")
    parser.add_argument("--min-interval", type=float, default=0.0,
                        help="minimum seconds between API call starts (pace down under rate limits)")
    parser.add_argument("--dry-run", action="store_true", help="print one request without calling the API")
    args = parser.parse_args()
    MODEL = args.model
    ENDPOINT = args.endpoint
    _MIN_INTERVAL = float(args.min_interval or 0.0)

    prompt_path = Path(args.prompt)
    prompt_text = prompt_path.read_text(encoding="utf-8")
    prompt_hash = sha256_text(prompt_text)
    if prompt_hash != PROMPT_SHA256:
        raise SystemExit(f"judge prompt hash mismatch: {prompt_hash} != frozen {PROMPT_SHA256}")

    run = Path(args.run)
    samples = load_run_samples(run)
    references = load_references(Path(args.questions))
    missing = [qid for qid in {s["question_id"] for s in samples.values()} if qid not in references]
    if missing:
        raise SystemExit(f"questions file lacks {len(missing)} question_ids, e.g. {missing[:3]}")

    # the questions file defines the expected coverage; extra traces must not exist
    run_questions = [q for q in references if q in {s["question_id"] for s in samples.values()}]
    print(f"run={run.name} samples={len(samples)} questions_in_file={len(references)}")

    target_ids = set(samples)
    if args.sample_ids:
        wanted = {line.strip() for line in Path(args.sample_ids).read_text().splitlines() if line.strip()}
        unknown = wanted - set(samples)
        if unknown:
            raise SystemExit(f"sample-ids not in run: {sorted(unknown)[:3]}")
        target_ids = wanted
        print(f"scoped to {len(target_ids)} requested samples (stored rows outside the scope are kept)")

    label_dir = ROOT / f"data/tre_repro/labels/{run.name}"
    output = Path(args.output) if args.output else label_dir / "paper_judgments.jsonl"
    raw_output = Path(args.raw_output) if args.raw_output else label_dir / "judge_raw.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)

    # Resume safety: every stored judgment must re-verify against the current run and prompt
    # before it can be reused. Stale rows are quarantined and re-judged.
    existing_rows = read_jsonl(output)
    valid_rows, stale_rows = validate_existing(existing_rows, samples, prompt_hash)
    existing = {row["sample_id"]: row for row in valid_rows}
    if existing_rows:
        print(f"existing judgments={len(existing_rows)} reusable={len(valid_rows)} stale={len(stale_rows)}")
    if stale_rows and not args.dry_run:
        stale_path = output.with_suffix(output.suffix + ".stale.jsonl")
        with open(stale_path, "a", encoding="utf-8") as fh:
            for row in stale_rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        tmp = output.with_suffix(output.suffix + ".tmp")
        tmp.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in valid_rows), encoding="utf-8")
        os.replace(tmp, output)
        print(f"quarantined {len(stale_rows)} stale judgments -> {stale_path}; those samples are re-judged")

    # needs_review rows must be re-judged (rate limits, schema anomalies) before the main
    # table can be complete; the previous attempt is backed up, never mixed in.
    if args.retry_needs_review:
        retry_rows = [row for row in valid_rows if row.get("status") == "needs_review"
                      and row.get("sample_id") in target_ids]
        if retry_rows and not args.dry_run:
            retry_path = output.with_suffix(output.suffix + ".retry.jsonl")
            with open(retry_path, "a", encoding="utf-8") as fh:
                for row in retry_rows:
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            retry_ids = {row["sample_id"] for row in retry_rows}
            keep = [row for row in valid_rows if row.get("sample_id") not in retry_ids]
            tmp = output.with_suffix(output.suffix + ".tmp")
            tmp.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in keep), encoding="utf-8")
            os.replace(tmp, output)
            valid_rows = keep
            existing = {row["sample_id"]: row for row in valid_rows}
            print(f"retrying {len(retry_rows)} needs_review judgments (previous attempts -> {retry_path})")
        elif retry_rows:
            print(f"dry-run: would retry {len(retry_rows)} needs_review judgments")

    if args.dry_run:
        sample_id = next(iter(sorted(samples)))
        sample = samples[sample_id]
        entry = references[sample["question_id"]]
        request = build_request(prompt_text, entry["question"], entry["references"],
                                sample["generated_text"], args.max_tokens)
        print(json.dumps({"sample_id": sample_id, "request": request}, indent=2, ensure_ascii=False))
        print("dry-run: no API call made; set MOMA_API_KEY and drop --dry-run to judge")
        return 0

    api_key = os.environ.get("MOMA_API_KEY")
    if not api_key:
        raise SystemExit("MOMA_API_KEY is not set; export it in the shell before judging")

    pending = [sid for sid in sorted(target_ids) if sid not in existing]
    if args.limit:
        pending = pending[: args.limit]
    print(f"already judged={len(existing)} pending={len(pending)} -> {output}")

    started = time.perf_counter()
    with open(output, "a", encoding="utf-8") as out_fh, open(raw_output, "a", encoding="utf-8") as raw_fh:
        def worker(sample_id: str) -> dict:
            return judge_sample(sample_id, samples[sample_id], references[samples[sample_id]["question_id"]],
                                prompt_text, api_key, args.timeout, args.max_tokens, args.retries, raw_fh)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
            for index, row in enumerate(pool.map(worker, pending), 1):
                with LOCK:
                    out_fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                    out_fh.flush()
                verdict = row.get("judge_first")
                second = row.get("judge_second")
                tag = row["status"] if row["status"] != "done" else (
                    "kept" if verdict == "correct" or second == "incorrect" else "dropped")
                print(f"[{index}/{len(pending)}] {row['sample_id'][:44]} first={verdict} second={second} -> {tag}")

    all_rows = read_jsonl(output)
    kept = [r for r in all_rows if r["status"] == "done" and (r["judge_first"] == "correct" or r.get("judge_second") == "incorrect")]
    negatives = [r for r in kept if r["judge_first"] == "correct"]
    positives = [r for r in kept if r["judge_first"] == "incorrect"]
    dropped = [r for r in all_rows if r["status"] == "done" and r["judge_first"] == "incorrect" and r.get("judge_second") == "correct"]
    needs = [r for r in all_rows if r["status"] == "needs_review"]
    summary = {"run": str(run), "judgments": len(all_rows), "kept": len(kept),
               "kept_correct_y0": len(negatives), "kept_incorrect_y1": len(positives),
               "dropped_incorrect_then_correct": len(dropped), "needs_review": len(needs),
               "seconds": round(time.perf_counter() - started, 1),
               "output": str(output), "raw_output": str(raw_output),
               "prompt_sha256": prompt_hash}
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if not needs and len(all_rows) == len(samples) else 1


if __name__ == "__main__":
    raise SystemExit(main())
