#!/usr/bin/env bash
# Judge + score the Dream x TriviaQA run after collection.
# Same frozen prompt v3, same vendor as the other post-moma runs (vankit), serial pacing.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/dream_tre_logs
cd "$REPO" || exit 1
set -a; . /root/autodl-tmp/.env.judge; set +a
log() { echo "$(date -Is) $*" >> "$LOG/judge_driver.log"; }
RUN="$REPO/data/trajectories/tre_repro/dream_triviaqa_bf16_L128_S64_B128_v1"
Q=data/tre_repro/questions/triviaqa_eval800.jsonl
OUT=data/tre_repro/labels/dream_triviaqa_bf16_L128_S64_B128_v1/paper_judgments.jsonl

while pgrep -f "collect_dream.py.*triviaqa_eval800" >/dev/null; do sleep 60; done
log "collection finished"
[ -f "$RUN/manifest.json" ] || { log "FATAL no manifest"; exit 1; }

for pass in 1 2 3 4; do
  n=$(wc -l < "$OUT" 2>/dev/null || echo 0)
  log "pass $pass rows=$n"
  [ "$n" -ge 800 ] && break
  .venv/bin/python scripts/tre_repro/judge.py --run "$RUN" --questions "$Q" \
    --endpoint "$JUDGE_ENDPOINT" --model "$JUDGE_MODEL" \
    --concurrency 1 --timeout 240 --retries 10 --min-interval 1.2 \
    >> "$LOG/judge_run.log" 2>&1
  log "pass $pass rc=$? rows=$(wc -l < "$OUT" 2>/dev/null || echo 0)"
  sleep 30
done

.venv/bin/python scripts/score_tre_repro.py --run "$RUN" --questions "$Q" \
  --judgments "$OUT" --output "results/tre_repro/dream_triviaqa_bf16_L128_S64_B128_v1" \
  --judge-prompt data/tre_repro/judge_prompt_v3.txt --bootstrap 1000 \
  >> "$LOG/score.log" 2>&1
log "score rc=$?"
if [ -f results/tre_repro/dream_triviaqa_bf16_L128_S64_B128_v1/scores.csv ]; then
  .venv/bin/python scripts/tre_repro/permutation_test.py \
    --scores results/tre_repro/dream_triviaqa_bf16_L128_S64_B128_v1/scores.csv \
    --out reports/tre_repro/dream_triviaqa_permutation_test.json --permutations 10000 \
    >> "$LOG/perm.log" 2>&1
  log "permutation rc=$?"
fi
log "dream pipeline done"
