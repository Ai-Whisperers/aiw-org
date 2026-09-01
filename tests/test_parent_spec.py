"""test_parent_spec.py — Tests for scripts/agent-context-loader.py.

Phase 9 R3 / Tier B8. Validates that the parent_spec audit correctly
identifies missing/incorrect parent_spec and that the cache resolves.
"""
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

import pytest

REPO = Path("/opt/data/agents")
SCRIPT = REPO / "scripts" / "agent-context-loader.py"
FIX_SCRIPT = REPO / "scripts" / "fix-parent-spec.py"


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_audit_after_fix():
    """After the fix-parent-spec.py run, all 47 PROMPT.md files are correct."""
    mod = _load_module(SCRIPT, "loader")
    # Use the real audit function (returns 0 if all correct)
    rc = mod.audit()
    assert rc == 0, "Audit should report 0 incorrect/missing parent_spec"


def test_infer_parent_spec_known_dept():
    """infer_parent_spec returns expected values for known dept prefixes."""
    mod = _load_module(SCRIPT, "loader")
    assert mod.infer_parent_spec(REPO / "04-engineering" / "test" / "PROMPT.md") == "departments/04-engineering-delivery.md"
    assert mod.infer_parent_spec(REPO / "06-people-culture" / "test" / "PROMPT.md") == "departments/06-people-culture.md"
    assert mod.infer_parent_spec(REPO / "demiurge" / "agents" / "test" / "PROMPT.md") == "constitution/ORG-AGENTS.md"


def test_infer_parent_spec_unknown_dept():
    """Unknown dept prefix falls back to ORG-AGENTS.md."""
    mod = _load_module(SCRIPT, "loader")
    result = mod.infer_parent_spec(REPO / "99-unknown" / "test" / "PROMPT.md")
    assert result == "constitution/ORG-AGENTS.md"


def test_cache_written():
    """cache command writes /opt/data/state/agent-parent-spec-cache.json."""
    mod = _load_module(SCRIPT, "loader")
    rc = mod.cache()
    assert rc == 0
    cache_path = Path("/opt/data/state/agent-parent-spec-cache.json")
    assert cache_path.exists()
    data = json.loads(cache_path.read_text())
    assert len(data) >= 47  # at least 47 agents
    # Spot-check known agents
    assert "04-engineering/ai-safety-engineer-30min/PROMPT.md" in data


def test_validate_passes():
    """After audit + cache, validate finds 0 missing spec files."""
    mod = _load_module(SCRIPT, "loader")
    rc = mod.validate()
    assert rc == 0


def test_resolve_known_agent():
    """resolve returns the correct parent_spec for a known agent."""
    mod = _load_module(SCRIPT, "loader")
    rc = mod.resolve("04-engineering/ai-safety-engineer-30min/PROMPT.md")
    assert rc == 0