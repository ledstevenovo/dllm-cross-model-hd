#!/usr/bin/env bash
# No-GPU overnight pass: backup -> main-project sign-off -> features -> first real transfer
# matrix -> DynHD delivery summary -> morning summary -> commit/push.
#
# Safe to re-run: every step is idempotent (backup skipped if MANIFEST exists, labels and
# features are regenerated, evaluate writes new output dirs, commit is skipped when clean).
# No GPU is used anywhere in this script.
#
# Usage:
#   bash scripts/overnight_nogpu.sh                 # full pass
#   DRY_RUN=1 bash scripts/overnight_nogpu.sh       # print the plan only
#
# Logs: /root/autodl-tmp/overnight_logs/driver.log (+ one log per step)
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG="${OVERNIGHT_LOG_DIR:-/root/autodl-tmp/overnight_logs}"
BACKUP="${OVERNIGHT_BACKUP_DIR:-/root/autodl-tmp/backup_$(date +%Y%m%d)}"
RUN="$REPO/.venv/bin/python"
DRUN="$REPO/.venv-dynhd/bin/python"
REVIEWER="${REVIEWER:-ledstevenovo}"
SIGNED_OFF_AT="${SIGNED_OFF_AT:-$(date +%Y-%m-%d)}"

mkdir -p "$LOG" "$BACKUP" || exit 1
cd "$REPO" || exit 1
export HF_HOME="${HF_HOME:-/root/autodl-tmp/hf-cache}"
export HF_HUB_OFFLINE=1
export PYTHONPATH="$REPO/references/repos/DynHD"

log() { echo "$1 $(date -Is)" >> "$LOG/driver.log"; }

if [ "${DRY_RUN:-0}" = "1" ]; then
  cat <<PLAN
No-GPU overnight plan (dry run)
  repo        : $REPO
  logs        : $LOG
  backup      : $BACKUP
  1 backup    : TRE + main project + DynHD archives with MANIFEST.sha256
  2 labels    : smoke/pilot200 reviewed labels ($REVIEWER, rule-signoff, $SIGNED_OFF_AT) + parquet extract
  3 stage 7   : offline.py evaluate (entropy_raw, relative_normalized x lr/mlp, bootstrap 1000)
                + ablation sweep (bootstrap 200), axis=model
  4 DynHD     : scripts/dynhd_repro/step7_summary.py -> reports/dynhd_reproduction_summary.{md,json}
  5 wrap-up   : reports/overnight_YYYYMMDD_summary.md + commit/push
PLAN
  exit 0
fi

log "overnight start pid=$$"

