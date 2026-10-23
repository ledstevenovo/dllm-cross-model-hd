"""Contract tests for the TRE-vs-detector comparison.

Two things are easy to get silently wrong in that script and both would invalidate the
comparison without looking broken: cluster folds that leak a question into both sides, and
the two-pass judge protocol being collapsed into "first verdict wins" (which would keep
samples that should be dropped).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tre_vs_detectors import cluster_folds, protocol_label  # noqa: E402


def frame_with_clusters():
    rows = []
    for cluster in ("a", "b", "c", "d", "e"):
        for inside in range(4):
            rows.append({"question_id": f"{cluster}{inside}", "cluster_id": cluster,
                         "label": "correct" if inside % 2 else "incorrect"})
    frame = pd.DataFrame(rows)
    frame["y"] = frame.label.eq("incorrect").astype(int)
    return frame


def test_folds_are_disjoint_and_cover_everything():
    frame = frame_with_clusters()
    folds = cluster_folds(frame, k=5, seed=42)
    assert len(folds) == 5
    held = np.concatenate([h for h, _ in folds])
    assert len(held) == len(frame)
    assert len(set(held.tolist())) == len(frame), "a row was held out more than once"


def test_no_cluster_appears_on_both_sides_of_a_split():
    frame = frame_with_clusters()
    for held, trained in cluster_folds(frame, k=5, seed=42):
        held_clusters = set(frame.loc[held, "cluster_id"])
        train_clusters = set(frame.loc[trained, "cluster_id"])
        assert not (held_clusters & train_clusters), "cluster leaked across the fold"


def test_folds_are_deterministic_for_a_seed():
    frame = frame_with_clusters()
    first = [h.tolist() for h, _ in cluster_folds(frame, k=5, seed=7)]
    second = [h.tolist() for h, _ in cluster_folds(frame, k=5, seed=7)]
    assert first == second


def test_different_seeds_give_different_folds():
    frame = frame_with_clusters()
    first = [h.tolist() for h, _ in cluster_folds(frame, k=5, seed=1)]
    second = [h.tolist() for h, _ in cluster_folds(frame, k=5, seed=2)]
    assert first != second


def test_protocol_label_keeps_correct_and_double_incorrect():
    assert protocol_label({"judge_first": "correct"}) == "correct"
    assert protocol_label({"judge_first": "incorrect", "judge_second": "incorrect"}) == "incorrect"


def test_protocol_label_drops_the_flip():
    # The frozen protocol drops a sample whose second pass overturns "incorrect"; treating
    # the first verdict as final would keep 14 such samples on the LLaDA HotpotQA run.
    assert protocol_label({"judge_first": "incorrect", "judge_second": "correct"}) is None


def test_protocol_label_rejects_incomplete_or_missing_verdicts():
    assert protocol_label({"judge_first": "incorrect"}) is None
    assert protocol_label({}) is None
    assert protocol_label({"judge_first": None}) is None
