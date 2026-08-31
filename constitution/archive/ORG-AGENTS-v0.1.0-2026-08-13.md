# AI Whisperers — Agent Organization

> The operating constitution. Defines how the company is structured as agents,
> who owns what, who talks to whom, and how decisions escalate.

**Version**: 0.1.0 — initial rollout 2026-08-13
**Authors**: Erebus (designed per Ivan's directive), ratified by Ivan
**Status**: Active — replaces ad-hoc decision-making with explicit roles

---

## TL;DR

The company is **2 founders + 17 agents across 6 departments + 3 cross-cutting roles**. Every meaningful recurring decision is owned by exactly one agent with explicit escalation paths. The founder layer is intentionally thin: Ivan is the CEO/board, Kiki is the CTO/technical director. Everything else runs on cron.

```
┌─────────────────────────────────────────────────────────────────┐
│  Board (Ivan)                                                  │
│  - Sets direction, approves >USD 500 spend, signs contracts    │
│  - Receives morning brief, business analyst, weekly review     │
└─────────────────┬───────────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────────┐
│  Cross-cutting (always-on intelligence)                        │
│  - business-analyst (daily)                                    │
│  - management-coordinator (Mon+Thu)                            │
│  - health.sh watchdog (every 5m)                               │
└─────────┬─────────┬─────────┬─────────┬─────────┬─────────────┘
          │         │         │         │         │
   ┌──────▼──┐ ┌────▼───┐ ┌───▼────┐ ┌──▼─────┐ ┌─▼──────┐
   │ Ops     │ │Finance │ │Sales & │ │Engr &  │ │People  │
   │         │ │ & Legal│ │ Growth │ │Delivery│ │& Culture│
   └─────────┘ └────────┘ └────────┘ └────────┘ └────────┘
```

**Why 6, not 12**: A 2-person org needs fewer departments, but each one needs clear ownership. The six chosen match where decisions actually live in this org today (verified against the 17 active repos + 47 installed skills + 13 cron jobs). Research & Education is its own department because the thesis is a flagship asset, not a side project.

---

## Department directory

| # | Department | Head (human) | Lead agent | Cadence | File |
|---|------------|--------------|------------|---------|------|
| 1 | **Operations** | Ivan | management-coordinator | Mon+Thu 17:00 | `01-operations.md` |
| 2 | **Finance & Legal** | Ivan | finance-controller | Fri 18:00 | `02-finance-legal.md` |
| 3 | **Sales & Growth** | Ivan | sales-pipeline | Daily 12:00 | `03-sales-growth.md` |
| 4 | **Engineering & Delivery** | Kiki | engineering-roster | Tue+Fri 17:00 | `04-engineering-delivery.md` |
| 5 | **Research & Education** | Ivan | research-tracker | Sun 18:00 | `05-research-education.md` |
| 6 | **People & Culture** | Kiki | kiki-coach | Fri 17:00 | `06-people-culture.md` |

**Cross-cutting** (touch every department, report to Ivan):
- **business-analyst** — daily 06:30 PYT — revenue/pipeline/sites snapshot
- **morning-brief** — daily 06:00 PYT (existing cron, fixed 2026-08-13)
- **health.sh** — every 5 min — agent liveness watchdog

---

## Decision rights matrix

| Decision type | Authority | Escalation |
|---------------|-----------|------------|
| Spend < USD 50, recurring ops | agent (logged) | — |
| Spend USD 50-500, one-time | department lead agent | Ivan (next brief) |
| Spend USD 500-5K | Ivan | — (board) |
| Spend > USD 5K | Ivan + Kiki together | — |
| New client contract | Ivan | Kiki reviews delivery scope |
| Code deploy to production | Engineering lead agent (logged) | Kiki if rollback |
| Thesis chapter sign-off | Research tracker | Ivan |
| Hiring contractor > USD 500/mo | Ivan | — |
| Public-facing post (LinkedIn, blog) | Sales agent drafts → Ivan approves | — |
| Course / paid product copy | Sales + Ivan | — |
| Legal / compliance wording | Finance & Legal lead | Ivan |
| Kiki's weekly lesson topic | Kiki (her choice) | — |

If a decision is ambiguous, the default is **escalate to Ivan at next brief**, not autonomous action.

---

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