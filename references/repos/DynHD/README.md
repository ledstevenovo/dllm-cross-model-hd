# DynHD

Official implementation of **DynHD: Hallucination Detection for Diffusion Large Language Models via Denoising Dynamics Deviation Learning**.

Paper: [arXiv:2603.16459](https://arxiv.org/abs/2603.16459)

DynHD detects hallucinated answers from the denoising trajectory of a diffusion language model. The public pipeline contains four stages:

1. generate answers and collect per-step entropy evidence;
2. retain semantic token positions and construct mean/max/top-k evidence;
3. train the factual reference trajectory generator and deviation detector;
4. evaluate the detector on a fixed train/validation/test split.

## Repository layout

```text
configs/                 Collection configurations for LLaDA and Dream
docs/                    Data format and experiment details
scripts/                 End-to-end runner
dynhd/
  cli/                   collect, train, and evaluate
  data/                  trace serialization and splitting
  detectors/             DynHD reference generator and detector
  features/              entropy evidence construction
  labeling/              automatic correctness judge
  model/                 LLaDA and Dream adapters/samplers
```

## Installation

The reference environment uses Linux, Python 3.10 or 3.11, CUDA, and an NVIDIA GPU with 24 GB VRAM. Create a clean environment and install the package:

```bash
conda create -n dynhd python=3.11 -y
conda activate dynhd
pip install -r requirements.txt
pip install -e .
```

Model weights and datasets are downloaded by Hugging Face on first use. To force cached/offline loading, set `HF_HUB_OFFLINE=1`.

## Quick start

Set the judge API key in the environment. Never put it in a YAML file or commit it.

```bash
export OPENAI_API_KEY="..."
```

Run the LLaDA/TriviaQA pipeline with a small sample first:

```bash
bash scripts/run_llada_full_pipeline.sh \
  --dataset triviaqa \
  --num-samples 100 \
  --num-steps 64 \
  --gen-length 64
```

The script writes traces to `data/traces/` and checkpoints, the split, logs, and metrics to `results/current/`. Both directories are ignored by Git.

For the paper-scale setting, use `--num-samples 2000`. The split is 1,400/300/300 (70/15/15) with stratification and seed 42.

## Run stages separately

Collect semantic-aware evidence:

```bash
python -m dynhd.cli.collect_traces \
  --config configs/llada_dynhd.yaml \
  --dataset triviaqa \
  --num-samples 2000 \
  --num-steps 64 \
  --gen-length 64
```

Train the paper method. Each trace stores the paper's semantic evidence vector as `[mean, max, top-k mean]`.

```bash
python -m dynhd.cli.train_detector \
  --data-path data/traces/triviaqa/<run-directory> \
  --out-dir results/current/triviaqa_llada64 \
  --device cuda --seed 42 --stratify-split \
  --prompt-dim 256 --hidden-dim 256 --max-steps 64 \
  --epochs-stage1 10 --epochs-stage2 30 --batch-size 32 \
  --lr-stage1 1e-3 --lr-stage2 3e-4 \
  --weight-decay-stage1 0.05 --weight-decay-stage2 0.0 \
  --projector-dropout 0.3 \
  --lambda-path 0.05 --lambda-rebound 0.2 \
  --margin-quantile 0.8 --margin-ema 0.9
```

Evaluate the held-out test set:

```bash
python -m dynhd.cli.eval_detector \
  --data-path data/traces/triviaqa/<run-directory> \
  --ckpt results/current/triviaqa_llada64/detector.pt \
  --split results/current/triviaqa_llada64/split.json \
  --split-part test \
  --device cuda
```

Use `configs/dream_dynhd.yaml` for Dream. See [configs/README.md](configs/README.md) and [docs/data_and_splits.md](docs/data_and_splits.md).

## Supported settings

- Backbones: `GSAI-ML/LLaDA-8B-Instruct`, `Dream-org/Dream-v0-Instruct-7B`
- Datasets: TriviaQA, HotpotQA, CommonsenseQA
- Denoising steps: 64 and 128
- Main metric: AUROC

The default labeler uses the OpenAI-compatible Chat Completions endpoint. You may change `labeling.kwargs.base_url` for another compatible service, but should document that change when reporting results.

## Reproducibility notes

- Keep the generated `split.json` and reuse it for every comparison.
- Model repositories use `trust_remote_code=True`; review remote model code before running in a sensitive environment.
- Full trace collection is GPU- and network-intensive. The detector itself trains from saved traces without loading the backbone model.

## Citation

```bibtex
@article{qian2026dynhd,
  title={Dynhd: Hallucination detection for diffusion large language models via denoising dynamics deviation learning},
  author={Qian, Yanyu and Tan, Yue and Liu, Yixin and Yu, Wang and Pan, Shirui},
  journal={arXiv preprint arXiv:2603.16459},
  year={2026}
}
```

## License

This project is released under the [MIT License](LICENSE). Model weights and datasets remain subject to their respective upstream licenses.
