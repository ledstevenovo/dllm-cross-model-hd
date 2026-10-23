#!/usr/bin/env bash
# LLaDA x HotpotQA with the context REMOVED (bare question), then judge with LongCat.
#
# Control for R2: isolates whether the ~11-point shortfall comes from the context-grounded
# prompt or from HotpotQA's multi-hop nature. Same 800 questions, same seed, same judge as the
# LongCat HotpotQA pairs, so the only change is the absence of distractor paragraphs.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/bare_logs
OUT="$REPO/data/trajectories/tre_repro/llada_hotpotqa_bare_fp16_L128_S64_B128_v1"
mkdir -p "$LOG"
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1
set -a; . /root/autodl-tmp/.env.longcat; set +a
export MOMA_API_KEY="$LONGCAT_API_KEY"
log() { echo "$(date -Is) $*" >> "$LOG/driver.log"; }

log "bare start"
.venv-llada/bin/python scripts/collect_llada.py \
  --questions data/tre_repro/questions/hotpotqa_bare800.jsonl \
  --output "$OUT" --precision float16 \
  --gen-length 128 --steps 64 --block-size 128 --seed 20261021 --resume \
  >> "$LOG/collect.log" 2>&1
log "collect rc=$? $(date -Is)"

Q=data/tre_repro/questions/hotpotqa_bare800.jsonl
OUTL=data/tre_repro/labels/llada_hotpotqa_bare_v1/paper_judgments.jsonl
EP="${LONGCAT_BASE_URL%/}/chat/completions"
for pass in 1 2 3; do
  n=$(wc -l < "$OUTL" 2>/dev/null || echo 0)
  log "judge pass $pass rows=$n"
  [ "$n" -ge 800 ] && break
  .venv/bin/python scripts/tre_repro/judge.py --run "$OUT" --questions "$Q" \
    --endpoint "$EP" --model "LongCat-2.5-Preview" \
    --output "$OUTL" --raw-output "$(dirname "$OUTL")/judge_raw.jsonl" \
    --concurrency 3 --timeout 240 --retries 10 >> "$LOG/judge.log" 2>&1
  log "judge pass $pass rc=$? rows=$(wc -l < "$OUTL" 2>/dev/null || echo 0)"
  sleep 20
done

if [ -f "$OUTL" ] && [ "$(wc -l < "$OUTL")" -ge 800 ]; then
  .venv/bin/python scripts/score_tre_repro.py --run "$OUT" --questions "$Q" \
    --judgments "$OUTL" --output results/tre_repro/llada_hotpotqa_bare_v1 \
    --judge-prompt data/tre_repro/judge_prompt_v3.txt --bootstrap 1000 \
    >> "$LOG/score.log" 2>&1
  log "score rc=$?"
  .venv/bin/python scripts/tre_repro/permutation_test.py \
    --scores results/tre_repro/llada_hotpotqa_bare_v1/scores.csv \
    --out reports/tre_repro/hotpotqa_bare_permutation_test.json --permutations 10000 \
    >> "$LOG/perm.log" 2>&1
  log "perm rc=$?"
fi
log "bare done"
