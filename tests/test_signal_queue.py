"""Tests for scripts/signal_queue.py."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "signal_queue.py"


def load_module():
    spec = importlib.util.spec_from_file_location("signal_queue", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_append_signal_assigns_id_and_ts():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        qp = Path(tmp) / "queue.ndjson"
        sig = mod.append_signal({"source": "test", "signal_type": "inbound"}, queue_path=qp)
        assert sig["id"].startswith("sig-")
        assert "ts" in sig
        assert sig["status"] == "pending"
        assert qp.exists()
        lines = qp.read_text().strip().split("\n")
        assert len(lines) == 1
        loaded = json.loads(lines[0])
        assert loaded["id"] == sig["id"]


def test_append_preserves_provided_fields():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        qp = Path(tmp) / "queue.ndjson"
        sig = mod.append_signal({
            "id": "my-custom-id",
            "ts": "2026-09-01T00:00:00Z",
            "source": "test",
            "signal_type": "inbound",
            "status": "routed",
        }, queue_path=qp)
        assert sig["id"] == "my-custom-id"
        assert sig["ts"] == "2026-09-01T00:00:00Z"
        assert sig["status"] == "routed"


def test_list_signals_filters_by_status():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        qp = Path(tmp) / "queue.ndjson"
        mod.append_signal({"source": "a", "signal_type": "inbound", "status": "pending"}, queue_path=qp)
        mod.append_signal({"source": "b", "signal_type": "inbound", "status": "routed"}, queue_path=qp)
        mod.append_signal({"source": "c", "signal_type": "inbound", "status": "pending"}, queue_path=qp)
        all_sigs = mod.list_signals(queue_path=qp, status=None)
        assert len(all_sigs) == 3
        pending = mod.list_signals(queue_path=qp, status="pending")
        assert len(pending) == 2
        routed = mod.list_signals(queue_path=qp, status="routed")
        assert len(routed) == 1


def test_update_signal_status():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        qp = Path(tmp) / "queue.ndjson"
        sig = mod.append_signal({"source": "test", "signal_type": "inbound"}, queue_path=qp)
        ok = mod.update_signal_status(sig["id"], "routed", queue_path=qp, extra={"routed_to": ["agent-x"]})
        assert ok is True
        sigs = mod.list_signals(queue_path=qp)
        assert len(sigs) == 1
        assert sigs[0]["status"] == "routed"
        assert sigs[0]["routed_to"] == ["agent-x"]


def test_update_nonexistent_signal_returns_false():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        qp = Path(tmp) / "queue.ndjson"
        ok = mod.update_signal_status("sig-doesnotexist", "routed", queue_path=qp)
        assert ok is False


def test_list_signals_handles_malformed_lines():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        qp = Path(tmp) / "queue.ndjson"
        qp.write_text('{"id":"valid","source":"test","signal_type":"inbound"}\nNOT_JSON\n{"id":"valid2","source":"test","signal_type":"inbound"}\n')
        sigs = mod.list_signals(queue_path=qp)
        assert len(sigs) == 2
        assert sigs[0]["id"] == "valid"
        assert sigs[1]["id"] == "valid2"


def test_list_signals_returns_empty_when_missing():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        qp = Path(tmp) / "nonexistent.ndjson"
        sigs = mod.list_signals(queue_path=qp)
        assert sigs == []


def test_update_preserves_other_signals():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        qp = Path(tmp) / "queue.ndjson"
        sig_a = mod.append_signal({"source": "a", "signal_type": "inbound"}, queue_path=qp)
        sig_b = mod.append_signal({"source": "b", "signal_type": "inbound"}, queue_path=qp)
        sig_c = mod.append_signal({"source": "c", "signal_type": "inbound"}, queue_path=qp)
        mod.update_signal_status(sig_b["id"], "routed", queue_path=qp)
        all_sigs = mod.list_signals(queue_path=qp)
        assert len(all_sigs) == 3
        for s in all_sigs:
            if s["id"] == sig_b["id"]:
                assert s["status"] == "routed"
            else:
                assert s["status"] == "pending"


if __name__ == "__main__":
    test_append_signal_assigns_id_and_ts()
    test_append_preserves_provided_fields()
    test_list_signals_filters_by_status()
    test_update_signal_status()
    test_update_nonexistent_signal_returns_false()
    test_list_signals_handles_malformed_lines()
    test_list_signals_returns_empty_when_missing()
    test_update_preserves_other_signals()
    print("\nAll signal_queue tests passed!")
