"""Tests for scripts/thread-aiw-root.py — the WS-3 item 1 helper.

Per DEMIURGE-098 (Phase Kernel brief WS-3 item 1):
  "scripts/_paths.py exposing AIW_ROOT ... Thread through all ~107 files.
   Mechanical; commit in batches by directory."

This helper threads one file at a time. It MUST:
1. AST-detect Path() calls accurately (no false positives)
2. Replace literals with the matching _paths constant
3. Add a sys.path bootstrap preamble BEFORE the first non-import
   module-level line, AFTER the last import
4. PRESERVE every line of the file (no truncation)
5. Auto-rollback if pytest fails (R9 compliance)
6. Skip already-threaded files (idempotent)
7. Skip files with no applicable /opt/data/X Path() calls (no spurious
   imports)

Per R1 (Phase Kernel brief): "A skipped test is a failing test."
No @unittest.skip decorators allowed.
"""

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).parent.parent
SCRIPTS = REPO / "scripts"
HELPER = SCRIPTS / "thread-aiw-root.py"
LIBCODE = SCRIPTS / "_paths.py"


def load_helper():
    spec = importlib.util.spec_from_file_location("helper_under_test", str(HELPER))
    assert spec is not None, "failed to load spec"
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


SAMPLE_FILE = '''#!/usr/bin/env python3
"""agent-tracer.py — Sample file for testing."""
import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

STATE_DIR = Path("/opt/data/state")
TRACES_FILE = STATE_DIR / "agent-traces.jsonl"


def helper():
    """Function."""
    return 0


def main():
    pass


if __name__ == "__main__":
    main()
'''


def make_tmp_file(tmpdir: Path, content: str = None) -> Path:
    """Write SAMPLE_FILE to a tmp path."""
    content = content if content is not None else SAMPLE_FILE
    p = tmpdir / "test_script.py"
    p.write_text(content)
    return p


class TestScriptImports(unittest.TestCase):
    def test_helper_exists(self):
        self.assertTrue(HELPER.exists(), f"missing: {HELPER}")

    def test_helper_compiles(self):
        import py_compile
        py_compile.compile(str(HELPER), doraise=True)

    def _load_helper_safely(self):
        mod = load_helper()
        return mod

    def test_helper_loads(self):
        mod = self._load_helper_safely()
        self.assertTrue(callable(mod.detect))
        self.assertTrue(callable(mod.apply_to_source))
        self.assertTrue(callable(mod.ensure_preamble))


