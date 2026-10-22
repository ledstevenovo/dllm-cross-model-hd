#!/usr/bin/env bash
# ==============================================================================
# 整夜有卡队列 —— 2026-10-23 02:10 起
# ==============================================================================
# 先等 pool2000 的 Dream 采集结束，再按"先出结论、后出稳健性"的顺序推进。
# 每步可重入：产物已存在就跳过；失败重试 3 次（5/20/45 秒退避）；单步失败不中断队列。
#
# 排序理由：夜里可能跑不完。先跑能回答预注册判据的步骤（迁移矩阵 → 置换 →
# 对齐 → 消融），再跑耗时的稳健性（稳定性 ×2 种子、多种子）。这样即使 08:00
# 被掐，核心结论已经在盘上。
#
# 红线（不因赶进度放松）：
#   * 同一张迁移矩阵的轨迹必须同设备。pool2000 与 pilot200 全量来自本机 4080 SUPER。
#   * 标签必须 human_reviewed=true 且 label_source=human:<reviewer> 才进正式指标；
#     rule-signoff 晋升时如实署名，不伪装成逐条人工。
#   * 不同 judge / 端点不拼进同一份标签。新 judge（vankit）只用于 R2 与
#     pool2000 的第二 judge 一致性，不改写 R1 的 moma 标签。
#   * 不用测试集调参。
#
# 用法：
#   screen -dmS night bash scripts/run_overnight_gpu.sh
#   tail -f /root/autodl-tmp/night_logs/driver.log
#   cat /root/autodl-tmp/night_logs/heartbeat.txt
# ==============================================================================
set -u

REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/night_logs
PY="$REPO/.venv/bin/python"
DONE="$LOG/.done"
REVIEWER="${REVIEWER:-ledstevenovo}"
SIGNED_OFF_AT="${SIGNED_OFF_AT:-$(date +%Y-%m-%d)}"
# concurrency 4: the endpoint 429s at 8 (30/100 during the cross-check). Every 429
# costs a retry, so slow-and-steady is faster overall overnight.
JUDGE_WORKERS="${JUDGE_WORKERS:-4}"
ATTEMPTS="${ATTEMPTS:-3}"
FORCE="${FORCE:-0}"
FAILED=""

mkdir -p "$LOG" "$DONE" || exit 1
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache
export HF_HUB_OFFLINE=1
export MPLBACKEND=Agg
set -a
# shellcheck disable=SC1091
. /root/autodl-tmp/.env.judge
set +a

log()  { echo "$(date -Is) $*" >> "$LOG/driver.log"; }
beat() { echo "$(date -Is) | $*" > "$LOG/heartbeat.txt"; }
is_done() { [ "$FORCE" != "1" ] && [ -f "$DONE/$1" ]; }
mark_done() { touch "$DONE/$1"; }

try() {  # try <attempts> <logfile> <cmd...>
  local attempts="$1" logfile="$2"; shift 2
  local i rc
  for i in $(seq 1 "$attempts"); do
    log "  attempt $i/$attempts: $*"
    "$@" >> "$logfile" 2>&1
    rc=$?
    log "  attempt $i rc=$rc"
    [ $rc -eq 0 ] && return 0
    [ "$i" -lt "$attempts" ] && sleep $((5 * i * i))
  done
  return $rc
}

step() {  # step <name> <logfile> <cmd...>
  local name="$1" logfile="$2"; shift 2
  if is_done "$name"; then log "SKIP $name"; beat "skip $name"; return 0; fi
  beat "running $name"
  log "START $name"
  if try "$ATTEMPTS" "$logfile" "$@"; then
    mark_done "$name"; log "OK $name"; beat "done $name"; return 0
  fi
  log "FAIL $name"
  FAILED="$FAILED $name"
  beat "failed $name"
  return 1
}

log "night queue start pid=$$ host=$(hostname)"

# ── 0. 等 pool2000 收完 ─────────────────────────────────────────────────────
beat "waiting for pool2000"
while ! grep -q "driver done" /root/autodl-tmp/pool2000_logs/driver.log 2>/dev/null; do
  sleep 60
done
log "pool2000 finished"

# ── 1. Dream 签核草案（LLaDA 的已在 01:25 完成）──────────────────────────
step 01_dream_draft 01_dream_draft.log \
  "$PY" scripts/draft_signoff_review.py \
    --questions data/raw_qa/subsets/pool2000_v1.jsonl \
    --run-root data/trajectories/bf16_pool2000 \
    --prefix pool2000 --models dream \
    --sheet reports/pool2000_draft_review.md

# ── 2. 晋升 reviewed（rule-signoff，署名与 pilot200 一致）──────────────
step 02_promote 02_promote.log bash -c "
  set -e
  for m in llada dream; do
    '$PY' scripts/finalize_reviewed_labels.py \
      --input data/labels/pool2000_\${m}.draft_review.jsonl \
      --out data/labels/pool2000_\${m}.reviewed.jsonl \
      --reviewer '$REVIEWER' --signed-off-at '$SIGNED_OFF_AT'
  done
"

# ── 3. 特征抽取（用 reviewed 标签）────────────────────────────────────────
step 03_extract 03_extract.log bash -c "
  set -e
  for m in llada dream; do
    '$PY' scripts/offline.py extract \
      --questions data/raw_qa/subsets/pool2000_v1.jsonl \
      --traces data/trajectories/bf16_pool2000/\${m} \
      --labels data/labels/pool2000_\${m}.reviewed.jsonl \
      --output data/features/pool2000_\${m}.parquet
  done
"

# ── 4. 合并 pilot200 + pool2000 = 2000 题全量 ─────────────────────────────
step 04_combine 04_combine.log bash -c "
  set -e
  '$PY' - <<'PY'
