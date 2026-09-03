#!/usr/bin/env bash
# evo-poll-watchdog.sh — bash replacement for the every-5m MiniMax-M3 agent.
#
# Original (wasteful):
#   LLM agent every 5 min reads state files, then runs `pgrep` and decides
#   whether to restart. 4,751 lifetime fires, ~$10.80/day estimated.
#
# Replacement (this script):
#   `pgrep && exit 0 || restart` — no LLM, deterministic, sub-second.
#
# Exits:
#   0 — poller running (silent)
#   1 — poller not running; restart attempted
#
# Logs to /opt/data/logs/evo-poll-watchdog.log on restart only.

set -uo pipefail

LOG=/opt/data/logs/evo-poll-watchdog.log
RESTART_CMD="/opt/data/scripts/evolution-poller.sh restart"

mkdir -p "$(dirname "$LOG")"

# Check the poller. Allow multiple grep matches (pgrep -f matches the script itself).
POLLER_PIDS=$(pgrep -f "evolution[_-]poller\.py" || true)
if [[ -n "$POLLER_PIDS" ]]; then
    exit 0  # running, silent
fi

# Not running — restart and log.
ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
{
    echo "[$(ts)] evo-poller not running (no PIDs matched evolution-poller.py); restarting"
    if "$RESTART_CMD" >> "$LOG" 2>&1; then
        echo "[$(ts)] restart OK"
        exit 1  # signal cron that action was taken
    else
        echo "[$(ts)] restart FAILED (rc=$?)"
        exit 1
    fi
} >> "$LOG" 2>&1
