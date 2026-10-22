#!/usr/bin/env bash
# pool2000 expansion collection: 1800 new questions x 2 models on ONE device.
# Runs detached in screen 'pool2000' so a dropped SSH/session cannot kill it.
# Same accepted config as pilot200 (cuda/bf16/64-64-64/seed 20261020/--verify-observer).
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/pool2000_logs
OUT="$REPO/data/trajectories/bf16_pool2000"
mkdir -p "$LOG" || exit 1
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache
export HF_HUB_OFFLINE=1

echo "driver start $(date -Is) host=$(hostname) pid=$$" | tee -a "$LOG/driver.log"

# Record the device before collecting: trajectories may only be pooled when both
# models came from the same GPU (reports/device_migration_5090.md section 4).
.venv-llada/bin/python scripts/gpu_env_probe.py --out "$LOG/gpu_env_probe_llada.json" >>"$LOG/driver.log" 2>&1
echo "probe_llada_rc=$? $(date -Is)" >> "$LOG/driver.log"
.venv-dream/bin/python scripts/gpu_env_probe.py --out "$LOG/gpu_env_probe_dream.json" >>"$LOG/driver.log" 2>&1
echo "probe_dream_rc=$? $(date -Is)" >> "$LOG/driver.log"

.venv-llada/bin/python scripts/collect_llada.py \
  --questions data/raw_qa/subsets/pool2000_v1_new.jsonl \
  --output "$OUT/llada" --precision bf16 --verify-observer >>"$LOG/llada.log" 2>&1
llada_rc=$?
echo "llada_rc=$llada_rc $(date -Is)" >> "$LOG/driver.log"

.venv-dream/bin/python scripts/collect_dream.py \
  --questions data/raw_qa/subsets/pool2000_v1_new.jsonl \
  --output "$OUT/dream" --precision bf16 --verify-observer >>"$LOG/dream.log" 2>&1
dream_rc=$?
echo "dream_rc=$dream_rc $(date -Is)" >> "$LOG/driver.log"

if [ "$llada_rc" -eq 0 ] && [ "$dream_rc" -eq 0 ]; then
  echo "collection complete $(date -Is)" >> "$LOG/driver.log"
else
  echo "collection FAILED llada=$llada_rc dream=$dream_rc -- rerun with --resume after fixing" >> "$LOG/driver.log"
fi
echo "driver done $(date -Is)" >> "$LOG/driver.log"
