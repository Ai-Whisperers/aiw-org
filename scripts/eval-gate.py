#!/usr/bin/env python3
"""Eval-gate POC for business-analyst brief.

Golden trajectory: a high-quality business-analyst daily brief has these properties.
Score the actual brief against the spec, return PASS/FAIL.
"""
import re
import sys
import sqlite3
import os
from datetime import datetime, timezone

REQUIRED_SECTIONS = ["Pipeline", "Revenue direction", "Site & infra health", "Today"]
MIN_WORDS = 50
MAX_WORDS = 300
BANNED = ["proveedor de IA", "modelo de IA", "proveedor de IA", "asistente de IA generativa", "gpt-4", "texto", "whatsapp", "canal de texto", "telegram"]


def score_brief(brief_path: str) -> dict:
    with open(brief_path) as f:
        brief = f.read()

    checks = []
    score = 0
    max_score = 0

    # 1. Required sections (4 pts)
    for section in REQUIRED_SECTIONS:
        max_score += 1
        present = section in brief
        if present:
            score += 1
        checks.append({"check": f"section:{section}", "pass": present})

    # 2. Word count (1 pt)
    max_score += 1
    wc = len(brief.split())
    in_range = MIN_WORDS <= wc <= MAX_WORDS
    if in_range:
        score += 1
    checks.append({"check": "word_count", "pass": in_range, "value": wc, "range": f"{MIN_WORDS}-{MAX_WORDS}"})

    # 3. Has numbers (1 pt)
    max_score += 1
    numbers = re.findall(r"\d+", brief)
    has_numbers = len(numbers) > 0
    if has_numbers:
        score += 1
    checks.append({"check": "has_numbers", "pass": has_numbers, "value": numbers[:5]})

    # 4. Source attribution (1 pt)
    max_score += 1
    has_source = any(s in brief for s in ["Source", "source", "state/", "gh API", "API"])
    if has_source:
        score += 1
    checks.append({"check": "source_attribution", "pass": has_source})

    # 5. No banned trademarks (1 pt)
    max_score += 1
    found_banned = [b for b in BANNED if b.lower() in brief.lower()]
    no_banned = not found_banned
    if no_banned:
        score += 1
    checks.append({"check": "no_banned_trademarks", "pass": no_banned, "violations": found_banned})

    # 6. Action items in "Today" section are concrete (1 pt)
    max_score += 1
    today_section = ""
    in_today = False
    for line in brief.split("\n"):
        if line.strip() == "Today":
            in_today = True
            continue
        if in_today:
            today_section += line + "\n"

    # Vague actions: "improve", "consider", "look into" (without specifics)
    vague_patterns = [r"\bconsider\b", r"\blook into\b", r"\bimprove things\b"]
    is_concrete = not any(re.search(p, today_section, re.IGNORECASE) for p in vague_patterns)
    if is_concrete:
        score += 1
    checks.append({"check": "today_actions_concrete", "pass": is_concrete, "today_section": today_section.strip()[:200]})

    return {
        "brief_path": brief_path,
        "score": score,
        "max_score": max_score,
        "pass_rate": score / max_score,
        "verdict": "PASS" if score / max_score >= 0.7 else "FAIL",
        "checks": checks,
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def log_to_db(result: dict, db_path: str = "/opt/data/db/analyst.db"):
    """Record eval result to eval_log table (creates if missing)."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS eval_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT NOT NULL,
            brief_path TEXT NOT NULL,
            score INTEGER NOT NULL,
            max_score INTEGER NOT NULL,
            pass_rate REAL NOT NULL,
            verdict TEXT NOT NULL,
            ts TEXT NOT NULL,
            details TEXT
        )
    """)
    c.execute(
        "INSERT INTO eval_log (agent, brief_path, score, max_score, pass_rate, verdict, ts, details) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            "business-analyst",
            result["brief_path"],
            result["score"],
            result["max_score"],
            result["pass_rate"],
            result["verdict"],
            result["ts"],
            str(result["checks"]),
        ),
    )
    conn.commit()
    conn.close()


def main():
    brief_path = sys.argv[1] if len(sys.argv) > 1 else "/opt/data/agents/business-analyst/outbox/2026-08-14.md"
    if not os.path.exists(brief_path):
        print(f"ERROR: brief not found at {brief_path}", file=sys.stderr)
        sys.exit(1)

    result = score_brief(brief_path)
    log_to_db(result)

    print(f"\n=== Eval-Gate: business-analyst ===")
    print(f"Brief: {result['brief_path']}")
    print(f"Score: {result['score']}/{result['max_score']} = {result['pass_rate']*100:.0f}%")
    print(f"Verdict: {result['verdict']}\n")

    for check in result["checks"]:
        mark = "✓" if check["pass"] else "✗"
        print(f"  {mark} {check['check']}")
        for k, v in check.items():
            if k not in ("check", "pass"):
                print(f"      {k}: {v}")

    sys.exit(0 if result["verdict"] == "PASS" else 2)


if __name__ == "__main__":
    main()
