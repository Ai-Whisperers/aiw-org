#!/bin/bash
# backup-drill.sh - Test backup + restore end-to-end

BACKUP_DIR="/opt/data/backups/db/$(date -u +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"

echo "=== STEP 1: Backup ==="
python3 /opt/data/agents-v2/scripts/db-snapshot.py 2>&1 | tail -3

echo ""
echo "=== STEP 2: Verify backup integrity ==="
LATEST=$(ls -t /opt/data/backups/db/ | head -1)
for db in /opt/data/backups/db/$LATEST/*.gz; do
    if gunzip -t "$db" 2>/dev/null; then
        echo "  ✓ $(basename $db)"
    else
        echo "  ✗ $(basename $db) CORRUPT"
    fi
done

echo ""
echo "=== STEP 3: Test restore ==="
mkdir -p /tmp/restore-test
for db in /opt/data/backups/db/$LATEST/*.gz; do
    name=$(basename $db .gz)
    gunzip -c "$db" > /tmp/restore-test/$name
    # Verify integrity
    result=$(python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('/tmp/restore-test/$name')
    c = conn.cursor()
    c.execute('PRAGMA integrity_check')
    print(c.fetchone()[0])
    conn.close()
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null)
    echo "  $name: $result"
done

echo ""
echo "=== Cleanup ==="
rm -rf /tmp/restore-test

echo ""
echo "=== Drill complete ==="
