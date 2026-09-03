#!/usr/bin/env bash
# thesis-watchdog-cron.sh — bash replacement for the every-15m MiniMax-M3 agent.
#
# Original (wasteful):
#   LLM agent every 15 min activates venv, runs thesis_watchdog.py --check-only,
#   reads stdout, exits. 2,084 lifetime fires, ~$3.60/day estimated.
#
# Replacement (this script):
#   Direct cron call to the existing Python watchdog. On URGENT-RESUME (non-zero
#   exit), writes a signal flag. A separate once-daily MiniMax-M3 agent reads
#   the flag and runs `make tick` — preserves resume capability without
#   15-min LLM polling.
#
# Exit codes (from thesis_watchdog.py):
#   0  — OK or recent warning, no action needed
#   1  — RESUME (heartbeat stale >6h, but <24h)
#   2  — URGENT-RESUME (heartbeat stale >24h)
#
# Signal flag: /opt/data/state/thesis-resume-signal.flag (overwritten each run)

set -uo pipefail

THESIS_DIR="/opt/data/thesis-active"
VENV_PY="${THESIS_DIR}/.venv/bin/python3"
WATCHDOG="${THESIS_DIR}/scripts/thesis_watchdog.py"
LOG=/opt/data/logs/thesis-watchdog-cron.log
SIGNAL=/opt/data/state/thesis-resume-signal.flag

mkdir -p "$(dirname "$LOG")"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

if [[ ! -x "$VENV_PY" ]]; then
    echo "[$(ts)] FATAL: venv python not found at $VENV_PY" >> "$LOG"
    exit 0  # don't page cron; this is a host-config issue, not a thesis issue
fi

if [[ ! -f "$WATCHDOG" ]]; then
    echo "[$(ts)] FATAL: watchdog script not found at $WATCHDOG" >> "$LOG"
    exit 0
fi

# Run the watchdog with --check-only (read-only, fast).
set +e
cd "$THESIS_DIR"
OUTPUT=$("$VENV_PY" "$WATCHDOG" --check-only 2>&1)
RC=$?
set -e

echo "[$(ts)] watchdog rc=$RC" >> "$LOG"
echo "$OUTPUT" >> "$LOG"

case "$RC" in
    0)
        # OK / recent — clear any stale signal flag.
        rm -f "$SIGNAL"
        exit 0
        ;;
    1)
        # RESUME — write signal flag for the daily handler.
        echo "[$(ts)] RESUME signal raised" >> "$LOG"
        echo "raised_at=$(ts) reason=stale_6h_24h rc=1" > "$SIGNAL"
        exit 0
        ;;
    2)
        # URGENT-RESUME — write signal flag with URGENT marker.
        echo "[$(ts)] URGENT-RESUME signal raised" >> "$LOG"
        echo "raised_at=$(ts) reason=stale_gt_24h rc=2 URGENT" > "$SIGNAL"
        exit 0
        ;;
    *)
        echo "[$(ts)] unexpected rc=$RC" >> "$LOG"
        exit 0
        ;;
esac
