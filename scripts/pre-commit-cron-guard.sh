#!/usr/bin/env bash
# pre-commit hook for /opt/data/agents/ — guards two things:
#   1. State files in /opt/data/agents/state/ validate against JSON Schema
#      (catches agent writes that break the dashboard).
#   2. cron/jobs.json and .hermes/cron/jobs.json stay in sync (the 2026-08-13
#      outage happened because edits only landed in .hermes/cron/jobs.json
#      while the gateway reads /opt/data/cron/jobs.json).
#
# Install: cp pre-commit-cron-guard.sh /opt/data/agents/.git/hooks/pre-commit
# Bypass:  git commit --no-verify (but don't, except for emergency fixes)

set -uo pipefail

REPO="/opt/data/agents"
STATE_DIR="$REPO/state"
SCHEMA_DIR="$REPO/schemas"
VALIDATOR="$REPO/scripts/validate-state.py"
CANON_JOBS="/opt/data/.hermes/cron/jobs.json"
GATE_JOBS="/opt/data/cron/jobs.json"

fail=0

# Only run if there are staged files
if ! git diff --cached --name-only --diff-filter=ACM | grep -q .; then
  exit 0
fi

echo "[cron-guard] checking staged files..."

# 1. State files staged — validate against schema
staged_states=$(git diff --cached --name-only --diff-filter=ACM | grep -E '^state/[a-z-]+\.json$' || true)
if [[ -n "$staged_states" ]]; then
  echo "[cron-guard] validating state files: $staged_states"
  if [[ -f "$VALIDATOR" ]]; then
    files=""
    for f in $staged_states; do
      files="$files $REPO/$f"
    done
    if ! python3 "$VALIDATOR" $files; then
      echo "[cron-guard] FAIL: state file schema validation failed"
      echo "[cron-guard] fix the state files, or bypass with --no-verify (avoid)"
      fail=1
    fi
  else
    echo "[cron-guard] WARN: validator not found at $VALIDATOR"
  fi
fi

# 2. Cron-store drift — always check, regardless of staged files.
#    This is the 2026-08-13 outage prevention. If the canonical and gateway
#    cron stores differ, the gateway may be running stale config even if
#    the agent thinks it's been updated. Block the commit so drift is
#    surfaced immediately, not on the next ticker tick.
if [[ -f "$CANON_JOBS" && -f "$GATE_JOBS" ]]; then
  canon_hash=$(sha256sum "$CANON_JOBS" | awk '{print $1}')
  gate_hash=$(sha256sum "$GATE_JOBS" | awk '{print $1}')
  if [[ "$canon_hash" != "$gate_hash" ]]; then
    echo "[cron-guard] FAIL: cron-store drift detected"
    echo "[cron-guard]   /opt/data/cron/jobs.json (gateway) hash:    ${gate_hash:0:16}..."
    echo "[cron-guard]   /opt/data/.hermes/cron/jobs.json (canon) hash: ${canon_hash:0:16}..."
    echo "[cron-guard] gateway reads /opt/data/cron/jobs.json — drift means stale config is running"
    echo "[cron-guard] Run: bash /opt/data/scripts/cron-sync.sh   (or wait for cron-sync every 5m)"
    fail=1
  fi
fi

if (( fail )); then
  echo ""
  echo "[cron-guard] COMMIT BLOCKED — fix issues above or use --no-verify"
  exit 1
fi

exit 0