#!/usr/bin/env bash
# build-signal-index.sh — Build the Mnemosyne memory L3 signal index.
#
# Cron wrapper for aiw-signal-indexer. The previous inline `python3 -c` in
# jobs.json had nested-escape-quoting that broke execution. This wrapper
# invokes the signal_index.py module with proper args.
#
# Schedule: daily 02:00 UTC (low-traffic window).
# Outputs: /opt/data/state/signal_index.json
#
# Exit codes:
#   0 = success (index built or no-op if no source signals)
#   1 = source path missing
#   2 = script invocation failed

set -euo pipefail

REPO="/opt/data/agents"
STATE="/opt/data/state"
SOURCE="$STATE/signal-queue.ndjson"
OUTPUT="$STATE/signal_index.json"

# If no signals to index, exit cleanly (no-op)
if [[ ! -f "$SOURCE" ]]; then
    echo "[signal-index] no source file at $SOURCE — skipping (no-op)"
    exit 0
fi

# Build index. Pass the source as arg; signal_index.py writes to its
# default path unless --output is specified.
python3 -m scripts.memory.signal_index build --source "$SOURCE" --index "$OUTPUT"

EXIT=$?
if (( EXIT == 0 )); then
    # Sanity: confirm output exists and is non-empty
    if [[ -s "$OUTPUT" ]]; then
        SIZE=$(stat -c%s "$OUTPUT")
        echo "[signal-index] OK: $OUTPUT ($SIZE bytes)"
        exit 0
    else
        echo "[signal-index] WARN: build returned 0 but output empty"
        exit 2
    fi
else
    echo "[signal-index] FAIL: build exited $EXIT"
    exit 2
fi