#!/usr/bin/env python3
"""Snapshot all state files + key metrics for trend tracking.

Run: python3 ~/.hermes/scripts/snapshot-state.py

Stores daily snapshots in /opt/data/agents/state/history/YYYY-MM-DD.json
"""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path('/opt/data/agents/state')
HISTORY_DIR = STATE_DIR / 'history'
HISTORY_DIR.mkdir(parents=True, exist_ok=True)
CRON_FILE = Path('/opt/data/.hermes/cron/jobs.json')
CONFIG_FILE = Path('/opt/data/.hermes/config.yaml')


def read_state_files():
    states = {}
    for f in STATE_DIR.glob('*.json'):
        if f.parent.name == 'history':  # skip history files
            continue
        try:
            data = json.loads(f.read_text())
            states[f.stem] = data
        except Exception:
            pass
    return states


def read_cron_status():
    if not CRON_FILE.exists():
        return {}
    try:
        data = json.loads(CRON_FILE.read_text())
        jobs = data.get('jobs', [])
        return {
            'total': len(jobs),
            'ok': sum(1 for j in jobs if j.get('last_status') == 'ok'),
            'error': sum(1 for j in jobs if j.get('last_status') == 'error'),
            'pending': sum(1 for j in jobs if not j.get('last_status')),
        }
    except Exception:
        return {}


def read_kanban_stats():
    db = Path('/opt/data/kanban.db')
    if not db.exists():
        return {}
    import sqlite3
    try:
        conn = sqlite3.connect(str(db), timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
        rows = cur.fetchall()
        conn.close()
        return dict(rows)
    except Exception:
        return {}


def read_mcp_count():
    if not CONFIG_FILE.exists():
        return 0
    content = CONFIG_FILE.read_text()
    # Count mcp servers in config
    return len(re.findall(r'^  \w+:\n    url:|^  \w+:\n    command:', content, re.MULTILINE))


def main():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    snapshot = {
        'date': today,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'state': read_state_files(),
        'cron': read_cron_status(),
        'kanban': read_kanban_stats(),
        'mcp_count': read_mcp_count(),
    }
    out = HISTORY_DIR / f'{today}.json'
    with open(out, 'w') as f:
        json.dump(snapshot, f, indent=2, default=str)
    
    # Also keep a CSV summary for quick scanning
    csv_path = HISTORY_DIR / 'summary.csv'
    is_new = not csv_path.exists()
    with open(csv_path, 'a') as f:
        if is_new:
            f.write('date,cron_total,cron_ok,cron_error,cron_pending,mcp_count,kanban_total\n')
        cron = snapshot['cron']
        kanban_total = sum(snapshot['kanban'].values()) if snapshot['kanban'] else 0
        f.write(f"{today},{cron.get('total', 0)},{cron.get('ok', 0)},{cron.get('error', 0)},{cron.get('pending', 0)},{snapshot['mcp_count']},{kanban_total}\n")
    
    print(f"snapshot: {out} ({os.path.getsize(out):,} bytes)")
    print(f"summary:  {csv_path}")


if __name__ == '__main__':
    main()
