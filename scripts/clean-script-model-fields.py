#!/usr/bin/env python3
"""
clean-script-model-fields.py — Clear model/provider on no_agent=True cron jobs.

Script-only jobs (no_agent=True) don't make LLM calls, so model/provider fields
are meaningless on them. This script clears them for consistency and to prevent
operators from being confused about which jobs actually use the LLM.

Idempotent. Reports what it changed.

Created: 2026-09-03 (AIW litellm cleanup).
"""
import json
import shutil
import sys
from pathlib import Path

CANONICAL = Path("/opt/data/.hermes/cron/jobs.json")
GATEWAY = Path("/opt/data/cron/jobs.json")


def main() -> int:
    if not CANONICAL.exists():
        print(f"ERROR: {CANONICAL} not found", file=sys.stderr)
        return 1

    data = json.loads(CANONICAL.read_text())
    jobs = data["jobs"]

    cleaned = []
    for j in jobs:
        if j.get("enabled") and j.get("no_agent"):
            if j.get("model") or j.get("provider"):
                j["model"] = None
                j["provider"] = None
                j["_last_modified_by"] = "clean-script-model-fields.py"
                j["_last_modified"] = "2026-09-03T16:50:00+00:00"
                cleaned.append(j["name"])

    print(f"Cleaned {len(cleaned)} script-only jobs")

    if cleaned:
        tmp = CANONICAL.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.replace(CANONICAL)
        shutil.copy2(CANONICAL, GATEWAY)
        print("Cron registry updated (canonical + gateway)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
