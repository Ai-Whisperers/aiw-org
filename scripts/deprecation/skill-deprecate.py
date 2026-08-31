#!/usr/bin/env python3
"""skill-deprecate.py — Mark skills as deprecated with 90-day timeline.

Implements Eneve skill deprecation workflow:
1. Mark skill with deprecated: true in frontmatter
2. Add superseded_by field pointing to replacement
3. Keep file for 90 days for backward compatibility
4. After 90 days, archive to skills/.archive/
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

SKILLS_ROOT = Path("/opt/data/skills")
ARCHIVE_DIR = SKILLS_ROOT / ".archive"
DEPR_WINDOW_DAYS = 90


def deprecate_skill(skill_path: Path, superseded_by: str, reason: str = ""):
    """Mark skill as deprecated."""
    if not skill_path.exists():
        print(f"SKIP: {skill_path} (not found)")
        return
    
    text = skill_path.read_text()
    
    # Parse frontmatter
    m = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if not m:
        print(f"SKIP: {skill_path} (no frontmatter)")
        return
    
    fm = m.group(1)
    body = m.group(2)
    
    # Add deprecation fields
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    archive_date = (datetime.now(timezone.utc) + timedelta(days=DEPR_WINDOW_DAYS)).strftime("%Y-%m-%d")
    
    # Replace or add deprecated field
    new_fm = re.sub(r'^deprecated:\s*\S+', 'deprecated: true', fm, flags=re.MULTILINE)
    if 'deprecated' not in new_fm:
        new_fm += f'\ndeprecated: true\nsuperseded_by: {superseded_by}\ndeprecation_started: {today}\narchive_date: {archive_date}\ndeprecation_reason: "{reason}"\n'
    else:
        # Add superseded_by if not present
        if 'superseded_by' not in new_fm:
            new_fm += f'\nsuperseded_by: {superseded_by}\ndeprecation_started: {today}\narchive_date: {archive_date}\n'
    
    # Update last_review
    new_fm = re.sub(r'last_review:\s*\S+', f'last_review: \'{today}\'', new_fm)
    
    new_text = f"---\n{new_fm}---\n{body}"
    skill_path.write_text(new_text)
    print(f"✓ Deprecated {skill_path.parent.name} -> archive {archive_date}")


def check_archived():
    """Move skills past archive_date to .archive/."""
    if not ARCHIVE_DIR.exists():
        return 0
    
    archived = 0
    today = datetime.now(timezone.utc)
    
    for skill_dir in SKILLS_ROOT.iterdir():
        if skill_dir.name in ("_objetivo", "_agent-applications", "_collections", ".archive"):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        
        text = skill_md.read_text()
        m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
        if not m:
            continue
        
        fm = m.group(1)
        archive_date_match = re.search(r'archive_date:\s*(\S+)', fm)
        if not archive_date_match:
            continue
        
        archive_date = archive_date_match.group(1)
        try:
            archive_dt = datetime.strptime(archive_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        
        if today >= archive_dt:
            # Move to archive
            archive_target = ARCHIVE_DIR / skill_dir.name
            archive_target.mkdir(parents=True, exist_ok=True)
            for f in skill_dir.iterdir():
                (archive_target / f.name).write_bytes(f.read_bytes())
            import shutil
            shutil.rmtree(skill_dir)
            archived += 1
            print(f"✓ Archived {skill_dir.name} (past archive_date)")
    
    return archived


def main():
    if len(sys.argv) < 3:
        print("Usage: skill-deprecate.py <skill-name> <superseded-by> [--reason 'why']")
        print("       skill-deprecate.py --archive   # archive expired skills")
        sys.exit(1)
    
    if sys.argv[1] == "--archive":
        n = check_archived()
        print(f"Archived {n} expired skills")
        return
    
    skill_name = sys.argv[1]
    superseded_by = sys.argv[2]
    
    reason = ""
    if "--reason" in sys.argv:
        idx = sys.argv.index("--reason")
        reason = sys.argv[idx + 1]
    
    skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
    deprecate_skill(skill_path, superseded_by, reason)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

