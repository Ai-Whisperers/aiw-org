"""Tests for scripts/eval-aggregate-pass-rate.py.

Tests the aggregate pass_rate computation logic by feeding known input data via
tempfiles (no importlib magic — uses the public `compute_aggregate` function).
"""
import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "eval-aggregate-pass-rate.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("eval_agg", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_no_agents_missing_file():
    """When eval-per-agent.json doesn't exist, script exits with error."""
    mod = _load_module()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        # Don't create the file
        nonexistent = Path(tmp) / "does-not-exist.json"
        try:
            mod.compute_aggregate(eval_file=nonexistent)
            assert False, "Should have raised SystemExit"
        except SystemExit as e:
            assert e.code == 1
    print("✓ test_no_agents_missing_file passed")


def test_empty_by_agent_no_alert():
    """When by_agent is empty, no alert should fire (avoid false CRITICAL on stale state)."""
    mod = _load_module()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        eval_file = Path(tmp) / "eval-per-agent.json"
        eval_file.write_text(json.dumps({
            "version": "1.0.0",
            "total": 0,
            "passed": 0,
            "failed": 0,
            "by_agent": {}
        }))
        result = mod.compute_aggregate(eval_file=eval_file)

    assert result["agent_count"] == 0
    assert result["aggregate_pass_rate"] == 0.0
    assert result["alert"] is None, f"Empty state should NOT alert; got: {result['alert']}"
    print("✓ test_empty_by_agent_no_alert passed")


def test_passing_agents_no_alert():
    """When all agents are above 0.95, alert should be None."""
    mod = _load_module()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        eval_file = Path(tmp) / "eval-per-agent.json"
        eval_file.write_text(json.dumps({
            "version": "1.0.0",
            "total": 100,
            "passed": 98,
            "failed": 2,
            "by_agent": {
                "agent_a": {"pass_rate": 0.97, "eval_count": 50, "consecutive_failures": 0},
                "agent_b": {"pass_rate": 0.99, "eval_count": 50, "consecutive_failures": 0},
            }
        }))
        result = mod.compute_aggregate(eval_file=eval_file)

    assert result["agent_count"] == 2
    assert result["passing_agents"] == 2
    assert result["warning_agents"] == 0
    assert result["failing_agents"] == 0
    assert result["aggregate_pass_rate"] >= 0.95
    assert result["alert"] is None
    print("✓ test_passing_agents_no_alert passed")


def test_mixed_agents_high_streak_alert():
    """When one agent has 5+ consecutive failures AND aggregate is good, alert should mention the agent."""
    mod = _load_module()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        eval_file = Path(tmp) / "eval-per-agent.json"
        # 99 good agents + 1 bad with high streak; aggregate should be high
        # but the bad agent's streak should still trigger the alert
        eval_file.write_text(json.dumps({
            "version": "1.0.0",
            "by_agent": {
                "agent_good": {"pass_rate": 1.0, "eval_count": 100, "consecutive_failures": 0},
                "agent_bad": {"pass_rate": 0.96, "eval_count": 1, "consecutive_failures": 7},
            }
        }))
        result = mod.compute_aggregate(eval_file=eval_file)

    # With aggregate weighted: (1.0*100 + 0.96*1) / 101 = 100.96/101 = 0.9996 → above 0.95
    # So aggregate alert shouldn't fire; only streak alert
    assert result["aggregate_pass_rate"] >= 0.95
    assert result["longest_streak"]["agent"] == "agent_bad"
    assert result["longest_streak"]["consecutive_failures"] == 7
    assert result["alert"] is not None
    assert "agent_bad" in result["alert"]
    print("✓ test_mixed_agents_high_streak_alert passed")


def test_low_aggregate_alert():
    """When aggregate pass_rate < 0.5, alert should be CRITICAL."""
    mod = _load_module()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        eval_file = Path(tmp) / "eval-per-agent.json"
        eval_file.write_text(json.dumps({
            "version": "1.0.0",
            "by_agent": {
                "a": {"pass_rate": 0.3, "eval_count": 5, "consecutive_failures": 0},
                "b": {"pass_rate": 0.4, "eval_count": 5, "consecutive_failures": 0},
            }
        }))
        result = mod.compute_aggregate(eval_file=eval_file)

    assert result["aggregate_pass_rate"] < 0.5
    assert result["alert"] == "CRITICAL: aggregate pass_rate below 0.5"
    print("✓ test_low_aggregate_alert passed")


def test_backward_compat_no_by_agent():
    """When state file is in flat form (no by_agent), still works."""
    mod = _load_module()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        eval_file = Path(tmp) / "eval-per-agent.json"
        # Flat form (legacy)
        eval_file.write_text(json.dumps({
            "agent_legacy": {"pass_rate": 0.8, "eval_count": 5, "consecutive_failures": 0}
        }))
        result = mod.compute_aggregate(eval_file=eval_file)

    assert result["agent_count"] == 1
    assert "agent_legacy" in result["per_agent"]
    print("✓ test_backward_compat_no_by_agent passed")


if __name__ == "__main__":
    test_no_agents_missing_file()
    test_empty_by_agent_no_alert()
    test_passing_agents_no_alert()
    test_mixed_agents_high_streak_alert()
    test_low_aggregate_alert()
    test_backward_compat_no_by_agent()
    print("\nAll eval-aggregate-pass-rate tests passed!")
