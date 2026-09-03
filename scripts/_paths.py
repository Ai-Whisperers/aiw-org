"""_paths.py — Centralized path resolution for AIW scripts and tests.

Per DEMIURGE-098 (Phase Kernel brief WS-3 item 1):
  "scripts/_paths.py exposing AIW_ROOT = Path(os.environ.get(
   'AIW_ROOT', '/opt/data')) plus derived constants. Thread through
   all ~107 files. Mechanical; commit in batches by directory."

Why it exists:
- 114 Python files hardcode '/opt/data' which breaks hermetic tests +
  portability across hosts.
- One module replaces hundreds of literal paths with semantic lookups.
- An AIW_ROOT env var lets tests run with a tmp_path + minimal fixtures,
  satisfying hermetic-test requirement (DEMIURGE-099).

Usage:
    from _paths import AIW_ROOT, STATE, AGENTS, CRON, WORK

    log = AIW_ROOT / "state" / "coord.json"        # /opt/data/state/coord.json
    log = STATE / "coord.json"                      # same path via derived const
    log = AGENTS / "01-operations" / "bizops-tracker" / "PROMPT.md"

Backward compatibility:
    When AIW_ROOT is unset or empty, defaults to '/opt/data' (production).
    This makes the refactor safe -- if any file accidentally falls through
    to the old literal, behavior is unchanged.

Migration:
- Old: ROOT = Path("/opt/data/agents")
- New: from _paths import AGENTS ; ROOT = AGENTS
- For files that have their own ROOT constants, see refactor notes.
"""

from __future__ import annotations

import os
from pathlib import Path

# Default to /opt/data when unset (production). When a test or hermetic
# environment sets AIW_ROOT=/some/other/path, all derived constants shift.
_AIW_ROOT = Path(os.environ.get("AIW_ROOT", "/opt/data")).resolve()

# Core directory roots. Each is derived from AIW_ROOT so a single env var
# repoints everything in a deployed instance. Paths are .resolve()d so
# /opt/data/agents (a symlink in CI) and /opt/data/agents (a real dir in
# production) compare equal in tests.
AIW_ROOT: Path = _AIW_ROOT
STATE: Path = (_AIW_ROOT / "state").resolve()
AGENTS: Path = (_AIW_ROOT / "agents").resolve()
CRON: Path = (_AIW_ROOT / ".hermes" / "cron").resolve()
WORK: Path = (_AIW_ROOT / "agents-v2" / "work").resolve()
HERMES: Path = (_AIW_ROOT / ".hermes").resolve()
SCHEMAS: Path = (_AIW_ROOT / "agents" / "schemas").resolve()
OUTBOX: Path = (_AIW_ROOT / "agents" / "outbox").resolve()

# Repo (where the code lives). Computed from this file's location.
# scripts/_paths.py is at <REPO>/scripts/_paths.py, so REPO = parent.
import sys as _sys
REPO: Path = Path(__file__).resolve().parent.parent

# Files commonly opened by scripts.
COORD_JSON: Path = STATE / "coord.json"
TOKEN_LEDGER: Path = STATE / "token-ledger.json"
JOBS_JSON: Path = HERMES / "cron" / "jobs.json"
PROMPTS_DIR: Path = AGENTS

def aiw_root() -> Path:
    """Return AIW_ROOT (re-reads env var each call; allows test overrides)."""
    return Path(os.environ.get("AIW_ROOT", "/opt/data")).resolve()


def set_aiw_root(path: str | Path) -> None:
    """Test helper: re-derive all paths after changing AIW_ROOT.

    Note: AIW_ROOT/STATE/AGENTS are computed at import time from the
    initial env var. To override, set os.environ['AIW_ROOT'] BEFORE
    importing _paths in a test, then re-import. This helper is kept for
    completeness; hermetic tests should set the env var up-front.
    """
    os.environ["AIW_ROOT"] = str(path)


__all__ = [
    "AIW_ROOT",
    "STATE",
    "AGENTS",
    "CRON",
    "WORK",
    "HERMES",
    "SCHEMAS",
    "OUTBOX",
    "REPO",
    "COORD_JSON",
    "TOKEN_LEDGER",
    "JOBS_JSON",
    "PROMPTS_DIR",
    "aiw_root",
    "set_aiw_root",
]
