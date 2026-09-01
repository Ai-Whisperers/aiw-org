#!/usr/bin/env python3
"""restore-prompt-bodies.py — Recover PROMPT.md bodies destroyed by bulk frontmatter edits.

Incident: commit fffd7c4 ("cap max_output_tokens: 800 on all 74 PROMPTs") ran
add-max-output-tokens.py, whose extract_frontmatter() never captured the body:

    new_content = prefix + new_fm + suffix    # suffix is the closing "---" only

72 of 76 PROMPT.md files were reduced to frontmatter. Both the repo and the
live host at /opt/data/agents are affected.

There is no single good snapshot. Different prompts were last intact at
different commits (590c6d1, fa160ff, 930a3cc, 505025f, 4c37b0e), so this
script searches each file's own history for its richest version and splices
that body onto the CURRENT frontmatter -- preserving the legitimate
frontmatter work (max_output_tokens, parent_spec, cluster) done since.

DRY-RUN BY DEFAULT. --apply requires --force.

Usage:
    python3 scripts/restore-prompt-bodies.py                 # dry run, prints plan
    python3 scripts/restore-prompt-bodies.py --json          # machine-readable plan
    python3 scripts/restore-prompt-bodies.py --apply --force # write files
    python3 scripts/restore-prompt-bodies.py --verify        # post-restore check

Exit codes: 0 ok, 1 unrecoverable files found, 2 bad invocation.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

MIN_BODY_LINES = 20      # a real prompt body is at least this many lines
SEARCH_DEPTH = 40        # commits of history to search per file


def run(args: list[str]) -> str:
    return subprocess.run(args, capture_output=True, text=True).stdout


def split_frontmatter(text: str) -> tuple[str, str] | None:
    """Return (frontmatter_block_including_delimiters, body) or None.

    Correctly locates the CLOSING delimiter, which is the bug the original
    script got wrong.
    """
    if not text.startswith("---"):
        return None
    rest = text[3:]
    idx = rest.find("\n---")
    if idx == -1:
        return None
    after = rest[idx + 4:]
    nl = after.find("\n")
    if nl == -1:
        return text, ""
    return text[: 3 + idx + 4 + nl + 1], after[nl + 1:]


def body_lines(text: str) -> int:
    parts = split_frontmatter(text)
    body = parts[1] if parts else text
    return len([ln for ln in body.splitlines() if ln.strip()])


def find_best_source(rel: str) -> tuple[str | None, int]:
    """Search this file's history for the version with the largest body."""
    commits = run(["git", "log", f"-{SEARCH_DEPTH}", "--format=%h", "--", rel]).split()
    best_commit, best_n = None, 0
    for c in commits:
        blob = run(["git", "show", f"{c}:{rel}"])
        if not blob:
            continue
        n = body_lines(blob)
        if n > best_n:
            best_commit, best_n = c, n
    return best_commit, best_n


def plan(repo: Path) -> list[dict]:
    out = []
    for path in sorted(repo.rglob("PROMPT.md")):
        if ".git" in path.parts:
            continue
        rel = str(path.relative_to(repo))
        current = path.read_text()
        cur_n = body_lines(current)
        if cur_n >= MIN_BODY_LINES:
            continue
        commit, n = find_best_source(rel)
        out.append({
            "file": rel,
            "current_body_lines": cur_n,
            "source_commit": commit,
            "source_body_lines": n,
            "recoverable": bool(commit) and n >= MIN_BODY_LINES,
        })
    return out


def apply(repo: Path, items: list[dict]) -> tuple[int, int]:
    restored = failed = 0
    for it in items:
        if not it["recoverable"]:
            failed += 1
            continue
        path = repo / it["file"]
        current = path.read_text()
        source = run(["git", "show", f"{it['source_commit']}:{it['file']}"])
        cur_split = split_frontmatter(current)
        src_split = split_frontmatter(source)
        if not cur_split or not src_split:
            failed += 1
            continue
        # Keep CURRENT frontmatter (has the legitimate new fields),
        # splice in the SOURCE body.
        path.write_text(cur_split[0] + src_split[1])
        restored += 1
    return restored, failed


def verify(repo: Path) -> int:
    bad = []
    for path in sorted(repo.rglob("PROMPT.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text()
        n = body_lines(text)
        if n < MIN_BODY_LINES:
            bad.append((str(path.relative_to(repo)), n))
    total = len([p for p in repo.rglob("PROMPT.md") if ".git" not in p.parts])
    print(f"[verify] {total - len(bad)}/{total} prompts have a body >= {MIN_BODY_LINES} lines")
    for f, n in bad:
        print(f"  SHORT {f} ({n})")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".", help="repo root (default: cwd)")
    ap.add_argument("--apply", action="store_true", help="write files")
    ap.add_argument("--force", action="store_true", help="required with --apply")
    ap.add_argument("--json", action="store_true", help="machine-readable plan")
    ap.add_argument("--verify", action="store_true", help="post-restore check only")
    a = ap.parse_args()
    repo = Path(a.repo).resolve()

    if a.verify:
        return verify(repo)

    if a.apply and not a.force:
        print("refusing: --apply requires --force", file=sys.stderr)
        return 2

    items = plan(repo)

    if a.json:
        print(json.dumps(items, indent=2))
        return 0

    recoverable = [i for i in items if i["recoverable"]]
    unrecoverable = [i for i in items if not i["recoverable"]]

    print(f"[plan] {len(items)} truncated prompts; "
          f"{len(recoverable)} recoverable, {len(unrecoverable)} not")
    by_src: dict[str, int] = {}
    for i in recoverable:
        by_src[i["source_commit"]] = by_src.get(i["source_commit"], 0) + 1
    for c, n in sorted(by_src.items(), key=lambda kv: -kv[1]):
        print(f"  source {c}: {n} files")
    for i in unrecoverable:
        print(f"  UNRECOVERABLE {i['file']} (best {i['source_body_lines']} lines)")

    if not a.apply:
        print("\n[dry-run] no files written. re-run with --apply --force")
        return 0

    restored, failed = apply(repo, items)
    print(f"[apply] restored {restored}, failed {failed}")
    return verify(repo)


if __name__ == "__main__":
    sys.exit(main())