# ---- Step 1: backup packages -------------------------------------------------
if [ ! -f "$BACKUP/MANIFEST.sha256" ]; then
  {
    tar -czf "$BACKUP/tre_repro.tar.gz" data/trajectories/tre_repro data/tre_repro/labels results/tre_repro reports/tre_repro
    tar -czf "$BACKUP/main_project.tar.gz" data/trajectories/bf16_pilot200 data/trajectories/bf16_smoke20 data/labels data/features
    tar -czf "$BACKUP/dynhd_repro.tar.gz" -C /root/autodl-tmp dynhd_repro
    ( cd "$BACKUP" && sha256sum ./*.tar.gz > MANIFEST.sha256 )
  } > "$LOG/01_backup.log" 2>&1
  log "backup_rc=$? size=$(du -sh "$BACKUP" | cut -f1)"
else
  log "backup_skip=exists"
fi

# ---- Step 2: main-project reviewed labels + features -------------------------
{
  for model in llada dream; do
    "$RUN" scripts/finalize_reviewed_labels.py \
      --input "data/labels/smoke_${model}.assistant_review.jsonl" \
      --out "data/labels/smoke_${model}.reviewed.jsonl" \
      --reviewer "$REVIEWER" --signed-off-at "$SIGNED_OFF_AT"
  done
  for model in llada dream; do
    "$RUN" scripts/finalize_reviewed_labels.py \
      --input "data/labels/pilot200_${model}.draft_review.jsonl" \
      --out "data/labels/pilot200_${model}.reviewed.jsonl" \
      --reviewer "$REVIEWER" --signed-off-at "$SIGNED_OFF_AT"
  done
  for model in llada dream; do
    "$RUN" scripts/offline.py extract \
      --questions data/raw_qa/subsets/pilot200.jsonl \
      --traces "data/trajectories/bf16_pilot200/$model/traces" \
      --labels "data/labels/pilot200_${model}.reviewed.jsonl" \
      --output "data/features/pilot200_${model}.parquet"
  done
  "$RUN" - <<'PY'
import pathlib
import pandas as pd
a = pd.read_parquet('data/features/pilot200_llada.parquet')
b = pd.read_parquet('data/features/pilot200_dream.parquet')
for name, frame in (('llada', a), ('dream', b)):
    print(name, len(frame), frame['label'].value_counts().to_dict(),
          'eligible=', int((frame['human_reviewed'] & frame['label'].isin(['correct', 'incorrect'])).sum()))
pathlib.Path('results/stage7').mkdir(parents=True, exist_ok=True)
combined = pd.concat([a, b], ignore_index=True)
combined.to_parquet('results/stage7/features_combined.parquet')
print('combined rows', len(combined), 'models', combined['model_id'].nunique(),
      'datasets', combined['dataset'].nunique())
PY
} > "$LOG/02_main_labels.log" 2>&1
log "main_labels_rc=$?"

# ---- Step 3: first real transfer matrix + ablations (CPU) --------------------
{
  "$RUN" scripts/offline.py evaluate --features results/stage7/features_combined.parquet \
    --output results/stage7/main --feature-sets entropy_raw relative_normalized \
    --kinds lr mlp --bootstrap 1000 --axis model
  echo "main_rc=$?"
  "$RUN" scripts/offline.py evaluate --features results/stage7/features_combined.parquet \
    --output results/stage7/ablations --kinds lr --bootstrap 200 --axis model
  echo "ablations_rc=$?"
} > "$LOG/03_stage7.log" 2>&1
log "stage7_rc=$?"

# ---- Step 4: DynHD step-7 delivery summary -----------------------------------
"$DRUN" scripts/dynhd_repro/step7_summary.py > "$LOG/04_dynhd_step7.log" 2>&1
log "dynhd_step7_rc=$?"

# ---- Step 5: morning summary + commit/push -----------------------------------
STAMP="$(date +%Y%m%d)"
{
  {
    echo "# 无卡通宵结果（$STAMP）"
    echo
    echo "- 备份包：\`$BACKUP\`（$(du -sh "$BACKUP" | cut -f1)）"
    echo
    echo "## 标签与特征"
    tail -6 "$LOG/02_main_labels.log"
    echo
    echo "## 阶段 7（结果目录 results/stage7/，不入库）"
    tail -8 "$LOG/03_stage7.log"
    echo
    echo "## DynHD 步骤 7"
    echo "- reports/dynhd_reproduction_summary.md / .json"
    echo
    echo "## 早上验收顺序"
    echo "1. \`cat $LOG/driver.log\` 看每步 rc"
    echo "2. 看 \`results/stage7/main\` 的指标与 \`reports/dynhd_reproduction_summary.md\`"
    echo "3. \`screen -ls\` 确认为空后再切无卡"
  } > "reports/overnight_${STAMP}_summary.md"
  git add reports/ docs/ scripts/ data/labels/*.reviewed.jsonl 2>/dev/null
  if git diff --cached --quiet; then
    echo "nothing to commit"
  else
    git commit -q -m "Overnight no-GPU pass: reviewed labels, first real transfer matrix, DynHD delivery summary"
    git push git@github.com:ledstevenovo/dllm-cross-model-hd.git main:main
  fi
} > "$LOG/05_commit.log" 2>&1
log "commit_rc=$?"
log "overnight done"
