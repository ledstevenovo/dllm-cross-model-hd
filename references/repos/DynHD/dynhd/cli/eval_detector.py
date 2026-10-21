from __future__ import annotations

import argparse
import json
from typing import Dict, List

import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

from dynhd.data import load_trace_dir
from dynhd.detectors import DetectorConfig, DynHDDetector


def _load_split(path: str, part: str, size: int) -> List[int]:
    with open(path, "r", encoding="utf-8") as handle:
        split: Dict[str, List[int]] = json.load(handle)
    if part not in split:
        raise ValueError(f"Split does not contain partition {part!r}")
    indices = [int(index) for index in split[part]]
    if any(index < 0 or index >= size for index in indices):
        raise ValueError("Split contains an out-of-range trace index")
    return indices


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained DynHD detector")
    parser.add_argument("--data-path", required=True, help="Directory containing .pt traces")
    parser.add_argument("--ckpt", required=True, help="detector.pt produced by train_detector")
    parser.add_argument("--split", default=None, help="Optional split.json")
    parser.add_argument("--split-part", default="test", choices=["train", "val", "test"])
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    if not 0.0 <= args.threshold <= 1.0:
        raise ValueError("--threshold must be in [0, 1]")
    data = load_trace_dir(args.data_path)
    if args.split:
        indices = _load_split(args.split, args.split_part, len(data))
        data = [data[index] for index in indices]
    if not data:
        raise ValueError("Evaluation partition is empty")

    checkpoint = torch.load(args.ckpt, map_location="cpu", weights_only=True)
    cfg = DetectorConfig(**checkpoint["cfg"])
    detector = DynHDDetector(cfg, device=args.device)
    detector.ensure_prompt_projector(data)
    detector.reference.load_state_dict(checkpoint["reference"])
    detector.deviation.load_state_dict(checkpoint["deviation"])
    if checkpoint.get("prompt_projector") is not None:
        if detector.prompt_projector is None:
            raise ValueError("Checkpoint expects prompt embeddings with a projected dimension")
        detector.prompt_projector.load_state_dict(checkpoint["prompt_projector"])

    labels = np.asarray([int(item["label"]) for item in data], dtype=np.int64)
    scores = detector.predict_proba(data)
    predictions = (scores >= args.threshold).astype(np.int64)
    metrics = {
        "samples": int(labels.size),
        "auroc": float(roc_auc_score(labels, scores)) if np.unique(labels).size > 1 else None,
        "accuracy": float(accuracy_score(labels, predictions)),
        "precision": float(precision_score(labels, predictions, zero_division=0)),
        "recall": float(recall_score(labels, predictions, zero_division=0)),
        "f1": float(f1_score(labels, predictions, zero_division=0)),
    }
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
