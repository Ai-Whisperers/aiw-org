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


def _assert_disabled(j, reason_substr):
    assert j["enabled"] is False
    assert reason_substr in j["paused_reason"]
    assert j["paused_at"]


def test_dry_run_does_not_modify(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-research-associate-daily", "enabled": True,
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=False)
    assert json.loads(fake.read_text())["jobs"][0]["enabled"] is True


def test_disables_anthropic_research_cron(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-research-associate-daily", "enabled": True,
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    _assert_disabled(json.loads(fake.read_text())["jobs"][0], "Anthropic")


def test_disables_cerebras_saas_lifecycle(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-saas-lifecycle-reconcile", "enabled": True,
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    _assert_disabled(json.loads(fake.read_text())["jobs"][0], "Cerebras")


def test_disables_bitwarden_sdk_chain(tmp_path, monkeypatch):
    mod = _load_module()
    for name in ["kv-bws-sync", "linkedin-token-refresh", "instagram-token-refresh"]:
        parent = tmp_path / name
        parent.mkdir()
        fake = _make_jobs_file(parent, [{
            "name": name, "enabled": True,
        }])
        monkeypatch.setattr(mod, "CRON_PATHS", [fake])
        mod.patch(apply=True)
        _assert_disabled(json.loads(fake.read_text())["jobs"][0], "bitwarden_sdk")


def test_disables_boundary_validate(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-boundary-validate-hourly",
        "enabled": True,
        "script": "/opt/data/scripts/boundary-validate.py --all",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    j = json.loads(fake.read_text())["jobs"][0]
    assert j["enabled"] is False
    assert "boundary-validate" in j["paused_reason"].lower() or "whitespace" in j["paused_reason"]


def test_skip_unrelated_jobs(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-something-else", "enabled": True, "script": "x.py",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    assert json.loads(fake.read_text())["jobs"][0]["enabled"] is True


def test_skip_already_disabled(tmp_path, monkeypatch):
    mod = _load_module()
    original_reason = "already disabled for X"
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-research-associate-daily",
        "enabled": False,
        "paused_reason": original_reason,
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    assert json.loads(fake.read_text())["jobs"][0]["paused_reason"] == original_reason


def test_idempotent(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-research-associate-daily", "enabled": True,
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    state = fake.read_text()
    mod.patch(apply=True)
    mod.patch(apply=True)
    assert fake.read_text() == state


def test_handles_both_registries(tmp_path, monkeypatch):
    mod = _load_module()
    for sub in ("a", "b"):
        (tmp_path / sub).mkdir()
    fake_a = _make_jobs_file(tmp_path / "a", [{
        "name": "aiw-research-associate-daily", "enabled": True,
    }])
    fake_b = _make_jobs_file(tmp_path / "b", [{
        "name": "aiw-research-associate-daily", "enabled": True,
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_a, fake_b])
    mod.patch(apply=True)
    assert json.loads(fake_a.read_text())["jobs"][0]["enabled"] is False
    assert json.loads(fake_b.read_text())["jobs"][0]["enabled"] is False


@pytest.mark.parametrize("name", [
    # Block A — Anthropic auth (no Anthropic available)
    "aiw-research-associate-daily",
    "aiw-research-engineer-weekly",
    "aiw-research-tracker-6h",
    "aiw-citation-checker-daily",
    "aiw-publication-coordinator-weekly",
    # Block B — Cerebras billing (no Cerebras plan)
    "aiw-saas-lifecycle-reconcile",
    # Block C — missing infra
    "kv-bws-sync",
    "linkedin-token-refresh",
    "instagram-token-refresh",
    "aiw-boundary-validate-hourly",
])
def test_all_disabled_crons_listed(name):
    """Regression guard: every cron in the disable list must remain listed.

    Adding a new cron to JOBS_TO_DISABLE requires updating the parametrize
    list. Removing one breaks this test. That's the intended contract.
    """
    mod = _load_module()
    assert name in mod.JOBS_TO_DISABLE, f"missing {name} from JOBS_TO_DISABLE"
