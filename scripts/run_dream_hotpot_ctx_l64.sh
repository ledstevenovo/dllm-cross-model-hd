#!/usr/bin/env bash
# Dream x HotpotQA WITH context at L64, to complete the context x budget interaction.
#
# The bare 2x2x2 matrix is nearly done and is the configuration closest to the paper. This cell is
# the interaction term: context L128 for Dream is 0.719, and knowing whether a shorter block helps
# there (as it did for Dream/TriviaQA, +0.105) or hurts (as for LLaDA/HotpotQA, -0.034) tests
# whether the purity-vs-truncation trade generalises across prompt types.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/ctx_l64_logs
mkdir -p "$LOG"
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1
set -a; . /root/autodl-tmp/.env.longcat; set +a
export MOMA_API_KEY="$LONGCAT_API_KEY"
log() { echo "$(date -Is) $*" >> "$LOG/driver.log"; }
EP="${LONGCAT_BASE_URL%/}/chat/completions"
TRAJ="$REPO/data/trajectories/tre_repro/dream_hotpotqa_bf16_L64_S64_B64_v1"
Q=data/tre_repro/questions/hotpotqa_eval800.jsonl
LAB=data/tre_repro/labels/dream_hotpotqa_ctx_l64
RES=results/tre_repro/dream_hotpotqa_ctx_l64

log "START dream_hotpot_ctx_l64"
.venv-dream/bin/python scripts/collect_dream.py --questions "$Q" --output "$TRAJ" \
  --precision bf16 --gen-length 64 --steps 64 --block-size 64 --seed 20261021 --resume \
  >> "$LOG/collect.log" 2>&1
log "collect rc=$?"
for pass in 1 2 3; do
  n=$(wc -l < "$LAB/paper_judgments.jsonl" 2>/dev/null || echo 0)
  log "judge pass $pass rows=$n"
  [ "$n" -ge 800 ] && break
  .venv/bin/python scripts/tre_repro/judge.py --run "$TRAJ" --questions "$Q" \
    --endpoint "$EP" --model "LongCat-2.5-Preview" \
    --output "$LAB/paper_judgments.jsonl" --raw-output "$LAB/judge_raw.jsonl" \
    --concurrency 3 --timeout 240 --retries 10 >> "$LOG/judge.log" 2>&1
  log "judge pass $pass rc=$?"
  sleep 20
done
if [ "$(wc -l < "$LAB/paper_judgments.jsonl" 2>/dev/null || echo 0)" -ge 800 ]; then
  .venv/bin/python scripts/score_tre_repro.py --run "$TRAJ" --questions "$Q" \
    --judgments "$LAB/paper_judgments.jsonl" --output "$RES" \
    --judge-prompt data/tre_repro/judge_prompt_v3.txt --bootstrap 1000 >> "$LOG/score.log" 2>&1
  log "score rc=$?"
fi
log "dream_hotpot_ctx_l64 done"
