"""Tests for scripts/fix_security_watchdog_path.py.

Verifies the dry-run / apply / idempotency contract.
"""
import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "fix_security_watchdog_path.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "fix_security_watchdog_path", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _make_jobs_file(tmp_path, jobs):
    f = tmp_path / "jobs.json"
    f.write_text(json.dumps({"jobs": jobs}))
    return f


def test_dry_run_does_not_modify(tmp_path):
    mod = _load_module()
    f = _make_jobs_file(tmp_path, [{
        "name": "aiw-security-watchdog-30min",
        "prompt": "Read /opt/data/agents/04-engineering/security-watchdog-30min/PROMPT.md. "
                  "Write to /opt/data/agents/security-watchdog-30min/outbox/YYYY-MM-DD.md.",
        "enabled": True,
    }])
    original = f.read_text()
    original_paths = mod.CRON_PATHS
    mod.CRON_PATHS = [f]
    try:
        mod.patch(apply=False)
    finally:
        mod.CRON_PATHS = original_paths
    assert f.read_text() == original


def test_apply_replaces_outbox_path(tmp_path):
    mod = _load_module()
    f = _make_jobs_file(tmp_path, [{
        "name": "aiw-security-watchdog-30min",
        "prompt": "Read /opt/data/agents/04-engineering/security-watchdog-30min/PROMPT.md. "
                  "Write to /opt/data/agents/security-watchdog-30min/outbox/YYYY-MM-DD.md.",
        "enabled": True,
    }])
    original_paths = mod.CRON_PATHS
    mod.CRON_PATHS = [f]
    try:
        mod.patch(apply=True)
    finally:
        mod.CRON_PATHS = original_paths
    data = json.loads(f.read_text())
    prompt = data["jobs"][0]["prompt"]
    assert "/opt/data/agents/04-engineering/security-watchdog-30min/outbox/" in prompt
    assert "/opt/data/agents/security-watchdog-30min/outbox/" not in prompt.replace(
        "/opt/data/agents/04-engineering/security-watchdog-30min/outbox/", ""
    )


def test_idempotent_when_already_correct(tmp_path):
    mod = _load_module()
    f = _make_jobs_file(tmp_path, [{
        "name": "aiw-security-watchdog-30min",
        "prompt": "Read /opt/data/agents/04-engineering/security-watchdog-30min/PROMPT.md. "
                  "Write to /opt/data/agents/04-engineering/security-watchdog-30min/outbox/YYYY-MM-DD.md.",
        "enabled": True,
    }])
    original = f.read_text()
    original_paths = mod.CRON_PATHS
    mod.CRON_PATHS = [f]
    try:
        rc1 = mod.patch(apply=True)
        rc2 = mod.patch(apply=True)
    finally:
        mod.CRON_PATHS = original_paths
    assert rc1 == 0
    assert rc2 == 0
    assert f.read_text() == original


def test_skips_unrelated_jobs(tmp_path):
    mod = _load_module()
    f = _make_jobs_file(tmp_path, [
        {
            "name": "aiw-something-else",
            "prompt": "Read /opt/data/agents/security-watchdog-30min/PROMPT.md for the role.",
        },
        {
            "name": "aiw-security-watchdog-30min",
            "prompt": "Write to /opt/data/agents/security-watchdog-30min/outbox/YYYY-MM-DD.md.",
        },
    ])
    original_paths = mod.CRON_PATHS
    mod.CRON_PATHS = [f]
    try:
        mod.patch(apply=True)
    finally:
        mod.CRON_PATHS = original_paths
    data = json.loads(f.read_text())
    # unrelated job untouched
    assert data["jobs"][0]["prompt"] == "Read /opt/data/agents/security-watchdog-30min/PROMPT.md for the role."
    # target job patched
    assert "/opt/data/agents/04-engineering/security-watchdog-30min/outbox/" in data["jobs"][1]["prompt"]
