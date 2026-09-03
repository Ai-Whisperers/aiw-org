"""Tests for scripts/disable_or_fix_broken_crons.py."""
import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "disable_or_fix_broken_crons.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "disable_or_fix_broken_crons", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _make_jobs_file(tmp_path, jobs):
    f = tmp_path / "jobs.json"
    f.write_text(json.dumps({"jobs": jobs}))
    return f


def test_dry_run_does_not_modify(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-research-associate-daily",
        "enabled": True,
        "last_status": "error",
    }])
    original = fake.read_text()
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=False)
    assert fake.read_text() == original


def test_disables_anthropic_research_cron(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-research-associate-daily",
        "enabled": True,
        "last_status": "error",
        "script": "x.py",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    data = json.loads(fake.read_text())
    j = data["jobs"][0]
    assert j["enabled"] is False
    assert "Anthropic" in j["paused_reason"]
    assert j["paused_at"]


def test_disables_cerebras_saas_lifecycle(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-saas-lifecycle-reconcile",
        "enabled": True,
        "last_status": "error",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    data = json.loads(fake.read_text())
    assert data["jobs"][0]["enabled"] is False
    assert "Cerebras" in data["jobs"][0]["paused_reason"]


def test_disables_bitwarden_sdk_chain(tmp_path, monkeypatch):
    mod = _load_module()
    for name in ["kv-bws-sync", "linkedin-token-refresh", "instagram-token-refresh"]:
        parent = tmp_path / name
        parent.mkdir()
        fake = _make_jobs_file(parent, [{
            "name": name,
            "enabled": True,
            "last_status": "error",
        }])
        monkeypatch.setattr(mod, "CRON_PATHS", [fake])
        mod.patch(apply=True)
        data = json.loads(fake.read_text())
        assert data["jobs"][0]["enabled"] is False, f"{name} should be disabled"
        assert "bitwarden_sdk" in data["jobs"][0]["paused_reason"]


def test_disables_boundary_validate(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-boundary-validate-hourly",
        "enabled": True,
        "last_status": "error",
        "script": "/opt/data/scripts/boundary-validate.py --all",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    data = json.loads(fake.read_text())
    assert data["jobs"][0]["enabled"] is False
    assert "boundary-validate" in data["jobs"][0]["paused_reason"].lower() or "whitespace" in data["jobs"][0]["paused_reason"]


def test_skip_unrelated_jobs(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-something-else",
        "enabled": True,
        "script": "x.py",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    original = fake.read_text()
    mod.patch(apply=True)
    assert fake.read_text() == original


def test_skip_already_disabled(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-research-associate-daily",
        "enabled": False,
        "last_status": "error",
        "paused_reason": "already disabled for X",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    original = fake.read_text()
    mod.patch(apply=True)
    # Should not change paused_reason
    data = json.loads(fake.read_text())
    assert data["jobs"][0]["paused_reason"] == "already disabled for X"


def test_idempotent(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-research-associate-daily",
        "enabled": True,
        "script": "x.py",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    state = fake.read_text()
    mod.patch(apply=True)
    mod.patch(apply=True)
    assert fake.read_text() == state


def test_handles_both_registries(tmp_path, monkeypatch):
    mod = _load_module()
    a_dir = tmp_path / "a"
    b_dir = tmp_path / "b"
    a_dir.mkdir()
    b_dir.mkdir()
    fake_a = _make_jobs_file(a_dir, [{
        "name": "aiw-research-associate-daily",
        "enabled": True,
    }])
    fake_b = _make_jobs_file(b_dir, [{
        "name": "aiw-research-associate-daily",
        "enabled": True,
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_a, fake_b])
    mod.patch(apply=True)
    assert json.loads(fake_a.read_text())["jobs"][0]["enabled"] is False
    assert json.loads(fake_b.read_text())["jobs"][0]["enabled"] is False


def test_all_block_a_jobs_listed(tmp_path, monkeypatch):
    """Block A has 5 crons; ensure all are in JOBS_TO_DISABLE."""
    import importlib
    spec = importlib.util.spec_from_file_location(
        "disable_or_fix_broken_crons", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    expected = {
        "aiw-research-associate-daily",
        "aiw-research-engineer-weekly",
        "aiw-research-tracker-6h",
        "aiw-citation-checker-daily",
        "aiw-publication-coordinator-weekly",
    }
    assert expected.issubset(set(mod.JOBS_TO_DISABLE.keys())), \
        f"missing: {expected - set(mod.JOBS_TO_DISABLE.keys())}"


def test_block_b_and_c_jobs_listed(tmp_path, monkeypatch):
    """Block B (1) and Block C (4) should also be in JOBS_TO_DISABLE."""
    import importlib
    spec = importlib.util.spec_from_file_location(
        "disable_or_fix_broken_crons", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    expected = {
        "aiw-saas-lifecycle-reconcile",
        "kv-bws-sync",
        "linkedin-token-refresh",
        "instagram-token-refresh",
        "aiw-boundary-validate-hourly",
    }
    assert expected.issubset(set(mod.JOBS_TO_DISABLE.keys())), \
        f"missing: {expected - set(mod.JOBS_TO_DISABLE.keys())}"
