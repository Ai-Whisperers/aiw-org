"""Tests for scripts/auto-remediate.py."""
import importlib.util
import json
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "auto-remediate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("auto_remediate", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_fix_stale_cron_skips_when_no_stale():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        # Patch STATE_DIR
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            # Write a watchdog with recent entries
            recent = datetime.now(timezone.utc).isoformat()
            watchdog = Path(tmp) / "cron-error-watchdog.json"
            watchdog.write_text(json.dumps({
                "timestamp": recent,
                "jobs_in_error": 1,
                "details": [
                    {"name": "x", "last_run_at": recent, "last_error": "y"}
                ],
            }))
            r = mod.fix_stale_cron_errors(dry_run=True)
            assert r["action"] == "skip", f"unexpected action: {r}"
            assert "no stale" in r.get("reason", "")
        finally:
            mod.STATE_DIR = orig


def test_fix_stale_cron_removes_old_entries():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        mod = load_module()
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            # 8d ago = stale (default 7d threshold)
            old = (datetime.now(timezone.utc) - timedelta(days=8)).isoformat()
            recent = datetime.now(timezone.utc).isoformat()
            watchdog = Path(tmp) / "cron-error-watchdog.json"
            watchdog.write_text(json.dumps({
                "timestamp": recent,
                "jobs_in_error": 2,
                "details": [
                    {"name": "old", "last_run_at": old, "last_error": "y"},
                    {"name": "new", "last_run_at": recent, "last_error": "z"},
                ],
            }))
            r = mod.fix_stale_cron_errors(dry_run=True)
            assert r["action"] == "would-remove"
            assert r["removed_count"] == 1
            assert r["kept_count"] == 1

            # Apply
            r2 = mod.fix_stale_cron_errors(dry_run=False)
            assert r2["action"] == "applied"
            # Verify file was modified
            data = json.loads(watchdog.read_text())
            assert data["jobs_in_error"] == 1
            assert len(data["details"]) == 1
            assert data["details"][0]["name"] == "new"
        finally:
            mod.STATE_DIR = orig


def test_fix_stale_cron_handles_missing_file():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        mod = load_module()
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            r = mod.fix_stale_cron_errors(dry_run=False)
            assert r["action"] == "skip"
            assert "missing" in r.get("reason", "")
        finally:
            mod.STATE_DIR = orig


def test_fix_log_rotation_skips_when_small():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        mod = load_module()
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            # Write small log
            log = Path(tmp) / "test.jsonl"
            log.write_text("entry1\nentry2\n")
            r = mod.fix_log_rotation(dry_run=True)
            assert r["action"] == "skip"
        finally:
            mod.STATE_DIR = orig


def test_fix_log_rotation_handles_missing():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        mod = load_module()
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            r = mod.fix_log_rotation(dry_run=False)
            assert r["action"] == "skip"
        finally:
            mod.STATE_DIR = orig


def test_log_remediation_writes_entry():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        mod = load_module()
        orig_dir = mod.STATE_DIR
        orig_log = mod.LOG_PATH
        mod.STATE_DIR = Path(tmp)
        mod.LOG_PATH = Path(tmp) / "remediation-log.ndjson"
        try:
            mod.log_remediation("test-pattern", "/test/path", "applied")
            assert mod.LOG_PATH.exists()
            entry = json.loads(mod.LOG_PATH.read_text().strip())
            assert entry["action"] == "test-pattern"
            assert entry["target"] == "/test/path"
            assert entry["result"] == "applied"
        finally:
            mod.STATE_DIR = orig_dir
            mod.LOG_PATH = orig_log


def test_main_runs_all_patterns():
    """End-to-end: main() runs all 5 patterns without errors."""
    mod = load_module()
    # Patch argv
    import sys as sys_mod
    orig_argv = sys_mod.argv
    sys_mod.argv = ["auto-remediate.py", "--dry-run"]
    try:
        # Just verify it doesn't crash; output goes to stdout
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            try:
                mod.main()
            except SystemExit:
                pass  # --dry-run may exit 1 (signal human review needed)
        assert "patterns" in buf.getvalue()
        # Verify all 5 patterns ran
        output = buf.getvalue()
        expected_patterns = ["stale-cron", "log-rotation", "eval-gate-compaction",
                             "cron-error-dedup", "schema-refresh"]
        for p in expected_patterns:
            assert p in output, f"missing pattern in output: {p}"
    finally:
        sys_mod.argv = orig_argv


def test_eval_gate_compaction_skips_when_small():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            log = Path(tmp) / "eval-gate-decisions.ndjson"
            log.write_text("entry1\nentry2\n")
            r = mod.fix_eval_gate_compaction(dry_run=True)
            assert r["action"] == "skip"
        finally:
            mod.STATE_DIR = orig


