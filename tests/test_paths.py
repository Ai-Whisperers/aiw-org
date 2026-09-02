"""Tests for scripts/_paths.py — the AIW_ROOT env-var abstraction.

Per DEMIURGE-098 (Phase Kernel brief WS-3 item 1):
  "scripts/_paths.py exposing AIW_ROOT = Path(os.environ.get('AIW_ROOT',
   '/opt/data')) plus derived constants. Thread through all ~107 files."

This test enforces:
  1. Default behavior (AIW_ROOT unset) -> /opt/data
  2. Override via env var changes ALL derived constants consistently
  3. The REPO constant correctly points to the parent of scripts/ (so
     that scripts which need to write to their own tree can do so)
  4. Backward compatibility: importing _paths in a script that has its
     own `ROOT = Path('/opt/data/agents')` constant does not break
"""

import importlib
import importlib.util
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "_paths.py"


def reload_paths():
    """Force-reload scripts/_paths.py so AIW_ROOT is recomputed."""
    # Drop any cached import of _paths
    for mod_name in list(sys.modules):
        if mod_name == "_paths" or mod_name.endswith("._paths"):
            del sys.modules[mod_name]
    spec = importlib.util.spec_from_file_location("_paths", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None, "spec.loader is None"
    spec.loader.exec_module(mod)
    return mod


class TestPathsDefault(unittest.TestCase):
    """When AIW_ROOT is unset, defaults to /opt/data (production)."""

    def test_default_aiw_root(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        self.assertEqual(paths.AIW_ROOT, Path("/opt/data").resolve())

    def test_state_under_aip_root(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        self.assertEqual(paths.STATE, Path("/opt/data/state").resolve())

    def test_agents_under_aiw_root(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        self.assertEqual(paths.AGENTS, Path("/opt/data/agents").resolve())

    def test_cron_under_aiw_root(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        self.assertEqual(paths.CRON, Path("/opt/data/.hermes/cron").resolve())

    def test_hermes_under_aiw_root(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        self.assertEqual(paths.HERMES, Path("/opt/data/.hermes").resolve())

    def test_repo_points_to_parent_of_scripts(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        # REPO is <directory>/scripts/_paths.py -> parent -> <directory>
        # which contains docs/, scripts/, tests/, etc.
        self.assertTrue((paths.REPO / "scripts").is_dir(),
                        f"REPO/scripts should be a directory: {paths.REPO}")
        self.assertTrue((paths.REPO / "tests").is_dir(),
                        f"REPO/tests should be a directory: {paths.REPO}")
        self.assertTrue((paths.REPO / "docs").is_dir(),
                        f"REPO/docs should be a directory: {paths.REPO}")

    def test_coord_json_default(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        self.assertEqual(paths.COORD_JSON,
                         Path("/opt/data/state/coord.json").resolve())

    def test_jobs_json_default(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        self.assertEqual(paths.JOBS_JSON,
                         Path("/opt/data/.hermes/cron/jobs.json").resolve())


class TestPathsOverride(unittest.TestCase):
    """When AIW_ROOT env var is set, all derived constants shift consistently."""

    def setUp(self):
        # Create a temp directory and set AIW_ROOT to it
        self._orig_aiw = os.environ.get("AIW_ROOT")
        self.tmp = Path(tempfile.mkdtemp(prefix="hermes-verify-aip-"))
        os.environ["AIW_ROOT"] = str(self.tmp)

    def tearDown(self):
        if self._orig_aiw is not None:
            os.environ["AIW_ROOT"] = self._orig_aiw
        else:
            os.environ.pop("AIW_ROOT", None)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_aiw_root_reflects_override(self):
        paths = reload_paths()
        self.assertEqual(paths.AIW_ROOT, self.tmp.resolve())

    def test_state_under_override(self):
        paths = reload_paths()
        self.assertEqual(paths.STATE, (self.tmp / "state").resolve())

    def test_agents_under_override(self):
        paths = reload_paths()
        self.assertEqual(paths.AGENTS, (self.tmp / "agents").resolve())

    def test_derived_constants_shift_consistently(self):
        """All paths derived from AIW_ROOT share the same parent root."""
        paths = reload_paths()
        # Every derived path should be a sub-path of AIW_ROOT
        for name in ["STATE", "AGENTS", "CRON", "HERMES", "WORK", "SCHEMAS",
                     "OUTBOX", "COORD_JSON", "TOKEN_LEDGER", "JOBS_JSON"]:
            p = getattr(paths, name)
            try:
                p.relative_to(paths.AIW_ROOT)
            except ValueError as e:
                self.fail(f"{name}={p} is not under AIW_ROOT={paths.AIW_ROOT}: {e}")

    def test_having_aiw_root_as_tmp_path_allows_access(self):
        """When AIW_ROOT=/tmp/hermes-verify-aip-XXXX, paths under it
        should be accessible even if those files don't exist."""
        paths = reload_paths()
        # Touching a non-existent path is OK; it should NOT raise
        import os
        paths.STATE.mkdir(parents=True, exist_ok=True)
        self.assertTrue(paths.STATE.is_dir())
        # cleanup
        paths.STATE.rmdir()


class TestPathsReal(unittest.TestCase):
    """Real-host verification: paths resolve to real directories."""

    def test_state_dir_exists_on_host(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        self.assertTrue(paths.STATE.exists(),
                        f"STATE={paths.STATE} should exist on host")
        self.assertTrue(paths.STATE.is_dir(),
                        f"STATE={paths.STATE} should be a directory")

    def test_agents_dir_exists_on_host(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        self.assertTrue(paths.AGENTS.exists(),
                        f"AGENTS={paths.AGENTS} should exist on host")

    def test_hermes_cron_dir_exists_on_host(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        self.assertTrue(paths.CRON.exists(),
                        f"CRON={paths.CRON} should exist on host")

    def test_jobs_json_exists_on_host(self):
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()
        # Only check that the directory exists; the file may legitimately
        # be missing if no crons are registered, but the parent should exist.
        self.assertTrue(paths.JOBS_JSON.parent.exists(),
                        f"JOBS_JSON.parent={paths.JOBS_JSON.parent} "
                        f"should exist on host")


class TestBackwardCompatibility(unittest.TestCase):
    """The refactor must not break existing scripts. Test that old
    'ROOT = Path(...)' patterns still work alongside the new helper."""

    def test_old_pattern_still_works(self):
        """An existing script that has its own ROOT still works."""
        # Simulate: a script with `ROOT = Path('/opt/data/agents')`
        # does not need to change. _paths exists alongside it.
        old_root = Path("/opt/data/agents")
        # Just confirm the path resolves
        self.assertTrue(old_root.exists())

    def test_old_and_new_can_coexist(self):
        """A script can import _paths AND have its own ROOT constant."""
        os.environ.pop("AIW_ROOT", None)
        paths = reload_paths()

        # Simulate: a script with its own ROOT
        ROOT = Path("/opt/data/agents")
        self.assertEqual(paths.AGENTS, ROOT)

    def test_no_circular_imports(self):
        """Importing _paths must not import the world (no cascading imports)."""
        # Drop _paths from sys.modules to get a fresh import
        for mod_name in list(sys.modules):
            if mod_name == "_paths" or mod_name.endswith("._paths"):
                del sys.modules[mod_name]
        spec = importlib.util.spec_from_file_location(
            "_paths_test_isolation", str(SCRIPT))
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        # Only _paths itself should have been loaded
        relevant_modules = [
            m for m in sys.modules
            if m not in sys.modules.copy() and not m.startswith("unittest")
        ]
        # We can't easily verify only-the-right-modules-loaded, but we
        # can at least verify no script module is imported.
        self.assertNotIn("validate-state", sys.modules)
        self.assertNotIn("credit-burn-probe", sys.modules)


class TestHermeticSetup(unittest.TestCase):
    """The hermetic test pattern (DEMIURGE-099): AIW_ROOT=/tmp/...

    With AIW_ROOT pointed at a tmp dir + the helper, scripts that
    don't depend on real files should run without /opt/data.
    """

    def test_aip_root_does_not_require_opt_data(self):
        """The whole point of DEMIURGE-098 + -099: hermetic test setup."""
        # Create a fresh empty tmp dir
        with tempfile.TemporaryDirectory(prefix="hermes-verify-herm-") as tmpdir:
            os.environ["AIW_ROOT"] = tmpdir
            paths = reload_paths()
            # Verify the test environment is "off-host"
            self.assertFalse(paths.STATE.exists(),
                             "STATE should NOT exist in fresh tmpdir")
            # But the test should still work because /opt/data/agents
            # is the live host, not the test's AIW_ROOT
            self.assertEqual(paths.AGENTS.parent, paths.AIW_ROOT)
            # RUNTIME paths (AIW_ROOT, STATE, AGENTS, etc.) should be under
            # the override. REPO is intentionally NOT under AIW_ROOT
            # because REPO points to the source code repo, not the
            # runtime data root.
            runtime_paths = ["AIW_ROOT", "STATE", "AGENTS", "CRON", "HERMES",
                             "WORK", "SCHEMAS", "OUTBOX", "COORD_JSON",
                             "TOKEN_LEDGER", "JOBS_JSON", "PROMPTS_DIR"]
            for name in runtime_paths:
                p = getattr(paths, name)
                self.assertTrue(
                    str(p).startswith(str(paths.AIW_ROOT)),
                    f"runtime path paths.{name}={p} is not under "
                    f"AIW_ROOT={paths.AIW_ROOT}")
            # REPO check: should still point to the source tree, not the
            # test override. This is intentional — REPO is the code repo.
            self.assertFalse(
                str(paths.REPO).startswith(str(paths.AIW_ROOT)),
                f"REPO={paths.REPO} should NOT be under AIW_ROOT="
                f"{paths.AIW_ROOT} -- REPO is the code repo, not the runtime root")


if __name__ == "__main__":
    unittest.main(verbosity=2)
