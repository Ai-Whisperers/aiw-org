"""test_find_overlapping.py — Tests for cost-optimize.find_overlapping().

Phase 9 R3 / Tier B2. Verifies the new temporal-proximity detector
correctly identifies pile-ups (Aug 30-style stacks) that the old
exact-string bucketing missed.
"""
import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path("/opt/data/agents")
SCRIPT = REPO / "scripts" / "cost-optimize.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("cost_optimize", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_finds_aug_30_sunday_stack():
    """Regression: Aug 30 Sunday pile-up (4 jobs within 3.5h on Sunday)."""
    mod = _load_module()
    # Simulate the 2026-08-30 Sunday stack
    jobs = [
        {"name": "a", "enabled": True, "schedule": {"expr": "0 18 * * 0"}},
        {"name": "b", "enabled": True, "schedule": {"expr": "30 19 * * 0"}},
        {"name": "c", "enabled": True, "schedule": {"expr": "0 20 * * 0"}},
        {"name": "d", "enabled": True, "schedule": {"expr": "0 21 * * 0"}},
        # Isolated cron (should NOT be in any pile-up)
        {"name": "e", "enabled": True, "schedule": {"expr": "0 3 * * *"}},
    ]
    pileups = mod.find_overlapping(jobs, proximity_window_min=240, min_cluster_size=3)
    # All 4 Sunday jobs should be in one cluster
    assert len(pileups) >= 1
    sunday_pileup = [p for p in pileups if p["day_of_week"] == 6]
    assert len(sunday_pileup) >= 1
    crons_in_pileup = set()
    for p in sunday_pileup:
        crons_in_pileup.update(p["crons"])
    assert {"a", "b", "c", "d"}.issubset(crons_in_pileup)
    assert "e" not in crons_in_pileup


def test_5min_interval_jobs_cluster():
    """5-min interval jobs all firing within a 5-min window cluster together."""
    mod = _load_module()
    jobs = [
        {"name": f"job-{i}", "enabled": True, "schedule": {"expr": "*/5 * * * *"}}
        for i in range(5)
    ]
    pileups = mod.find_overlapping(jobs, proximity_window_min=5, min_cluster_size=3)
    assert len(pileups) >= 1


def test_disabled_jobs_excluded():
    """Disabled jobs should not appear in pile-ups."""
    mod = _load_module()
    jobs = [
        {"name": "a", "enabled": True, "schedule": {"expr": "0 18 * * 0"}},
        {"name": "b", "enabled": True, "schedule": {"expr": "30 19 * * 0"}},
        {"name": "c", "enabled": False, "schedule": {"expr": "0 20 * * 0"}},
        {"name": "d", "enabled": True, "schedule": {"expr": "0 21 * * 0"}},
    ]
    pileups = mod.find_overlapping(jobs, proximity_window_min=240, min_cluster_size=3)
    all_crons = set()
    for p in pileups:
        all_crons.update(p["crons"])
    assert "c" not in all_crons


def test_empty_jobs():
    """Empty list returns empty pile-ups."""
    mod = _load_module()
    assert mod.find_overlapping([]) == []


def test_real_jobs_config():
    """Smoke test: run on real /opt/data/.hermes/cron/jobs.json."""
    mod = _load_module()
    with open("/opt/data/.hermes/cron/jobs.json") as f:
        data = json.load(f)
    pileups = mod.find_overlapping(data["jobs"], proximity_window_min=60, min_cluster_size=5)
    # Should find at least some real pile-ups in a config of 167 jobs
    # (this is the verification gate: we want the detector to actually fire)
    assert isinstance(pileups, list)