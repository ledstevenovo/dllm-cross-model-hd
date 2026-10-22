#!/usr/bin/env bash
# ==============================================================================
# TRE R2 收尾：等 R2 采集结束 → judge → 打分
# ==============================================================================
# R2（HotpotQA × LLaDA）的轨迹由 scripts/run_gpu_queue.sh 采集。本脚本接在它后面，
# 把轨迹变成能写进论文表 1 的数字。
#
# judge 口径（必须与记录一致，不能事后改）：
#   * 冻结提示词 v3（sha256 校验，漂移即拒跑）；
#   * 模型 deepseek-v4.1-flash，端点 sub.vankit.top（与 R1 的 moma 端点不同）；
#   * 因为端点不同，R2 的标签单独一个目录、单独一个 judge 口径，**不与 R1 混用**。
#     两者的可比性由 reports/tre_repro/judge_crosscheck.json 量化（100/100 解决，
#     一致率 0.990 / κ 0.979），在论文里作为"同模型不同供应商"的协议差异记录。
#
# 用法：screen -dmS r2_judge bash scripts/run_r2_judge.sh
# ==============================================================================
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/r2_judge_logs
PY="$REPO/.venv/bin/python"
# The 800-question run was launched with an absolute path that dropped the
# data/trajectories/tre_repro prefix (a bug in run_gpu_queue.sh, fixed there), so the
# trajectories live outside the repo.  Accept either location: prefer the repo copy and
# fall back to the absolute one, then move it into place so every downstream path works.
QUESTIONS=data/tre_repro/questions/hotpotqa_eval800.jsonl
STRAY=/root/autodl-tmp/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1
RUN=data/trajectories/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1
mkdir -p "$LOG" || exit 1
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache
export HF_HUB_OFFLINE=1
set -a
# shellcheck disable=SC1091
. /root/autodl-tmp/.env.judge
set +a

log() { echo "$(date -Is) $*" >> "$LOG/driver.log"; }
log "r2_judge start pid=$$"

# 1. 等 R2 采集完成（gpuqueue 写 "END r2_hotpotqa_800"）
while ! grep -qE "END r2_hotpotqa_800 rc=0|SKIP r2_hotpotqa_800" /root/autodl-tmp/tre_r2_logs/queue.log 2>/dev/null; do
  sleep 60
done
log "R2 collection finished"

# Relocate the run into the repo if it was written to the stray absolute path.
if [ -d "$STRAY" ] && [ ! -d "$RUN" ]; then
  mkdir -p "$(dirname "$RUN")"
  mv "$STRAY" "$RUN" && log "moved $STRAY -> $RUN"
elif [ -d "$STRAY" ] && [ -d "$RUN" ]; then
  log "WARNING both $STRAY and $RUN exist; refusing to merge, judging $RUN"
fi
if [ ! -d "$RUN" ]; then
  log "FATAL: no R2 run at $RUN or $STRAY"
  exit 1
fi

# 2. 完整性预检：轨迹数、配置一致性、prompt 往返
"$PY" - <<'PY' >> "$LOG/preflight.log" 2>&1
import json, sys
from pathlib import Path
sys.path.insert(0, '/root/autodl-tmp/dllm-cross-model-hd')
from src.tre_repro import load_questions
run = Path('/root/autodl-tmp/dllm-cross-model-hd/data/trajectories/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1')
man = json.loads((run / 'manifest.json').read_text())
qs = {q.sample_id: q for q in load_questions('/root/autodl-tmp/dllm-cross-model-hd/data/tre_repro/questions/hotpotqa_eval800.jsonl')}
got = set(man['samples'])
print('traces', len(got), 'expected', len(qs), 'missing', len(set(qs) - got), 'extra', len(got - set(qs)))
ident = man['identity']
print('decoding', ident['decoding'], 'seed', ident['seed'], 'precision', ident['precision'])
print('gpu', ident['environment']['gpu'], 'verify_observer', ident['verify_observer'])
if len(got) != len(qs) or set(qs) - got:
    raise SystemExit('INCOMPLETE: refusing to judge a partial run')
PY
rc=$?
log "preflight rc=$rc"
[ $rc -ne 0 ] && { log "preflight failed; stopping"; exit 1; }

# 3. judge（新端点，单独目录；--retry-needs-review 收尾限流残留）
for attempt in 1 2 3; do
  log "judge attempt $attempt"
  "$PY" scripts/tre_repro/judge.py \
    --run "$RUN" --questions "$QUESTIONS" \
    --endpoint "$JUDGE_ENDPOINT" --model "$JUDGE_MODEL" \
    --concurrency 4 --timeout 180 --retries 5 >> "$LOG/judge.log" 2>&1
  rc=$?
  log "judge attempt $attempt rc=$rc"
  [ $rc -eq 0 ] && break
  sleep 30
done

# 4. 收尾：重判 needs_review（限流/超时留下的）
"$PY" scripts/tre_repro/judge.py \
  --run "$RUN" --questions "$QUESTIONS" \
  --endpoint "$JUDGE_ENDPOINT" --model "$JUDGE_MODEL" \
  --concurrency 2 --timeout 180 --retries 6 --retry-needs-review >> "$LOG/judge_retry.log" 2>&1
log "judge retry rc=$?"

# 5. 打分（预注册主口径 tre；门禁会拦 needs_review）
"$PY" scripts/score_tre_repro.py \
  --run "$RUN" --questions "$QUESTIONS" \
  --judgments "data/tre_repro/labels/llada_hotpotqa_fp16_L128_S64_B128_v1/paper_judgments.jsonl" \
  --output results/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1 \
  --judge-prompt data/tre_repro/judge_prompt_v3.txt --bootstrap 1000 \
  >> "$LOG/score.log" 2>&1
log "score rc=$?"

# 6. 置换检验（TRE 也应有 p 值）
if [ -f results/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1/scores.csv ]; then
  "$PY" scripts/tre_repro/permutation_test.py \
    --scores results/tre_repro/llada_hotpotqa_fp16_L128_S64_B128_v1/scores.csv \
    --out reports/tre_repro/r2_permutation_test.json --permutations 10000 \
    >> "$LOG/permutation.log" 2>&1
  log "permutation rc=$?"
fi

log "r2_judge done"
