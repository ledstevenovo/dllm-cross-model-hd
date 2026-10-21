import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Union


def _ensure_v1(base_url: str) -> str:
    base_url = base_url.rstrip("/")
    if base_url.endswith("/v1"):
        return base_url
    return base_url + "/v1"


class OpenAIChatLabeler:
    """Implementation component used by the public DynHD pipeline."""

    def __init__(
        self,
        *,
        model: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com/v1",
        temperature: float = 0.0,
        max_retries: int = 3,
        max_tokens: int = 10,
        timeout_s: int = 60,
    ):
        self.model = model
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")
        self.base_url = _ensure_v1(base_url)
        self.temperature = float(temperature)
        self.max_retries = int(max_retries)
        self.max_tokens = int(max_tokens)
        self.timeout_s = int(timeout_s)

    @staticmethod
    def check_correctness_match(generated_text: str, ground_truth: Any) -> int:
        """Implementation component used by the public DynHD pipeline."""
        if not ground_truth:
            return 1
        if not generated_text or not str(generated_text).strip():
            return 1
        gen = str(generated_text).lower().strip()
        if isinstance(ground_truth, list):
            for gt in ground_truth:
                if str(gt).lower().strip() in gen:
                    return 0
            return 1
        gt = str(ground_truth).lower().strip()
        return 0 if gt in gen else 1

    @staticmethod
    def _format_ground_truth(ground_truth: Any) -> str:
        """Implementation component used by the public DynHD pipeline."""
        if isinstance(ground_truth, list):
            if len(ground_truth) == 1:
                return f"The expected answer is: {ground_truth[0]}"
            return f"The following are expected answers: {', '.join([str(x) for x in ground_truth])}"
        return f"The expected answer is: {ground_truth}"

    def _build_prompt(self, question: str, ground_truth: Union[str, List[str]], generated: str) -> List[Dict[str, str]]:

        gt_text = self._format_ground_truth(ground_truth)
        prompt = (
            "We are assessing the quality of answers to the following question:\n\n"
            f"Question: {question}\n\n"
            f"{gt_text}\n\n"
            f"The proposed answer is: {generated}\n\n"
            "On the basis of the given question, expected answer, and your own knowledge, is the proposed answer correct?\n"
            'Please think carefully and respond only with "yes" or "no".\n\n'
            "Response:"
        )
        return [
            {"role": "system", "content": "You are a helpful assistant that evaluates answer correctness."},
            {"role": "user", "content": prompt},
        ]

    def label_one(self, *, question: str, ground_truth: Any, generated: str) -> Dict[str, Any]:
        messages = self._build_prompt(question, ground_truth, generated)
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        url = self.base_url + "/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        last_err: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                req = urllib.request.Request(
                    url=url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                    raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                content = data["choices"][0]["message"]["content"]
                answer = (content or "").strip().lower().rstrip(".! ")
                if answer == "yes":
                    return {"label": 0, "rationale": content.strip()}
                if answer == "no":
                    return {"label": 1, "rationale": content.strip()}


                if attempt < self.max_retries - 1:
                    time.sleep(1.0)
                    continue
                raise ValueError(f"Judge returned an unclear response: {content.strip()!r}")
            except Exception as e:
                last_err = e
                if attempt < self.max_retries - 1:

                    time.sleep(2 ** attempt)
                    continue

                raise RuntimeError(f"Labeling request failed after {self.max_retries} attempts") from e


        raise RuntimeError(f"Labeling request failed after {self.max_retries} attempts") from last_err
