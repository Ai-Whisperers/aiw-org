#!/usr/bin/env python3
"""lint-prompts.py — Layer 2.4 enforcer.

Lints all PROMPT.md files in aiw-org for:
- Required fields: name, version, owner (schedule optional)
- Layer 3 recommended fields: layer, topology, archetype
- hard_stops schema: each stop has 'action' (str), 'require_approval' (bool)
- Optional fields: composition (list), negative_examples (list), transfer_targets (list), time_scale (str)

Exits 0 if all pass; 1 if any fail. Per-agent output: name + issues list.

No external deps — uses manual frontmatter parser.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path("/opt/data/agents")
REQUIRED_FIELDS = {"name", "version", "owner"}
RECOMMENDED_LAYER3 = {"layer", "topology", "archetype"}
VALID_TOPOLOGIES = {"stream-aligned", "platform", "enabling", "complicated-subsystem"}
VALID_LAYERS = {"atomic", "business", "governance"}
VALID_ARCHETYPES = {"team-lead", "architect", "solver", "right-hand", "specialist"}


def parse_frontmatter(content: str):
    """Parse simple YAML-like frontmatter into dict. Returns (dict, error_list)."""
    issues = []
    if not content.startswith("---"):
        issues.append("missing-frontmatter")
        return None, issues
    # Find closing ---
    m = re.search(r"\n---\n", content[3:])
    if not m:
        issues.append("malformed-frontmatter")
        return None, issues
    fm_text = content[3:3 + m.start()]
    fm = {}
    current_key = None
    current_list = None
    list_indent_re = re.compile(r"^\s+-\s+(.*)$")
    for raw_line in fm_text.split("\n"):
        if not raw_line.strip():
            continue
        # Comment
        if raw_line.strip().startswith("#"):
            continue
        # List item under current_key
        lm = list_indent_re.match(raw_line)
        if lm and current_list is not None:
            current_list.append(lm.group(1).strip().strip('\"\'').rstrip(','))
            continue
        # key: value
        if ":" in raw_line and not raw_line.startswith(" "):
            k, v = raw_line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('\"\'').rstrip(',')
            if not v:
                # Start of a list
                current_key = k
                current_list = []
                fm[k] = current_list
            elif v.lower() in ("true", "false"):
                fm[k] = (v.lower() == "true")
            elif re.match(r"^-?\d+$", v):
                fm[k] = int(v)
            else:
                fm[k] = v
                current_key = None
                current_list = None
    return fm, issues


def lint_one(prompt_path: Path):
    """Return list of issues for one PROMPT.md. Empty list = pass."""
    issues = []
    try:
        content = prompt_path.read_text()
    except Exception as e:
        return [f"read-error: {e}"]

    fm, fm_issues = parse_frontmatter(content)
    issues.extend(fm_issues)
    if fm is None:
        return issues

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in fm:
            issues.append(f"missing-required:{field}")
        elif not fm[field]:
            issues.append(f"empty-required:{field}")

    # Layer 3 recommended fields
    for field in RECOMMENDED_LAYER3:
        if field not in fm:
            issues.append(f"missing-recommended:{field}")

    # Validate layer values
    if "layer" in fm and fm["layer"] not in VALID_LAYERS:
        issues.append(f"invalid-layer:{fm['layer']}")

    # Validate topology values
    if "topology" in fm and fm["topology"] not in VALID_TOPOLOGIES:
        issues.append(f"invalid-topology:{fm['topology']}")

    # Validate archetype values
    if "archetype" in fm and fm["archetype"] not in VALID_ARCHETYPES:
        issues.append(f"invalid-archetype:{fm['archetype']}")

    # Validate hard_stops schema
    if "hard_stops" in fm:
        hs = fm["hard_stops"]
        if isinstance(hs, list):
            for i, stop in enumerate(hs):
                if not isinstance(stop, dict):
                    issues.append(f"hard-stops[{i}]:not-dict")
                    continue
                if "action" not in stop:
                    issues.append(f"hard-stops[{i}]:missing-action")
                elif not isinstance(stop["action"], str):
                    issues.append(f"hard-stops[{i}]:action-not-string")
                if "require_approval" not in stop:
                    issues.append(f"hard-stops[{i}]:missing-require_approval")
                elif not isinstance(stop["require_approval"], bool):
                    issues.append(f"hard-stops[{i}]:require_approval-not-bool")

    # Validate composition (list of strings)
    if "composition" in fm and not isinstance(fm["composition"], list):
        issues.append("composition-not-list")

    return issues


def find_all_prompts():
    """Find all PROMPT.md files in the repo, excluding archive + venv."""
    prompts = []
    for root, dirs, files in os.walk(ROOT):
        if "agents-v2" in root or "/archive" in root or "/.venv" in root or "/.git" in root:
            continue
        for f in files:
            if f == "PROMPT.md":
                prompts.append(Path(root) / f)
    return sorted(prompts)


def main():
    prompts = find_all_prompts()
    if not prompts:
        print("WARN: no PROMPT.md files found", file=sys.stderr)
        return 0

    print(f"Linting {len(prompts)} PROMPT.md files...")
    print()

    failures = []
    total_issues = 0
    for p in prompts:
        issues = lint_one(p)
        if issues:
            failures.append((p, issues))
            total_issues += len(issues)
        rel = p.relative_to(ROOT)
        status = "✓" if not issues else "✗"
        print(f"  {status} {rel}")
        for issue in issues:
            print(f"      - {issue}")

    print()
    print(f"Summary: {len(prompts) - len(failures)} pass, {len(failures)} fail")
    print(f"Total issues: {total_issues}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
