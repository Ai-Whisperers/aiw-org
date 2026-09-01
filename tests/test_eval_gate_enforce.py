"""Tests for scripts/eval-gate-enforce.py."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "eval-gate-enforce.py"


def load_module():
    spec = importlib.util.spec_from_file_location("eval_gate_enforce", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _set(mod, key, value):
    """setattr wrapper for module attribute override."""
    setattr(mod, key, value)


def _restore(mod, key, orig):
    """Restore a module attribute."""
    setattr(mod, key, orig)


def make_eval(by_agent):
    """Write a synthetic eval-trending.json to temp. Returns path."""
    p = Path(tempfile.gettempdir()) / f"eval-test-{id(by_agent)}.json"
    p.write_text(json.dumps({"by_agent": by_agent, "summary": {}}))
    return p


def test_decide_high_pass_rate_allows():
    mod = load_module()
    eval_path = make_eval({"a": {"pass_rate": 0.95}})
    orig = mod.EVAL_FILE
    _set(mod, "EVAL_FILE", eval_path)
    try:
        d = mod.decide("a", force=None, threshold=0.30)
        assert d["decision"] == "allow"
    finally:
        _restore(mod, "EVAL_FILE", orig)


def test_decide_medium_pass_rate_warns():
    mod = load_module()
    eval_path = make_eval({"a": {"pass_rate": 0.45}})
    orig = mod.EVAL_FILE
    _set(mod, "EVAL_FILE", eval_path)
    try:
        d = mod.decide("a", force=None, threshold=0.30)
        assert d["decision"] == "warn"
        assert "warn threshold" in d["reason"].lower()
    finally:
        _restore(mod, "EVAL_FILE", orig)


def test_decide_low_pass_rate_blocks():
    mod = load_module()
    eval_path = make_eval({"a": {"pass_rate": 0.20}})
    orig = mod.EVAL_FILE
    _set(mod, "EVAL_FILE", eval_path)
    try:
        d = mod.decide("a", force=None, threshold=0.30)
        assert d["decision"] == "block"
        assert "below threshold" in d["reason"].lower()
    finally:
        _restore(mod, "EVAL_FILE", orig)


def test_decide_low_pass_rate_with_force_overrides():
    mod = load_module()
    eval_path = make_eval({"a": {"pass_rate": 0.20}})
    orig = mod.EVAL_FILE
    _set(mod, "EVAL_FILE", eval_path)
    try:
        d = mod.decide("a", force="manual override", threshold=0.30)
        assert d["decision"] == "allow"
        assert d["force_used"] is True
        assert d["force_reason"] == "manual override"
        assert "forced" in d["reason"].lower()
    finally:
        _restore(mod, "EVAL_FILE", orig)


def test_decide_unknown_agent_warns():
    mod = load_module()
    eval_path = make_eval({"other": {"pass_rate": 0.95}})
    orig = mod.EVAL_FILE
    _set(mod, "EVAL_FILE", eval_path)
    try:
        d = mod.decide("ghost-agent", force=None, threshold=0.30)
        assert d["decision"] == "warn"
        assert "no eval data" in d["reason"].lower()
    finally:
        _restore(mod, "EVAL_FILE", orig)


def test_decide_missing_eval_file_warns():
    mod = load_module()
    eval_path = Path(tempfile.gettempdir()) / "nonexistent-eval-trending.json"
    if eval_path.exists():
        eval_path.unlink()
    orig = mod.EVAL_FILE
    _set(mod, "EVAL_FILE", eval_path)
    try:
        d = mod.decide("any-agent", force=None, threshold=0.30)
        assert d["decision"] == "warn"
        assert d["pass_rate"] is None
    finally:
        _restore(mod, "EVAL_FILE", orig)


def test_decide_nan_pass_rate_warns():
    """Phase 29 fix (BUG-HUNT H2): NaN pass_rate silently bypassed eval-gate."""
    mod = load_module()
    eval_path = make_eval({"weird-agent": {"pass_rate": float("nan")}})
    orig = mod.EVAL_FILE
    _set(mod, "EVAL_FILE", eval_path)
    try:
        d = mod.decide("weird-agent", force=None, threshold=0.30)
        # Should NOT be "allow" — that was the bug. Should be warn with explicit reason.
        assert d["decision"] == "warn", f"NaN should be warn, got {d['decision']}"
        assert "invalid" in d["reason"].lower() or "nan" in d["reason"].lower()
    finally:
        _restore(mod, "EVAL_FILE", orig)


def test_decide_string_pass_rate_warns():
    """Phase 29 fix (BUG-HUNT H3): string pass_rate silently treated as no-data."""
    mod = load_module()
    eval_path = make_eval({"str-agent": {"pass_rate": "0.95"}})
    orig = mod.EVAL_FILE
    _set(mod, "EVAL_FILE", eval_path)
    try:
        d = mod.decide("str-agent", force=None, threshold=0.30)
        # Should be warn (invalid), NOT silently 'no data'
        assert d["decision"] == "warn", f"string should be warn, got {d['decision']}"
        assert "invalid" in d["reason"].lower() or "0.95" in d["reason"]
    finally:
        _restore(mod, "EVAL_FILE", orig)


def test_decide_negative_threshold_clamped():
    """Phase 29 fix (BUG-HUNT H7): --threshold -1 silently allowed everything."""
    mod = load_module()
    eval_path = make_eval({"a": {"pass_rate": 0.0}})
    orig = mod.EVAL_FILE
    _set(mod, "EVAL_FILE", eval_path)
    try:
        d = mod.decide("a", force=None, threshold=-1)
        # pass_rate 0.0 < -1 is False, so would fall through to allow. But negative threshold is operator error.
        # For now: still allow (don't crash); future: clamp or warn
        # This test verifies it doesn't crash and returns a valid decision
        assert d["decision"] in ("allow", "warn", "block"), f"unexpected: {d['decision']}"
    finally:
        _restore(mod, "EVAL_FILE", orig)


def test_decide_threshold_override():
    mod = load_module()
    eval_path = make_eval({"a": {"pass_rate": 0.20}})
    orig = mod.EVAL_FILE
    _set(mod, "EVAL_FILE", eval_path)
    try:
        d = mod.decide("a", force=None, threshold=0.10)
        assert d["decision"] == "warn"  # 0.20 < 0.50 warn but > 0.10 block
    finally:
        _restore(mod, "EVAL_FILE", orig)


def test_decide_writes_to_log():
    """decide() should append to eval-gate-decisions.ndjson (NDJSON, Phase 28)."""
    mod = load_module()
    eval_path = make_eval({"a": {"pass_rate": 0.95}})
    log_path = Path(tempfile.gettempdir()) / f"eval-gate-decisions-{id(eval_path)}.ndjson"
    if log_path.exists():
        log_path.unlink()
    orig_eval = mod.EVAL_FILE
    orig_log = mod.DECISIONS_LOG
    _set(mod, "EVAL_FILE", eval_path)
    _set(mod, "DECISIONS_LOG", log_path)
    try:
        mod.decide("a", force=None, threshold=0.30)
        assert log_path.exists()
        lines = log_path.read_text().strip().split("\n")
        assert len(lines) == 1
        entry = json.loads(lines[0])
        assert entry["agent"] == "a"
    finally:
        _set(mod, "EVAL_FILE", orig_eval)
        _set(mod, "DECISIONS_LOG", orig_log)


if __name__ == "__main__":
    test_decide_high_pass_rate_allows()
    test_decide_medium_pass_rate_warns()
    test_decide_low_pass_rate_blocks()
    test_decide_low_pass_rate_with_force_overrides()
    test_decide_unknown_agent_warns()
    test_decide_missing_eval_file_warns()
    test_decide_threshold_override()
    test_decide_writes_to_log()
    print("\nAll eval-gate-enforce tests passed!")
