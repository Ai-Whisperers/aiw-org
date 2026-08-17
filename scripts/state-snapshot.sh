#!/usr/bin/env bash
# state-snapshot.sh — Atomic snapshot of all state files every 6 hours
# Cron: 0 */6 * * * PYT (registered as aiw-state-snapshot-6h)

set -euo pipefail

STATE_DIR="/opt/data/agents/state"
SNAPSHOT_BASE="/opt/data/agents/state/snapshots"
DATETIME=$(date -u +%Y-%m-%dT%H-%M-%SZ)
SNAPSHOT_DIR="$SNAPSHOT_BASE/$DATETIME"

mkdir -p "$SNAPSHOT_DIR"

copied=0
skipped=0

for state_file in "$STATE_DIR"/*.json; do
    if [[ ! -f "$state_file" ]]; then
        continue
    fi

    name=$(basename "$state_file")
    target="$SNAPSHOT_DIR/$name"

    # Atomic copy: write to temp, then mv
    tmp=$(mktemp "$SNAPSHOT_DIR/.${name}.XXXXXX.tmp")
    if cp "$state_file" "$tmp" 2>/dev/null; then
        mv "$tmp" "$target"
        copied=$((copied + 1))
    else
        rm -f "$tmp"
        skipped=$((skipped + 1))
    fi
done

# Cleanup: keep only 30 most recent snapshots
find "$SNAPSHOT_BASE" -maxdepth 1 -type d -mmin +10080 -exec rm -rf {} + 2>/dev/null || true

echo "Snapshot $DATETIME: copied=$copied skipped=$skipped"
echo "Location: $SNAPSHOT_DIR"
