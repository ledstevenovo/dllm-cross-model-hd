"""Fetch revision-pinned raw parquet from an alternate HuggingFace endpoint.

Why this exists: ``scripts/download_raw.py`` uses the URLs recorded verbatim in
``configs/datasets/sources.lock.json``, and those point at ``huggingface.co`` --
unreachable from some hosts (verified on the AutoDL 4080 instance, HTTP 000).
Setting ``HF_ENDPOINT`` has no effect there because that script does not use
``huggingface_hub``.  So the mirror substitution is made explicit and auditable
here: **only the host is replaced**, the path/revision/filename stay identical,
and the downloaded bytes are verified against the SHA256 already recorded in the
lock file.  A mirror can therefore never smuggle different data in unnoticed.

Not required for the R1 question lists (decision B samples from the frozen pool;
see the plan §4.2); it is the documented path for rebuilding the *raw* pool or
for adding HotpotQA/CommonsenseQA in R2.

Usage::

    uv run python scripts/fetch_raw_via_mirror.py                       # all files in the lock
    uv run python scripts/fetch_raw_via_mirror.py --key triviaqa_rc_nocontext_validation
    uv run python scripts/fetch_raw_via_mirror.py --endpoint https://hf-mirror.com
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "configs/datasets/sources.lock.json"
DEFAULT_ENDPOINT = "https://hf-mirror.com"
REPORT = ROOT / "reports/raw_mirror_fetch.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def rewrite_host(url: str, endpoint: str) -> str:
    """Replace only the scheme+host of ``url`` with ``endpoint``'s."""
    if urlsplit(url).hostname is None:
        raise ValueError(f"lock URL has no host: {url}")
    parsed_endpoint = urlsplit(endpoint)
    if parsed_endpoint.scheme != "https" or not parsed_endpoint.hostname:
        raise ValueError("endpoint must be an absolute https URL")
    source = urlsplit(url)
    return urlunsplit((parsed_endpoint.scheme, parsed_endpoint.netloc, source.path, source.query, source.fragment))


def fetch(spec: dict, endpoint: str, *, force: bool, timeout: int = 180) -> dict:
    target = ROOT / spec["path"]
    url = rewrite_host(spec["url"], endpoint)
    result = {"key": spec["key"], "target": spec["path"], "lock_url": spec["url"], "url_used": url,
              "expected_bytes": spec["bytes"], "expected_sha256": spec["sha256"]}
    if target.exists() and not force:
        digest = sha256(target)
        if digest == spec["sha256"]:
            result.update(status="already_present_verified", bytes=target.stat().st_size, sha256=digest)
            return result
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".partial")
    request = urllib.request.Request(url, headers={"User-Agent": "dllm-hd/0.1 (tre-repro mirror fetch)"})
    with urllib.request.urlopen(request, timeout=timeout) as response, partial.open("wb") as handle:
        while True:
            block = response.read(1 << 20)
            if not block:
                break
            handle.write(block)
    digest = sha256(partial)
    size = partial.stat().st_size
    if size != spec["bytes"] or digest != spec["sha256"]:
        partial.unlink()
        raise ValueError(f"mirror content does not match the lock for {spec['key']}: {size} bytes / {digest}")
    partial.replace(target)
    result.update(status="fetched_and_verified", bytes=size, sha256=digest)
    return result


def merge_report(previous: list[dict], results: list[dict]) -> list[dict]:
    """Merge new fetch results into the existing report, keyed by lock key.

    ``--key X`` used to rewrite the whole report with only X's entry, silently
    dropping the record that the other raw files had been fetched and verified.
    The report is the evidence that raw inputs match the lock, so entries are
    merged and sorted rather than replaced.
    """
    merged = {entry["key"]: entry for entry in previous}
    for entry in results:
        merged[entry["key"]] = entry
    return [merged[key] for key in sorted(merged)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--key", help="only this lock key (default: every file in the lock)")
    parser.add_argument("--force", action="store_true", help="re-download even when a verified copy exists")
    args = parser.parse_args(argv)

    specs = json.loads(LOCK.read_text(encoding="utf-8"))["files"]
    if args.key:
        specs = [spec for spec in specs if spec["key"] == args.key]
        if not specs:
            raise SystemExit(f"no lock entry named {args.key!r}")
    results = []
    for spec in specs:
        print(f"[get] {spec['key']} <- {rewrite_host(spec['url'], args.endpoint)}", flush=True)
        results.append(fetch(spec, args.endpoint, force=args.force))
        print(f"      {results[-1]['status']} ({results[-1]['bytes']} bytes, sha256 {results[-1]['sha256'][:16]}…)", flush=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    # Merge into the existing report instead of replacing it: fetching one --key
    # used to erase the provenance of every other file, so the audit trail lost
    # the record of which raw files had actually been verified.
    previous: list[dict] = []
    if REPORT.exists():
        try:
            previous = json.loads(REPORT.read_text(encoding="utf-8"))["files"]
        except (KeyError, ValueError):
            previous = []
    merged = merge_report(previous, results)
    REPORT.write_text(json.dumps({
        "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "endpoint": args.endpoint,
        "note": "host-rewritten fetch; every file verified against configs/datasets/sources.lock.json",
        "files": merged,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[write] {REPORT.relative_to(ROOT)} ({len(merged)} file(s) recorded)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
