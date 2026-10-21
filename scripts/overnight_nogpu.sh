#!/usr/bin/env bash
# ==============================================================================
# 无卡通宵队列 v4 —— 带重试 / 降级 / 断点续跑 / 看门狗
# ==============================================================================
# 设计目标：任何一步失败都不会让整晚白跑。
#   1. 每步最多重试 N 次（默认 3），退避 5/15/45 秒；
#   2. 每步失败后自动降级重试（全参数 -> 小参数）；
#   3. 成功即写 .done 标记，重跑时直接跳过（断点续跑）；
#   4. 外层看门狗：整轮跑完若仍有未完成步骤，等 60 秒再来一轮（最多 CYCLES 轮）；
#   5. 每步写心跳 + 单独日志，任何时刻可查进度；
#   6. 最后无论成败都生成晨检报告并尝试提交（提交本身也重试）。
#
# 全部 CPU，不占 GPU。可反复执行，幂等。
#
# 用法：
#   DRY_RUN=1 bash scripts/overnight_nogpu.sh          # 只看计划
#   bash scripts/overnight_nogpu.sh                    # 前台跑（建议 screen）
#   screen -dmS overnight bash scripts/overnight_nogpu.sh
#   tail -f /root/autodl-tmp/overnight_logs/heartbeat.txt
#
# 可调参数（环境变量）：
#   STABILITY_REPEATS=2000   稳定性重采样次数（每 2000 次约 1.6 小时）
#   PERMUTATIONS=10000       置换检验次数
#   STOP_AFTER_MIN=600       整轮硬上限（分钟，0=不限）
#   CYCLES=4                 看门狗最多跑几轮
#   FORCE=1                  忽略 .done 标记，全部重跑
#   REVIEWER / SIGNED_OFF_AT 标签签核人 / 日期
# ==============================================================================
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG="${OVERNIGHT_LOG_DIR:-/root/autodl-tmp/overnight_logs}"
BACKUP="${OVERNIGHT_BACKUP_DIR:-/root/autodl-tmp/backup_$(date +%Y%m%d)}"
DONE="$LOG/.done"
RUN="$REPO/.venv/bin/python"
DRUN="$REPO/.venv-dynhd/bin/python"
REVIEWER="${REVIEWER:-ledstevenovo}"
SIGNED_OFF_AT="${SIGNED_OFF_AT:-$(date +%Y-%m-%d)}"
STABILITY_REPEATS="${STABILITY_REPEATS:-2000}"
PERMUTATIONS="${PERMUTATIONS:-10000}"
STOP_AFTER_MIN="${STOP_AFTER_MIN:-600}"
CYCLES="${CYCLES:-4}"
FORCE="${FORCE:-0}"
ATTEMPTS="${ATTEMPTS:-3}"
DRY_RUN="${DRY_RUN:-0}"
START_EPOCH="$(date +%s)"
FAILED_STEPS=""

mkdir -p "$LOG" "$DONE" "$BACKUP" || exit 1
cd "$REPO" || exit 1
export HF_HOME="${HF_HOME:-/root/autodl-tmp/hf-cache}"
export HF_HUB_OFFLINE=1
export PYTHONPATH="$REPO/references/repos/DynHD"
export MPLBACKEND=Agg

# ---------------------------------------------------------------- 基础工具
log()      { echo "$(date -Is) $*" >> "$LOG/driver.log"; }
beat()     { echo "$(date -Is) | $*" > "$LOG/heartbeat.txt"; }
elapsed_min() { echo $(( ($(date +%s) - START_EPOCH) / 60 )); }
remaining_min() { echo $(( STOP_AFTER_MIN - $(elapsed_min) )); }

budget_ok() {  # $1 = 需要多少分钟
  [ "$STOP_AFTER_MIN" -le 0 ] && return 0
  [ "$(remaining_min)" -ge "$1" ]
}

mark_done() { touch "$DONE/$1"; }
is_done()   { [ "$FORCE" != "1" ] && [ -f "$DONE/$1" ]; }

