"""Tests for scripts/drift-calibrate.py."""
import importlib.util
import json
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "drift-calibrate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("drift_cal", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_empty_alerts():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        alerts_path = Path(tmp) / "alerts.json"
        output_path = Path(tmp) / "calibration.json"
        alerts_path.write_text(json.dumps([]))

        report = mod.calibrate([], window_days=30)
        # Empty input → no calibrations
        assert report["alerts_analyzed"] == 0
        assert report["calibrations"] == []
        assert report["summary"]["monitors_needing_calibration"] == 0


def test_zero_fires_recommends_loosen():
    mod = load_module()
    # 1 alert outside window (31 days old) - shouldn't be counted
    # 0 alerts in window - all monitors in window get "loosen"
    with tempfile.TemporaryDirectory() as tmp:
        alerts_path = Path(tmp) / "alerts.json"
        old_date = (datetime.now(timezone.utc) - timedelta(days=31)).isoformat()
        alerts_path.write_text(json.dumps([
            {"monitor": "old-monitor", "category": "D1", "timestamp": old_date},
        ]))
        recent = mod.load_alerts(alerts_path)
        report = mod.calibrate(recent, window_days=30)
        assert report["alerts_analyzed"] == 0


def test_high_fire_count_recommends_tighten():
    mod = load_module()
    # 25 alerts in window for one monitor - should recommend tighten
    now = datetime.now(timezone.utc)
    alerts = []
    for i in range(25):
        alerts.append({
            "monitor": "noisy-monitor",
            "category": "D1",
            "timestamp": (now - timedelta(days=i % 28)).isoformat(),
        })
    report = mod.calibrate(alerts, window_days=30)
    assert report["alerts_analyzed"] == 25
    assert len(report["calibrations"]) == 1
    cal = report["calibrations"][0]
    assert cal["monitor"] == "noisy-monitor"
    assert cal["recommendation"] == "tighten"
    assert cal["fires_in_window"] == 25


def test_moderate_fires_recommends_keep():
    mod = load_module()
    now = datetime.now(timezone.utc)
    alerts = [{
        "monitor": "stable-monitor",
        "category": "D1",
        "timestamp": (now - timedelta(days=5)).isoformat(),
    }]
    report = mod.calibrate(alerts, window_days=30)
    assert report["alerts_analyzed"] == 1
    cal = report["calibrations"][0]
    assert cal["recommendation"] == "keep"


def test_multiple_monitors_categories():
    mod = load_module()
    now = datetime.now(timezone.utc)
    alerts = [
        {"monitor": "a", "category": "D1", "timestamp": (now - timedelta(days=1)).isoformat()},
        {"monitor": "a", "category": "D1", "timestamp": (now - timedelta(days=2)).isoformat()},
        {"monitor": "b", "category": "D4", "timestamp": (now - timedelta(days=3)).isoformat()},
        {"monitor": "c", "category": "D5", "timestamp": (now - timedelta(days=4)).isoformat()},
    ]
    report = mod.calibrate(alerts, window_days=30)
    assert report["alerts_analyzed"] == 4
    assert len(report["calibrations"]) == 3  # (a,D1), (b,D4), (c,D5)
    monitors = {(c["monitor"], c["category"]) for c in report["calibrations"]}
    assert ("a", "D1") in monitors
    assert ("b", "D4") in monitors
    assert ("c", "D5") in monitors


def test_load_alerts_handles_missing_file():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        bogus = Path(tmp) / "nonexistent.json"
        alerts = mod.load_alerts(bogus)
        assert alerts == []


def test_load_alerts_handles_dict_with_alerts_key():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "alerts.json"
        path.write_text(json.dumps({
            "alerts": [
                {"monitor": "x", "category": "D2", "timestamp": datetime.now(timezone.utc).isoformat()}
            ]
        }))
        alerts = mod.load_alerts(path)
        assert len(alerts) == 1
        assert alerts[0]["monitor"] == "x"


def test_suggest_threshold_returns_string():
    mod = load_module()
    s = mod.suggest_threshold("D1", {"MEDIUM": 2.0, "HIGH": 3.0, "CRITICAL": 5.0}, "tighten")
    assert isinstance(s, str)
    assert "MEDIUM" in s and "HIGH" in s and "CRITICAL" in s


if __name__ == "__main__":
    test_empty_alerts()
    test_zero_fires_recommends_loosen()
    test_high_fire_count_recommends_tighten()
    test_moderate_fires_recommends_keep()
    test_multiple_monitors_categories()
    test_load_alerts_handles_missing_file()
    test_load_alerts_handles_dict_with_alerts_key()
    test_suggest_threshold_returns_string()
    print("\nAll drift-calibrate tests passed!")
