# Contributing

Bug reports and focused pull requests are welcome. Please describe the backbone, dataset, denoising steps, configuration, random seed, and a minimal reproduction.

Before submitting a change:

```bash
python -m unittest discover -s tests -v
python -m compileall -q dynhd tests
```

Do not commit model weights, generated traces, checkpoints, personal data, API credentials, or local absolute paths. Changes that affect the method should explain how they map to the paper.
