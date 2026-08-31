# Org Buildout — Master Index

> All artifacts produced in this session. Master navigation.
> **Last updated**: 2026-08-14

---

## Research artifacts (Session 1 — foundational)

| # | File | Purpose |
|---|------|---------|
| 1 | `/opt/data/source-materials/topics/org-design/INDEX.md` | Source provenance catalog (27 sources) |
| 2 | `/opt/data/source-materials/topics/org-design/literature.md` | Strategic synthesis (7 sections) |
| 3 | `/opt/data/source-materials/topics/org-design/cheatsheet.md` | Org-size decision table |
| 4 | `/opt/data/agents/research/roles-glossary.md` | 98 roles (now superseded by ROLES-INVENTORY.md) |

## Research artifacts (deep research — 105 queries)

| # | File | Purpose |
|---|------|---------|
| 5 | `/opt/data/agents-v2/RESEARCH-COMPLETE-ORG.md` | 30 functional areas, ~135 roles, storage arch |

## Decisions + audit

| # | File | Purpose |
|---|------|---------|
| 6 | `/opt/data/agents/DECISIONS-2026-Q3.md` | 16 ratified decisions (D1-D8, Q1-Q5, v5 NEW, operational) |
| 7 | `/opt/data/agents-v2/STATE-AUDIT-2026-08-14.md` | Existing state inventory (3 lead agents, 19 cron jobs, 8 state files, 6 dept specs) |

## Plans (versions)

| # | File | Purpose | Status |
|---|------|---------|--------|
| 8 | `/opt/data/agents-v2/PLAN-v4.md` | v4 plan with 9 phases | Superseded by v5 |
| 9 | `/opt/data/agents-v2/PLAN-v5.md` | v5 plan with 11 phases + storage | **CURRENT** |

## Patterns (Phase 3 input)

| # | File | Purpose |
|---|------|---------|
| 10 | `/opt/data/agents-v2/prompts/PROMPT-TEMPLATE.md` | Master 12-section template |
| 11 | `/opt/data/agents-v2/patterns/hard-stops-schema.md` | YAML schema spec |
| 12 | `/opt/data/agents-v2/patterns/idempotency.md` | Idempotency contract pattern |
| 13 | `/opt/data/agents-v2/patterns/sqlite-schema.md` | SQLite schemas for all 11 DBs |
| 14 | `/opt/data/agents-v2/patterns/trademark-scrub.sh` | Mechanical banlist enforcement |

## Reference docs (Phase 6+ input)

| # | File | Purpose |
|---|------|---------|
| 15 | `/opt/data/agents-v2/ROLES-INVENTORY.md` | ~135 roles across 30 functional areas |
| 16 | `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md` | 3-layer model spec |
| 17 | `/opt/data/agents-v2/FAILURE-MODES.md` | 15 failure modes + 3 chaos test scenarios |
| 18 | `/opt/data/agents-v2/THREAT-MODEL.md` | 7 threats + defenses + action items |
| 19 | `/opt/data/agents-v2/ROLLBACK-PLAYBOOK.md` | Per-phase rollback procedure |

---

## Reading order for a new session

If a future session needs to resume work, read in this order:

1. **STATE-AUDIT-2026-08-14.md** — what's already built
2. **DECISIONS-2026-Q3.md** — what's ratified
3. **PLAN-v5.md** — what to do next
4. **PROMPT-TEMPLATE.md** — when upgrading agents
5. **STORAGE-ARCHITECTURE.md** — when migrating to SQLite
6. **THREAT-MODEL.md + FAILURE-MODES.md + ROLLBACK-PLAYBOOK.md** — when in doubt

---

## Total file count and size

| Category | Count | Total Size |
|----------|-------|------------|
| Research artifacts | 5 | ~85 KB |
| Decisions + audit | 2 | ~17 KB |
| Plans | 2 | ~82 KB |
| Patterns | 5 | ~32 KB |
| Reference docs | 5 | ~50 KB |
| **TOTAL** | **19 files** | **~266 KB** |

---

## What's NOT yet written

These are placeholders / planned for future phases:

| Artifact | When | Phase |
|----------|------|-------|
| `PHASE-0-COMPLETE.md` | After Phase 0 runs | Phase 0 |
| `PHASE-1-COMPLETE.md` | After Phase 1 runs | Phase 1 |
| ... (PHASE-N-COMPLETE.md for each phase) | ... | ... |
| `playbooks/00-INDEX.md` | After Operations playbook | Phase 6A |
| `playbooks/01-operations.md` ... `08-deferred-tier3.md` | After each playbook | Phase 6 |
| `playbooks/role-tool-sop-matrix.md` | After all playbooks | Phase 6B |
| `git-repos/aiw-agents-*/` (per-agent repos) | After Phase 5.5A | Phase 5.5 |
| `db/*.db` (per-agent SQLite) | After Phase 5.5B | Phase 5.5 |
| `state/SCHEMAS.md` | After Phase 2B | Phase 2 |
| `scripts/state-snapshot.sh`, `validate-state.py`, `cron-heartbeat.sh` | After Phase 2 | Phase 2 |
| `cost-cap.sh`, `tool-stack-decisions.md` | After Phase 7 | Phase 7 |
| `DEFERRED-ROLES.md`, `DEFERRED-AGENTS.md`, `REVIEW-2026-Q4.md` | After Phase 8 | Phase 8 |

---

## File locations summary

```
/opt/data/agents/
├── DECISIONS-2026-Q3.md                # NEW: decisions
├── departments/
│   ├── ORG-AGENTS.md (v0.1.0)
│   ├── 01-operations.md ... 06-people-culture.md
│   └── archive/
│       └── ORG-AGENTS-v0.1.0-2026-08-13.md
└── (existing agents: business-analyst, management-coordinator, kiki-coach, ...)

/opt/data/agents-v2/
├── PLAN-v4.md                          # superseded
├── PLAN-v5.md                          # CURRENT
├── RESEARCH-COMPLETE-ORG.md
├── STATE-AUDIT-2026-08-14.md
├── ROLES-INVENTORY.md
├── STORAGE-ARCHITECTURE.md
├── FAILURE-MODES.md
├── THREAT-MODEL.md
├── ROLLBACK-PLAYBOOK.md
├── INDEX.md                            # this file
├── patterns/
│   ├── hard-stops-schema.md
│   ├── idempotency.md
│   ├── sqlite-schema.md
│   └── trademark-scrub.sh
└── prompts/
    └── PROMPT-TEMPLATE.md

/opt/data/source-materials/topics/org-design/
├── INDEX.md                            # source provenance
├── literature.md
└── cheatsheet.md
```

---

## Per-department packages

The mono-repo has been split into 6 per-department packages under
`/opt/data/agents-v2/packages/`. Each package is independently
deployable so customers can pick "just the sales agents" or "just
the coaching product" without copying the whole repo.

| # | Package | Lead agent | Use case |
|---|---------|------------|----------|
| 1 | `packages/finance/` | `finance-controller` | Cash flow, contracts, compliance, procurement |
| 2 | `packages/sales/` | `sales-pipeline` | Lead capture, ICP scoring, outreach, proposals |
| 3 | `packages/operations/` | `management-coordinator` | Cross-repo review, daily brief, AI-ops, OKRs, burnout watch |
| 4 | `packages/coaching/` | `kiki-coach` | Coaching product: lessons, thesis, courses, conversion funnel |
| 5 | `packages/engineering/` | `engineering-roster` | Deploys, infra monitoring, QA, security, AI safety, chaos tests |
| 6 | `packages/research/` | `research-tracker` | Thesis, citations, course modules, OKRs, funding programs |

**Master package index**: [`/opt/data/agents-v2/PACKAGE-INDEX.md`](./PACKAGE-INDEX.md)
(34 agents, ~616 KB total, all packages MIT-licensed, all trademark-clean).

---

**Document path**: `/opt/data/agents-v2/INDEX.md`
**Last updated**: 2026-08-26 (package split)


## Agent Naming (portmanteau framework)

The org uses a portmanteau naming framework for all agents: [Domain Root] + [Personal Suffix]. Examples:
- `sales-pipeline` → **Saleina**
- `engineering-roster` → **Devin**
- `finance-controller` → **Finus**
- `ai-safety-engineer` → **Safina**
- `kiki-coach` → **Magistra**

Full reference (54 agents): `/opt/data/scratchpad/analysis/AGENT-NAMES-V2.md`
