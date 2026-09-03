#!/usr/bin/env python3
"""Fix Hermes script-path blocks by setting workdir=/opt/data."""
import json, shutil, sys
from pathlib import Path

CANONICAL = Path("/opt/data/.hermes/cron/jobs.json")
GATEWAY = Path("/opt/data/cron/jobs.json")
BACKUP = Path("/opt/data/.hermes/cron/jobs.json.pre-workdir-fix-20260903.bak")

WORKDIR_EXCEPTIONS = {"aiw-script-tests"}

if not BACKUP.exists():
    shutil.copy2(CANONICAL, BACKUP)
    print(f"Backup: {BACKUP}")

data = json.loads(CANONICAL.read_text())
jobs = data["jobs"]

fixed = 0
for j in jobs:
    if not j.get("enabled"):
        continue
    name = j.get("name", "")
    if name in WORKDIR_EXCEPTIONS:
        continue
    msg = j.get("last_error", "") or ""
    if "Blocked: script path" in msg:
        old_wd = j.get("workdir")
        j["workdir"] = "/opt/data"
        j["_last_modified_by"] = "fix-cron-workdirs.py"
        j["_last_modified"] = "2026-09-03T02:25:00+00:00"
        print(f"  fix: {name:50} workdir: {old_wd} -> /opt/data")
        fixed += 1

print(f"\nFixed: {fixed} jobs")

tmp = CANONICAL.with_suffix(".tmp")
tmp.write_text(json.dumps(data, indent=2))
tmp.replace(CANONICAL)
shutil.copy2(CANONICAL, GATEWAY)

def norm(p):
    d = json.loads(Path(p).read_text())
    return sorted(
        [{k: j.get(k) for k in ("id","name","schedule","provider","enabled","workdir")}
         for j in d["jobs"]],
        key=lambda x: x.get("id") or x.get("name",""))

if norm(CANONICAL) == norm(GATEWAY):
    print("Mirror parity: OK")
else:
    print("Mirror parity: MISMATCH")
