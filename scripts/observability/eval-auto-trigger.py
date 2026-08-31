#!/usr/bin/env python3
"""eval-auto-trigger.py - Auto-trigger eval-gate when new briefs appear.

Runs every 5 min. Scans outbox/ for new briefs (modified in last 5 min).
For each new brief, runs eval-agent-aware.py and logs result.

This is the post-brief-write hook that 12-factor-agents pattern requires.
"""
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

AGENTS_DIR = Path("/opt/data/agents")
STATE_DIR = Path("/opt/data/state")
LOG_FILE = STATE_DIR / "auto-eval-log.jsonl"


def main():
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=6)
    triggered = 0
    
    for agent_dir in AGENTS_DIR.iterdir():
        if not (agent_dir / "PROMPT.md").exists():
            continue
        agent_name = agent_dir.name
        
        for subdir in ["outbox", "lessons"]:
            d = agent_dir / subdir
            if not d.exists():
                continue
            for brief in d.glob("*.md"):
                mtime = datetime.fromtimestamp(brief.stat().st_mtime, timezone.utc)
                if mtime < cutoff:
                    continue
                
                # New brief! Trigger eval
                r = subprocess.run(
                    ["python3", "/opt/data/eval/eval-agent-aware.py", str(brief)],
                    capture_output=True, text=True, timeout=30
                )
                try:
                    result = json.loads(r.stdout.split("Verdict:")[0].split("Score:")[1] if "Score:" in r.stdout else r.stdout)
                except:
                    result = {"raw": r.stdout[:200]}
                
                # Log it
                with LOG_FILE.open("a") as f:
                    f.write(json.dumps({
                        "ts": datetime.now(timezone.utc).isoformat(),
                        "agent": agent_name,
                        "brief": str(brief),
                        "result": r.stdout[:300],
                    }) + "\n")
                
                triggered += 1
    
    print(f"Auto-triggered eval for {triggered} new briefs")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

