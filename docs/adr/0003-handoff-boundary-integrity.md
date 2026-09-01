# ADR-0003: Adopt "Handoff Boundary Integrity" Rule from Boundary Metadata Collapse Research

- **Date:** 2026-09-01
- **Status:** Accepted
- **Deciders:** Ivan + Hermes session `20260901_134405_00cab4`
- **Affects:** `/opt/data/agents/scripts/router.py`, `/opt/data/agents/scripts/intake.py`, `/opt/data/agents/AGENTS.md`

## Context

Academic paper found this session — **"Facts Without Rules: Boundary Metadata Collapse in Multi-Agent LLM Handoffs"** (arXiv 2026) — measures that when handoff artifacts are compressed to ≤25 words:
- Operational facts (the work that was done) survive ~100%
- Boundary metadata (who can see this, what permissions apply) collapses to 57%
- Privacy leakage rate: 73% on GPT-5-mini, 50% on DeepSeek-R1-32B

The cause is structural: handoff compression heuristics preserve "what happened" but strip "who's allowed to know."

AIW currently does handoff via `scripts/router.py:deliver_to_outbox()` which writes a full markdown envelope (the `outbox/signals/<signal-id>.md` file). This preserves boundaries. **The risk is future**: if someone adds auto-summarization to the pipeline (e.g., to fit signals into smaller outboxes, or to compress for review), boundary metadata will collapse silently.

The paper recommends: **explicit audience allowlists** at the handoff layer, not implicit compression heuristics.

## Decision

Adopt the **Handoff Boundary Integrity Rule** as a permanent org-wide rule:

1. **NEVER auto-summarize handoff artifacts** (`outbox/signals/*.md`, signal-queue.ndjson, intake.py output). Full text only.
2. **Every handoff MUST include an explicit `Audience:` header** listing who can read it.
3. **Every handoff MUST include an explicit `Visibility:` scope** (`internal` | `dept-scoped:<id>` | `agent-scoped:<id>` | `public`)
4. **A `BWS`-protected secret MUST NEVER appear** in any handoff artifact (already covered by AGENTS.md "NEVER commit secrets" rule; this ADR makes it explicit for handoff context).
5. **The `pre_dispatch_check` function (already in `router.py`) is the canonical enforcement point** — extend it to validate the handoff artifact schema before writing.

## Alternatives Considered

### Alternative 1: Wait for a tool to handle this automatically
- **Pros:** No new code to maintain.
- **Cons:** Per the paper, the failure is **structural** in compression heuristics. Tools built on those heuristics will inherit the bug.
- **Why not:** Defensive org rule > waiting for tooling.

### Alternative 2: Use encrypted channels for everything
- **Pros:** Privacy by default.
- **Cons:** AIW runs locally; encryption adds ops burden without solving the actual problem (boundary metadata collapse is about *which* fields are present, not channel encryption).
- **Why not:** Solves a different problem.

### Alternative 3: Do nothing — AIW is local-first and has no untrusted callers
- **Pros:** Minimal change.
- **Cons:** AIW has 63 agents that pass data between them. Each handoff is a potential leak point. And future contributors (including forks) may add summarization without knowing the risk.
- **Why not:** The cost of the rule (1 line in AGENTS.md, 1 function call in router.py) is trivial vs the asymmetric downside.

## Consequences

### Positive
- Defense against the failure mode empirically measured in the literature
- Explicit boundary metadata in every handoff makes auditing trivial
- Composable with existing `pre_dispatch_check` (which already validates signal structure)
- Documentation of WHY (the paper) means future contributors don't accidentally remove the rule

### Negative / Costs
- ~30 lines of code added to `router.py` (extension of `pre_dispatch_check`)
- Schema change: every handoff artifact needs `Audience:` + `Visibility:` headers — minor breaking change for any consumer that parses handoffs today
- One-time audit of existing 181 traces in `state/agent-traces.jsonl` to confirm they're compliant

### Risks + Mitigations
- **Risk:** Existing outbox files lack the headers → audit + retroactive schema migration
  **Mitigation:** Add migration script in Phase 1; mark non-compliant artifacts as `Visibility: legacy` so they're still readable
- **Risk:** Performance impact of validating every handoff
  **Mitigation:** Validation is string-matching against regex, <1ms per handoff. No measurable cost.

## Implementation plan (next session)

1. Extend `pre_dispatch_check` in `/opt/data/agents/scripts/router.py` to validate handoff schema
2. Update `deliver_to_outbox` to write the new headers
3. Add a CLI command `/opt/data/agents/scripts/handoff_audit.py` that scans existing outbox files for compliance
4. Update `/opt/data/agents/AGENTS.md` "Engineering principles" section with this rule
5. Add to `/opt/data/agents/docs/HANDOFF.md` "Known pitfalls" section

## Provenance

- Paper: "Facts Without Rules: Boundary Metadata Collapse in Multi-Agent LLM Handoffs" (arXiv 2026)
- Found in: `/opt/data/profiles/ivan/plans/2026-09-01-aiw-research-round-5-people-papers.md` §3.1
- Related: ADR-0001 (AGENTS.md methodology), ADR-0002 (instinct integration plan)

## Related

- `/opt/data/profiles/ivan/plans/2026-09-01-aiw-research-round-5-people-papers.md` (research digest)
- `/opt/data/agents/scripts/router.py` (pre_dispatch_check function)
- `/opt/data/agents/AGENTS.md` (org-wide rulebook — to be updated)
