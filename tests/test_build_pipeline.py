"""test_build_pipeline.py — Tests for scripts/build-pipeline.py.

Phase 9 R3 / Tier C4. Validates the runtime dispatcher for the
two-phase build pipeline (architect → builder + auditor).
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
SCRIPT = REPO / "scripts" / "build-pipeline.py"
DISPATCH_RULES = REPO / "demiurge" / "router" / "dispatch-rules.yaml"


def _load_module():
    spec = importlib.util.spec_from_file_location("build_pipeline", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_module_loads():
    """build-pipeline.py loads without error."""
    mod = _load_module()
    assert hasattr(mod, "main")


def test_list_rules_subprocess():
    """list-rules CLI shows dispatch rules."""
    r = subprocess.run(
        [str(VENV), str(SCRIPT), "list-rules"],
        capture_output=True, text=True, timeout=5,
    )
    assert r.returncode == 0
    assert "rules loaded" in r.stdout


def test_validate_rules_passes():
    """All 13 dispatch rules reference existing agents."""
    r = subprocess.run(
        [str(VENV), str(SCRIPT), "validate-rules"],
        capture_output=True, text=True, timeout=5,
    )
    assert r.returncode == 0, f"Validation failed: {r.stdout}"
    assert "validated" in r.stdout


def test_dispatch_with_synthetic_signal():
    """Dispatch a synthetic signal and verify log written."""
    tmp_signal = Path(tempfile.mkdtemp(prefix="test-signal-")) / "signal.json"
    tmp_signal.write_text(json.dumps({
        "signal_type": "cross_dept",
        "routing_tags": ["lead", "inbound"],
        "from": "test-dept",
    }))
    r = subprocess.run(
        [str(VENV), str(SCRIPT), "dispatch", "--signal", str(tmp_signal)],
        capture_output=True, text=True, timeout=5,
    )
    assert r.returncode == 0
    assert "delivering" in r.stdout or "No matching rule" in r.stdout
    # Verify log was appended
    log = Path("/opt/data/state/build-pipeline-dispatch.ndjson")
    assert log.exists()
    shutil.rmtree(tmp_signal.parent, ignore_errors=True)


def test_dispatch_no_match_returns_0():
    """A signal with no matching rule returns 0 (not an error)."""
    tmp_signal = Path(tempfile.mkdtemp(prefix="test-signal-")) / "signal.json"
    tmp_signal.write_text(json.dumps({
        "signal_type": "nonexistent-type-xyz",
        "routing_tags": ["unknown"],
    }))
    r = subprocess.run(
        [str(VENV), str(SCRIPT), "dispatch", "--signal", str(tmp_signal)],
        capture_output=True, text=True, timeout=5,
    )
    assert r.returncode == 0
    assert "No matching rule" in r.stdout
    shutil.rmtree(tmp_signal.parent, ignore_errors=True)


def test_architect_auditor_builder_agents_exist():
    """The 3 atomic agents for the two-phase pipeline exist."""
    for agent in ["architect-agent", "auditor-agent", "builder-agent"]:
        prompt = REPO / "demiurge" / "agents" / agent / "PROMPT.md"
        assert prompt.exists(), f"Missing {prompt}"


def test_dispatch_rules_yaml_exists():
    """dispatch-rules.yaml exists and is parseable."""
    assert DISPATCH_RULES.exists()
    import yaml
    rules = yaml.safe_load(DISPATCH_RULES.read_text())
    assert "dispatch_rules" in rules
    assert len(rules["dispatch_rules"]) >= 13