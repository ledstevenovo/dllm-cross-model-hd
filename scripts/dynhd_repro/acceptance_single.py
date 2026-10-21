#!/usr/bin/env python
"""Step-2 acceptance checks in the DynHD sampling path.

1. Hook alignment: verify the logits that reach the evidence extractor equal the native model
   output after the documented shift (Dream: cat([raw[:,:1], raw[:,:-1]]); LLaDA: identity).
2. Observation non-interference: same item, same seed, feature_extractor=None vs enabled must
   produce identical final token ids.
3. Decode unit check: controlled token sequences must be cut at the first EOS/mask token.

Writes/merges reports/dynhd_singleq.json.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO / "references/repos/DynHD"))

import torch  # noqa: E402

import common  # noqa: E402
from dynhd.features import SemanticEntropyExtractor  # noqa: E402
from dynhd.model import DreamDiffusionSampler, DreamModel, LLaDAModel, LLaDASampler  # noqa: E402

OUT = REPO / "reports/dynhd_singleq.json"


def load_item(subset: Path, index: int):
    rows = [json.loads(line) for line in subset.read_text(encoding="utf-8").splitlines() if line.strip()]
    return rows[index]


def build_model_and_sampler(model: str, config_path: Path, steps: int):
    config = json.loads(json.dumps(__import__("yaml").safe_load(config_path.read_text())))
    model_path = config["model"]["model_path"]
    inference = config.get("inference", {})
    if model == "dream":
        dream = DreamModel(model_path, device="cuda")
        common.coerce_dream_logits_hook(dream)
        sampler = DreamDiffusionSampler(
            dream, num_steps=steps, temperature=float(inference.get("temperature", 0.0)),
            top_p=inference.get("top_p"), top_k=inference.get("top_k"),
            alg=str(inference.get("dream_alg", "entropy")), alg_temp=float(inference.get("alg_temp", 0.0)))
        return dream, sampler
    llada = LLaDAModel(model_path, device="cuda")
    return llada, LLaDASampler(llada, num_steps=steps)


def check_alignment(model: str, wrapper_model, sampler, item, gen_length: int, steps_checked: int) -> dict:
    """Capture raw model logits and extractor logits for the first steps and compare."""
    tokenizer = wrapper_model.tokenizer
    messages = [{"role": "user", "content": item["prompt"]}]
    raw_calls, captured = [], []
    original_hf_forward = wrapper_model.model.forward

    def recording_forward(*args, **kwargs):
        out = original_hf_forward(*args, **kwargs)
        if kwargs.get("output_hidden_states") is not True and len(raw_calls) < steps_checked:
            raw_calls.append(out.logits.detach().float().cpu())
        return out

    extractor = SemanticEntropyExtractor(tokenizer=tokenizer, top_k=5)
    original_step = extractor.step_from_logits

    def recording_step(logits_step):
        if len(captured) < steps_checked:
            captured.append(logits_step.detach().float().cpu())
        return original_step(logits_step)

    extractor.step_from_logits = recording_step
    wrapper_model.model.forward = recording_forward
    try:
        if model == "dream":
            sampler.sample(messages, gen_length=gen_length, feature_extractor=extractor,
                           prompt_emb_messages=[{"role": "user", "content": item["question"]}])
        else:
            rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            sampler.sample(rendered, gen_length=gen_length, feature_extractor=extractor)
    finally:
        wrapper_model.model.forward = original_hf_forward
        extractor.step_from_logits = original_step

    results = []
    for index, (raw, got) in enumerate(zip(raw_calls, captured)):
        total_len = raw.shape[1]
        prompt_len = total_len - gen_length
        if model == "dream":
            aligned = torch.cat([raw[:, :1], raw[:, :-1]], dim=1)[:, prompt_len:]
            rule = "cat([raw[:,:1], raw[:,:-1]])[:, prompt_len:]"
        else:
            aligned = raw[:, prompt_len:]
            rule = "raw[:, prompt_len:] (identity)"
        exact = torch.equal(aligned, got)
        max_abs = float((aligned - got).abs().max()) if aligned.shape == got.shape else None
        results.append({"step": index, "exact_equal": exact, "max_abs_diff": max_abs,
                        "shape_raw": list(raw.shape), "shape_extractor": list(got.shape)})
    return {"model": model, "rule": rule if raw_calls else None,
            "steps_checked": len(results), "steps_requested": steps_checked,
            "exact_matches": sum(1 for r in results if r["exact_equal"]), "results": results}


def final_tokens_with_and_without_extractor(model: str, wrapper_model, sampler, item, gen_length: int,
                                            mask_id: int) -> dict:
    tokenizer = wrapper_model.tokenizer
    captured = {}

    def run_once(with_extractor: bool):
        states = []

        if model == "dream":
            original_generate = wrapper_model.model.diffusion_generate

            def capturing_generate(*args, **kwargs):
                out = original_generate(*args, **kwargs)
                captured["sequences"] = out.sequences.detach().cpu()
                return out

            wrapper_model.model.diffusion_generate = capturing_generate
            try:
                messages = [{"role": "user", "content": item["prompt"]}]
                sampler.sample(messages, gen_length=gen_length,
                               feature_extractor=SemanticEntropyExtractor(tokenizer=tokenizer, top_k=5) if with_extractor else None,
                               prompt_emb_messages=[{"role": "user", "content": item["question"]}])
            finally:
                wrapper_model.model.diffusion_generate = original_generate
            return captured["sequences"]
        original_remask = sampler._remask_step

        def recording_remask(*args, **kwargs):
            out = original_remask(*args, **kwargs)
            states.append(out.detach().cpu())
            return out

        sampler._remask_step = recording_remask
        try:
            rendered = tokenizer.apply_chat_template([{"role": "user", "content": item["prompt"]}],
                                                     tokenize=False, add_generation_prompt=True)
            sampler.sample(rendered, gen_length=gen_length,
                           feature_extractor=SemanticEntropyExtractor(tokenizer=tokenizer, top_k=5) if with_extractor else None)
        finally:
            sampler._remask_step = original_remask
        return states[-1]

    with_extractor = run_once(True)
    without_extractor = run_once(False)
    if model == "llada":
        prompt_len = with_extractor.shape[1] - gen_length
        with_extractor = with_extractor[:, prompt_len:]
        without_extractor = without_extractor[:, prompt_len:]
    same_tokens = torch.equal(with_extractor, without_extractor)
    same_text = True
    prompt_len = without_extractor.shape[1] - gen_length
    if model == "dream":
        text_a = tokenizer.decode(with_extractor[0, prompt_len:].tolist(), skip_special_tokens=True)
        text_b = tokenizer.decode(without_extractor[0, prompt_len:].tolist(), skip_special_tokens=True)
        same_text = text_a == text_b
    gen_ids = (with_extractor[0, prompt_len:] if model == "dream" else with_extractor[0]).tolist()
    eos = tokenizer.eos_token_id
    first_eos = next((i for i, token in enumerate(gen_ids) if token == eos), None)
    first_mask = next((i for i, token in enumerate(gen_ids) if mask_id is not None and token == mask_id), None)
    if model == "dream":
        cut = min([p for p in (first_eos, first_mask) if p is not None], default=len(gen_ids))
        rule = "cut at first EOS or mask, then skip_special_tokens"
    else:
        cut = None
        rule = "mask dropped in place, EOS removed by skip_special_tokens (no positional cut)"
    analysis = {
        "identical_tokens": same_tokens, "identical_text": same_text,
        "generated_token_count": len(gen_ids), "first_eos_position": first_eos,
        "first_mask_position": first_mask, "upstream_decode_cut_position": cut,
        "eos_observed": first_eos is not None, "mask_observed": first_mask is not None,
        "decode_rule": rule,
    }
    if first_eos is None:
        analysis["eos_status"] = "not covered by this probe; controlled-token decode unit check supplied"
    return analysis


def decode_unit_check() -> dict:
    """Controlled token sequences: verify each upstream decode rule.

    LLaDA: mask ids are dropped wherever they appear; EOS/EOT are removed by
    ``skip_special_tokens`` (no positional cut). Dream: cut at the first EOS or mask,
    then ``skip_special_tokens``.
    """
    from transformers import AutoTokenizer
    from dynhd.model import DreamModel, LLaDAModel

    out = {}
    cases = [
        ("llada", "GSAI-ML/LLaDA-8B-Instruct",
         "/root/autodl-tmp/hf-cache/hub/models--GSAI-ML--LLaDA-8B-Instruct/snapshots/08b83a6feb34df1a6011b80c3c00c7563e963b07"),
        ("dream", "Dream-org/Dream-v0-Instruct-7B",
         "/root/autodl-tmp/hf-cache/hub/models--Dream-org--Dream-v0-Instruct-7B/snapshots/05334cb9faaf763692dcf9d8737c642be2b2a6ae"),
    ]
    for model, name, path in cases:
        tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True, local_files_only=True)
        base = tokenizer.encode("The capital of France is Paris", add_special_tokens=False)
        eos = tokenizer.eos_token_id
        mask = getattr(tokenizer, "mask_token_id", None)
        if mask is None:  # LLaDA keeps the mask id in the model config, not the tokenizer
            try:
                mask = json.loads((Path(path) / "config.json").read_text()).get("mask_token_id")
            except Exception:
                mask = None
        row = {"tokenizer": name, "eos_id": eos, "mask_id": mask,
               "rule": ("mask dropped anywhere; EOS/EOT removed by skip_special_tokens"
                        if model == "llada" else "cut at first EOS or mask, then skip_special_tokens")}
        if model == "llada":
            decoder = LLaDAModel.__new__(LLaDAModel)
            decoder.tokenizer = tokenizer
            decoder.mask_id = int(mask)

            def decode(ids):
                return LLaDAModel.decode(decoder, torch.tensor([ids]))
            plain = decode(base)
            row["mask_dropped_in_place"] = decode(base[:2] + [mask] + base[2:]) == plain
            row["eos_removed_by_skip_special"] = decode(base[:2] + [eos] + base[2:]) == plain
            row["keeps_text_after_eos"] = decode(base + [eos] + base) != plain
        else:
            decoder = DreamModel.__new__(DreamModel)
            decoder.tokenizer = tokenizer

            def decode(ids):
                return DreamModel.decode(decoder, torch.tensor([ids]))
            plain = decode(base)
            row["cut_at_eos"] = decode(base + [eos] + base) == plain
            row["cut_at_mask"] = decode(base + [mask] + base) == plain
        row["base_text"] = plain
        out[model] = row
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["llada", "dream"], required=True)
    parser.add_argument("--subset", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--gen-length", type=int, default=64)
    parser.add_argument("--steps", type=int, default=64)
    parser.add_argument("--hook-steps", type=int, default=5)
    parser.add_argument("--out", default=str(OUT))
    args = parser.parse_args()

    item = load_item(Path(args.subset), 0)
    evidence = {"model": args.model, "item": {"sample_id": item["sample_id"], "role": item.get("acceptance_role"),
                                              "rendered_prompt_tokens": item.get("rendered_prompt_tokens")},
                "started_utc": common.utc_now()}
    started = time.perf_counter()
    wrapper_model, sampler = build_model_and_sampler(args.model, Path(args.config), args.steps)
    evidence["load_seconds"] = round(time.perf_counter() - started, 3)
    evidence["device"] = str(next(wrapper_model.model.parameters()).device)
    evidence["dtype"] = str(next(wrapper_model.model.parameters()).dtype)
    if torch.cuda.is_available():
        free_bytes, total_bytes = torch.cuda.mem_get_info()
        evidence["device_memory_after_load"] = {"free_bytes": int(free_bytes), "total_bytes": int(total_bytes)}
    tokenizer = wrapper_model.tokenizer
    mask_id = getattr(tokenizer, "mask_token_id", None)
    if mask_id is None:  # LLaDA keeps the mask id in the model config
        model_path = __import__("yaml").safe_load(Path(args.config).read_text())["model"]["model_path"]
        mask_id = json.loads((Path(model_path) / "config.json").read_text()).get("mask_token_id")
    mask_id = int(mask_id) if mask_id is not None else None

    evidence["hook_alignment"] = check_alignment(args.model, wrapper_model, sampler, item, args.gen_length, args.hook_steps)
    try:
        evidence["observation_non_interference"] = final_tokens_with_and_without_extractor(
            args.model, wrapper_model, sampler, item, args.gen_length, mask_id)
    except Exception as error:
        evidence["observation_non_interference"] = {"error": f"{type(error).__name__}: {error}"}
    try:
        evidence["decode_unit_check"] = decode_unit_check()
    except Exception as error:
        evidence["decode_unit_check"] = {"error": f"{type(error).__name__}: {error}"}

    failed = [key for key in ("hook_alignment", "observation_non_interference", "decode_unit_check")
              if isinstance(evidence[key], dict) and "error" in evidence[key]]
    evidence["checks_failed"] = failed

    out_path = Path(args.out)
    existing = json.loads(out_path.read_text()) if out_path.exists() else {}
    existing[args.model] = evidence
    out_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(evidence, indent=2, ensure_ascii=False))
    print("wrote", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
