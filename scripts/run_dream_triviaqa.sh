#!/usr/bin/env bash
# Dream x TriviaQA at the R1 budget (L128/S64/B128), seed 20261021.
#
# Fills the paper's Table 1 row "Dream-7B-Instruct / TriviaQA" (83.9 / 84.8), which the
# project has never had. Question list and seed are identical to R1 so the only differences
# are the model and the precision.
#
# PRECISION: Dream runs BF16, not FP16. src/collection_cli.validate_precision rejects
# Dream+FP16 because the native entropy ranking can produce NaN there; that guard is not
# being disabled for a table cell. BF16 is therefore a registered protocol difference
# against R1 (LLaDA, FP16) and must be listed next to any comparison.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/dream_tre_logs
OUT="$REPO/data/trajectories/tre_repro/dream_triviaqa_bf16_L128_S64_B128_v1"
mkdir -p "$LOG"
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1
echo "dream_triviaqa start $(date -Is) host=$(hostname) pid=$$" >> "$LOG/driver.log"
.venv-dream/bin/python scripts/gpu_env_probe.py --out "$LOG/gpu_env_probe.json" >> "$LOG/driver.log" 2>&1
echo "probe_rc=$? $(date -Is)" >> "$LOG/driver.log"
.venv-dream/bin/python scripts/collect_dream.py \
  --questions data/tre_repro/questions/triviaqa_eval800.jsonl \
  --output "$OUT" --precision bf16 \
  --gen-length 128 --steps 64 --block-size 128 --seed 20261021 --resume \
  >> "$LOG/collect.log" 2>&1
rc=$?
echo "collect_rc=$rc $(date -Is)" >> "$LOG/driver.log"
