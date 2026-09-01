#!/usr/bin/env python3
"""Citation coverage enforcer — scan research outputs and report coverage.

Built Phase 7 R5 (implementation plan §4 Phase 2.1+2.2).

The Research dept's #1 gap is citation coverage at 15% (per
research/citation-coverage-audit-2026.md). This script:

  - scans markdown files in research/ subdirectories
  - extracts citation patterns (DOI, arXiv, URL, bibliography refs)
  - computes per-file coverage and aggregate coverage
  - writes /opt/data/agents/state/citation-coverage.json (atomic per P2)
  - exits non-zero if --strict mode and coverage below threshold
    (used by git pre-commit hook to block merges with 0 citations)

Usage:
    python3 scripts/citation-coverage-enforcer.py               # scan + write state
    python3 scripts/citation-coverage-enforcer.py --print       # print only
    python3 scripts/citation-coverage-enforcer.py --strict      # exit 1 if below threshold
    python3 scripts/citation-coverage-enforcer.py --threshold 80 # custom threshold
    python3 scripts/citation-coverage-enforcer.py --files research/wizard-academy/foo.md research/wizard-academy/bar.md  # specific files

Citation patterns detected:
  - DOI:        doi:10.xxxx/yyyy or https://doi.org/10.xxxx
  - arXiv:      arXiv:1234.5678 or https://arxiv.org/abs/...
  - URL:        https://... (cited as reference)
  - Markdown:   [text](url) — links as references
  - Footnote:   [^N]: ...  (pandoc-style)
  - Bibtex:     @article{...}
  - Inline:     (Author, Year) / (Author Year) — APA-like
  - Year tag:   [@Author2023]  — pandoc-citeproc
"""

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration ----------------------------------------------------------

AGENTS_REPO = Path("/opt/data/agents")
RESEARCH_DIR = AGENTS_REPO / "research"
STATE_FILE_AGENT = Path("/opt/data/agents/state/citation-coverage.json")
STATE_FILE_LIVE = Path("/opt/data/state/citation-coverage.json")

# Subdirectories/files of research/ to scan (where published research outputs live)
# AIW actual structure: most files are flat under research/
SCAN_PATHS = [
    "wizard-academy",
    "satellite-paraguay",
    "courses",
    "company/Company/marketing",
    "30-research-areas",  # this file references sources
]

# Files at top of research/ to ALSO scan (most research lives here)
TOP_LEVEL_RESEARCH_FILES = [
    "30-research-areas.md",
    "30-coaching-research-areas.md",
    "PROMPT-ANALYSIS.md",
    "STRATEGY.md",
    "coaching-continuation-plan.md",
    "coaching-strategic-implications.md",
    "citation-coverage-audit-2026.md",
    "org-design-literature.md",
    "roles-glossary.md",
    "org-upgrade-coaching-context.md",
    "peer-review-process.md",
    "source-materials-curation-policy.md",
    "aiw-public-resume.md",
    "funding-landscape-2026-Q3.md",
    "dept-research",  # also scan dept-research/ subdirectory
]

# Files to NEVER scan (meta-files, schemas, etc.)
SKIP_PATTERNS = [
    re.compile(r"\.schema\.json$"),
    re.compile(r"node_modules"),
    re.compile(r"__pycache__"),
    re.compile(r"\.git/"),
    re.compile(r"/monitor-notes/"),
]

# Minimum "expected citation density" per N lines (rough heuristic)
# Default: 1 citation per 200 lines is "good"; < 1 per 500 is "low"
LINES_PER_CITATION_HEALTHY = 200
LINES_PER_CITATION_WARNING = 500

DEFAULT_THRESHOLD_PCT = 50.0  # target coverage (per Phase 2 plan: 50% by end Q3 2026)

# --- Citation regex patterns ------------------------------------------------

