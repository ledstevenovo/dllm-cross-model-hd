#!/usr/bin/env python
"""Cross-judge check on Dream x HotpotQA rows, to decide whether switching vendors is safe.

The deepseek endpoint slowed to ~12 s/call (from 2.6 s), which would push the remaining
judging past 18:00. LongCat is still ~2.8 s. But swapping judges mid-file would violate
"one label file, one judge", so first measure whether the two agree on this dataset --
Dream's answers here are short entity names, unlike LLaDA's recitations, so the earlier
0.990 agreement on TriviaQA cannot simply be assumed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "data/tre_repro/judge_prompt_v3.txt"
PROMPT_SHA256 = "2d125bea4f6a5d5a5f97cbb48666c1c872f093d9356a00b09283dc88e5bd46cd"


def call(endpoint, model, prompt, row, key, timeout=180):
    payload = json.dumps({"question": row["question"], "reference_answers": [row["gold"]],
                          "proposed_answer": row["answer"]}, ensure_ascii=False)
    body = json.dumps({"model": model, "temperature": 0, "max_tokens": 2048,
                       "response_format": {"type": "json_object"},
                       "messages": [{"role": "system", "content": prompt},
                                    {"role": "user", "content": payload}]}).encode()
    request = urllib.request.Request(endpoint, data=body, method="POST",
                                     headers={"Content-Type": "application/json",
                                              "Authorization": f"Bearer {key}"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                content = json.loads(response.read())["choices"][0]["message"]["content"]
            verdict = str(json.loads(content)["verdict"]).lower()
            if verdict in ("correct", "incorrect"):
                return {"ok": True, "verdict": verdict}
            raise ValueError(f"bad verdict {verdict!r}")
        except Exception as error:
            if attempt == 5:
                return {"ok": False, "error": f"{type(error).__name__}: {error}"}
            time.sleep(2 ** (attempt + 1))
    return {"ok": False, "error": "unreachable"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()

    key = os.environ.get("LONGCAT_API_KEY")
    if not key:
        raise SystemExit("LONGCAT_API_KEY not set")
    base = os.environ.get("LONGCAT_BASE_URL", "").rstrip("/")
    endpoint = base + "/chat/completions"
    prompt = PROMPT.read_text(encoding="utf-8")
    import hashlib
    if hashlib.sha256(prompt.encode()).hexdigest() != PROMPT_SHA256:
        raise SystemExit("prompt hash mismatch")

    rows = json.loads(Path(args.sample).read_text(encoding="utf-8"))
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(call, endpoint, "LongCat-2.5-Preview", prompt, r, key): r for r in rows}
        for done, future in enumerate(as_completed(futures), 1):
            row = futures[future]
            verdict = future.result()
            results.append({**row, "other_verdict": verdict.get("verdict"), "ok": verdict["ok"]})
            if done % 20 == 0:
                print(f"  {done}/{len(rows)}", flush=True)

    resolved = [r for r in results if r["ok"]]
    pairs = [(r["judge_label"], r["other_verdict"]) for r in resolved]
    agreement = sum(1 for a, b in pairs if a == b) / len(pairs) if pairs else None
    labels = sorted({v for pair in pairs for v in pair})
    expected = sum((sum(1 for a, _ in pairs if a == l) / len(pairs)) *
                   (sum(1 for _, b in pairs if b == l) / len(pairs)) for l in labels) if pairs else 0
    kappa = (agreement - expected) / (1 - expected) if pairs and expected < 1 else None

    payload = {"sample": str(args.sample), "n": len(rows), "resolved": len(resolved),
               "deepseek_labels": dict(Counter(r["judge_label"] for r in resolved)),
               "longcat_labels": dict(Counter(r["other_verdict"] for r in resolved)),
               "agreement": agreement, "cohens_kappa": kappa,
               "confusion": {f"{a}|{b}": v for (a, b), v in Counter(pairs).items()},
               "rows": results}
    out = Path(args.out)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("n", "resolved", "agreement", "cohens_kappa", "confusion")},
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
