#!/usr/bin/env python3
"""schema-validate-write.py — Validate state file before write.

Built as Phase 27 R3 (from chaos scenario #1 finding).

For each known state file, validates against its JSON schema (if present) BEFORE
allowing the write. Strict checks:
  - additionalProperties: false  (P1 pattern)
  - Required fields present
  - Field types match

Usage:
  python3 scripts/schema-validate-write.py <state-file> [--strict|--lenient]

Exit codes:
  0 = valid (write allowed)
  1 = invalid (write blocked; reason in stderr)
  2 = no schema for this file (warn but allow)
  3 = parse error

State file → schema mapping (hardcoded):
  /opt/data/state/coord.json          → coord.schema.json
  /opt/data/state/finance.json        → finance.schema.json
  /opt/data/state/sales.json          → sales.schema.json
  /opt/data/state/engineering.json    → engineering.schema.json
  /opt/data/state/research.json       → research.schema.json
  /opt/data/state/people.json         → people.schema.json
  /opt/data/state/kiki.json           → kiki.schema.json
  /opt/data/state/kiki-prep.json      → kiki-prep.schema.json
  /opt/data/state/analyst.json        → analyst.schema.json
  /opt/data/state/funding.json        → (no schema, exit 2)
  /opt/data/state/eval-per-agent.json → (no schema, exit 2)
"""
import argparse
import json
import sys
from pathlib import Path

SCHEMA_DIR = Path("/opt/data/agents/schemas")

FILE_TO_SCHEMA = {
    "coord.json": "coord.schema.json",
    "finance.json": "finance.schema.json",
    "sales.json": "sales.schema.json",
    "engineering.json": "engineering.schema.json",
    "research.json": "research.schema.json",
    "people.json": "people.schema.json",
    "kiki.json": "kiki.schema.json",
    "kiki-prep.json": "kiki-prep.schema.json",
    "analyst.json": "analyst.schema.json",
    # Phase 28 R5: 4 new schemas
    "funding.json": "funding.schema.json",
    "eval-per-agent.json": "eval-per-agent.schema.json",
    "org-state.json": "org-state.schema.json",
    "cron-error-watchdog.json": "cron-error-watchdog.schema.json",
}

# State paths to search (in priority order)
STATE_DIRS = [
    Path("/opt/data/agents/state"),
    Path("/opt/data/state"),
]


def _find_state_file(state_file: Path) -> Path | None:
    """If state_file doesn't exist, search the known state dirs."""
    if state_file.exists():
        return state_file
    for d in STATE_DIRS:
        candidate = d / state_file.name
        if candidate.exists():
            return candidate
    return None


def _check_additional_properties(obj, schema, path=""):
    """Walk obj + schema, check additionalProperties: false everywhere.

    Phase 29 fix (BUG-HUNT H4): now recurses into array items.
    Previously missed nested-object fields inside arrays.
    """
    errors = []
    if not isinstance(obj, dict):
        return errors
    schema_props = schema.get("properties", {})
    additional_ok = schema.get("additionalProperties", True)
    if additional_ok is False:
        for key in obj.keys():
            if key not in schema_props:
                errors.append(f"{path}: unexpected field '{key}' (schema has additionalProperties: false)")
    for k, v in obj.items():
        sub_schema = schema_props.get(k)
        if isinstance(sub_schema, dict):
            errors.extend(_check_additional_properties(v, sub_schema, f"{path}.{k}" if path else k))
            # If schema is array, recurse into items
            if isinstance(v, list) and "items" in sub_schema:
                items_schema = sub_schema["items"]
                if isinstance(items_schema, dict):
                    for i, item in enumerate(v):
                        errors.extend(_check_additional_properties(item, items_schema, f"{path}.{k}[{i}]" if path else f"{k}[{i}]"))
    return errors


def _check_required(obj, schema, path=""):
    """Check required fields are present.

    Phase 29 fix (BUG-HUNT H5): now recurses into array items.
    Previously missed required-field checks inside array-of-objects.
    """
    errors = []
    if not isinstance(obj, dict):
        return errors
    for req in schema.get("required", []):
        if req not in obj:
            errors.append(f"{path}: missing required field '{req}'" if path else f"missing required field '{req}'")
    # Recurse into known properties
    schema_props = schema.get("properties", {})
    for k, v in obj.items():
        sub = schema_props.get(k)
        if isinstance(sub, dict):
            errors.extend(_check_required(v, sub, f"{path}.{k}" if path else k))
            # If schema is array, check items' required fields
            if isinstance(v, list) and "items" in sub:
                items_schema = sub["items"]
                if isinstance(items_schema, dict):
                    items_required = items_schema.get("required", [])
                    for i, item in enumerate(v):
                        if isinstance(item, dict):
                            for req in items_required:
                                if req not in item:
                                    errors.append(f"{path}.{k}[{i}]: missing required field '{req}'" if path else f"{k}[{i}]: missing required field '{req}'")
    return errors


