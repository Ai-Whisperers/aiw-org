# AI Whisperers — Agent Organization v0.2.0

> The operating constitution. Defines how the company is structured as agents,
> who owns what, who talks to whom, and how decisions escalate.

**Version**: 0.2.0 — bumped 2026-08-14 (after Phase 8 of PLAN-v5)
**Authors**: Erebus (designed per Ivan's directive), ratified by Ivan
**Status**: Active — v0.1.0 archived; v0.2.0 adds storage architecture, AI Ops cross-cutting, and per-dept role catalogs
**Previous**: v0.2.0 (2026-08-14) at `archive/ORG-AGENTS-v0.1.0-2026-08-13.md`

---

## What changed in v0.2.0

| Change | v0.1.0 | v0.2.0 |
|--------|--------|--------|
| Functional areas | 6 depts | 6 depts + 8 Tier 2 cross-cutting + 12 Tier 3 deferred |
| Role catalog | ~30 roles | ~135 roles (`/opt/data/agents-v2/ROLES-INVENTORY.md`) |
| Agent count | 7 lead + ~10 sub | 7 lead + ~14 sub + ~8 cross-cutting (Tier 2) |
| State storage | JSON files | SQLite per agent (`/opt/data/db/`) |
| Memory storage | None | Per-agent git repos (planned in Phase 5.5) |
| Patterns | 16 (described) | 5 mandatory + 4 atomic patterns + verification |
| Sub-roles per dept | 2-3 | 8-24 (full catalog) |
| Storage architecture | (none) | 3-layer model (git + SQLite + Qdrant-Tier2) |
| Compliance Officer | (none) | Named role, Ivan wearing hat, EU client hard-stop |
| Failure modes | (none) | 15 documented + 3 chaos tests |
| Threat model | (none) | 5 actors, 7 threats, defenses |
| Decisions | (scattered) | Consolidated in `DECISIONS-2026-Q3.md` (16 ratified) |
| Backup policy | Manual | 6h snapshot cron + 90-day retention |
| On-call rotation | (none) | Ivan primary, Kiki backup (documented) |
| Cross-references | Minimal | Full to v0.2.0 playbooks, agents, patterns |

---

## TL;DR

The company is **2 founders + ~45 agents across 30 functional areas**. Every meaningful recurring decision is owned by exactly one agent with explicit escalation paths. The founder layer is intentionally thin: Ivan is the CEO/board, Kiki is the CTO/technical director. Everything else runs on cron.


## Department directory

| # | Department | Head (human) | Lead agent | Cadence | File | Sub-agents | Version |
|---|------------|--------------|------------|---------|------|-----------|---------|
| 1 | **Operations** | Ivan | management-coordinator | Mon+Thu 17:00 PYT | `01-operations.md` | business-analyst, kiki-coach, ai-ops-coordinator, bizops-tracker, compliance-monitor, source-curator, founder-bandwidth-watchdog | v0.2.0 |
| 2 | **Finance & Legal** | Ivan | finance-controller | Fri 18:00 PYT | `02-finance-legal.md` | accounting-automation, tax-receipt-tracker, procurement-tracker, compliance-monitor | v0.2.0 |
| 3 | **Sales & Growth** | Ivan | sales-pipeline | Daily 12:00 PYT | `03-sales-growth.md` | proposal-drafter, lead-enrichment, marketing-content-producer, multimedia-producer | v0.2.0 |
| 4 | **Engineering & Delivery** | Kiki | engineering-roster | Tue+Fri 17:00 PYT | `04-engineering-delivery.md` | devops-monitor, qa-automation-runner, security-watchdog, ai-safety-engineer | v0.2.0 |
| 5 | **Research & Education** | Ivan | research-tracker | Sun 18:00 PYT | `05-research-education.md` | citation-checker, thesis-tracker, course-producer, source-curator | v0.2.0 |
| 6 | **People & Culture** | Kiki | kiki-coach | Fri 17:00 PYT | `06-people-culture.md` | founder-bandwidth-watchdog | v0.2.0 |

**Cross-cutting** (touch every department, report to Ivan):
- **business-analyst** — daily 06:30 PYT — pipeline/revenue/sites snapshot
- **morning-brief** — daily 06:00 PYT (existing cron, fixed 2026-08-13)
- **health.sh** — every 15 min — agent liveness watchdog
- **aiw-state-snapshot-6h** — every 6 hours — state snapshots
- **aiw-state-validate-15m** — every 15 min — state schema validation
- **aiw-cron-heartbeat-onhours** — every 30 min (06:00-22:00 PYT) — error detection
- **aiw-cron-heartbeat-offhours** — every 15 min (23:00-05:00 PYT) — error detection
- **aiw-db-snapshot-daily** — daily 02:00 PYT — SQLite backup

**Total cron jobs**: 24 (verified `hermes cron list` count)

## Handoff matrix

When an agent in one department needs action from another:

| From → To | Trigger | How |
|-----------|---------|-----|
| Sales → Engineering | New contract signed | Open issue in client repo, tag engineering-roster |
| Sales → Finance | Proposal accepted | Add deal to `state/finance.json` deals_open list |
| Engineering → Finance | Deploy costs change | Log to `state/finance.json` infra_costs |
| Engineering → People | Kiki commits >5d on a single feature | Surface in next People brief |
| Research → Sales | New IP that could be productized | Add to `state/sales.json` productization_queue |
| Finance → Sales | Contract ready to send | Surface in sales-pipeline next brief |
| People → Engineering | Kiki's curriculum topic needs infra context | Cross-link in lesson file |
| Operations → all | Org-pulse anomaly | Broadcast via health.sh escalation |

Every cross-department handoff MUST:
1. Be **logged to a state file** (not just chat)
2. Have an **owner** (specific human or agent)
3. Have a **deadline** (date or "next brief")

If a handoff has no owner, it's a bug — flag it.

---

## Escalation paths

```
   ┌──────────────────────────────┐
   │  Agent notices something      │
   │  outside its decision rights  │
   └──────────┬───────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │  Log to state file           │
   │  + tag with @ivan or @kiki   │
   └──────────┬───────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │  Surface in next brief       │
   │  (department lead or analyst)│
   └──────────┬───────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │  Ivan/Kiki decides           │
   │  + state.json updated        │
   └──────────────────────────────┘
```

**Hard rule**: An agent never silently makes a decision outside its rights matrix. If unsure → escalate, don't act.

---

## Agent design vocabulary (the patterns)

All agents in this org are built using the patterns documented in **`Ai-Whisperers/agentic-schemas`** (the company's own 20-pattern framework). The vocabulary:

- **Prompt chaining** — every agent prompt follows Concept → Read → Act → Write → State-update
- **Routing** — health.sh + analyst route work to the right department
- **Parallelization** — daily brief pulls from all 6 departments in parallel
- **Reflection** — every agent has a state.json for self-feedback across runs
- **Tool use** — agents use gh, curl, file I/O, cron as tools
- **Planning** — each agent has a fixed output structure (sections) it must follow
- **Multi-agent collaboration** — cross-cutting agents (analyst, coordinator) consume dept agents' outputs
- **Memory management** — state/*.json files roll forward, decisions auto-prune
- **Exception handling** — every script has graceful degradation when a tool (gh, jq) is missing
- **Human-in-the-loop** — Ivan + Kiki are explicit HITL gates for high-stakes decisions
- **RAG** — department agents read canonical docs (MODELO DE IA.md, INDEX.md) before acting
- **Inter-agent communication** — only via state/*.json files + chat; never direct call
- **Resource-aware model routing** — analyst uses minimax-m3 (cheap), engineering uses bigger models for code reasoning
- **Reasoning strategies** — chain-of-thought baked into prompt structure
- **Evaluation** — health.sh + outbox freshness + state.json self-checks
- **Guardrails** — every agent has a "must not" section in its prompt

The full pattern catalog: https://github.com/Ai-Whisperers/agentic-schemas (canonical).

---

## Cadence map (no collisions)

| Time (PYT) | Job | What |
|------------|-----|------|
| 06:00 | morning-brief | Ivan's morning brief |
| 06:30 | business-analyst | Pipeline/revenue/sites snapshot |
| 09:00 | sales-pipeline | Inbound leads triage |
| 12:00 | sales-pipeline | Mid-day outreach queue refresh |
| 17:00 Mon/Thu | management-coordinator | Cross-repo stuck/stale/PR review |
| 17:00 Tue/Fri | engineering-roster | Code velocity, deploy health, errors |
| 17:00 Fri | kiki-coach | Weekly lesson delivery |
| 18:00 Fri | finance-controller | Monthly burn, contracts pending, runway |
| 18:00 Sun | research-tracker | Thesis chapter status, research backlog |

Plus watchdogs (silent unless firing):
- `site-health` — every 15 min
- `thesis-watchdog` — every 15 min
- `evo-poll-watchdog` — every 5 min
- `health.sh` — every 5 min (new)

Visual verification: `/opt/data/agents/scripts/grid.sh` (new) — prints the weekly schedule grid.

---

## State files (the org's memory)

```
/opt/data/agents/state/
├── analyst.json       # business-analyst decisions + open_questions
├── coord.json         # management-coordinator open_stuck + decisions_for_ivan
├── finance.json       # NEW — deals open/closed, burn, runway, contracts pending
├── sales.json         # NEW — leads in flight, proposals out, conversion rate
├── engineering.json   # NEW — deploy health, error budget, Kiki workload
├── research.json      # NEW — thesis chapter status, research backlog, publications queue
├── people.json        # NEW — Kiki lesson streak, contractor list, onboarding
├── kiki.json          # kiki-coach state (existing)
├── kiki-prep.json     # kiki-coach data prep (existing)
└── health.json        # NEW — last health check per agent (auto-rolled)
```

Every department agent reads its own + the cross-cutting analyst/coord. Nobody reads another's state file unless explicitly listed in their "What you read" section.

---

## Update protocol

To change the org structure:
1. Edit this file (the constitution) + the affected department file
2. Bump version + add CHANGELOG entry
3. Update cron schedule if needed (verify with `grid.sh`)
4. Commit to the agents repo (or scratchpad — your call)
5. Run `health.sh` to verify nothing broke

To add a department:
1. Create `0N-<name>.md` in this dir
2. Add row to "Department directory" table above
3. Add lead agent cron job
4. Add state file
5. Update "Cadence map" + "Handoff matrix" + "Decision rights matrix"

To remove a department:
1. Remove cron jobs first (`hermes cron remove <job-id>`)
2. Archive state file to `/opt/data/agents/state/archive/<dept>-YYYYMMDD.json`
3. Update all matrices + cadence map
4. Mark as `cancelled` in directory table (don't delete history)

---

## Ratification

This document is the canonical org structure. Any agent prompt that contradicts it loses. Any agent output that violates the decision rights matrix is a bug — file an issue.

Last updated: 2026-08-13 (initial ratification)
Next review: 2026-09-13 (after 30 days of operation)

---

## Appendix A — Cross-cutting concerns (NEW in v0.2.0)

8 cross-cutting Tier 2 concerns documented in `/opt/data/agents-v2/playbooks/07-cross-cutting-concerns.md`:

1. **AI Ops** — agent layer health (Kiki)
2. **Compliance** — named role, Ivan wearing hat, EU hard-stop
3. **Knowledge Management** — source-materials policy (Research owns)
4. **RevOps** — funnel optimization (Sales sub-function)
5. **BizOps** — OKR tracking (Operations sub-function)
6. **Customer Success** — post-sale (Sales sub-function)
7. **AI Safety** — Kiro-class prevention (Engineering sub-function)
8. **Procurement** — vendor mgmt (Finance sub-function)

Each has documented promotion triggers for becoming standalone depts.

## Appendix B — Deferred Tier-3 departments

12-15 departments documented in `/opt/data/agents-v2/playbooks/08-deferred-tier3.md` with quantitative promotion triggers. Examples:

- Customer Success (5+ clients)
- Marketing independent (>$2K/mo budget)
- Compliance standalone (first EU client)
- Investor Relations (first external investor)
- Chief of Staff (>50 hrs coord/week)

## Appendix C — Storage architecture (NEW in v0.2.0)

Per `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md`:

- **Layer 1**: Per-agent git repos (`/opt/data/git-repos/aiw-agents-*/`)
- **Layer 2**: Per-agent SQLite DBs (`/opt/data/db/*.db`)
- **Layer 3**: Qdrant (deferred to Tier 2)

Backups: daily snapshot cron + 90-day retention + weekly R2 offsite.

## Appendix D — 5 mandatory patterns (NEW in v0.2.0)

Every agent PROMPT.md must conform:

1. **Hard Stops** — action-level approval gates, enforced via `hard-stop-wrapper.py`
2. **Idempotency Contract** — state.last_run + window check
3. **Context-Packaging Escalation** — 6-field JSON payload
4. **Reflection Loop** — content-producing agents only
5. **Fallback Model** — primary + fallback + retry

See `/opt/data/agents-v2/prompts/PROMPT-TEMPLATE.md`.

## Appendix E — Decisions ratified (NEW in v0.2.0)

16 autonomous decisions documented in `/opt/data/agents/DECISIONS-2026-Q3.md`:
- D1-D8: Phase 0 decisions (cost cap, sales priority, compliance, storage path, backup policy, idempotency, hard stops, template order)
- Q1-Q5: earlier decisions
- V5 NEW: storage architecture, 30 functional areas, ~135 roles, ~50 agents, build order
- OP-1 to OP-10: operational decisions

## Appendix F — Cultural artifacts (PRESERVE)

Per `06-people-culture.md` and preserved in v0.2.0:
1. First signed contract in new ICP → LinkedIn post
2. Thesis chapter published → celebration
3. Major deploy win → engineering notes
4. Kiki milestone → kiki-coach notes in next lesson

## Appendix G — On-call rotation

- **Primary**: Ivan
- **Backup**: Kiki
- **Cycle**: monthly
- **Documented in**: `/opt/data/agents/ON-CALL.md` (TODO)

---

## CHANGELOG

- v0.2.0 (2026-08-14): bumped per Phase 8 of PLAN-v5. Added Appendices A-G (cross-cutting, deferred depts, storage, patterns, decisions, rituals, on-call). Each dept spec also bumped to v0.2.0 with full role catalogs.
- v0.1.0 (2026-08-13): initial ratification. 6 depts, 12 ratified cron jobs.
