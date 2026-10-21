from __future__ import annotations

from typing import Dict, List, Optional

import torch

from dynhd.features import SemanticEntropyExtractor
from dynhd.model.dream import DreamModel


class DreamDiffusionSampler:
    """Run Dream denoising while collecting one evidence vector per step."""

    def __init__(
        self,
        model: DreamModel,
        num_steps: int = 64,
        alg: str = "entropy",
        alg_temp: float = 0.0,
        top_p: Optional[float] = 0.95,
        top_k: Optional[int] = None,
        temperature: float = 0.2,
    ) -> None:
        self.model = model
        self.steps = int(num_steps)
        self.device = model.model.device
        self.alg = alg
        self.alg_temp = float(alg_temp)
        self.top_p = None if top_p is None else float(top_p)
        self.top_k = None if top_k is None else int(top_k)
        self.temperature = float(temperature)

    @torch.no_grad()
    def sample(
        self,
        prompt: object,
        gen_length: int = 128,
        feature_extractor: Optional[SemanticEntropyExtractor] = None,
        prompt_emb_messages: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, object]:
        tokenizer = self.model.tokenizer
        if isinstance(prompt, list):
            inputs = tokenizer.apply_chat_template(
                prompt, return_tensors="pt", return_dict=True, add_generation_prompt=True
            )
            input_ids = inputs.input_ids.to(self.device)
            attention_mask = inputs.attention_mask.to(self.device)
        else:
            inputs = tokenizer(str(prompt), return_tensors="pt")
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)
        prompt_length = int(input_ids.shape[1])

        if prompt_emb_messages is not None:
            embedding_inputs = tokenizer.apply_chat_template(
                prompt_emb_messages,
                return_tensors="pt",
                return_dict=True,
                add_generation_prompt=True,
            )
            embedding_ids = embedding_inputs.input_ids.to(self.device)
            embedding_mask = embedding_inputs.attention_mask.to(self.device)
        else:
            embedding_ids = input_ids
            embedding_mask = attention_mask
        prompt_output = self.model.forward(
            embedding_ids, attention_mask=embedding_mask, output_hidden_states=True
        )
        hidden_states = getattr(prompt_output, "hidden_states", None)
        if not hidden_states or hidden_states[-1] is None:
            raise RuntimeError("Dream did not return hidden states for the prompt embedding")
        prompt_embedding = hidden_states[-1].mean(dim=1).squeeze(0).detach().cpu()

        evidence: List[torch.Tensor] = []

        def capture_step(step: int, tokens: torch.Tensor, logits: torch.Tensor) -> torch.Tensor:
            del step
            if logits is None:
                return tokens
            generation_logits = logits[:, prompt_length:]
            if feature_extractor is not None:
                evidence.append(feature_extractor.step_from_logits(generation_logits))
            return tokens

        output = self.model.diffusion_generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=int(gen_length),
            steps=self.steps,
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            alg=self.alg,
            alg_temp=self.alg_temp,
            output_history=True,
            return_dict_in_generate=True,
            generation_tokens_hook_func=capture_step,
            generation_logits_hook_func=None,
        )

        generated_ids = output.sequences[0, prompt_length:].detach().cpu()
        end = int(generated_ids.numel())
        for token_id in (tokenizer.eos_token_id, tokenizer.mask_token_id):
            if token_id is not None:
                positions = (generated_ids == int(token_id)).nonzero(as_tuple=False)
                if positions.numel() > 0:
                    end = min(end, int(positions[0].item()))
        generated_text = tokenizer.decode(generated_ids[:end].tolist(), skip_special_tokens=True)
        return {
            "clean_text": generated_text,
            "prompt_emb": prompt_embedding,
            "features": torch.stack(evidence) if evidence else None,
        }
