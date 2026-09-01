#!/usr/bin/env python3
"""agent-context-loader.py — Runtime loader for parent_spec references.

Phase 9 R3 / Tier B8. Implements ADR-0001 and ADR-0003.

Per the audit (BUG-HUNT-2026-09-01.md), only 3/74 PROMPT.md files have
parent_spec fields, but the agent design assumes every agent has one.
This loader:

  1. Audits every PROMPT.md for parent_spec correctness
  2. Builds a cache: {agent_path: parent_spec_path}
  3. Resolves the actual parent_spec based on dept:
     - dept-01-*: departments/01-*
     - dept-02-*: departments/02-*
     - dept-03-*: departments/03-*
     - dept-04-*: departments/04-*
     - dept-05-*: departments/05-*
     - dept-06-*: departments/06-*
     - board-*: departments/00-board-charter.md
     - demiurge/*: constitution/ORG-AGENTS.md
     - tier3/*: TBD (none yet)

CLI:
  python3 agent-context-loader.py audit
  python3 agent-context-loader.py resolve <agent_path>
  python3 agent-context-loader.py cache     # build + write cache
  python3 agent-context-loader.py validate  # check all are correct
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path("/opt/data/agents")
CONSTITUTION = REPO / "constitution" / "ORG-AGENTS.md"
CACHE_PATH = Path("/opt/data/state/agent-parent-spec-cache.json")

DEPT_PREFIX_MAP = {
    "01-operations": "constitution/ORG-AGENTS.md",  # dept charter missing
    "02-finance-legal": "constitution/ORG-AGENTS.md",  # dept charter missing
    "03-sales-growth": "departments/03-sales-growth.md",
    "04-engineering": "departments/04-engineering-delivery.md",
    "05-research-education": "departments/05-research-education.md",
    "06-people-culture": "departments/06-people-culture.md",
    "board-of-directors": "constitution/ORG-AGENTS.md",  # board charter not yet written; use ORG-AGENTS
}


def find_prompt_files() -> list[Path]:
    """Find all PROMPT.md files in the repo."""
    return sorted(REPO.glob("*/PROMPT.md")) + sorted(REPO.glob("*/*/PROMPT.md"))


def infer_parent_spec(prompt_path: Path) -> str:
    """Infer the correct parent_spec for an agent based on its dept prefix."""
    # Find the top-level dept (e.g., "04-engineering" in "04-engineering/ai-safety-engineer/PROMPT.md")
    parts = prompt_path.relative_to(REPO).parts
    if parts[0].startswith("demiurge"):
        return str(CONSTITUTION.relative_to(REPO))
    # Department-based agents (including board-of-directors)
    if parts[0] in DEPT_PREFIX_MAP:
        return DEPT_PREFIX_MAP[parts[0]]
    return str(CONSTITUTION.relative_to(REPO))  # default fallback


def audit() -> int:
    """Audit all PROMPT.md files for parent_spec correctness."""
    prompts = find_prompt_files()
    missing = []
    incorrect = []
    correct = []
    for p in prompts:
        content = p.read_text()
        m = re.search(r"^parent_spec:\s*(.+)$", content, re.MULTILINE)
        if not m:
            missing.append(str(p.relative_to(REPO)))
        else:
            current = m.group(1).strip()
            expected = infer_parent_spec(p)
            if current != expected:
                incorrect.append({
                    "path": str(p.relative_to(REPO)),
                    "current": current,
                    "expected": expected,
                })
            else:
                correct.append(str(p.relative_to(REPO)))
    print(f"Audit complete:")
    print(f"  Total PROMPT.md: {len(prompts)}")
    print(f"  Correct parent_spec: {len(correct)}")
    print(f"  Missing parent_spec: {len(missing)}")
    print(f"  Incorrect parent_spec: {len(incorrect)}")
    if missing:
        print(f"\nFirst 10 missing:")
        for m in missing[:10]:
            print(f"  - {m}")
    if incorrect:
        print(f"\nFirst 10 incorrect:")
        for inc in incorrect[:10]:
            print(f"  - {inc['path']}: {inc['current']} → {inc['expected']}")
    return 0 if not missing and not incorrect else 1


def resolve(agent_path: str) -> int:
    """Resolve parent_spec for a given agent."""
    p = REPO / agent_path
    if not p.exists():
        print(f"ERROR: {p} not found")
        return 1
    expected = infer_parent_spec(p)
    expected_full = (REPO / expected).resolve()
    print(f"Agent: {agent_path}")
    print(f"parent_spec: {expected}")
    print(f"Full path: {expected_full}")
    print(f"Exists: {expected_full.exists()}")
    return 0 if expected_full.exists() else 1


def cache() -> int:
    """Build the parent_spec cache."""
    prompts = find_prompt_files()
    cache_data = {}
    for p in prompts:
        rel = str(p.relative_to(REPO))
        cache_data[rel] = infer_parent_spec(p)
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache_data, indent=2, sort_keys=True))
    print(f"Cache written: {CACHE_PATH} ({len(cache_data)} entries)")
    return 0


def validate() -> int:
    """Validate all parent_spec references resolve to existing files."""
    if not CACHE_PATH.exists():
        print("Cache missing — run `cache` first")
        return 1
    cache_data = json.loads(CACHE_PATH.read_text())
    missing_files = []
    for agent, spec in cache_data.items():
        full = REPO / spec
        if not full.exists():
            missing_files.append((agent, spec))
    print(f"Cache: {len(cache_data)} entries")
    print(f"Missing spec files: {len(missing_files)}")
    for a, s in missing_files[:10]:
        print(f"  - {a} → {s}")
    return 0 if not missing_files else 1


def main():
    parser = argparse.ArgumentParser(description="Agent parent_spec loader")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("audit", help="Audit parent_spec correctness")
    p_resolve = sub.add_parser("resolve", help="Resolve parent_spec for agent")
    p_resolve.add_argument("agent_path")
    sub.add_parser("cache", help="Build cache")
    sub.add_parser("validate", help="Validate cache")

    args = parser.parse_args()
    if args.cmd == "audit":
        return audit()
    if args.cmd == "resolve":
        return resolve(args.agent_path)
    if args.cmd == "cache":
        return cache()
    if args.cmd == "validate":
        return validate()
    return 0


if __name__ == "__main__":
    sys.exit(main())