"""Batch-one monotone diffusion collection. PyTorch is an inference-only dependency.

LLaDA follows the MIT-licensed reference loop (see THIRD_PARTY_NOTICES.md).
Dream uses its checkpoint's native diffusion_generate hooks: the logits hook
has ALREADY been shifted at the pinned revision. Observers return inputs intact.
"""
from dataclasses import dataclass
from contextlib import contextmanager
import numpy as np
import torch


@contextmanager
def count_forward_calls(model):
    counter = {'count': 0}
    def increment(module, args):
        counter['count'] += 1
    handle = model.register_forward_pre_hook(increment)
    try:
        yield counter
    finally:
        handle.remove()


@dataclass(frozen=True)
class DecodeConfig:
    gen_length: int = 64
    steps: int = 64
    block_size: int = 64
    temperature: float = 0.0

    def validate(self, family):
        if family not in ('llada', 'dream'):
            raise ValueError('unknown model family')
        if any(type(v) is not int or v < 1 for v in (self.gen_length, self.steps, self.block_size)):
            raise ValueError('length, steps and block_size must be positive integers')
        if self.temperature != 0:
            raise ValueError('collector-v1 supports greedy temperature=0 only')
        if self.gen_length % self.block_size or self.steps > self.gen_length:
            raise ValueError('invalid block/step schedule')
        blocks = self.gen_length // self.block_size
        if self.steps % blocks:
            raise ValueError('steps must be divisible by number of blocks')
        if family == 'dream' and self.block_size != self.gen_length:
            raise ValueError('Dream collector-v1 supports a single generation segment')


def align_generation_logits(logits, prompt_length, length, family, *, already_shifted=False):
    """Slice generation positions WITHOUT allocating a second full-vocabulary tensor.

    Raw Dream position j predicts token at j+1. The native hook, however,
    receives cat([raw[:,:1], raw[:,:-1]]) and must only be sliced.
    """
    if family not in ('llada', 'dream') or prompt_length < 1:
        raise ValueError('invalid alignment request')
    start = prompt_length - int(family == 'dream' and not already_shifted)
    result = logits[:, start:start+length]
    if result.ndim != 3 or result.shape[:2] != (1, length):
        raise ValueError('expected batch-one aligned generation logits')
    return result


@torch.no_grad()
def logits_statistics(logits, chunk_size=16):
    """FP32 reductions on-device, returning only O(L) arrays to CPU.

    Never mutate the original logits or retain a vocabulary tensor across steps.
    Negative infinity is allowed for zero-mass tokens; NaN/+inf/all-masked rows
    fail rather than manufacturing a finite entropy.
    """
    if logits.ndim != 3 or logits.shape[0] != 1 or chunk_size < 1:
        raise ValueError('expected [1,L,V] logits and positive chunk size')
    stats = {key: [] for key in ('entropy', 'top1_probability', 'top1_token')}
    for chunk in logits[0].split(chunk_size, dim=0):
        z = chunk.float()
        if torch.isnan(z).any() or torch.isposinf(z).any() or not torch.isfinite(z).any(dim=-1).all():
            raise ValueError('nonfinite predictive distribution')
        logp = torch.log_softmax(z, dim=-1)
        p = logp.exp()
        h = -torch.where(p > 0, p * logp, 0).sum(dim=-1)
        probability, token = p.max(dim=-1)
        for key, value in zip(stats, (h, probability, token)):
            stats[key].append(value.detach().cpu().numpy())
    return {key: np.concatenate(values) for key, values in stats.items()}


