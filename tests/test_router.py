"""Tests for scripts/router.py."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "router.py"


def load_module():
    spec = importlib.util.spec_from_file_location("router", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


# Sample dispatch rules used in tests
SAMPLE_RULES = {
    "dispatch_rules": [
        {
            "id": "route-lead",
            "match": {"signal_type": "cross_dept", "routing_tags": ["lead", "inbound"]},
            "deliver_to": [
                {"type": "agent", "id": "apollo-sales-lead"},
                {"type": "agent", "id": "cadmus-lead-enrichment"},
            ],
            "fan_out": "all",
        },
        {
            "id": "route-content",
            "match": {"routing_tags": ["content"]},
            "deliver_to": [{"type": "agent", "id": "hera-marketing-lead"}],
            "fan_out": "first_available",
        },
        {
            "id": "route-ops-anomaly",
            "match": {"routing_tags": ["drift"]},
            "deliver_to": [{"type": "agent", "id": "kronos-operations-lead"}],
            "fan_out": "first_available",
        },
    ]
}


def _patch_rules(mod, rules):
    """Replace DISPATCH_RULES_FILE with a temp file."""
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
    yaml_text = json.dumps(rules)  # not actually yaml but the test mock parses
    f.write(yaml_text)
    f.close()
    return Path(f.name)


def test_match_signal_finds_rule():
    mod = load_module()
    signal = {"signal_type": "cross_dept", "routing_tags": ["lead", "inbound"]}
    rule = mod.match_signal(signal, SAMPLE_RULES["dispatch_rules"])
    assert rule is not None
    assert rule["id"] == "route-lead"


def test_match_signal_requires_all_tags():
    mod = load_module()
    # Only 1 of 2 required tags -> no match
    signal = {"signal_type": "cross_dept", "routing_tags": ["lead"]}
    rule = mod.match_signal(signal, SAMPLE_RULES["dispatch_rules"])
    assert rule is None


def test_match_signal_department_constraint():
    mod = load_module()
    rules = [{
        "id": "dept-rule",
        "match": {"department_id": "sales", "routing_tags": ["lead"]},
        "deliver_to": [{"type": "agent", "id": "apollo-sales-lead"}],
        "fan_out": "all",
    }]
    # dept=sales, tags=[lead] -> match
    sig1 = {"department": "sales", "routing_tags": ["lead"]}
    assert mod.match_signal(sig1, rules) is not None
    # dept=ops -> no match
    sig2 = {"department": "ops", "routing_tags": ["lead"]}
    assert mod.match_signal(sig2, rules) is None


def test_match_signal_no_match():
    mod = load_module()
    signal = {"signal_type": "unknown", "routing_tags": ["nonexistent"]}
    rule = mod.match_signal(signal, SAMPLE_RULES["dispatch_rules"])
    assert rule is None


def test_compute_recipients_fan_out_all():
    mod = load_module()
    rule = {
        "deliver_to": [
            {"type": "agent", "id": "a"},
            {"type": "agent", "id": "b"},
            {"type": "agent", "id": "c"},
        ],
        "fan_out": "all",
    }
    recipients = mod.compute_recipients(rule)
    assert len(recipients) == 3
    assert [r["id"] for r in recipients] == ["a", "b", "c"]


def test_compute_recipients_fan_out_first():
    mod = load_module()
    rule = {
        "deliver_to": [
            {"type": "agent", "id": "a"},
            {"type": "agent", "id": "b"},
        ],
        "fan_out": "first_available",
    }
    recipients = mod.compute_recipients(rule)
    assert len(recipients) == 1
    assert recipients[0]["id"] == "a"


def test_compute_recipients_unknown_fan_out():
    mod = load_module()
    rule = {
        "deliver_to": [{"type": "agent", "id": "a"}],
        "fan_out": "unknown_strategy",
    }
    recipients = mod.compute_recipients(rule)
    # Safe default: deliver to all
    assert len(recipients) == 1


def test_process_pending_with_no_signals():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        sq = Path(tmp) / "signal-queue.ndjson"
        # Patch signal_queue.SIGNAL_QUEUE by setting it via the module attribute
        sq_mod = sys.modules.get("signal_queue")
        if sq_mod is None:
            import signal_queue
            sq_mod = signal_queue
        orig_sq = sq_mod.SIGNAL_QUEUE
        sq_mod.SIGNAL_QUEUE = sq
        try:
            summary = mod.process_pending(limit=10)
            assert summary["processed"] == 0
            assert summary["routed"] == 0
        finally:
            sq_mod.SIGNAL_QUEUE = orig_sq


def test_process_pending_routes_signal():
    """End-to-end: append signal, process, verify outbox + routing log."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        # Patch signal queue
        import signal_queue as sq_mod
        orig_sq = sq_mod.SIGNAL_QUEUE
        sq_path = Path(tmp) / "signal-queue.ndjson"
        sq_mod.SIGNAL_QUEUE = sq_path

        # Patch dispatch rules
        orig_dispatch = mod.DISPATCH_RULES_FILE
        rules_path = Path(tmp) / "dispatch-rules.yaml"
        # Write YAML manually (not JSON)
        import yaml
        rules_path.write_text(yaml.safe_dump(SAMPLE_RULES))
        mod.DISPATCH_RULES_FILE = rules_path

        # Patch outbox (use temp dir)
        orig_outbox = mod.AGENT_OUTBOX
        outbox_dir = Path(tmp) / "outbox"
        mod.AGENT_OUTBOX = {
            "apollo-sales-lead": str(outbox_dir / "apollo"),
            "cadmus-lead-enrichment": str(outbox_dir / "cadmus"),
            "hera-marketing-lead": str(outbox_dir / "hera"),
            "kronos-operations-lead": str(outbox_dir / "kronos"),
        }

        # Patch routing log
        orig_log = mod.ROUTING_LOG
        log_path = Path(tmp) / "routing.ndjson"
        mod.ROUTING_LOG = log_path

        try:
            # Append a signal
            sig = sq_mod.append_signal({
                "source": "webhook-test",
                "signal_type": "cross_dept",
                "routing_tags": ["lead", "inbound"],
            })

            # Process
            summary = mod.process_pending(limit=10)
            assert summary["processed"] == 1
            assert summary["routed"] == 1
            assert summary["no_rule"] == 0

            # Verify signal marked as routed
            sigs = sq_mod.list_signals()
            assert sigs[0]["status"] == "routed"
            assert sigs[0]["routed_via_rule"] == "route-lead"

            # Verify both outboxes have the signal file
            apollo_path = outbox_dir / "apollo" / "signals" / f"{sig['id']}.md"
            cadmus_path = outbox_dir / "cadmus" / "signals" / f"{sig['id']}.md"
            assert apollo_path.exists()
            assert cadmus_path.exists()

            # Verify routing log
            assert log_path.exists()
            lines = log_path.read_text().strip().split("\n")
            assert len(lines) == 1
            decision = json.loads(lines[0])
            assert decision["rule_id"] == "route-lead"
            assert set(decision["recipients"]) == {"apollo-sales-lead", "cadmus-lead-enrichment"}
        finally:
            sq_mod.SIGNAL_QUEUE = orig_sq
            mod.DISPATCH_RULES_FILE = orig_dispatch
            mod.AGENT_OUTBOX = orig_outbox
            mod.ROUTING_LOG = orig_log


