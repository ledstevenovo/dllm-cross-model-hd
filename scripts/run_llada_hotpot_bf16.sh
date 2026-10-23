#!/usr/bin/env bash
# LLaDA x TriviaQA at llada_hotpot_bf16, to test the prediction from budget_final_answer.md:
# if the net budget loss for LLaDA is truncation rather than block size, then a budget well above
# its answer-length p95 (~62) should remove truncation and turn the effect positive relative to L128.
#
# This is the one experiment that distinguishes "model-dependent" from "truncation-dependent".
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/precision_logs
mkdir -p "$LOG"
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1
set -a; . /root/autodl-tmp/.env.longcat; set +a
export MOMA_API_KEY="$LONGCAT_API_KEY"
log() { echo "$(date -Is) $*" >> "$LOG/driver.log"; }
EP="${LONGCAT_BASE_URL%/}/chat/completions"
TRAJ="$REPO/data/trajectories/tre_repro/llada_hotpotqa_bare_bf16_L128_S64_B128_v1"
Q=data/tre_repro/questions/hotpotqa_bare800.jsonl
LAB=data/tre_repro/labels/llada_hotpotqa_bare_bf16_longcat
RES=results/tre_repro/llada_hotpotqa_bare_bf16_longcat

log "START llada_hotpot_bf16"
.venv-llada/bin/python scripts/collect_llada.py --questions "$Q" --output "$TRAJ" \
  --precision bf16 --gen-length 128 --steps 64 --block-size 128 --seed 20261021 --resume \
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
log "llada_hotpot_bf16 done"
