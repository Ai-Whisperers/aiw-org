"""Tests for scripts/intake.py."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "intake.py"


def load_module():
    spec = importlib.util.spec_from_file_location("intake", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_assign_to_subagent_lead_match():
    mod = load_module()
    sig = {"routing_tags": ["lead", "inbound"]}
    assert mod.assign_to_subagent(sig, "sales") == "apollo-sales-lead"


def test_assign_to_subagent_enrichment_match():
    mod = load_module()
    sig = {"routing_tags": ["enrichment"]}
    assert mod.assign_to_subagent(sig, "sales") == "cadmus-lead-enrichment"


def test_assign_to_subagent_falls_back_to_dept_lead():
    mod = load_module()
    sig = {"routing_tags": ["completely_unknown"]}
    # First agent in sales dept is apollo-sales-lead
    assert mod.assign_to_subagent(sig, "sales") == "apollo-sales-lead"


def test_assign_to_subagent_drift_to_kronos():
    mod = load_module()
    sig = {"routing_tags": ["drift", "hard-stop"]}
    assert mod.assign_to_subagent(sig, "operations") == "kronos-operations-lead"


def test_create_task_basic():
    mod = load_module()
    sig = {
        "id": "sig-abc123",
        "source": "webhook",
        "signal_type": "cross_dept",
        "routing_tags": ["lead", "inbound"],
        "payload": {"name": "Test Lead", "email": "test@example.com"},
        "ts": "2026-09-01T00:00:00Z",
    }
    task = mod.create_task(sig, "sales", "apollo-sales-lead")
    assert task["task_id"] == "task-sig-abc123"
    assert task["dept"] == "sales"
    assert task["assignee"] == "apollo-sales-lead"
    assert task["status"] == "assigned"
    assert "test@example.com" in str(task["payload"])


def test_append_task_creates_file():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        # Patch STATE_DIR
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            task = {"task_id": "task-1", "dept": "sales", "assignee": "apollo", "status": "assigned"}
            mod.append_task(task, "sales")
            tasks_file = Path(tmp) / "sales" / "tasks.jsonl"
            assert tasks_file.exists()
            lines = tasks_file.read_text().strip().split("\n")
            assert len(lines) == 1
            loaded = json.loads(lines[0])
            assert loaded["task_id"] == "task-1"
        finally:
            mod.STATE_DIR = orig


def test_list_dept_tasks():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            mod.append_task({"task_id": "t1", "status": "assigned"}, "sales")
            mod.append_task({"task_id": "t2", "status": "done"}, "sales")
            mod.append_task({"task_id": "t3", "status": "assigned"}, "sales")
            all_tasks = mod.list_dept_tasks("sales")
            assert len(all_tasks) == 3
            assigned = mod.list_dept_tasks("sales", status="assigned")
            assert len(assigned) == 2
            done = mod.list_dept_tasks("sales", status="done")
            assert len(done) == 1
        finally:
            mod.STATE_DIR = orig


def test_list_dept_tasks_returns_empty_when_no_file():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            assert mod.list_dept_tasks("sales") == []
        finally:
            mod.STATE_DIR = orig


def test_process_dept_filters_routed_signals():
    """Process only signals routed to this dept."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig_state = mod.STATE_DIR
        orig_sq_path = sys.modules["signal_queue"].SIGNAL_QUEUE
        sq_path = Path(tmp) / "signal-queue.ndjson"
        sys.modules["signal_queue"].SIGNAL_QUEUE = sq_path

        mod.STATE_DIR = Path(tmp)
        try:
            # Append a sales signal
            sys.modules["signal_queue"].append_signal({
                "id": "sig-sales-1",
                "source": "webhook",
                "signal_type": "cross_dept",
                "routing_tags": ["lead", "inbound"],
                "status": "routed",
                "routed_to": ["apollo-sales-lead"],
            }, queue_path=sq_path)
            # Append an unrelated signal (routed to engineering)
            sys.modules["signal_queue"].append_signal({
                "id": "sig-eng-1",
                "source": "monitor",
                "signal_type": "internal",
                "routing_tags": ["drift"],
                "status": "routed",
                "routed_to": ["kronos-operations-lead"],
            }, queue_path=sq_path)

            summary = mod.process_dept("sales", limit=10)
            assert summary["relevant"] == 1
            assert summary["assigned"] == 1
            assert summary["tasks"][0]["task_id"] == "task-sig-sales-1"
            assert summary["tasks"][0]["assignee"] == "apollo-sales-lead"
        finally:
            sys.modules["signal_queue"].SIGNAL_QUEUE = orig_sq_path
            mod.STATE_DIR = orig_state


def test_process_dept_handles_no_signals():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig_sq_path = sys.modules["signal_queue"].SIGNAL_QUEUE
        sq_path = Path(tmp) / "signal-queue.ndjson"
        sys.modules["signal_queue"].SIGNAL_QUEUE = sq_path
        try:
            summary = mod.process_dept("sales", limit=10)
            assert summary["relevant"] == 0
            assert summary["assigned"] == 0
        finally:
            sys.modules["signal_queue"].SIGNAL_QUEUE = orig_sq_path


def test_notify_assignee_writes_to_outbox():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        agents_root = Path(tmp) / "agents"
        outbox = agents_root / "demiurge" / "agents" / "apollo-sales-lead" / "outbox"
        outbox.mkdir(parents=True)

        orig_root = mod.AGENTS_ROOT
        mod.AGENTS_ROOT = agents_root
        try:
            task = {
                "task_id": "task-test",
                "dept": "sales",
                "assignee": "apollo-sales-lead",
                "summary": "Test task",
                "payload": {"x": 1},
                "source": "test",
                "created_at": "2026-09-01T00:00:00Z",
                "signal_id": "sig-test",
            }
            path = mod.notify_assignee(task, "apollo-sales-lead")
            assert Path(path).exists()
            content = Path(path).read_text()
            assert "task-test" in content
            assert "Sales intake" in content
            assert "sig-test" in content
        finally:
            mod.AGENTS_ROOT = orig_root


def test_dept_name_mapping():
    mod = load_module()
    assert mod.dept_name("sales") == "Sales"
    assert mod.dept_name("engineering") == "Engineering"
    assert mod.dept_name("unknown") == "unknown"


if __name__ == "__main__":
    test_assign_to_subagent_lead_match()
    test_assign_to_subagent_enrichment_match()
    test_assign_to_subagent_falls_back_to_dept_lead()
    test_assign_to_subagent_drift_to_kronos()
    test_create_task_basic()
    test_append_task_creates_file()
    test_list_dept_tasks()
    test_list_dept_tasks_returns_empty_when_no_file()
    test_process_dept_filters_routed_signals()
    test_process_dept_handles_no_signals()
    test_notify_assignee_writes_to_outbox()
    test_dept_name_mapping()
    print("\nAll intake tests passed!")
