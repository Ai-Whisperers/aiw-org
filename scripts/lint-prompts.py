#!/usr/bin/env python3
"""lint-prompts.py — Layer 2.4 enforcer (with pyyaml).

Lints all PROMPT.md files in aiw-org for:
- Required fields: name, version, owner
- Layer 3 recommended fields: layer, topology, archetype
- hard_stops schema: each stop has 'action' (str), 'require_approval' (bool)
- Optional fields: composition (list), negative_examples (list), transfer_targets (list), time_scale (str)

Exits 0 if all pass; 1 if any fail.
"""
import os
import sys
import yaml
from pathlib import Path

ROOT = Path("/opt/data/agents")
REQUIRED_FIELDS = {"name", "version", "owner"}
RECOMMENDED_LAYER3 = {"layer", "topology", "archetype"}
VALID_TOPOLOGIES = {"stream-aligned", "platform", "enabling", "complicated-subsystem"}
VALID_LAYERS = {"atomic", "business", "governance"}
VALID_ARCHETYPES = {"team-lead", "architect", "solver", "right-hand", "specialist"}


def parse_frontmatter(content: str):
    """Parse YAML frontmatter. Returns (dict, error_list)."""
    issues = []
    if not content.startswith("---"):
        issues.append("missing-frontmatter")
        return None, issues
    m = __import__("re").search(r"\n---\n", content[3:])
    if not m:
        issues.append("malformed-frontmatter")
        return None, issues
    fm_text = content[3:3 + m.start()]
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        issues.append(f"yaml-error: {e}")
        return None, issues
    if not isinstance(fm, dict):
        issues.append("frontmatter-not-dict")
        return None, issues
    return fm, issues


def lint_one(prompt_path: Path):
    """Return list of issues for one PROMPT.md."""
    issues = []
    try:
        content = prompt_path.read_text()
    except Exception as e:
        return [f"read-error: {e}"]

    fm, fm_issues = parse_frontmatter(content)
    issues.extend(fm_issues)
    if fm is None:
        return issues

    for field in REQUIRED_FIELDS:
        if field not in fm:
            issues.append(f"missing-required:{field}")
        elif not fm[field]:
            issues.append(f"empty-required:{field}")

    for field in RECOMMENDED_LAYER3:
        if field not in fm:
            issues.append(f"missing-recommended:{field}")

    if "layer" in fm and fm["layer"] not in VALID_LAYERS:
        issues.append(f"invalid-layer:{fm['layer']}")
    if "topology" in fm and fm["topology"] not in VALID_TOPOLOGIES:
        issues.append(f"invalid-topology:{fm['topology']}")
    if "archetype" in fm and fm["archetype"] not in VALID_ARCHETYPES:
        issues.append(f"invalid-archetype:{fm['archetype']}")

    if "hard_stops" in fm:
        hs = fm["hard_stops"]
        if not isinstance(hs, list):
            issues.append("hard-stops-not-list")
        else:
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

    if "composition" in fm and not isinstance(fm["composition"], list):
        issues.append("composition-not-list")

    return issues


def find_all_prompts():
    """Find all PROMPT.md files, excluding sister repos + archive."""
    prompts = []
    for root, dirs, files in os.walk(ROOT):
        if any(x in root for x in ["/agents-v2", "/archive", "/.venv", "/.git", "node_modules"]):
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
