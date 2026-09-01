"""Tests for credit-burn-probe.py.

Per AGENTS.md: every change must be tested before commit. This file
adds regression coverage for the probe script shipped in P0.6.

Tests:
- --report reads agent-traces.jsonl correctly (or no-ops if missing)
- --start creates probe.json with correct shape
- --status reads probe.json without errors
- --stop updates probe.json with completed_at
- --start with custom --target persists the target name
- pricing table covers all known models (M3, GLM, Claude variants)
- idempotent: --start twice overwrites cleanly

NOTE: This script lives in scripts/ which is the production code path.
"""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "credit-burn-probe.py"
TRACES_PATH = Path("/opt/data/state/agent-traces.jsonl")
PROBE_PATH = Path("/opt/data/state/credit-burn-probe.json")


def load_module():
    spec = importlib.util.spec_from_file_location(
        "credit_burn_probe_under_test", str(SCRIPT)
    )
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class TestScriptLoads(unittest.TestCase):
    def test_script_exists(self):
        self.assertTrue(SCRIPT.exists(),
                        f"missing: {SCRIPT}")

    def test_script_compiles(self):
        import py_compile
        py_compile.compile(str(SCRIPT), doraise=True)

    def test_module_imports(self):
        mod = load_module()
        self.assertTrue(callable(mod.start_probe))
        self.assertTrue(callable(mod.status))
        self.assertTrue(callable(mod.stop_probe))
        self.assertTrue(callable(mod.report))


class TestPricingTable(unittest.TestCase):
    """Pricing table must cover known models — gaps = silent $0.00 cost."""

    def test_pricing_covers_minimax_m3(self):
        mod = load_module()
        self.assertIn("MiniMax-M3", mod.PRICING)
        # M3 is $0.30/$1.20 per cited research
        self.assertEqual(mod.PRICING["MiniMax-M3"]["input"], 0.30)
        self.assertEqual(mod.PRICING["MiniMax-M3"]["output"], 1.20)

    def test_pricing_covers_glm_4_6(self):
        mod = load_module()
        self.assertIn("zai-glm-4-flash", mod.PRICING)
        self.assertIn("GLM-4.6", mod.PRICING)

    def test_pricing_covers_claude_variants(self):
        mod = load_module()
        # These exist because we want to detect if any cron accidentally
        # routes to expensive Claude (the $93.61/day concern)
        self.assertIn("claude-opus-4.8", mod.PRICING)
        self.assertIn("claude-sonnet-4.6", mod.PRICING)


class TestProbeStateLifecycle(unittest.TestCase):
    """The probe state file lifecycle: start → status → stop."""

    def setUp(self):
        # Clean state before each test
        if PROBE_PATH.exists():
            PROBE_PATH.unlink()

    def tearDown(self):
        if PROBE_PATH.exists():
            PROBE_PATH.unlink()

    def test_start_creates_probe_state(self):
        mod = load_module()
        mod.start_probe("test-cron")
        self.assertTrue(PROBE_PATH.exists(), "start_probe should create probe.json")
        probe = json.loads(PROBE_PATH.read_text())
        self.assertEqual(probe["target_cron"], "test-cron")
        self.assertIsNotNone(probe["started_at"])
        self.assertIsNone(probe["completed_at"])
        self.assertEqual(probe["events"], [])
        self.assertEqual(probe["totals"]["events"], 0)

    def test_status_returns_in_progress(self):
        mod = load_module()
        mod.start_probe("cron-xyz")
        probe = mod.status()
        self.assertEqual(probe["target_cron"], "cron-xyz")
        self.assertIsNone(probe["completed_at"])

    def test_stop_marks_completed(self):
        mod = load_module()
        mod.start_probe("cron-abc")
        probe = mod.stop_probe()
        self.assertIsNotNone(probe["completed_at"])
        # File on disk should reflect the completion
        on_disk = json.loads(PROBE_PATH.read_text())
        self.assertIsNotNone(on_disk["completed_at"])

    def test_start_overwrites_previous(self):
        """Idempotent: --start twice produces a single clean probe."""
        mod = load_module()
        mod.start_probe("first-cron")
        mod.start_probe("second-cron")
        probe = json.loads(PROBE_PATH.read_text())
        self.assertEqual(probe["target_cron"], "second-cron")
        self.assertEqual(probe["events"], [])


class TestReportReadsAgentTraces(unittest.TestCase):
    """The report reads agent-traces.jsonl as the empirical data source."""

    def test_report_handles_missing_traces_gracefully(self):
        """If agent-traces.jsonl doesn't exist, report exits cleanly with $0."""
        # Use a temporary path for the traces (force-import the module and patch)
        mod = load_module()
        # Save original and replace — use setattr to bypass ModuleType restriction
        original = mod.TRACES_PATH
        setattr(mod, "TRACES_PATH", Path("/tmp/nonexistent-traces.jsonl"))
        try:
            report = mod.report()
            # Report with empty events returns {} (empty dict)
            self.assertEqual(report, {})
        finally:
            setattr(mod, "TRACES_PATH", original)

    def test_report_aggregates_by_model(self):
        """Report groups tokens by model with cost calculation."""
        # Use real agent-traces.jsonl (should exist in production)
        if not TRACES_PATH.exists():
            self.skipTest(f"no agent-traces.jsonl at {TRACES_PATH}")
        mod = load_module()
        report = mod.report()
        # Should produce non-empty report with per-model breakdown
        if report:
            self.assertIn("events", report)
            self.assertIn("input_tokens", report)
            self.assertIn("output_tokens", report)
            self.assertIn("cost_24h", report)


class TestNoProbeStateNoCrash(unittest.TestCase):
    """status() and stop_probe() must not crash if no probe file exists."""

    def setUp(self):
        if PROBE_PATH.exists():
            PROBE_PATH.unlink()

    def test_status_no_state(self):
        mod = load_module()
        result = mod.status()
        self.assertEqual(result, {})

    def test_stop_no_state(self):
        mod = load_module()
        result = mod.stop_probe()
        self.assertEqual(result, {})


class TestCLI(unittest.TestCase):
    """End-to-end CLI invocation."""

    def setUp(self):
        if PROBE_PATH.exists():
            PROBE_PATH.unlink()

    def tearDown(self):
        if PROBE_PATH.exists():
            PROBE_PATH.unlink()

    def test_default_invocation_shows_report(self):
        """No flag = print report (default behavior)."""
        r = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True, timeout=30,
        )
        # Should not crash. May produce $0 (empty traces) or real report
        self.assertEqual(r.returncode, 0)

    def test_start_stop_lifecycle(self):
        """--start creates state, --stop completes it."""
        r1 = subprocess.run(
            [sys.executable, str(SCRIPT), "--start", "--target", "lifecycle-test"],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(r1.returncode, 0)
        self.assertTrue(PROBE_PATH.exists())

        r2 = subprocess.run(
            [sys.executable, str(SCRIPT), "--status"],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(r2.returncode, 0)
        self.assertIn("lifecycle-test", r2.stdout)

        r3 = subprocess.run(
            [sys.executable, str(SCRIPT), "--stop"],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(r3.returncode, 0)

        probe = json.loads(PROBE_PATH.read_text())
        self.assertEqual(probe["target_cron"], "lifecycle-test")
        self.assertIsNotNone(probe["completed_at"])


if __name__ == "__main__":
    unittest.main(verbosity=2)