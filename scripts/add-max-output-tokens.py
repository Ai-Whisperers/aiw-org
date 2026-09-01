#!/usr/bin/env python3
"""Add max_output_tokens: 800 to all PROMPT.md frontmatter.

Tier-aware insertion: places max_output_tokens AFTER parent_spec (added
by Tier-B8) and BEFORE the closing --- marker.

Idempotent — safe to re-run. Skips files with malformed frontmatter.
"""
import re
import sys
from pathlib import Path

ROOT = Path("/opt/data/agents-v2/aiw-org-clone")
TARGET_VALUE = 800
TARGET_KEY = "max_output_tokens"


def find_prompt_files(root: Path) -> list[Path]:
    return sorted(root.rglob("PROMPT.md"))


def extract_frontmatter(content: str) -> tuple[str, str, str] | None:
    """Return (prefix '---\n', fm_text, suffix '\n---\n') or None."""
    if not content.startswith("---"):
        return None
    m = re.search(r"\n---\s*\n", content[3:])
    if not m:
        return None
    return ("---\n", content[3 : 3 + m.start()], content[3 + m.start() : 3 + m.end()])


def has_target(fm_text: str) -> bool:
    return bool(re.search(rf"^{TARGET_KEY}\s*:", fm_text, re.MULTILINE))


def insert_target(fm_text: str) -> str:
    """Insert max_output_tokens: 800 after parent_spec if present, else at end."""
    if not fm_text.endswith("\n"):
        fm_text += "\n"

    # If parent_spec exists, insert immediately after it
    parent_spec_re = re.compile(r"^(parent_spec\s*:.*\n)", re.MULTILINE)
    m = parent_spec_re.search(fm_text)
    if m:
        insertion = f"{TARGET_KEY}: {TARGET_VALUE}\n"
        return fm_text[: m.end()] + insertion + fm_text[m.end() :]

    # Fallback: append at end
    return fm_text + f"{TARGET_KEY}: {TARGET_VALUE}\n"


def process_file(path: Path) -> str:
    try:
        content = path.read_text()
    except Exception as e:
        return f"skipped:read-error:{e}"

    parts = extract_frontmatter(content)
    if parts is None:
        return "skipped:no-frontmatter"

    prefix, fm_text, suffix = parts
    if has_target(fm_text):
        return "present"

    new_fm = insert_target(fm_text)
    new_content = prefix + new_fm + suffix
    try:
        path.write_text(new_content)
        return "added"
    except Exception as e:
        return f"skipped:write-error:{e}"


def main() -> int:
    files = find_prompt_files(ROOT)
    added = present = skipped = 0
    for f in files:
        rel = f.relative_to(ROOT)
        result = process_file(f)
        if result == "added":
            added += 1
            print(f"  + {rel}")
        elif result == "present":
            present += 1
        else:
            skipped += 1
            print(f"  ! {rel}: {result}", file=sys.stderr)
    print(f"\nSummary: added={added} present={present} skipped={skipped}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())