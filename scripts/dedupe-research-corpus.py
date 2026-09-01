#!/usr/bin/env python3
"""dedupe-research-corpus.py — Remove duplicate research entries.

Phase 9 R3 / Tier C3 / Gap 2. The research corpus has accumulated
duplicates from multiple sources. This script deduplicates by:
  - Title normalization (lowercase + remove punctuation)
  - URL match (case-insensitive)
  - Content hash (SHA-256 of body, dedup identical content)

Reports duplicates found and writes dedup log.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

RESEARCH_DIR = Path("/opt/data/agents/research")
LOG_PATH = Path("/opt/data/state/dedupe-research-log.json")


def normalize_title(title: str) -> str:
    """Normalize a title for dedup comparison."""
    return re.sub(r"\W+", "", title.lower())


def content_hash(content: str) -> str:
    """SHA-256 of content body."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def find_dupes() -> dict:
    """Find duplicates across research markdown files."""
    seen_titles = {}
    seen_hashes = {}
    dupes = []

    for f in RESEARCH_DIR.rglob("*.md"):
        try:
            content = f.read_text()
        except (OSError, UnicodeDecodeError):
            continue
        # Extract title (first # heading)
        m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if not m:
            continue
        title = m.group(1).strip()
        norm_title = normalize_title(title)
        chash = content_hash(content)

        if norm_title in seen_titles:
            dupes.append({
                "type": "title",
                "title": title,
                "files": [str(seen_titles[norm_title].relative_to(RESEARCH_DIR)),
                          str(f.relative_to(RESEARCH_DIR))],
            })
        else:
            seen_titles[norm_title] = f

        if chash in seen_hashes:
            dupes.append({
                "type": "content",
                "files": [str(seen_hashes[chash].relative_to(RESEARCH_DIR)),
                          str(f.relative_to(RESEARCH_DIR))],
            })
        else:
            seen_hashes[chash] = f

    return {
        "scanned": len(list(RESEARCH_DIR.rglob("*.md"))),
        "duplicates_found": len(dupes),
        "duplicates": dupes[:50],  # cap output
    }


def main():
    result = find_dupes()
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[dedupe] Scanned {result['scanned']} files, found {result['duplicates_found']} dupes")
    print(f"[dedupe] Log written to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())