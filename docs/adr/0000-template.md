# ADR Template — AIW Org

> **Use this template for every architectural decision in AIW org repos.**
> Copy, fill in, save as `ADR-NNNN-<short-slug>.md` in this directory.
> Update `README.md` (the index) when adding new ADRs.

---

# ADR-NNNN: <Decision Title>

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNNN
- **Deciders:** <people / agents involved>
- **Affects:** <list of files / modules / agents / cron jobs>

## Context

What is the issue motivating this decision? What are the constraints and forces at play?

[2-5 sentences describing the situation, what made the current state unsatisfactory, and what we need to optimize for.]

## Decision

What are we doing? State it clearly in 1-3 sentences.

## Alternatives Considered

### Alternative 1: <Name>
- **Pros:**
- **Cons:**
- **Why not:**

### Alternative 2: <Name>
- **Pros:**
- **Cons:**
- **Why not:**

## Consequences

### Positive
- [benefit 1]
- [benefit 2]

### Negative / Costs
- [trade-off 1]
- [trade-off 2]

### Risks + Mitigations
- **Risk:** [what could go wrong]
  **Mitigation:** [how we reduce or detect it]

## Provenance

- Adapted from Michael Nygard's lightweight ADR format
- Refined for AIW org context (adapted from `iPythoning/b2b-sdr-agent-template` + `affaan-m/ECC/skills/architecture-decision-records/`)
- Maintained per `/opt/data/agents/AGENTS.md` (architecture-decisions rule)

## Related

- [ADR-NNNN-other-decision](0001-other-decision.md) — if applicable
- `/opt/data/profiles/ivan/plans/<date>-<topic>.md` — research digest that informed this decision
