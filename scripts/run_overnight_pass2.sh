#!/usr/bin/env bash
# ==============================================================================
# 夜间队列第二轮（03:55 起）—— 重排剩余步骤以适配时间预算
# ==============================================================================
# 第一轮在 12_stability 处发现真实代价：池 2000 后每次簇级重采样要重拟合 3760 行，
# 2.8 s/次，16 个组合 × 300 次 = 3.8 h，会跑到 07:20 并挤压 R2 的 judge 窗口。
#
# 因此第二轮把稳定性降到 150 次/组合（= 2×150 = 300 次边际，与 pilot200 的 300×2
# 持平），并改为**两个种子并行**（16 核，每个 numpy/BLAS 线程受限），实测 2 路并行
# 各自不显著变慢。这样 16 组合 × 150 次 ≈ 1.9 h，两个种子同时跑完 ≈ 1.9 h。
#
# 其余步骤全部保留，顺序改为：稳定性（并行）→ 多种子/重要性（快）→ 晨检。
# 已完成的步骤由 .done 标记自动跳过。
# ==============================================================================
set -u
REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/night_logs
PY="$REPO/.venv/bin/python"
DONE="$LOG/.done"
REPEATS="${REPEATS:-150}"
FAILED=""

mkdir -p "$LOG" "$DONE" || exit 1
cd "$REPO" || exit 1
export HF_HOME=/root/autodl-tmp/hf-cache HF_HUB_OFFLINE=1 MPLBACKEND=Agg
# Two parallel fits: keep each BLAS pool small so they do not fight for 16 cores.
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-6}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-6}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-6}"

log()  { echo "$(date -Is) $*" >> "$LOG/driver2.log"; }
beat() { echo "$(date -Is) | $*" > "$LOG/heartbeat.txt"; }
is_done() { [ -f "$DONE/$1" ]; }
mark_done() { touch "$DONE/$1"; }

log "second pass start pid=$$"

# 12_stability: two seeds in parallel, 150 repeats each.
if is_done 12_stability; then
  log "SKIP 12_stability"
else
  beat "running 12_stability (2 seeds parallel, ${REPEATS} repeats)"
  log "START 12_stability x2 parallel repeats=$REPEATS"
  "$PY" scripts/stability_study.py --features results/pool2000/features_combined.parquet \
    --out reports/pool2000_stability.json --repeats "$REPEATS" --seed 20261021 \
    --checkpoint reports/pool2000_stability.json.checkpoint.json \
    > "$LOG/12_stability.log" 2>&1 &
  pid1=$!
  "$PY" scripts/stability_study.py --features results/pool2000/features_combined.parquet \
    --out reports/pool2000_stability_seed2.json --repeats "$REPEATS" --seed 20261022 \
    --checkpoint reports/pool2000_stability_seed2.json.checkpoint.json \
    > "$LOG/13_stability_seed2.log" 2>&1 &
  pid2=$!
  wait $pid1; rc1=$?
  wait $pid2; rc2=$?
  log "stability rc seed1=$rc1 seed2=$rc2"
  if [ $rc1 -eq 0 ] && [ $rc2 -eq 0 ]; then
    mark_done 12_stability; mark_done 13_stability_seed2
    beat "done 12_stability"
  else
    FAILED="$FAILED 12_stability(seed1=$rc1,seed2=$rc2)"
    beat "failed 12_stability"
  fi
fi

# 14_two_seeds
if is_done 14_two_seeds; then log "SKIP 14_two_seeds"; else
  beat "running 14_two_seeds"
  if "$PY" scripts/stability_two_seeds.py \
       --seed1 reports/pool2000_stability.json \
       --seed2 reports/pool2000_stability_seed2.json \
       --out reports/pool2000_stability_two_seeds.json >> "$LOG/14_two_seeds.log" 2>&1; then
    mark_done 14_two_seeds; log "OK 14_two_seeds"
  else
    FAILED="$FAILED 14_two_seeds"; log "FAIL 14_two_seeds"
  fi
fi

# 15_multiseed
if is_done 15_multiseed; then log "SKIP 15_multiseed"; else
  beat "running 15_multiseed"
  if "$PY" scripts/multiseed_transfer.py --features results/pool2000/features_combined.parquet \
       --out reports/pool2000_multiseed.json --bootstrap 300 >> "$LOG/15_multiseed.log" 2>&1; then
    mark_done 15_multiseed; log "OK 15_multiseed"
  else
    FAILED="$FAILED 15_multiseed"; log "FAIL 15_multiseed"
  fi
fi

# 16_importance
if is_done 16_importance; then log "SKIP 16_importance"; else
  beat "running 16_importance"
  if "$PY" scripts/feature_importance.py --features results/pool2000/features_combined.parquet \
       --out reports/pool2000_importance.json >> "$LOG/16_importance.log" 2>&1; then
    mark_done 16_importance; log "OK 16_importance"
  else
    FAILED="$FAILED 16_importance"; log "FAIL 16_importance"
  fi
fi

# 17_digest
if is_done 17_digest; then log "SKIP 17_digest"; else
  beat "running 17_digest"
  if "$PY" scripts/morning_digest.py --out reports/morning_digest_20261023.md \
       >> "$LOG/17_digest.log" 2>&1; then
    mark_done 17_digest; log "OK 17_digest"
  else
    FAILED="$FAILED 17_digest"; log "FAIL 17_digest"
  fi
fi

if [ -n "$FAILED" ]; then
  log "second pass done WITH FAILURES:$FAILED"; beat "done with failures:$FAILED"
else
  log "second pass done, all ok"; beat "done, all ok"
fi
