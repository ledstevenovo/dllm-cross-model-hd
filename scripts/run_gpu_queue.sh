#!/usr/bin/env bash
# GPU queue for the remaining R2 / robustness runs, run AFTER pool2000 finishes.
#
# Only one 8B model fits comfortably on the 31.5 GiB card at a time (each peaks at
# ~15 GiB), so every job here is strictly sequential.  The queue waits for the
# pool2000 driver to write its final line rather than guessing a duration.
#
# Jobs, in order:
#   1. R2 smoke20 (20 q)      -- catches prompt/format breakage before 800 questions
#   2. R2 HotpotQA 800        -- the actual R2 result (LLaDA FP16, L128/S64/B128)
#   3. TRE TriviaQA L64        -- the second budget column the paper reports
#   4. TRE HotpotQA L64        -- R2 at the other budget (same questions as job 2)
#   5. Dream TRE HotpotQA BF16 -- Dream's TRE variant (FP16 is blocked: NaN entropy)
#
# Each job is skipped if its output already exists, so the script is re-runnable.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/tre_r2_logs
Q="$REPO/data/trajectories/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1"
mkdir -p "$LOG" || exit 1
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache
export HF_HUB_OFFLINE=1

log() { echo "$* $(date -Is)" >> "$LOG/queue.log"; }

log "queue start pid=$$ host=$(hostname)"

# --- wait for pool2000 -------------------------------------------------------
while ! grep -q "driver done" /root/autodl-tmp/pool2000_logs/driver.log 2>/dev/null; do
  sleep 60
done
log "pool2000 finished; starting GPU queue"

run() {  # run <label> <logfile> <command...>
  local label=$1 logfile=$2
  shift 2
  log "START $label"
  "$@" >> "$LOG/$logfile" 2>&1
  local rc=$?
  log "END $label rc=$rc"
  return $rc
}

# --- 1. R2 smoke20 -----------------------------------------------------------
if [ ! -f "$REPO/data/trajectories/tre_repro/llada_hotpotqa_smoke20_fp16_v1/manifest.json" ]; then
  run smoke20_r2 smoke20.log .venv-llada/bin/python scripts/collect_llada.py \
    --questions data/tre_repro/questions/hotpotqa_smoke20.jsonl \
    --output "$REPO/data/trajectories/tre_repro/llada_hotpotqa_smoke20_fp16_v1" \
    --precision float16 --gen-length 128 --steps 64 --block-size 128 --seed 20261021 \
    --resume
else
  log "SKIP smoke20_r2 (exists)"
fi

# --- 2. R2 HotpotQA 800 ------------------------------------------------------
if [ ! -f "$Q/manifest.json" ]; then
  run r2_hotpotqa_800 r2_800.log .venv-llada/bin/python scripts/collect_llada.py \
    --questions data/tre_repro/questions/hotpotqa_eval800.jsonl \
    --output "$Q" \
    --precision float16 --gen-length 128 --steps 64 --block-size 128 --seed 20261021 \
    --resume
else
  log "SKIP r2_hotpotqa_800 (exists)"
fi

# --- 3. TRE TriviaQA, 64-generation budget ----------------------------------
if [ ! -f "$REPO/data/trajectories/tre_repro/llada_triviaqa_fp16_L64_S64_B64_v1/manifest.json" ]; then
  run tre_triviaqa_L64 triviaqa_L64.log .venv-llada/bin/python scripts/collect_llada.py \
    --questions data/tre_repro/questions/triviaqa_eval800.jsonl \
    --output "$REPO/data/trajectories/tre_repro/llada_triviaqa_fp16_L64_S64_B64_v1" \
    --precision float16 --gen-length 64 --steps 64 --block-size 64 --seed 20261021 \
    --resume
else
  log "SKIP tre_triviaqa_L64 (exists)"
fi

# --- 4. TRE HotpotQA, 64-generation budget ----------------------------------
if [ ! -f "$REPO/data/trajectories/tre_repro/llada_hotpotqa_fp16_L64_S64_B64_v1/manifest.json" ]; then
  run tre_hotpotqa_L64 hotpotqa_L64.log .venv-llada/bin/python scripts/collect_llada.py \
    --questions data/tre_repro/questions/hotpotqa_eval800.jsonl \
    --output "$REPO/data/trajectories/tre_repro/llada_hotpotqa_fp16_L64_S64_B64_v1" \
    --precision float16 --gen-length 64 --steps 64 --block-size 64 --seed 20261021 \
    --resume
else
  log "SKIP tre_hotpotqa_L64 (exists)"
fi

# --- 5. Dream TRE on HotpotQA (BF16; FP16 is blocked by the NaN guard) ------
if [ ! -f "$REPO/data/trajectories/tre_repro/dream_hotpotqa_bf16_L128_S64_B128_v1/manifest.json" ]; then
  run dream_hotpotqa_bf16 dream_bf16.log .venv-dream/bin/python scripts/collect_dream.py \
    --questions data/tre_repro/questions/hotpotqa_eval800.jsonl \
    --output "$REPO/data/trajectories/tre_repro/dream_hotpotqa_bf16_L128_S64_B128_v1" \
    --precision bf16 --gen-length 128 --steps 64 --block-size 128 --seed 20261021 \
    --resume
else
  log "SKIP dream_hotpotqa_bf16 (exists)"
fi

log "queue done"
