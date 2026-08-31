# State-Write Discipline — Pattern Catalog

> **Phase 8 Area #11** | Engineering dept | Owner: management-coordinator + ai-ops-coordinator
> **Date**: 2026-09-01
> **Status**: First formal catalog (organic patterns become documented)

---

## Why this catalog exists

We discovered state-write patterns organically across 49 agents. Without formalization, future agents will reinvent or violate them. This catalog captures the **canonical patterns** with name, problem, when-to-use, example, anti-pattern.

---

## The 7 canonical patterns

### P1 — additionalProperties: false

| | |
|---|---|
| **Problem** | State files accumulate garbage fields (e.g., "hacker_payload") |
| **Solution** | JSON schema with `additionalProperties: false` |
| **When** | ALWAYS for state files |
| **Example** | `schemas/coord.schema.json` — every field named, no extras allowed |
| **Anti-pattern** | Free-form JSON without schema |

### P2 — Atomic write with .bak

| | |
|---|---|
| **Problem** | Crash during write leaves state half-written |
| **Solution** | Write to .tmp, then rename; keep .bak of previous |
| **When** | For state files updated by multiple agents |
| **Example** | `state/coord.json` writes go: write .tmp → fsync → rename → keep .bak |
| **Anti-pattern** | Direct write to file (no tmp, no backup) |

### P3 — Monitor notes parallel file

| | |
|---|---|
| **Problem** | State file gets noisy with daily/weekly observation logs |
| **Solution** | Separate `monitor-notes/{agent}-{date}.md` files; state file stays signal-only |
| **When** | For monitor agents that produce human-readable notes |
| **Example** | `04-engineering/engineering-roster/monitor-notes/2026-09-01.md` |
| **Anti-pattern** | Embedding free-text in JSON state |

### P4 — additionalProperties: false + rolling archive

| | |
|---|---|
| **Problem** | Long-lived state files bloat over time |
| **Solution** | Combine P1 (strict schema) + P5 (rolling archive) |
| **When** | For state files that accumulate entries over months |
| **Example** | `state/cron-error-watchdog.json` (rolling, schema-strict) |
| **Anti-pattern** | Unbounded arrays without trim policy |

### P5 — Rolling archive (cron-nightly)

| | |
|---|---|
| **Problem** | State files accumulate entries (e.g., audit log) |
| **Solution** | Cron job at 03:00 UTC: trim entries older than 30 days to `state-versioned/` repo |
| **When** | For any state file with growing arrays |
| **Example** | cron `aiw-state-roll` archives `coord.json:decisions[]` over 30d |
| **Anti-pattern** | No trim policy → file bloats to MBs |

### P6 — last_updated_at + version

| | |
|---|---|
| **Problem** | Concurrent writes conflict |
| **Solution** | Every state file has `last_updated_at` + `version` fields; writers increment version |
| **When** | For state files written by >1 agent |
| **Example** | `state/coord.json` has both fields; consumers detect drift |
| **Anti-pattern** | No version tracking → last-write-wins silently |

### P7 — Read-only mirror (git-tracked)

| | |
|---|---|
| **Problem** | Need to version state history but can't commit to live state dir |
| **Solution** | Live state at `/opt/data/state/`; hourly snapshots at `Ai-Whisperers/state-versioned` repo |
| **When** | For all critical state files |
| **Example** | Cron `state-versioned-push` runs hourly |
| **Anti-pattern** | Only live state, no history |

---

## Cross-agent enforcement

| Pattern | Where enforced | Tool |
|---------|----------------|------|
| P1 | Schema validation | `jsonschema` lib in scripts |
| P2 | Wrapper script | `scripts/state-write.sh` (atomic) |
| P3 | Convention | Documented in PROMPT-monitor.md |
| P4 | Cron + schema | Both |
| P5 | Cron | `aiw-state-roll` job |
| P6 | Schema field | Required in schema |
| P7 | Cron | `state-versioned-push` job |

---

## Anti-patterns (do not do these)

- ❌ Writing free-form JSON without schema
- ❌ Direct file writes (always use .tmp + rename)
- ❌ Embedding notes/long-text in JSON state
- ❌ No version field on multi-writer state
- ❌ No rolling archive on growing arrays
- ❌ Skipping the state-versioned push

---

**Cross-references**:
- `~/skills/aiw-state-file-write-discipline/`
- `dept-monitors/INDEX.md` (mentions P3)
- `schemas/` directory (every schema enforces P1+P6)
- `analysis/PHASE-7-dept-research/04-engineering-research-areas.md` Area #7
- `analysis/PHASE-6-REFINEMENT-FEEDBACK.md` (state-path fixes)