# 执行一条命令，带重试与退避；成功返回 0
try() {  # try <attempts> <logfile> <cmd...>
  local attempts="$1" logfile="$2"; shift 2
  local i rc
  for i in $(seq 1 "$attempts"); do
    log "  attempt $i/$attempts: $*"
    "$@" >> "$logfile" 2>&1
    rc=$?
    log "  attempt $i rc=$rc"
    [ $rc -eq 0 ] && return 0
    [ "$i" -lt "$attempts" ] && sleep $((5 * i * i))   # 5s, 20s, 45s
  done
  return $rc
}

# 单步执行：标记 / 预算 / 重试 / 降级
step() {  # step <name> <min_budget_min> <attempts> <logfile> <cmd...>
  local name="$1" need="$2" attempts="$3" logfile="$4"; shift 4
  if is_done "$name"; then
    log "SKIP $name (already done)"; beat "skip $name"; return 0
  fi
  if ! budget_ok "$need"; then
    log "SKIP $name (budget: need ${need}m, left $(remaining_min)m)"; beat "budget-skip $name"; return 0
  fi
  beat "running $name"
  log "START $name (need ${need}m, left $(remaining_min)m)"
  if try "$attempts" "$logfile" "$@"; then
    mark_done "$name"; log "OK $name ($(elapsed_min)m elapsed)"; beat "done $name"
    return 0
  fi
  log "FAIL $name after $attempts attempts"
  FAILED_STEPS="$FAILED_STEPS $name"
  beat "failed $name"
  return 1
}

if [ "$DRY_RUN" = "1" ]; then
  cat <<PLAN
无卡通宵队列 v4（dry run）
  repo        : $REPO
  logs        : $LOG   （心跳 heartbeat.txt，每步日志 NN_*.log）
  已完成标记  : $DONE
  backup      : $BACKUP
  stability   : $STABILITY_REPEATS 次 ≈ $(python3 -c "print(round($STABILITY_REPEATS*58/20/60,1))") 分钟
  permutations: $PERMUTATIONS 次 ≈ $(python3 -c "print(round($PERMUTATIONS*15.5/2000/60,1))") 分钟
  硬上限      : ${STOP_AFTER_MIN} 分钟；看门狗 ${CYCLES} 轮；每步重试 ${ATTEMPTS} 次

  01 备份打包              ~10s
  02 标签签核 + 特征       ~5s
  03 阶段 7 迁移矩阵       ~3min   （失败降级：单特征集 + bootstrap 200）
  04 TRE 离线分析          ~1min   （29 个分数族、空间/时间消融）
  05 TRE 置换检验          ~2min   （失败降级：2000 次）
  06 多种子矩阵            ~1min   （5 seeds）
  07 特征重要性            ~1min   （LOO + 置换）
  08 稳定性重采样          ~1.6h   （失败降级：次数 /10）
  09 DynHD 交付汇总        ~2s
  10 标签一致性（需 key）  ~2min   （无 key 自动跳过）
  11 晨检报告 + 提交       ~10s    （提交重试 3 次）
PLAN
  exit 0
fi

log "================ overnight v4 start pid=$$ ================"
log "repeats=$STABILITY_REPEATS perms=$PERMUTATIONS cap=${STOP_AFTER_MIN}m cycles=$CYCLES attempts=$ATTEMPTS"
beat "start"

