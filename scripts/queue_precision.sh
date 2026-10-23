#!/usr/bin/env bash
# After the L256 run, rerun LLaDA/HotpotQA-bare in BF16 to separate precision from model.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/precision_logs
mkdir -p "$LOG"
. "$REPO/scripts/lib/gpu_wait.sh"
echo "$(date -Is) queue waiting" >> "$LOG/queue.log"
gpu_wait "$LOG/queue.log"
echo "$(date -Is) GPU free; starting precision control" >> "$LOG/queue.log"
screen -dmS precision bash "$REPO/scripts/run_llada_hotpot_bf16.sh"
echo "$(date -Is) started" >> "$LOG/queue.log"