CITE_PATTERNS = {
    "doi": re.compile(r"(?:doi:|(?:https?://)?(?:dx\.)?doi\.org/)(10\.\d{4,9}/[^\s\)\]\}\,]+)", re.IGNORECASE),
    "arxiv": re.compile(r"(?:arXiv:|(?:https?://)?arxiv\.org/(?:abs|pdf)/)(\d{4}\.\d{4,5}(?:v\d+)?)", re.IGNORECASE),
    "url": re.compile(r"https?://[^\s\)\]\}\,]+", re.IGNORECASE),
    "md_link": re.compile(r"\[[^\]]+\]\((?:https?://|doi:|arxiv\.org/)[^\s\)]+\)"),
    "footnote": re.compile(r"\[\^[^\]]+\]:\s"),
    "bibtex": re.compile(r"@\w+\{[^}]+,"),
    "apa_inline": re.compile(r"\(([A-Z][a-zA-Z\-]+(?:\s+(?:&|and)\s+[A-Z][a-zA-Z\-]+)?,?\s+\d{4}[a-z]?)\)"),
    "pandoc_cite": re.compile(r"\[@[A-Za-z\-]+\d{4}[a-z]?\]"),
}

# URL patterns to EXCLUDE (false positives — not citations):
# - internal anchors (start with #)
# - mailto:
# - relative paths
EXCLUDE_URL_PATTERNS = [
    re.compile(r"^#"),
    re.compile(r"^mailto:"),
    re.compile(r"^\./"),
    re.compile(r"^\.\./"),
    re.compile(r"^/opt/data/agents/"),  # internal repo links
    re.compile(r"\.md(#|$)"),  # markdown internal links
]


# --- Helpers ----------------------------------------------------------------

