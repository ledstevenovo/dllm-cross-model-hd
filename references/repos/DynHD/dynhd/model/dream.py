import os
from typing import Any, Dict, Optional

import torch
from transformers import AutoModel, AutoTokenizer
import glob


class DreamModel:
    """Implementation component used by the public DynHD pipeline."""

    def __init__(
        self,
        model_path: str,
        device: str = "cuda",
        temperature: float = 0.0,
        device_id: int = 0,
    ):
        self.device = device if (device == "cpu" or torch.cuda.is_available()) else "cpu"
        self.temperature = float(temperature)

        torch_type = torch.bfloat16 if self.device == "cuda" else torch.float32



        model_path_for_hf = model_path
        is_hf_hub_path = "/" in model_path and not os.path.isdir(model_path)
        if os.environ.get("HF_HUB_OFFLINE") == "1" and is_hf_hub_path:
            model_name = model_path.replace("/", "--")
            cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
            pattern = os.path.join(cache_dir, f"models--{model_name}", "snapshots", "*")
            matches = glob.glob(pattern)
            if matches:
                model_path_for_hf = matches[0]
        local_files_only = os.environ.get("HF_HUB_OFFLINE") == "1"
        load_kwargs: Dict[str, Any] = dict(
            pretrained_model_name_or_path=model_path_for_hf,
            trust_remote_code=True,
            torch_dtype=torch_type,
            local_files_only=local_files_only,
        )
        tok_kwargs: Dict[str, Any] = dict(
            pretrained_model_name_or_path=model_path_for_hf,
            trust_remote_code=True,
            local_files_only=local_files_only,
        )


        self.tokenizer = AutoTokenizer.from_pretrained(**tok_kwargs)
        self.model = AutoModel.from_pretrained(**load_kwargs)
        if self.device == "cuda":
            self.model = self.model.to(device=f"cuda:{device_id}")
        else:
            self.model = self.model.to(self.device)
        self.model.eval()

        self.mask_id = int(self.tokenizer.mask_token_id) if self.tokenizer.mask_token_id is not None else -100
        self.vocab_size = int(getattr(self.model.config, "vocab_size", getattr(self.tokenizer, "vocab_size", 0)))

    def encode(self, text: str) -> torch.Tensor:

        return self.tokenizer.encode(text, return_tensors="pt").to(self.model.device)

    def decode(self, token_ids: torch.Tensor) -> str:
        if token_ids.dim() > 1:
            token_ids = token_ids[0]
        ids = token_ids.detach().cpu()

        eos_id = getattr(self.tokenizer, "eos_token_id", None)
        mask_id = getattr(self.tokenizer, "mask_token_id", None)

        cut = int(ids.numel())
        if eos_id is not None:
            pos = (ids == int(eos_id)).nonzero(as_tuple=False)
            if pos.numel() > 0:
                cut = min(cut, int(pos[0].item()))
        if mask_id is not None:
            pos = (ids[:cut] == int(mask_id)).nonzero(as_tuple=False)
            if pos.numel() > 0:
                cut = min(cut, int(pos[0].item()))

        return self.tokenizer.decode(ids[:cut].tolist(), skip_special_tokens=True)

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        output_hidden_states: bool = False,
    ):


        am = attention_mask


        if am is not None and am.dtype not in (torch.bool, torch.float16, torch.float32, torch.bfloat16):
            am = am.bool()
        return self.model(input_ids=input_ids, attention_mask=am, output_hidden_states=output_hidden_states)

    @torch.no_grad()
    def diffusion_generate(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        *,
        max_new_tokens: int,
        steps: int,
        temperature: float = 0.0,
        top_p: Optional[float] = 1.0,
        top_k: Optional[int] = None,
        alg: str = "entropy",
        alg_temp: float = 0.0,
        output_history: bool = True,
        return_dict_in_generate: bool = True,
        generation_tokens_hook_func=None,
        generation_logits_hook_func=None,
    ):

        return self.model.diffusion_generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            output_history=output_history,
            return_dict_in_generate=return_dict_in_generate,
            steps=steps,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            alg=alg,
            alg_temp=alg_temp,
            generation_tokens_hook_func=generation_tokens_hook_func,
            generation_logits_hook_func=generation_logits_hook_func,
        )