class TraceRecorder:
    def __init__(self, prompt_length, length, mask_id, family):
        self.prompt_length, self.length = prompt_length, length
        self.mask_id, self.family = mask_id, family
        self.rows = []
        self.pending = None

    def before(self, step, x, logits, *, already_shifted=False):
        if self.pending is not None or step != len(self.rows):
            raise ValueError('unexpected forward/hook order')
        before = x[:, self.prompt_length:].clone()
        aligned = align_generation_logits(logits, self.prompt_length, self.length,
                                           self.family, already_shifted=already_shifted)
        stats = logits_statistics(aligned)
        self.pending = (before, stats)

    def after(self, step, x):
        if self.pending is None or step != len(self.rows):
            raise ValueError('missing pre-reveal observation')
        before, stats = self.pending
        after = x[:, self.prompt_length:]
        mask = before.eq(self.mask_id)
        if ((~mask) & after.ne(before)).any():
            raise ValueError('non-monotone generation: an already revealed token changed')
        stats['mask_before'] = mask[0].cpu().numpy()
        stats['revealed'] = (mask & after.ne(self.mask_id))[0].cpu().numpy()
        self.rows.append(stats)
        self.pending = None

    def arrays(self, final):
        if self.pending is not None or not self.rows:
            raise ValueError('incomplete observation sequence')
        generated = final[0, self.prompt_length:]
        if generated.eq(self.mask_id).any():
            raise ValueError('generation ended with MASK tokens; trace-v1 cannot claim completion')
        return {**{key: np.stack([row[key] for row in self.rows]) for key in self.rows[0]},
                'final_tokens': generated.detach().cpu().numpy()}


@torch.no_grad()
def _llada_generate(model, ids, cfg, mask_id, recorder):
    prompt_length = ids.shape[1]
    x = torch.full((1, prompt_length+cfg.gen_length), mask_id, device=ids.device, dtype=torch.long)
    x[:, :prompt_length] = ids
    blocks = cfg.gen_length // cfg.block_size
    per_block = cfg.steps // blocks
    for block in range(blocks):
        start = prompt_length + block * cfg.block_size
        # Matches upstream uniform integer allocation including the remainder.
        base, remainder = divmod(cfg.block_size, per_block)
        for i in range(per_block):
            step = block * per_block + i
            mask = x.eq(mask_id)
            logits = model(x).logits
            if recorder is not None:
                recorder.before(step, x, logits)
            predicted = logits.argmax(dim=-1)
            probabilities = torch.softmax(logits, dim=-1)
            confidence = probabilities.gather(-1, predicted.unsqueeze(-1)).squeeze(-1)
            confidence[:, start+cfg.block_size:] = -torch.inf
            confidence = torch.where(mask, confidence, -torch.inf)
            count = base + int(i < remainder)
            selected = torch.topk(confidence, count, dim=-1).indices
            x.scatter_(1, selected, predicted.gather(1, selected))
            if recorder is not None:
                recorder.after(step, x)
            del logits, probabilities, confidence, predicted
    return x


@torch.no_grad()
def collect(model, input_ids, cfg, family, mask_id, *, observe=True):
    """Use the SAME actual decode path with observation on/off (no mock trace shortcut)."""
    cfg.validate(family)
    if input_ids.ndim != 2 or input_ids.shape[0] != 1 or not input_ids.shape[1]:
        raise ValueError('collector-v1 requires a nonempty batch-one prompt')
    if input_ids.eq(mask_id).any():
        raise ValueError('prompt contains MASK ID; cannot preserve prompt semantics')
    recorder = TraceRecorder(input_ids.shape[1], cfg.gen_length, mask_id, family) if observe else None
    if family == 'llada':
        final = _llada_generate(model, input_ids, cfg, mask_id, recorder)
    else:
        def logits_hook(step, x, logits):
            if logits.dtype == torch.float16:
                raise ValueError('Dream native entropy ranking is unsafe in FP16; use BF16/FP32 until the sampler is re-audited')
            if recorder is not None:
                recorder.before(step, x, logits, already_shifted=True)
            return logits

        def tokens_hook(step, x, logits):
            if step is not None and recorder is not None:
                recorder.after(step, x)
            return x

        final = model.diffusion_generate(
            input_ids, attention_mask=torch.ones_like(input_ids),
            max_new_tokens=cfg.gen_length, steps=cfg.steps, temperature=0.,
            alg='entropy', alg_temp=0., top_p=None, top_k=None,
            output_history=False, return_dict_in_generate=False,
            generation_logits_hook_func=logits_hook, generation_tokens_hook_func=tokens_hook)
    if not torch.equal(final[:, :input_ids.shape[1]], input_ids):
        raise ValueError('sampler changed the prompt')
    return final, recorder.arrays(final) if recorder is not None else None
