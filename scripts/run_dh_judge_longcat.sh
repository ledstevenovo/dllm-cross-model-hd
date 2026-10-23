#!/usr/bin/env bash
# Judge Dream x HotpotQA with LongCat-2.5-Preview, start to finish, one judge for the file.
#
# Why LongCat: the deepseek endpoint slowed from 2.6 s to ~12 s per call, which would have
# pushed the run past 18:00. The project rule is "one label file, one judge", so this does not
# splice: the partial deepseek file (202 rows) is archived and this run judges all 800 fresh.
# Cross-judge agreement on a 57-row stratified sample of this dataset was 0.965 / kappa 0.916,
# so the switch is measured rather than assumed.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/dream_hotpot_logs
cd "$REPO" || exit 1
set -a; . /root/autodl-tmp/.env.longcat; set +a
# scripts/tre_repro/judge.py reads MOMA_API_KEY by name (its original vendor). The credential
# here is LongCat's, so alias it rather than editing the judge client's variable contract.
export MOMA_API_KEY="$LONGCAT_API_KEY"
log() { echo "$(date -Is) $*" >> "$LOG/longcat.log"; }
RUN="$REPO/data/trajectories/tre_repro/dream_hotpotqa_bf16_L128_S64_B128_v1"
Q=data/tre_repro/questions/hotpotqa_eval800.jsonl
OUT=data/tre_repro/labels/dream_hotpotqa_bf16_L128_S64_B128_v1/paper_judgments.jsonl
EP="${LONGCAT_BASE_URL%/}/chat/completions"

log "longcat judge start"
for pass in 1 2 3 4; do
  n=$(wc -l < "$OUT" 2>/dev/null || echo 0)
  log "pass $pass rows=$n"
  [ "$n" -ge 800 ] && break
  .venv/bin/python scripts/tre_repro/judge.py --run "$RUN" --questions "$Q" \
    --endpoint "$EP" --model "LongCat-2.5-Preview" \
    --concurrency 3 --timeout 240 --retries 10 \
    >> "$LOG/judge_longcat.log" 2>&1
  log "pass $pass rc=$? rows=$(wc -l < "$OUT" 2>/dev/null || echo 0)"
  sleep 20
done

if [ -f "$OUT" ] && [ "$(wc -l < "$OUT")" -ge 800 ]; then
  .venv/bin/python scripts/score_tre_repro.py --run "$RUN" --questions "$Q" \
    --judgments "$OUT" --output "results/tre_repro/dream_hotpotqa_bf16_L128_S64_B128_v1" \
    --judge-prompt data/tre_repro/judge_prompt_v3.txt --bootstrap 1000 \
    >> "$LOG/score.log" 2>&1
  log "score rc=$?"
  .venv/bin/python scripts/tre_repro/permutation_test.py \
    --scores results/tre_repro/dream_hotpotqa_bf16_L128_S64_B128_v1/scores.csv \
    --out reports/tre_repro/dream_hotpotqa_permutation_test.json --permutations 10000 \
    >> "$LOG/perm.log" 2>&1
  log "permutation rc=$?"
  .venv/bin/python scripts/tre_vs_detectors.py --run "$RUN" --questions "$Q" --judgments "$OUT" \
    --out reports/tre_repro/tre_vs_detectors_dream_hotpotqa.json >> "$LOG/detectors.log" 2>&1
  log "tre_vs_detectors rc=$?"
  .venv/bin/python scripts/dream_hotpot_post.py >> "$LOG/post.log" 2>&1
  log "five-cell rc=$?"
fi
log "longcat pipeline done"
