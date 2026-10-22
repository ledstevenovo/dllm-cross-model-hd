#!/usr/bin/env bash
# Wait for the R2 800-question collection to finish, then relocate it and judge.
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/r2_judge_logs
STRAY=/root/autodl-tmp/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1
DEST="$REPO/data/trajectories/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1"
mkdir -p "$LOG"
cd "$REPO" || exit 1
log() { echo "$(date -Is) $*" >> "$LOG/watch.log"; }
log "watch start"

# wait until the collector process exits
while pgrep -f "collect_llada.py.*hotpotqa_eval800" >/dev/null; do sleep 60; done
log "collector exited"

if [ -d "$STRAY" ] && [ ! -d "$DEST" ]; then
  mkdir -p "$(dirname "$DEST")"
  mv "$STRAY" "$DEST" && log "moved to $DEST"
fi
[ -d "$DEST" ] || { log "FATAL no run dir"; exit 1; }

# integrity preflight
"$REPO/.venv/bin/python" - <<'PY' >> "$LOG/preflight.log" 2>&1
import json, sys
from pathlib import Path
sys.path.insert(0, '/root/autodl-tmp/dllm-cross-model-hd')
from src.tre_repro import load_questions
run = Path('/root/autodl-tmp/dllm-cross-model-hd/data/trajectories/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1')
man = json.loads((run / 'manifest.json').read_text())
qs = {q.sample_id for q in load_questions('/root/autodl-tmp/dllm-cross-model-hd/data/tre_repro/questions/hotpotqa_eval800.jsonl')}
got = set(man['samples'])
print('traces', len(got), 'expected', len(qs), 'missing', len(qs - got), 'extra', len(got - qs))
print('status', man['status'], 'errors', len(man['errors']))
if len(got) != len(qs) or (qs - got):
    raise SystemExit('INCOMPLETE')
PY
rc=$?
log "preflight rc=$rc"
[ $rc -ne 0 ] && exit 1

log "watch done"
