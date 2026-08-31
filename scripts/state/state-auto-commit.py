#!/usr/bin/env python3
"""state-auto-commit.py - Auto-commit state to git for audit trail.

Runs after every build-org-state.py via cron chain.
Creates git history of all state changes.
"""
import subprocess
from pathlib import Path
from datetime import datetime, timezone

STATE_DIR = Path("/opt/data/state")
VERSIONED_REPO = Path("/opt/data/state-versioned")


def main():
    if not VERSIONED_REPO.exists():
        return
    
    # Copy current state files
    for fname in ["org-state.json", "customers.json", "coaching-customers.json",
                  "cost-tracker.json", "eval-trending.json", "errors.json"]:
        src = STATE_DIR / fname
        if src.exists():
            dst = VERSIONED_REPO / fname
            dst.write_bytes(src.read_bytes())
    
    # Git commit
    import os
    os.chdir(VERSIONED_REPO)
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    msg = f"state: auto-snapshot {today}"
    
    subprocess.run(["git", "add", "."], check=False)
    r = subprocess.run(["git", "commit", "-m", msg, "--allow-empty"], 
                      capture_output=True, text=True)
    
    if "nothing to commit" in r.stdout + r.stderr:
        print("No state changes")
    else:
        print(f"Committed state snapshot: {today}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

