#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DATASET="triviaqa"
NUM_SAMPLES="2000"
NUM_STEPS="64"
GEN_LENGTH="64"
DEVICE="cuda"
SEED="42"
CFG="$ROOT/configs/llada_dynhd.yaml"
RUN_ID="$(date +%Y%m%d_%H%M%S)"
DATA_PATH="$ROOT/data/traces/$DATASET/$RUN_ID"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dataset) DATASET="$2"; shift 2 ;;
    --num-samples) NUM_SAMPLES="$2"; shift 2 ;;
    --num-steps) NUM_STEPS="$2"; shift 2 ;;
    --gen-length) GEN_LENGTH="$2"; shift 2 ;;
    --device) DEVICE="$2"; shift 2 ;;
    --seed) SEED="$2"; shift 2 ;;
    --config) CFG="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

DATA_PATH="$ROOT/data/traces/$DATASET/$RUN_ID"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY is required for the paper labeling protocol." >&2
  exit 1
fi

echo "[1/3] Collect traces"
python -m dynhd.cli.collect_traces \
  --config "$CFG" \
  --dataset "$DATASET" \
  --num-samples "$NUM_SAMPLES" \
  --num-steps "$NUM_STEPS" \
  --gen-length "$GEN_LENGTH" \
  --output-dir "$DATA_PATH"

OUT="$ROOT/results/current/${DATASET}_llada${NUM_STEPS}_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"

echo "[2/3] Train DynHD"
python -m dynhd.cli.train_detector \
  --data-path "$DATA_PATH" \
  --out-dir "$OUT" \
  --device "$DEVICE" \
  --seed "$SEED" \
  --stratify-split \
  --prompt-dim 256 \
  --hidden-dim 256 \
  --max-steps "$NUM_STEPS" \
  --epochs-stage1 10 \
  --epochs-stage2 30 \
  --batch-size 32 \
  --lr-stage1 1e-3 \
  --lr-stage2 3e-4 \
  --weight-decay-stage1 0.05 \
  --weight-decay-stage2 0.0 \
  --lambda-path 0.05 \
  --lambda-rebound 0.2 \
  --margin-quantile 0.8 \
  --margin-ema 0.9 \
  --verbose |& tee "$OUT/run.log"

echo "[3/3] Evaluate validation and test partitions"
for PART in val test; do
  python -m dynhd.cli.eval_detector \
    --data-path "$DATA_PATH" \
    --ckpt "$OUT/detector.pt" \
    --split "$OUT/split.json" \
    --split-part "$PART" \
    --device "$DEVICE" |& tee -a "$OUT/run.log"
done

echo "TRACE_DIR=$DATA_PATH"
echo "OUT_DIR=$OUT"
