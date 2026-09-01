"""test_risk_mitigations.py — Tests for Phase 9 R4 risk-mitigation scripts.

Covers:
  - scripts/strict-schemas.py (R5)
  - scripts/cron-secret-sentinel.py (R9)
"""
import importlib.util
import json
import os
import tempfile
from pathlib import Path

REPO = Path("/opt/data/agents")


def load_script(name: str):
    path = REPO / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- R5: strict-schemas ---

def test_strict_schemas_sets_additional_properties_false():
    """All type=object should have additionalProperties: false after the run."""
    mod = load_script("strict-schemas.py")
    doc = {
        "type": "object",
        "properties": {
            "x": {"type": "object", "properties": {}},
            "y": {"type": "object", "properties": {}, "additionalProperties": True},
        },
    }
    mod.walk_and_strict(doc)
    assert doc.get("additionalProperties") is False, "outer object should be strict"
    assert doc["properties"]["x"].get("additionalProperties") is False
    assert doc["properties"]["y"].get("additionalProperties") is False, \
        "additionalProperties: True should be overwritten"
    print("[PASS] strict-schemas sets additionalProperties: false everywhere")


def test_strict_schemas_preserves_already_strict_objects_at_property_level():
    """An object with additionalProperties: false at the top stays exactly as it is."""
    mod = load_script("strict-schemas.py")
    import copy
    inner = {"type": "object", "additionalProperties": False, "props": {"k": "v"}}
    obj = {"type": "object", "additionalProperties": False,
           "properties": {"x": inner}}
    before = copy.deepcopy(obj)
    mod.walk_and_strict(obj)
    # Object that had strict should keep their marker
    assert obj["properties"]["x"].get("additionalProperties") is False
    assert obj["properties"]["x"]["props"] == before["properties"]["x"]["props"]
    print("[PASS] strict-schemas leaves already-strict objects untouched")


def test_strict_schemas_handles_array_items():
    mod = load_script("strict-schemas.py")
    doc = {"type": "array", "items": {"type": "object", "props": {}}}
    mod.walk_and_strict(doc)
    assert doc["items"].get("additionalProperties") is False
    print("[PASS] strict-schemas recurses into array items")


def test_strict_schemas_handles_non_object():
    mod = load_script("strict-schemas.py")
    doc = {"type": "string", "maxLength": 10}
    mod.walk_and_strict(doc)
    assert "additionalProperties" not in doc
    print("[PASS] strict-schemas ignores non-object types")


def test_strict_schemas_handles_empty():
    mod = load_script("strict-schemas.py")
    doc = {}
    mod.walk_and_strict(doc)
    assert doc == {}
    print("[PASS] strict-schemas handles empty doc")


# --- R9: cron-secret-sentinel ---

def test_gh_token_health_ok():
    mod = load_script("cron-secret-sentinel.py")
    # Use a temp dir for testing
    with tempfile.TemporaryDirectory() as td:
        test_token = Path(td) / ".gh_token"
        test_token.write_text("a" * 40)
        # Patch the module's constant
        saved = mod.GH_TOKEN_PATH
        mod.GH_TOKEN_PATH = test_token
        try:
            result = mod.check_gh_token()
        finally:
            mod.GH_TOKEN_PATH = saved
    assert result.get("ok") is True, f"expected ok=True, got {result}"
    print("[PASS] cron-secret-sentinel sees healthy gh_token")


def test_gh_token_health_zero_bytes():
    mod = load_script("cron-secret-sentinel.py")
    with tempfile.TemporaryDirectory() as td:
        test_token = Path(td) / ".gh_token"
        test_token.write_text("")
        saved = mod.GH_TOKEN_PATH
        mod.GH_TOKEN_PATH = test_token
        try:
            result = mod.check_gh_token()
        finally:
            mod.GH_TOKEN_PATH = saved
    assert result["ok"] is False
    assert "empty" in result.get("issue", "")
    print("[PASS] cron-secret-sentinel flags zero-byte token")


def test_gh_token_missing():
    mod = load_script("cron-secret-sentinel.py")
    with tempfile.TemporaryDirectory() as td:
        nonexistent = Path(td) / ".gh_token"
        saved = mod.GH_TOKEN_PATH
        mod.GH_TOKEN_PATH = nonexistent
        try:
            result = mod.check_gh_token()
        finally:
            mod.GH_TOKEN_PATH = saved
    assert result["ok"] is False
    assert "missing" in result.get("issue", "")
    print("[PASS] cron-secret-sentinel flags missing token")


def test_discover_token_uses_clean_prompt():
    """Clean prompts should produce zero findings (loaded via temp cron file)."""
    mod = load_script("cron-secret-sentinel.py")
    fake_cron = {"jobs": [{"name": "good-job", "enabled": True,
                            "prompt": "do something normal"}]}
    with tempfile.TemporaryDirectory() as td:
        cron_file = Path(td) / "jobs.json"
        cron_file.write_text(json.dumps(fake_cron))
        saved = mod.JOBS_FILE
        mod.JOBS_FILE = cron_file
        try:
            findings = mod.discover_token_uses()
        finally:
            mod.JOBS_FILE = saved
    high = [f for f in findings if f["severity"] == "high"]
    assert len(high) == 0, f"Should not flag clean prompts: got {high}"
    print("[PASS] cron-secret-sentinel does not flag clean prompts")


def test_discover_token_uses_catches_hardcoded_pat():
    """A prompt with ghp_xxxxx should be flagged as severity=high."""
    mod = load_script("cron-secret-sentinel.py")
    fake_cron = {"jobs": [{
        "name": "leaky-job",
        "enabled": True,
        "prompt": "deploy with ghp_AbCdEf1234567890abcdef1234567890ABCDEF"
    }]}
    with tempfile.TemporaryDirectory() as td:
        cron_file = Path(td) / "jobs.json"
        cron_file.write_text(json.dumps(fake_cron))
        saved = mod.JOBS_FILE
        mod.JOBS_FILE = cron_file
        try:
            findings = mod.discover_token_uses()
        finally:
            mod.JOBS_FILE = saved
    high = [f for f in findings if f["severity"] == "high"]
    gh_hits = [f for f in high if f["job_name"] == "leaky-job"]
    assert len(gh_hits) >= 1, \
        f"Should flag ghp_ in leaky-job prompt. Findings: {findings}"
    print("[PASS] cron-secret-sentinel detects hardcoded gh tokens")
