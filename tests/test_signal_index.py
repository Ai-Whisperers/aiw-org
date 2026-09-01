"""Tests for memory/signal_index.py — L3 memory inverted index."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "memory" / "signal_index.py"


def load_module():
    spec = importlib.util.spec_from_file_location("signal_index", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["signal_index"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_tokenize_basic():
    mod = load_module()
    tokens = mod._tokenize("The quick brown fox jumps over the lazy dog")
    assert "quick" in tokens
    assert "brown" in tokens
    assert "fox" in tokens
    # Stopwords removed (the is in stopwords list)
    assert "the" not in tokens


def test_tokenize_handles_empty_and_short():
    mod = load_module()
    assert mod._tokenize("") == []
    assert mod._tokenize("a") == []  # too short
    assert mod._tokenize("ab") == ["ab"]  # exactly 2 chars kept


def test_tokenize_handles_underscores():
    mod = load_module()
    tokens = mod._tokenize("route_inbound_lead deploy_prod")
    assert "route_inbound_lead" in tokens
    assert "deploy_prod" in tokens


def test_extract_signal_meta_with_tags():
    mod = load_module()
    signal = {
        "id": "sig-1",
        "routing_tags": ["meeting", "lead"],
        "source": "sales-monitor",
        "type": "lead_signal",
        "payload": {"company": "Acme Corp"},
    }
    meta = mod._extract_signal_meta(signal)
    assert meta["tags"] == ["meeting", "lead"]
    assert "sales" in meta["keywords"]
    assert "monitor" in meta["keywords"]
    assert "acme" in meta["keywords"]


def test_extract_signal_meta_tags_as_string():
    mod = load_module()
    signal = {
        "id": "sig-2",
        "routing_tags": "alert, critical, deploy",
        "source": "monitor",
    }
    meta = mod._extract_signal_meta(signal)
    assert meta["tags"] == ["alert", "critical", "deploy"]


def test_extract_signal_meta_no_tags_uses_alternate_key():
    mod = load_module()
    signal = {"id": "sig-3", "tags": ["urgent"]}
    meta = mod._extract_signal_meta(signal)
    assert meta["tags"] == ["urgent"]


def test_build_index_from_jsonl():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir) / "signals.ndjson"
        index = Path(tmpdir) / "idx.json"
        source.write_text(
            json.dumps({"id": "s1", "routing_tags": ["meeting"], "source": "calendar"}) + "\n" +
            json.dumps({"id": "s2", "routing_tags": ["meeting", "lead"], "source": "sales"}) + "\n" +
            json.dumps({"id": "s3", "routing_tags": ["deploy"], "source": "ci"}) + "\n"
        )
        report = mod.build_index(source, index)
        assert report["signals_processed"] == 3
        assert report["unique_tags"] == 3  # meeting, lead, deploy
        assert index.exists()

        # Test query
        assert mod.query_tag("meeting", index) == ["s1", "s2"]
        assert mod.query_tag("deploy", index) == ["s3"]
        assert mod.query_tag("nonexistent", index) == []
        # keywords
        assert "s1" in mod.query_keyword("calendar", index)
        assert "s2" in mod.query_keyword("sales", index)


def test_build_index_idempotent():
    """Building twice should not duplicate signal_ids in tag/keyword lists."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir) / "signals.ndjson"
        index = Path(tmpdir) / "idx.json"
        source.write_text(json.dumps({"id": "s1", "routing_tags": ["x"], "source": "ymonitor"}) + "\n")
        mod.build_index(source, index)
        mod.build_index(source, index)
        assert mod.query_tag("x", index) == ["s1"]
        assert mod.query_keyword("ymonitor", index) == ["s1"]


def test_build_index_handles_empty_index_file():
    """Empty index file (just-created tempfile) should be treated as fresh index, not crash."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir) / "s.ndjson"
        idx = Path(tmpdir) / "empty_idx.json"
        # Pre-create empty index file (mimics tempfile.NamedTemporaryFile behavior)
        idx.write_text("")
        source.write_text(json.dumps({"id": "s1", "routing_tags": ["x"]}) + "\n")
        # Should not raise JSONDecodeError
        report = mod.build_index(source, idx)
        assert report["signals_processed"] == 1
        # Verify query works on the rebuilt index
        assert "s1" in mod.query_tag("x", idx)


def test_build_index_handles_malformed_lines():
    """Malformed JSONL lines should be skipped, not crash."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir) / "signals.ndjson"
        index = Path(tmpdir) / "idx.json"
        source.write_text(
            "this is not json\n" +
            json.dumps({"id": "s1", "routing_tags": ["x"]}) + "\n" +
            "{bad json\n" +
            json.dumps({"id": "s2", "routing_tags": ["y"]}) + "\n"
        )
        report = mod.build_index(source, index)
        assert report["signals_processed"] == 2  # 2 valid signals


def test_build_index_skips_signals_without_id():
    """Signals without id/signal_id should be skipped silently."""
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir) / "signals.ndjson"
        index = Path(tmpdir) / "idx.json"
        source.write_text(
            json.dumps({"routing_tags": ["x"]}) + "\n" +  # no id
            json.dumps({"id": "s1", "routing_tags": ["x"]}) + "\n"
        )
        report = mod.build_index(source, index)
        assert report["signals_processed"] == 1


def test_query_date_range():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir) / "s.ndjson"
        index = Path(tmpdir) / "idx.json"
        source.write_text(
            json.dumps({"id": "s1", "ts": "2026-09-01T10:00:00Z", "source": "a"}) + "\n" +
            json.dumps({"id": "s2", "ts": "2026-09-15T10:00:00Z", "source": "b"}) + "\n" +
            json.dumps({"id": "s3", "ts": "2026-09-30T10:00:00Z", "source": "c"}) + "\n"
        )
        mod.build_index(source, index)
        result = mod.query_date_range("2026-09-10", "2026-09-20", index)
        assert "s2" in result
        assert "s1" not in result
        assert "s3" not in result
