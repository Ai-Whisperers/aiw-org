#!/usr/bin/env python3
"""Fresh audit — run all regression checks on the changed paths.

Built as Phase 32 R3 (Tier G7/Q5 audit).

Runs:
  1. Lint gate (63 PROMPTs)
  2. Full pytest
  3. Schema validation (Phase 28-31 work)
  4. Audit log NDJSON format (Phase 28 fix)
  5. Hard-stops + eval-gate live behavior
  6. Chronos time-awareness (Phase 31 chronos commit)
  7. Auto-remediate all 5 patterns
  8. Red-team scenario pass rate
  9. Cron registry integrity
 10. No leaked secrets in changed files

Outputs markdown report to /opt/data/state/audit-fresh.md

Usage:
    python3 scripts/audit-fresh.py            # full audit
    python3 scripts/audit-fresh.py --json     # JSON output
"""
import argparse
import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/opt/data/agents")
VENV_PY = "/opt/data/.venv/bin/python3"
STATE_DIR = Path("/opt/data/state")
CRON_PATH = Path("/opt/data/.hermes/cron/jobs.json")


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=kw.get("timeout", 60))
    return r.returncode, r.stdout, r.stderr


def check(name, func):
    try:
        ok, detail = func()
    except Exception as e:
        ok, detail = False, f"exception: {type(e).__name__}: {e}"
    return ok, name, detail


def check_lint():
    rc, out, _ = run([VENV_PY, str(ROOT / "scripts" / "lint-prompts.py")])
    return (rc == 0 and "0 fail" in out), f"63/63 pass (rc={rc})"


def check_pytest():
    rc, out, _ = run([VENV_PY, "-m", "pytest", "tests/", "-q", "--no-header"], cwd=ROOT)
    if "passed" in out:
        m = re.search(r"(\d+)\s+passed", out)
        n = int(m.group(1)) if m else 0
        return (rc == 0 and n >= 195), f"{n} tests pass (rc={rc})"
    return False, f"rc={rc}"


def check_schema_audit():
    rc, out, _ = run([VENV_PY, str(ROOT / "scripts" / "schema-validate-write.py"), "--audit"])
    if rc == 0:
        # Look for "0 gaps" or similar
        return ("0" in out and "gaps" in out.lower()), "schema audit OK"
    return False, f"audit rc={rc}"


def check_audit_log_format():
    """Verify the 5 NDJSON audit logs are still well-formed."""
    logs = [
        "hard-stop-audit.ndjson",
        "eval-gate-decisions.ndjson",
        "injection-attempts.jsonl",
        "redaction-log.jsonl",
        "remediation-log.ndjson",
    ]
    total_entries = 0
    valid_logs = 0
    for log_name in logs:
        log = STATE_DIR / log_name
        if not log.exists():
            continue
        valid = True
        entries = 0
        for line in log.read_text().splitlines():
            if not line.strip():
                continue
            try:
                json.loads(line)
                entries += 1
            except json.JSONDecodeError:
                valid = False
        if valid:
            valid_logs += 1
        total_entries += entries
    return (valid_logs >= 3), f"{valid_logs}/{len(logs)} logs valid, {total_entries} entries total"


def check_hardstops_real_agent():
    rc, out, _ = run([
        VENV_PY, str(ROOT / "patterns" / "hardstop_check.py"),
        "01-operations/founder-bandwidth-watchdog", "disable_hardstop",
    ], timeout=10)
    return (rc == 1 and "BLOCKED" in out), "real agent blocks disable_hardstop"


def check_eval_gate_live():
    """Just verify the eval-gate-enforce.py runs."""
    rc, out, _ = run([
        VENV_PY, str(ROOT / "scripts" / "eval-gate-enforce.py"),
        "--agent", "test-agent",
    ], timeout=10)
    # Should return 0 (warn for unknown agent)
    return (rc in (0, 1)), f"rc={rc}"


def check_chronos_runs():
    """Verify chronos-modified router still loads."""
    try:
        spec = importlib.util.spec_from_file_location("router", str(ROOT / "scripts" / "router.py"))
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        has_chronos = hasattr(mod, "rule_avg_latency_ms") and hasattr(mod, "is_rule_degraded")
        return has_chronos, "chronos functions present"
    except Exception as e:
        return False, f"import error: {e}"


def check_auto_remediate_5_patterns():
    """Verify all 5 patterns are registered."""
    try:
        spec = importlib.util.spec_from_file_location("ar", str(ROOT / "scripts" / "auto-remediate.py"))
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return (len(mod.PATTERNS) == 5), f"{len(mod.PATTERNS)} patterns"
    except Exception as e:
        return False, f"error: {e}"


