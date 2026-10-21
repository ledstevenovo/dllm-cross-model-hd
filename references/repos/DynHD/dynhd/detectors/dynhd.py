from __future__ import annotations

import copy
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


class ReferenceTrajectoryGenerator(nn.Module):
    """Question- and timestep-conditioned factual evidence generator."""

    def __init__(
        self,
        prompt_dim: int,
        hidden_dim: int,
        max_steps: int,
        output_dim: int,
        dropout: float,
    ) -> None:
        super().__init__()
        self.max_steps = int(max_steps)
        self.prompt_encoder = nn.Sequential(
            nn.Linear(prompt_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.time_embedding = nn.Embedding(max_steps, hidden_dim)
        self.generator = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, prompt_emb: torch.Tensor, num_steps: int) -> torch.Tensor:
        if num_steps > self.max_steps:
            raise ValueError(f"num_steps={num_steps} exceeds max_steps={self.max_steps}")
        batch_size = prompt_emb.shape[0]
        prompt = self.prompt_encoder(prompt_emb).unsqueeze(1).expand(-1, num_steps, -1)
        time_ids = torch.arange(num_steps, device=prompt_emb.device)
        time = self.time_embedding(time_ids).unsqueeze(0).expand(batch_size, -1, -1)
        return self.generator(torch.cat([prompt, time], dim=-1))


class DeviationDetector(nn.Module):
    """Shared step MLP, temporal attention, and binary classifier from Eq. 6."""

    def __init__(self, input_dim: int, hidden_dim: int, dropout: float) -> None:
        super().__init__()
        self.step_encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )
        self.attention = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1),
        )
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, max(1, hidden_dim // 2)),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(max(1, hidden_dim // 2), 1),
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        hidden = self.step_encoder(x)
        weights = F.softmax(self.attention(hidden).squeeze(-1), dim=1)
        pooled = (hidden * weights.unsqueeze(-1)).sum(dim=1)
        return self.classifier(pooled).squeeze(-1), weights


@dataclass
class DetectorConfig:
    prompt_dim: int = 256
    hidden_dim: int = 256
    max_steps: int = 64
    reference_dropout: float = 0.1
    detector_dropout: float = 0.1
    projector_dropout: float = 0.3
    projector_layernorm: bool = True
    lambda_path: float = 0.05
    lambda_rebound: float = 0.2
    margin_quantile: float = 0.8
    margin_ema: float = 0.9
    lr_stage1: float = 1e-3
    lr_stage2: float = 3e-4
    weight_decay_stage1: float = 0.05
    weight_decay_stage2: float = 0.0
    batch_size: int = 32
    epochs_stage1: int = 10
    epochs_stage2: int = 30
    seed: int = 42

    @property
    def obs_dim(self) -> int:
        return 3

    def validate(self) -> None:
        if self.prompt_dim < 1 or self.hidden_dim < 1 or self.max_steps < 1:
            raise ValueError("prompt_dim, hidden_dim, and max_steps must be positive")
        if self.batch_size < 1 or self.epochs_stage1 < 1 or self.epochs_stage2 < 1:
            raise ValueError("batch size and epoch counts must be positive")
        if not 0.0 <= self.margin_quantile <= 1.0:
            raise ValueError("margin_quantile must be in [0, 1]")
        if not 0.0 <= self.margin_ema < 1.0:
            raise ValueError("margin_ema must be in [0, 1)")


class DynHDDetector(nn.Module):
    """Two-stage DynHD reference-trajectory and deviation detector."""

    def __init__(self, cfg: DetectorConfig, device: str = "cuda") -> None:
        super().__init__()
        cfg.validate()
        self.cfg = cfg
        selected = torch.device(device if device == "cpu" or torch.cuda.is_available() else "cpu")
        self.device = selected
        self.prompt_projector: Optional[nn.Module] = None
        self.reference = ReferenceTrajectoryGenerator(
            cfg.prompt_dim,
            cfg.hidden_dim,
            cfg.max_steps,
            cfg.obs_dim,
            cfg.reference_dropout,
        ).to(selected)
        self.deviation = DeviationDetector(
            input_dim=cfg.obs_dim * 3,
            hidden_dim=cfg.hidden_dim,
            dropout=cfg.detector_dropout,
        ).to(selected)
        self._margin_path: Optional[float] = None
        self._margin_rebound: Optional[float] = None

    def _validate_data(self, data: Sequence[Dict]) -> None:
        if not data:
            raise ValueError("Trace collection is empty")
        for position, item in enumerate(data):
            features = item.get("features")
            if not isinstance(features, torch.Tensor) or features.ndim != 2:
                raise ValueError(f"Trace {position} must contain a [T, D] features tensor")
            if features.shape[0] < 1 or features.shape[1] != self.cfg.obs_dim:
                raise ValueError(f"Trace {position} must have shape [T, 3], got {tuple(features.shape)}")
            if int(item.get("label", -1)) not in (0, 1):
                raise ValueError(f"Trace {position} has an invalid binary label")
            if not isinstance(item.get("prompt_emb"), torch.Tensor):
                raise ValueError(f"Trace {position} is missing its prompt_emb tensor")

    def ensure_prompt_projector(self, data: Sequence[Dict]) -> None:
        if self.prompt_projector is not None:
            return
        dimensions = {
            int(item["prompt_emb"].numel())
            for item in data
            if isinstance(item.get("prompt_emb"), torch.Tensor)
        }
        if not dimensions:
            return
        if len(dimensions) != 1:
            raise ValueError(f"Inconsistent prompt embedding sizes: {sorted(dimensions)}")
        input_dim = dimensions.pop()
        if input_dim == self.cfg.prompt_dim:
            return
        layers: List[nn.Module] = [nn.Linear(input_dim, self.cfg.prompt_dim)]
        if self.cfg.projector_layernorm:
            layers.append(nn.LayerNorm(self.cfg.prompt_dim))
        if self.cfg.projector_dropout > 0:
            layers.append(nn.Dropout(self.cfg.projector_dropout))
        self.prompt_projector = nn.Sequential(*layers).to(self.device)

    def _prompt_batch(self, batch: Sequence[Dict]) -> torch.Tensor:
        raw = torch.stack([item["prompt_emb"].flatten().float() for item in batch]).to(self.device)
        return self.prompt_projector(raw) if self.prompt_projector is not None else raw

    def _make_batch(self, batch: Sequence[Dict]) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        steps = min(self.cfg.max_steps, *(int(item["features"].shape[0]) for item in batch))
        observations = torch.stack(
            [item["features"][:steps].float() for item in batch]
        ).to(self.device)
        labels = torch.tensor([int(item["label"]) for item in batch], dtype=torch.float32, device=self.device)
        prompts = self._prompt_batch(batch)
        references = self.reference(prompts, steps)
        return observations, references, labels

    @staticmethod
    def _detector_inputs(
        observations: torch.Tensor,
        references: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        velocity = torch.zeros_like(observations)
        velocity[:, 1:] = observations[:, 1:] - observations[:, :-1]
        inputs = torch.cat([observations, references, velocity], dim=-1)
        path = torch.abs(observations - references).sum(dim=-1)
        rebound = F.relu(velocity).square().sum(dim=-1)
        return inputs, path, rebound

    def _batches(self, data: Sequence[Dict], *, shuffle: bool, epoch: int) -> Iterable[List[Dict]]:
        indices = list(range(len(data)))
        if shuffle:
            random.Random(self.cfg.seed + epoch).shuffle(indices)
        size = self.cfg.batch_size
        for start in range(0, len(indices), size):
            yield [data[index] for index in indices[start : start + size]]

    @staticmethod
    def _set_trainable(module: nn.Module, enabled: bool) -> None:
        module.train(enabled)
        for parameter in module.parameters():
            parameter.requires_grad_(enabled)

    def train_stage1(
        self,
        train_data: Sequence[Dict],
        *,
        verbose: bool = False,
        log_every: int = 1,
    ) -> None:
        self._validate_data(train_data)
        factual = [item for item in train_data if int(item["label"]) == 0]
        if not factual:
            raise ValueError("Stage one requires at least one factual trace")
        self.ensure_prompt_projector(train_data)
        self._set_trainable(self.reference, True)
        if self.prompt_projector is not None:
            self._set_trainable(self.prompt_projector, True)
        parameters = list(self.reference.parameters())
        if self.prompt_projector is not None:
            parameters += list(self.prompt_projector.parameters())
        optimizer = torch.optim.AdamW(
            parameters,
            lr=self.cfg.lr_stage1,
            weight_decay=self.cfg.weight_decay_stage1,
        )
        for epoch in range(self.cfg.epochs_stage1):
            losses = []
            for batch in self._batches(factual, shuffle=True, epoch=epoch):
                optimizer.zero_grad(set_to_none=True)
                observations, references, _ = self._make_batch(batch)
                loss = F.smooth_l1_loss(references, observations)
                loss.backward()
                optimizer.step()
                losses.append(float(loss.detach().cpu()))
            if verbose and (epoch % max(1, log_every) == 0 or epoch + 1 == self.cfg.epochs_stage1):
                print(f"stage1 epoch={epoch + 1} loss={np.mean(losses):.6f}")

    def _update_margin(self, current: Optional[float], factual_scores: torch.Tensor) -> Optional[float]:
        if factual_scores.numel() == 0:
            return current
        value = float(torch.quantile(factual_scores.detach(), self.cfg.margin_quantile).cpu())
        if current is None:
            return value
        decay = self.cfg.margin_ema
        return decay * current + (1.0 - decay) * value

    @staticmethod
    def _margin_loss(scores: torch.Tensor, labels: torch.Tensor, margin: float) -> torch.Tensor:
        return ((1.0 - labels) * scores + labels * F.relu(margin - scores)).mean()

    def train_stage2(
        self,
        train_data: Sequence[Dict],
        val_data: Optional[Sequence[Dict]] = None,
        *,
        verbose: bool = False,
        log_every: int = 1,
    ) -> None:
        self._validate_data(train_data)
        self._set_trainable(self.reference, False)
        if self.prompt_projector is not None:
            self._set_trainable(self.prompt_projector, False)
        self._set_trainable(self.deviation, True)
        optimizer = torch.optim.AdamW(
            self.deviation.parameters(),
            lr=self.cfg.lr_stage2,
            weight_decay=self.cfg.weight_decay_stage2,
        )
        best_state = None
        best_auroc = float("-inf")
        for epoch in range(self.cfg.epochs_stage2):
            self.deviation.train()
            losses = []
            for batch in self._batches(train_data, shuffle=True, epoch=epoch):
                optimizer.zero_grad(set_to_none=True)
                observations, references, labels = self._make_batch(batch)
                references = references.detach()
                inputs, path, rebound = self._detector_inputs(observations, references)
                logits, weights = self.deviation(inputs)
                path_scores = (weights * path).sum(dim=1)
                rebound_scores = (weights * rebound).sum(dim=1)
                factual = labels == 0
                self._margin_path = self._update_margin(self._margin_path, path_scores[factual])
                self._margin_rebound = self._update_margin(self._margin_rebound, rebound_scores[factual])
                classification = F.binary_cross_entropy_with_logits(logits, labels)
                path_loss = self._margin_loss(path_scores, labels, self._margin_path or 0.0)
                rebound_loss = self._margin_loss(rebound_scores, labels, self._margin_rebound or 0.0)
                loss = classification + self.cfg.lambda_path * path_loss + self.cfg.lambda_rebound * rebound_loss
                loss.backward()
                optimizer.step()
                losses.append(float(loss.detach().cpu()))
            val_auroc = None
            if val_data:
                labels = np.asarray([int(item["label"]) for item in val_data], dtype=np.int64)
                if np.unique(labels).size > 1:
                    val_auroc = float(roc_auc_score(labels, self.predict_proba(val_data)))
                    if val_auroc > best_auroc:
                        best_auroc = val_auroc
                        best_state = copy.deepcopy(self.deviation.state_dict())
            if verbose and (epoch % max(1, log_every) == 0 or epoch + 1 == self.cfg.epochs_stage2):
                suffix = "" if val_auroc is None else f" val_auroc={val_auroc:.4f}"
                print(f"stage2 epoch={epoch + 1} loss={np.mean(losses):.6f}{suffix}")
        if best_state is not None:
            self.deviation.load_state_dict(best_state)

    @torch.no_grad()
    def predict_proba(self, data: Sequence[Dict]) -> np.ndarray:
        self._validate_data(data)
        self.reference.eval()
        if self.prompt_projector is not None:
            self.prompt_projector.eval()
        self.deviation.eval()
        probabilities: List[float] = []
        for batch in self._batches(data, shuffle=False, epoch=0):
            observations, references, _ = self._make_batch(batch)
            inputs, _, _ = self._detector_inputs(observations, references)
            logits, _ = self.deviation(inputs)
            probabilities.extend(torch.sigmoid(logits).cpu().tolist())
        return np.asarray(probabilities, dtype=np.float32)
