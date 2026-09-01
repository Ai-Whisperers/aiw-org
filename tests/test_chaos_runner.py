"""test_chaos_runner.py — Tests for scripts/chaos-runner.py scenarios 2-5.

Phase 9 R3 / Tier B7. Validates that chaos scenarios for network,
provider, disk, and schema-migration failures work correctly.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO = Path("/opt/data/agents")
VENV = Path("/opt/data/.venv") / "bin" / "python3"
SCRIPT = REPO / "scripts" / "chaos-runner.py"


@pytest.fixture
def staging():
    """Per-test staging directory."""
    tmp = Path(tempfile.mkdtemp(prefix="test-chaos-"))
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


def _run_scenario(n: int, staging: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(VENV), str(SCRIPT), "--scenario", str(n), "--staging-dir", str(staging)],
        capture_output=True, text=True, timeout=60,
    )


def test_scenario_2_network_partition(staging):
    """Scenario 2: TEST-NET-1 unreachable + fetch fails fast."""
    r = _run_scenario(2, staging)
    assert r.returncode == 0, f"rc={r.returncode}, stderr={r.stderr}"
    result_path = Path("/opt/data/state/chaos-test-result.json")
    assert result_path.exists()
    data = json.loads(result_path.read_text())
    assert data["scenario"] == 2
    assert data["passed"] is True
    assert any(c["step"] == "test-net-unreachable" for c in data["checks"])
    assert any(c["step"] == "fetch-fails-fast" for c in data["checks"])


def test_scenario_3_provider_outage(staging):
    """Scenario 3: 429 cascade → backoff → give up."""
    r = _run_scenario(3, staging)
    assert r.returncode == 0, f"rc={r.returncode}, stderr={r.stderr}"
    result_path = Path("/opt/data/state/chaos-test-result.json")
    data = json.loads(result_path.read_text())
    assert data["scenario"] == 3
    assert data["passed"] is True
    assert any(c["step"] == "rate-limit-backoff" for c in data["checks"])


def test_scenario_4_disk_full(staging):
    """Scenario 4: disk writes + atomic-write cleanup."""
    r = _run_scenario(4, staging)
    assert r.returncode == 0, f"rc={r.returncode}, stderr={r.stderr}"
    result_path = Path("/opt/data/state/chaos-test-result.json")
    data = json.loads(result_path.read_text())
    assert data["scenario"] == 4
    assert data["passed"] is True
    # Either ENOSPC was detected, or disk had space (skipped)
    check_steps = {c["step"] for c in data["checks"]}
    assert "enospc-detected" in check_steps or "disk-write-completed" in check_steps
    assert "atomic-write-cleanup" in check_steps


def test_scenario_5_schema_migration(staging):
    """Scenario 5: v1 → v2 migration idempotent."""
    r = _run_scenario(5, staging)
    assert r.returncode == 0, f"rc={r.returncode}, stderr={r.stderr}"
    result_path = Path("/opt/data/state/chaos-test-result.json")
    data = json.loads(result_path.read_text())
    assert data["scenario"] == 5
    assert data["passed"] is True
    assert any(c["step"] == "migration-first-run" for c in data["checks"])
    assert any(c["step"] == "migration-second-run" for c in data["checks"])
    assert any(c["step"] == "final-state-is-v2" for c in data["checks"])


def test_unknown_scenario_rejected():
    """Scenario 6+ should error out."""
    r = subprocess.run(
        [str(VENV), str(SCRIPT), "--scenario", "99"],
        capture_output=True, text=True, timeout=5,
    )
    assert r.returncode != 0
    assert "not implemented" in r.stdout or "ERROR" in r.stdout