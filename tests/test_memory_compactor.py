"""Tests for memory/compactor.py — L2 memory compactor.

Per AIW upgrade plan Phase 1.2: token-threshold-based compaction with archive.
"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

# Module path
SCRIPT = Path(__file__).parent.parent / "scripts" / "memory" / "compactor.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compactor", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["compactor"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_threshold_constants():
    mod = load_module()
    assert mod.DEFAULT_THRESHOLD_PCT == 80
    assert mod.DEFAULT_CONTEXT_CHARS == 200_000 * 4
    assert mod.KEEP_RECENT_DECISIONS == 50
    assert mod.STALE_BRIEF_DAYS == 30


def test_compact_dry_run_creates_no_archive():
    """Dry run must NOT modify coord.json or create archive."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        coord = Path(tmpdir) / "coord.json"
        archive = Path(tmpdir) / "archive"
        # Make a coord.json with 100 decisions
        data = {
            "_last_modified_by": "test",
            "decisions_for_ivan": [{"i": i, "context": "x" * 200} for i in range(100)],
            "agents": {},
        }
        coord.write_text(json.dumps(data))
        before_size = coord.stat().st_size

        report = mod.compact(coord_path=coord, archive_dir=archive,
                            threshold_pct=80, keep_recent=10, dry_run=True)
        assert report["dry_run"] is True
        assert report["compacted"] is False
        assert coord.stat().st_size == before_size, "dry-run should not modify file"
        if archive.exists():
            assert not any(archive.iterdir()), "dry-run should not create archive"
        assert report["savings_bytes"] == 0  # dry run reports hypothetical savings


def test_compact_archives_old_decisions():
    """Compact mode should archive old decisions and keep recent ones."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        coord = Path(tmpdir) / "coord.json"
        archive = Path(tmpdir) / "archive"
        data = {
            "_last_modified_by": "test",
            "decisions_for_ivan": [{"i": i} for i in range(100)],
            "agents": {},
        }
        coord.write_text(json.dumps(data))

        report = mod.compact(coord_path=coord, archive_dir=archive,
                            threshold_pct=80, keep_recent=10, dry_run=False)
        assert report["compacted"] is True
        assert report["savings_bytes"] > 0
        assert any("archived" in a and a["archived"] == 90 for a in report["actions"])

        # Verify coord.json now has only 10 decisions
        new_data = json.loads(coord.read_text())
        assert len(new_data["decisions_for_ivan"]) == 10

        # Verify archive file exists
        assert archive.exists()
        archive_files = list(archive.glob("coord-compact-*.json"))
        assert len(archive_files) == 1
        archive_data = json.loads(archive_files[0].read_text())
        assert archive_data["archived_decisions_count"] == 90
        assert len(archive_data["archived_decisions"]) == 90


def test_compact_no_op_when_under_keep_recent():
    """If decisions count <= keep_recent, should be a no-op."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        coord = Path(tmpdir) / "coord.json"
        archive = Path(tmpdir) / "archive"
        data = {
            "_last_modified_by": "test",
            "decisions_for_ivan": [{"i": i} for i in range(5)],  # < keep_recent
            "agents": {},
        }
        coord.write_text(json.dumps(data))

        report = mod.compact(coord_path=coord, archive_dir=archive,
                            threshold_pct=80, keep_recent=10, dry_run=False)
        assert report["compacted"] is True
        assert report["savings_bytes"] == 0
        new_data = json.loads(coord.read_text())
        assert len(new_data["decisions_for_ivan"]) == 5


def test_compact_detects_stale_agents():
    """Stale agents (latest_brief file > 30d old or missing) should be flagged."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        coord = Path(tmpdir) / "coord.json"
        archive = Path(tmpdir) / "archive"
        # Create an agent whose latest_brief points to a non-existent file
        data = {
            "_last_modified_by": "test",
            "decisions_for_ivan": [],
            "agents": {
                "fresh-agent": {"latest_brief": str(Path(tmpdir) / "fresh.md")},
                "stale-agent": {"latest_brief": str(Path(tmpdir) / "stale.md")},
            },
        }
        coord.write_text(json.dumps(data))
        # Create fresh.md (recent), don't create stale.md
        (Path(tmpdir) / "fresh.md").write_text("fresh")

        report = mod.compact(coord_path=coord, archive_dir=archive,
                            threshold_pct=80, keep_recent=10, dry_run=True)
        # Find stale_agents_detected action
        stale_action = next(a for a in report["actions"] if a["type"] == "stale_agents_detected")
        assert stale_action["count"] >= 1
        assert "stale-agent" in stale_action["agents"]


def test_compact_preserves_header():
    """The _last_modified_by header must be preserved (audit trail)."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        coord = Path(tmpdir) / "coord.json"
        archive = Path(tmpdir) / "archive"
        data = {
            "_last_modified_by": "important-monitor",
            "_last_modified": "2026-09-01T00:00:00+00:00",
            "decisions_for_ivan": [{"i": i} for i in range(100)],
            "agents": {},
        }
        coord.write_text(json.dumps(data))

        mod.compact(coord_path=coord, archive_dir=archive,
                    threshold_pct=80, keep_recent=10, dry_run=False)
        new_data = json.loads(coord.read_text())
        assert new_data["_last_modified_by"] == "important-monitor"
        assert new_data["_last_modified"] == "2026-09-01T00:00:00+00:00"


def test_compact_over_threshold_detection():
    """Over-threshold flag should be correct based on file size."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        coord = Path(tmpdir) / "coord.json"
        archive = Path(tmpdir) / "archive"
        # Create a large coord.json (over 80% of 200k context = 640k chars)
        data = {
            "decisions_for_ivan": [{"i": i, "context": "x" * 7000} for i in range(100)],  # ~700k chars
        }
        coord.write_text(json.dumps(data))
        report = mod.compact(coord_path=coord, archive_dir=archive,
                            threshold_pct=80, keep_recent=10, dry_run=True)
        assert report["over_threshold"] is True
        assert report["original_chars"] > report["threshold_chars"]


def test_compact_archive_filename_pattern():
    """Archive file should be named coord-compact-YYYYMMDDTHHMMSSZ.json."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        coord = Path(tmpdir) / "coord.json"
        archive = Path(tmpdir) / "archive"
        data = {
            "decisions_for_ivan": [{"i": i} for i in range(100)],
            "agents": {},
        }
        coord.write_text(json.dumps(data))

        mod.compact(coord_path=coord, archive_dir=archive,
                    threshold_pct=80, keep_recent=10, dry_run=False)
        archive_files = list(archive.glob("coord-compact-*.json"))
        assert len(archive_files) == 1
        # Filename should match coord-compact-YYYYMMDDTHHMMSSZ.json
        name = archive_files[0].name
        assert name.startswith("coord-compact-")
        assert name.endswith(".json")
        # 8 digits date + T + 6 digits time + Z
        ts_part = name[len("coord-compact-"):-len(".json")]
        assert len(ts_part) == 16  # YYYYMMDDTHHMMSSZ
        assert ts_part[8] == "T"
        assert ts_part[-1] == "Z"


def test_compact_handles_missing_coord():
    """If coord.json doesn't exist, should return error gracefully."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        coord = Path(tmpdir) / "nonexistent.json"
        archive = Path(tmpdir) / "archive"
        report = mod.compact(coord_path=coord, archive_dir=archive,
                            threshold_pct=80, keep_recent=10, dry_run=False)
        assert "error" in report
        assert report["compacted"] is False
