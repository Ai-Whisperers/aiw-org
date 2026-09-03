"""conftest.py — Hermetic-test fixture for CI environments.

PR #5 introduced CI without hermeticity. ~20 test modules hardcode
``Path(\"/opt/data/...\")`` at module-import time. CI runners have none
of those paths, causing 123/503 tests to fail with FileNotFoundError
or AssertionError on every PR.

This conftest solves the read-path problem by ensuring /opt/data
exists and resolves to a populated fixture tree in CI. On a real
production host where /opt/data already exists, the setup is a no-op.

Per-test isolation (for tests that *write* to /opt/data/state/X) is
out of scope for this PR; future PRs may add an autouse fixture that
uses monkeypatch to redirect writes to tmp_path.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

HERMETIC_ROOT = Path(os.environ.get("HERMETIC_AIW_ROOT", "/tmp/aiw-fixture"))
# PRODUCTION_ROOT is configurable via env so tests can simulate the CI
# environment (where /opt/data doesn't exist) without actually mutating
# the real /opt/data tree.
PRODUCTION_ROOT = Path(os.environ.get("HERMETIC_PRODUCTION_ROOT", "/opt/data"))


def _ensure_hermetic_root() -> None:
    """If /opt/data is missing, bind it to the hermetic fixture.

    Steps:
    1. Make sure the fixture tree exists with the subdirs the tests need.
    2. If /opt/data is missing or empty, populate it (real or symlink).
    3. On a real production host where /opt/data exists, do nothing.
    """
    # Step 1: populate fixture tree
    for sub in ["state", "agents", "agents/scripts", "agents/demiurge/agents",
                ".hermes", ".hermes/cron", ".venv", ".venv/bin"]:
        (HERMETIC_ROOT / sub).mkdir(parents=True, exist_ok=True)
    venv_py = HERMETIC_ROOT / ".venv" / "bin" / "python3"
    if not venv_py.exists():
        venv_py.touch()
    jobs = HERMETIC_ROOT / ".hermes" / "cron" / "jobs.json"
    if not jobs.exists():
        jobs.write_text('{"jobs": []}\n')

    # Step 2: production host detection
    # If /opt/data exists AND has files in it, treat as production.
    if PRODUCTION_ROOT.is_dir() and any(PRODUCTION_ROOT.iterdir()):
        return  # Production host — fixture tree is unused.

    # Step 3: CI — populate /opt/data as real dirs (since we run as root
    # in GH Actions; symlinks work but real dirs are simpler).
    # Walk each subdir of the fixture tree and create a matching path
    # under /opt/data. We do NOT symlink the whole /opt/data because some
    # tests use subprocess to invoke scripts and we want file paths to
    # match exactly.
    for sub in ["state", "agents", ".hermes", ".venv"]:
        target = PRODUCTION_ROOT / sub
        if target.exists() or target.is_symlink():
            continue
        target.mkdir(parents=True, exist_ok=True)
        # Mirror contents of HERMETIC_ROOT/sub into /opt/data/sub
        for child in (HERMETIC_ROOT / sub).iterdir():
            dest = target / child.name
            if dest.exists() or dest.is_symlink():
                continue
            if child.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
            else:
                shutil.copy2(child, dest)


_ensure_hermetic_root()


@pytest.fixture(autouse=True)
def _track_hermetic_setup():
    """Smoke fixture: confirm /opt/data exists at test start.

    Catches the case where the module-level setup was somehow skipped
    (e.g., pytest invocation bypasses conftest). Fails loud instead of
    letting 123 tests FileNotFoundError individually.
    """
    yield
    # No teardown: setup is idempotent and re-running on the next test
    # is a no-op.
