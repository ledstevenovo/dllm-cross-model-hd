from __future__ import annotations

import argparse
import os
import re
from datetime import datetime
from typing import Any, Dict, List

import torch
from tqdm import tqdm

os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

from dynhd.config import load_yaml_config
from dynhd.data import save_trace_with_prompt_emb
from dynhd.features import SemanticEntropyExtractor
from dynhd.labeling import OpenAIChatLabeler
from dynhd.model import DreamDiffusionSampler, DreamModel, LLaDAModel, LLaDASampler

def _load_dataset_items(name: str, split: str, limit: int) -> List[Dict[str, Any]]:
    from datasets import load_dataset

    if name == "triviaqa":
        dataset = load_dataset("trivia_qa", "rc", split=split)
        items = []
        for index, row in enumerate(dataset):
            if index >= limit:
                break
            answer = row.get("answer", {}) or {}
            aliases = {
                value
                for value in [answer.get("normalized_value"), answer.get("value"), *(answer.get("aliases", []) or [])]
                if value
            }
            items.append({"id": row.get("question_id", str(index)), "question": row.get("question", ""), "answer": sorted(aliases)})
        return items
    if name == "hotpotqa":
        dataset = load_dataset("hotpot_qa", "distractor", split=split)
        items = []
        for index, row in enumerate(dataset):
            if index >= limit:
                break
            items.append({"id": row.get("id", str(index)), "question": row.get("question", ""), "answer": row.get("answer", "")})
        return items
    if name == "commonsenseqa":
        dataset = load_dataset("commonsense_qa", split=split)
        items = []
        for index, row in enumerate(dataset):
            if index >= limit:
                break
            raw_choices = row.get("choices", {}) or {}
            choices = dict(zip(raw_choices.get("label", []) or [], raw_choices.get("text", []) or []))
            key = str(row.get("answerKey", "")).upper()
            items.append({
                "id": row.get("id", str(index)),
                "question": row.get("question", ""),
                "answer": [key, choices.get(key, "")],
                "answer_key": key,
                "choices": choices,
            })
        return items
    raise ValueError(f"Unsupported dataset: {name}")


def _question_content(item: Dict[str, Any]) -> str:
    if not item.get("choices"):
        return item["question"]
    block = "\n".join(f"{key}) {item['choices'][key]}" for key in "ABCDE" if key in item["choices"])
    return (
        "Choose the best option and output only its letter (A, B, C, D, or E).\n\n"
        f"Question: {item['question']}\nChoices:\n{block}\nAnswer:"
    )


def _llada_prompt(model: Any, item: Dict[str, Any]) -> str:
    content = _question_content(item)
    messages = [{"role": "user", "content": content}]
    if hasattr(model.tokenizer, "apply_chat_template"):
        return model.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return f"User: {content}\n\nAssistant: "


def _judge_question(item: Dict[str, Any]) -> str:
    if not item.get("choices"):
        return item["question"]
    block = "\n".join(f"{key}) {item['choices'][key]}" for key in "ABCDE" if key in item["choices"])
    return f"{item['question']}\n\nChoices:\n{block}"


def _prediction_key(text: str) -> str:
    match = re.search(r"\b([A-E])\b", text.upper())
    return match.group(1) if match else ""


