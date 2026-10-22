"""The mirror fetch report is an audit trail, so a single-key fetch must not erase it.

History: ``--key X`` used to rewrite ``reports/raw_mirror_fetch.json`` with only X's
entry, silently dropping the record that the other raw files had been fetched and
sha256-verified.  The report is the evidence that raw inputs match the lock, so
losing entries weakens the provenance of everything built from them.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from fetch_raw_via_mirror import merge_report  # noqa: E402


def entry(key, status="fetched_and_verified"):
    return {"key": key, "status": status, "sha256": "0" * 64}


def test_merging_a_single_key_keeps_the_earlier_entries():
    previous = [entry("triviaqa_rc_nocontext_validation")]
    merged = merge_report(previous, [entry("hotpotqa_distractor_validation", "already_present_verified")])
    assert [e["key"] for e in merged] == [
        "hotpotqa_distractor_validation",
        "triviaqa_rc_nocontext_validation",
    ]


def test_a_re_fetch_replaces_that_key_only():
    previous = [entry("a", "fetched_and_verified"), entry("b")]
    merged = merge_report(previous, [entry("a", "already_present_verified")])
    by_key = {e["key"]: e for e in merged}
    assert by_key["a"]["status"] == "already_present_verified"
    assert by_key["b"]["status"] == "fetched_and_verified"


def test_merge_is_stable_and_does_not_mutate_inputs():
    previous = [entry("b")]
    results = [entry("a")]
    merge_report(previous, results)
    assert previous == [entry("b")] and results == [entry("a")]


def test_empty_previous_report_is_fine():
    assert [e["key"] for e in merge_report([], [entry("a"), entry("b")])] == ["a", "b"]
