# Data, trace format, and splits

## Datasets

The collector supports the validation splits of:

- TriviaQA (`trivia_qa`, `rc` configuration)
- HotpotQA (`hotpot_qa`, `distractor` configuration)
- CommonsenseQA (`commonsense_qa`)

For paper-scale experiments, the first 2,000 examples of a dataset split are generated and labeled. CommonsenseQA uses a multiple-choice prompt; TriviaQA and HotpotQA use short-answer prompts.

## Trace files

Each generated example is stored as one `.pt` mapping:

```text
features:   float tensor [T, 3]
label:      integer; 0 = factual/correct, 1 = hallucinated/incorrect
prompt_emb: float tensor used by the reference trajectory generator, or null
meta:       question, reference answer, generated answer, IDs, model and labeler metadata
```

The three stored evidence columns are:

1. mean entropy across retained semantic positions;
2. maximum entropy across retained semantic positions;
3. mean of the top-k entropies across retained semantic positions.

Trace files may contain generated text and automated-judge rationales. Review them for privacy and dataset-license constraints before redistributing them. Generated traces and checkpoints are excluded from Git by default.

## Labels

The paper protocol uses GPT-4o-mini to judge generated answers against the question and reference answer. Set `OPENAI_API_KEY` in the environment.

## Splits

`train_detector` creates a 70/15/15 train/validation/test split. With 2,000 examples this gives 1,400/300/300 examples. Use `--stratify-split --split-seed 42`, then retain the generated `split.json` for evaluation.
