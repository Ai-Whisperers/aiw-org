#!/usr/bin/env python3
"""thread-aiw-root.py — Thread AIW_ROOT env var through one script at a time.

DEMIURGE-098 (Phase Kernel brief WS-3 item 1) helper.

Per-file AST-based threading that:
1. Finds `Path("/opt/data/X")` calls via AST (robust to multiline, escaped
   quotes, and indentation in surrounding code)
2. Replaces with the matching `_paths` constant (STATE, AGENTS, HERMES, CRON)
3. Adds a 4-line sys.path bootstrap preamble + `from _paths import ...`
4. Skips unknown sub-paths and script-specific ROOT constants
5. DRY-RUN by default; --apply performs + auto-rolls-back on test failure

Auto-rollback design: after each file is modified, pytest is run on
the full suite. If exit code != 0, the file is restored from backup.
This prevents the cascading-batch failure mode we saw earlier.

Usage:
    python3 scripts/thread-aiw-root.py scripts/observability/agent-tracer.py
        # dry-run, prints planned changes
    python3 scripts/thread-aiw-root.py --apply scripts/observability/agent-tracer.py
        # applies, runs pytest, rolls back on failure
"""
import argparse
import ast
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TESTS = REPO / "tests"

# Known /opt/data path -> constant name from _paths
PATH_MAP = {
    "/opt/data/state": "STATE",
    "/opt/data/agents": "AGENTS",
    "/opt/data/.hermes": "HERMES",
    "/opt/data/.hermes/cron": "CRON",
}

# Sub-paths we DON'T touch (script-specific: their own ROOT or scripts/)
SKIP_SUBPATHS = ("/opt/data/cron/", "/opt/data/db/", "/opt/data/agents-v2/")


def detect(path: Path) -> tuple[list, str]:
    """Return list of AST-detected Path() calls that need threading."""
    src = path.read_text()
    tree = ast.parse(src)
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            fn_name = (fn.id if isinstance(fn, ast.Name)
                       else fn.attr if isinstance(fn, ast.Attribute)
                       else None)
            if fn_name != "Path":
                continue
            if not (len(node.args) >= 1
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)):
                continue
            arg = node.args[0].value
            if arg == "/opt/data":
                continue  # root - leave as-is
            if not arg.startswith("/opt/data"):
                continue
            if arg in PATH_MAP:
                found.append((node.lineno,
                              f'Path("{arg}")',
                              PATH_MAP[arg],
                              "Path_arg"))
                continue
            # Skip known script-specific paths
            if any(arg.startswith(sp) for sp in SKIP_SUBPATHS):
                continue
            # Unknown sub-path: skip silently for now (preserve safety)
            continue
    return found, src


def make_bootstrap_preamble(syms: str) -> str:
    """Generate the 4-line preamble that bootstraps sys.path before
    importing from _paths. Required because scripts/observability/*.py
    runs in a CWD that is one level deeper than scripts/_paths.py.

    The preamble uses mangled names (`_sys_bootstrap_098`) so it cannot
    collide with any other import the script already has.
    """
    return (
        "\n# --- AIW_ROOT path bootstrap (DEMIURGE-098) ---\n"
        "import sys as _sys_bootstrap_098\n"
        "from pathlib import Path as _Path_bootstrap_098\n"
        "_PY_PATHS_ROOT = _Path_bootstrap_098(__file__).resolve().parent.parent\n"
        "if str(_PY_PATHS_ROOT) not in _sys_bootstrap_098.path:\n"
        "    _sys_bootstrap_098.path.insert(0, str(_PY_PATHS_ROOT))\n"
        f"from _paths import {syms}\n"
        "# --- end bootstrap ---\n"
    )


def apply_to_source(src: str, found: list) -> str:
    """Replace each known Path() call with the constant name.

    Walks replacements in REVERSE line order so byte offsets remain valid.
    Skips multi-line Path() calls (rare; would need complex AST rewrite).
    """
    items = sorted(found, key=lambda x: x[0], reverse=True)
    lines = src.split("\n")
    for lineno, original, name, _kind in items:
        idx = lineno - 1
        if idx >= len(lines):
            continue
        line = lines[idx]
        if original not in line:
            print(f"WARNING: line {lineno} did not contain {original!r}; skipping")
            continue
        lines[idx] = line.replace(original, name)
    return "\n".join(lines)


