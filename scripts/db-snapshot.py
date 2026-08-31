#!/usr/bin/env python3
"""db-snapshot.py — Daily SQLite backup using Python's sqlite3 module.

Cron: 0 2 * * * PYT (registered as aiw-db-snapshot-daily)

Usage: python3 db-snapshot.py [--dry-run]
"""
import argparse
import gzip
import sqlite3
import shutil
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

DB_DIR = Path("/opt/data/db")
BACKUP_BASE = Path("/opt/data/backups/db")
RETENTION_DAYS = 90


def backup_all(dry_run: bool = False) -> dict:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    backup_dir = BACKUP_BASE / today
    backup_dir.mkdir(parents=True, exist_ok=True)

    backed = 0
    skipped = 0

    for db in sorted(DB_DIR.glob("*.db")):
        if not db.is_file():
            continue

        target = backup_dir / db.name

        if dry_run:
            backed += 1
            continue

        try:
            src = sqlite3.connect(str(db))
            dst = sqlite3.connect(str(target))
            with dst:
                src.backup(dst)
            src.close()
            dst.close()

            # Compress
            with open(target, "rb") as f_in:
                with gzip.open(f"{target}.gz", "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            target.unlink()

            backed += 1
        except Exception as e:
            print(f"  FAILED {db.name}: {e}")
            skipped += 1

    return {
        "date": today,
        "location": str(backup_dir),
        "backed": backed,
        "skipped": skipped,
    }


def cleanup_old():
    """Remove backups older than RETENTION_DAYS."""
    if not BACKUP_BASE.exists():
        return 0
    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    removed = 0
    for d in BACKUP_BASE.iterdir():
        if d.is_dir():
            try:
                d_mtime = datetime.fromtimestamp(d.stat().st_mtime, tz=timezone.utc)
                if d_mtime < cutoff:
                    shutil.rmtree(d)
                    removed += 1
            except (ValueError, OSError):
                pass
    return removed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result = backup_all(args.dry_run)
    removed = cleanup_old()

    if args.dry_run:
        print(f"DRY RUN: would back up {result['backed']} databases to {result['location']}")
    else:
        print(f"Backup {result['date']}: backed={result['backed']} skipped={result['skipped']}")
        print(f"Location: {result['location']}")
        print(f"Cleanup: removed {removed} old backup dirs (>{RETENTION_DAYS}d)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
