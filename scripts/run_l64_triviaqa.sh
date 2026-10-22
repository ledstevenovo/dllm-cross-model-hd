#!/usr/bin/env bash
# TRE TriviaQA at the 64-token budget: the second column of the paper's Table 1.
# R1 covered the 128-generation budget; the paper reports both, so a 64 run is needed to
# compare against the 86.5 column. Pure collection -- judging happens after, by the same
# frozen prompt and the same judge used for R1 (so it stays one label file, one judge).
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/tre_r2_logs
OUT="$REPO/data/trajectories/tre_repro/llada_triviaqa_fp16_L64_S64_B64_v1"
mkdir -p "$LOG"
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1
echo "l64_triviaqa start $(date -Is)" >> "$LOG/l64.log"
.venv-llada/bin/python scripts/collect_llada.py \
  --questions data/tre_repro/questions/triviaqa_eval800.jsonl \
  --output "$OUT" --precision float16 \
  --gen-length 64 --steps 64 --block-size 64 --seed 20261021 \
  >> "$LOG/l64_collect.log" 2>&1
rc=$?
echo "l64_triviaqa rc=$rc $(date -Is)" >> "$LOG/l64.log"