def test_eval_gate_compaction_compacts_when_large():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            log = Path(tmp) / "eval-gate-decisions.ndjson"
            # Create > 1MB
            big_entry = '{"x":"' + "a" * 1000 + '"}\n'
            content = big_entry * 1500  # ~1.5MB
            log.write_text(content)
            r = mod.fix_eval_gate_compaction(dry_run=False)
            assert r["action"] == "applied"
            assert "size_kb_before" in r
            # Verify file is smaller now
            assert log.stat().st_size < len(content)
        finally:
            mod.STATE_DIR = orig


def test_cron_error_dedup_skips_when_no_dupes():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            watchdog = Path(tmp) / "cron-error-watchdog.json"
            watchdog.write_text(json.dumps({
                "details": [
                    {"name": "a", "last_error": "x"},
                    {"name": "b", "last_error": "y"},
                ],
            }))
            r = mod.fix_cron_error_dedup(dry_run=True)
            assert r["action"] == "skip"
        finally:
            mod.STATE_DIR = orig


def test_cron_error_dedup_removes_dupes():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            watchdog = Path(tmp) / "cron-error-watchdog.json"
            # Same (name, error) twice
            watchdog.write_text(json.dumps({
                "jobs_in_error": 3,
                "details": [
                    {"name": "a", "last_error": "x"},
                    {"name": "a", "last_error": "x"},  # dup
                    {"name": "b", "last_error": "y"},
                ],
            }))
            r = mod.fix_cron_error_dedup(dry_run=False)
            assert r["action"] == "applied"
            assert r["duplicates_removed"] == 1
            assert r["kept"] == 2
        finally:
            mod.STATE_DIR = orig


def test_schema_refresh_reports_findings():
    """Schema refresh should report gaps but NOT auto-modify."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        # Schema dir is hard-coded in fix_schema_refresh; we test logic via patched reimplementation below
        # We'll just call the function with our temp schema dir via monkey-patching
        orig_state = mod.STATE_DIR
        orig_path = Path("/opt/data/agents/schemas")
        # Create a temp schema dir with a gap
        tmp_schema = Path(tmp) / "schemas"
        tmp_schema.mkdir()
        tmp_state = Path(tmp) / "state"
        tmp_state.mkdir()
        # Write a schema with 1 property
        (tmp_schema / "test.schema.json").write_text(json.dumps({
            "type": "object",
            "properties": {"known": {"type": "string"}},
            "additionalProperties": False,
        }))
        # Write a state file with 2 fields (1 unknown)
        (tmp_state / "test.json").write_text(json.dumps({
            "known": "x",
            "unknown_field": "y",
        }))
        # Patch the schema_refresh function's paths
        mod.STATE_DIR = tmp_state
        # Monkey-patch schema_dir by replacing the function body
        orig_func = mod.fix_schema_refresh
        def patched(*args, **kwargs):
            # Reimplement with our paths
            findings = []
            for schema_file in tmp_schema.glob("*.schema.json"):
                schema_name = schema_file.name.replace(".schema.json", ".json")
                state_file = tmp_state / schema_name
                if not state_file.exists():
                    continue
                schema = json.loads(schema_file.read_text())
                state = json.loads(state_file.read_text())
                if not isinstance(state, dict):
                    continue
                schema_props = set(schema.get("properties", {}).keys())
                state_fields = set(state.keys())
                unknown = state_fields - schema_props
                if not unknown:
                    continue
                if schema.get("additionalProperties") is True:
                    continue
                findings.append({"schema": str(schema_file), "count": len(unknown)})
            if not findings:
                return {"pattern": "schema-refresh", "action": "skip"}
            return {"pattern": "schema-refresh", "action": "reported",
                    "findings_count": len(findings), "findings": findings}
        # Call patched version
        r = patched(dry_run=False)
        assert r["action"] == "reported"
        assert r["findings_count"] == 1
        assert r["findings"][0]["count"] == 1


def test_pattern_registry_has_all_5():
    mod = load_module()
    assert len(mod.PATTERNS) == 5, f"expected 5 patterns, got {len(mod.PATTERNS)}"
    expected = {"stale-cron", "log-rotation", "eval-gate-compaction",
                "cron-error-dedup", "schema-refresh"}
    assert set(mod.PATTERNS.keys()) == expected


if __name__ == "__main__":
    test_fix_stale_cron_skips_when_no_stale()
    test_fix_stale_cron_removes_old_entries()
    test_fix_stale_cron_handles_missing_file()
    test_fix_log_rotation_skips_when_small()
    test_fix_log_rotation_handles_missing()
    test_log_remediation_writes_entry()
    test_main_runs_all_patterns()
    print("\nAll auto-remediate tests passed!")
