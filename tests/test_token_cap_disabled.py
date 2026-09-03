"""Tests for token-cap.py — guards the real-measurement contract.

Per WS-2 item 3 of the Phase Kernel brief: a token-budget gate that
'always fires' due to a unit mismatch is worse than no gate. The original
stub was disabled to stop the false alarms.

Phase 9 R6 (2026-09-03): token-cap.py was rewritten to do REAL measurement
from session_model_usage + token-ledger.json, excluding the 18 test events
that were causing the false 180x over-budget alarm. It now:

  - Reads real fleet usage from state.db
  - Excludes test events (agent in {test-agent, verify}) from the ledger
  - Computes usage in 'credits' (1 credit = 1000 input-equivalent tokens)
  - Writes /opt/data/state/token-cap-alert.json with status: ok/warning/exceeded
  - Exits 0=ok, 1=warning, 2=exceeded

These tests verify the NEW contract.
"""
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "token-cap.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "token_cap_under_test", str(SCRIPT)
    )
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class TestScriptLoads(unittest.TestCase):
    def test_script_exists(self):
        self.assertTrue(SCRIPT.exists())

    def test_script_compiles(self):
        import py_compile
        py_compile.compile(str(SCRIPT), doraise=True)

    def test_module_imports(self):
        mod = load_module()
        self.assertTrue(callable(mod.main))


class TestRealMeasurementContract(unittest.TestCase):
    """The new contract: real measurement, real alerts, real exit codes."""

    def test_runs_and_produces_alert(self):
        """token-cap.py must write a token-cap-alert.json on each run."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True, timeout=30,
        )
        # Exit 0, 1, or 2 all acceptable; 0 means ok, 1 = warning, 2 = exceeded
        self.assertIn(result.returncode, (0, 1, 2),
                      f"Unexpected rc={result.returncode}: {result.stderr[:200]}")
        alert_path = Path("/opt/data/state/token-cap-alert.json")
        self.assertTrue(alert_path.exists(), "token-cap-alert.json must be written")
        alert = json.loads(alert_path.read_text())
        self.assertIn("status", alert)
        self.assertIn("used_credits", alert)
        self.assertIn("budget_credits", alert)
        self.assertIn(alert["status"], ("ok", "warning", "exceeded"))

    def test_alert_excludes_test_events(self):
        """The 18 test events in token-ledger.json must NOT contribute to
        used_credits (they're synthetic 999999 values)."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True, timeout=30,
        )
        alert = json.loads(Path("/opt/data/state/token-cap-alert.json").read_text())
        # If test events were included, used_credits would be > 10M
        # (18 * 999999 ≈ 18M). Real usage from session_model_usage is ~50k.
        self.assertLess(alert["used_credits"], 1_000_000,
                        f"used_credits={alert['used_credits']} suggests test events leaked in")
        # The sources section should report test_events_excluded >= 18
        excluded = alert.get("sources", {}).get("token_ledger_real_events", {}).get(
            "test_events_excluded", 0
        )
        self.assertGreaterEqual(excluded, 18,
                                "Test events should be reported as excluded")

    def test_alert_uses_real_session_data(self):
        """The used_credits should be derived from session_model_usage,
        not from synthetic test data."""
        alert = json.loads(Path("/opt/data/state/token-cap-alert.json").read_text())
        # Window should be 24h
        self.assertEqual(alert.get("window_hours"), 24)
        # Status must be a real value (not 'disabled' from the old stub)
        self.assertNotEqual(alert.get("status"), "disabled",
                           "Should not report 'disabled' — does real work now")

    def test_writes_only_token_cap_alert_not_coord(self):
        """Per the original WS-2 finding: token-cap must NOT spam
        coord.json:decisions_for_ivan with fake alerts."""
        coord = Path("/opt/data/state/coord.json")
        if not coord.exists():
            self.skipTest("coord.json not present in test environment")

        before = json.loads(coord.read_text())
        before_count = len(before.get("decisions_for_ivan", []))

        for _ in range(3):
            subprocess.run([sys.executable, str(SCRIPT)],
                          capture_output=True, timeout=30)

        after = json.loads(coord.read_text())
        after_count = len(after.get("decisions_for_ivan", []))
        new_entries = after.get("decisions_for_ivan", [])[before_count:]
        token_cap_entries = [
            e for e in new_entries
            if "token-cap" in str(e.get("source", ""))
        ]
        self.assertEqual(len(token_cap_entries), 0,
                         f"token-cap wrote {len(token_cap_entries)} coord entries; expected 0")


class TestModuleExports(unittest.TestCase):
    """Static checks: the rewritten module has the expected surface."""

    def test_has_required_helpers(self):
        mod = load_module()
        self.assertTrue(hasattr(mod, "tokens_to_credits"),
                        "Should export tokens_to_credits helper")
        self.assertTrue(hasattr(mod, "read_real_24h_tokens"),
                        "Should export read_real_24h_tokens")
        self.assertTrue(hasattr(mod, "read_ledger_real_credits"),
                        "Should export read_ledger_real_credits")


if __name__ == "__main__":
    unittest.main(verbosity=2)
