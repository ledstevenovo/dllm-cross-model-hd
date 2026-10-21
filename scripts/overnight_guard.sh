#!/usr/bin/env bash
# Operational copy (versioned) of /root/autodl-tmp/overnight_guard.sh
# Independent guard for the overnight queue (runs in its own screen session).
# Survives the agent session ending. Every INTERVAL seconds:
#   - exit when the queue reports "overnight v4 done"
#   - restart the queue when its screen session is gone but the queue is unfinished
#   - kill+restart the queue when the current step has no process for STALL_MIN minutes
#     (retry backoff is <=45s, so a missing process for minutes means a real hang)
set -u

REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/overnight_logs
DONE="$LOG/.done"
GUARDLOG="$LOG/guard.log"
INTERVAL="${GUARD_INTERVAL:-300}"      # check every 5 min
STALL_MIN="${GUARD_STALL_MIN:-8}"      # no process for this long -> hang
STABILITY_REPEATS="${STABILITY_REPEATS:-500}"
STABILITY_MAX_SECONDS="${STABILITY_MAX_SECONDS:-10800}"
STOP_AFTER_MIN="${STOP_AFTER_MIN:-420}"
CYCLES="${CYCLES:-4}"

log() { echo "$(date -Is) $*" >> "$GUARDLOG"; }

process_for_step() {
  case "$1" in
    03_stage7*)          echo "offline.py evaluate" ;;
    04_tre_offline)      echo "offline_analysis.py" ;;
    05_tre_permutation*) echo "permutation_test.py" ;;
    06_multiseed)        echo "multiseed_transfer.py" ;;
    07_importance)       echo "feature_importance.py" ;;
    08_stability*)       echo "stability_study.py" ;;
    09_dynhd)            echo "step7_summary.py" ;;
    10_consistency)      echo "label_consistency.py" ;;
    *)                   echo "" ;;
  esac
}

start_queue() {
  cd "$REPO" || return 1
  screen -dmS overnight bash -c \
    "STABILITY_REPEATS=$STABILITY_REPEATS STABILITY_MAX_SECONDS=$STABILITY_MAX_SECONDS STOP_AFTER_MIN=$STOP_AFTER_MIN CYCLES=$CYCLES bash $REPO/scripts/overnight_nogpu.sh"
  sleep 10
  screen -ls 2>&1 | grep -q overnight
}

log "guard start interval=${INTERVAL}s stall=${STALL_MIN}m"

while true; do
  sleep "$INTERVAL"

  if grep -q "overnight v4 done" "$LOG/driver.log" 2>/dev/null; then
    log "queue finished -> guard exit"
    break
  fi

  if ! screen -ls 2>&1 | grep -q overnight; then
    log "queue session missing -> restarting"
    if start_queue; then log "restart ok"; else log "restart FAILED"; fi
    continue
  fi

  # screen alive: check the current step has a live process
  current="$(grep -E '^.*(START|OK|SKIP|FAIL) [0-9]' "$LOG/driver.log" 2>/dev/null | tail -1 | awk '{print $3}')"
  [ -z "$current" ] && continue
  [ -f "$DONE/$current" ] && continue
  pattern="$(process_for_step "$current")"
  if [ -z "$pattern" ]; then
    # bash-only step; give it one missed cycle before acting
    continue
  fi
  if ! pgrep -f "$pattern" >/dev/null 2>&1; then
    last="$(stat -c %Y "$LOG/driver.log" 2>/dev/null || echo 0)"
    age=$(( ( $(date +%s) - last ) / 60 ))
    if [ "$age" -ge "$STALL_MIN" ]; then
      log "step $current has no '$pattern' process and driver silent ${age}m -> kill+restart"
      pkill -f "overnight_nogpu.sh" 2>/dev/null
      sleep 3
      screen -S overnight -X quit 2>/dev/null
      sleep 3
      if start_queue; then log "stall restart ok"; else log "stall restart FAILED"; fi
    fi
  fi
done
