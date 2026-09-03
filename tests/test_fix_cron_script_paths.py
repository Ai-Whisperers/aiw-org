"""Tests for scripts/fix_cron_script_paths.py."""
import importlib.util
import json
from pathlib import Path
import pytest

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "fix_cron_script_paths.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "fix_cron_script_paths", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_dry_run_does_not_modify(tmp_path, monkeypatch):
    mod = _load_module()
    fake_old = tmp_path / "test-script.py"
    fake_old.write_text("#!/usr/bin/env python3\nprint('x')\n")
    fake_old.chmod(0o755)
    fake_new = tmp_path / "scripts" / "test-script.py"
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-test", "enabled": True, "script": str(fake_old), "last_error": "Blocked: script path resolves outside the scripts directory", "last_status": "error"}]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    monkeypatch.setattr(mod, "CANONICAL_SCRIPTS_DIR", fake_new.parent)
    original = fake_cron.read_text()
    mod.patch(apply=False)
    assert fake_cron.read_text() == original
    assert not fake_new.exists()
    assert fake_old.exists() and not fake_old.is_symlink()


def test_apply_copies_links_and_updates(tmp_path, monkeypatch):
    mod = _load_module()
    fake_old = tmp_path / "test-script.py"
    fake_old.write_text("#!/usr/bin/env python3\nprint('x')\n")
    fake_old.chmod(0o755)
    fake_new = tmp_path / "scripts" / "test-script.py"
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-test", "enabled": True, "script": str(fake_old), "last_error": "Blocked: script path resolves outside the scripts directory", "last_status": "error"}]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    monkeypatch.setattr(mod, "CANONICAL_SCRIPTS_DIR", fake_new.parent)
    mod.patch(apply=True)
    assert fake_new.exists()
    assert fake_new.read_text() == "#!/usr/bin/env python3\nprint('x')\n"
    assert fake_new.stat().st_mode & 0o100
    assert fake_old.is_symlink()
    backup = fake_old.with_suffix(fake_old.suffix + ".real")
    assert backup.exists()
    data = json.loads(fake_cron.read_text())
    assert data["jobs"][0]["script"] == str(fake_new)


def test_preserves_arguments(tmp_path, monkeypatch):
    mod = _load_module()
    fake_old = tmp_path / "build-pipeline.py"
    fake_old.write_text("#!/usr/bin/env python3\n")
    fake_old.chmod(0o755)
    fake_new = tmp_path / "scripts" / "build-pipeline.py"
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-build", "enabled": True, "script": str(fake_old) + " list-rules", "last_error": "Blocked: script path resolves outside the scripts directory", "last_status": "error"}]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    monkeypatch.setattr(mod, "CANONICAL_SCRIPTS_DIR", fake_new.parent)
    mod.patch(apply=True)
    data = json.loads(fake_cron.read_text())
    assert data["jobs"][0]["script"] == str(fake_new) + " list-rules"


def test_skips_already_canonical(tmp_path, monkeypatch):
    mod = _load_module()
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-test", "enabled": True, "script": "/opt/data/scripts/already-canonical.py", "last_error": "Blocked: script path resolves outside the scripts directory", "last_status": "error"}]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    monkeypatch.setattr(mod, "CANONICAL_SCRIPTS_DIR", tmp_path / "scripts")
    original = fake_cron.read_text()
    mod.patch(apply=True)
    assert fake_cron.read_text() == original


def test_skips_when_source_missing(tmp_path, monkeypatch):
    mod = _load_module()
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-test", "enabled": True, "script": "/opt/data/nonexistent/script.py", "last_error": "Blocked: script path resolves outside the scripts directory", "last_status": "error"}]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    monkeypatch.setattr(mod, "CANONICAL_SCRIPTS_DIR", tmp_path / "scripts")
    original = fake_cron.read_text()
    mod.patch(apply=True)
    assert fake_cron.read_text() == original


def test_skips_disabled_jobs(tmp_path, monkeypatch):
    mod = _load_module()
    fake_old = tmp_path / "disabled.py"
    fake_old.write_text("#!/usr/bin/env python3\n")
    fake_old.chmod(0o755)
    fake_new = tmp_path / "scripts" / "disabled.py"
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-test", "enabled": False, "script": str(fake_old), "last_error": "Blocked: script path resolves outside the scripts directory", "last_status": "error"}]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    monkeypatch.setattr(mod, "CANONICAL_SCRIPTS_DIR", fake_new.parent)
    mod.patch(apply=True)
    assert fake_old.exists() and not fake_old.is_symlink()
    assert not fake_new.exists()


def test_idempotent(tmp_path, monkeypatch):
    mod = _load_module()
    fake_old = tmp_path / "test.py"
    fake_old.write_text("#!/usr/bin/env python3\n")
    fake_old.chmod(0o755)
    fake_new = tmp_path / "scripts" / "test.py"
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-test", "enabled": True, "script": str(fake_old), "last_error": "Blocked: script path resolves outside the scripts directory", "last_status": "error"}]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    monkeypatch.setattr(mod, "CANONICAL_SCRIPTS_DIR", fake_new.parent)
    mod.patch(apply=True)
    state = fake_cron.read_text()
    mod.patch(apply=True)
    mod.patch(apply=True)
    assert fake_cron.read_text() == state


def test_skips_unrelated_errors(tmp_path, monkeypatch):
    mod = _load_module()
    fake_old = tmp_path / "unrelated.py"
    fake_old.write_text("#!/usr/bin/env python3\n")
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-test", "enabled": True, "script": str(fake_old), "last_error": "Script exited with code 1", "last_status": "error"}]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    monkeypatch.setattr(mod, "CANONICAL_SCRIPTS_DIR", tmp_path / "scripts")
    original = fake_cron.read_text()
    mod.patch(apply=True)
    assert fake_cron.read_text() == original
