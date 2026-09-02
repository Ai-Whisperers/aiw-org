"""Tests for scripts/readme-counts.py — guards against README drift.

Per DEMIURGE-096 (Phase Kernel brief WS-2 item 2):
  "scripts/readme-counts.py --check, wired into CI, so README claims
   must match measurement."

Per R1 (Phase Kernel brief): no @unittest.skip decorators allowed.
"""
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "readme-counts.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "readme_counts_under_test", str(SCRIPT))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestScriptLoads(unittest.TestCase):
    def test_script_exists(self):
        self.assertTrue(SCRIPT.exists())

    def test_script_compiles(self):
        import py_compile
        py_compile.compile(str(SCRIPT), doraise=True)


class TestMeasurementFunctions(unittest.TestCase):
    """Each measurement function returns an int."""

    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()

    def test_count_charter_departments_returns_int(self):
        # Live host has 8 dirs (7 charter + board). Repo clone has its own
        # structure; if REPO is the live host it returns 8, otherwise 0+.
        from pathlib import Path as _P
        live = _P("/opt/data/agents")
        n = self.mod.count_charter_departments(REPO, live)
        self.assertIsInstance(n, int)
        self.assertGreaterEqual(n, 7,
                                "AIW has 7 charter departments + board = 8")

    def test_count_prompts_returns_int(self):
        n = self.mod.count_prompts(REPO)
        self.assertIsInstance(n, int)
        # Repo currently has 76 PROMPT.md files (per WS-1 close-out)
        self.assertGreaterEqual(n, 70)

    def test_count_prompt_monitors_returns_int(self):
        n = self.mod.count_prompt_monitors(REPO)
        self.assertIsInstance(n, int)
        self.assertGreaterEqual(n, 0)

    def test_count_cron_jobs_returns_int_or_zero(self):
        n = self.mod.count_cron_jobs()
        self.assertIsInstance(n, int)
        self.assertGreaterEqual(n, 0)

    def test_count_kpi_stacks_returns_int(self):
        n = self.mod.count_kpi_stacks()
        self.assertIsInstance(n, int)
        self.assertGreaterEqual(n, 0)

    def test_count_signal_routes_returns_int(self):
        n = self.mod.count_signal_routes()
        self.assertIsInstance(n, int)
        self.assertGreaterEqual(n, 0)

    def test_count_research_areas_returns_52(self):
        """The README claims 52; the script must agree."""
        n = self.mod.count_research_areas()
        # The 52 is the actual sum of numbered areas across all dept files
        self.assertEqual(n, 52,
                         f"Expected 52 research areas, got {n}")

    def test_measure_returns_dict(self):
        m = self.mod.measure()
        self.assertIsInstance(m, dict)
        # Required keys
        for key in ["Tier-1 charter departments",
                    "PROMPT.md files (all agents)",
                    "PROMPT-monitor.md files",
                    "Cron jobs (heartbeat)",
                    "KPI stacks (per dept)",
                    "Signal routes (per dept)",
                    "Research areas documented"]:
            self.assertIn(key, m)


class TestNormalizeCount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()

    def test_plain_int(self):
        self.assertEqual(self.mod.normalize_count("74"), 74)

    def test_plus_suffix(self):
        self.assertEqual(self.mod.normalize_count("86+"), 86)

    def test_with_descriptive_text(self):
        self.assertEqual(self.mod.normalize_count("309 files"), 309)

    def test_negative_returns_minus_one(self):
        self.assertEqual(self.mod.normalize_count("not a number"), -1)


class TestCheck(unittest.TestCase):
    """The check function returns (all_match, list of mismatches)."""

    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()

    def test_check_returns_tuple(self):
        ok, mismatches = self.mod.check(
            {"metric_a": 5, "metric_b": 10},
            {"metric_a": "5", "metric_b": "10"},
        )
        self.assertIsInstance(ok, bool)
        self.assertIsInstance(mismatches, list)
        self.assertTrue(ok)
        self.assertEqual(mismatches, [])

    def test_check_detects_mismatch(self):
        ok, mismatches = self.mod.check(
            {"metric_a": 5},
            {"metric_a": "10"},
        )
        self.assertFalse(ok)
        self.assertEqual(len(mismatches), 1)
        self.assertEqual(mismatches[0]["metric"], "metric_a")
        self.assertEqual(mismatches[0]["claimed"], "10")
        self.assertEqual(mismatches[0]["actual"], 5)

    def test_check_skips_metrics_not_in_measurements(self):
        """If README claims a metric we don't measure, skip silently."""
        ok, mismatches = self.mod.check(
            {"metric_a": 5},
            {"metric_a": "5", "metric_x": "999"},
        )
        self.assertTrue(ok)
        self.assertEqual(mismatches, [])


class TestCLIRun(unittest.TestCase):
    """End-to-end: run the script as a CLI."""

    def test_help_works(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            capture_output=True, text=True, timeout=10)
        self.assertEqual(r.returncode, 0)
        self.assertIn("--check", r.stdout)

    def test_check_returns_zero(self):
        """If README is in sync, --check exits 0."""
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"],
            capture_output=True, text=True, timeout=10)
        self.assertEqual(r.returncode, 0,
                         f"--check failed:\n{r.stdout}\n{r.stderr}")

    def test_check_detects_drift(self):
        """If README claims 999 PROMPT.md files but actual is 76, fail."""
        import os
        import re
        readme = REPO / "README.md"
        original = readme.read_text()
        # Inject a bogus claim
        mutated = re.sub(
            r"PROMPT\.md files \(all agents\)\*\* \| \*\*\d+\*\*",
            "PROMPT.md files (all agents)** | **999**", original)
        if mutated == original:
            self.skipTest("Couldn't mutate README; pattern not found")
        readme.write_text(mutated)
        try:
            # Run the script with REPO pointed at the (mutated) clone
            # so it reads the mutated README + counts clone PROMPT.md files
            env = os.environ.copy()
            env["README_COUNTS_REPO"] = str(REPO)
            r = subprocess.run(
                [sys.executable, str(SCRIPT), "--check"],
                capture_output=True, text=True, timeout=10, env=env,
            )
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("PROMPT.md", r.stdout)
            self.assertIn("999", r.stdout)
        finally:
            readme.write_text(original)


class TestNoSkipDecorators(unittest.TestCase):
    """R1 compliance: no @unittest.skip / @pytest.mark.skip decorators."""

    def test_no_skip_decorators(self):
        text = SCRIPT.read_text()
        # Allow comments mentioning skip
        lines = [l for l in text.split("\n")
                 if not l.strip().startswith("#")]
        for line in lines:
            self.assertNotIn("@unittest.skip", line,
                              f"R1 violation: {line!r}")
            self.assertNotIn("@pytest.mark.skip", line,
                              f"R1 violation: {line!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
