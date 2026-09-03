"""Tests for scripts/inject_cache_control.py."""
import importlib.util
import json
from pathlib import Path
import pytest

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "inject_cache_control.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "inject_cache_control", str(SCRIPT)
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
    fake = tmp_path / "jobs.json"
    long_prompt = "x" * 500
    fake.write_text(json.dumps({"jobs": [{
        "name": "aiw-test",
        "enabled": True,
        "prompt": long_prompt,
    }]}))
    original = fake.read_text()
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=False)
    assert fake.read_text() == original


def test_apply_adds_marker_to_long_prompts(tmp_path, monkeypatch):
    mod = _load_module()
    fake = tmp_path / "jobs.json"
    long_prompt = "x" * 500
    fake.write_text(json.dumps({"jobs": [{
        "name": "aiw-test",
        "enabled": True,
        "prompt": long_prompt,
    }]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    data = json.loads(fake.read_text())
    assert "cache_control" in data["jobs"][0]["prompt"]


def test_skip_short_prompts(tmp_path, monkeypatch):
    mod = _load_module()
    fake = tmp_path / "jobs.json"
    short_prompt = "x" * 100
    fake.write_text(json.dumps({"jobs": [{
        "name": "aiw-test",
        "enabled": True,
        "prompt": short_prompt,
    }]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    data = json.loads(fake.read_text())
    assert data["jobs"][0]["prompt"] == short_prompt


def test_skip_already_marked(tmp_path, monkeypatch):
    mod = _load_module()
    fake = tmp_path / "jobs.json"
    long_prompt = "x" * 500 + "\n\n[cache_control: ephemeral]"
    fake.write_text(json.dumps({"jobs": [{
        "name": "aiw-test",
        "enabled": True,
        "prompt": long_prompt,
    }]}))
    original = fake.read_text()
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    assert fake.read_text() == original


def test_skip_disabled_jobs(tmp_path, monkeypatch):
    mod = _load_module()
    fake = tmp_path / "jobs.json"
    long_prompt = "x" * 500
    fake.write_text(json.dumps({"jobs": [{
        "name": "aiw-test",
        "enabled": False,
        "prompt": long_prompt,
    }]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    original = fake.read_text()
    mod.patch(apply=True)
    assert fake.read_text() == original


def test_idempotent(tmp_path, monkeypatch):
    mod = _load_module()
    fake = tmp_path / "jobs.json"
    long_prompt = "x" * 500
    fake.write_text(json.dumps({"jobs": [{
        "name": "aiw-test",
        "enabled": True,
        "prompt": long_prompt,
    }]}))
    monkeypatch.setattr(mod, "CRON_PATHS", [fake])
    mod.patch(apply=True)
    state = fake.read_text()
    mod.patch(apply=True)
    mod.patch(apply=True)
    assert fake.read_text() == state
