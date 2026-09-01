#!/usr/bin/env python3
"""Quarterly org-chart review.

Built Phase 7 R5 (implementation plan §4 Phase 2.7).

Scans:
  - /opt/data/agents/departments/       (charter files = dept-level agents)
  - /opt/data/agents/04-*/              (engineering dept sub-agents)
  - /opt/data/agents/05-*/              (research dept sub-agents)
  - /opt/data/agents/demiurge/agents/   (atomic demiurge agents)

Compares to last quarter's roster. Flags:
  - Added agents (new since last quarter)
  - Removed agents (missing now)
  - Changed topologies (cluster: field)
  - Hard-stop changes

Output: /opt/data/agents/state/org-chart-review.json (atomic per P2).

Usage:
    python3 scripts/org-chart-review.py              # compute + write
    python3 scripts/org-chart-review.py --print      # print only
"""

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

AGENTS_REPO = Path("/opt/data/agents")
STATE_FILE = Path("/opt/data/agents/state/org-chart-review.json")
PRIOR_STATE = Path("/opt/data/state/org-chart-review.json")

# Directories to scan
SCAN_PATHS = [
    AGENTS_REPO / "departments",
    AGENTS_REPO / "04-engineering",
    AGENTS_REPO / "05-research-education",
    AGENTS_REPO / "demiurge" / "agents",
    AGENTS_REPO / "03-sales-growth",
    AGENTS_REPO / "02-finance-legal",
    AGENTS_REPO / "01-operations",
    AGENTS_REPO / "06-people-culture",
]


def atomic_write_json(path: Path, payload: dict) -> None:
    """P2 pattern."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            path.replace(path.with_suffix(path.suffix + ".bak"))
        except OSError:
            pass
    fd, tmp = tempfile.mkstemp(prefix=".orgchart-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter as flat dict."""
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm = text[3:end]
    out = {}
    for line in fm.splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def scan_agents() -> dict:
    """Scan all PROMPT.md files and build roster."""
    roster = {}
    for parent in SCAN_PATHS:
        if not parent.exists():
            continue
        for prompt in parent.rglob("PROMPT.md"):
            if "monitor-notes" in str(prompt) or "__pycache__" in str(prompt):
                continue
            try:
                text = prompt.read_text(encoding="utf-8", errors="replace")
                fm = parse_frontmatter(text)
                if "name" not in fm:
                    continue
                roster[fm["name"]] = {
                    "path": str(prompt.relative_to(AGENTS_REPO)),
                    "topology": fm.get("topology"),
                    "cluster": fm.get("cluster"),
                    "layer": fm.get("layer"),
                    "archetype": fm.get("archetype"),
                    "owner": fm.get("owner"),
                    "version": fm.get("version"),
                }
            except (OSError, UnicodeError):
                pass
    return roster


def diff_rosters(prior: dict, current: dict) -> dict:
    """Compute add/remove/change diff."""
    prior_names = set(prior.keys())
    current_names = set(current.keys())

    added = sorted(current_names - prior_names)
    removed = sorted(prior_names - current_names)
    common = prior_names & current_names

    changed = []
    for name in sorted(common):
        if prior[name] != current[name]:
            changes = {}
            for k in prior[name]:
                if prior[name].get(k) != current[name].get(k):
                    changes[k] = {"before": prior[name].get(k), "after": current[name].get(k)}
            if changes:
                changed.append({"name": name, "changes": changes})

    return {
        "added": added,
        "removed": removed,
        "changed": changed,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "Org chart review")
    p.add_argument("--print", action="store_true")
    args = p.parse_args(argv)

    current = scan_agents()
    prior = {}
    if PRIOR_STATE.exists():
        try:
            prior_data = json.loads(PRIOR_STATE.read_text())
            prior = prior_data.get("roster", {})
        except json.JSONDecodeError:
            pass

    diff = diff_rosters(prior, current)

    # Cluster distribution
    by_cluster = {"run": 0, "build": 0, "enable": 0, "unset": 0}
    for a in current.values():
        c = a.get("cluster") or "unset"
        by_cluster[c] = by_cluster.get(c, 0) + 1

    by_topology = {}
    for a in current.values():
        t = a.get("topology") or "unset"
        by_topology[t] = by_topology.get(t, 0) + 1

    payload = {
        "version": "1.0.0",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "agent_count": len(current),
        "roster": current,
        "by_cluster": by_cluster,
        "by_topology": by_topology,
        "diff_vs_prior": diff,
        "comparison_prior_state": str(PRIOR_STATE) if prior else None,
    }

    if args.print:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    atomic_write_json(STATE_FILE, payload)
    # Update prior state for next quarter's diff
    try:
        atomic_write_json(PRIOR_STATE, payload)
    except OSError:
        pass

    d = diff
    print(
        f"Org chart review: {len(current)} agents | "
        f"added={len(d['added'])} removed={len(d['removed'])} changed={len(d['changed'])} | "
        f"clusters={by_cluster}"
    )
    if d["added"]:
        print(f"  NEW: {d['added']}")
    if d["removed"]:
        print(f"  REMOVED: {d['removed']}")
    if d["changed"]:
        print(f"  CHANGED: {[c['name'] for c in d['changed']]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())