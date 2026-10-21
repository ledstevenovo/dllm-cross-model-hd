# Configurations

Collection is configured with YAML files. Training hyperparameters are explicit CLI arguments so that every output directory records the exact detector configuration in `detector_config.json`.

| File | Backbone | Purpose |
| --- | --- | --- |
| `llada_dynhd.yaml` | LLaDA-8B-Instruct | DynHD main method |
| `dream_dynhd.yaml` | Dream-7B-Instruct | DynHD main method |

Common fields:

- `model.model_path`: Hugging Face model ID or local directory.
- `model.device`: normally `cuda`; use `cpu` only for lightweight checks.
- `inference.num_steps`: denoising trajectory length.
- `data.datasets`: dataset names and sample counts.
- `data.trace_save_dir`: output root for `.pt` traces.
- `features.top_k`: regional-uncertainty aggregation size.
- `labeling`: correctness judge settings.

Credentials are read only from `OPENAI_API_KEY`; do not add an `api_key` field to committed YAML files.
