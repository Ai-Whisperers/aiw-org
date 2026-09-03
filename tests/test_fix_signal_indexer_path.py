"""Tests for scripts/fix_signal_indexer_path.py.

Verifies the dry-run / apply / idempotency contract.
"""
import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "fix_signal_indexer_path.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "fix_signal_indexer_path", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_dry_run_does_not_modify(tmp_path, monkeypatch):
    mod = _load_module()
    fake_old = tmp_path / "build-signal-index.sh"
    fake_old.write_text("#!/usr/bin/env bash\necho fake\n")
    fake_old.chmod(0o755)
    fake_new = tmp_path / "new-signal-index.sh"
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-signal-indexer", "script": str(fake_old)}]}))
    monkeypatch.setattr(mod, "OLD_SCRIPT", fake_old)
    monkeypatch.setattr(mod, "NEW_SCRIPT", fake_new)
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    mod.patch(apply=False)
    assert fake_old.exists() and not fake_old.is_symlink()
    assert not fake_new.exists()
    cron = json.loads(fake_cron.read_text())
    assert cron["jobs"][0]["script"] == str(fake_old)


def test_apply_copies_and_links(tmp_path, monkeypatch):
    mod = _load_module()
    fake_old = tmp_path / "build-signal-index.sh"
    fake_old.write_text("#!/usr/bin/env bash\necho fake\n")
    fake_old.chmod(0o755)
    fake_new = tmp_path / "new-signal-index.sh"
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-signal-indexer", "script": str(fake_old)}]}))
    monkeypatch.setattr(mod, "OLD_SCRIPT", fake_old)
    monkeypatch.setattr(mod, "NEW_SCRIPT", fake_new)
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    mod.patch(apply=True)
    assert fake_new.exists()
    assert fake_new.read_text() == "#!/usr/bin/env bash\necho fake\n"
    assert fake_new.stat().st_mode & 0o100
    assert fake_old.is_symlink()
    backup = fake_old.with_suffix(fake_old.suffix + ".real")
    assert backup.exists()
    cron = json.loads(fake_cron.read_text())
    assert cron["jobs"][0]["script"] == str(fake_new)


def test_idempotent(tmp_path, monkeypatch):
    mod = _load_module()
    fake_old = tmp_path / "build-signal-index.sh"
    fake_old.write_text("#!/usr/bin/env bash\necho fake\n")
    fake_old.chmod(0o755)
    fake_new = tmp_path / "new-signal-index.sh"
    fake_cron = tmp_path / "jobs.json"
    fake_cron.write_text(json.dumps({"jobs": [{"name": "aiw-signal-indexer", "script": str(fake_old)}]}))
    monkeypatch.setattr(mod, "OLD_SCRIPT", fake_old)
    monkeypatch.setattr(mod, "NEW_SCRIPT", fake_new)
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_cron])
    mod.patch(apply=True)
    state = json.loads(fake_cron.read_text())
    rc1 = mod.patch(apply=True)
    rc2 = mod.patch(apply=True)
    assert rc1 == 0
    assert rc2 == 0
    assert json.loads(fake_cron.read_text()) == state
