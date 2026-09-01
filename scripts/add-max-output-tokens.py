#!/usr/bin/env python3
"""Add max_output_tokens: 800 to all PROMPT.md frontmatter.

Tier-aware insertion: places max_output_tokens AFTER parent_spec (added
by Tier-B8) and BEFORE the closing --- marker.

Idempotent -- safe to re-run.

v2 fix 2026-09-02 (per Phase Kernel WS-1 item 4 / DEMIURGE-092):
The original v1 (commit fffd7c4) returned (prefix, fm_text, suffix) from
extract_frontmatter() and then wrote prefix + new_fm + suffix -- DISCAR-
DING everything after the closing --- separator. This silently trun-
cated 72 of 76 PROMPT.md files (each lost its body). See:
  analysis/INCIDENT-2026-09-01-PROMPT-TRUNCATION.md
  tests/test_add_max_output_tokens.py::test_handles_well_formed_single_block
  (the test that would have caught this was skipped as "implementation
   detail" -- per Phase Kernel brief R1, a skipped test is a failing test)

v2 fix: extract_frontmatter() now returns 4-tuple (prefix, fm_text,
suffix, body). process_file() writes prefix + new_fm + suffix + body --
so the body is preserved across round-trips.
"""
import re
import sys
from pathlib import Path

ROOT = Path("/opt/data/agents-v2/aiw-org-clone")
TARGET_VALUE = 800
TARGET_KEY = "max_output_tokens"


def find_prompt_files(root: Path) -> list[Path]:
    return sorted(root.rglob("PROMPT.md"))


def extract_frontmatter(content: str) -> tuple[str, str, str, str] | None:
    """Return (prefix '---\\n', fm_text, suffix '\\n---\\n', body) or None.

    v2 fix: also captures the body so process_file() can preserve it. The
    previous v1 discarded the body. This was the root cause of the
    2026-09-01 prompt-body destruction incident.

    Slice math explained:
      content[0:3]   = "---"           the opening delimiter (3 chars)
      content[3]     = "\n"             newline that ENDS the opening line
      content[4:mstart]              frontmatter (YAML, no leading \n)
      content[mstart:mend] = "\n---\n"  the closing delimiter (newline + --- + newline)
      content[mend:]                 the body

    To keep the math simple, we slice from content[3:] and treat that as
    "everything after opening ---\\n". The first character of that slice
    is the leading \\n of the frontmatter-block, but the YAML block
    boundaries don't care about leading whitespace.
    """
    if not content.startswith("---"):
        return None
    # IMPORTANT: skip past the opening "---\n" (offsets 0-3). Anything
    # before that is not frontmatter.
    m = re.search(r"\n---\n", content[4:])
    if not m:
        return None
    prefix = "---\n"
    # content[4:] slice begins with the frontmatter (no leading \n).
    # The closing \n is part of m.group() = "\n---\n".
    # fm_text ends just BEFORE the closing \n; it has no trailing newline.
    fm_text = content[4 : 4 + m.start()]
    suffix = "\n---\n"  # standard closing delimiter
    body = content[4 + m.end() :]  # everything after closing --- + \n
    return (prefix, fm_text, suffix, body)


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

    prefix, fm_text, suffix, body = parts
    if has_target(fm_text):
        return "present"

    new_fm = insert_target(fm_text)
    # v2 fix: include body in the new content. The previous version did
    # `prefix + new_fm + suffix` and discarded body. That destroyed 72
    # PROMPT.md bodies in fffd7c4.
    new_content = prefix + new_fm + suffix + body
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
