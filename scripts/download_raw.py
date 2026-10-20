"""Download the raw QA source files (public HF parquet mirrors) into data/raw_download.

Design note: the master question pool is built ONLY from held-out splits
(TriviaQA rc.nocontext validation+test, HotpotQA distractor validation), so that
neither dataset's original *training* corpus can leak into our detector splits.

Usage:
  python scripts/download_raw.py [--force]

Idempotent: skips files whose sha256 matches the recorded digest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request

HF = "https://huggingface.co/datasets"

FILES = [
    dict(
        key="triviaqa_rc_nocontext_validation",
        url=f"{HF}/mandarjoshi/trivia_qa/resolve/main/rc.nocontext/validation-00000-of-00001.parquet",
        dest="triviaqa/rc.nocontext_validation.parquet",
        dataset="triviaqa",
        config="rc.nocontext",
        split="validation",
    ),
    dict(
        key="triviaqa_rc_nocontext_test",
        url=f"{HF}/mandarjoshi/trivia_qa/resolve/main/rc.nocontext/test-00000-of-00001.parquet",
        dest="triviaqa/rc.nocontext_test.parquet",
        dataset="triviaqa",
        config="rc.nocontext",
        split="test",
    ),
    dict(
        key="hotpotqa_distractor_validation",
        url=f"{HF}/hotpotqa/hotpot_qa/resolve/main/distractor/validation-00000-of-00001.parquet",
        dest="hotpotqa/distractor_validation.parquet",
        dataset="hotpotqa",
        config="distractor",
        split="validation",
    ),
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw_download")
INDEX = os.path.join(RAW, "raw_index.json")


def sha256(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def fetch(url: str, dest: str, retries: int = 4) -> None:
    last = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "dllm-hd-dataprep/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as fh:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    fh.write(b)
            return
        except Exception as e:  # noqa: BLE001
            last = e
            sys.stderr.write(f"    attempt {attempt}/{retries} failed: {e}\n")
            time.sleep(3 * attempt)
    raise RuntimeError(f"download failed for {url}: {last}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    os.makedirs(RAW, exist_ok=True)
    index = {}
    if os.path.exists(INDEX):
        with open(INDEX, encoding="utf-8") as fh:
            index = json.load(fh)
    records = index.get("files", {})

    for spec in FILES:
        dest = os.path.join(RAW, spec["dest"].replace("/", os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        rec = records.get(spec["key"], {})
        if os.path.exists(dest) and not args.force and rec.get("sha256") == sha256(dest):
            print(f"[skip] {spec['dest']} already present ({os.path.getsize(dest)} bytes)")
            continue
        print(f"[get ] {spec['url']}")
        fetch(spec["url"], dest)
        digest = sha256(dest)
        records[spec["key"]] = {
            "url": spec["url"],
            "path": "data/raw_download/" + spec["dest"],
            "dataset": spec["dataset"],
            "config": spec["config"],
            "source_split": spec["split"],
            "bytes": os.path.getsize(dest),
            "sha256": digest,
        }
        print(f"       -> {spec['dest']}  {os.path.getsize(dest)} bytes  sha256={digest[:16]}...")

    with open(INDEX, "w", encoding="utf-8") as fh:
        json.dump({"files": records}, fh, indent=2, ensure_ascii=False, sort_keys=True)
    print(f"\nwrote {INDEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
