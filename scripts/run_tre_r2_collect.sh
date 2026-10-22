#!/usr/bin/env bash
# TRE R2: HotpotQA x LLaDA, 800 questions, FP16, L128/S64/B128, seed 20261021.
#
# Mirrors the R1 configuration (run_tre800.sh) exactly except for the question
# list and the prompt style: R2 questions carry the HotpotQA distractor context,
# so the prompt is the context-grounded v4 form.  That is a *different prompt
# version*, recorded per record and in the manifest, never an edit of R1's.
#
# No --verify-observer: R1's formal 800-question run did not use it either, and
# doubling every generation would double an already expensive run.  Determinism
# is still checked by the same-machine bit-identical reproduction established for
# pilot200 (reports/device_migration_5090.md section 4).
#
# Runs detached in screen 'tre_r2'.  Re-runnable: --resume is passed so an
# interrupted run continues instead of restarting.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/tre_r2_logs
OUT="$REPO/data/trajectories/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1"
mkdir -p "$LOG" || exit 1
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache
export HF_HUB_OFFLINE=1

echo "tre_r2 start $(date -Is) host=$(hostname) pid=$$" | tee -a "$LOG/driver.log"

# Record the device before collecting; R2 is a single-model run but the GPU that
# produced it must still be on record for any later cross-device comparison.
.venv-llada/bin/python scripts/gpu_env_probe.py --out "$LOG/gpu_env_probe_llada.json" >>"$LOG/driver.log" 2>&1
echo "probe_rc=$? $(date -Is)" >> "$LOG/driver.log"

.venv-llada/bin/python scripts/collect_llada.py \
  --questions data/tre_repro/questions/hotpotqa_eval800.jsonl \
  --output "$OUT" \
  --precision float16 --gen-length 128 --steps 64 --block-size 128 --seed 20261021 \
  --resume >>"$LOG/collect.log" 2>&1
rc=$?
echo "collect_rc=$rc $(date -Is)" >> "$LOG/driver.log"
if [ "$rc" -eq 0 ]; then
  echo "collection complete $(date -Is)" >> "$LOG/driver.log"
else
  echo "collection FAILED rc=$rc -- rerun with --resume after fixing" >> "$LOG/driver.log"
fi
echo "tre_r2 done $(date -Is)" >> "$LOG/driver.log"
