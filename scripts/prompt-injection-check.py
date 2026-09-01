#!/usr/bin/env python3
"""Prompt injection detection on inbound content.

Built as Phase 30 R2 (Tier H1).

Inspects text content (emails, webhooks, agent outputs) for known
prompt injection patterns. Returns a verdict:
  - safe: no patterns detected
  - suspicious: some patterns detected (low confidence)
  - blocked: high-confidence patterns detected (recommended reject)

Detects:
  - "ignore previous instructions" / "disregard prior"
  - "you are now X" / role override attempts
  - system prompt extraction attempts
  - jailbreak keywords ("DAN", "developer mode", etc.)
  - hidden instruction markers (zero-width unicode, base64 in prompts)

Usage:
    python3 scripts/prompt-injection-check.py --file /path/to/inbound.txt
    echo "$text" | python3 scripts/prompt-injection-check.py --stdin
    python3 scripts/prompt-injection-check.py --text "ignore all previous"
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

LOG_PATH = Path("/opt/data/state/injection-attempts.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class InjectionVerdict:
    verdict: str  # safe | suspicious | blocked
    score: float  # 0.0-1.0
    patterns_matched: list  # list of matched pattern names
    sample: str  # first 200 chars of suspicious content


# Pattern catalog: each (name, regex, weight)
# Higher weight = stronger signal of injection
PATTERNS = [
    # === English ===
    # Direct instruction override
    ("ignore-previous", re.compile(r"\b(ignore|disregard|forget)\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|rules?|prompts?)\b", re.I), 0.9),
    ("you-are-now", re.compile(r"\byou\s+are\s+now\s+(a|an|the)\s+", re.I), 0.7),
    ("system-prompt-extract", re.compile(r"\b(show|reveal|print|output)\s+(your|the)\s+(system|initial|original)\s+(prompt|instructions?)\b", re.I), 0.8),
    ("jailbreak-dan", re.compile(r"\bDAN\b|\bdo\s+anything\s+now\b", re.I), 0.9),
    ("jailbreak-developer-mode", re.compile(r"\bdeveloper\s+mode\s+enabled?\b|\bjailbreak\b", re.I), 0.8),
    ("role-override", re.compile(r"\boverride\s+(your|the)\s+(rules?|instructions?)\b", re.I), 0.7),
    ("hidden-instruction", re.compile(r"\[INST\]|<<SYS>>|<\|im_start\|>", re.I), 0.6),
    # Data exfiltration
    ("exfiltrate", re.compile(r"\b(exfiltrate|extract|reveal)\b[^.]{0,30}?\b(user|customer|private|secret)\s+data\b", re.I | re.S), 0.8),
    # Instruction injection in data fields
    ("execute-this", re.compile(r"\b(execute|run|eval)\s+(this|the\s+following)\s+(code|command|sql)\b", re.I), 0.7),
    # Bypass safety phrases
    ("pretend-no-rules", re.compile(r"\bpretend\s+(you|there\s+are)\s+(?:don'?t\s+have\s+|haven'?t\s+|have\s+no\s+|no\s+)?rules?\b", re.I), 0.9),
    # === Phase 33 R3: Multilingual patterns ===
    # Spanish
    ("es-ignora-instrucciones", re.compile(r"\bignora\s+(todas?\s+)?(las?\s+)?instrucciones?\s+(anteriores?|previas?)\b", re.I), 0.9),
    ("es-revela-prompt", re.compile(r"\b(revela|muestra|ens[eé]ame)\s+(tu|el)\s+(prompt|instrucciones?)\s+(del?\s+sistema)\b", re.I), 0.8),
    ("es-ahora-er", re.compile(r"\b(ahora\s+eres|ahora\s+act[uú]a\s+como)\s+", re.I), 0.7),
    # French
    ("fr-ignore-instructions", re.compile(r"\bignore[zr]?\s+(toutes?\s+)?(les?\s+)?instructions?\s+(pr[eé]c[eé]dentes?|ant[eé]rieures?)\b", re.I), 0.9),
    ("fr-revele-prompt", re.compile(r"\b(r[eé]v[eè]le|affiche|montre)\s+(ton|votre|le)\s+(prompt|instructions?)\s+(syst[eè]me)\b", re.I), 0.8),
    # German
    ("de-ignoriere-anweisungen", re.compile(r"\bignoriere?\s+(alle\s+)?(die\s+)?(vorherigen?|bisherigen?)\s+(anweisungen?|instruktionen?)\b", re.I), 0.9),
    ("de-zeige-prompt", re.compile(r"\b(zeige|offenbare)\s+(deinen?|den)\s+(system-?prompt|system-?anweisungen?)\b", re.I), 0.8),
    # Portuguese
    ("pt-ignore-instrucoes", re.compile(r"\bignore\s+(todas?\s+)?(as\s+)?instru[cç][oõ]es\s+(anteriores|pr[eé]vias)\b", re.I), 0.9),
    # === Phase 33 R3: Encoded content detection ===
    # Base64-encoded "ignore previous" instructions (common attack vector)
    ("base64-injection", re.compile(r"(?:[A-Za-z0-9+/]{40,}={0,2})"), 0.4),  # base64 heuristic
    # Hex-encoded instruction markers
    ("hex-injection", re.compile(r"\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}"), 0.6),
    # Zero-width unicode characters (used to hide instructions)
    ("zero-width-unicode", re.compile(r"[\u200b\u200c\u200d\u200e\u200f\ufeff]"), 0.7),
]


def analyze_text(text: str) -> InjectionVerdict:
    """Analyze text for prompt injection patterns.

    Returns InjectionVerdict with verdict (safe/suspicious/blocked), score, and details.
    """
    patterns_matched = []
    total_score = 0.0
    for name, regex, weight in PATTERNS:
        if regex.search(text):
            patterns_matched.append({"name": name, "weight": weight})
            total_score += weight

    # Cap score at 1.0
    score = min(total_score, 1.0)

    # Verdict thresholds
    if score >= 1.5 or any(p["weight"] >= 0.9 for p in patterns_matched):
        verdict = "blocked"
    elif score >= 0.7 or patterns_matched:
        verdict = "suspicious"
    else:
        verdict = "safe"

    sample = text[:200].replace("\n", " ").strip()

    return InjectionVerdict(
        verdict=verdict,
        score=score,
        patterns_matched=patterns_matched,
        sample=sample,
    )


def log_verdict(text: str, verdict: InjectionVerdict) -> None:
    """Log injection attempt to NDJSON audit log."""
    from datetime import datetime, timezone
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict.verdict,
        "score": verdict.score,
        "patterns": verdict.patterns_matched,
        "sample": verdict.sample,
        "input_len": len(text),
    }
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(entry, separators=(",", ":")) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Prompt injection detection")
    parser.add_argument("--text", help="Text to analyze")
    parser.add_argument("--file", type=Path, help="File to analyze")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--quiet", action="store_true",
                        help="Exit silently with code only (for cron use)")
    args = parser.parse_args()

    # Get text
    if args.text:
        text = args.text
    elif args.file:
        if not args.file.exists():
            print(f"ERROR: file not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        text = args.file.read_text()
    elif args.stdin or not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    verdict = analyze_text(text)
    log_verdict(text, verdict)

    if args.quiet:
        sys.exit(0 if verdict.verdict == "safe" else 1)

    print(json.dumps(asdict(verdict), indent=2))
    sys.exit(0 if verdict.verdict == "safe" else 1)


if __name__ == "__main__":
    main()
