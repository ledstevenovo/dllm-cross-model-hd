#!/usr/bin/env bash
# Wait until no collection process is running and the GPU is free.
#
# The original queues each waited on one specific process pattern, so a queue whose pattern did
# not match anything started immediately -- which is how the precision control ended up racing the
# Dream collection and dying with CUDA OOM (23 GB + 15 GB on a 31 GB card). Waiting on "any
# collector" plus "low GPU memory" is what the queues actually needed.
gpu_wait() {
  local log="${1:-/dev/null}"
  while true; do
    if pgrep -f "scripts/collect_(llada|dream)\.py" >/dev/null; then
      echo "$(date -Is) waiting: a collector is running" >> "$log"
      sleep 60; continue
    fi
    local used
    used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1 | tr -d ' ')
    if [ "${used:-0}" -gt 500 ]; then
      echo "$(date -Is) waiting: GPU still holds ${used} MiB" >> "$log"
      sleep 60; continue
    fi
    echo "$(date -Is) gpu free" >> "$log"
    return 0
  done
}
