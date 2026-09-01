#!/usr/bin/env python3
"""Right-size toolsets for AIW cron jobs.

Per research/efficient-ai-use-2026-09-01.md + research/aiw-token-efficiency-v4-2026-09-01.md:
69 of 186 crons have the full 5-toolset bundle enabled (`code_execution` +
`file` + `memory` + `skills` + `web`). Each toolset adds hundreds of tokens of
system-prompt scaffolding per turn. For crons that only need bash + state reads,
the other 3 toolsets are pure waste.

This script:
1. Loads /opt/data/.hermes/cron/jobs.json
2. For each cron, infers which toolsets the prompt actually uses
3. Compares to the currently-configured enabled_toolsets
4. If the configured set is a strict superset of the inferred set,
   write the right-sized set back
5. Is idempotent: running twice produces no further changes
6. Writes a JSON diff to /opt/data/state/toolset-rightsizing-2026-09-01.json

Heuristic mapping (prompt keywords → needed toolsets):

| Toolset | Trigger keywords |
|---|---|
| `code_execution` | bash, shell, subprocess, /bin/, systemctl, curl, wget, pip install |
| `file` | read, cat, read_file, read_state, /opt/data/, /opt/hermes/, .md, .json, .py |
| `web` | web_search, web_extract, http, https://, search the web, browse |
| `memory` | memory, remember, recall, previous context |
| `skills` | skill, skills_hub, hub skill |

Default: NO toolsets (cron that genuinely needs none is fine).

Run:
    python3 scripts/right-size-toolsets.py             # apply
    python3 scripts/right-size-toolsets.py --dry-run    # preview only
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

JOBS_FILE = Path("/opt/data/.hermes/cron/jobs.json")
OUTPUT_DIFF = Path("/opt/data/state/toolset-rightsizing-2026-09-01.json")

ALL_TOOLSETS = {"code_execution", "file", "memory", "skills", "web"}

# Keyword → toolset inference
INFERENCE_RULES = {
    "code_execution": [
        r"\bbash\b", r"\bshell\b", r"\bsubprocess\b", r"/bin/",
        r"\bsystemctl\b", r"\bcurl\b", r"\bwget\b", r"\bpip install\b",
        r"`[^`]*`",  # any inline backtick = likely a shell command
    ],
    "file": [
        r"\bread\b", r"\bcat\b", r"\bread_file\b", r"\bread_state\b",
        r"/opt/data/", r"/opt/hermes/", r"\.md\b", r"\.json\b", r"\.py\b",
        r"\bPROMPT\.md\b",
    ],
    "web": [
        r"\bweb_search\b", r"\bweb_extract\b", r"https?://",
        r"\bsearch the web\b", r"\bbrowse\b",
    ],
    "memory": [
        r"\bmemory\b", r"\bremember\b", r"\brecall\b", r"\bprevious context\b",
    ],
    "skills": [
        r"\bskill\b", r"\bskills_hub\b", r"\bhub skill\b",
    ],
}

# Compile patterns once
COMPILED_RULES = {ts: [re.compile(p, re.IGNORECASE) for p in patterns]
                  for ts, patterns in INFERENCE_RULES.items()}


def infer_toolsets(prompt: str) -> set[str]:
    """Return the set of toolsets the prompt actually needs."""
    needed = set()
    for ts, patterns in COMPILED_RULES.items():
        for p in patterns:
            if p.search(prompt):
                needed.add(ts)
                break
    return needed


def process_jobs(dry_run: bool = False, force: bool = False) -> dict:
    """Read jobs, compute diff, optionally apply.

    SAFETY: dry-run is the default. To apply changes you must pass
    --apply --force, after reviewing the diff in dry-run output.
    The heuristic has known false-negatives (e.g. `repo-ci-monitor` prompt
    needs code_execution but the keyword heuristic doesn't infer it).
    Never apply without manual review of every diff.
    """
    jobs = json.loads(JOBS_FILE.read_text())
    diffs = []
    kept = []
    no_change = 0

    for j in jobs["jobs"]:
        name = j["name"]
        configured = set(j.get("enabled_toolsets") or set())
        prompt = j.get("prompt", "")

        # Skip crons with no prompt (script-only)
        if not prompt.strip():
            no_change += 1
            continue

        inferred = infer_toolsets(prompt)

        if configured == inferred:
            no_change += 1
            continue

        # If configured is a strict superset of inferred, we can shrink
        if configured and inferred.issubset(configured) and configured != inferred:
            excess = configured - inferred
            diffs.append({
                "name": name,
                "before": sorted(configured),
                "after": sorted(inferred),
                "excess": sorted(excess),
            })
            if not dry_run:
                j["enabled_toolsets"] = sorted(inferred) if inferred else None
        elif not configured and inferred:
            # Under-specified — add the missing toolsets
            diffs.append({
                "name": name,
                "before": [],
                "after": sorted(inferred),
                "excess": [],
            })
            if not dry_run:
                j["enabled_toolsets"] = sorted(inferred)
        else:
            # Configured is missing something inferred needs — leave alone
            kept.append({"name": name, "configured": sorted(configured),
                         "inferred": sorted(inferred)})

    summary = {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "total_jobs": len(jobs["jobs"]),
        "right_sized": len(diffs),
        "no_change": no_change,
        "left_alone_under_specified": len(kept),
        "dry_run": dry_run,
        "diffs": diffs,
        "left_alone": kept[:20],  # cap at 20 for readability
    }

    if not dry_run and diffs:
        JOBS_FILE.write_text(json.dumps(jobs, indent=2))
        OUTPUT_DIFF.write_text(json.dumps(summary, indent=2))

    return summary


def main():
    parser = argparse.ArgumentParser(description="Right-size cron toolsets (dry-run only by default)")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Preview only (DEFAULT — no flag needed)")
    parser.add_argument("--apply", action="store_true",
                        help="Apply changes (requires --force)")
    parser.add_argument("--force", action="store_true",
                        help="Skip confirmation prompt (use only after reviewing --dry-run output)")
    args = parser.parse_args()

    # If --apply was passed, use that; otherwise dry-run
    apply_mode = args.apply
    dry_run = not apply_mode

    if apply_mode and not args.force:
        print("ERROR: --apply requires --force to skip safety check.", file=sys.stderr)
        print("       Run with --dry-run first, review the diff, then re-run with --apply --force.", file=sys.stderr)
        return 1

    summary = process_jobs(dry_run=dry_run, force=args.force)

    print(f"=== Toolset Right-Sizing Summary ===")
    print(f"  Total jobs: {summary['total_jobs']}")
    print(f"  Will right-size: {summary['right_sized']}")
    print(f"  No change needed: {summary['no_change']}")
    print(f"  Left alone (under-specified): {summary['left_alone_under_specified']}")
    print(f"  Dry run: {summary['dry_run']}")
    print()
    print(f"=== First 15 diffs ===")
    for d in summary["diffs"][:15]:
        before = d["before"] if d["before"] else "(none)"
        after = d["after"] if d["after"] else "(none)"
        print(f"  {d['name']:40s}: {before} → {after}")

    if not args.dry_run:
        print(f"\nWritten: {JOBS_FILE}")
        print(f"Diff:    {OUTPUT_DIFF}")

    return 0


if __name__ == "__main__":
    sys.exit(main())