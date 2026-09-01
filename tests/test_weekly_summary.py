"""Tests for cron/weekly_summary.py — Phase 4.2 weekly summary generator."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timezone, timedelta

SCRIPT = Path(__file__).parent.parent / "scripts" / "cron" / "weekly_summary.py"


def load_module():
    spec = importlib.util.spec_from_file_location("weekly_summary", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["weekly_summary"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_iso_week_format():
    mod = load_module()
    now = datetime(2026, 9, 1, tzinfo=timezone.utc)  # Tuesday
    assert mod._iso_week(now) == "2026-W36"


def test_iso_week_year_boundary():
    mod = load_module()
    # Jan 4, 2024 is in ISO week 1 of 2024
    assert mod._iso_week(datetime(2024, 1, 4, tzinfo=timezone.utc)) == "2024-W01"


def test_read_jsonl_missing_file():
    mod = load_module()
    assert mod._read_jsonl(Path("/nonexistent")) == []


def test_read_jsonl_skips_malformed():
    mod = load_module()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write('{"a": 1}\n')
        f.write('not json\n')
        f.write('{"b": 2}\n')
        path = Path(f.name)
    try:
        result = mod._read_jsonl(path)
        assert len(result) == 2
        assert result[0] == {"a": 1}
        assert result[1] == {"b": 2}
    finally:
        path.unlink()


def test_read_json_missing_file():
    mod = load_module()
    assert mod._read_json(Path("/nonexistent")) == {}


def test_generate_summary_dry_run():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        traces = Path(tmpdir) / "traces.jsonl"
        coord = Path(tmpdir) / "coord.json"
        routing = Path(tmpdir) / "routing.jsonl"
        outbox = Path(tmpdir) / "outbox"
        snapshots = Path(tmpdir) / "snapshots"

        traces.write_text(
            json.dumps({"ts": "2026-09-01T10:00:00Z", "agent": "alpha"}) + "\n" +
            json.dumps({"ts": "2026-09-01T11:00:00Z", "agent": "beta"}) + "\n"
        )
        coord.write_text(json.dumps({
            "decisions_for_ivan": [
                {"raised_at": "2026-09-01T10:00:00Z", "question": "Q1"},
            ],
            "commitments": [
                {"id": "c-1", "text": "send", "signal_id": "s1",
                 "detected_at": "2026-09-01", "type": "promise"},
            ],
        }))
        routing.write_text(
            json.dumps({"ts": "2026-09-01T10:00:00Z", "rule_id": "r1",
                        "result": "routed", "latency_ms": 10, "degraded": False}) + "\n"
        )

        report = mod.generate_summary("2026-W36", traces, coord, routing,
                                    outbox, snapshots, dry_run=True)
        assert report["week"] == "2026-W36"
        assert report["stats"]["traces"] == 2
        assert report["stats"]["routing"] == 1
        assert report["stats"]["decisions"] == 1
        assert report["stats"]["commitments"] == 1
        assert report["dry_run"] is True
        assert report["out_path"] is None  # no outbox write in dry-run
        # Verify outbox was NOT created
        assert not outbox.exists()


def test_generate_summary_writes_outbox_and_snapshot():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        traces = Path(tmpdir) / "traces.jsonl"
        coord = Path(tmpdir) / "coord.json"
        routing = Path(tmpdir) / "routing.jsonl"
        outbox = Path(tmpdir) / "outbox"
        snapshots = Path(tmpdir) / "snapshots"

        traces.write_text(json.dumps({
            "ts": "2026-09-01T10:00:00Z", "agent": "alpha"
        }) + "\n")
        coord.write_text(json.dumps({"decisions_for_ivan": [], "commitments": []}))
        routing.write_text(json.dumps({
            "ts": "2026-09-01T10:00:00Z", "rule_id": "r1",
            "result": "routed", "latency_ms": 5, "degraded": False
        }) + "\n")

        report = mod.generate_summary("2026-W36", traces, coord, routing,
                                    outbox, snapshots, dry_run=False)
        assert (outbox / "weekly-2026-W36.md").exists()
        content = (outbox / "weekly-2026-W36.md").read_text()
        assert "Weekly Summary" in content
        assert "2026-W36" in content
        assert "alpha" in content  # agent name
        # Snapshot created
        assert (snapshots / "2026-W36").is_dir()


def test_generate_summary_filters_by_week():
    """Items outside the target week should not be counted."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        traces = Path(tmpdir) / "traces.jsonl"
        coord = Path(tmpdir) / "coord.json"
        routing = Path(tmpdir) / "routing.jsonl"
        outbox = Path(tmpdir) / "outbox"
        snapshots = Path(tmpdir) / "snapshots"

        # 2026-W36 = Aug 31 (Mon) to Sep 6 (Sun)
        # 2026-W35 = Aug 24 to Aug 30
        traces.write_text(
            json.dumps({"ts": "2026-09-01T10:00:00Z", "agent": "in_w36"}) + "\n" +  # in W36
            json.dumps({"ts": "2026-08-25T10:00:00Z", "agent": "in_w35"}) + "\n"    # in W35
        )
        coord.write_text(json.dumps({"decisions_for_ivan": [], "commitments": []}))
        routing.write_text(
            json.dumps({"ts": "2026-09-01T10:00:00Z", "rule_id": "r1",
                        "result": "routed", "latency_ms": 5, "degraded": False}) + "\n"
        )

        report = mod.generate_summary("2026-W36", traces, coord, routing,
                                    outbox, snapshots, dry_run=True)
        assert report["stats"]["traces"] == 1  # only the W36 trace
        agent_names = [a[0] for a in report["top_agents"]]
        assert "in_w36" in agent_names
        assert "in_w35" not in agent_names