class TestEnsurePreamblePreservesAllLines(unittest.TestCase):
    """CRITICAL: ensure_preamble must preserve every line of the file.
    Per R9: never execute a wrong task to completion. The previous v1 of
    this helper had a bug where it truncated files to ~21 lines. These
    tests prevent that regression.
    """

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="thread-helper-"))
        self.target = make_tmp_file(self.tmpdir)
        self.mod = load_helper()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_line_count_preserved(self):
        original = self.target.read_text()
        original_lines = original.splitlines()
        result, _ = self.mod.ensure_preamble(original, "AIW_ROOT, STATE")
        result_lines = result.splitlines()
        self.assertEqual(len(result_lines), len(original_lines) + 10,
                         f"expected {len(original_lines) + 10} lines (original + "
                         f"10-line preamble (1 leading blank + 8 content + 1 trailing blank)), got {len(result_lines)}: "
                         f"DIFF={len(result_lines) - len(original_lines):+d}")

    def test_no_truncation(self):
        original = self.target.read_text()
        original_bytes = len(original)
        result, _ = self.mod.ensure_preamble(original, "AIW_ROOT, STATE")
        self.assertGreater(len(result), original_bytes,
                            "result should be LONGER (preamble added) -- if it's "
                            "shorter, the file was truncated")

    def test_every_marker_line_present_in_result(self):
        original = self.target.read_text()
        result, _ = self.mod.ensure_preamble(original, "AIW_ROOT, STATE")
        # All non-preamble content from original must be present in result
        # (the preamble is extra content; non-preamble must be preserved)
        original_lines = original.splitlines()
        result_lines = result.splitlines()
        # Take a unique line from each "section" of the original
        markers = [
            '"""agent-tracer.py — Sample file for testing."""',
            "import json",
            "import os",
            "from pathlib import Path",
            "STATE_DIR = Path(\"/opt/data/state\")",
            'TRACES_FILE = STATE_DIR / "agent-traces.jsonl"',
            "def helper():",
            "def main():",
            "main()",
        ]
        for m in markers:
            self.assertIn(m, result, f"marker line lost from result: {m!r}")

    def test_docstring_lines_preserved(self):
        original = self.target.read_text()
        result, _ = self.mod.ensure_preamble(original, "AIW_ROOT, STATE")
        # The docstring body line "Function." must be preserved
        self.assertIn('"""Function."""', result,
                      "docstring body line lost")

    def test_indented_lines_preserved(self):
        original = self.target.read_text()
        result, _ = self.mod.ensure_preamble(original, "AIW_ROOT, STATE")
        # Indented function body should be preserved (preserves leading spaces)
        self.assertIn('    return 0', result,
                      "indented function-body line lost")

    def test_preamble_appears_exactly_once(self):
        original = self.target.read_text()
        result, _ = self.mod.ensure_preamble(original, "AIW_ROOT, STATE")
        count = result.count("# --- AIW_ROOT path bootstrap (DEMIURGE-098) ---")
        self.assertEqual(count, 1, f"preamble count {count} != 1")

    def test_preamble_positioned_correctly(self):
        """Preamble should be AFTER the imports and BEFORE the first
        non-import module-level code.
        """
        original = self.target.read_text()
        result, _ = self.mod.ensure_preamble(original, "AIW_ROOT, STATE")
        lines = result.splitlines()
        # Find preamble position
        preamble_start = next(
            i for i, ln in enumerate(lines)
            if "AIW_ROOT path bootstrap" in ln
        )
        preamble_end = preamble_start + 8  # 9 lines of preamble
        # Find LAST import line before the preamble (preamble should be
        # right after it).
        last_import_idx = -1
        for i in range(preamble_start):
            ln = lines[i]
            s = ln.lstrip()
            if s.startswith(("import ", "from ")):
                last_import_idx = i
        self.assertGreater(last_import_idx, -1,
                            f"no module-level import found before preamble "
                            f"(preamble at line {preamble_start+1})")
        self.assertEqual(preamble_start, last_import_idx + 2,
                         f"preamble (line {preamble_start+1}) should be exactly "
                         f"one line after the last import (line {last_import_idx+1}), "
                         f"with one blank line between")
        # Verify the from _paths import line is between preamble_start and preamble_end
        for i in range(preamble_start, preamble_end + 1):
            if "from _paths import" in lines[i]:
                break
        else:
            self.fail(f"'from _paths import' not found in preamble (lines "
                      f"{preamble_start+1} to {preamble_end+1}):\n"
                      + "\n".join(f"  L{j+1}: {ln!r}"
                                    for j, ln in
                                    enumerate(lines[preamble_start:preamble_end+1],
                                              preamble_start)))

    def test_already_threaded_returns_content_unchanged(self):
        """File with the preamble already present: return unchanged.
        (The helper should detect this and not insert a duplicate.)
        """
        # Use a content string that has the full preamble present.
        original_with_preamble = SAMPLE_FILE + (

            "\n# --- AIW_ROOT path bootstrap (DEMIURGE-098) ---\n"
            "import sys as _sys_bootstrap_098\n"
            "from pathlib import Path as _Path_bootstrap_098\n"
            "_PY_PATHS_ROOT = _Path_bootstrap_098(__file__).resolve().parent.parent\n"
            "if str(_PY_PATHS_ROOT) not in _sys_bootstrap_098.path:\n"
            "    _sys_bootstrap_098.path.insert(0, str(_PY_PATHS_ROOT))\n"
            "from _paths import AIW_ROOT, STATE\n"
            "# --- end bootstrap ---\n"
        )
        result, had_existing = self.mod.ensure_preamble(
            original_with_preamble, "AIW_ROOT, STATE")
        self.assertTrue(had_existing, "should detect already-threaded")
        self.assertEqual(result, original_with_preamble,
                         "should return unchanged when already threaded")

    def test_no_imports_returns_unchanged(self):
        """File with no imports: return unchanged rather than corrupt."""
        no_imports = '''#!/usr/bin/env python3
"""Docstring only."""
FOO = "bar"
'''
        result, _ = self.mod.ensure_preamble(no_imports, "AIW_ROOT, STATE")
        self.assertEqual(result, no_imports,
                         "no-imports file should return unchanged")

    def test_shebangs_skipped(self):
        """Shebang line (#!/usr/bin/env python3) must be SKIPPED, not
        treated as a non-import module-level line. (Bug fixed in this PR.)
        """
        with_shebang = '''#!/usr/bin/env python3
"""Has shebang."""
import os

FOO = "bar"
'''
        result, _ = self.mod.ensure_preamble(
            with_shebang, "AIW_ROOT")
        # Preamble should be AFTER import os, BEFORE FOO = "bar"
        lines = result.splitlines()
        preamble_idx = next(
            i for i, ln in enumerate(lines) if "AIW_ROOT path bootstrap" in ln)
        foo_idx = next(
            i for i, ln in enumerate(lines) if ln.startswith("FOO"))
        import_idx = next(
            i for i, ln in enumerate(lines)
            if ln.lstrip().startswith(("import", "from"))
            and ("import" in ln[:8] or "from" in ln[:8])
        )
        self.assertGreater(preamble_idx, import_idx - 1,
                            "preamble should be after imports")
        self.assertLess(preamble_idx, foo_idx,
                        "preamble should be before next module-level code")


