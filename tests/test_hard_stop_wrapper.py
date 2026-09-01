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
    """Verify _log_check writes NDJSON (Phase 28 fix for race condition)."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "audit.ndjson"
        orig = mod.LOG_PATH
        setattr(mod, "LOG_PATH", log_path)
        try:
            mod._log_check("test-agent", "foo_action", "ai-agent", True)
            mod._log_check("test-agent", "bar_action", "ai-agent", False)
            assert log_path.exists()
            # NDJSON: one JSON per line
            lines = log_path.read_text().strip().split("\n")
            assert len(lines) == 2
            entry1 = json.loads(lines[0])
            entry2 = json.loads(lines[1])
            assert entry1["action"] == "foo_action"
            assert entry1["allowed"] is True
            assert entry2["allowed"] is False
        finally:
            setattr(mod, "LOG_PATH", orig)


def test_audit_log_concurrent_writes_safe():
    """Phase 28: NDJSON append-only means concurrent writes don't corrupt."""
    import threading
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "audit.ndjson"
        orig = mod.LOG_PATH
        setattr(mod, "LOG_PATH", log_path)
        try:
            threads = []
            for i in range(10):
                t = threading.Thread(
                    target=lambda j=[i]: [mod._log_check(f"agent-{j[0]}", "act", "ai-agent", True) for _ in range(5)]
                )
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            lines = log_path.read_text().strip().split("\n")
            assert len(lines) == 50
            # All lines must parse as valid JSON
            for line in lines:
                json.loads(line)
        finally:
            setattr(mod, "LOG_PATH", orig)


def test_audit_log_rotates_at_50mb():
    """Phase 28: rotate log when it exceeds 50MB."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "audit.ndjson"
        log_path.write_text("x" * (51 * 1024 * 1024))
        orig = mod.LOG_PATH
        setattr(mod, "LOG_PATH", log_path)
        try:
            mod._log_check("test", "action", "ai-agent", True)
            files = list(Path(tmp).iterdir())
            assert any(f.name.startswith("audit.audit-") for f in files), f"No rotated file. Files: {[f.name for f in files]}"
            assert log_path.exists()
        finally:
            setattr(mod, "LOG_PATH", orig)


def test_validate_prompt_real_file():
    """Validate an actual existing PROMPT that has hard_stops."""
    mod = load_module()
    valid, errors = mod.validate_prompt("01-operations/founder-bandwidth-watchdog")
    assert valid, f"expected valid, got errors: {errors}"


def test_check_action_wildcard_allows_all():
    """Whitelist with action='*' allows everything."""
    mod = load_module()
    stops = [{"action": "*", "mode": "whitelist"}]
    # Wildcard overrides whitelist — all allowed
    assert mod.check_action("deploy_prod", "ai-agent", stops) is True
    assert mod.check_action("anything", "ai-agent", stops) is True


def test_check_action_whitelist_mode():
    """Whitelist mode: only listed actions allowed."""
    mod = load_module()
    stops = [
        {"mode": "whitelist"},
        {"action": "read_state"},
        {"action": "write_state"},
    ]
    # Listed actions allowed
    assert mod.check_action("read_state", "ai-agent", stops) is True
    assert mod.check_action("write_state", "ai-agent", stops) is True
    # Unlisted actions blocked (default-deny)
    assert mod.check_action("deploy_prod", "ai-agent", stops) is False
    assert mod.check_action("git_push", "ai-agent", stops) is False


def test_check_action_whitelist_with_mode_marker():
    """Detection: 'mode: whitelist' marker activates whitelist mode."""
    mod = load_module()
    stops = [
        {"mode": "whitelist"},
        {"action": "merge_pr"},
        {"action": "comment_on_pr"},
    ]
    # Listed actions allowed
    assert mod.check_action("merge_pr", "ai-agent", stops) is True
    # Unlisted blocked
    assert mod.check_action("deploy_prod", "ai-agent", stops) is False
    assert mod.check_action("delete_resource", "ai-agent", stops) is False


def test_check_action_blacklist_still_works():
    """Verify blacklist mode unchanged after whitelist addition."""
    mod = load_module()
    stops = [
        {"action": "deploy_prod", "require_approval": True, "approved_human": "ivan"},
        {"action": "force_push", "require_approval": True, "approved_human": "ivan"},
    ]
    # Blocked for ai-agent
    assert mod.check_action("deploy_prod", "ai-agent", stops) is False
    assert mod.check_action("force_push", "ai-agent", stops) is False
    # Allowed for ivan
    assert mod.check_action("deploy_prod", "ivan", stops) is True
    # Unrelated action allowed by default (blacklist)
    assert mod.check_action("read_state", "ai-agent", stops) is True


def test_check_action_empty_hard_stops():
    """Empty hard_stops allows all actions (default blacklist behavior)."""
    mod = load_module()
    assert mod.check_action("deploy_prod", "ai-agent", []) is True


if __name__ == "__main__":
    test_check_action_no_rules_allows()
    test_check_action_require_approval_blocks_non_approved()
    test_check_action_any_of_approved()
    test_check_action_list_approved()
    test_check_action_wildcard_allows_all()
    test_check_action_whitelist_mode()
    test_check_action_whitelist_with_mode_marker()
    test_check_action_blacklist_still_works()
    test_check_action_empty_hard_stops()
    test_load_hard_stops_frontmatter()
    test_load_hard_stops_legacy_double_block()
    test_load_hard_stops_bare_block()
    test_load_hard_stops_missing()
    test_audit_log_writes_entry()
    test_audit_log_concurrent_writes_safe()
    test_audit_log_rotates_at_50mb()
    test_validate_prompt_real_file()
    print("\nAll hard-stop-wrapper tests passed!")
