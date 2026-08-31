#!/usr/bin/env python3
"""eval-agent-aware.py — Agent-aware brief scorer.

Adapts scoring criteria based on the agent name (detected from path).
"""
import re
import sys
import json
from pathlib import Path


def detect_agent_format(path: str) -> set:
    """Return the keywords that should appear in this brief format."""
    p = Path(path)
    agent = p.parent.parent.name.lower()
    
    format_map = {
        "ai-safety-engineer-30min": {"hard stops", "validation", "trademark"},
        "coaching-quality-reviewer": {"GROW", "Sunstein", "informed consent", "nudge"},
        "devops-monitor-30min": {"system status", "load", "disk", "memory"},
        "kiki-coach": {"concept", "exercise", "stretch", "sources"},
        "business-analyst": {"pipeline", "revenue", "site", "today"},
        "management-coordinator": {"stuck", "stale", "PR", "decision", "ivan"},
        "finance-controller": {"cash", "revenue", "compliance", "contracts"},
        "sales-pipeline": {"lead", "outreach", "stalled", "conversion"},
        "engineering-roster": {"deploy", "PR", "infra", "kiki"},
        "research-tracker": {"thesis", "publications", "course", "blocker"},
    }
    
    for key, keywords in format_map.items():
        if key in agent:
            return keywords
    
    return set()


def score_brief(brief_path: str) -> dict:
    """Generic agent-aware scorer."""
    p = Path(brief_path)
    if not p.exists():
        return {"score": 0, "max_score": 0, "verdict": "FAIL", "reason": "brief not found"}
    
    text = p.read_text()
    keywords = detect_agent_format(brief_path)
    word_count = len(text.split())
    
    checks = []
    score = 0
    max_score = 0
    
    max_score += 1
    if word_count >= 50:
        score += 1
        checks.append({"check": "min_words", "pass": True, "value": word_count})
    else:
        checks.append({"check": "min_words", "pass": False, "value": word_count})
    
    if keywords:
        max_score += 1
        found = [k for k in keywords if k.lower() in text.lower()]
        if found:
            score += 1
            checks.append({"check": "format_keywords", "pass": True, "found": found})
        else:
            checks.append({"check": "format_keywords", "pass": False, "expected": list(keywords)})
    
    max_score += 1
    if re.search(r'^#+\s+.+', text, re.MULTILINE):
        score += 1
        checks.append({"check": "has_sections", "pass": True})
    else:
        checks.append({"check": "has_sections", "pass": False})
    
    max_score += 1
    banned = ["proveedor de IA", "modelo de IA", "proveedor de IA", "asistente de IA generativa", "gpt-4", "texto", "whatsapp", "canal de texto", "pasarela de pagos", "pasarela de pagos secundaria"]
    found = [b for b in banned if b.lower() in text.lower()]
    if not found:
        score += 1
        checks.append({"check": "no_banned_trademarks", "pass": True})
    else:
        checks.append({"check": "no_banned_trademarks", "pass": False, "violations": found})
    
    max_score += 1
    placeholders = ["TODO", "FIXME", "XXX", "TBD", "lorem ipsum"]
    found = [p for p in placeholders if p.lower() in text.lower()]
    if not found:
        score += 1
        checks.append({"check": "no_placeholders", "pass": True})
    else:
        checks.append({"check": "no_placeholders", "pass": False, "found": found})
    
    pct = score / max_score if max_score > 0 else 0
    return {
        "brief_path": brief_path,
        "score": score,
        "max_score": max_score,
        "pass_rate": pct,
        "verdict": "PASS" if pct >= 0.7 else "FAIL",
        "checks": checks,
        "ts": "2026-08-17",
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: eval-agent-aware.py <brief_path>")
        sys.exit(1)
    
    result = score_brief(sys.argv[1])
    print(f"=== Eval-Gate (agent-aware) ===")
    print(f"Brief: {result['brief_path']}")
    print(f"Score: {result['score']}/{result['max_score']} = {result['pass_rate']*100:.0f}%")
    print(f"Verdict: {result['verdict']}")
    print()
    for check in result["checks"]:
        mark = "OK" if check["pass"] else "FAIL"
        print(f"  {mark} {check['check']}")
        for k, v in check.items():
            if k not in ("check", "pass"):
                print(f"      {k}: {v}")
    
    sys.exit(0 if result["verdict"] == "PASS" else 2)