def test_generate_summary_calculates_degraded_rate():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        traces = Path(tmpdir) / "traces.jsonl"
        coord = Path(tmpdir) / "coord.json"
        routing = Path(tmpdir) / "routing.jsonl"
        outbox = Path(tmpdir) / "outbox"
        snapshots = Path(tmpdir) / "snapshots"
        traces.write_text("")
        coord.write_text(json.dumps({"decisions_for_ivan": [], "commitments": []}))
        routing.write_text(
            json.dumps({"ts": "2026-09-01T10:00:00Z", "rule_id": "r1",
                        "result": "routed", "latency_ms": 5, "degraded": True}) + "\n" +
            json.dumps({"ts": "2026-09-01T10:00:00Z", "rule_id": "r2",
                        "result": "routed", "latency_ms": 10, "degraded": False}) + "\n" +
            json.dumps({"ts": "2026-09-01T10:00:00Z", "rule_id": "r3",
                        "result": "no_rule", "latency_ms": 1, "degraded": False}) + "\n"
        )
        report = mod.generate_summary("2026-W36", traces, coord, routing,
                                    outbox, snapshots, dry_run=True)
        assert report["no_rule_count"] == 1
        assert report["degraded_count"] == 1
        # avg latency = (5+10+1)/3 = 5.33...
        assert 5.0 <= report["avg_latency_ms"] <= 6.0


def test_generate_summary_top_decisions():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        traces = Path(tmpdir) / "traces.jsonl"
        coord = Path(tmpdir) / "coord.json"
        routing = Path(tmpdir) / "routing.jsonl"
        outbox = Path(tmpdir) / "outbox"
        snapshots = Path(tmpdir) / "snapshots"
        traces.write_text("")
        coord.write_text(json.dumps({
            "decisions_for_ivan": [
                {"raised_at": "2026-09-01T10:00:00Z",
                 "question": "X" * 200, "context": "y"},
            ],
            "commitments": [],
        }))
        routing.write_text("")

        report = mod.generate_summary("2026-W36", traces, coord, routing,
                                    outbox, snapshots, dry_run=False)
        out_md = (outbox / "weekly-2026-W36.md").read_text()
        # Should truncate long questions to 120 chars + "..."
        assert "X" * 120 + "..." in out_md
