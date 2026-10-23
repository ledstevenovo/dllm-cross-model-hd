#!/usr/bin/env bash
# Complete the 2x2x2 matrix: Dream at L64 on both datasets, then judge and score.
#
# TriviaQA uses the frozen R1 list (bare questions); HotpotQA uses the derived bare list so the
# budget comparison is not confounded by prompt type. Both judged with LongCat for consistency
# with the other post-moma runs.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/dream_l64_logs
mkdir -p "$LOG"
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1
set -a; . /root/autodl-tmp/.env.longcat; set +a
export MOMA_API_KEY="$LONGCAT_API_KEY"
log() { echo "$(date -Is) $*" >> "$LOG/driver.log"; }
EP="${LONGCAT_BASE_URL%/}/chat/completions"

run_cell() {  # run_cell <tag> <questions> <traj> <labels> <results>
  local tag="$1" Q="$2" TRAJ="$3" LAB="$4" RES="$5"
  log "START $tag"
  .venv-dream/bin/python scripts/collect_dream.py --questions "$Q" --output "$TRAJ" \
    --precision bf16 --gen-length 64 --steps 64 --block-size 64 --seed 20261021 --resume \
    >> "$LOG/${tag}_collect.log" 2>&1
  log "$tag collect rc=$?"
  for pass in 1 2 3; do
    local n; n=$(wc -l < "$LAB/paper_judgments.jsonl" 2>/dev/null || echo 0)
    log "$tag judge pass $pass rows=$n"
    [ "$n" -ge 800 ] && break
    .venv/bin/python scripts/tre_repro/judge.py --run "$TRAJ" --questions "$Q" \
      --endpoint "$EP" --model "LongCat-2.5-Preview" \
      --output "$LAB/paper_judgments.jsonl" --raw-output "$LAB/judge_raw.jsonl" \
      --concurrency 3 --timeout 240 --retries 10 >> "$LOG/${tag}_judge.log" 2>&1
    log "$tag judge pass $pass rc=$?"
    sleep 20
  done
  if [ "$(wc -l < "$LAB/paper_judgments.jsonl" 2>/dev/null || echo 0)" -ge 800 ]; then
    .venv/bin/python scripts/score_tre_repro.py --run "$TRAJ" --questions "$Q" \
      --judgments "$LAB/paper_judgments.jsonl" --output "$RES" \
      --judge-prompt data/tre_repro/judge_prompt_v3.txt --bootstrap 1000 \
      >> "$LOG/${tag}_score.log" 2>&1
    log "$tag score rc=$?"
    .venv/bin/python scripts/tre_vs_detectors.py --run "$TRAJ" --questions "$Q" \
      --judgments "$LAB/paper_judgments.jsonl" --out "reports/tre_repro/tre_vs_detectors_${tag}.json" \
      >> "$LOG/${tag}_detectors.log" 2>&1
    log "$tag detectors rc=$?"
  fi
  log "END $tag"
}

run_cell dream_triviaqa_l64 data/tre_repro/questions/triviaqa_eval800.jsonl \
  "$REPO/data/trajectories/tre_repro/dream_triviaqa_bf16_L64_S64_B64_v1" \
  "data/tre_repro/labels/dream_triviaqa_bf16_L64_S64_B64_v1" \
  "results/tre_repro/dream_triviaqa_bf16_L64_S64_B64_v1"

run_cell dream_hotpotqa_bare_l64 data/tre_repro/questions/hotpotqa_bare800.jsonl \
  "$REPO/data/trajectories/tre_repro/dream_hotpotqa_bare_bf16_L64_S64_B64_v1" \
  "data/tre_repro/labels/dream_hotpotqa_bare_l64" \
  "results/tre_repro/dream_hotpotqa_bare_l64"

log "both cells done"
