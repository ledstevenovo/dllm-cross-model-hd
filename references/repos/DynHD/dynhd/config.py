from __future__ import annotations

from typing import Any, Dict

import yaml


def load_yaml_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    if not isinstance(cfg, dict):
        raise ValueError(f"Config root must be a dict, got {type(cfg)}")
    return cfg

