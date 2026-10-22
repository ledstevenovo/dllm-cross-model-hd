#!/usr/bin/env bash
# Judge the TriviaQA L64 run after collection, then score it.
#
# Judge note: R1's labels came from moma, which no longer authenticates (401). This run
# therefore uses the vankit endpoint, and the two are NOT silently merged: the cross-vendor
# agreement was measured at 0.990 / kappa 0.979 over 100 rows
# (reports/tre_repro/judge_crosscheck.json), and any L64-vs-R1 comparison must carry that
# as a protocol difference. Same frozen prompt v3 either way.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/tre_r2_logs
cd "$REPO" || exit 1
set -a; . /root/autodl-tmp/.env.judge; set +a
log() { echo "$(date -Is) $*" >> "$LOG/l64_judge.log"; }
RUN="$REPO/data/trajectories/tre_repro/llada_triviaqa_fp16_L64_S64_B64_v1"
Q=data/tre_repro/questions/triviaqa_eval800.jsonl
OUT=data/tre_repro/labels/llada_triviaqa_fp16_L64_S64_B64_v1/paper_judgments.jsonl

while pgrep -f "collect_llada.py.*triviaqa_eval800.*L64" >/dev/null; do sleep 60; done
log "collection finished"

if [ ! -f "$RUN/manifest.json" ]; then log "FATAL no manifest"; exit 1; fi
# serial with pacing: this endpoint 429s under any real concurrency
for pass in 1 2 3; do
  n=$(wc -l < "$OUT" 2>/dev/null || echo 0)
  log "pass $pass rows=$n"
  [ "$n" -ge 800 ] && break
  .venv/bin/python scripts/tre_repro/judge.py --run "$RUN" --questions "$Q" \
    --endpoint "$JUDGE_ENDPOINT" --model "$JUDGE_MODEL" \
    --concurrency 1 --timeout 240 --retries 10 --min-interval 1.2 \
    >> "$LOG/l64_judge_run.log" 2>&1
  log "pass $pass rc=$? rows=$(wc -l < "$OUT" 2>/dev/null || echo 0)"
  sleep 30
done

.venv/bin/python scripts/score_tre_repro.py --run "$RUN" --questions "$Q" \
  --judgments "$OUT" --output results/tre_repro/llada_triviaqa_fp16_L64_S64_B64_v1 \
  --judge-prompt data/tre_repro/judge_prompt_v3.txt --bootstrap 1000 \
  >> "$LOG/l64_score.log" 2>&1
log "score rc=$?"
if [ -f results/tre_repro/llada_triviaqa_fp16_L64_S64_B64_v1/scores.csv ]; then
  .venv/bin/python scripts/tre_repro/permutation_test.py \
    --scores results/tre_repro/llada_triviaqa_fp16_L64_S64_B64_v1/scores.csv \
    --out reports/tre_repro/r2_l64_permutation_test.json --permutations 10000 \
    >> "$LOG/l64_perm.log" 2>&1
  log "permutation rc=$?"
fi
log "l64 pipeline done"