# ---------------------------------------------------------------- 队列主体
run_queue() {

# ---- 01 备份 ---------------------------------------------------------------
step 01_backup 1 2 "$LOG/01_backup.log" bash -c "
  set -e
  tar -czf '$BACKUP/tre_repro.tar.gz' data/trajectories/tre_repro data/tre_repro/labels results/tre_repro reports/tre_repro
  tar -czf '$BACKUP/main_project.tar.gz' data/trajectories/bf16_pilot200 data/trajectories/bf16_smoke20 data/labels data/features
  tar -czf '$BACKUP/dynhd_repro.tar.gz' -C /root/autodl-tmp dynhd_repro
  cd '$BACKUP' && sha256sum ./*.tar.gz > MANIFEST.sha256
"

# ---- 02 标签 + 特征 --------------------------------------------------------
step 02_labels 2 3 "$LOG/02_main_labels.log" bash -c "
  set -e
  for model in llada dream; do
    '$RUN' scripts/finalize_reviewed_labels.py \
      --input data/labels/smoke_\${model}.assistant_review.jsonl \
      --out data/labels/smoke_\${model}.reviewed.jsonl \
      --reviewer '$REVIEWER' --signed-off-at '$SIGNED_OFF_AT'
    '$RUN' scripts/finalize_reviewed_labels.py \
      --input data/labels/pilot200_\${model}.draft_review.jsonl \
      --out data/labels/pilot200_\${model}.reviewed.jsonl \
      --reviewer '$REVIEWER' --signed-off-at '$SIGNED_OFF_AT'
  done
  for model in llada dream; do
    '$RUN' scripts/offline.py extract \
      --questions data/raw_qa/subsets/pilot200.jsonl \
      --traces data/trajectories/bf16_pilot200/\${model}/traces \
      --labels data/labels/pilot200_\${model}.reviewed.jsonl \
      --output data/features/pilot200_\${model}.parquet
  done
  mkdir -p results/stage7
  '$RUN' - <<'PY'
import pandas as pd
a = pd.read_parquet('data/features/pilot200_llada.parquet')
b = pd.read_parquet('data/features/pilot200_dream.parquet')
for name, frame in (('llada', a), ('dream', b)):
    print(name, len(frame), frame['label'].value_counts().to_dict(),
          'eligible=', int((frame['human_reviewed'] & frame['label'].isin(['correct','incorrect'])).sum()))
combined = pd.concat([a, b], ignore_index=True)
combined.to_parquet('results/stage7/features_combined.parquet')
print('combined rows', len(combined), 'models', combined['model_id'].nunique())
PY
"

# ---- 03 阶段 7 迁移矩阵（带降级） -------------------------------------------
if ! step 03_stage7 5 3 "$LOG/03_stage7.log" bash -c "
  set -e
  '$RUN' scripts/offline.py evaluate --features results/stage7/features_combined.parquet \
    --output results/stage7/main --feature-sets entropy_raw relative_normalized \
    --kinds lr mlp --bootstrap 1000 --axis model
  '$RUN' scripts/offline.py evaluate --features results/stage7/features_combined.parquet \
    --output results/stage7/ablations --kinds lr --bootstrap 200 --axis model
"; then
  log "03_stage7 degraded retry"
  step 03_stage7_degraded 3 2 "$LOG/03_stage7_degraded.log" bash -c "
    set -e
    '$RUN' scripts/offline.py evaluate --features results/stage7/features_combined.parquet \
      --output results/stage7/main --feature-sets entropy_raw --kinds lr --bootstrap 200 --axis model
  "
fi

# ---- 04 TRE 离线分析 --------------------------------------------------------
step 04_tre_offline 3 3 "$LOG/04_tre_offline.log" \
  "$RUN" scripts/tre_repro/offline_analysis.py --bootstrap 1000

# ---- 05 TRE 置换检验（带降级） ---------------------------------------------
if ! step 05_tre_permutation 4 3 "$LOG/05_tre_permutation.log" \
      "$RUN" scripts/tre_repro/permutation_test.py --permutations "$PERMUTATIONS"; then
  log "05 degraded to 2000 permutations"
  step 05_tre_permutation_degraded 3 2 "$LOG/05_tre_permutation_degraded.log" \
    "$RUN" scripts/tre_repro/permutation_test.py --permutations 2000
fi

# ---- 06 多种子矩阵 ----------------------------------------------------------
step 06_multiseed 3 3 "$LOG/06_multiseed.log" \
  "$RUN" scripts/multiseed_transfer.py --bootstrap 500

# ---- 07 特征重要性 ----------------------------------------------------------
step 07_importance 3 3 "$LOG/07_importance.log" \
  "$RUN" scripts/feature_importance.py

# ---- 08 稳定性重采样（最长，带降级） ---------------------------------------
if ! step 08_stability 30 2 "$LOG/08_stability.log" \
      "$RUN" scripts/stability_study.py --repeats "$STABILITY_REPEATS"; then
  reduced=$(( STABILITY_REPEATS / 10 )); [ "$reduced" -lt 50 ] && reduced=50
  log "08 degraded to $reduced repeats"
  step 08_stability_degraded 20 2 "$LOG/08_stability_degraded.log" \
    "$RUN" scripts/stability_study.py --repeats "$reduced"
fi

# ---- 09 DynHD 交付 ----------------------------------------------------------
step 09_dynhd 1 3 "$LOG/09_dynhd_step7.log" \
  "$DRUN" scripts/dynhd_repro/step7_summary.py

# ---- 10 标签一致性（可选） --------------------------------------------------
if [ -n "${MOMA_API_KEY:-}" ]; then
  step 10_consistency 5 3 "$LOG/10_label_consistency.log" \
    "$DRUN" scripts/dynhd_repro/label_consistency.py
else
  echo "MOMA_API_KEY unset: skipped" > "$LOG/10_label_consistency.log"
  log "SKIP 10_consistency (no key)"
  mark_done 10_consistency
fi

# ---- 11 晨检报告 ------------------------------------------------------------
step 11_report 2 3 "$LOG/11_report.log" bash -c "
  set -e
  STAMP=\$(date +%Y%m%d)
  {
    echo '# 无卡通宵结果（'\$STAMP'，用时 $(elapsed_min) 分钟）'
    echo
    echo '- 备份：\`$BACKUP\`（'\$(du -sh '$BACKUP' | cut -f1)'）'
    echo '- 未完成步骤：${FAILED_STEPS:- 无}'
    echo
    echo '## 标签与特征'; tail -6 '$LOG/02_main_labels.log' 2>/dev/null || true
    echo; echo '## 阶段 7 迁移矩阵'; tail -8 '$LOG/03_stage7.log' 2>/dev/null || true
    echo; echo '## TRE 离线分析（主口径 tre 不变）'; head -18 '$LOG/04_tre_offline.log' 2>/dev/null || true
    echo; echo '## TRE 置换显著性'; tail -6 '$LOG/05_tre_permutation.log' 2>/dev/null || true
    echo; echo '## 多种子稳健性'; tail -8 '$LOG/06_multiseed.log' 2>/dev/null || true
    echo; echo '## 特征重要性'; tail -6 '$LOG/07_importance.log' 2>/dev/null || true
    echo; echo '## 稳定性重采样'; tail -8 '$LOG/08_stability.log' 2>/dev/null || true
    echo; echo '## DynHD 交付'; echo '- reports/dynhd_reproduction_summary.md / .json'
    echo; echo '## 早上验收'; echo '1. cat $LOG/driver.log'
    echo '2. cat reports/overnight_'\$STAMP'_summary.md'
    echo '3. screen -ls 为空后再切无卡'
  } > reports/overnight_\${STAMP}_summary.md
"

# ---- 12 提交推送（单独重试，失败不影响实验） -------------------------------
if ! step 12_commit 2 3 "$LOG/12_commit.log" bash -c "
  set -e
  git add reports/ scripts/ docs/ data/labels/*.reviewed.jsonl
  if git diff --cached --quiet; then echo 'nothing to commit'; exit 0; fi
  git commit -q -m 'Overnight no-GPU pass: transfer matrix, TRE analyses, stability study, DynHD delivery'
  git push git@github.com:ledstevenovo/dllm-cross-model-hd.git main:main
"; then
  log "12_commit failed (local commit may exist); will retry next cycle"
fi

}  # run_queue

# ---------------------------------------------------------------- 看门狗
for cycle in $(seq 1 "$CYCLES"); do
  log "-------- cycle $cycle/$CYCLES --------"
  beat "cycle $cycle"
  run_queue
  pending=0
  for s in 01_backup 02_labels 03_stage7 04_tre_offline 05_tre_permutation \
           06_multiseed 07_importance 08_stability 09_dynhd 10_consistency 11_report 12_commit; do
    is_done "$s" || pending=$((pending + 1))
  done
  log "cycle $cycle finished: pending=$pending elapsed=$(elapsed_min)m"
  if [ "$pending" -eq 0 ]; then
    log "all steps done"; break
  fi
  if ! budget_ok 5; then
    log "budget exhausted with $pending pending"; break
  fi
  log "retrying $pending pending steps in 60s"
  sleep 60
done

log "================ overnight v4 done elapsed=$(elapsed_min)m ================"
beat "finished elapsed=$(elapsed_min)m pending=$(ls "$DONE" | wc -l)/12"