class TestApplyToSourcePreservesAllLines(unittest.TestCase):
    """apply_to_source must preserve line count exactly."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="thread-apply-"))
        self.target = make_tmp_file(self.tmpdir)
        self.mod = load_helper()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_apply_preserves_line_count(self):
        original = self.target.read_text()
        original_lines = original.splitlines()
        items = [
            (8, 'Path("/opt/data/state")', "STATE", "Path_arg"),
        ]
        result = self.mod.apply_to_source(original, items)
        result_lines = result.splitlines()
        self.assertEqual(len(result_lines), len(original_lines),
                         f"apply_to_source changed line count: "
                         f"{len(original_lines)} -> {len(result_lines)}")

    def test_apply_replaces_clearly(self):
        original = self.target.read_text()
        items = [
            (8, 'Path("/opt/data/state")', "STATE", "Path_arg"),
        ]
        result = self.mod.apply_to_source(original, items)
        self.assertIn("STATE_DIR = STATE", result,
                      "Path(\"/opt/data/state\") was not replaced")
        self.assertNotIn('Path("/opt/data/state")', result,
                         "literal still in result")


class TestFullThreadingWorks(unittest.TestCase):
    """End-to-end test: ensure_preamble + apply_to_source compose
    correctly to thread a single file.
    """

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="thread-e2e-"))
        self.target = make_tmp_file(self.tmpdir)
        self.mod = load_helper()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_e2e_preserves_lines(self):
        original = self.target.read_text()
        original_lines = original.splitlines()
        # Apply both transformations
        items = [
            (8, 'Path("/opt/data/state")', "STATE", "Path_arg"),
        ]
        post_apply = self.mod.apply_to_source(original, items)
        final, _ = self.mod.ensure_preamble(post_apply, "AIW_ROOT, STATE")
        final_lines = final.splitlines()
        # Should be original + 9 preamble lines
        self.assertEqual(len(final_lines), len(original_lines) + 10,
                         f"line count mismatch: original={len(original_lines)}, "
                         f"final={len(final_lines)} (should be +9 for preamble)")
        # Every original line still present (after apply_to_source
        # replaces Path() with the constant name)
        for ln in original_lines:
            # apply_to_source does a string.replace on the WHOLE line
            expected = ln.replace('Path("/opt/data/state")', "STATE")
            self.assertIn(expected, final,
                          f"line lost: {expected!r} (from original: {ln!r})")


if __name__ == "__main__":
    unittest.main(verbosity=2)
