#!/usr/bin/env python3
"""Schema migration tool — auto-generate JSON schemas from live state files.

Built as Phase 30 R1 (Tier G6 - Schema migration tooling).

For each known state file, reads the current JSON and generates a draft
schema. Useful for:
  - New state files that don't yet have a schema
  - Out-of-date schemas that need to be refreshed
  - Diffing actual vs expected shape

Outputs drafts to /tmp/schema-drafts/ for review before committing.
NEVER overwrites existing schemas without --force.

Usage:
    python3 scripts/schema-migration.py --all           # generate drafts for all
    python3 scripts/schema-migration.py funding.json    # one file
    python3 scripts/schema-migration.py --outdated      # only files with gaps
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_DIR = Path("/opt/data/agents/schemas")
STATE_DIRS = [
    Path("/opt/data/agents/state"),
    Path("/opt/data/state"),
]
OUTPUT_DIR = Path("/tmp/schema-drafts")


# Mapping of state file → schema file
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
    "funding.json": "funding.schema.json",
    "eval-per-agent.json": "eval-per-agent.schema.json",
    "org-state.json": "org-state.schema.json",
    "cron-error-watchdog.json": "cron-error-watchdog.json",
}


def find_state_file(name: str) -> Path | None:
    """Find state file by name across known dirs."""
    for d in STATE_DIRS:
        path = d / name
        if path.exists():
            return path
    return None


def infer_type(value) -> str:
    """Infer JSON Schema type from a Python value."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "null"


def generate_schema_from_state(state_file: Path, schema_name: str) -> dict:
    """Walk state file and generate a draft schema.

    For top-level object: emits `properties` for each field.
    For nested objects: emits nested properties (depth-limited).
    For arrays: emits `type: array` with items.type from first element.
    """
    data = json.loads(state_file.read_text())
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": f"agent.state — {schema_name.replace('.schema.json', '')}",
        "description": f"Auto-generated from {state_file.name} at {datetime.now(timezone.utc).isoformat()}. Review before committing.",
        "type": "object",
        "properties": {},
        "additionalProperties": True,  # lenient default; tighten after review
    }

    if isinstance(data, dict):
        # Find required fields (those without None values)
        required = []
        for k, v in data.items():
            prop = _infer_property(v)
            schema["properties"][k] = prop
            if v is not None:
                required.append(k)
        if required:
            schema["required"] = required

    return schema


def _infer_property(value, depth: int = 0, max_depth: int = 3) -> dict:
    """Infer a JSON Schema property from a value."""
    if depth >= max_depth:
        return {"type": "object", "additionalProperties": True}

    if value is None:
        return {"type": ["string", "null"]}

    if isinstance(value, bool):
        return {"type": "boolean"}

    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}

    if isinstance(value, str):
        # Detect ISO timestamps
        if "T" in value and ("Z" in value or "+" in value or "-" in value[10:]):
            return {"type": ["string", "null"], "format": "date-time"}
        return {"type": "string"}

    if isinstance(value, list):
        items_schema = {"type": "object", "additionalProperties": True}
        if value and isinstance(value[0], dict):
            # Use first item as schema template
            items_schema = _infer_property(value[0], depth + 1, max_depth)
        return {"type": "array", "items": items_schema}

    if isinstance(value, dict):
        properties = {}
        for k, v in value.items():
            properties[k] = _infer_property(v, depth + 1, max_depth)
        return {"type": "object", "properties": properties, "additionalProperties": True}

    return {"type": "null"}


def main():
    parser = argparse.ArgumentParser(description="Schema migration tool")
    parser.add_argument("--all", action="store_true", help="Generate drafts for all files")
    parser.add_argument("--outdated", action="store_true",
                        help="Generate drafts only for files where schema has gaps")
    parser.add_argument("files", nargs="*", help="Specific files (e.g. funding.json)")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.all:
        targets = list(FILE_TO_SCHEMA.keys())
    elif args.outdated:
        # Find files where schema has gaps (vs current state)
        targets = []
        for state_name, schema_name in FILE_TO_SCHEMA.items():
            sf = find_state_file(state_name)
            if not sf:
                continue
            schema_path = SCHEMA_DIR / schema_name
            if not schema_path.exists():
                targets.append(state_name)
                continue
            # Quick gap check: try to validate current state against schema
            from schema_validate_write import validate_file
            with open(sf) as f:
                data = json.load(f)
            valid, errors, _ = validate_file(sf)
            if not valid:
                targets.append(state_name)
        # Note: import only on demand to avoid hard dependency
    elif args.files:
        targets = args.files
    else:
        parser.print_help()
        return

    print(f"=== Schema Migration Tool ===")
    print(f"Targets: {len(targets)} files\n")

    generated = 0
    for state_name in targets:
        sf = find_state_file(state_name)
        if not sf:
            print(f"  SKIP {state_name}: not found in any state dir")
            continue

        schema_name = FILE_TO_SCHEMA.get(state_name)
        if not schema_name:
            schema_name = state_name.replace(".json", ".schema.json")

        schema = generate_schema_from_state(sf, schema_name)
        out_path = OUTPUT_DIR / schema_name
        out_path.write_text(json.dumps(schema, indent=2))
        print(f"  GENERATED {state_name} -> {out_path}")
        generated += 1

    print(f"\n=== {generated} drafts written to {OUTPUT_DIR} ===")
    print(f"Review each draft before committing to {SCHEMA_DIR}/")


if __name__ == "__main__":
    main()
