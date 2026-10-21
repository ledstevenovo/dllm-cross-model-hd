import os
from types import SimpleNamespace
from typing import Optional

import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer, AutoConfig


class LLaDAModel:
    """Implementation component used by the public DynHD pipeline."""

    def __init__(
        self,
        model_path: str,
        device: str = "cuda",
        temperature: float = 0.0,
        masking_strategy: str = "low_conf",
        device_id: int = 0,
    ):
        self.device = device if (device == "cpu" or torch.cuda.is_available()) else "cpu"
        self.temperature = temperature
        self.masking_strategy = masking_strategy


        torch_type = torch.bfloat16 if self.device == "cuda" else torch.float32
        device_map = None
        if self.device == "cuda":
            try:
                import accelerate  # noqa: F401

                device_map = {"": device_id}
            except Exception:
                device_map = None


        is_hf_hub_path = "/" in model_path and not os.path.isdir(model_path)
        model_path_for_hf = model_path
        if os.environ.get("HF_HUB_OFFLINE") == "1" and is_hf_hub_path:
            import glob

            model_name = model_path.replace("/", "--")
            cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
            pattern = os.path.join(cache_dir, f"models--{model_name}", "snapshots", "*")
            matches = glob.glob(pattern)
            if matches:
                model_path_for_hf = matches[0]

        local_files_only = os.environ.get("HF_HUB_OFFLINE") == "1"
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path_for_hf, trust_remote_code=True, local_files_only=local_files_only
        )

        load_kwargs = dict(
            pretrained_model_name_or_path=model_path_for_hf,
            trust_remote_code=True,
            torch_dtype=torch_type,
            local_files_only=local_files_only,
        )
        if device_map is not None:
            load_kwargs["device_map"] = device_map

        self.model = AutoModel.from_pretrained(**load_kwargs)


        if device_map is None:
            self.model.to(self.device)
        self.model.eval()


        try:
            self.mask_id = self.tokenizer.vocab["[MASK]"]
        except Exception:
            cfg = AutoConfig.from_pretrained(
                model_path_for_hf,
                trust_remote_code=True,
                local_files_only=local_files_only,
            )
            self.mask_id = int(getattr(cfg, "mask_token_id", 126336))
        self.vocab_size = int(getattr(self.model.config, "vocab_size", self.tokenizer.vocab_size))


        self.lm_head = self._find_lm_head_robust()

    def _find_lm_head_robust(self) -> nn.Linear:
        candidates = ["lm_head", "output_layer", "embed_out", "head", "linear"]

        for name in candidates:
            if hasattr(self.model, name):
                m = getattr(self.model, name)
                if isinstance(m, nn.Linear):
                    return m

        if hasattr(self.model, "model"):
            for name in candidates:
                if hasattr(self.model.model, name):
                    m = getattr(self.model.model, name)
                    if isinstance(m, nn.Linear):
                        return m

        possible = []
        for name, m in self.model.named_modules():
            if isinstance(m, nn.Linear) and abs(int(m.out_features) - int(self.vocab_size)) < 128:
                possible.append((name, m))

        if len(possible) == 1:
            return possible[0][1]
        if len(possible) > 1:
            for name, m in possible:
                if ("head" in name) or ("lm" in name) or ("output" in name):
                    return m
            return possible[-1][1]

        raise AttributeError("Critical: cannot locate lm_head; cannot compute logits reliably.")

    def forward(self, input_ids: torch.Tensor, output_hidden_states: bool = False):
        """Implementation component used by the public DynHD pipeline."""
        out = self.model(input_ids, output_hidden_states=output_hidden_states)


        if hasattr(out, "logits") and out.logits is not None:
            return out


        hidden_states = getattr(out, "hidden_states", None)
        last_hidden = None
        if hidden_states is not None and len(hidden_states) > 0:
            last_hidden = hidden_states[-1]
        elif hasattr(out, "last_hidden_state") and out.last_hidden_state is not None:
            last_hidden = out.last_hidden_state


        if last_hidden is None:
            out2 = self.model(input_ids, output_hidden_states=True)
            hidden_states = getattr(out2, "hidden_states", None)
            if hidden_states is not None and len(hidden_states) > 0:
                last_hidden = hidden_states[-1]
            elif hasattr(out2, "last_hidden_state") and out2.last_hidden_state is not None:
                last_hidden = out2.last_hidden_state
            else:
                raise RuntimeError("Model forward returned neither logits nor hidden states.")
            out = out2

        logits = self.lm_head(last_hidden)
        return SimpleNamespace(logits=logits, hidden_states=hidden_states)

    def encode(self, text: str) -> torch.Tensor:
        return self.tokenizer.encode(text, return_tensors="pt").to(self.model.device)

    def decode(self, token_ids: torch.Tensor) -> str:
        if token_ids.dim() > 1:
            token_ids = token_ids[0]
        token_ids = token_ids.detach().cpu()
        ids_clean = token_ids[token_ids != self.mask_id]
        return self.tokenizer.decode(ids_clean, skip_special_tokens=True)
