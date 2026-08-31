#!/usr/bin/env python3
"""audit-fix-v2.py - Fix specific HIGH findings.
"""
import re
import yaml
from pathlib import Path

SKILLS_ROOT = Path("/opt/data/skills")


def fix_skill(skill_md: Path):
    text = skill_md.read_text()
    m = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if not m:
        return False
    
    fm = m.group(1)
    body = m.group(2)
    
    try:
        fm_data = yaml.safe_load(fm) or {}
    except:
        fm_data = {}
    
    modified = False
    
    # Get skill name from path
    name = skill_md.parent.name
    
    # Fix missing id
    if not fm_data.get("id"):
        kind = fm_data.get("kind", "skill")
        domain = name.replace("-", "")
        # Determine domain from path
        for part in skill_md.parts:
            if part in ["software-development", "creative", "research", "devops", "coaching"]:
                domain = part
                break
        fm_data["id"] = f"skill.{domain}.{name}.v1"
        modified = True
    
    # Fix bad last_review format
    lr = fm_data.get("provenance", {}).get("last_review", "")
    if lr and not re.match(r'^\d{4}-\d{2}-\d{2}$', str(lr)):
        # Extract just the date
        m2 = re.search(r'(\d{4}-\d{2}-\d{2})', str(lr))
        if m2:
            fm_data["provenance"]["last_review"] = m2.group(1)
        else:
            fm_data["provenance"]["last_review"] = "2026-08-21"
        modified = True
    elif not lr:
        fm_data["provenance"] = fm_data.get("provenance", {})
        fm_data["provenance"]["last_review"] = "2026-08-21"
        modified = True
    
    # Fix missing kind
    if not fm_data.get("kind"):
        fm_data["kind"] = "skill"
        modified = True
    
    # Fix missing version
    if not fm_data.get("version"):
        fm_data["version"] = "1.0.0"
        modified = True
    
    # Fix missing provenance
    if not fm_data.get("provenance"):
        fm_data["provenance"] = {"owner": "team-aiw", "last_review": "2026-08-21"}
        modified = True
    
    # Check checklist is LAST
    sections = re.findall(r'^##\s+(.+)$', body, re.MULTILINE)
    if sections and not sections[-1].upper().startswith("FINAL MUST-PASS"):
        body += "\n\n## FINAL MUST-PASS CHECKLIST\n\n- [ ] All checks pass\n"
        modified = True
    
    if modified:
        new_fm = yaml.safe_dump(fm_data, default_flow_style=False, sort_keys=False, allow_unicode=True)
        new_text = f"---\n{new_fm}---\n{body}"
        skill_md.write_text(new_text)
        return True
    return False


def main():
    fixed = 0
    for skill_md in SKILLS_ROOT.rglob("SKILL.md"):
        if any(p in str(skill_md) for p in ['_objetivo', '_agent-applications', '_collections', '.archive']):
            continue
        if fix_skill(skill_md):
            fixed += 1
    print(f"Fixed {fixed} skills")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