def test_process_pending_no_matching_rule():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        import signal_queue as sq_mod
        orig_sq = sq_mod.SIGNAL_QUEUE
        sq_path = Path(tmp) / "signal-queue.ndjson"
        sq_mod.SIGNAL_QUEUE = sq_path

        orig_dispatch = mod.DISPATCH_RULES_FILE
        rules_path = Path(tmp) / "dispatch-rules.yaml"
        import yaml
        rules_path.write_text(yaml.safe_dump(SAMPLE_RULES))
        mod.DISPATCH_RULES_FILE = rules_path

        orig_log = mod.ROUTING_LOG
        log_path = Path(tmp) / "routing.ndjson"
        mod.ROUTING_LOG = log_path

        try:
            sig = sq_mod.append_signal({
                "source": "test",
                "signal_type": "unknown_type",
                "routing_tags": ["unknown_tag"],
            })
            summary = mod.process_pending(limit=10)
            assert summary["processed"] == 1
            assert summary["routed"] == 0
            assert summary["no_rule"] == 1

            # Signal still marked as routed (so we don't loop)
            sigs = sq_mod.list_signals()
            assert sigs[0]["status"] == "routed"
            assert sigs[0]["routed_via_rule"] is None
        finally:
            sq_mod.SIGNAL_QUEUE = orig_sq
            mod.DISPATCH_RULES_FILE = orig_dispatch
            mod.ROUTING_LOG = orig_log


def test_load_rules_missing_files():
    mod = load_module()
    orig_dispatch = mod.DISPATCH_RULES_FILE
    orig_timing = mod.TIMING_RULES_FILE
    missing = Path("/tmp/does-not-exist-xyz.yaml")
    mod.DISPATCH_RULES_FILE = missing
    mod.TIMING_RULES_FILE = missing
    try:
        dispatch, timing = mod.load_rules()
        assert dispatch == []
        assert timing == []
    finally:
        mod.DISPATCH_RULES_FILE = orig_dispatch
        mod.TIMING_RULES_FILE = orig_timing


if __name__ == "__main__":
    test_match_signal_finds_rule()
    test_match_signal_requires_all_tags()
    test_match_signal_department_constraint()
    test_match_signal_no_match()
    test_compute_recipients_fan_out_all()
    test_compute_recipients_fan_out_first()
    test_compute_recipients_unknown_fan_out()
    test_process_pending_with_no_signals()
    test_process_pending_routes_signal()
    test_process_pending_no_matching_rule()
    test_load_rules_missing_files()
    print("\nAll router tests passed!")
