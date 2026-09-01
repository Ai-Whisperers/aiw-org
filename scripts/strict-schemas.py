#!/usr/bin/env python3
"""strict-schemas.py — Apply P1 pattern: additionalProperties: false.

Phase 9 R4 / Risk R5 mitigation. Reads every JSON file in schemas/,
finds every {"type": "object"} NOT having additionalProperties: false,
and adds it.

Pattern (P1):
  {"type": "object", "additionalProperties": false, ...}

Why: LLM prompt injection can mutate state files by including extra
keys. Strict schemas reject unknown keys at validation time, killing
the attack class at the JSON Schema boundary.

Idempotent. Skips non-object top-level. Backups to .bak.
"""
import json
import shutil
from pathlib import Path

ROOT = Path("/opt/data/agents/schemas")
BACKUP = ROOT / ".bak-strict-schemas"


def walk_and_strict(obj, path=""):
    """Recursively set additionalProperties: false on type=object."""
    if isinstance(obj, dict):
        if obj.get("type") == "object":
            ap = obj.get("additionalProperties")
            if ap is not False:
                obj["additionalProperties"] = False
        for k, v in obj.items():
            walk_and_strict(v, path + f".{k}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            walk_and_strict(item, path + f"[{i}]")


def harden(path: Path) -> dict:
    """Harden one schema file. Returns change summary."""
    text = path.read_text()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return {"file": path.name, "error": str(e), "modified": False}
    before = json.dumps(data, sort_keys=True)
    walk_and_strict(data)
    after = json.dumps(data, sort_keys=True)
    modified = before != after
    if modified:
        path.write_text(json.dumps(data, indent=2) + "\n")
    return {
        "file": path.name,
        "modified": modified,
        "objects": sum(1 for line in after.split("\n") if '"type": "object"' in line),
    }


def main():
    BACKUP.mkdir(parents=True, exist_ok=True)
    # Backup all first
    for f in ROOT.glob("*.json"):
        shutil.copy2(f, BACKUP / f.name)
    
    results = []
    for f in sorted(ROOT.glob("*.json")):
        results.append(harden(f))
    modified = [r for r in results if r.get("modified")]
    errors = [r for r in results if r.get("error")]
    print(f"Modified: {len(modified)}, errors: {len(errors)}, total: {len(results)}")
    for r in modified:
        print(f"  + {r['file']} (objects: {r['objects']})")
    for r in errors:
        print(f"  ! {r['file']}: {r['error']}")
    # Cleanup backup if no errors
    if not errors:
        shutil.rmtree(BACKUP, ignore_errors=True)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
