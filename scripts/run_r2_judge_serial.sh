#!/usr/bin/env bash
# Serial R2 judging: 1 worker, paced, high retries.
# Concurrency 4 and 2 both drew 429s; the endpoint's limit is low enough that only a
# serial loop with a minimum interval sustains throughput. At ~3 s/call and ~1.6 calls
# per sample the remaining 443 samples are about 35-40 minutes, which fits the morning.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/r2_judge_logs
cd "$REPO" || exit 1
set -a; . /root/autodl-tmp/.env.judge; set +a
log() { echo "$(date -Is) $*" >> "$LOG/serial.log"; }
RUN=data/trajectories/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1
Q=data/tre_repro/questions/hotpotqa_eval800.jsonl
OUT=data/tre_repro/labels/llada_hotpotqa_fp16_L128_S64_B128_v1/paper_judgments.jsonl

log "serial judge start"
for pass in 1 2 3 4; do
  n=$(wc -l < "$OUT" 2>/dev/null || echo 0)
  log "pass $pass, rows=$n"
  [ "$n" -ge 800 ] && break
  .venv/bin/python scripts/tre_repro/judge.py --run "$RUN" --questions "$Q" \
    --endpoint "$JUDGE_ENDPOINT" --model "$JUDGE_MODEL" \
    --concurrency 1 --timeout 240 --retries 10 --min-interval 1.2 \
    >> "$LOG/judge_serial.log" 2>&1
  log "pass $pass rc=$? rows=$(wc -l < "$OUT")"
  sleep 30
done
log "serial judge done rows=$(wc -l < "$OUT")"
