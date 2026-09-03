"""Tests for scripts/fix_intake_cron_args.py."""
import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "fix_intake_cron_args.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "fix_intake_cron_args", str(SCRIPT)
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
        "name": "aiw-intake-sales-10min",
        "enabled": True,
        "script": "/opt/data/scripts/intake.py",
    }])
    original = fake.read_text()
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=False)
    assert fake.read_text() == original


def test_apply_replaces_intake_script(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-intake-sales-10min",
        "enabled": True,
        "script": "/opt/data/scripts/intake.py",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    data = json.loads(fake.read_text())
    assert data["jobs"][0]["script"] == "/opt/data/scripts/intake-sales.sh"


def test_apply_replaces_all_intake_depts(tmp_path, monkeypatch):
    mod = _load_module()
    depts = ["sales", "finance", "operations", "research", "engineering", "people", "board"]
    jobs = [{
        "name": f"aiw-intake-{d}-10min",
        "enabled": True,
        "script": "/opt/data/scripts/intake.py",
    } for d in depts]
    fake = _make_jobs_file(tmp_path, jobs)
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    data = json.loads(fake.read_text())
    for i, d in enumerate(depts):
        assert data["jobs"][i]["script"] == f"/opt/data/scripts/intake-{d}.sh", \
            f"dept {d} script not updated"


def test_apply_replaces_eval_gate_decisions_summary(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-eval-gate-decisions-summary",
        "enabled": True,
        "script": "/opt/data/scripts/eval-gate-enforce.py",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    data = json.loads(fake.read_text())
    assert data["jobs"][0]["script"] == "/opt/data/scripts/eval-gate-decisions-summary.sh"


def test_skip_unrelated_jobs(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-something-else",
        "enabled": True,
        "script": "/opt/data/scripts/x.py",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    original = fake.read_text()
    mod.patch(apply=True)
    assert fake.read_text() == original


def test_skip_already_updated(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-intake-sales-10min",
        "enabled": True,
        "script": "/opt/data/scripts/intake-sales.sh",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    original = fake.read_text()
    mod.patch(apply=True)
    assert fake.read_text() == original


def test_idempotent(tmp_path, monkeypatch):
    mod = _load_module()
    fake = _make_jobs_file(tmp_path, [{
        "name": "aiw-intake-sales-10min",
        "enabled": True,
        "script": "/opt/data/scripts/intake.py",
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
        "name": "aiw-intake-sales-10min",
        "enabled": True,
        "script": "/opt/data/scripts/intake.py",
    }])
    fake_b = _make_jobs_file(b_dir, [{
        "name": "aiw-intake-sales-10min",
        "enabled": True,
        "script": "/opt/data/scripts/intake.py",
    }])
    monkeypatch.setattr(mod, "CRON_PATHS", [fake_a, fake_b])
    mod.patch(apply=True)
    assert json.loads(fake_a.read_text())["jobs"][0]["script"] == "/opt/data/scripts/intake-sales.sh"
    assert json.loads(fake_b.read_text())["jobs"][0]["script"] == "/opt/data/scripts/intake-sales.sh"
