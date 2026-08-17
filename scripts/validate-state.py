#!/usr/bin/env python3
"""validate-state.py — Validate state JSON files against schema.

Uses a lockfile to prevent concurrent runs from racing.

Cron: */15 * * * * PYT (registered as aiw-state-validate-15m)
"""
import json
import os
import sys
import time
from pathlib import Path

STATE_DIR = Path("/opt/data/agents/state")
LOCK_FILE = Path("/tmp/validate-state.lock")
LOCK_TIMEOUT_SEC = 60

# Required fields per dept state file (basic schema)
SCHEMAS = {
    "analyst.json": ["last_run", "decisions", "open_questions"],
    "coord.json": ["last_run"],
    "kiki.json": ["last_run", "lessons_delivered", "current_focus", "next_topic"],
    "finance.json": ["last_run"],
    "sales.json": ["last_run"],
    "engineering.json": ["last_run"],
    "research.json": ["last_run"],
    "people.json": ["last_run"],
    "kiki-prep.json": [],
}

errors = []
warnings = []
checked = 0

def acquire_lock() -> bool:
    """Acquire lock with timeout. Returns True if acquired."""
    if LOCK_FILE.exists():
        try:
            age = time.time() - LOCK_FILE.stat().st_mtime
            if age > LOCK_TIMEOUT_SEC:
                # Stale lock, remove
                LOCK_FILE.unlink()
        except OSError:
            pass

    if LOCK_FILE.exists():
        return False

    LOCK_FILE.write_text(str(os.getpid()))
    return True

def release_lock():
    try:
        LOCK_FILE.unlink()
    except OSError:
        pass

def validate_file(path: Path) -> bool:
    """Validate one state file. Returns True if valid."""
    global checked
    checked += 1

    if not path.exists():
        warnings.append(f"{path.name}: missing")
        return True  # Missing is not an error, just a warning

    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"{path.name}: invalid JSON: {e}")
        return False

    # Check required fields
    required = SCHEMAS.get(path.name, [])
    for field in required:
        if field not in data:
            errors.append(f"{path.name}: missing field '{field}'")

    # Cap checks (warn if exceeded)
    if "decisions" in data and isinstance(data["decisions"], list) and len(data["decisions"]) > 8:
        warnings.append(f"{path.name}: decisions > 8 (currently {len(data['decisions'])})")
    if "open_questions" in data and isinstance(data["open_questions"], list) and len(data["open_questions"]) > 5:
        warnings.append(f"{path.name}: open_questions > 5")

    return len([e for e in errors if path.name in e]) == 0

def main():
    if not acquire_lock():
        print(f"Another validate is running (lock: {LOCK_FILE}). Skipping.")
        return 0

    try:
        for state_file in sorted(STATE_DIR.glob("*.json")):
            validate_file(state_file)

        # Report
        print(f"Checked {checked} files")
        if errors:
            print(f"\nERRORS ({len(errors)}):")
            for e in errors:
                print(f"  - {e}")
        if warnings:
            print(f"\nWARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"  - {w}")
        if not errors:
            print("OK: All state files valid")
            return 0
        return 1
    finally:
        release_lock()

if __name__ == "__main__":
    sys.exit(main())
