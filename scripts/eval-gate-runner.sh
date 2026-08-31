#!/bin/bash
# aiw-eval-gate-runner.sh — Agent-aware eval-gate cron
set -euo pipefail
AGENTS_DIR="/opt/data/agents"
TODAY=$(date -u +%Y-%m-%d)
PASS=0
FAIL=0
TOTAL=0
RESULTS=""

for agent_dir in "$AGENTS_DIR"/*/; do
    [[ ! -f "$agent_dir/PROMPT.md" ]] && continue
    agent=$(basename "$agent_dir")
    for subdir in "outbox" "lessons"; do
        brief="$agent_dir$subdir/${TODAY}.md"
        if [[ -f "$brief" ]]; then
            TOTAL=$((TOTAL + 1))
            if python3 /opt/data/eval/eval-agent-aware.py "$brief" 2>&1 | grep -q "Verdict: PASS"; then
                PASS=$((PASS + 1))
                RESULTS="$RESULTS\n  PASS: $agent/$subdir"
            else
                FAIL=$((FAIL + 1))
                RESULTS="$RESULTS\n  FAIL: $agent/$subdir"
            fi
        fi
    done
done

if [[ $TOTAL -gt 0 ]]; then
    echo "Eval-gate $(date -u +%H:%M)Z: $TOTAL briefs, $PASS PASS, $FAIL FAIL"
    echo -e "$RESULTS"
fi

# Log to eval-gate.db
python3 << PYEOF
import sqlite3
import os
from datetime import datetime, timezone
db_path = "/opt/data/db/eval-gate.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)
con = sqlite3.connect(db_path)
c = con.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    total INTEGER, pass_count INTEGER, fail_count INTEGER
)""")
c.execute("INSERT INTO runs (ts, total, pass_count, fail_count) VALUES (?, ?, ?, ?)",
          (datetime.now(timezone.utc).isoformat(), $TOTAL, $PASS, $FAIL))
con.commit()
con.close()
PYEOF
