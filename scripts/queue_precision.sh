#!/usr/bin/env bash
# After the L256 experiment, rerun LLaDA/HotpotQA-bare in BF16 to separate precision from model.
# LLaDA is currently FP16 and Dream BF16, so the ~0.016 model gap contains an unmeasured
# precision effect of unknown size. One BF16 rerun of the identical config resolves it.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/precision_logs
mkdir -p "$LOG"
log() { echo "$(date -Is) $*" >> "$LOG/queue.log"; }
log "waiting for l256 collector to finish"
while pgrep -f "collect_llada.py.*triviaqa_eval800" >/dev/null; do sleep 60; done
log "starting precision control"
screen -dmS precision bash "$REPO/scripts/run_llada_hotpot_bf16.sh"
log "started"
