"""Tests for token-cap.py — guards the disabled state.

Per WS-2 item 3 of the Phase Kernel brief: a token-budget gate that
'always fires' due to a unit mismatch is worse than no gate. We disable
it. This test prevents accidental re-enablement.

The replacement (gated-token-check.py) will live in a separate commit.
Until then, the cron should:
  - exit 0 (success, not error)
  - print a clear advisory message about its disabled state
  - NOT write any fake alert to coord.json
"""
import importlib.util
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


class TestDisabledContract(unittest.TestCase):
    """The CRITICAL property: disabled state must be exit 0, not silent."""

    def test_cli_exits_zero(self):
        """The cron entry 'aiw-token-cap-daily' must succeed, not error."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0,
                         f"Disabled script must exit 0, got {result.returncode}\n"
                         f"stderr: {result.stderr[:200]}")

    def test_advisory_message_present(self):
        """Operators must be able to tell from cron output that this is
        intentional, not a real budget alert."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True, timeout=10,
        )
        self.assertIn("DISABLED", result.stdout,
                      "Output must announce the disabled state")
        self.assertIn("unit-mismatch", result.stdout,
                      "Output must explain why (unit mismatch with ledger)")
        self.assertIn("fb2b81f", result.stdout,
                      "Output must cite the audit commit")

    def test_does_not_write_coord_alert(self):
        """The disabled script must not append fake alerts to coord.json.

        Pre-fix token-cap wrote to coord.json:decisions_for_ivan on
        every run. The replacement must NOT do this until it has real
        data to alert on.
        """
        coord = Path("/opt/data/state/coord.json")
        if not coord.exists():
            self.skipTest("coord.json not present in test environment")

        # Snapshot decisions_for_ivan length before
        import json
        before = json.loads(coord.read_text())
        before_count = len(before.get("decisions_for_ivan", []))

        # Run the disabled script 5 times -- each would have appended
        # to the queue under the broken behavior.
        for _ in range(5):
            subprocess.run([sys.executable, str(SCRIPT)],
                          capture_output=True, timeout=10)
        after = json.loads(coord.read_text())
        after_count = len(after.get("decisions_for_ivan", []))

        # Allow other crons to write between runs; assert NO token-cap
        # entries specifically added.
        new_entries = after.get("decisions_for_ivan", [])[before_count:]
        token_cap_entries = [
            e for e in new_entries
            if "token-cap" in str(e.get("source", ""))
        ]
        self.assertEqual(len(token_cap_entries), 0,
                         f"Disabled token-cap wrote {len(token_cap_entries)} "
                         f"queue entries; expected 0")


class TestNoUnintendedSideEffects(unittest.TestCase):
    """Static checks: the disabled file does not pull in the broken imports."""

    def test_does_not_import_json_datetime(self):
        """Old token-cap imported json/datetime to do its broken work.
        The replacement must not import those (no work to do)."""
        content = SCRIPT.read_text()
        # It SHOULD import sys (to call sys.exit), but not json or datetime
        self.assertNotIn("import json", content,
                         "Disabled script should not import json")
        # Reading 'datetime' (not 'date' or 'time') catches the bad import
        self.assertFalse(
            any(line.strip().startswith("from datetime")
                for line in content.splitlines()),
            "Disabled script should not import from datetime"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
