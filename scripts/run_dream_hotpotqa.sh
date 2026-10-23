#!/usr/bin/env bash
# Dream x HotpotQA at L128/S64/B128, BF16, same 800 questions as R2.
#
# Why this cell matters beyond filling a table row: LLaDA's HotpotQA answers run to the
# 126-token budget 46.6% of the time (it recites the context), while Dream's TriviaQA
# answers have median length 3.  If Dream answers HotpotQA briefly, then the HotpotQA
# shortfall can be attributed to the recitation behaviour rather than to the dataset --
# that is a hypothesis test, not just a fifth cell.
#
# BF16 because validate_precision hard-rejects Dream + FP16 on NaN risk in the native
# entropy ranking. Judge afterwards with the deepseek judge directly: the R2 adjudication
# showed the rule sign-off is unusable for long HotpotQA answers (126/142 disagreements
# went to the judge).
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/dream_hotpot_logs
OUT="$REPO/data/trajectories/tre_repro/dream_hotpotqa_bf16_L128_S64_B128_v1"
mkdir -p "$LOG"
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1
echo "dream_hotpotqa start $(date -Is) pid=$$" >> "$LOG/driver.log"
.venv-dream/bin/python scripts/collect_dream.py \
  --questions data/tre_repro/questions/hotpotqa_eval800.jsonl \
  --output "$OUT" --precision bf16 \
  --gen-length 128 --steps 64 --block-size 128 --seed 20261021 --resume \
  >> "$LOG/collect.log" 2>&1
rc=$?
echo "collect_rc=$rc $(date -Is)" >> "$LOG/driver.log"
