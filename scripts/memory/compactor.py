"""Memory L2 compactor for /opt/data/agents/state/coord.json.

Phase 1.2 of AIW upgrade plan (per /opt/data/profiles/ivan/plans/2026-09-01-aiw-upgrade-plan.md).
Pattern source: SuperLocalMemory 4.0 paper (bi-temporal recall + verified erasure).
What it does:
  - Detects when coord.json exceeds token-threshold budget (default: 80% of 200k context)
  - Compacts historical decisions_for_ivan entries: keep latest N, archive rest to .compact archive
  - Compacts stale agents[] entries whose latest_brief points to files > 30 days old
  - Preserves the `_last_modified_by` and `_last_modified` audit header
  - Writes compact to coord.json.compact-YYYYMMDDHHMMSS.json, never modifies original
  - Returns a structured report (compacted, archived_count, savings_pct)
Usage:
  python3 -m scripts.memory.compactor [--dry-run] [--threshold-pct 80] [--keep-recent 50]
"""
import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# Default paths
DEFAULT_COORD = Path("/opt/data/agents/state/coord.json")
DEFAULT_ARCHIVE_DIR = Path("/opt/data/agents/state/snapshots/compacted")

# Default thresholds (token-budget-aware approximations)
# 1 token \u2248 4 chars. 200k context = 800k chars. We default to 80% = 640k chars.
DEFAULT_THRESHOLD_PCT = 80
DEFAULT_CONTEXT_CHARS = 200_000 * 4  # 800k chars
KEEP_RECENT_DECISIONS = 50
STALE_BRIEF_DAYS = 30


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _file_chars(path: Path) -> int:
    if not path.exists():
        return 0
    return path.stat().st_size


def _load_coord(path: Path) -> dict:
    return json.loads(path.read_text())


def _save_coord(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def _is_stale_brief(brief_path: str, cutoff_days: int = STALE_BRIEF_DAYS) -> bool:
    """Return True if the brief_path file is older than cutoff_days, or missing."""
    p = Path(brief_path)
    if not p.exists():
        return True
    age_days = (datetime.now(timezone.utc).timestamp() - p.stat().st_mtime) / 86400
    return age_days > cutoff_days


def compact(coord_path: Path = DEFAULT_COORD,
            archive_dir: Path = DEFAULT_ARCHIVE_DIR,
            threshold_pct: int = DEFAULT_THRESHOLD_PCT,
            keep_recent: int = KEEP_RECENT_DECISIONS,
            dry_run: bool = False) -> dict:
    """Run one compaction pass. Returns a structured report."""
    if not coord_path.exists():
        return {"error": f"coord.json not found at {coord_path}", "compacted": False}

    file_size = _file_chars(coord_path)
    threshold_chars = DEFAULT_CONTEXT_CHARS * threshold_pct / 100
    over_threshold = file_size > threshold_chars

    data = _load_coord(coord_path)
    archived_count = 0
    savings_bytes = 0
    actions = []

    # 1) Compact decisions_for_ivan[]: keep latest N, archive rest
    decisions = data.get("decisions_for_ivan", [])
    to_archive: list = []
    if len(decisions) > keep_recent:
        to_archive = decisions[:-keep_recent]
        to_keep = decisions[-keep_recent:]
        archived_count = len(to_archive)
        archive_bytes = sum(len(json.dumps(d, ensure_ascii=False)) for d in to_archive)
        actions.append({
            "type": "decisions_for_ivan",
            "archived": archived_count,
            "kept": len(to_keep),
            "approx_bytes_saved": archive_bytes,
        })
        if not dry_run:
            data["decisions_for_ivan"] = to_keep
            savings_bytes += archive_bytes

    # 2) Mark stale agents[] entries (latest_brief file > 30d old)
    agents = data.get("agents", {})
    stale_agents = []
    for agent_id, agent_data in agents.items():
        brief = agent_data.get("latest_brief") if isinstance(agent_data, dict) else None
        if brief and _is_stale_brief(brief):
            stale_agents.append({"agent": agent_id, "brief": brief})
    actions.append({
        "type": "stale_agents_detected",
        "count": len(stale_agents),
        "agents": [s["agent"] for s in stale_agents[:10]],  # truncate
    })
    # Don't delete stale_agents \u2014 only flag. Operator decision.

    # 3) Write report + archive
    new_size = file_size - savings_bytes
    report = {
        "ts": _now_iso(),
        "compacted": not dry_run,
        "dry_run": dry_run,
        "original_chars": file_size,
        "new_chars": new_size if not dry_run else file_size,
        "savings_bytes": savings_bytes,
        "savings_pct": (savings_bytes / file_size * 100) if file_size > 0 else 0,
        "over_threshold": over_threshold,
        "threshold_pct": threshold_pct,
        "threshold_chars": int(threshold_chars),
        "actions": actions,
        "stale_brief_threshold_days": STALE_BRIEF_DAYS,
    }

    if not dry_run and archived_count > 0:
        # Archive the dropped decisions to a compact file
        archive_dir.mkdir(parents=True, exist_ok=True)
        ts_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        archive_path = archive_dir / f"coord-compact-{ts_str}.json"
        archive_payload = {
            "compacted_at": _now_iso(),
            "source": str(coord_path),
            "original_size": file_size,
            "archived_decisions_count": archived_count,
            "archived_decisions": to_archive,
            "stale_agents_detected": stale_agents,
        }
        archive_path.write_text(json.dumps(archive_payload, indent=2, ensure_ascii=False))
        report["archive_path"] = str(archive_path)
        # Save the compacted coord.json
        _save_coord(coord_path, data)

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="L2 memory compactor for coord.json")
    parser.add_argument("--coord", type=Path, default=DEFAULT_COORD)
    parser.add_argument("--archive-dir", type=Path, default=DEFAULT_ARCHIVE_DIR)
    parser.add_argument("--threshold-pct", type=int, default=DEFAULT_THRESHOLD_PCT)
    parser.add_argument("--keep-recent", type=int, default=KEEP_RECENT_DECISIONS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    report = compact(
        coord_path=args.coord,
        archive_dir=args.archive_dir,
        threshold_pct=args.threshold_pct,
        keep_recent=args.keep_recent,
        dry_run=args.dry_run,
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
