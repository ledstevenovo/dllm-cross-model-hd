#!/usr/bin/env bash
# Run the L256 prediction test once the GPU is genuinely free.
#
# Originally this waited on "collect_dream.py.*hotpotqa_eval800", which is fine when a Dream
# collection is what holds the card -- but the precision queue used a different pattern, matched
# nothing, and started immediately, racing the running collection into CUDA OOM. Both queues now
# use gpu_wait(), which checks any collector plus actual GPU memory.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/l256_logs
mkdir -p "$LOG"
. "$REPO/scripts/lib/gpu_wait.sh"
echo "$(date -Is) queue waiting" >> "$LOG/queue.log"
gpu_wait "$LOG/queue.log"
echo "$(date -Is) GPU free; starting L256" >> "$LOG/queue.log"
screen -dmS l256 bash "$REPO/scripts/run_llada_tq_l256.sh"
echo "$(date -Is) started l256" >> "$LOG/queue.log"
