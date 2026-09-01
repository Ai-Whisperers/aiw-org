"""Tests for curator/instinct_generator.py — Phase 4.3 instinct generator."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "curator" / "instinct_generator.py"


def load_module():
    spec = importlib.util.spec_from_file_location("instinct_generator", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["instinct_generator"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_read_jsonl_missing_file():
    mod = load_module()
    assert mod._read_jsonl(Path("/nonexistent")) == []


def test_confidence_from_count():
    mod = load_module()
    assert mod._confidence_from_count(0, min_count=5) == 0.0
    assert mod._confidence_from_count(4, min_count=5) == 0.0  # below threshold
    assert mod._confidence_from_count(5, min_count=5) == 0.5  # low
    assert mod._confidence_from_count(15, min_count=5) == 0.75  # medium
    assert mod._confidence_from_count(30, min_count=5) == 0.9  # high


def test_yaml_escape_simple():
    mod = load_module()
    assert mod._yaml_escape("hello") == "hello"
    assert mod._yaml_escape("with: colon") == '"with: colon"'
    assert mod._yaml_escape('with "quote"') == '"with \\"quote\\""'


def test_detect_instincts_empty():
    mod = load_module()
    assert mod.detect_instincts([]) == []


def test_detect_agent_frequency():
    mod = load_module()
    traces = [{"agent": "alpha", "id": f"t{i}"} for i in range(10)]
    traces += [{"agent": "beta", "id": f"b{i}"} for i in range(3)]
    instincts = mod.detect_instincts(traces, min_count=5)
    freq = [i for i in instincts if i["domain"] == "agent-selection"]
    assert len(freq) == 1  # only alpha (beta < min_count)
    assert freq[0]["source_evidence_count"] == 10
    assert freq[0]["confidence"] >= 0.5


def test_detect_workflow_tag():
    mod = load_module()
    traces = [{"agent": "a", "routing_tags": ["urgent"], "id": f"t{i}"} for i in range(8)]
    instincts = mod.detect_instincts(traces, min_count=5)
    tags = [i for i in instincts if i["domain"] == "routing"]
    assert any(t["source_evidence_count"] == 8 for t in tags)


def test_detect_error_rate_watch():
    mod = load_module()
    traces = [
        {"agent": "a", "status": "ok", "id": "1"},
        {"agent": "a", "status": "error: timeout", "id": "2"},
        {"agent": "a", "status": "error: fail", "id": "3"},
        {"agent": "a", "status": "error: fail", "id": "4"},
        {"agent": "a", "status": "error: fail", "id": "5"},
        {"agent": "a", "status": "error: fail", "id": "6"},
    ]
    instincts = mod.detect_instincts(traces, min_count=5)
    error_instincts = [i for i in instincts if i["domain"] == "reliability"]
    assert len(error_instincts) == 1
    assert error_instincts[0]["source_evidence_count"] == 5


def test_detect_source_frequency():
    mod = load_module()
    traces = [{"agent": "a", "source": "monitor", "id": f"t{i}"} for i in range(7)]
    instincts = mod.detect_instincts(traces, min_count=5)
    source_instincts = [i for i in instincts if i["domain"] == "observability"]
    assert any(s["source_evidence_count"] == 7 for s in source_instincts)


def test_instincts_to_yaml_format():
    mod = load_module()
    instincts = [{
        "id": "test-1",
        "trigger": "When test",
        "confidence": 0.75,
        "domain": "test",
        "source_repo": "aiw",
        "source_evidence_count": 10,
        "action": "Do something",
        "generated_at": "2026-09-01T00:00:00Z",
    }]
    yaml = mod.instincts_to_yaml(instincts)
    assert "id: test-1" in yaml
    assert "confidence: 0.75" in yaml
    assert "Auto-generated" in yaml


def test_generate_dry_run():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        traces = Path(tmpdir) / "traces.jsonl"
        out = Path(tmpdir) / "out"
        traces.write_text("\n".join(
            json.dumps({"agent": "a", "id": f"t{i}"}) for i in range(10)
        ))
        report = mod.generate(traces, out, min_count=5, dry_run=True)
        assert report["dry_run"] is True
        assert report["generated"] >= 1
        assert not out.exists() or not any(out.iterdir())


def test_generate_writes_file():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        traces = Path(tmpdir) / "traces.jsonl"
        out = Path(tmpdir) / "out"
        traces.write_text("\n".join(
            json.dumps({"agent": "a", "id": f"t{i}"}) for i in range(10)
        ))
        report = mod.generate(traces, out, min_count=5, dry_run=False)
        assert report["generated"] >= 1
        assert (out / "instincts-latest.yaml").exists()
        yaml_text = (out / "instincts-latest.yaml").read_text()
        assert "agent-selection" in yaml_text


def test_generate_no_traces():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        traces = Path(tmpdir) / "traces.jsonl"
        out = Path(tmpdir) / "out"
        # Empty file
        traces.write_text("")
        report = mod.generate(traces, out, min_count=5, dry_run=False)
        assert report["generated"] == 0
        assert "No traces found" in report["message"]
