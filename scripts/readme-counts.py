#!/usr/bin/env python3
"""readme-counts.py — Regenerate README counts from live state.

Per DEMIURGE-096 (Phase Kernel brief WS-2 item 2):
  "scripts/readme-counts.py --check, wired into CI, so README claims
   must match measurement."

This script measures real numbers from the repo and live host, then
either:
- --check: exits 0 if README matches, 1 if it doesn't
- (default): prints the measurements as a Markdown table

Usage:
    python3 scripts/readme-counts.py --check
    python3 scripts/readme-counts.py            # prints table
    python3 scripts/readme-counts.py --diff   # shows what would change
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path("/opt/data/agents-v2/aiw-org-clone")
LIVE = Path("/opt/data/agents")
README = REPO / "README.md"


def count_prompts(repo_root: Path, live_root: Path | None = None) -> int:
    """Total unique PROMPT.md files.

    Counts ONLY the repo clone (not the live host). The repo is the
    authoritative source-of-truth for README claims; the live host
    is a runtime snapshot that gets synced FROM the repo. Counting
    both would double-count identical files.

    The `live_root` parameter is accepted for signature compatibility
    but not used.
    """
    seen = set()
    for p in repo_root.rglob("PROMPT.md"):
        if ".git" in p.parts:
            continue
        # Resolve to handle symlinks (e.g. marketing-content-mon-wed-fri)
        try:
            seen.add(p.resolve())
        except (OSError, RuntimeError):
            seen.add(p)
    return len(seen)


def count_prompt_monitors(repo_root: Path) -> int:
    """PROMPT-monitor.md files (one per monitored agent)."""
    return sum(1 for _ in repo_root.rglob("PROMPT-monitor.md")
               if ".git" not in _.parts)


def count_cron_jobs() -> int:
    """Enabled cron jobs (live host).

    The canonical cron registry is at /opt/data/.hermes/cron/jobs.json
    (NOT /opt/data/agents/.hermes/). The /agents path is a placeholder.
    """
    cron_paths = [
        Path("/opt/data/.hermes/cron/jobs.json"),  # canonical
        LIVE / ".hermes" / "cron" / "jobs.json",   # fallback
        REPO / ".hermes" / "cron" / "jobs.json",   # repo-clone fallback
    ]
    for cron_file in cron_paths:
        if cron_file.exists():
            try:
                data = json.loads(cron_file.read_text())
                jobs = data if isinstance(data, list) else data.get("jobs", [])
                return sum(1 for j in jobs if j.get("enabled", True))
            except (json.JSONDecodeError, KeyError):
                continue
    return 0


def count_kpi_stacks() -> int:
    """KPI YAML files (per dept)."""
    kpi_dir = REPO / "demiurge" / "kpi"
    if not kpi_dir.exists():
        return 0
    return len(list(kpi_dir.glob("*-stack.yaml")))


def count_signal_routes() -> int:
    """Signal YAML files in demiurge/signals/."""
    sig_dir = REPO / "demiurge" / "signals"
    if not sig_dir.exists():
        return 0
    return len(list(sig_dir.glob("*.yaml")))


def count_research_areas() -> int:
    """Research areas documented (per dept + board).

    Counts numbered research areas (### N. ...) within each
    *-research-areas.md file. Pattern follows research/DEPT-RESEARCH-METHODOLOGY.md
    which uses ### N. Title for each area.
    """
    depts_dir = REPO / "research" / "dept-research"
    if not depts_dir.exists():
        return 0
    total = 0
    for f in depts_dir.glob("*-research-areas.md"):
        if f.is_file():
            # Each numbered research area is at H3 level: ### N. Title
            text = f.read_text()
            # Match "### N." at start of line (the "N." indicates
            # numbering; plain "###" headers are section dividers)
            total += sum(1 for line in text.split('\n')
                          if line.startswith("### ") and ". " in line[5:10])
    return total


def count_charter_departments(repo_root: Path, live_root: Path | None = None) -> int:
    """Tier-1 charter departments (the NN-* dirs at top level).

    Counts NN-* dirs at the top level. Live root is the canonical
    source per the README ("Source-of-truth (live)").
    """
    def _count(root: Path) -> int:
        if not root.exists():
            return 0
        depts = [d.name for d in root.iterdir()
                 if d.is_dir() and re.match(r"^\d{2}-", d.name)]
        if (root / "board-of-directors").is_dir():
            depts.append("board-of-directors")
        return len(depts)

    # Live host is canonical
    if live_root and live_root.exists():
        return _count(live_root)
    return _count(repo_root)


def measure() -> dict:
    """Compute all current measurements."""
    return {
        "Tier-1 charter departments": count_charter_departments(REPO, LIVE),
        "PROMPT.md files (all agents)": count_prompts(REPO, LIVE),
        "PROMPT-monitor.md files": count_prompt_monitors(REPO),
        "Cron jobs (heartbeat)": count_cron_jobs(),
        "KPI stacks (per dept)": count_kpi_stacks(),
        "Signal routes (per dept)": count_signal_routes(),
        "Research areas documented": count_research_areas(),
    }


def read_readme_claims(readme_path: Path) -> dict:
    """Parse the README's metrics table.

    Handles two formats:
    1. Standard Markdown table row: | Metric | **NN** |
    2. Inline count: "Metric: NN" or "Metric: NN (description)"

    Returns {metric: claimed_value_str}.
    """
    if not readme_path.exists():
        return {}
    text = readme_path.read_text()
    claims = {}

    # Format 1: | Metric | **NN** |
    for m in re.finditer(
        r"\|\s*\*?\*?([^|\*]+?)\*?\*?\s*\|\s*"
        r"\*?\*?(\d+(?:\+\d*)?)\*?\*?\s*\|",
        text,
    ):
        metric = m.group(1).strip().rstrip(":")
        if metric and metric not in ("Metric", "---"):
            claims[metric] = m.group(2).strip()

    # Format 2: "Metric: NN" (no table format)
    table_keys = set(claims.keys())
    for m in re.finditer(
        r"\*\*([^*]+?):\*\*\s*\*?\*?(\d+(?:\+\d*)?)",
        text,
    ):
        metric = m.group(1).strip()
        if metric and metric not in table_keys:
            claims[metric] = m.group(2).strip()

    return claims


def normalize_count(s: str) -> int:
    """Parse "7", "86+", "309 files" -> int. Strips non-digits suffix."""
    s = s.strip().rstrip("+").strip()
    # Take first numeric token
    m = re.match(r"(\d+)", s)
    return int(m.group(1)) if m else -1


def check(measurements: dict, claims: dict) -> tuple[bool, list]:
    """Return (all_match, list of mismatches)."""
    mismatches = []
    for metric, claimed in claims.items():
        if metric not in measurements:
            # README claims a metric we don't measure — skip silently
            continue
        claimed_n = normalize_count(claimed)
        actual_n = measurements[metric]
        if claimed_n != actual_n:
            mismatches.append({
                "metric": metric,
                "claimed": claimed,
                "actual": actual_n,
            })
    return len(mismatches) == 0, mismatches


def format_table(measurements: dict) -> str:
    """Format measurements as a Markdown table."""
    rows = ["| Metric | Count |", "| --- | ---: |"]
    for k, v in measurements.items():
        rows.append(f"| {k} | {v} |")
    return "\n".join(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="exit 0 if README matches, 1 if it doesn't")
    ap.add_argument("--diff", action="store_true",
                    help="print what would change in the README")
    args = ap.parse_args()

    measurements = measure()
    claims = read_readme_claims(README)

    if args.check:
        ok, mismatches = check(measurements, claims)
        if ok:
            print(f"[readme-counts] ✓ README matches measurements ({len(measurements)} metrics)")
            return 0
        print(f"[readme-counts] ✗ README has {len(mismatches)} mismatches:")
        for m in mismatches:
            print(f"  {m['metric']}: claimed={m['claimed']!r}, actual={m['actual']}")
        return 1

    if args.diff:
        ok, mismatches = check(measurements, claims)
        if not mismatches:
            print("[readme-counts] README matches. No diff.")
            return 0
        print("[readme-counts] README needs updating:")
        for m in mismatches:
            print(f"  - {m['metric']}: {m['claimed']} -> {m['actual']}")
        return 0

    # Default: print table
    print(format_table(measurements))
    return 0


if __name__ == "__main__":
    sys.exit(main())
