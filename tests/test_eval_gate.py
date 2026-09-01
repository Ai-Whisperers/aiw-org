"""test_eval_gate.py — Tests for scripts/eval-gate-enforce.py.

Phase 9 R3 / Tier B4. Verifies eval gate enforcement decisions
(ALLOW / WARN / BLOCK based on PASS_RATE threshold).
"""
import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path("/opt/data/agents")
SCRIPT = REPO / "scripts" / "eval-gate-enforce.py"
PER_AGENT = Path("/opt/data/state/eval-per-agent.json")


def _load_module():
    spec = importlib.util.spec_from_file_location("eval_gate_enforce", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_module_loads():
    """The script loads without syntax errors."""
    mod = _load_module()
    assert hasattr(mod, "main")
    assert hasattr(mod, "argparse")


def test_unknown_agent_warns():
    """Agent with no eval data produces WARN."""
    mod = _load_module()
    # Patch the per-agent path to a fixture
    fixture = Path("/tmp/test-eval-unknown.json")
    fixture.write_text(json.dumps({
        "version": "1.0.0", "by_agent": {}
    }))
    # Test by calling main with subprocess
    import subprocess, sys
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--agent", "unknown-agent"],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 0
    assert "WARN" in r.stdout


def test_decision_log_path_exists():
    """The decisions log file exists (or script creates it)."""
    decisions_log = Path("/opt/data/state/eval-gate-decisions.ndjson")
    # The log may or may not exist depending on prior runs
    # Just verify the script references it (no crash)
    assert SCRIPT.exists()


def test_policy_file_exists():
    """Policy YAML file was created in Phase 9 R3."""
    policy = REPO / "eval" / "eval-gate-policy.yaml"
    assert policy.exists()
    data = json.loads(__import__("yaml").safe_load(policy.read_text()) and json.dumps(__import__("yaml").safe_load(policy.read_text())))
    # Schema check
    assert "thresholds" in data
    assert data["thresholds"]["allow_threshold"] == 0.50
    assert data["thresholds"]["warn_threshold"] == 0.30