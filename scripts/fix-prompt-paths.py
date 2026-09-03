#!/usr/bin/env python3
"""
fix-prompt-paths.py — Fix stale PROMPT.md paths in cron job prompts.

Background: Some cron jobs reference PROMPT.md paths at the old non-dept-prefixed
location (e.g. /opt/data/agents/foo/PROMPT.md) when the actual file lives at
/opt/data/agents/<dept>/foo/PROMPT.md. The LLM still runs (status=ok) but with
incomplete context.

This script:
  1. Reads jobs.json
  2. For each active agent-driven job, extracts the PROMPT.md path from the prompt
  3. If the path doesn't exist, looks for the real PROMPT.md by agent name
  4. Updates the prompt to point at the real path
  5. Atomically writes back

Idempotent. Reports what it changed.

Usage:
  python3 scripts/fix-prompt-paths.py            # apply
  python3 scripts/fix-prompt-paths.py --dry-run  # report only

Created: 2026-09-03 (AIW token audit followup).
"""
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

CANONICAL = Path("/opt/data/.hermes/cron/jobs.json")
GATEWAY = Path("/opt/data/cron/jobs.json")
AGENTS_DIR = Path("/opt/data/agents")


def find_real_prompt(name_hint: str) -> str | None:
    """Find the real PROMPT.md for an agent by name hint.

    name_hint is typically the agent dir name (e.g. "multimedia-producer").
    We search for both exact match and common suffixes (-daily, -weekly).
    """
    candidates = [
        Path(AGENTS_DIR) / f"{name_hint}/PROMPT.md",
    ]
    # Try stripping common suffixes from the name hint
    for suffix in ("-on-demand", "-daily", "-weekly", "-monthly"):
        stripped = name_hint.removesuffix(suffix) if name_hint.endswith(suffix) else None
        if stripped:
            candidates.append(Path(AGENTS_DIR) / f"{stripped}/PROMPT.md")
    # Search recursively
    for c in candidates:
        if c.exists():
            return str(c)
    # Last resort: recursive search by name
    for p in AGENTS_DIR.rglob(f"*/{name_hint}/PROMPT.md"):
        if p.exists():
            return str(p)
    return None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    data = json.loads(CANONICAL.read_text())
    jobs = data["jobs"]

    fixed = []
    not_fixed = []

    for j in jobs:
        if not j.get("enabled") or j.get("no_agent"):
            continue
        prompt = j.get("prompt", "") or ""
        paths = re.findall(r"/opt/data/[/\w\-]+/PROMPT\.md", prompt)
        if not paths:
            continue
        stale_path = paths[0]
        if os.path.exists(stale_path):
            continue

        # Try multiple name hints
        name_hints = [
            j["name"].replace("aiw-", ""),
            j["name"].replace("aiw-", "").replace("-on-demand", ""),
            j["name"].replace("aiw-", "").replace("-daily", ""),
            j["name"].replace("aiw-", "").replace("-weekly", ""),
        ]
        real_path = None
        for hint in name_hints:
            real_path = find_real_prompt(hint)
            if real_path:
                break

        if real_path:
            if args.dry_run:
                fixed.append((j["name"], stale_path, real_path))
            else:
                j["prompt"] = prompt.replace(stale_path, real_path)
                j["_last_modified_by"] = "fix-prompt-paths.py"
                j["_last_modified"] = "2026-09-03T05:40:00+00:00"
                fixed.append((j["name"], stale_path, real_path))
        else:
            not_fixed.append((j["name"], stale_path))

    if not args.dry_run and fixed:
        tmp = CANONICAL.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.replace(CANONICAL)
        shutil.copy2(CANONICAL, GATEWAY)

    print(f"{'[DRY-RUN] ' if args.dry_run else ''}Fixed: {len(fixed)}")
    for n, old, new in fixed:
        print(f"  {n}: {old} -> {new}")
    if not_fixed:
        print(f"\nNot fixed (no real PROMPT.md found): {len(not_fixed)}")
        for n, p in not_fixed:
            print(f"  {n}: {p}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
