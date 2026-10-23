#!/usr/bin/env python
"""Third-opinion adjudication of the R2 rule-vs-judge disagreements.

R2's TRE AUROC is 0.682 under judge labels but 0.542 under rule labels, so the
conclusion depends on which labeller is right. This asks a *different* judge --
LongCat-2.5-Preview, a different model family from deepseek-v4.1-flash -- to label
only the 142 rows where rule and judge disagree, under the same frozen prompt v3.

It does not overwrite anything. The deliverable is a count: of the disagreements, how
many does the third judge side with the rule, and how many with the deepseek judge.
That number decides whether the rule or the judge is the systematic outlier on
HotpotQA's long answers.

Usage:
  set -a; . /root/autodl-tmp/.env.longcat; set +a
  .venv/bin/python scripts/r2_adjudicate.py \
      --disagreements /tmp/opencode/r2_disagreements.json \
      --out reports/tre_repro/r2_adjudication.json --workers 3
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
VERDICTS = ("correct", "incorrect")


def call(endpoint: str, model: str, prompt: str, row: dict, key: str, timeout: int) -> dict:
    payload = json.dumps({"question": row["question"], "reference_answers": [row["gold"]],
                          "proposed_answer": row["answer"]}, ensure_ascii=False)
    body = json.dumps({"model": model, "temperature": 0, "max_tokens": 2048,
                       "response_format": {"type": "json_object"},
                       "messages": [{"role": "system", "content": prompt},
                                    {"role": "user", "content": payload}]}).encode("utf-8")
    request = urllib.request.Request(endpoint, data=body, method="POST",
                                     headers={"Content-Type": "application/json",
                                              "Authorization": f"Bearer {key}"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                content = json.loads(response.read())["choices"][0]["message"]["content"]
            verdict = str(json.loads(content)["verdict"]).lower()
            if verdict not in VERDICTS:
                raise ValueError(f"verdict {verdict!r}")
            return {"ok": True, "verdict": verdict,
                    "reason": str(json.loads(content).get("reason", ""))[:300]}
        except Exception as error:  # noqa: BLE001
            if attempt == 4:
                return {"ok": False, "error": f"{type(error).__name__}: {error}"}
            time.sleep(2 ** (attempt + 1))
    return {"ok": False, "error": "unreachable"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--disagreements", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--endpoint", default=os.environ.get("LONGCAT_BASE_URL", "").rstrip("/") + "/chat/completions")
    parser.add_argument("--model", default="LongCat-2.5-Preview")
    parser.add_argument("--key-env", default="LONGCAT_API_KEY")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    key = os.environ.get(args.key_env)
    if not key:
        raise SystemExit(f"{args.key_env} is not set")
    prompt = PROMPT.read_text(encoding="utf-8")
    import hashlib
    if hashlib.sha256(prompt.encode()).hexdigest() != PROMPT_SHA256:
        raise SystemExit("frozen judge prompt hash mismatch")

    rows = json.loads(Path(args.disagreements).read_text(encoding="utf-8"))
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(call, args.endpoint, args.model, prompt, row, key, args.timeout): row
                   for row in rows}
        for done, future in enumerate(as_completed(futures), 1):
            row = futures[future]
            verdict = future.result()
            results.append({**row, "third_verdict": verdict.get("verdict"),
                            "third_reason": verdict.get("reason", ""),
                            "third_ok": verdict["ok"]})
            if done % 20 == 0:
                print(f"  {done}/{len(rows)}", flush=True)

    resolved = [r for r in results if r["third_ok"]]
    sides = Counter()
    for r in resolved:
        if r["third_verdict"] == r["rule_label"] == r["judge_label"]:
            sides["both"] += 1
        elif r["third_verdict"] == r["rule_label"]:
            sides["rule"] += 1
        elif r["third_verdict"] == r["judge_label"]:
            sides["deepseek_judge"] += 1
        else:
            sides["neither"] += 1
    by_type = Counter((r["rule_label"], r["judge_label"],
                       "rule" if r["third_verdict"] == r["rule_label"] else
                       ("judge" if r["third_verdict"] == r["judge_label"] else "other"))
                      for r in resolved)

    payload = {
        "disagreements": str(args.disagreements),
        "third_judge": args.model,
        "third_endpoint": args.endpoint,
        "judge_prompt_sha256": PROMPT_SHA256,
        "n": len(rows),
        "resolved": len(resolved),
        "sides_with": dict(sides),
        "by_disagreement_type": {str(k): v for k, v in by_type.items()},
        "note": ("third opinion on the rows where the rule and the deepseek judge differed; "
                 "nothing is overwritten, this only says which labeller is the outlier"),
        "rows": results,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("n", "resolved", "sides_with", "by_disagreement_type")},
                     indent=2, ensure_ascii=False))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