def atomic_write_json(path: Path, payload: dict) -> None:
    """P2 pattern: atomic write with .tmp + rename + .bak."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            path.replace(path.with_suffix(path.suffix + ".bak"))
        except OSError:
            pass
    fd, tmp = tempfile.mkstemp(prefix=".cite-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def should_skip(path: Path) -> bool:
    s = str(path)
    for pat in SKIP_PATTERNS:
        if pat.search(s):
            return True
    return False


def is_excluded_url(url: str) -> bool:
    for pat in EXCLUDE_URL_PATTERNS:
        if pat.match(url):
            return True
    return False


def extract_citations(text: str) -> set:
    """Return set of unique citation IDs/URLs found in text."""
    cites = set()
    for label, pattern in CITE_PATTERNS.items():
        for match in pattern.finditer(text):
            val = match.group(0)
            # Strip URL of trailing punctuation
            val = val.rstrip(".,;:!?)")
            if label == "url" and is_excluded_url(val):
                continue
            cites.add(f"{label}:{val}")
    return cites


def compute_file_coverage(path: Path) -> dict:
    """Compute citation coverage for one markdown file."""
    # Resolve relative paths against repo root
    if not path.is_absolute():
        path = AGENTS_REPO / path
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.count("\n") + 1
    cites = extract_citations(text)

    # Categorize
    by_type = {}
    for cite in cites:
        label = cite.split(":", 1)[0]
        by_type[label] = by_type.get(label, 0) + 1

    coverage_score = min(1.0, len(cites) / max(1, lines / LINES_PER_CITATION_HEALTHY))
    if len(cites) == 0:
        status = "orphan"
    elif lines / max(1, len(cites)) >= LINES_PER_CITATION_HEALTHY:
        status = "healthy"
    elif lines / max(1, len(cites)) >= LINES_PER_CITATION_WARNING:
        status = "warning"
    else:
        status = "low"

    try:
        rel_path = str(path.relative_to(AGENTS_REPO))
    except ValueError:
        rel_path = str(path)

    return {
        "path": rel_path,
        "lines": lines,
        "citation_count": len(cites),
        "by_type": by_type,
        "coverage_score": round(coverage_score, 3),
        "status": status,
    }


def scan_research(scan_paths=None, top_level=None) -> list:
    """Scan all markdown files in research/ subdirectories + top-level files."""
    scan_paths = scan_paths or SCAN_PATHS
    top_level = top_level or TOP_LEVEL_RESEARCH_FILES
    results = []

    # Scan specified subdirectories
    for sub in scan_paths:
        sub_path = RESEARCH_DIR / sub
        if not sub_path.exists():
            continue
        for f in sub_path.rglob("*.md"):
            if should_skip(f):
                continue
            try:
                results.append(compute_file_coverage(f))
            except (OSError, UnicodeError):
                pass

    # Scan top-level files
    for f_name in top_level:
        f_path = RESEARCH_DIR / f_name
        if f_path.is_dir():
            # Recursively scan if it's a directory
            for nested in f_path.rglob("*.md"):
                if should_skip(nested):
                    continue
                try:
                    results.append(compute_file_coverage(nested))
                except (OSError, UnicodeError):
                    pass
        elif f_path.exists() and f_path.suffix == ".md" and not should_skip(f_path):
            try:
                results.append(compute_file_coverage(f_path))
            except (OSError, UnicodeError):
                pass

    # De-duplicate by path
    seen = set()
    deduped = []
    for r in results:
        if r["path"] not in seen:
            seen.add(r["path"])
            deduped.append(r)
    return deduped


def aggregate(results: list) -> dict:
    """Compute aggregate stats across all files."""
    total_files = len(results)
    total_lines = sum(r["lines"] for r in results)
    total_cites = sum(r["citation_count"] for r in results)
    overall_pct = (total_cites / total_lines * 100.0) if total_lines > 0 else 0.0

    by_status = {"healthy": 0, "warning": 0, "low": 0, "orphan": 0}
    for r in results:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1

    return {
        "files_total": total_files,
        "files_healthy": by_status["healthy"],
        "files_warning": by_status["warning"],
        "files_low": by_status["low"],
        "files_orphan": by_status["orphan"],
        "lines_total": total_lines,
        "citations_total": total_cites,
        "coverage_pct": round(overall_pct, 2),
        "citations_per_100_lines": round(total_cites / total_lines * 100.0, 2) if total_lines > 0 else 0.0,
    }


# --- Main -------------------------------------------------------------------

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "Citation coverage")
    p.add_argument("--print", action="store_true", help="Print JSON, don't write")
    p.add_argument("--strict", action="store_true", help="Exit non-zero if below threshold")
    p.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD_PCT,
                   help=f"Coverage threshold for --strict (default {DEFAULT_THRESHOLD_PCT}%)")
    p.add_argument("--files", nargs="*", help="Specific files to scan (override scan_dirs)")
    p.add_argument("--scan-dir", help="Override scan_dirs (single subdir under research/)")
    args = p.parse_args(argv)

    if args.files:
        results = []
        for f in args.files:
            path = Path(f)
            if not path.exists():
                print(f"WARN: {f} does not exist, skipping", file=sys.stderr)
                continue
            try:
                results.append(compute_file_coverage(path))
            except Exception as e:
                print(f"WARN: {f}: {e}", file=sys.stderr)
    elif args.scan_dir:
        results = scan_research(scan_paths=[args.scan_dir], top_level=[])
    else:
        results = scan_research()

    agg = aggregate(results)
    payload = {
        "version": "1.0.0",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "threshold_pct": args.threshold,
        "aggregate": agg,
        "files": sorted(results, key=lambda r: -r["citation_count"]),
    }

    if args.print:
        print(json.dumps(payload, indent=2, sort_keys=True))
        if args.strict:
            return 1 if agg["coverage_pct"] < args.threshold else 0
        return 0

    # Write to both locations
    atomic_write_json(STATE_FILE_AGENT, payload)
    try:
        atomic_write_json(STATE_FILE_LIVE, payload)
    except OSError as exc:
        print(f"WARN: live mirror write failed: {exc}", file=sys.stderr)

    # Stdout summary
    print(
        f"Citation coverage: {agg['coverage_pct']}% | "
        f"files={agg['files_total']} (healthy={agg['files_healthy']}, "
        f"warning={agg['files_warning']}, low={agg['files_low']}, "
        f"orphan={agg['files_orphan']}) | "
        f"citations={agg['citations_total']}/{agg['lines_total']} lines"
    )
    if agg["files_orphan"] > 0:
        print(f"  WARN: {agg['files_orphan']} files have ZERO citations")

    if args.strict and agg["coverage_pct"] < args.threshold:
        print(f"  STRICT FAIL: {agg['coverage_pct']}% < threshold {args.threshold}%", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())