"""CPU fixtures for the DynHD adapter acceptance (never enters formal data).

FixtureSampler mirrors the upstream sampler interface
(``tokenizer.apply_chat_template/encode/decode``; ``sample(...) -> {clean_text, features, prompt_emb}``)
and injects deterministic shape/label/save/abort faults from a fault plan.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

import torch

FEATURE_DIM = 3


class AbortRun(BaseException):
    """Simulated interruption: not caught by the upstream per-item ``except Exception``."""


class Context:
    """Tracks the item currently being processed (set by the patched prompt builders)."""

    item: Optional[Dict[str, Any]] = None
    provisional_kind: Optional[str] = None

    @classmethod
    def set_item(cls, item: Dict[str, Any]) -> None:
        cls.item = item
        cls.provisional_kind = None

    @classmethod
    def current(cls) -> Dict[str, Any]:
        if cls.item is None:
            raise RuntimeError("no current item bound; prompt builder was not called")
        return cls.item

    @classmethod
    def current_id(cls) -> str:
        return str(cls.item["id"]) if cls.item else "<unknown>"


class FixtureTokenizer:
    """Minimal tokenizer surface used by the upstream sampler and extractor."""

    all_special_ids = [0]
    eos_token_id = 0
    pad_token_id = 0
    mask_token_id = 126336

    def apply_chat_template(self, messages, tokenize: bool = False, add_generation_prompt: bool = True) -> str:
        text = "\n".join(f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages)
        return f"<fixture>{text}<assistant>"

    def encode(self, text: str) -> torch.Tensor:
        size = 4 + len(str(text)) % 8
        return torch.arange(size, dtype=torch.long).unsqueeze(0)

    def decode(self, ids: torch.Tensor) -> str:
        return "fixture decoded text"

    def convert_ids_to_tokens(self, token_id: int) -> str:
        return f"tok{token_id}"


class FixtureModel:
    def __init__(self, steps: int = 64):
        self.tokenizer = FixtureTokenizer()
        self.steps = int(steps)


class FixtureSampler:
    def __init__(self, model: FixtureModel, *, steps: int, fault_plan: Optional[Dict[str, Any]] = None):
        self.model = model
        self.tokenizer = model.tokenizer
        self.steps = int(steps)
        self.fault_plan = fault_plan or {}

    def sample(self, prompt=None, gen_length: int = 64, feature_extractor=None,
               messages=None, prompt_emb_messages=None):
        item = Context.current()
        plan = self.fault_plan.get("per_item", {}).get(item["id"], {})
        if plan.get("abort"):
            raise AbortRun(f"fixture abort before item {item['id']}")
        if plan.get("shape_failure"):
            actual_t = max(self.steps - 1, 1)
            features = torch.zeros((actual_t, FEATURE_DIM), dtype=torch.float32)
            return {"clean_text": "shape failure fixture", "features": features,
                    "prompt_emb": torch.zeros(8), "actual_T": actual_t}
        features = torch.zeros((self.steps, FEATURE_DIM), dtype=torch.float32)
        for t in range(self.steps):
            for d in range(FEATURE_DIM):
                features[t, d] = float((t + d + 1) % 7) / 7.0
        text = plan.get("clean_text") or f"fixture answer for {item['id']}"
        return {"clean_text": text, "features": features,
                "prompt_emb": torch.ones(8, dtype=torch.float32), "actual_T": self.steps}


class FixtureLabeler:
    """Deterministic labels from the fault plan (engineering data only)."""

    def __init__(self, fault_plan: Optional[Dict[str, Any]] = None):
        self.fault_plan = fault_plan or {}

    def label_one(self, question=None, ground_truth=None, generated=None) -> Dict[str, Any]:
        item = Context.current()
        plan = self.fault_plan.get("per_item", {}).get(item["id"], {})
        if plan.get("label_failure"):
            raise RuntimeError(f"fixture label failure for {item['id']}")
        labels = self.fault_plan.get("labels", {})
        label = int(labels.get(item["id"], 0))
        return {"label": label, "rationale": "fixture plan label",
                "provisional": False, "test_fixture": True}
