#!/usr/bin/env bash
# Rejudge four TriviaQA runs with LongCat so the budget comparison is judge-clean.
#
# Why: the L64 cells ended up on a different judge than their L128 counterparts (Dream vankit ->
# LongCat, LLaDA deepseek -> deepseek under a different endpoint). Since switching judge moved
# HotpotQA by 0.063, the budget effect (-0.082 / +0.105) cannot be trusted while the judge also
# changed. This rejudges all four into separate directories and leaves the published labels
# untouched; the comparison is then made between the LongCat versions.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/rejudge_logs
mkdir -p "$LOG"
cd "$REPO" || exit 1
set -a; . /root/autodl-tmp/.env.longcat; set +a
export MOMA_API_KEY="$LONGCAT_API_KEY"
log() { echo "$(date -Is) $*" >> "$LOG/driver.log"; }
EP="${LONGCAT_BASE_URL%/}/chat/completions"

cell() {  # cell <tag> <traj> <questions> <labels> <results>
  local tag="$1" TRAJ="$2" Q="$3" LAB="$4" RES="$5"
  log "START $tag"
  for pass in 1 2 3 4; do
    local n; n=$(wc -l < "$LAB/paper_judgments.jsonl" 2>/dev/null || echo 0)
    [ "$n" -ge 800 ] && break
    log "$tag pass $pass rows=$n"
    .venv/bin/python scripts/tre_repro/judge.py --run "$TRAJ" --questions "$Q" \
      --endpoint "$EP" --model "LongCat-2.5-Preview" \
      --output "$LAB/paper_judgments.jsonl" --raw-output "$LAB/judge_raw.jsonl" \
      --concurrency 3 --timeout 240 --retries 10 >> "$LOG/${tag}.log" 2>&1
    log "$tag pass $pass rc=$?"
    sleep 20
  done
  if [ "$(wc -l < "$LAB/paper_judgments.jsonl" 2>/dev/null || echo 0)" -ge 800 ]; then
    .venv/bin/python scripts/score_tre_repro.py --run "$TRAJ" --questions "$Q" \
      --judgments "$LAB/paper_judgments.jsonl" --output "$RES" \
      --judge-prompt data/tre_repro/judge_prompt_v3.txt --bootstrap 1000 \
      >> "$LOG/${tag}_score.log" 2>&1
    log "$tag score rc=$?"
  fi
  log "END $tag"
}

TQ=data/tre_repro/questions/triviaqa_eval800.jsonl
cell llada_tq_128 data/trajectories/tre_repro/llada_triviaqa_fp16_L128_S64_B128_v3 "$TQ" \
  data/tre_repro/labels/llada_triviaqa_l128_longcat results/tre_repro/llada_triviaqa_l128_longcat
cell llada_tq_64 data/trajectories/tre_repro/llada_triviaqa_fp16_L64_S64_B64_v1 "$TQ" \
  data/tre_repro/labels/llada_triviaqa_l64_longcat results/tre_repro/llada_triviaqa_l64_longcat
cell dream_tq_128 data/trajectories/tre_repro/dream_triviaqa_bf16_L128_S64_B128_v1 "$TQ" \
  data/tre_repro/labels/dream_triviaqa_l128_longcat results/tre_repro/dream_triviaqa_l128_longcat
log "all done"