def _build_model_and_sampler(model_path: str, device: str, inference: Dict[str, Any], steps: int):
    if "dream" in model_path.lower():
        model = DreamModel(model_path, device=device)
        sampler = DreamDiffusionSampler(
            model,
            num_steps=steps,
            temperature=float(inference.get("temperature", 0.2)),
            top_p=inference.get("top_p", 0.95),
            top_k=inference.get("top_k"),
            alg=str(inference.get("dream_alg", "entropy")),
            alg_temp=float(inference.get("dream_alg_temp", 0.0)),
        )
        return "dream", model, sampler
    model = LLaDAModel(model_path, device=device)
    return "llada", model, LLaDASampler(model, num_steps=steps)


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect semantic entropy trajectories for DynHD")
    parser.add_argument("--config", required=True, help="Collection YAML configuration")
    parser.add_argument("--dataset", required=True, choices=["triviaqa", "hotpotqa", "commonsenseqa"])
    parser.add_argument("--split", default="validation", help="Hugging Face dataset split")
    parser.add_argument("--num-samples", type=int, default=None)
    parser.add_argument("--num-steps", type=int, default=None)
    parser.add_argument("--gen-length", type=int, default=64)
    parser.add_argument("--output-dir", default=None, help="Exact trace output directory")
    args = parser.parse_args()

    config = load_yaml_config(args.config)
    model_config = config.get("model", {})
    inference = config.get("inference", {})
    model_path = str(model_config.get("model_path", ""))
    if not model_path:
        raise ValueError("config.model.model_path is required")
    if args.num_samples is not None and args.num_samples < 1:
        raise ValueError("--num-samples must be positive")
    if args.num_steps is not None and args.num_steps < 1:
        raise ValueError("--num-steps must be positive")
    if args.gen_length < 1:
        raise ValueError("--gen-length must be positive")

    configured = {
        str(entry.get("name", "")).lower(): entry
        for entry in config.get("data", {}).get("datasets", [])
        if isinstance(entry, dict)
    }
    dataset_config = configured.get(args.dataset, {})
    sample_count = int(args.num_samples or dataset_config.get("num_samples", 2000))
    steps = int(args.num_steps or inference.get("num_steps", 64))

    labeling = config.get("labeling", {})
    if labeling.get("method") != "openai":
        raise ValueError("The public pipeline requires labeling.method=openai")
    label_kwargs = labeling.get("kwargs", {}) or {}
    if "api_key" in label_kwargs:
        raise ValueError("Do not store API keys in YAML; set OPENAI_API_KEY")
    labeler = OpenAIChatLabeler(
        model=str(label_kwargs.get("model", "gpt-4o-mini")),
        base_url=str(label_kwargs.get("base_url", "https://api.openai.com/v1")),
        temperature=float(label_kwargs.get("temperature", 0.0)),
        max_retries=int(label_kwargs.get("max_retries", 3)),
    )

    items = _load_dataset_items(args.dataset, args.split, sample_count)
    if len(items) != sample_count:
        raise RuntimeError(f"Requested {sample_count} samples but loaded {len(items)}")
    family, model, sampler = _build_model_and_sampler(
        model_path, str(model_config.get("device", "cuda")), inference, steps
    )
    extractor = SemanticEntropyExtractor(
        tokenizer=model.tokenizer,
        top_k=int(config.get("features", {}).get("top_k", 5)),
    )

    trace_root = str(config.get("data", {}).get("trace_save_dir", "data/traces"))
    output_dir = args.output_dir or os.path.join(
        trace_root, args.dataset, f"{datetime.now():%Y%m%d_%H%M%S}_{family}_n{sample_count}"
    )
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=False)
    print(f"Collecting {len(items)} traces into {output_dir}")

    failures = []
    for index, item in tqdm(enumerate(items), total=len(items), desc=f"collect[{args.dataset}]"):
        try:
            if family == "dream":
                result = sampler.sample(
                    [{"role": "user", "content": _question_content(item)}],
                    gen_length=args.gen_length,
                    feature_extractor=extractor,
                    prompt_emb_messages=[{"role": "user", "content": item["question"]}],
                )
            else:
                result = sampler.sample(
                    _llada_prompt(model, item),
                    gen_length=args.gen_length,
                    feature_extractor=extractor,
                )
            features = result.get("features")
            if not isinstance(features, torch.Tensor) or tuple(features.shape) != (steps, 3):
                raise RuntimeError(f"Expected features [{steps}, 3], got {getattr(features, 'shape', None)}")
            generated = str(result.get("clean_text", ""))
            judgment = labeler.label_one(
                question=_judge_question(item), ground_truth=item["answer"], generated=generated
            )
            metadata = {
                "id": item["id"],
                "dataset": args.dataset,
                "model_family": family,
                "model_path": model_path,
                "question": item["question"],
                "ground_truth": item["answer"],
                "generated_text": generated,
                "labeling_method": "openai",
                "labeling_rationale": judgment.get("rationale", ""),
            }
            if item.get("choices"):
                metadata.update(choices=item["choices"], answerKey=item["answer_key"], predKey=_prediction_key(generated))
            save_trace_with_prompt_emb(
                os.path.join(output_dir, f"{index:06d}.pt"),
                features=features,
                label=int(judgment["label"]),
                meta=metadata,
                prompt_emb=result.get("prompt_emb"),
            )
        except Exception as error:
            failures.append(f"index={index} id={item['id']}: {type(error).__name__}: {error}")
            print(f"[error] {failures[-1]}")

    if failures:
        raise RuntimeError(
            f"Collection failed for {len(failures)}/{len(items)} samples:\n" + "\n".join(failures[:10])
        )
    print(f"Saved {len(items)} complete traces to {output_dir}")


if __name__ == "__main__":
    main()
