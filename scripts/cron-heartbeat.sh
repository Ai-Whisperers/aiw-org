#!/usr/bin/env bash
# cron-heartbeat.sh — Detect cron job errors and stale jobs.
# Posts to origin chat via state-monitor agent or fallback log.
# Rate-limited to max 1 alert per agent per 24h.
#
# Two cron entries:
#   aiw-cron-heartbeat-onhours: */30 6-22 * * * PYT
#   aiw-cron-heartbeat-offhours: */15 23-5 * * * PYT

set -euo pipefail

STATE_DIR="/opt/data/agents/state"
HEARTBEAT_STATE="$STATE_DIR/heartbeat-alerts.json"
JOBS_FILE="/opt/data/cron/jobs.json"
ALERT_LOG="$STATE_DIR/cron-heartbeat-alerts.log"

now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
today=$(date -u +%Y-%m-%d)

# Load or init rate-limit state
if [[ ! -f "$HEARTBEAT_STATE" ]]; then
    echo '{"last_alerts": {}}' > "$HEARTBEAT_STATE"
fi

alerts=()

# Check 1: jobs in error state
if [[ -f "$JOBS_FILE" ]]; then
    error_jobs=$(python3 -c "
import json, sys
with open('$JOBS_FILE') as f:
    data = json.load(f)
jobs = data.get('jobs', data) if isinstance(data, dict) else data
if isinstance(jobs, dict):
    jobs = jobs.get('jobs', list(jobs.values()))
errors = []
for j in jobs:
    if isinstance(j, dict):
        name = j.get('name', '')
        status = j.get('last_status', '')
        if status == 'error':
            errors.append(name)
print(' '.join(errors))
" 2>/dev/null)

    for job in $error_jobs; do
        # Check rate limit
        last_alert=$(python3 -c "
import json
with open('$HEARTBEAT_STATE') as f:
    state = json.load(f)
print(state.get('last_alerts', {}).get('$job', ''))
")
        if [[ "$last_alert" != "$today" ]]; then
            alerts+=("[ERROR] cron job '$job' is in error state")
            # Update rate limit
            python3 -c "
import json
with open('$HEARTBEAT_STATE') as f:
    state = json.load(f)
state.setdefault('last_alerts', {})['$job'] = '$today'
with open('$HEARTBEAT_STATE', 'w') as f:
    json.dump(state, f, indent=2)
"
        fi
    done
fi

# Check 2: jobs not run in 7+ days
if [[ -f "$JOBS_FILE" ]]; then
    stale_jobs=$(python3 -c "
import json, sys
from datetime import datetime, timedelta, timezone
with open('$JOBS_FILE') as f:
    data = json.load(f)
jobs = data.get('jobs', data) if isinstance(data, dict) else data
if isinstance(jobs, dict):
    jobs = jobs.get('jobs', list(jobs.values()))
stale = []
now = datetime.now(timezone.utc)
for j in jobs:
    if isinstance(j, dict):
        last_run = j.get('last_run_at')
        if last_run:
            try:
                last_dt = datetime.fromisoformat(last_run.replace('Z', '+00:00'))
                if (now - last_dt).days > 7:
                    name = j.get('name', 'unknown')
                    days = (now - last_dt).days
                    stale.append(f'{name}:{days}')
            except (ValueError, TypeError):
                pass
print(' '.join(stale))
" 2>/dev/null)

    for entry in $stale_jobs; do
        job=$(echo "$entry" | cut -d: -f1)
        days=$(echo "$entry" | cut -d: -f2)
        last_alert=$(python3 -c "
import json
with open('$HEARTBEAT_STATE') as f:
    state = json.load(f)
print(state.get('last_alerts', {}).get('stale_$job', ''))
")
        if [[ "$last_alert" != "$today" ]]; then
            alerts+=("[STALE] cron job '$job' has not run in $days days")
            python3 -c "
import json
with open('$HEARTBEAT_STATE') as f:
    state = json.load(f)
state.setdefault('last_alerts', {})['stale_$job'] = '$today'
with open('$HEARTBEAT_STATE', 'w') as f:
    json.dump(state, f, indent=2)
"
        fi
    done
fi

# Report
if [[ ${#alerts[@]} -gt 0 ]]; then
    echo "[$now] Heartbeat found ${#alerts[@]} issue(s):"
    for alert in "${alerts[@]}"; do
        echo "  $alert"
        echo "[$now] $alert" >> "$ALERT_LOG"
    done
    echo ""
    echo "Total alerts: ${#alerts[@]}"
    echo "Log: $ALERT_LOG"
else
    echo "[$now] Heartbeat OK: no errors, no stale jobs"
fi
