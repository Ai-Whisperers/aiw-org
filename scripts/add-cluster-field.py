#!/usr/bin/env python3
"""Add `cluster:` field to PROMPT.md frontmatters.

Built Phase 7 R5 (implementation plan §4 Phase 1.6).

Maps each agent to Run/Build/Enable cluster (per theorgchart.com IT
blueprints):

  Run     = always-on monitors (every 30 min): devops, security,
            ai-safety, chaos-test, drift-detector, eval-gate-runner,
            compliance-monitor
  Build   = shipping agents: engineering-roster, qa-automation-runner,
            qa-automation-on-pr, security-auditor, security-watchdog
  Enable  = gating/scopes: scope-intake, delivery-tracker,
            feasibility-gate, architect-agent, auditor-agent

Safe to re-run (idempotent — skips if field already present).
"""

import sys
from pathlib import Path

# Mapping agent → cluster
CLUSTERS = {
    # Run (always-on monitors)
    "ai-safety-engineer": "run",
    "ai-safety-engineer-30min": "run",
    "chaos-test-runner": "run",
    "compliance-monitor": "run",
    "devops-monitor": "run",
    "devops-monitor-30min": "run",
    "drift-detector": "run",
    "eval-gate-runner": "run",
    # Build (shipping/PR)
    "engineering-roster": "build",
    "qa-automation-on-pr": "build",
    "qa-automation-runner": "build",
    "security-auditor": "build",
    "security-watchdog": "build",
    "security-watchdog-30min": "build",
    # Enable (gates / scopes)
    "architect-agent": "enable",
    "auditor-agent": "enable",
    "delivery-tracker": "enable",
    "feasibility-gate": "enable",
    "scope-intake": "enable",
}

# Where to find PROMPT.md files
AGENTS_REPO = Path("/opt/data/agents")
SEARCH_PATHS = [
    AGENTS_REPO / "04-engineering",
    AGENTS_REPO / "demiurge" / "agents",
]


def find_agent_dirs():
    """Yield (agent_name, prompt_path) for every agent."""
    for parent in SEARCH_PATHS:
        if not parent.exists():
            continue
        for d in parent.iterdir():
            if not d.is_dir():
                continue
            prompt = d / "PROMPT.md"
            if prompt.exists():
                yield d.name, prompt


def has_cluster_field(prompt_path: Path) -> bool:
    """Check if frontmatter already has cluster: field."""
    text = prompt_path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return False
    end = text.find("---", 3)
    if end == -1:
        return False
    frontmatter = text[3:end]
    for line in frontmatter.splitlines():
        if line.strip().startswith("cluster:"):
            return True
    return False


def add_cluster_field(prompt_path: Path, cluster: str) -> None:
    """Add `cluster: <cluster>` to frontmatter (after topology field if present)."""
    text = prompt_path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        print(f"  SKIP {prompt_path.parent.name}: no frontmatter")
        return
    end = text.find("---", 3)
    if end == -1:
        print(f"  SKIP {prompt_path.parent.name}: malformed frontmatter")
        return

    frontmatter = text[3:end]
    # IMPORTANT: preserve the newline after the closing --- delimiter
    # by keeping everything from end onward exactly as-is.
    rest = text[end:]

    # Insert after `topology:` line if present, else append to end of frontmatter
    lines = frontmatter.splitlines()
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if not inserted and line.strip().startswith("topology:"):
            new_lines.append(f"cluster: {cluster}")
            inserted = True

    if not inserted:
        new_lines.append(f"cluster: {cluster}")

    new_frontmatter = "\n".join(new_lines)
    new_text = "---" + new_frontmatter + rest
    # Ensure file ends with a newline (best practice)
    if not new_text.endswith("\n"):
        new_text += "\n"
    prompt_path.write_text(new_text, encoding="utf-8")
    print(f"  ADD {prompt_path.parent.name}: cluster={cluster}")


def main():
    added = 0
    skipped = 0
    unmapped = 0
    for name, prompt in find_agent_dirs():
        if name not in CLUSTERS:
            unmapped += 1
            continue
        if has_cluster_field(prompt):
            skipped += 1
            continue
        add_cluster_field(prompt, CLUSTERS[name])
        added += 1

    print(f"\n{added} added, {skipped} skipped (already have cluster), {unmapped} unmapped (not in CLUSTERS dict)")


if __name__ == "__main__":
    main()