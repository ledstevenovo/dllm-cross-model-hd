from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict
from typing import Dict, List, Sequence

import numpy as np
import torch
from sklearn.model_selection import StratifiedShuffleSplit

from dynhd.data import create_splits, load_trace_dir
from dynhd.detectors import (
    DetectorConfig,
    DynHDDetector,
    set_seed,
)


def _save_json(path: str, value: object) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)


def _load_json(path: str) -> Dict[str, List[int]]:
    with open(path, "r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict) or not all(name in value for name in ("train", "val", "test")):
        raise ValueError("split.json must contain train, val, and test index lists")
    return {name: [int(index) for index in value[name]] for name in ("train", "val", "test")}


def _random_split(size: int, seed: int) -> Dict[str, List[int]]:
    rows = [{"index": index} for index in range(size)]
    train, val, test = create_splits(rows, seed=seed)
    return {
        "train": [row["index"] for row in train],
        "val": [row["index"] for row in val],
        "test": [row["index"] for row in test],
    }


def _stratified_split(labels: Sequence[int], seed: int) -> Dict[str, List[int]]:
    if len(labels) < 7 or min(labels.count(0), labels.count(1)) < 3:
        return _random_split(len(labels), seed)
    indices = np.arange(len(labels))
    y = np.asarray(labels, dtype=np.int64)
    first = StratifiedShuffleSplit(n_splits=1, test_size=0.30, random_state=seed)
    train_indices, temporary_indices = next(first.split(indices, y))
    temporary_labels = y[temporary_indices]
    second = StratifiedShuffleSplit(n_splits=1, test_size=0.50, random_state=seed + 1)
    val_relative, test_relative = next(second.split(temporary_indices, temporary_labels))
    return {
        "train": train_indices.tolist(),
        "val": temporary_indices[val_relative].tolist(),
        "test": temporary_indices[test_relative].tolist(),
    }


def _validate_indices(split: Dict[str, List[int]], size: int) -> None:
    flattened = split["train"] + split["val"] + split["test"]
    if any(index < 0 or index >= size for index in flattened):
        raise ValueError("Split contains an out-of-range trace index")
    if len(flattened) != len(set(flattened)):
        raise ValueError("Split partitions overlap")
    if set(flattened) != set(range(size)):
        raise ValueError("Split must cover every trace exactly once")
    if not split["train"] or not split["val"] or not split["test"]:
        raise ValueError("Train, validation, and test partitions must be non-empty")


def _infer_prompt_dim(data: Sequence[Dict]) -> int:
    dimensions = {
        int(item["prompt_emb"].numel())
        for item in data
        if isinstance(item.get("prompt_emb"), torch.Tensor)
    }
    if len(dimensions) != 1:
        raise ValueError("--prompt-dim -1 requires one consistent prompt_emb size")
    return dimensions.pop()


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the two-stage DynHD detector")
    parser.add_argument("--data-path", required=True, help="Directory containing .pt traces")
    parser.add_argument("--out-dir", required=True, help="Output directory")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--split", default=None, help="Reuse an existing split.json")
    parser.add_argument("--split-seed", type=int, default=42)
    parser.add_argument("--stratify-split", action="store_true")
    parser.add_argument("--epochs-stage1", type=int, default=10)
    parser.add_argument("--epochs-stage2", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--prompt-dim", type=int, default=256)
    parser.add_argument("--hidden-dim", type=int, default=256)
    parser.add_argument("--max-steps", type=int, default=64)
    parser.add_argument("--reference-dropout", type=float, default=0.1)
    parser.add_argument("--detector-dropout", type=float, default=0.1)
    parser.add_argument("--projector-dropout", type=float, default=0.3)
    parser.add_argument("--no-projector-layernorm", action="store_true")
    parser.add_argument("--lr-stage1", type=float, default=1e-3)
    parser.add_argument("--lr-stage2", type=float, default=3e-4)
    parser.add_argument("--weight-decay-stage1", type=float, default=0.05)
    parser.add_argument("--weight-decay-stage2", type=float, default=0.0)
    parser.add_argument("--lambda-path", type=float, default=0.05)
    parser.add_argument("--lambda-rebound", type=float, default=0.2)
    parser.add_argument("--margin-quantile", type=float, default=0.8)
    parser.add_argument("--margin-ema", type=float, default=0.9)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--log-every", type=int, default=1)
    args = parser.parse_args()

    set_seed(args.seed)
    data = load_trace_dir(args.data_path)
    if len(data) < 3:
        raise ValueError("At least three traces are required")
    if args.split:
        split = _load_json(args.split)
    elif args.stratify_split:
        split = _stratified_split([int(item["label"]) for item in data], args.split_seed)
    else:
        split = _random_split(len(data), args.split_seed)
    _validate_indices(split, len(data))
    os.makedirs(args.out_dir, exist_ok=True)
    split_path = os.path.join(args.out_dir, "split.json")
    _save_json(split_path, split)

    prompt_dim = _infer_prompt_dim(data) if args.prompt_dim < 0 else args.prompt_dim
    cfg = DetectorConfig(
        prompt_dim=prompt_dim,
        hidden_dim=args.hidden_dim,
        max_steps=args.max_steps,
        reference_dropout=args.reference_dropout,
        detector_dropout=args.detector_dropout,
        projector_dropout=args.projector_dropout,
        projector_layernorm=not args.no_projector_layernorm,
        lambda_path=args.lambda_path,
        lambda_rebound=args.lambda_rebound,
        margin_quantile=args.margin_quantile,
        margin_ema=args.margin_ema,
        lr_stage1=args.lr_stage1,
        lr_stage2=args.lr_stage2,
        weight_decay_stage1=args.weight_decay_stage1,
        weight_decay_stage2=args.weight_decay_stage2,
        batch_size=args.batch_size,
        epochs_stage1=args.epochs_stage1,
        epochs_stage2=args.epochs_stage2,
        seed=args.seed,
    )
    cfg.validate()
    _save_json(os.path.join(args.out_dir, "detector_config.json"), asdict(cfg))

    train_data = [data[index] for index in split["train"]]
    val_data = [data[index] for index in split["val"]]
    detector = DynHDDetector(cfg, device=args.device)
    detector.train_stage1(train_data, verbose=args.verbose, log_every=args.log_every)
    detector.train_stage2(train_data, val_data, verbose=args.verbose, log_every=args.log_every)
    checkpoint = {
        "cfg": asdict(cfg),
        "reference": detector.reference.state_dict(),
        "deviation": detector.deviation.state_dict(),
        "prompt_projector": None
        if detector.prompt_projector is None
        else detector.prompt_projector.state_dict(),
    }
    checkpoint_path = os.path.join(args.out_dir, "detector.pt")
    torch.save(checkpoint, checkpoint_path)
    print(f"Saved checkpoint: {checkpoint_path}")


if __name__ == "__main__":
    main()
