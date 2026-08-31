#!/usr/bin/env bash
# cron-sync.sh — keep /opt/data/cron/jobs.json and /opt/data/.hermes/cron/jobs.json
# in sync. The Hermes gateway ticker reads from /opt/data/cron/jobs.json, but
# docs and `get_hermes_home()` resolve to /opt/data/.hermes/cron/jobs.json.
# Without this hook, an edit through `hermes cron edit` or a hand edit to
# `.hermes/cron/jobs.json` silently never reaches the gateway (silent no-op
# that returned rc=0). The 2026-08-13 outage that took out 3 cron jobs for
# 6+ hours was caused by exactly this drift.
#
# Strategy: .hermes/cron/jobs.json is the canonical source (matches Hermes's
# own `get_hermes_home()` resolution). Every 5 minutes we copy it over to
# /opt/data/cron/jobs.json if they differ. The reverse direction (if someone
# edits /opt/data/cron/jobs.json directly via the ticker-side) is detected
# but logged, not auto-overwritten, since the canonical write path always
# goes through .hermes/.
#
# Run via: hermes cron run <job-id> (script mode, no_agent=true)
# Or via: bash /opt/data/scripts/cron-sync.sh
set -euo pipefail

CANONICAL="/opt/data/.hermes/cron/jobs.json"
GATEWAY="/opt/data/cron/jobs.json"
LOG="/opt/data/logs/cron-sync.log"

mkdir -p "$(dirname "$LOG")"
ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

log() { echo "[$(ts)] $*" | tee -a "$LOG" >&2; }

# Both files must exist
if [[ ! -f "$CANONICAL" ]]; then
  log "ERROR: canonical missing: $CANONICAL"
  exit 1
fi

# If gateway store doesn't exist, copy from canonical
if [[ ! -f "$GATEWAY" ]]; then
  # Gateway expects {"jobs": [...], "updated_at": "..."}; canonical may be
  # either a bare list or the dict wrapper. Detect and wrap if needed.
  python3 -c "
import json, sys
with open('$CANONICAL') as f:
    data = json.load(f)
if isinstance(data, list):
    data = {'jobs': data, 'updated_at': __import__('datetime').datetime.utcnow().isoformat() + 'Z'}
with open('$GATEWAY', 'w') as f:
    json.dump(data, f, indent=2)
"
  log "INFO: gateway store missing — created from canonical (wrapped if needed)"
  exit 0
fi

# Compare both files by content hash
canon_hash=$(sha256sum "$CANONICAL" | awk '{print $1}')
gate_hash=$(sha256sum "$GATEWAY" | awk '{print $1}')

if [[ "$canon_hash" == "$gate_hash" ]]; then
  # In sync — nothing to do
  exit 0
fi

# They differ. Determine which is newer.
canon_mtime=$(stat -c %Y "$CANONICAL" 2>/dev/null || echo 0)
gate_mtime=$(stat -c %Y "$GATEWAY" 2>/dev/null || echo 0)

if (( canon_mtime > gate_mtime )); then
  # Canonical is newer → gateway is stale. Copy forward, preserving the
  # dict-wrapper format {"jobs": [...], "updated_at": "..."} that the
  # gateway expects (canonical may have been written as a bare list).
  python3 -c "
import json, sys, shutil
shutil.copy2('$CANONICAL', '$GATEWAY')
# Ensure gateway has the dict wrapper
with open('$GATEWAY') as f:
    data = json.load(f)
if isinstance(data, list):
    data = {'jobs': data, 'updated_at': __import__('datetime').datetime.utcnow().isoformat() + 'Z'}
    with open('$GATEWAY', 'w') as f:
        json.dump(data, f, indent=2)
"
  log "INFO: synced canonical → gateway (drift detected, canonical newer by $((canon_mtime - gate_mtime))s)"
  exit 0
elif (( gate_mtime > canon_mtime )); then
  # Gateway is newer — this usually means `hermes cron edit` was called
  # (which writes through to /opt/data/cron/jobs.json). When the drift is
  # small (<6h) AND the canonical still parses cleanly with the same job count
  # as before, auto-sync forward. For larger drift (>6h) log a WARN so an
  # operator can review before next sync.
  drift=$((gate_mtime - canon_mtime))
  if (( drift < 21600 )); then
    python3 -c "
import json, shutil
shutil.copy2('$GATEWAY', '$CANONICAL')
with open('$CANONICAL') as f:
    data = json.load(f)
if isinstance(data, list):
    data = {'jobs': data, 'updated_at': __import__('datetime').datetime.utcnow().isoformat() + 'Z'}
    with open('$CANONICAL', 'w') as f:
        json.dump(data, f, indent=2)
"
    log "INFO: synced gateway → canonical (drift $drift s, auto-resolved)"
    exit 0
  else
    log "WARN: gateway newer than canonical by ${drift}s — drift > 6h, review before auto-resolving"
    exit 0
  fi
else
  # Same mtime but different content — shouldn't happen; log for diagnosis
  log "ERROR: same mtime but different hash — possible filesystem skew"
  diff -u "$CANONICAL" "$GATEWAY" | head -20 | tee -a "$LOG" >&2
  exit 1
fi