"""Tests for patterns/hard-stop-wrapper.py.

Verifies:
- check_action correctly blocks/allows based on hard_stops
- load_hard_stops extracts from frontmatter (legacy + new) and bare blocks
- audit log records every check
- role matching supports 'ivan+kiki' (any-of) and list formats
"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "patterns" / "hard-stop-wrapper.py"


def load_module():
    spec = importlib.util.spec_from_file_location("hsw", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_check_action_no_rules_allows():
    mod = load_module()
    assert mod.check_action("any_action", "ai-agent", []) is True


def test_check_action_require_approval_blocks_non_approved():
    mod = load_module()
    hard_stops = [{"action": "force_push", "require_approval": True, "approved_human": "ivan"}]
    assert mod.check_action("force_push", "ai-agent", hard_stops) is False
    assert mod.check_action("force_push", "ivan", hard_stops) is True


def test_check_action_any_of_approved():
    """'ivan+kiki' means any-of: ivan OR kiki."""
    mod = load_module()
    hard_stops = [{"action": "force_push", "require_approval": True, "approved_human": "ivan+kiki"}]
    assert mod.check_action("force_push", "ai-agent", hard_stops) is False
    assert mod.check_action("force_push", "ivan", hard_stops) is True
    assert mod.check_action("force_push", "kiki", hard_stops) is True


def test_check_action_list_approved():
    mod = load_module()
    hard_stops = [{"action": "force_push", "require_approval": True, "approved_human": ["ivan", "kiki"]}]
    assert mod.check_action("force_push", "ai-agent", hard_stops) is False
    assert mod.check_action("force_push", "ivan", hard_stops) is True


def test_load_hard_stops_frontmatter():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "PROMPT.md"
        p.write_text("""---
name: test-agent
version: 0.1.0
hard_stops:
  - action: foo
    require_approval: true
    approved_human: ivan
---

# Test PROMPT
""")
        hs = mod.load_hard_stops(p)
        assert len(hs) == 1
        assert hs[0]["action"] == "foo"


def test_load_hard_stops_legacy_double_block():
    """Test legacy format used in 3 PROMPTs (second --- block contains hard_stops)."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "PROMPT.md"
        p.write_text("""---
name: founder-bandwidth-watchdog
version: 0.2.0
owner: ai-ops-coordinator
---

name: founder-bandwidth-watchdog
version: 0.1.0
schedule: "0 18 * * 0"
hard_stops:
  - action: disable_hardstop
    require_approval: true
    approved_human: ivan+kiki
""")
        hs = mod.load_hard_stops(p)
        assert len(hs) == 1
        assert hs[0]["action"] == "disable_hardstop"
        assert hs[0]["approved_human"] == "ivan+kiki"


def test_load_hard_stops_bare_block():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "PROMPT.md"
        p.write_text("""---
name: test
---
hard_stops:
  - action: foo
    require_approval: false
""")
        hs = mod.load_hard_stops(p)
        assert len(hs) == 1
        assert hs[0]["action"] == "foo"


def test_load_hard_stops_missing():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "PROMPT.md"
        p.write_text("""---
name: test
---
# No hard_stops here
""")
        hs = mod.load_hard_stops(p)
        assert hs == []


def test_audit_log_writes_entry():
    """Verify _log_check writes to /opt/data/state/hard-stop-audit.json (use temp override)."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        # Override LOG_PATH
        log_path = Path(tmp) / "audit.json"
        orig = mod.LOG_PATH
        setattr(mod, "LOG_PATH", log_path)
        try:
            mod._log_check("test-agent", "foo_action", "ai-agent", True)
            mod._log_check("test-agent", "bar_action", "ai-agent", False)
            assert log_path.exists()
            log = json.loads(log_path.read_text())
            assert len(log) == 2
            assert log[0]["action"] == "foo_action"
            assert log[0]["allowed"] is True
            assert log[1]["allowed"] is False
        finally:
            mod.LOG_PATH = orig


def test_audit_log_caps_at_1000():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "audit.json"
        orig = mod.LOG_PATH
        setattr(mod, "LOG_PATH", log_path)
        try:
            for i in range(1500):
                mod._log_check("test-agent", f"action_{i}", "ai-agent", True)
            log = json.loads(log_path.read_text())
            assert len(log) == 1000
            # Last entry should be action_1499
            assert log[-1]["action"] == "action_1499"
        finally:
            mod.LOG_PATH = orig


def test_validate_prompt_real_file():
    """Validate an actual existing PROMPT that has hard_stops."""
    mod = load_module()
    valid, errors = mod.validate_prompt("01-operations/founder-bandwidth-watchdog")
    assert valid, f"expected valid, got errors: {errors}"


if __name__ == "__main__":
    test_check_action_no_rules_allows()
    test_check_action_require_approval_blocks_non_approved()
    test_check_action_any_of_approved()
    test_check_action_list_approved()
    test_load_hard_stops_frontmatter()
    test_load_hard_stops_legacy_double_block()
    test_load_hard_stops_bare_block()
    test_load_hard_stops_missing()
    test_audit_log_writes_entry()
    test_audit_log_caps_at_1000()
    test_validate_prompt_real_file()
    print("\nAll hard-stop-wrapper tests passed!")
