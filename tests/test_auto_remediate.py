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
    """End-to-end: main() runs both patterns without errors."""
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
    finally:
        sys_mod.argv = orig_argv


if __name__ == "__main__":
    test_fix_stale_cron_skips_when_no_stale()
    test_fix_stale_cron_removes_old_entries()
    test_fix_stale_cron_handles_missing_file()
    test_fix_log_rotation_skips_when_small()
    test_fix_log_rotation_handles_missing()
    test_log_remediation_writes_entry()
    test_main_runs_all_patterns()
    print("\nAll auto-remediate tests passed!")
