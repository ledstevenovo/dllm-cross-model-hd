#!/usr/bin/env bash
# Judge R2 at a rate the endpoint tolerates.
# The first attempt at concurrency 4 hit 429s within minutes; 2 workers with a small
# minimum interval and more retries is slower but finishes, which is what matters at 07:30.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/r2_judge_logs
cd "$REPO" || exit 1
set -a; . /root/autodl-tmp/.env.judge; set +a
log() { echo "$(date -Is) $*" >> "$LOG/slow.log"; }
RUN=data/trajectories/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1
Q=data/tre_repro/questions/hotpotqa_eval800.jsonl

log "slow judge start"
for pass in 1 2 3; do
  log "pass $pass concurrency=2"
  .venv/bin/python scripts/tre_repro/judge.py --run "$RUN" --questions "$Q" \
    --endpoint "$JUDGE_ENDPOINT" --model "$JUDGE_MODEL" \
    --concurrency 2 --timeout 180 --retries 8 --min-interval 0.8 \
    >> "$LOG/judge_slow.log" 2>&1
  log "pass $pass rc=$?"
  # stop early if everything resolved
  n=$(wc -l < "data/tre_repro/labels/llada_hotpotqa_fp16_L128_S64_B128_v1/paper_judgments.jsonl" 2>/dev/null || echo 0)
  log "rows now $n"
  [ "$n" -ge 800 ] && break
  sleep 60
done
log "slow judge done rows=$(wc -l < data/tre_repro/labels/llada_hotpotqa_fp16_L128_S64_B128_v1/paper_judgments.jsonl)"
