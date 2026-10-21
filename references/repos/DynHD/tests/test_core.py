from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import torch

from dynhd.config import load_yaml_config
from dynhd.data import load_trace_dir, save_trace_with_prompt_emb
from dynhd.detectors import DetectorConfig, DynHDDetector
from dynhd.features import SemanticEntropyExtractor


class FakeTokenizer:
    all_special_ids = [0]
    eos_token_id = 0
    pad_token_id = None
    mask_token_id = None
    bos_token_id = None

    tokens = {
        0: "<|endoftext|>",
        1: "the",
        2: ",",
        3: "Paris",
        4: "##ing",
        5: "Answer",
        6: "France",
    }

    def convert_ids_to_tokens(self, token_id: int) -> str:
        return self.tokens[token_id]


class RepositoryTests(unittest.TestCase):
    def test_public_text_has_no_secrets_or_non_ascii_comments(self) -> None:
        root = Path(__file__).resolve().parents[1]
        suffixes = {".cff", ".example", ".md", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml"}
        excluded = {".build-test", ".git", "build", "dist", "__pycache__"}
        secret = re.compile(r"sk-[A-Za-z0-9_-]{20,}")
        yaml_key = re.compile(r"(?im)^\s*api_key\s*:\s*\S+")
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in suffixes or excluded.intersection(path.parts):
                continue
            content = path.read_text(encoding="utf-8")
            self.assertIsNone(secret.search(content), str(path))
            self.assertIsNone(yaml_key.search(content), str(path))
            if path.suffix == ".py":
                content.encode("ascii")


class FeatureTests(unittest.TestCase):
    def test_semantic_filter_covers_paper_categories(self) -> None:
        extractor = SemanticEntropyExtractor(FakeTokenizer(), top_k=2)
        predicted = torch.tensor([0, 1, 2, 3, 4, 5, 6])
        keep = extractor._keep_mask(predicted)
        self.assertEqual(keep.tolist(), [False, False, False, True, False, False, True])

    def test_entropy_evidence_shape_and_order(self) -> None:
        extractor = SemanticEntropyExtractor(FakeTokenizer(), top_k=2)
        logits = torch.full((7, 7), -4.0)
        for position, token_id in enumerate(range(7)):
            logits[position, token_id] = float(position + 1)
        evidence = extractor.step_from_logits(logits)
        self.assertEqual(tuple(evidence.shape), (3,))
        self.assertTrue(torch.isfinite(evidence).all())
        self.assertGreaterEqual(float(evidence[1]), float(evidence[2]))
        self.assertGreaterEqual(float(evidence[2]), float(evidence[0]))


class DataTests(unittest.TestCase):
    def test_trace_round_trip_and_config_loading(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "000000.pt"
            save_trace_with_prompt_emb(
                str(path),
                features=torch.ones((4, 3)),
                label=0,
                meta={"question": "Where?"},
                prompt_emb=torch.ones(6),
            )
            loaded = load_trace_dir(directory)
            self.assertEqual(len(loaded), 1)
            self.assertEqual(tuple(loaded[0]["features"].shape), (4, 3))
        root = Path(__file__).resolve().parents[1]
        for name in ("llada_dynhd.yaml", "dream_dynhd.yaml"):
            config = load_yaml_config(str(root / "configs" / name))
            self.assertIn("model", config)
            self.assertIn("features", config)
            self.assertNotIn("api_key", config["labeling"]["kwargs"])


class DetectorTests(unittest.TestCase):
    @staticmethod
    def _synthetic_data() -> list[dict]:
        generator = torch.Generator().manual_seed(7)
        data = []
        for index in range(24):
            label = index % 2
            base = torch.linspace(1.0, 0.1, 8).unsqueeze(1).repeat(1, 3)
            if label == 1:
                base[-3:] += torch.tensor([0.2, 0.4, 0.7]).unsqueeze(1)
            features = base + 0.01 * torch.randn((8, 3), generator=generator)
            data.append(
                {
                    "features": features,
                    "label": label,
                    "prompt_emb": torch.randn(6, generator=generator),
                    "meta": {"question": f"Question {index}"},
                }
            )
        return data

    def test_two_stage_training_and_prediction(self) -> None:
        data = self._synthetic_data()
        cfg = DetectorConfig(
            prompt_dim=4,
            hidden_dim=8,
            max_steps=8,
            batch_size=6,
            epochs_stage1=2,
            epochs_stage2=2,
            seed=3,
        )
        detector = DynHDDetector(cfg, device="cpu")
        detector.train_stage1(data)
        detector.train_stage2(data)
        probabilities = detector.predict_proba(data)
        self.assertEqual(probabilities.shape, (24,))
        self.assertTrue(np.isfinite(probabilities).all())
        self.assertTrue(((probabilities >= 0.0) & (probabilities <= 1.0)).all())

    def test_invalid_feature_shape_fails_fast(self) -> None:
        detector = DynHDDetector(DetectorConfig(), device="cpu")
        with self.assertRaises(ValueError):
            detector.predict_proba([{"features": torch.ones(4), "label": 0}])

    def test_training_and_evaluation_cli(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            traces = root / "traces"
            output = root / "output"
            traces.mkdir()
            for index, item in enumerate(self._synthetic_data()):
                torch.save(item, traces / f"{index:06d}.pt")
            train = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dynhd.cli.train_detector",
                    "--data-path",
                    str(traces),
                    "--out-dir",
                    str(output),
                    "--device",
                    "cpu",
                    "--stratify-split",
                    "--prompt-dim",
                    "4",
                    "--hidden-dim",
                    "8",
                    "--max-steps",
                    "8",
                    "--epochs-stage1",
                    "1",
                    "--epochs-stage2",
                    "1",
                    "--batch-size",
                    "6",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Saved checkpoint", train.stdout)
            evaluation = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dynhd.cli.eval_detector",
                    "--data-path",
                    str(traces),
                    "--ckpt",
                    str(output / "detector.pt"),
                    "--split",
                    str(output / "split.json"),
                    "--split-part",
                    "test",
                    "--device",
                    "cpu",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn('"auroc"', evaluation.stdout)


if __name__ == "__main__":
    unittest.main()
