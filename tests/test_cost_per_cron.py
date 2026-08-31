"""Tests for scripts/cost-per-cron.py."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "cost-per-cron.py"


def load_module():
    spec = importlib.util.spec_from_file_location("cost_per_cron", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_runs_per_day_interval():
    mod = load_module()
    s = {"kind": "interval", "minutes": 30}
    runs = mod._runs_per_day_from_schedule(s)
    assert runs == 48.0


def test_runs_per_day_weekly_cron():
    mod = load_module()
    s = {"kind": "cron", "expr": "0 22 * * 1"}  # Mondays at 22:00
    runs = mod._runs_per_day_from_schedule(s)
    assert 0.14 <= runs <= 0.20  # ~1/7


def test_runs_per_day_invalid_schedule():
    mod = load_module()
    runs = mod._runs_per_day_from_schedule({})
    assert runs == 1.0


def test_match_cost_direct():
    mod = load_module()
    costs = {"foo-bar": {"daily_cost_usd": 1.0}}
    m = mod._match_cost("foo-bar", costs)
    assert m is not None
    assert m["daily_cost_usd"] == 1.0


def test_match_cost_strip_prefix():
    mod = load_module()
    costs = {"business-analyst-daily": {"daily_cost_usd": 0.5}}
    m = mod._match_cost("aiw-business-analyst-daily", costs)
    assert m is not None
    assert m["daily_cost_usd"] == 0.5


def test_match_cost_strip_suffix():
    mod = load_module()
    costs = {"business-analyst": {"daily_cost_usd": 0.5}}
    m = mod._match_cost("aiw-business-analyst-daily", costs)
    assert m is not None
    assert m["daily_cost_usd"] == 0.5


def test_match_cost_returns_none_for_unknown():
    mod = load_module()
    costs = {"foo": {"daily_cost_usd": 1.0}}
    m = mod._match_cost("totally-unrelated-name", costs)
    assert m is None


def test_correlate_basic():
    mod = load_module()
    jobs = [
        {"name": "aiw-business-analyst-daily", "schedule": {"kind": "cron", "expr": "0 9 * * *"}},
        {"name": "aiw-unknown", "schedule": {"kind": "interval", "minutes": 60}},
    ]
    costs = {
        "agents": {
            "business-analyst-daily": {"daily_cost_usd": 0.04, "monthly_cost_usd": 1.12, "model": "primary"},
        }
    }
    report = mod.correlate(jobs, costs)
    assert report["total_jobs"] == 2
    assert report["matched_jobs"] == 1  # only one matched
    assert report["uncategorized"][0]["cron_name"] == "aiw-unknown"


def test_correlate_orders_top_by_cost():
    mod = load_module()
    jobs = [
        {"name": "cheap", "schedule": {"kind": "interval", "minutes": 1440}},
        {"name": "expensive", "schedule": {"kind": "interval", "minutes": 30}},
    ]
    costs = {
        "agents": {
            "cheap": {"daily_cost_usd": 0.01, "monthly_cost_usd": 0.30, "model": "primary"},
            "expensive": {"daily_cost_usd": 5.0, "monthly_cost_usd": 150.0, "model": "primary"},
        }
    }
    report = mod.correlate(jobs, costs)
    top = report["top_10_by_daily"]
    assert top[0]["cron_name"] == "expensive"


if __name__ == "__main__":
    test_runs_per_day_interval()
    test_runs_per_day_weekly_cron()
    test_runs_per_day_invalid_schedule()
    test_match_cost_direct()
    test_match_cost_strip_prefix()
    test_match_cost_strip_suffix()
    test_match_cost_returns_none_for_unknown()
    test_correlate_basic()
    test_correlate_orders_top_by_cost()
    print("\nAll cost-per-cron tests passed!")
