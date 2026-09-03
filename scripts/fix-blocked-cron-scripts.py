#!/usr/bin/env python3
"""
fix-blocked-cron-scripts.py — Fix cron jobs whose script path resolves outside /opt/data/scripts/.

Background: Hermes cron scheduler enforces that script paths must resolve
within HERMES_HOME/scripts/ (which is /opt/data/scripts/ for the active profile).
Jobs whose scripts are symlinks pointing outside this dir, or point at
/opt/data/agents/scripts/ (the aiw-org repo copy), will be BLOCKED with
"script path resolves outside the scripts directory".

This script:
  1. Finds all enabled script-only jobs (no_agent=True)
  2. For each, checks if script path resolves within /opt/data/scripts/
  3. If not, fixes by either:
     a. Replacing the symlink with the real file content
     b. Updating the cron job's script path to point at the correct location

Reports changes; idempotent.

Created: 2026-09-03 (AIW token audit followup).
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

CANONICAL = Path("/opt/data/.hermes/cron/jobs.json")
GATEWAY = Path("/opt/data/cron/jobs.json")
SCRIPTS_DIR = Path("/opt/data/scripts")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if not CANONICAL.exists():
        print(f"ERROR: {CANONICAL} not found", file=sys.stderr)
        return 1

    data = json.loads(CANONICAL.read_text())
    jobs = data["jobs"]

    fixed = []
    for j in jobs:
        if not j.get("enabled") or not j.get("no_agent"):
            continue
        script = j.get("script")
        if not script:
            continue
        if not os.path.exists(script):
            continue  # File missing — separate issue
        resolved = os.path.realpath(script)
        if resolved.startswith(str(SCRIPTS_DIR) + "/"):
            continue  # Already good

        # Find a fix: either the symlink target, or the canonical script
        symlink = Path(script)
        if symlink.is_symlink():
            target = symlink.readlink()
            target_resolved = target if os.path.isabs(target) else (symlink.parent / target).resolve()
            # Replace symlink with real file content
            if target_resolved.exists():
                if not args.dry_run:
                    real_content = Path(target_resolved).read_bytes()
                    symlink.unlink()
                    symlink.write_bytes(real_content)
                    symlink.chmod(0o755)
                fixed.append((j["name"], str(symlink), f"replaced symlink with real file from {target_resolved}"))
            else:
                fixed.append((j["name"], str(symlink), f"SKIP: symlink target {target_resolved} does not exist"))
        elif "/opt/data/agents/scripts/" in script:
            # Path points at aiw-org repo. Try to find a /opt/data/scripts/ equivalent
            basename = os.path.basename(script)
            target_path = SCRIPTS_DIR / basename
            if target_path.exists():
                # Update cron to point at the /opt/data/scripts/ version
                if not args.dry_run:
                    j["script"] = str(target_path)
                    j["_last_modified_by"] = "fix-blocked-cron-scripts.py"
                    j["_last_modified"] = "2026-09-03T17:00:00+00:00"
                fixed.append((j["name"], script, str(target_path)))
            else:
                # Need to copy the file
                src = Path(script)
                if src.exists():
                    if not args.dry_run:
                        target_path.write_bytes(src.read_bytes())
                        target_path.chmod(0o755)
                        j["script"] = str(target_path)
                        j["_last_modified_by"] = "fix-blocked-cron-scripts.py"
                        j["_last_modified"] = "2026-09-03T17:00:00+00:00"
                    fixed.append((j["name"], script, f"copied to {target_path}"))

    if args.dry_run:
        print(f"[DRY-RUN] Would fix {len(fixed)} jobs:")
    else:
        print(f"Fixed {len(fixed)} jobs:")
    for n, old, new in fixed:
        print(f"  {n}: {old}")
        print(f"    -> {new}")

    if fixed and not args.dry_run:
        tmp = CANONICAL.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.replace(CANONICAL)
        shutil.copy2(CANONICAL, GATEWAY)
        print(f"\nCron registry updated")

    return 0


if __name__ == "__main__":
    sys.exit(main())
