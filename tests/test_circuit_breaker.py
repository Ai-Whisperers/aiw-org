"""Tests for circuit_breaker.py."""
import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "circuit_breaker.py"


def load_module():
    spec = importlib.util.spec_from_file_location("cb_under_test", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_state_file_constant():
    mod = load_module()
    assert mod.STATE_FILE.name == "circuit-breakers.json"
    assert "state" in str(mod.STATE_FILE)


def test_new_state_shape():
    mod = load_module()
    s = mod._new_state()
    assert s["state"] == "closed"
    assert s["failures"] == []
    assert s["successes"] == []
    assert s["opened_at"] is None


def test_can_deliver_unknown_recipient():
    mod = load_module()
    mod.reset_all()
    allowed, reason = mod.can_deliver(f"never-seen-{__import__('uuid').uuid4().hex[:8]}")
    assert allowed is True
    assert reason == "closed"


def test_record_failure_below_threshold():
    mod = load_module()
    mod.reset_all()
    rid = f"below-thr-{__import__('uuid').uuid4().hex[:8]}"
    mod.record_failure(rid, "err1")
    mod.record_failure(rid, "err2")
    # 2 failures < threshold of 3 → circuit still closed
    state = mod.get_state(rid)
    assert state["state"] == "closed"
    assert len(state["failures"]) == 2


def test_record_failure_opens_circuit():
    mod = load_module()
    mod.reset_all()
    rid = f"trip-{__import__('uuid').uuid4().hex[:8]}"
    for i in range(3):  # threshold is 3
        mod.record_failure(rid, f"err-{i}")
    state = mod.get_state(rid)
    assert state["state"] == "open"
    assert state["opened_at"] is not None
    assert len(state["failures"]) == 3


def test_can_deliver_open_circuit():
    mod = load_module()
    mod.reset_all()
    rid = f"blocked-{__import__('uuid').uuid4().hex[:8]}"
    for i in range(3):
        mod.record_failure(rid, "x")
    allowed, reason = mod.can_deliver(rid)
    assert allowed is False
    assert reason == "circuit-open"


def test_record_success_closes_half_open():
    """Simulate cooldown elapsing then probe succeeds."""
    mod = load_module()
    mod.reset_all()
    rid = f"halfopen-{__import__('uuid').uuid4().hex[:8]}"

    # Trip the breaker
    for i in range(3):
        mod.record_failure(rid, "x")
    assert mod.get_state(rid)["state"] == "open"

    # Manually advance opened_at past cooldown
    state_dict = mod._load_state()
    state_dict[rid]["opened_at"] = "2020-01-01T00:00:00+00:00"  # way in the past
    mod._save_state(state_dict)

    # First delivery after cooldown → half-open probe allowed
    allowed, reason = mod.can_deliver(rid)
    assert allowed is True
    assert reason == "half-open-probe"

    # Subsequent probe NOT allowed until result recorded
    allowed2, _ = mod.can_deliver(rid)
    assert allowed2 is False

    # Record success → closes circuit
    mod.record_success(rid)
    assert mod.get_state(rid)["state"] == "closed"


def test_record_failure_resets_window():
    """Failures list shouldn't grow unbounded — should trim to WINDOW_SIZE."""
    mod = load_module()
    mod.reset_all()
    rid = f"window-{__import__('uuid').uuid4().hex[:8]}"
    # Add 15 failures (> WINDOW_SIZE of 10)
    for i in range(15):
        mod.record_failure(rid, f"err-{i}")
    state = mod.get_state(rid)
    assert len(state["failures"]) == mod.WINDOW_SIZE


def test_reset_all():
    mod = load_module()
    mod.reset_all()
    # Use unique IDs to avoid collision with other tests
    unique_a = f"reset-test-a-{__import__('uuid').uuid4().hex[:8]}"
    unique_b = f"reset-test-b-{__import__('uuid').uuid4().hex[:8]}"
    mod.record_failure(unique_a, "x")
    mod.record_failure(unique_b, "y")
    assert len(mod._load_state()) == 2
    n = mod.reset_all()
    assert n == 2
    assert mod._load_state() == {}


def test_summary_shape():
    mod = load_module()
    mod.reset_all()
    mod.record_failure("r1", "err")
    s = mod.summary()
    assert "r1" in s
    assert s["r1"]["state"] == "closed"  # 1 failure < threshold
    assert s["r1"]["failure_count"] == 1
    assert s["r1"]["last_error"] == "err"


if __name__ == "__main__":
    test_state_file_constant()
    test_new_state_shape()
    test_can_deliver_unknown_recipient()
    test_record_failure_below_threshold()
    test_record_failure_opens_circuit()
    test_can_deliver_open_circuit()
    test_record_success_closes_half_open()
    test_record_failure_resets_window()
    test_reset_all()
    test_summary_shape()
    print("\nAll circuit_breaker tests passed!")
