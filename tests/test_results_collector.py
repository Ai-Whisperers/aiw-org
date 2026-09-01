"""Tests for scripts/results-collector.py."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "results-collector.py"


def load_module():
    spec = importlib.util.spec_from_file_location("results_collector", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_verify_result_passes():
    mod = load_module()
    # 60+ words with both required sections for apollo-sales-lead
    content = """## Summary
This is a test result with the required sections. We have enough words
to pass the minimum word count check for apollo-sales-lead which is fifty.
Adding more words to ensure we exceed fifty total word count for the check.
A comprehensive test result with sufficient content and proper sections.

## Next Steps
Follow up with the appropriate team and verify the deliverable meets
all the requirements as specified in the original task description.
"""
    v = mod.verify_result("apollo-sales-lead", content)
    assert v["verified"] is True, f"issues: {v['issues']}"


def test_verify_result_missing_section():
    mod = load_module()
    content = """Just some content here. No required sections present.
A few more words to pad."""
    v = mod.verify_result("apollo-sales-lead", content)
    assert v["verified"] is False
    assert any("missing section" in i for i in v["issues"])


def test_verify_result_too_short():
    mod = load_module()
    content = "## Summary\nBrief."
    v = mod.verify_result("apollo-sales-lead", content)
    assert v["verified"] is False
    assert any("too short" in i for i in v["issues"])


def test_verify_result_fail_pattern():
    mod = load_module()
    content = """## Summary
TODO fix this later.
More words here to pass the count check.
""" * 10
    v = mod.verify_result("apollo-sales-lead", content)
    assert v["verified"] is False
    assert any("fail pattern" in i for i in v["issues"])


def test_verify_result_unknown_uses_defaults():
    mod = load_module()
    content = "Short."
    v = mod.verify_result("unknown-agent", content)
    # Defaults: no required sections, min_words=10, no fail patterns
    # "Short." is only 1 word, too short for default min
    assert v["verified"] is False
    assert any("too short" in i for i in v["issues"])


def test_load_save_tasks():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            # Save (creates parent dirs)
            tasks = [
                {"task_id": "t1", "status": "assigned"},
                {"task_id": "t2", "status": "done"},
            ]
            mod.save_tasks("sales", tasks)
            loaded = mod.load_tasks("sales")
            assert len(loaded) == 2
            assert loaded[0]["task_id"] == "t1"
            assert loaded[1]["status"] == "done"
        finally:
            mod.STATE_DIR = orig


def test_load_tasks_empty_when_missing():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp)
        try:
            assert mod.load_tasks("sales") == []
        finally:
            mod.STATE_DIR = orig


def test_check_dept_marks_done_when_outbox_exists():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig_state = mod.STATE_DIR
        orig_root = mod.AGENTS_ROOT
        mod.STATE_DIR = Path(tmp) / "state"
        mod.AGENTS_ROOT = Path(tmp) / "agents"

        # Create task
        task = {
            "task_id": "task-sig-1",
            "status": "assigned",
            "assignee": "apollo-sales-lead",
        }
        mod.save_tasks("sales", [task])

        # Create matching outbox
        day = "2026-09-01"
        outbox_dir = mod.AGENTS_ROOT / "demiurge" / "agents" / "apollo-sales-lead" / "outbox"
        outbox_dir.mkdir(parents=True)
        outbox_file = outbox_dir / f"{day}.md"
        # 60 words with required sections
        outbox_file.write_text("## Summary\n" + "word " * 60 + "\n## Next Steps\nMore content here.")

        try:
            s = mod.check_dept("sales", day=day)
            assert s["done"] == 1
            assert s["failed"] == 0
            # Verify task was updated
            tasks = mod.load_tasks("sales")
            assert tasks[0]["status"] == "done"
            assert "verified_at" in tasks[0]
        finally:
            mod.STATE_DIR = orig_state
            mod.AGENTS_ROOT = orig_root


def test_check_dept_marks_needs_review_when_outbox_fails():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig_state = mod.STATE_DIR
        orig_root = mod.AGENTS_ROOT
        mod.STATE_DIR = Path(tmp) / "state"
        mod.AGENTS_ROOT = Path(tmp) / "agents"

        task = {
            "task_id": "task-sig-bad",
            "status": "assigned",
            "assignee": "apollo-sales-lead",
        }
        mod.save_tasks("sales", [task])

        # Outbox exists but fails verification (no required sections, too short)
        day = "2026-09-01"
        outbox_dir = mod.AGENTS_ROOT / "demiurge" / "agents" / "apollo-sales-lead" / "outbox"
        outbox_dir.mkdir(parents=True)
        outbox_file = outbox_dir / f"{day}.md"
        outbox_file.write_text("Bad.")

        try:
            s = mod.check_dept("sales", day=day)
            assert s["done"] == 0
            assert s["failed"] == 1
            tasks = mod.load_tasks("sales")
            assert tasks[0]["status"] == "needs_review"
        finally:
            mod.STATE_DIR = orig_state
            mod.AGENTS_ROOT = orig_root


def test_check_dept_skips_done_tasks():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig_state = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp) / "state"
        try:
            # Pre-existing done task
            tasks = [
                {"task_id": "t1", "status": "done"},
                {"task_id": "t2", "status": "assigned", "assignee": "x"},
            ]
            mod.save_tasks("sales", tasks)
            s = mod.check_dept("sales")
            # Only t2 is checked
            assert s["checked"] == 1
            assert s["total"] == 2
        finally:
            mod.STATE_DIR = orig_state


def test_show_summary_aggregates():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        orig_state = mod.STATE_DIR
        mod.STATE_DIR = Path(tmp) / "state"
        try:
            mod.save_tasks("sales", [{"task_id": "t1", "status": "done"}])
            mod.save_tasks("ops", [{"task_id": "t2", "status": "assigned"}])
            mod.save_tasks("eng", [{"task_id": "t3", "status": "needs_review"}])
            out = mod.show_summary()
            assert out["day"] is not None
            dept_names = {d["dept"]: d for d in out["depts"]}
            assert "sales" in dept_names
            assert "ops" in dept_names
            assert "eng" in dept_names
            assert dept_names["sales"]["done"] == 1
            assert dept_names["ops"]["open"] == 1
            assert dept_names["eng"]["needs_review"] == 1
        finally:
            mod.STATE_DIR = orig_state


if __name__ == "__main__":
    test_verify_result_passes()
    test_verify_result_missing_section()
    test_verify_result_too_short()
    test_verify_result_fail_pattern()
    test_verify_result_unknown_uses_defaults()
    test_load_save_tasks()
    test_load_tasks_empty_when_missing()
    test_check_dept_marks_done_when_outbox_exists()
    test_check_dept_marks_needs_review_when_outbox_fails()
    test_check_dept_skips_done_tasks()
    test_show_summary_aggregates()
    print("\nAll results-collector tests passed!")
