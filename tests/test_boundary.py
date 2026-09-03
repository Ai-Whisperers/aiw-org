"""test_boundary.py — Tests for scripts/boundary-validate.py + boundary-sync.py.

Phase 9 R3 / Tier C6. Validates the boundary between aiw-org and
growth-coaching repos.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO = Path("/opt/data/agents")
VENV = Path("/opt/data/.venv") / "bin" / "python3"
VALIDATE = REPO / "scripts" / "boundary-validate.py"
SYNC = REPO / "scripts" / "boundary-sync.py"
BOUNDARY = Path("/opt/data/boundary")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_validate_module_loads():
    mod = _load(VALIDATE, "boundary_validate")
    assert hasattr(mod, "validate_signal")
    assert hasattr(mod, "validate_session")
    assert hasattr(mod, "validate_coach")


def test_sync_module_loads():
    mod = _load(SYNC, "boundary_sync")
    assert hasattr(mod, "sync_file")
    assert hasattr(mod, "load_sync_state")


def test_validate_signal_good():
    mod = _load(VALIDATE, "boundary_validate")
    rec = {
        "signal_type": "coach_engagement",
        "source": "growth-coaching",
        "target": "ai-ops-coordinator",
        "payload": {"coach_id": "abc"},
        "timestamp": "2026-09-01T21:00:00+00:00",
    }
    errors = mod.validate_signal(rec)
    assert errors == []


def test_validate_signal_missing_field():
    mod = _load(VALIDATE, "boundary_validate")
    rec = {"signal_type": "coach_engagement", "source": "x"}  # missing fields
    errors = mod.validate_signal(rec)
    assert len(errors) > 0


def test_validate_signal_bad_type():
    mod = _load(VALIDATE, "boundary_validate")
    rec = {
        "signal_type": "INVALID_TYPE",
        "source": "x", "target": "y", "payload": {}, "timestamp": "2026-09-01T21:00:00+00:00",
    }
    errors = mod.validate_signal(rec)
    assert any("signal_type" in e for e in errors)


def test_validate_session_uuid():
    mod = _load(VALIDATE, "boundary_validate")
    rec = {
        "session_id": "550e8400-e29b-41d4-a716-446655440000",
        "coach_id": "abc",
        "customer_id": "xyz",
        "started_at": "2026-09-01T20:00:00+00:00",
    }
    errors = mod.validate_session(rec)
    assert errors == []


def test_validate_session_bad_uuid():
    mod = _load(VALIDATE, "boundary_validate")
    rec = {
        "session_id": "not-a-uuid",
        "coach_id": "abc",
        "customer_id": "xyz",
        "started_at": "2026-09-01T20:00:00+00:00",
    }
    errors = mod.validate_session(rec)
    assert any("session_id" in e for e in errors)


def test_validate_coach_status():
    mod = _load(VALIDATE, "boundary_validate")
    rec = {"coach_id": "abc", "name": "Test Coach", "status": "active"}
    errors = mod.validate_coach(rec)
    assert errors == []
    rec["status"] = "INVALID"
    errors = mod.validate_coach(rec)
    assert any("status" in e for e in errors)


def test_validate_cli_runs():
    r = subprocess.run(
        [str(VENV), str(VALIDATE), "--all"],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 0
    assert "TOTAL" in r.stdout


def test_sync_cli_runs():
    r = subprocess.run(
        [str(VENV), str(SYNC)],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 0
    assert "TOTAL" in r.stdout


@pytest.mark.slow  # integration: requires production state
def test_boundary_config_exists():
    """Boundary config.yaml exists at /opt/data/boundary/."""
    config = BOUNDARY / "config.yaml"
    assert config.exists()
    data = yaml_load(config)
    assert "schema_versions" in data
    assert "sync_interval_min" in data


def test_boundary_spec_doc_exists():
    """The boundary spec doc is committed."""
    spec = REPO / "docs" / "COACHING-AIW-BOUNDARY-SPEC.md"
    assert spec.exists()
    content = spec.read_text()
    assert "ADR-0004" in content
    assert "boundary" in content.lower()


@pytest.mark.slow  # integration: requires production state
def test_2_boundary_crons_wired():
    """2 boundary cron entries should be wired."""
    cron_path = Path("/opt/data/.hermes/cron/jobs.json")
    with cron_path.open() as f:
        jobs = json.load(f)
    boundary_crons = [j for j in jobs["jobs"] if "boundary" in j["name"]]
    assert len(boundary_crons) >= 2


def yaml_load(p):
    import yaml
    return yaml.safe_load(p.read_text())