"""Tests for scripts/schema-validate-write.py."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "schema-validate-write.py"


def load_module():
    spec = importlib.util.spec_from_file_location("schema_validate_write", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_check_required_missing_field():
    mod = load_module()
    schema = {"type": "object", "required": ["name"], "properties": {"name": {"type": "string"}}}
    errors = mod._check_required({"other": "x"}, schema)
    assert len(errors) == 1
    assert "name" in errors[0]


def test_check_required_present():
    mod = load_module()
    schema = {"type": "object", "required": ["name"], "properties": {"name": {"type": "string"}}}
    errors = mod._check_required({"name": "ok"}, schema)
    assert errors == []


def test_check_additional_properties_strict():
    mod = load_module()
    schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "additionalProperties": False,
    }
    errors = mod._check_additional_properties({"name": "ok", "extra": "x"}, schema)
    assert len(errors) == 1
    assert "extra" in errors[0]


def test_check_additional_properties_lenient():
    mod = load_module()
    schema = {"type": "object", "properties": {"name": {"type": "string"}}  # no additionalProperties key
    }
    errors = mod._check_additional_properties({"name": "ok", "extra": "x"}, schema)
    assert errors == []


def test_check_nested():
    mod = load_module()
    schema = {
        "type": "object",
        "properties": {
            "outer": {
                "type": "object",
                "properties": {"inner": {"type": "string"}},
                "additionalProperties": False,
            }
        },
    }
    errors = mod._check_additional_properties({"outer": {"inner": "x", "rogue": "y"}}, schema)
    assert len(errors) == 1
    assert "rogue" in errors[0]


def test_validate_file_no_schema_returns_warn():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        # Use a filename that isn't in FILE_TO_SCHEMA (post-Phase 28 all registered files have schemas)
        p = Path(tmp) / "no-schema-test.json"
        p.write_text("{}")
        is_valid, errors, schema_path = mod.validate_file(p)
        # No schema registered = warn + allow
        assert schema_path is None
        assert "no schema registered" in errors[0]


def test_validate_file_missing_returns_error():
    mod = load_module()
    p = Path(tempfile.gettempdir()) / "nonexistent-xyz.json"
    if p.exists():
        p.unlink()
    is_valid, errors, schema_path = mod.validate_file(p)
    assert is_valid is False
    assert "not found" in errors[0]


def test_validate_file_invalid_json():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "kiki.json"  # has schema
        p.write_text("{ not json")
        is_valid, errors, schema_path = mod.validate_file(p)
        assert is_valid is False
        assert "invalid JSON" in errors[0]


def test_find_state_file_searches_dirs():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        # Create a file in /opt/data/state if writable
        if (Path("/opt/data/state")).exists():
            target = Path("/opt/data/state") / "test_schema_validator.json"
            target.write_text("{}")
            try:
                result = mod._find_state_file(Path(tmp) / "test_schema_validator.json")
                assert result is not None
                assert result.exists()
            finally:
                target.unlink()


def test_validate_strict_blocks():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "kiki.json"
        # kiki schema requires last_run + open_stuck; rogue fields trigger strict block
        p.write_text(json.dumps({
            "last_run": "2026-09-01T00:00:00Z",
            "open_stuck": [],
            "rogue_field": "should_block",
        }))
        is_valid, errors, _ = mod.validate_file(p, lenient=False)
        assert is_valid is False
        assert any("rogue_field" in e for e in errors)


def test_validate_lenient_warns():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "kiki.json"
        p.write_text(json.dumps({
            "last_run": "2026-09-01T00:00:00Z",
            "open_stuck": [],
            "rogue_field": "should_warn",
        }))
        is_valid, errors, _ = mod.validate_file(p, lenient=True)
        assert is_valid is True  # lenient = valid


if __name__ == "__main__":
    test_check_required_missing_field()
    test_check_required_present()
    test_check_additional_properties_strict()
    test_check_additional_properties_lenient()
    test_check_nested()
    test_validate_file_no_schema_returns_warn()
    test_validate_file_missing_returns_error()
    test_validate_file_invalid_json()
    test_find_state_file_searches_dirs()
    test_validate_strict_blocks()
    test_validate_lenient_warns()
    print("\nAll schema-validate-write tests passed!")