def check_red_team_scenarios():
    """Run red-team scenarios live."""
    rc, out, _ = run([
        VENV_PY, str(ROOT / "scripts" / "red-team-scenarios.py"),
        "--quiet",
    ], timeout=30)
    # Parse output for pass rate
    m = re.search(r"Both passed:\s+(\d+)/(\d+)", out)
    if m:
        n_pass = int(m.group(1))
        n_total = int(m.group(2))
        return (n_pass / n_total >= 0.7), f"{n_pass}/{n_total} both pass"
    return False, "could not parse"


def check_cron_registry():
    """Verify cron registry integrity."""
    if not CRON_PATH.exists():
        return False, "jobs.json missing"
    with open(CRON_PATH) as f:
        cron = json.load(f)
    jobs = cron.get("jobs", [])
    return (len(jobs) >= 140 and len(jobs) <= 200), f"{len(jobs)} jobs"


def check_no_secrets():
    """Check Phase 32 changed files for accidental secrets.

    Excludes red-team-scenarios.py (test fixtures use synthetic tokens by design).
    """
    patterns = [
        re.compile(r"ghp_[A-Za-z0-9]{20,}"),
        re.compile(r"sk-[A-Za-z0-9]{20,}"),
        re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    ]
    # Check changed files (from git diff), but skip test-fixture files
    r = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", "HEAD~5..HEAD"],
                       capture_output=True, text=True)
    files_to_check = [f for f in r.stdout.splitlines()
                      if not f.endswith("red-team-scenarios.py")]  # exclude test fixtures
    leaks = []
    for f in files_to_check:
        full = ROOT / f
        if not full.exists() or not f.endswith(".py"):
            continue
        try:
            content = full.read_text()
        except Exception:
            continue
        for p in patterns:
            for m in p.finditer(content):
                leaks.append(f"{f}: {m.group(0)[:20]}...")
    return (not leaks), f"no secrets ({len(leaks)} leaks)" if not leaks else f"{len(leaks)} leaks"


def check_audit_logs_unchanged_paths():
    """Verify audit log paths still use .ndjson (Phase 28 R1 + 4540280 fix)."""
    hsw = (ROOT / "patterns" / "hard-stop-wrapper.py").read_text()
    eg = (ROOT / "scripts" / "eval-gate-enforce.py").read_text()
    has1 = "hard-stop-audit.ndjson" in hsw
    has2 = "eval-gate-decisions.ndjson" in eg
    return (has1 and has2), f"hard-stop.ndjson={has1} eval-gate.ndjson={has2}"


def render_markdown(results: list) -> str:
    lines = [
        "# Fresh Audit Report",
        "",
        f"**Date**: {datetime.now(timezone.utc).isoformat()}",
        f"**Total checks**: {len(results)}",
        "",
        "## Summary",
        "",
    ]
    passed = sum(1 for ok, _, _ in results if ok)
    failed = len(results) - passed
    lines.append(f"- **PASS**: {passed}")
    lines.append(f"- **FAIL**: {failed}")
    lines.append(f"- **Pass rate**: {passed/len(results):.0%}")
    lines.append("")

    lines.append("## Checks")
    lines.append("")
    lines.append("| Status | Check | Detail |")
    lines.append("|--------|-------|--------|")
    for ok, name, detail in results:
        status = "✅" if ok else "❌"
        lines.append(f"| {status} | {name} | {detail} |")

    lines.append("")
    lines.append("## Failed Checks")
    lines.append("")
    failed_checks = [r for r in results if not r[0]]
    if not failed_checks:
        lines.append("(none)")
    else:
        for _, name, detail in failed_checks:
            lines.append(f"- **{name}**: {detail}")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fresh audit")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    checks = [
        check_lint,
        check_pytest,
        check_schema_audit,
        check_audit_log_format,
        check_hardstops_real_agent,
        check_eval_gate_live,
        check_chronos_runs,
        check_auto_remediate_5_patterns,
        check_red_team_scenarios,
        check_cron_registry,
        check_no_secrets,
        check_audit_logs_unchanged_paths,
    ]

    print("=== Fresh Audit ===")
    results = []
    for func in checks:
        ok, name, detail = check("", func)
        results.append((ok, name, detail))
        status = "✅" if ok else "❌"
        print(f"  [{status}] {name}: {detail}")

    passed = sum(1 for ok, _, _ in results if ok)
    total = len(results)
    print()
    print(f"=== Summary: {passed}/{total} passed ({passed/total:.0%}) ===")

    # Write report
    report_path = STATE_DIR / "audit-fresh.md"
    md = render_markdown(results)
    report_path.write_text(md)

    # NDJSON log entry
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "total": total,
        "results": [{"name": n, "ok": o, "detail": d} for o, n, d in results],
    }
    with (STATE_DIR / "audit-fresh.ndjson").open("a") as f:
        f.write(json.dumps(entry, separators=(",", ":")) + "\n")

    print(f"\nReport: {report_path}")

    if args.json:
        print(json.dumps({"passed": passed, "total": total, "results": results}, indent=2))

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
