from __future__ import annotations

import unicodedata
from typing import Optional, Set

import torch
import torch.nn.functional as F


STOPWORDS = frozenset(
    "a an and are as at be been being but by can could did do does doing for from had has have "
    "he her hers him his i if in into is it its itself may me might mine my no not of on or our "
    "ours she should so than that the their theirs them themselves then there these they this those "
    "to too under until up us was we were what when where which who whom why will with would you your yours".split()
)
BOILERPLATE = frozenset({"answer", "assistant", "question", "response", "user"})
BOUNDARY_MARKERS = ("<|", "|>", "[pad]", "[mask]", "[cls]", "[sep]", "<pad>", "<mask>")


class SemanticEntropyExtractor:
    """Construct the paper's ``[mean, max, top-k mean]`` evidence vector."""

    def __init__(
        self,
        tokenizer=None,
        top_k: int = 5,
    ) -> None:
        if top_k < 1:
            raise ValueError("top_k must be positive")
        self.tokenizer = tokenizer
        self.top_k = int(top_k)
        self.ignore_token_ids: Set[int] = set()
        self._semantic_cache: Dict[int, bool] = {}
        self._initialize_special_ids()

    def _add_id(self, token_id: Optional[int]) -> None:
        if isinstance(token_id, int) and token_id >= 0:
            self.ignore_token_ids.add(token_id)

    def _initialize_special_ids(self) -> None:
        if self.tokenizer is None:
            return
        for token_id in getattr(self.tokenizer, "all_special_ids", []) or []:
            self._add_id(token_id)
        for attribute in ("eos_token_id", "pad_token_id", "mask_token_id", "bos_token_id"):
            self._add_id(getattr(self.tokenizer, attribute, None))

    def _token_string(self, token_id: int) -> str:
        if self.tokenizer is None:
            return ""
        try:
            token = self.tokenizer.convert_ids_to_tokens(int(token_id))
        except Exception:
            token = None
        return token if isinstance(token, str) else ""

    @staticmethod
    def _normalize_token(token: str) -> str:
        normalized = token
        for marker in ("##", "\u2581", "\u0120", "\u010a"):
            normalized = normalized.replace(marker, " ")
        return normalized.strip().lower()

    @staticmethod
    def _is_lexical_noise(text: str) -> bool:
        if not text:
            return True
        return all(unicodedata.category(character)[0] in {"P", "S", "Z", "C"} for character in text)

    def _is_semantic_id(self, token_id: int) -> bool:
        cached = self._semantic_cache.get(token_id)
        if cached is not None:
            return cached
        if token_id in self.ignore_token_ids:
            self._semantic_cache[token_id] = False
            return False
        raw = self._token_string(token_id)
        normalized = self._normalize_token(raw)
        is_boundary = any(marker in raw.lower() for marker in BOUNDARY_MARKERS)
        is_subword_fragment = raw.startswith("##") or "\ufffd" in raw
        semantic = not (
            is_boundary
            or is_subword_fragment
            or self._is_lexical_noise(normalized)
            or normalized in STOPWORDS
            or normalized in BOILERPLATE
        )
        self._semantic_cache[token_id] = semantic
        return semantic

    def _keep_mask(self, predicted_ids: torch.Tensor) -> torch.Tensor:
        keep = torch.ones_like(predicted_ids, dtype=torch.bool)
        for token_id in torch.unique(predicted_ids).detach().cpu().tolist():
            if not self._is_semantic_id(int(token_id)):
                keep &= predicted_ids != int(token_id)
        return keep

    def _aggregate(self, logits: torch.Tensor) -> torch.Tensor:
        if logits.ndim == 3:
            logits = logits.squeeze(0)
        if logits.ndim != 2:
            raise ValueError(f"Expected logits [L, V], got {tuple(logits.shape)}")
        probabilities = F.softmax(logits.float(), dim=-1)
        entropies = -(probabilities * torch.log(probabilities.clamp_min(1e-10))).sum(dim=-1)
        predicted_ids = torch.argmax(logits, dim=-1)
        semantic = entropies[self._keep_mask(predicted_ids)]
        if semantic.numel() == 0:
            zero = torch.zeros((), dtype=entropies.dtype, device=entropies.device)
            return torch.stack([zero, zero, zero]).cpu()
        top_count = min(self.top_k, int(semantic.numel()))
        return torch.stack(
            [semantic.mean(), semantic.max(), torch.topk(semantic, top_count).values.mean()]
        ).cpu()

    @torch.no_grad()
    def step_from_logits(self, logits_step: torch.Tensor) -> torch.Tensor:
        return self._aggregate(logits_step)
