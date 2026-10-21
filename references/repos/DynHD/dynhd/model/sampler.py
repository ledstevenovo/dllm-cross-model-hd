from __future__ import annotations

from typing import Dict, List, Optional

import torch

from dynhd.features import SemanticEntropyExtractor

def get_num_transfer_tokens(mask_index: torch.Tensor, steps: int) -> torch.Tensor:
    """Distribute masked-token updates as evenly as possible across steps."""
    mask_num = mask_index.sum(dim=1, keepdim=True)
    base = mask_num // steps
    remainder = mask_num % steps

    num_transfer_tokens = torch.zeros(mask_index.size(0), steps, device=mask_index.device, dtype=torch.int64) + base
    for i in range(mask_index.size(0)):
        num_transfer_tokens[i, : int(remainder[i].item())] += 1
    return num_transfer_tokens


class LLaDASampler:
    """Run LLaDA denoising while collecting one evidence vector per step."""

    def __init__(self, model, num_steps: int = 64):
        self.llada = model
        self.steps = int(num_steps)
        self.device = model.device

    @torch.no_grad()
    def sample(
        self,
        prompt: str,
        gen_length: int = 128,
        feature_extractor: Optional[SemanticEntropyExtractor] = None,
    ) -> Dict[str, object]:

        prompt_ids = self.llada.encode(prompt)
        prompt_len = prompt_ids.shape[1]



        prompt_output = self.llada.forward(prompt_ids, output_hidden_states=True)
        hidden_states = getattr(prompt_output, "hidden_states", None)
        if not hidden_states or hidden_states[-1] is None:
            raise RuntimeError("LLaDA did not return hidden states for the prompt embedding")
        prompt_emb = hidden_states[-1].mean(dim=1).squeeze(0).detach().cpu()

        x_mask = torch.full((1, gen_length), self.llada.mask_id, device=self.device, dtype=torch.long)
        x = torch.cat([prompt_ids, x_mask], dim=1)

        mask_index = (x[:, prompt_len:] == self.llada.mask_id)
        num_transfer_tokens = get_num_transfer_tokens(mask_index, self.steps)

        results: Dict[str, object] = {
            "clean_text": "",
            "prompt_emb": prompt_emb,
            "features": None,
        }
        feat_list = []

        for i in range(self.steps):
            out = self.llada.forward(x, output_hidden_states=False)
            logits = out.logits  # [1, prompt+gen, V]
            logits_gen = logits[:, prompt_len:]  # [1, L, V]
            if feature_extractor is not None:
                feat_list.append(feature_extractor.step_from_logits(logits_gen))
            x = self._remask_step(x, logits, step_idx=i, num_transfer_tokens=num_transfer_tokens)

        if feature_extractor is not None:
            if feat_list:
                results["features"] = torch.stack(feat_list, dim=0)
        results["clean_text"] = self.llada.decode(x[:, prompt_len:])
        return results

    def _remask_step(self, x_curr: torch.Tensor, logits: torch.Tensor, step_idx: int, num_transfer_tokens: torch.Tensor) -> torch.Tensor:
        # NOTE (performance-critical):
        # Avoid materializing softmax over [seq, vocab] at every denoising step.
        # We only need confidence scores on currently-masked positions to select top-k tokens to "lock in".
        #
        # Compute:
        #   conf = max_softmax_prob = exp(max_logit - logsumexp(logits))
        # on masked positions only.
        x0 = torch.argmax(logits, dim=-1)  # [B, seq] (B==1 for our sampler)

        mask_id = self.llada.mask_id
        is_mask = (x_curr == mask_id)  # [B, seq]
        num_masks = int(is_mask.sum().item())
        if num_masks == 0:
            return x_curr

        k = int(num_transfer_tokens[0, step_idx].item())
        k = max(1, min(k, num_masks))

        # Select highest-confidence tokens within masked region.
        # Batch size is 1 in our sampling code path.
        bsz = int(logits.shape[0])
        if bsz != 1:
            # Fallback to older (slower) logic for unexpected batch sizes.
            probs = torch.softmax(logits, dim=-1)
            token_conf = torch.gather(probs, dim=-1, index=x0.unsqueeze(-1)).squeeze(-1)  # [B, seq]
            mask_conf = token_conf.clone()
            mask_conf[~is_mask] = -1e9
            _, topk_indices = torch.topk(mask_conf, k=k, dim=-1)
            update_mask = torch.zeros_like(x_curr, dtype=torch.bool)
            update_mask.scatter_(1, topk_indices, True)
        else:
            # Positions that are masked: [M]
            pos = torch.nonzero(is_mask[0], as_tuple=False).squeeze(-1)  # [M]
            logits_m = logits[0].index_select(0, pos)  # [M, V]
            # Use float32 for stability; returns [M]
            strategy = str(getattr(self.llada, "masking_strategy", "low_conf") or "low_conf").lower().strip()

            # score: higher => more likely to be "locked in" (kept / filled)
            if strategy == "random":
                score = torch.rand((int(pos.numel()),), device=logits_m.device, dtype=torch.float32)
            elif strategy == "topk":
                # margin between top-1 and top-2 logits (bigger margin => more confident)
                top2 = torch.topk(logits_m.float(), k=2, dim=-1).values  # [M,2]
                score = (top2[:, 0] - top2[:, 1]).to(dtype=torch.float32)  # [M]
            elif strategy == "entropy":
                # approximate entropy by top-K (cheap) => lower entropy => higher score
                K = int(getattr(self.llada, "entropy_topk", 50) or 50)
                K = max(8, min(K, int(logits_m.shape[-1])))
                top = torch.topk(logits_m.float(), k=K, dim=-1).values  # [M,K]
                logp = top - torch.logsumexp(top, dim=-1, keepdim=True)  # [M,K]
                p = torch.exp(logp)
                H = -(p * logp).sum(dim=-1)  # [M]
                score = (-H).to(dtype=torch.float32)
            else:
                # low_conf (default): max softmax prob (exact, but uses logsumexp only)
                max_logit, _ = torch.max(logits_m, dim=-1)
                logZ = torch.logsumexp(logits_m.float(), dim=-1).to(dtype=max_logit.dtype)
                score = torch.exp((max_logit - logZ).clamp(min=-50.0, max=0.0)).to(dtype=torch.float32)  # [M]

            # choose k positions with max score
            _, topk_local = torch.topk(score, k=k, dim=-1)  # [k]
            topk_indices = pos.index_select(0, topk_local).view(1, -1)  # [1,k]
            update_mask = torch.zeros_like(x_curr, dtype=torch.bool)
            update_mask.scatter_(1, topk_indices, True)

        x_new = x_curr.clone()
        x_new[update_mask] = x0[update_mask]
        return x_new
