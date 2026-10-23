#!/usr/bin/env bash
# Run the L256 prediction test once the context-L64 collection frees the GPU.
# Waits on the collector process rather than a guessed duration.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/l256_logs
mkdir -p "$LOG"
log() { echo "$(date -Is) $*" >> "$LOG/queue.log"; }
log "queue waiting for ctx_l64 collector"
while pgrep -f "collect_dream.py.*hotpotqa_eval800" >/dev/null; do sleep 60; done
log "GPU free; starting L256"
screen -dmS l256 bash "$REPO/scripts/run_llada_tq_l256.sh"
log "started l256"
