#!/usr/bin/env bash
# Re-judge R2 (LLaDA x HotpotQA) with LongCat, so LLaDA and Dream can be compared on this
# dataset under the SAME judge.
#
# R2's published number (0.706) used deepseek plus a third-judge arbitration, while
# Dream x HotpotQA had to switch to LongCat when deepseek degraded. Comparing the two models
# would otherwise mix a model difference with a judge difference. Re-judging R2 costs no GPU
# (~75 min of API) and removes that confound.
#
# Output goes to a separate label directory: the published R2 file is left untouched, and the
# two are compared rather than merged.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/dream_hotpot_logs
cd "$REPO" || exit 1
set -a; . /root/autodl-tmp/.env.longcat; set +a
export MOMA_API_KEY="$LONGCAT_API_KEY"
log() { echo "$(date -Is) $*" >> "$LOG/r2_longcat.log"; }
RUN="$REPO/data/trajectories/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1"
Q=data/tre_repro/questions/hotpotqa_eval800.jsonl
OUTDIR=data/tre_repro/labels/llada_hotpotqa_longcat
OUT="$OUTDIR/paper_judgments.jsonl"
EP="${LONGCAT_BASE_URL%/}/chat/completions"

log "r2 longcat start"
for pass in 1 2 3 4; do
  n=$(wc -l < "$OUT" 2>/dev/null || echo 0)
  log "pass $pass rows=$n"
  [ "$n" -ge 800 ] && break
  .venv/bin/python scripts/tre_repro/judge.py --run "$RUN" --questions "$Q" \
    --endpoint "$EP" --model "LongCat-2.5-Preview" \
    --output "$OUT" --raw-output "$OUTDIR/judge_raw.jsonl" \
    --concurrency 3 --timeout 240 --retries 10 \
    >> "$LOG/r2_longcat_judge.log" 2>&1
  log "pass $pass rc=$? rows=$(wc -l < "$OUT" 2>/dev/null || echo 0)"
  sleep 20
done

if [ -f "$OUT" ] && [ "$(wc -l < "$OUT")" -ge 800 ]; then
  .venv/bin/python scripts/score_tre_repro.py --run "$RUN" --questions "$Q" \
    --judgments "$OUT" --output results/tre_repro/llada_hotpotqa_longcat \
    --judge-prompt data/tre_repro/judge_prompt_v3.txt --bootstrap 1000 \
    >> "$LOG/r2_longcat_score.log" 2>&1
  log "score rc=$?"
  .venv/bin/python scripts/tre_vs_detectors.py --run "$RUN" --questions "$Q" --judgments "$OUT" \
    --out reports/tre_repro/tre_vs_detectors_llada_hotpotqa_longcat.json \
    >> "$LOG/r2_longcat_detectors.log" 2>&1
  log "detectors rc=$?"
fi
log "r2 longcat done"
