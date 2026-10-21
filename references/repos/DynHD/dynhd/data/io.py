import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch


def _coerce_features(features: torch.Tensor) -> torch.Tensor:
    """Normalize a saved evidence trajectory to a floating-point matrix."""
    if not isinstance(features, torch.Tensor):
        features = torch.tensor(features)
    if features.dim() != 2:
        raise ValueError(f"features must be 2D [T, D], got {tuple(features.shape)}")
    if int(features.shape[1]) < 1:
        raise ValueError(f"features must have D>=1, got {tuple(features.shape)}")
    return features.float()


def load_trace(path: str) -> Dict:
    data = torch.load(path, map_location="cpu", weights_only=True)
    if "features" in data:
        data["features"] = _coerce_features(data["features"])
    if "prompt_emb" in data and data["prompt_emb"] is not None:
        if not isinstance(data["prompt_emb"], torch.Tensor):
            data["prompt_emb"] = torch.tensor(data["prompt_emb"])
        data["prompt_emb"] = data["prompt_emb"].float()
    return data


def load_trace_dir(data_dir: str, suffix: str = ".pt") -> List[Dict]:
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"data_dir not found: {data_dir}")
    files = sorted([f for f in os.listdir(data_dir) if f.endswith(suffix)])
    out: List[Dict] = []
    for f in files:
        out.append(load_trace(os.path.join(data_dir, f)))
    return out


def save_trace(path: str, *, features: torch.Tensor, label: int, meta: Dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "features": _coerce_features(features).cpu(),
        "label": int(label),
        "meta": meta,
    }
    torch.save(data, path)


def save_trace_with_prompt_emb(path: str, *, features: torch.Tensor, label: int, meta: Dict, prompt_emb: Optional[torch.Tensor]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "features": _coerce_features(features).cpu(),
        "label": int(label),
        "meta": meta,
        "prompt_emb": None if prompt_emb is None else prompt_emb.detach().cpu().float(),
    }
    torch.save(data, path)


def create_splits(
    data_list: List[Dict],
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-6:
        raise ValueError("train/val/test ratios must sum to 1.0")
    n = len(data_list)
    if n == 0:
        return [], [], []
    idx = np.arange(n)
    rng = np.random.default_rng(seed)
    rng.shuffle(idx)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    train = [data_list[i] for i in idx[:n_train]]
    val = [data_list[i] for i in idx[n_train : n_train + n_val]]
    test = [data_list[i] for i in idx[n_train + n_val :]]
    return train, val, test