import pandas as pd
from pathlib import Path
frames = []
for model in ('llada', 'dream'):
    pilot = pd.read_parquet(f'data/features/pilot200_{model}.parquet')
    pool = pd.read_parquet(f'data/features/pool2000_{model}.parquet')
    both = pd.concat([pilot, pool], ignore_index=True)
    if both.duplicated(['model_id', 'sample_id']).any():
        raise SystemExit(f'duplicate sample ids in {model}')
    overlap = set(pilot.question_id) & set(pool.question_id)
    if overlap:
        raise SystemExit(f'{model}: {len(overlap)} questions in both pilot200 and pool2000')
    frames.append(both)
    print(model, 'pilot', len(pilot), '+ pool', len(pool), '=', len(both),
          'questions', both.question_id.nunique(),
          'eligible', int((both.human_reviewed & both.label.isin(['correct', 'incorrect'])).sum()))
combined = pd.concat(frames, ignore_index=True)
out = Path('results/pool2000/features_combined.parquet')
out.parent.mkdir(parents=True, exist_ok=True)
combined.to_parquet(out, index=False)
print('combined', len(combined), 'rows,', combined.question_id.nunique(), 'questions')
PY
"

# ── 5. 扩池迁移矩阵（预注册口径：entropy_raw / relative_normalized × LR/MLP）──
step 05_transfer 05_transfer.log \
  "$PY" scripts/offline.py evaluate \
    --features results/pool2000/features_combined.parquet \
    --output results/pool2000/main \
    --feature-sets entropy_raw relative_normalized \
    --kinds lr mlp --bootstrap 1000 --axis model

# ── 6. 预注册判据（唯一的"结论"步骤）────────────────────────────────────
step 06_verdict 06_verdict.log \
  "$PY" scripts/pool2000_verdict.py \
    --matrix results/pool2000/main/transfer_matrix.csv \
    --out reports/pool2000_verdict.json

# ── 7. 分层（hotpotqa / triviaqa）────────────────────────────────────────
step 07_strata 07_strata.log \
  "$PY" scripts/offline.py evaluate \
    --features results/pool2000/features_combined.parquet \
    --output results/pool2000/strata \
    --feature-sets entropy_raw relative_normalized \
    --kinds lr mlp --bootstrap 1000 --axis dataset

# ── 8. 簇级置换检验（回答"是不是噪声"）──────────────────────────────────
step 08_permutation 08_permutation.log \
  "$PY" scripts/main_permutation.py \
    --predictions results/pool2000/main/predictions.csv \
    --out reports/pool2000_permutation.json --permutations 10000

# ── 9. 尺度对齐诊断（异常格的机制）──────────────────────────────────────
step 09_alignment 09_alignment.log \
  "$PY" scripts/alignment_diagnostic.py \
    --features results/pool2000/features_combined.parquet \
    --out reports/pool2000_alignment_diagnostic.json

# ── 10. 全特征集消融（late_only 效应是否在扩池后保持）───────────────────
step 10_featuresets 10_featuresets.log \
  "$PY" scripts/offline.py evaluate \
    --features results/pool2000/features_combined.parquet \
    --output results/pool2000/featuresets \
    --feature-sets entropy_raw entropy_normalized early_only middle_only late_only \
      entropy_confidence absolute_time relative_time relative_normalized with_stability \
    --kinds lr mlp --bootstrap 500 --axis model

# ── 11. 第二 judge 一致性（新 judge，只做一致性，不改标签）──────────────
step 11_judge_consistency 11_judge_consistency.log \
  "$PY" scripts/judge_consistency_parallel.py \
    --subset data/raw_qa/subsets/pool2000_v1.jsonl \
    --trajectories data/trajectories/bf16_pool2000 \
    --labels data/labels --prefix pool2000 \
    --samples-per-model 500 \
    --out reports/pool2000_label_consistency.json \
    --endpoint "$JUDGE_ENDPOINT" --model "$JUDGE_MODEL" \
    --api-key-env MOMA_API_KEY --workers "$JUDGE_WORKERS"

# ── 12. 稳定性 ×2 种子（耗时最长，放最后）───────────────────────────────
step 12_stability 12_stability.log \
  "$PY" scripts/stability_study.py \
    --features results/pool2000/features_combined.parquet \
    --out reports/pool2000_stability.json --repeats 300 --seed 20261021

step 13_stability_seed2 13_stability_seed2.log \
  "$PY" scripts/stability_study.py \
    --features results/pool2000/features_combined.parquet \
    --out reports/pool2000_stability_seed2.json --repeats 300 --seed 20261022

step 14_two_seeds 14_two_seeds.log \
  "$PY" scripts/stability_two_seeds.py \
    --seed1 reports/pool2000_stability.json \
    --seed2 reports/pool2000_stability_seed2.json \
    --out reports/pool2000_stability_two_seeds.json

# ── 13. 多种子 + 特征重要性 ─────────────────────────────────────────────
step 15_multiseed 15_multiseed.log \
  "$PY" scripts/multiseed_transfer.py \
    --features results/pool2000/features_combined.parquet \
    --out reports/pool2000_multiseed.json --bootstrap 300

step 16_importance 16_importance.log \
  "$PY" scripts/feature_importance.py \
    --features results/pool2000/features_combined.parquet \
    --out reports/pool2000_importance.json

# ── 14. 晨检 ─────────────────────────────────────────────────────────────
step 17_digest 17_digest.log "$PY" scripts/morning_digest.py

if [ -n "$FAILED" ]; then
  log "queue done WITH FAILURES:$FAILED"
  beat "done with failures:$FAILED"
else
  log "queue done, all steps ok"
  beat "done, all ok"
fi
