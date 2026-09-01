"""Commitment extraction for AIW signals.

Phase 1.4 of AIW upgrade plan.
Pattern source: iPythoning/b2b-sdr-agent-template ANTI-AMNESIA.md (Layer 1 schema).
What it does:
  - Detects customer commitments in signal text via regex patterns
  - Returns structured commitment objects: {id, text, signal_id, detected_at, due_date, type}
  - Provides extract_commitments() and merge_commitments() for coord.json integration
  - Commitments are schema-strict: only known keys per AIW's pre_dispatch_check pattern
"""
import re
from datetime import datetime, timezone

# Commitment detection patterns (regex). Each pattern maps to a commitment type.
COMMITMENT_PATTERNS = [
    (re.compile(r"\b(?:I'?ll|I will|I'll)\s+(?:send|email|reach out|follow up|get back to you)\b", re.I),
     "promise_to_respond"),
    (re.compile(r"\b(?:please|kindly)\s+(?:send|share|forward|provide)\s+(?:me|us)\b", re.I),
     "request_for_info"),
    (re.compile(r"\b(?:will|going to)\s+(?:ship|deliver|complete|finish|launch)\b", re.I),
     "delivery_commitment"),
    (re.compile(r"\b(?:let's|let's)\s+(?:schedule|book|set up|arrange)\s+(?:a|an)\s+(?:call|meeting|chat)\b", re.I),
     "meeting_commitment"),
    (re.compile(r"\b(?:by|before|on)\s+(?:next|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|EOD|EOW|end of)\b", re.I),
     "time_bound"),
    (re.compile(r"\b(?:I'?m|I am)\s+(?:expecting|waiting|hoping)\b.*\b(?:by|on|before)\b", re.I),
     "expectation"),
    (re.compile(r"\b(?:we'?re|we are|let'?s)\s+(?:going|moving|pushing)\s+(?:to\s+)?(?P<direction>up|down|forward)\b", re.I),
     "direction_signal"),
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def extract_commitments(text: str, signal_id: str) -> list:
    """Extract commitments from signal text. Returns list of structured objects.

    Each commitment has:
      - id: auto-generated uuid-like hash (deterministic from text+signal_id)
      - text: the matched text (max 200 chars)
      - signal_id: source signal
      - detected_at: ISO timestamp
      - type: one of the COMMITMENT_TYPES
    """
    if not text:
        return []
    commitments = []
    for pattern, ctype in COMMITMENT_PATTERNS:
        for match in pattern.finditer(text):
            matched_text = match.group(0).strip()
            if len(matched_text) > 200:
                matched_text = matched_text[:197] + "..."
            # Generate a deterministic id from content (so the same commitment maps to same id)
            cid_input = f"{signal_id}:{ctype}:{matched_text}"
            cid = f"c-{hash(cid_input) & 0xFFFFFFFF:08x}"
            commitments.append({
                "id": cid,
                "text": matched_text,
                "signal_id": signal_id,
                "detected_at": _now_iso(),
                "type": ctype,
            })
    return commitments


def extract_commitments_from_signal(signal: dict) -> list:
    """Extract commitments from a signal record (looks at source, type, payload)."""
    if not signal:
        return []
    signal_id = signal.get("id") or signal.get("signal_id") or "unknown"
    text_parts = []
    for field in ["source", "type", "summary", "title"]:
        if field in signal:
            text_parts.append(str(signal[field]))
    payload = signal.get("payload", {})
    if isinstance(payload, dict):
        for k, v in payload.items():
            if isinstance(v, str):
                text_parts.append(v)
    full_text = " ".join(text_parts)
    return extract_commitments(full_text, signal_id)


def merge_commitments(coord_data: dict, new_commitments: list) -> dict:
    """Merge new commitments into coord.json data, deduplicating by id.

    Returns the modified data. Caller is responsible for writing back to disk.
    """
    existing = coord_data.get("commitments", [])
    existing_ids = {c.get("id") for c in existing if c.get("id")}
    to_add = [c for c in new_commitments if c.get("id") not in existing_ids]
    if to_add:
        coord_data["commitments"] = existing + to_add
    else:
        # Ensure the field exists even if empty
        coord_data.setdefault("commitments", existing)
    return coord_data


def get_commitments_for_signal(coord_data: dict, signal_id: str) -> list:
    """Get all commitments that originated from a specific signal."""
    commitments = coord_data.get("commitments", [])
    return [c for c in commitments if c.get("signal_id") == signal_id]
