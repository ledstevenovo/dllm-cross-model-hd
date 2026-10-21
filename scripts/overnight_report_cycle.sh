#!/usr/bin/env bash
# One monitoring cycle v2 for the overnight queue: sleep, snapshot, self-heal, escalate.
#
# Escalation contract (per user instruction):
#   a step that has FAILed and is still pending after the queue's own retries/watchdog is
#   marked ACTION_REQUIRED in this output; the agent session then dispatches a subagent to
#   diagnose from the step log, fix the cause and re-run the step. Failures are never merely
#   reported.
#
# Self-heal policy:
#   - screen alive + step has a live process    -> OK
#   - screen alive + no process + driver silent -> stall; kill+restart the queue
#   - screen dead  + queue unfinished           -> restart the queue (.done makes it resume)
#   - queue finished                            -> nothing to do
set -u

REPO=/root/autodl-tmp/dllm-cross-model-hd
LOG=/root/autodl-tmp/overnight_logs
DONE="$LOG/.done"
MONLOG="$LOG/monitor.log"
INTERVAL="${INTERVAL:-1200}"
STABILITY_REPEATS="${STABILITY_REPEATS:-800}"
STABILITY_MAX_SECONDS="${STABILITY_MAX_SECONDS:-12600}"
STOP_AFTER_MIN="${STOP_AFTER_MIN:-240}"
CYCLES="${CYCLES:-4}"
STALL_MIN="${STALL_MIN:-8}"

ALL_STEPS="01_backup 02_labels 03_stage7 04_tre_offline 05_tre_permutation \
06_multiseed 07_importance 08_stability 09_dynhd 10_consistency 11_report 12_commit"
# Degraded variants are fallbacks: they are only "pending" when their primary step failed.
DEGRADED="03_stage7_degraded 05_tre_permutation_degraded 08_stability_degraded"

sleep "$INTERVAL"

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
  sleep 12
  screen -ls 2>&1 | grep -q overnight
}

{
  echo "===== cycle $(date -Is) ====="
  echo "HEARTBEAT: $(cat "$LOG/heartbeat.txt" 2>/dev/null || echo none)"
  echo "DONE: $(ls "$DONE" 2>/dev/null | tr '\n' ' ')"

  pending=""
  for s in $ALL_STEPS; do [ -f "$DONE/$s" ] || pending="$pending $s"; done
  echo "PENDING:$pending"
  for s in $DEGRADED; do
    [ -f "$DONE/$s" ] || continue
    echo "DEGRADED_USED: $s"
  done

  # steps that failed and have no success marker -> need intervention
  failed=""
  for s in $ALL_STEPS; do
    [ -f "$DONE/$s" ] && continue
    if grep -q "FAIL $s" "$LOG/driver.log" 2>/dev/null; then
      # a successful degraded fallback covers the primary step
      case "$s" in
        03_stage7)          [ -f "$DONE/03_stage7_degraded" ] && continue ;;
        05_tre_permutation) [ -f "$DONE/05_tre_permutation_degraded" ] && continue ;;
        08_stability)       [ -f "$DONE/08_stability_degraded" ] && continue ;;
      esac
      failed="$failed $s"
    fi
  done
  if [ -n "$failed" ]; then
    echo "ACTION_REQUIRED: failed steps:$failed"
    echo "  -> dispatch a subagent to diagnose, fix and re-run these steps"
    # durable repair request: survives an agent-session restart
    {
      echo "REPAIR NEEDED $(date -Is)"
      echo "failed steps:$failed"
      for s in $failed; do
        echo "--- $s (driver FAIL lines) ---"
        grep -n "FAIL $s" "$LOG/driver.log" 2>/dev/null | tail -5
        logfile="$LOG/$(echo "$s" | sed 's/_degraded//').log"
        [ -f "$logfile" ] && { echo "--- $logfile tail ---"; tail -25 "$logfile"; }
      done
      echo "--- driver tail ---"
      tail -20 "$LOG/driver.log"
    } > "$LOG/REPAIR_NEEDED.txt"
  else
    echo "ACTION_REQUIRED: none"
    rm -f "$LOG/REPAIR_NEEDED.txt"
  fi

  screen_alive=0
  screen -ls 2>&1 | grep -q "overnight" && screen_alive=1
  echo "SCREEN: $([ $screen_alive -eq 1 ] && echo alive || echo dead)"

  current="$(grep -E '^.*(START|OK|SKIP|FAIL) [0-9]' "$LOG/driver.log" 2>/dev/null | tail -1 | awk '{print $3}')"
  echo "CURRENT_STEP: ${current:-none}"
  pattern="$(process_for_step "$current")"
  if [ -n "$pattern" ] && [ $screen_alive -eq 1 ] && [ ! -f "$DONE/$current" ]; then
    if pgrep -f "$pattern" >/dev/null 2>&1; then
      echo "PROCESS: running ($pattern)"
    else
      last="$(stat -c %Y "$LOG/driver.log" 2>/dev/null || echo 0)"
      age=$(( ( $(date +%s) - last ) / 60 ))
      echo "PROCESS: MISSING ($pattern), driver silent ${age}m"
      if [ "$age" -ge "$STALL_MIN" ]; then
        echo "ACTION: stall detected -> kill+restart queue"
        pkill -f "overnight_nogpu.sh" 2>/dev/null
        sleep 3
        screen -S overnight -X quit 2>/dev/null
        sleep 3
        if start_queue; then echo "RESTART: ok"; else echo "RESTART: FAILED"; fi
      fi
    fi
  fi

  echo "LOGS:"
  for f in 03_stage7 04_tre_offline 05_tre_permutation 06_multiseed 07_importance 08_stability; do
    [ -s "$LOG/$f.log" ] && echo "  $f: $(tail -1 "$LOG/$f.log" | cut -c1-120)"
  done

  if ! grep -q "overnight v4 done" "$LOG/driver.log" 2>/dev/null && [ $screen_alive -eq 0 ]; then
    echo "ACTION: queue dead and unfinished -> restarting"
    if start_queue; then echo "RESTART: ok"; else echo "RESTART: FAILED"; fi
  fi
} | tee -a "$MONLOG"
