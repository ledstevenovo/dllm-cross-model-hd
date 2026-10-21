# Detector hyperparameters

The end-to-end script uses the following public defaults. The complete resolved detector configuration is saved beside each checkpoint as `detector_config.json`.

| Argument | Default | Description |
| --- | ---: | --- |
| `--split-seed` | 42 | data split seed |
| `--max-steps` | 64 | number of trajectory steps; must match traces |
| `--prompt-dim` | 256 | projected question embedding size |
| `--hidden-dim` | 256 | reference/detector hidden size |
| `--epochs-stage1` | 10 | factual reference-generator epochs |
| `--epochs-stage2` | 30 | deviation-detector epochs |
| `--batch-size` | 32 | training batch size |
| `--lr-stage1` | 1e-3 | reference-generator learning rate |
| `--lr-stage2` | 3e-4 | deviation-detector learning rate |
| `--weight-decay-stage1` | 0.05 | stage-one weight decay |
| `--weight-decay-stage2` | 0.0 | stage-two weight decay |
| `--lambda-path` | 0.05 | path-deviation regularizer weight |
| `--lambda-rebound` | 0.2 | rebound regularizer weight |
| `--margin-quantile` | 0.8 | factual-score quantile for the margin |
| `--margin-ema` | 0.9 | EMA decay for adaptive margins |

The paper reports grid search ranges of `{3e-4, 1e-3}` for stage-one learning rate, `{1e-4, 3e-4, 1e-3}` for stage-two learning rate, `{0, 0.01, 0.05}` and `{0, 1e-4, 1e-3}` for stage-one/two weight decay, and `[0, 0.4]` in increments of `0.05` for both regularizer weights.
