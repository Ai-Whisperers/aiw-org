#!/usr/bin/env python3
"""fix-parent-spec.py — Bulk-add parent_spec to PROMPT.md files.

Phase 9 R3 / Tier B8. The audit found 47 PROMPT.md files but only 3
have parent_spec. This script adds parent_spec to all of them based on
the dept prefix mapping in agent-context-loader.py.

Usage:
  python3 fix-parent-spec.py --dry-run   # show what would change
  python3 fix-parent-spec.py --apply     # actually write
"""
import argparse
import re
import sys
from pathlib import Path

# Copy of the mapping from agent-context-loader.py
DEPT_PREFIX_MAP = {
    "01-operations": "constitution/ORG-AGENTS.md",
    "02-finance-legal": "constitution/ORG-AGENTS.md",
    "03-sales-growth": "departments/03-sales-growth.md",
    "04-engineering": "departments/04-engineering-delivery.md",
    "05-research-education": "departments/05-research-education.md",
    "06-people-culture": "departments/06-people-culture.md",
    "board-of-directors": "constitution/ORG-AGENTS.md",
}

REPO = Path("/opt/data/agents")


def find_prompt_files() -> list[Path]:
    """Find all PROMPT.md files in the repo."""
    return sorted(REPO.glob("*/PROMPT.md")) + sorted(REPO.glob("*/*/PROMPT.md"))


def infer_parent_spec(prompt_path: Path) -> str:
    parts = prompt_path.relative_to(REPO).parts
    if parts[0].startswith("demiurge"):
        return "constitution/ORG-AGENTS.md"
    if parts[0] in DEPT_PREFIX_MAP:
        return DEPT_PREFIX_MAP[parts[0]]
    return "constitution/ORG-AGENTS.md"


def has_frontmatter(content: str) -> bool:
    return content.startswith("---\n")


def has_parent_spec(content: str) -> bool:
    return bool(re.search(r"^parent_spec:\s*", content, re.MULTILINE))


def insert_parent_spec(content: str, parent_spec: str) -> str:
    """Insert parent_spec line at the end of frontmatter."""
    if not has_frontmatter(content):
        # Add frontmatter with parent_spec
        return f"---\nparent_spec: {parent_spec}\n---\n{content}"
    # Find end of frontmatter
    lines = content.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line == "---":
            end_idx = i
            break
    if end_idx is None:
        # No closing ---; add parent_spec at top
        return f"parent_spec: {parent_spec}\n---\n{content}"
    # Insert before closing ---
    lines.insert(end_idx, f"parent_spec: {parent_spec}")
    return "\n".join(lines)


def update_parent_spec(content: str, new_value: str) -> str:
    """Replace existing parent_spec with new value."""
    return re.sub(
        r"^parent_spec:\s*.+$",
        f"parent_spec: {new_value}",
        content,
        count=1,
        flags=re.MULTILINE,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--apply", action="store_true", help="Actually write changes")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("ERROR: must specify --dry-run or --apply")
        return 1

    prompts = find_prompt_files()
    changes = []
    for p in prompts:
        content = p.read_text()
        rel = str(p.relative_to(REPO))
        expected = infer_parent_spec(p)

        if has_parent_spec(content):
            m = re.search(r"^parent_spec:\s*(.+)$", content, re.MULTILINE)
            current = m.group(1).strip()
            if current != expected:
                changes.append((p, "update", current, expected))
                if args.apply:
                    new_content = update_parent_spec(content, expected)
                    p.write_text(new_content)
        else:
            changes.append((p, "add", None, expected))
            if args.apply:
                new_content = insert_parent_spec(content, expected)
                p.write_text(new_content)

    print(f"{'[DRY-RUN] ' if args.dry_run else '[APPLIED] '}"
          f"{len(changes)} changes across {len(prompts)} PROMPT.md files")
    for p, kind, old, new in changes[:10]:
        print(f"  {kind:6s} {p.relative_to(REPO)}")
        print(f"    {old} → {new}")
    if len(changes) > 10:
        print(f"  ... and {len(changes) - 10} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())