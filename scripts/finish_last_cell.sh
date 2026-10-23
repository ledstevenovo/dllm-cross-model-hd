#!/usr/bin/env bash
# After the last cell is scored, run the checks the other cells have: permutation test,
# detector comparison, the 12-cell table, and the pre-registered prediction check.
#
# Waits on the score file rather than a process, so it does not matter which pass produced it.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/llada_ctx_l64_logs
cd "$REPO" || exit 1
log() { echo "$(date -Is) $*" >> "$LOG/finish.log"; }

RUN=data/trajectories/tre_repro/llada_hotpotqa_fp16_L64_S64_B64_v1
Q=data/tre_repro/questions/hotpotqa_eval800.jsonl
RES=results/tre_repro/llada_hotpotqa_ctx_l64

log "waiting for $RES/metrics.json"
while [ ! -f "$RES/metrics.json" ]; do sleep 60; done
log "scored"

.venv/bin/python scripts/tre_repro/permutation_test.py \
  --scores "$RES/scores.csv" --out reports/tre_repro/finish_ctx_l64_permutation.json \
  --permutations 10000 >> "$LOG/finish_perm.log" 2>&1
log "permutation rc=$?"

.venv/bin/python scripts/fair_detector_comparison.py --run "$RUN" --questions "$Q" \
  --judgments data/tre_repro/labels/llada_hotpotqa_ctx_l64/paper_judgments.jsonl \
  --out reports/tre_repro/fair_det_llada_hp_ctx_l64.json >> "$LOG/finish_det.log" 2>&1
log "fair detector rc=$?"

.venv/bin/python scripts/tre_table.py >> "$LOG/finish_table.log" 2>&1
log "table rc=$?"

.venv/bin/python scripts/audit_paper_numbers.py >> "$LOG/finish_audit.log" 2>&1
log "audit rc=$?"

log "done"
