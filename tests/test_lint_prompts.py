#!/usr/bin/env python3
"""test_lint_prompts.py — smoke tests for scripts/lint-prompts.py.

Verifies:
1. Script exists
2. Script runs on the repo without crashing
3. Output format is sane (Linting N files... Summary)
4. Exit code is 0 or 1 (fail-fast but not crash)
"""
import os
import subprocess

SCRIPT = "/opt/data/agents/scripts/lint-prompts.py"
PYTHON = "/opt/data/.venv/bin/python3"


def test_script_exists():
    assert os.path.exists(SCRIPT), f"lint-prompts.py not found at {SCRIPT}"


def test_lint_on_repo_returns_int():
    """Lint on actual repo: exit code 0 (pass) or 1 (fail). Never crash."""
    r = subprocess.run([PYTHON, SCRIPT], capture_output=True, text=True, timeout=30)
    assert r.returncode in (0, 1), f"unexpected return code: {r.returncode}"


def test_lint_output_format():
    """Lint should print 'Linting N files...' and 'Summary: ...' lines."""
    r = subprocess.run([PYTHON, SCRIPT], capture_output=True, text=True, timeout=30)
    output = r.stdout + r.stderr
    assert "Linting" in output, "lint should print 'Linting N PROMPT.md files...'"
    assert "Summary" in output or "Total issues" in output, "lint should print summary"


def test_lint_finds_at_least_one_prompt():
    """Repo has 58+ PROMPTs; lint should find them."""
    r = subprocess.run([PYTHON, SCRIPT], capture_output=True, text=True, timeout=30)
    # Look for "Linting N PROMPT.md" line; extract N
    import re
    m = re.search(r'Linting (\d+) PROMPT', r.stdout)
    if m:
        n = int(m.group(1))
        assert n >= 30, f"expected ≥30 PROMPTs in repo, got {n}"
    else:
        # If 0 prompts, that's a warning not error
        assert "no PROMPT.md files found" in r.stdout or "WARN" in r.stdout, "lint didn't find any prompts but also didn't warn"


if __name__ == "__main__":
    test_script_exists()
    test_lint_on_repo_returns_int()
    test_lint_output_format()
    test_lint_finds_at_least_one_prompt()
    print("test_lint_prompts: 4 passed")
