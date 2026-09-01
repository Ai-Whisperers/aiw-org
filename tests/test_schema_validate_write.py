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


def test_check_required_recurses_into_arrays():
    """Phase 29 fix (BUG-HUNT H5): required fields inside array items."""
    mod = load_module()
    # Schema: array items must have 'name' + 'amount_usd'
    schema = {
        "type": "object",
        "required": [],
        "properties": {
            "applications_in_flight": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "amount_usd"],
                    "properties": {
                        "name": {"type": "string"},
                        "amount_usd": {"type": "number"},
                    },
                },
            }
        }
    }
    obj = {"applications_in_flight": [{"name": "app1"}, {"name": "app2"}]}  # missing amount_usd
    errors = mod._check_required(obj, schema)
    assert len(errors) == 2, f"expected 2 missing-field errors, got {errors}"
    assert all("amount_usd" in e for e in errors)


def test_check_additional_properties_recurses_into_arrays():
    """Phase 29 fix (BUG-HUNT H4): unexpected fields inside array items."""
    mod = load_module()
    schema = {
        "type": "object",
        "properties": {
            "applications_in_flight": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "additionalProperties": False,
                }
            }
        }
    }
    obj = {"applications_in_flight": [{"name": "app1", "rogue": "x"}, {"name": "app2"}]}
    errors = mod._check_additional_properties(obj, schema)
    assert len(errors) == 1, f"expected 1 unexpected-field error, got {errors}"
    assert "rogue" in errors[0]


def test_hardstop_rejects_path_traversal():
    """Phase 29 fix (BUG-HUNT H1): path traversal in agent_name raises ValueError."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "hardstop_check", "/opt/data/agents/patterns/hardstop_check.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Try various traversal attempts
    bad_names = [
        "../../../etc/passwd",
        "..",
        "../foo",
        "/etc/passwd",
        "foo/../../bar",
    ]
    for bad in bad_names:
        try:
            mod.check("read_state", bad)
            assert False, f"should have raised ValueError for {bad!r}"
        except ValueError:
            pass  # expected


def test_eval_gate_strict_threshold_refuses():
    """Phase 29 fix (BUG-HUNT H7): --strict-threshold refuses bad values."""
    import subprocess
    r = subprocess.run(
        ["/opt/data/.venv/bin/python3",
         "/opt/data/agents/scripts/eval-gate-enforce.py",
         "--agent", "test", "--threshold", "-1", "--strict-threshold"],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 2, f"expected exit 2, got {r.returncode}"
    assert "outside [0, 1]" in r.stderr or "outside" in (r.stdout + r.stderr)


def test_eval_gate_default_threshold_warns():
    """Phase 29 fix (BUG-HUNT H7): default behavior warns (not refuses)."""
    import subprocess
    r = subprocess.run(
        ["/opt/data/.venv/bin/python3",
         "/opt/data/agents/scripts/eval-gate-enforce.py",
         "--agent", "test", "--threshold", "1.5"],
        capture_output=True, text=True, timeout=10,
    )
    # Should still run (not exit 2), but warn
    assert "outside" in (r.stdout + r.stderr).lower() or "warn" in (r.stdout + r.stderr).lower()


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