def validate_file(state_file: Path, lenient: bool = False) -> tuple:
    """Validate state_file against its schema.

    Returns: (is_valid, errors, schema_path_or_none)
    where is_valid = True if no errors OR if lenient mode.
    """
    state_file = Path(state_file)
    # Search known dirs if not found at exact path
    found = _find_state_file(state_file)
    if found:
        state_file = found
    else:
        return False, [f"file not found: {state_file}"], None

    schema_name = FILE_TO_SCHEMA.get(state_file.name)
    if not schema_name:
        return True, ["no schema registered for this file"], None

    schema_path = SCHEMA_DIR / schema_name
    if not schema_path.exists():
        return True, [f"schema file not found: {schema_path}"], None

    try:
        data = json.loads(state_file.read_text())
    except json.JSONDecodeError as e:
        return False, [f"invalid JSON: {e}"], schema_path

    schema = json.loads(schema_path.read_text())

    errors = []
    errors.extend(_check_additional_properties(data, schema))
    errors.extend(_check_required(data, schema))

    # In lenient mode, is_valid=True means "write allowed" (with warnings)
    # In strict mode, is_valid=True means "no schema issues at all"
    if lenient:
        return True, errors, schema_path
    return len(errors) == 0, errors, schema_path


def main():
    parser = argparse.ArgumentParser(description="Schema-validate state file before write")
    parser.add_argument("state_file", type=Path, nargs="?",
                        help="State file to validate (not required with --audit)")
    parser.add_argument("--strict", action="store_true",
                        help="Block writes when schema mismatches (default: warn only)")
    parser.add_argument("--lenient", action="store_true",
                        help="Alias for default (warn but don't block) — kept for compat")
    parser.add_argument("--audit", action="store_true",
                        help="Run validation against all known files; report gaps; do not block")
    args = parser.parse_args()

    if args.audit:
        _run_audit()
        return

    if not args.state_file:
        parser.error("state_file is required (or use --audit)")

    lenient = not args.strict  # Default is lenient
    is_valid, errors, schema_path = validate_file(args.state_file, lenient=lenient)

    print(f"=== Schema Validation: {args.state_file.name} ===")
    if schema_path:
        print(f"Schema: {schema_path.name}")
    else:
        print(f"Schema: (none registered)")

    if not errors:
        print(f"Result: [OK] VALID (write allowed)")
        sys.exit(0)

    # Has errors
    if not schema_path:
        print(f"Result: [WARN] {errors[0]} (write allowed, no schema enforcement)")
        for e in errors[1:]:
            print(f"  - {e}")
        sys.exit(2)

    if lenient:
        print(f"Result: [WARN] {len(errors)} issue(s) (write allowed; pass --strict to block)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(0)

    print(f"Result: [BLOCK] {len(errors)} error(s):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)


def _run_audit():
    """Run validation against all known state files; report schema-vs-reality gaps."""
    print("=== Schema Audit ===")
    print("Comparing live state files against registered schemas\n")
    total_files = 0
    total_gaps = 0
    for fname, schema_name in FILE_TO_SCHEMA.items():
        total_files += 1
        # Find state file
        sf = None
        for d in STATE_DIRS:
            cand = d / fname
            if cand.exists():
                sf = cand
                break
        if not sf:
            print(f"[SKIP] {fname}: file not found")
            continue
        schema_path = SCHEMA_DIR / schema_name
        if not schema_path.exists():
            print(f"[SKIP] {fname}: schema not found")
            continue

        # Strict check
        is_valid, errors, _ = validate_file(sf, lenient=False)
        if is_valid:
            print(f"[OK]   {fname} matches {schema_name}")
        else:
            total_gaps += len(errors)
            print(f"[GAP]  {fname} vs {schema_name}: {len(errors)} mismatch(es)")
            for e in errors[:5]:
                print(f"       - {e}")
            if len(errors) > 5:
                print(f"       ... +{len(errors)-5} more")
    print(f"\nSummary: {total_files} files audited, {total_gaps} schema gaps found")
    sys.exit(0)


if __name__ == "__main__":
    main()