def ensure_preamble(content: str, needed_syms: str) -> tuple[str, bool]:
    """Insert the 4-line bootstrap preamble + `from _paths import ...`
    AFTER the last module-level import (lines with no leading whitespace).

    Returns (new_content, had_existing).

    Strategy (simplified, robust):
      Pass 1 — split content into segments: the imports block + the
                rest. Detection = walk lines; the imports block ends
                at the first non-indented, non-import module-level line.
      Pass 2 — split imports block from "the line that follows" and
                "the rest of the file" by simply identifying the
                boundary.
      Pass 3 — rejoin: imports_block + preamble + rest_of_file.
    """
    if make_bootstrap_preamble(needed_syms).strip() in content:
        return content, True  # already there

    preamble = make_bootstrap_preamble(needed_syms)

    lines = content.split("\n")
    insert_at = 0  # default: at the very top (no imports found)
    found_import = False
    # Docstring tracking: skip lines between triple-quote markers
    # (top-level Python module docstrings)
    in_docstring = False
    docstring_quote = None  # '"""' or "'''"

    for i, ln in enumerate(lines):
        s = ln.rstrip()
        # Skip blank lines and comments (also shebangs like #!/usr/bin/env)
        if not s or s.startswith("#"):
            continue
        # Docstring handling: track triple-quote state at the module level
        # Don't treat docstring content as module-level code
        if in_docstring:
            # Check if this line ENDS the docstring
            if docstring_quote and docstring_quote in s:
                # End of docstring on this line; flip state
                in_docstring = False
                docstring_quote = None
            continue
        # Detect start of docstring at module level
        # (after no imports seen yet)
        if not found_import and (s.lstrip().startswith('"""')
                                  or s.lstrip().startswith("'''")):
            in_docstring = True
            docstring_quote = s.lstrip()[:3]
            # If single-line docstring (opening and closing on same line)
            if docstring_quote in s[3:]:
                in_docstring = False
                docstring_quote = None
            continue
        if ln.startswith((" ", "\t")):
            # Indented line (function body or nested import).
            continue
        if s.lstrip().startswith(("import ", "from ")):
            # Module-level import — update insert point to AFTER this
            # line. We use the index of the next line as the insertion
            # target so we go after ALL imports, not just the last
            # one we encounter, by overwriting insert_at each time.
            insert_at = i + 1
            found_import = True
        else:
            # First non-import module-level line. The import block
            # is over. Insert now (if we've seen imports).
            if found_import:
                break
            # No imports seen before this line. Either the file is
            # all module-level code (rare; we wouldn't add the preamble),
            # OR we hit a code line before seeing imports because
            # the loop is processing a CLASS body or similar (rare).
            # In both cases, return unchanged rather than corrupt.
            return content, False

    # If we never saw imports, return unchanged
    if not found_import:
        return content, False

    # Adjust insert_at to account for blank lines that might follow
    # the last import. We want the preamble IMMEDIATELY after the
    # last import (no extra blank line).
    while (insert_at > 0
           and insert_at < len(lines)
           and not lines[insert_at - 1].rstrip()):
        # Previous line is blank; step back to insert BEFORE that blank,
        # i.e. immediately after the import.
        insert_at -= 1

    # Insert the preamble at insert_at
    new_lines = lines[:insert_at] + [preamble] + lines[insert_at:]
    return "\n".join(new_lines), False


def thread_one(path: Path, apply: bool = False) -> tuple[bool, str]:
    """Thread one file. Returns (changed, summary_msg)."""
    if path.name == "_paths.py":
        return False, "skipped: _paths.py is the helper itself"
    if "_sys_bootstrap_098" in path.read_text()[:1500]:
        return False, "skipped: already threaded"

    found, src = detect(path)
    applicable = [f for f in found if f[3] == "Path_arg"
                  and "/" + f[1].split('"')[1].split("/")[1] in PATH_MAP
                  or f[1].split('"')[1] in PATH_MAP]
    # simpler: filter to items whose Path arg value is in PATH_MAP
    applicable = []
    for f in found:
        lineno, original, name, kind = f
        if kind == "Path_arg":
            applicable.append(f)
    if not applicable:
        return False, "no applicable /opt/data/X Path() calls found"

    needed = set(f[2] for f in applicable)
    syms = ", ".join(sorted(needed | {"AIW_ROOT"}))

    rel = path.relative_to(REPO)
    print(f"\n{'=' * 60}\nTHREADING: {rel}\n{'=' * 60}")
    for f in applicable:
        print(f"  L{f[0]:3d}  {f[1]:40s} -> {f[2]}")
    print(f"  Will add bootstrap preamble with: {syms}")

    if not apply:
        return False, f"DRY RUN ({len(applicable)} replacements)"

    # Apply: build new content with replacements + preamble
    new_src = apply_to_source(src, applicable)
    new_src, _had_existing = ensure_preamble(new_src, syms)
    if new_src == src:
        return False, "no-op (no actual changes)"

    backup = path.read_text()
    path.write_text(new_src)
    print(f"\nApplied {len(applicable)} replacements; backup saved")
    print("\nRunning pytest for verification...")
    result = subprocess.run(
        ["/opt/data/.venv/bin/python3", "-m", "pytest",
         "tests/", "-q", "--tb=line"],
        cwd=str(REPO), capture_output=True, text=True, timeout=180,
    )
    last_line = result.stdout.splitlines()[-1] if result.stdout else ""
    print(f"  pytest: {last_line}")
    if result.returncode != 0:
        # AUTO-ROLLBACK
        path.write_text(backup)
        print(f"  !! ROLLBACK: reverted {path.name}")
        return False, f"FAILED pytest, auto-rolled back"
    print(f"  ✓ tests still pass after threading {path.name}")
    return True, f"applied {len(applicable)} replacements, tests pass"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="path to .py file to thread")
    ap.add_argument("--apply", action="store_true",
                    help="actually modify the file (default is dry-run)")
    a = ap.parse_args()
    p = Path(a.file).resolve()
    if not p.exists():
        print(f"FILE NOT FOUND: {p}", file=sys.stderr)
        sys.exit(2)
    if p.suffix != ".py":
        print(f"NOT A .py FILE: {p}", file=sys.stderr)
        sys.exit(2)
    changed, msg = thread_one(p, apply=a.apply)
    print(f"\n{msg}")
    sys.exit(0 if (a.apply and changed) or (not a.apply) else 1)


if __name__ == "__main__":
    main()
