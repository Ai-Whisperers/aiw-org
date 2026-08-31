# Complete Plan v4 — AI-Native Org Buildout

> Single consolidated document. Read this end-to-end. All prior roasts, decisions, and corrections folded in.

**Last updated**: 2026-08-14
**Author**: Erebus (for Ivan, AI Whisperers Paraguay EAS)
**Scope**: AI-native org buildout for the 6 canonical departments. No project-specific work.
**Implementation mode**: AI agent (not human) — series-first between phases, parallel within phases.

---

## How to read this document

1. **Part 1** — The 1-page executive summary
2. **Part 2** — What the org looks like when this plan is done
3. **Part 3** — Department build order (Ivan's directive: management → sales → marketing → ...)
4. **Part 4** — The 9-phase structure
5. **Part 5** — Per-phase atomic tasks
6. **Part 6** — The 5 mandatory patterns every agent conforms to
7. **Part 7** — Per-department work (the actual build)
8. **Part 8** — Verification gates (one per phase)
9. **Part 9** — AI-timeline reality (how this runs in practice)
10. **Part 10** — Decisions already made (no need to re-ask)
11. **Part 11** — What this plan cannot do

---

# Part 1 — Executive Summary

### The goal

Take the **6 canonical departments** (currently abstract shells with no role granularity) and fill them with:
- **Real roles** (98 from the glossary + 12 new from analysis = 110 total)
- **Real agents** (7 lead agents + 12-15 sub-agents = ~20 total)
- **Real cadences** (cron-driven, idempotent, off-hours denser heartbeat)
- **Real guardrails** (hard stops, context-payload escalation, eval gates)
- **Real verification** (every artifact verified by a different prompt)

### What "done" looks like

A **self-running org** where:
- All 7 dept lead agents deliver on schedule for 7+ consecutive days
- Cron errors are caught within 30 min (on-hours) or 15 min (off-hours)
- No silent corruption (state schema validates every 15 min)
- Ivan's "is X live?" messages drop to 0/week
- All public-facing artifacts pass trademark scrub
- Every agent has hard stops, idempotency, context-payload, and (where applicable) reflection

### How long it takes

- **AI sessions**: 17-22 sessions
- **Turns**: ~170-240 turns
- **Calendar**: 10-15 days at realistic pace (1-2 sessions/day)
- **Ivan reviews**: ~24 reviews across 9 phases, ~4-8 hours of his time
- **Tokens**: ~360K total

### The discipline

> **One version good → replicate.** Each artifact class is built once, verified end-to-end, then replicated with modifications. This prevents template drift, scope creep, and the "7 different styles" failure mode.

> **Series between phases, parallel within phases.** No phase N+1 starts until phase N is GREEN. Within a phase, independent sub-tasks can run in the same session.

> **AI-aware timeline.** Phases sized by turns (8-30), not days. Each phase fits in 1-2 AI sessions. Every phase ends with a handoff doc the next session reads first.

---

# Part 2 — What the org looks like when this plan is done

### Org chart (post-plan)

```
                    ┌──────────────────────────────────────┐
                    │  Board (Ivan + Kiki)                │
                    │  - Strategy                         │
                    │  - Approve >$500 spend              │
                    │  - Receive morning + weekly briefs  │
                    └──────────────┬───────────────────────┘
                                   │
                    ┌──────────────▼───────────────────────┐
                    │  Cross-cutting (always-on)           │
                    │  - business-analyst (daily 06:30)    │
                    │  - management-coordinator (Mon/Thu)  │
                    │  - kiki-coach (Fri 17:00)            │
                    │  - health.sh (every 15 min)          │
                    │  - cron-heartbeat (15/30 min)        │
                    │  - state-validator (every 15 min)    │
                    │  - state-snapshot (every 6 hr)       │
                    │  - cost-cap (hourly)                 │
                    └──────────────┬───────────────────────┘
                                   │
        ┌──────────┬───────────────┼───────────────┬──────────┬──────────┐
        │          │               │               │          │          │
        ▼          ▼               ▼               ▼          ▼          ▼
   ┌────────┐ ┌────────┐     ┌────────┐     ┌────────┐ ┌────────┐ ┌────────┐
   │  Ops   │ │Finance │     │ Sales  │     │  Eng   │ │Research│ │People  │
   │  +1-2  │ │  +1-2  │     │  +2-3  │     │  +1-2  │ │  +1-2  │ │  +1    │
   │agents  │ │agents  │     │agents  │     │agents  │ │agents  │ │agent   │
   └────────┘ └────────┘     └────────┘     └────────┘ └────────┘ └────────┘
```

### Agent inventory

| Tier | Agent | Dept | Cadence | Pattern class |
|------|-------|------|---------|---------------|
| 1 | `management-coordinator` | Cross-cutting | Mon/Thu 17:00 | OPERATIONAL |
| 1 | `business-analyst` | Cross-cutting | Daily 06:30 | OPERATIONAL |
| 1 | `kiki-coach` | Cross-cutting | Fri 17:00 | CONTENT (reflection) |
| 1 | `finance-controller` | Finance & Legal | Fri 18:00 | OPERATIONAL |
| 1 | `sales-pipeline` | Sales & Growth | Daily 12:00 | CONTENT (reflection, inbound-first) |
| 1 | `engineering-roster` | Engineering & Delivery | Tue/Fri 17:00 | OPERATIONAL |
| 1 | `research-tracker` | Research & Education | Sun 18:00 | CONTENT (reflection) |
| 2 | `proposal-drafter` | Sales | On-demand | CONTENT (reflection) |
| 2 | `lead-enrichment` | Sales | Daily | OPERATIONAL |
| 2 | `marketing-content-producer` | Marketing | Mon/Wed/Fri | CONTENT (reflection) |
| 2 | `multimedia-producer` | Marketing | On-demand | CONTENT (reflection) |
| 2 | `accounting-automation` | Finance | Daily | OPERATIONAL |
| 2 | `tax-receipt-tracker` | Finance | Weekly | OPERATIONAL |
| 2 | `devops-monitor` | Engineering | Every 30 min | OPERATIONAL |
| 2 | `qa-automation-runner` | Engineering | On-PR | OPERATIONAL |
| 2 | `security-watchdog` | Engineering | Every 30 min | OPERATIONAL |
| 2 | `citation-checker` | Research | On-demand | CONTENT (reflection) |
| 2 | `thesis-tracker` | Research | Daily 06:00 | OPERATIONAL |
| 2 | `course-producer` | Research | Weekly | CONTENT (reflection) |
| 2 | `founder-bandwidth-watchdog` | People | Weekly | OPERATIONAL |
| 2 | `source-curator` | Research | Weekly | OPERATIONAL |
| 3 | `compliance-officer` | Finance | On-trigger | OPERATIONAL |
| 3 | `customer-success` | Sales | Weekly | CONTENT (reflection) |
| 3 | `devrel-manager` | Engineering | On-trigger | CONTENT |
| 3 | `chief-of-staff` | Cross-cutting | Daily | OPERATIONAL |

**Total**: 7 Tier 1 + 14 Tier 2 + 4 Tier 3 = 25 agents at full buildout.

### State files

```
/opt/data/agents/state/
├── analyst.json              # business-analyst (cross-cutting)
├── coord.json                # management-coordinator (cross-cutting)
├── kiki.json                 # kiki-coach (cross-cutting)
├── finance.json              # finance-controller
├── sales.json                # sales-pipeline + proposal-drafter
├── engineering.json          # engineering-roster
├── research.json             # research-tracker + citation-checker
├── people.json               # founder-bandwidth-watchdog
├── heartbeat-alerts.json     # rate-limit table for cron-heartbeat
├── cost-tracker.json         # per-agent daily cost ledger
└── snapshots/{date}/{hour}/  # 6-hour snapshots
```

### Cron jobs (full inventory)

19 existing + 8-12 new + 7 infra = **~30 cron jobs at buildout**.

---

# Part 3 — Department build order (Ivan's directive)

> Ivan: "start with management dept then sales then marketing and so on"

The ordering for **building out the playbooks and agents** (the per-department work) is:

### Build order

1. **Management / Cross-cutting** (Phase 4-5 first, then Phase 6 first)
   - The cross-cutting agents (`business-analyst`, `management-coordinator`, `kiki-coach`) already exist as skeletons
   - Build them out FIRST because every other dept reads their output
   - The first playbook is Operations (which IS the management dept)
2. **Sales & Growth** (Phase 5)
   - Wire `sales-pipeline` + `proposal-drafter` + `lead-enrichment`
   - Build the Sales playbook (with Marketing sub-functions)
3. **Marketing** (Phase 5 sub-task)
   - Build into the Sales playbook initially
   - Wire `marketing-content-producer` + `multimedia-producer` as sub-agents of Sales
   - Promote to its own dept at Tier 3 (per Session 1 cheatsheet: 5+ recurring clients)
4. **Engineering & Delivery** (Phase 5)
   - Wire `engineering-roster` + `devops-monitor` + `qa-automation-runner` + `security-watchdog`
   - Build the Engineering playbook
5. **Finance & Legal** (Phase 5)
   - Wire `finance-controller` + `accounting-automation` + `tax-receipt-tracker`
   - Build the Finance playbook
6. **Research & Education** (Phase 5)
   - Wire `research-tracker` + `citation-checker` + `thesis-tracker` + `course-producer`
   - Build the Research playbook
7. **People & Culture** (Phase 5)
   - Wire `founder-bandwidth-watchdog`
   - Build the People playbook

### Why this order

- **Management first**: Every other dept's agent reads from cross-cutting agents. If management is broken, the whole org is blind.
- **Sales second**: It's the only revenue dept. Without sales, the company dies. Get it working.
- **Marketing third**: Marketing supports sales. Without working sales, marketing has nothing to market.
- **Engineering fourth**: Engineering supports everything. By the time we get here, we know what infra we need.
- **Finance fifth**: Finance depends on sales + engineering outputs. Has to wait.
- **Research sixth**: Research is a flagship but not a daily-driver. Can come later.
- **People seventh**: People & Culture is internal-facing. By the time we're here, we've seen real workloads and know what bandwidth signals look like.

### What this means for Phase 5 specifically

Phase 5 builds 6 lead agents in this order (sequential, not parallel, despite my earlier "parallel" claim):

1. `business-analyst` (cross-cutting) — already done in Phase 4
2. `management-coordinator` (cross-cutting) — wire + verify
3. `kiki-coach` (cross-cutting) — wire + verify
4. `finance-controller` — wire + verify
5. `sales-pipeline` — wire + verify
6. `engineering-roster` — wire + verify
7. `research-tracker` — wire + verify

**Each agent is a complete unit**: PROMPT.md + state.json + cron job + seed outbox + 3-day soak before next.

---

# Part 4 — The 9-phase structure

| Phase | Name | Goal | Turns | Series within |
|-------|------|------|-------|---------------|
| **0** | Decisions + Setup | 8 decisions ratified; backups taken; dir tree created | 8-12 | n/a |
| **1** | Fix P0 cron errors + unify storage | 3 erroring jobs → green; single storage path | 8-13 | 1A then 1B |
| **2** | Infra: snapshot + validate + heartbeat | 3 infra scripts proven with race/duplicate tests | 26-39 | 2A → 2B → 2C |
| **3** | Lock patterns + template | 3 atomic patterns + PROMPT-TEMPLATE.md verified | 15-20 | Series |
| **4** | First reference agent | `business-analyst` rewritten with all 5 patterns, 3-day soak | 10-15 | Series |
| **5** | Replicate to 6 lead agents | 6 agents built sequentially, each verified, each 1-day soak | 30-50 | Series (per agent) |
| **6** | Per-dept playbook catalog | 1 reference playbook + 5 replicated + INDEX + matrix | 35-50 | 6A → 6B |
| **7** | Procurement + cron grid + cash-flow | Tool decisions approved; cost-cap working; grid clean | 15-20 | Series |
| **8** | Constitution v0.2.0 + docs | 6 dept specs + ORG-AGENTS bumped; deferred docs | 15-20 | Series |
| **9** | Operational disciplines + self-running | Fallbacks + security + load + chaos + gitignore + milestone | 20-30 | 9A → 9B → 9C |

**Total**: 17-22 AI sessions, ~170-240 turns, ~360K tokens.

### Phase boundaries are checkpoints

After every phase:
1. Write `PHASE-N-COMPLETE.md` (handoff doc)
2. Report status to Ivan
3. **Wait for "continue" or "phase N+1" before starting next**

This is series-first. Each phase ends GREEN before the next starts.

---

# Part 5 — Per-phase atomic tasks

Each task is answerable in 1-3 sentences. Verification is 1 step. Tasks within a phase are sequential (each depends on the previous) unless explicitly parallel.

## Phase 0 — Decisions + Setup (8-12 turns, 1 session)

**Goal**: 8 decisions ratified; 8 backups taken; work-tree created.

| # | Task | Verification |
|---|------|--------------|
| 0.1 | Read existing `ORG-AGENTS.md`, `ORCHESTRATION.md`, `state/*.json` | 5-6 reads |
| 0.2 | Write `/opt/data/agents/DECISIONS-2026-Q3.md` with D1-D8 (cost cap, sales priority, compliance, storage path, backup policy, idempotency pattern, hard-stop enforcement, repo location) | File exists, 8 numbered decisions |
| 0.3 | Backup ORG-AGENTS.md to `/opt/data/agents-v2/backups/` | Backup exists, hash matches |
| 0.4 | Backup ORCHESTRATION.md | Backup exists |
| 0.5 | Backup jobs.json | Backup exists |
| 0.6 | Backup 8 state/*.json files | 8 backups exist |
| 0.7 | Create `/opt/data/agents-v2/{patterns,specs,playbooks,prompts,backups}/` | 5 dirs exist |
| 0.8 | Write `PHASE-0-COMPLETE.md` handoff | File exists |

**Verification gate**: 8 decisions + 12 backups + 5 dirs + handoff.

---

## Phase 1 — Fix P0 cron errors + unify storage (8-13 turns, 1-2 sessions)

### Phase 1A — Atomic cron fixes (5-8 turns)

| # | Task | Verification |
|---|------|--------------|
| 1A.1 | Read jobs.json, locate morning-brief entry | Show line |
| 1A.2 | Delete `provider_snapshot` + `model_snapshot` from morning-brief | Show diff |
| 1A.3 | Same for thesis-daily-tick | Show diff |
| 1A.4 | Locate aiw-dashboard-refresh entry | Show line |
| 1A.5 | Set `workdir: /opt/data/agents/dashboards`, `script: /opt/data/agents/dashboards/render-dashboard.py` | Show diff |
| 1A.6 | Run `hermes cron list \| grep -E 'morning-brief|thesis-daily-tick|aiw-dashboard-refresh'` | All 3 state: scheduled |
| 1A.7 | Run `hermes cron run aiw-dashboard-refresh` | Dashboard HTML written |
| 1A.8 | Append fix to `/opt/data/agents/CHANGELOG-2026-Q3.md` | Entry exists |

### Phase 1B — Unify cron storage (3-5 turns)

| # | Task | Verification |
|---|------|--------------|
| 1B.1 | Check `/opt/data/cron/jobs.json` exists | ls returns file |
| 1B.2 | Diff `/opt/data/cron/jobs.json` vs `/opt/data/.hermes/cron/jobs.json` | Show diff |
| 1B.3 | If different: pick canonical, copy → symlink | `hermes cron list` returns same count from both |
| 1B.4 | Write `PHASE-1-COMPLETE.md` | File exists |

**Verification gate**: 3 cron jobs green + storage unified.

---

## Phase 2 — Infra: snapshot + validate + heartbeat (26-39 turns, 2-3 sessions)

### Phase 2A — State snapshot (atomic write) (8-12 turns)

| # | Task | Verification |
|---|------|--------------|
| 2A.1 | Write `/opt/data/agents/scripts/state-snapshot.sh` (atomic: temp + mv) | `bash -n` passes |
| 2A.2 | Manual run | `state/snapshots/{date}/{hour}/` populated |
| 2A.3 | Race test: 2 concurrent runs | Both succeed, no torn writes |
| 2A.4 | Register cron `aiw-state-snapshot-6h` at `0 */6 * * *` PYT | Cron visible |
| 2A.5 | Wait 6hr OR manual trigger | Snapshot written |

### Phase 2B — State validate (lockfile + schema) (10-15 turns)

| # | Task | Verification |
|---|------|--------------|
| 2B.1 | Write `/opt/data/agents/state/SCHEMAS.md` (≥6 sections) | File exists |
| 2B.2 | Write `/opt/data/agents/scripts/validate-state.py` with `/tmp/validate-state.lock` | py_compile passes |
| 2B.3 | Run validator | Exit 0 |
| 2B.4 | Corrupt state file manually | Exit 1 + violation report |
| 2B.5 | Restore state | Exit 0 |
| 2B.6 | Concurrent test | Second waits for first |
| 2B.7 | Register cron `aiw-state-validate-15m` at `*/15 * * * *` PYT | Cron visible |

### Phase 2C — Cron heartbeat (off-hours denser) (8-12 turns)

| # | Task | Verification |
|---|------|--------------|
| 2C.1 | Write `/opt/data/agents/scripts/cron-heartbeat.sh` with rate-limit | `bash -n` passes |
| 2C.2 | Write `state/heartbeat-alerts.json` (empty rate-limit table) | File exists |
| 2C.3 | Simulate error in jobs.json, run heartbeat | Alert posted |
| 2C.4 | Run again within 24h | Suppressed (rate-limit) |
| 2C.5 | Register `aiw-cron-heartbeat-onhours` `*/30 6-22 * * *` PYT | Visible |
| 2C.6 | Register `aiw-cron-heartbeat-offhours` `*/15 23-5 * * *` PYT | Visible |
| 2C.7 | Restore jobs.json | No alerts |
| 2C.8 | Write `PHASE-2-COMPLETE.md` | File exists |

**Verification gate**: 3 infra scripts + 3 cron jobs + race/duplicate/rate-limit tests pass.

---

## Phase 3 — Lock patterns + template (15-20 turns, 1-2 sessions)

| # | Task | Verification |
|---|------|--------------|
| 3.1 | Write `/opt/data/agents-v2/patterns/idempotency.md` (state.last_run + window pattern) | File exists, ≥3 sections |
| 3.2 | Write `/opt/data/agents-v2/patterns/idempotency-example.py` | py_compile passes |
| 3.3 | Run example: first call → action; second within window → "duplicate_run" log | Captured output |
| 3.4 | Write `/opt/data/agents-v2/patterns/hard-stops.md` (YAML schema) | File exists |
| 3.5 | Write `/opt/data/agents-v2/patterns/hard-stop-wrapper.py` | py_compile passes |
| 3.6 | Test wrapper: block `delete_repo` from non-approved | Blocked + log |
| 3.7 | Test wrapper: allow `read_state` | Allowed + log |
| 3.8 | Write `/opt/data/agents-v2/patterns/context-payload.md` (6-field JSON schema) | File exists, schema valid |
| 3.9 | Write `/opt/data/agents-v2/patterns/reflection-loop.md` (for content agents) | File exists |
| 3.10 | Write `/opt/data/agents-v2/patterns/PROMPT-TEMPLATE.md` (12 sections, with `fallback_model` field) | 12 sections present |
| 3.11 | Write `/opt/data/agents-v2/patterns/trademark-scrub.sh` | `bash -n` passes |
| 3.12 | Test trademark-scrub on a sample file with banned term | Catches it |
| 3.13 | Write `PHASE-3-COMPLETE.md` | File exists |

**Verification gate**: 4 patterns + 1 template + 1 verifier, all end-to-end verified.

---

## Phase 4 — First reference agent (10-15 turns, 1 session)

**Goal**: ONE complete, working reference agent (`business-analyst`) with all 5 mandatory patterns.

| # | Task | Verification |
|---|------|--------------|
| 4.1 | Read current `business-analyst/PROMPT.md` | Read |
| 4.2 | Copy PROMPT-TEMPLATE.md to `business-analyst/PROMPT.md` | File overwritten |
| 4.3 | Fill dept-specific 10 sections | All placeholders replaced |
| 4.4 | Add Hard Stops table (3 stops for business-analyst) | Wrapper validates |
| 4.5 | Add Idempotency Contract section | Section present |
| 4.6 | Add Context-Packaging Escalation section | Section present |
| 4.7 | Add fallback_model field | Field present |
| 4.8 | Verify `grep -c "^## " PROMPT.md` returns 12 | Count = 12 |
| 4.9 | Save as `business-analyst/PROMPT.md.reference` (gold copy) | Gold copy exists |
| 4.10 | Update `ORCHESTRATION.md` row for `business-analyst` | Row reflects changes |
| 4.11 | Manual run `hermes cron run aiw-business-analyst-daily` | Outbox + state updated |
| 4.12 | Trigger duplicate within window | "duplicate_run" logged |
| 4.13 | Trigger simulated escalation | Context payload in outbox |
| 4.14 | Run trademark-scrub on PROMPT.md | Zero matches |
| 4.15 | Write `PHASE-4-COMPLETE.md` | File exists |

**Verification gate**: 1 agent has 12-section PROMPT.md + 5 patterns + 3-day soak.

---

## Phase 5 — Replicate to 6 lead agents sequentially (30-50 turns, 4-6 sessions)

**Order** (Ivan's directive, modified for dependencies):
1. `management-coordinator` (cross-cutting, infra monitoring)
2. `kiki-coach` (cross-cutting, training)
3. `finance-controller` (financial discipline, smaller scope)
4. `sales-pipeline` (revenue, biggest stakes)
5. `engineering-roster` (technical delivery)
6. `research-tracker` (knowledge work)

**Per-agent pattern** (~5-8 turns each):

| Sub-task | Verification |
|----------|--------------|
| Copy PROMPT-TEMPLATE.md → `<agent>/PROMPT.md` | File written |
| Fill dept-specific 10 sections | All placeholders replaced |
| Add Hard Stops (3-5 dept-specific) | Wrapper validates |
| Add Idempotency Contract | Section present |
| Add Context-Packaging Escalation | Section present |
| Add Reflection Loop (content agents only: sales-pipeline, kiki-coach, research-tracker) | Section present |
| Add fallback_model | Field present |
| Create `state/<dept>.json` with initial schema | File exists |
| Create `outbox/.gitkeep` | File exists |
| Seed example outbox `<date>.md` | File exists |
| Verifier pass: 12 sections + trademark scrub + URL check | All pass |
| Register cron job | `hermes cron list` shows |
| Run `grid.sh` verify zero collisions | No collisions |
| Manual run | Valid outbox |
| 1-day soak + write `<agent>-DAY-1-OBSERVATION.md` | Outbox history exists |

**Per-agent verification gate**: 12 sections + 5 patterns + 1-day soak + grid clean.

**Phase 5 verification gate**: All 6 agents conform + 6 cron jobs + grid clean + 1-day soak each.

---

## Phase 6 — Per-dept playbook catalog (35-50 turns, 3-4 sessions)

### Phase 6A — Reference playbook (Operations) + master INDEX (12-18 turns)

| # | Task | Verification |
|---|------|--------------|
| 6A.1 | Read roles-glossary.md Operations roles | Read |
| 6A.2 | Write `/opt/data/agents-v2/playbooks/PLAYBOOK-TEMPLATE.md` | ≥10 sections |
| 6A.3 | Write `01-operations.md` from template + glossary | File exists |
| 6A.4 | `curl -I` every tool URL | All 200 or logged |
| 6A.5 | Trademark scrub | Zero matches |
| 6A.6 | Save as `01-operations.md.reference` (gold) | Gold exists |
| 6A.7 | Write `00-INDEX.md` master cross-dept table | File exists |
| 6A.8 | Write `PHASE-6A-COMPLETE.md` | File exists |

### Phase 6B — Replicate to 5 more playbooks + matrix (23-32 turns)

**Order** (Ivan's directive): Sales → Marketing (sub of Sales) → Engineering → Finance → Research → People

| # | Task | Verification |
|---|------|--------------|
| 6B.1 | Write `02-sales-growth.md` (includes Marketing sub-functions) | File exists |
| 6B.2 | Write `03-engineering-delivery.md` | File exists |
| 6B.3 | Write `04-finance-legal.md` | File exists |
| 6B.4 | Write `05-research-education.md` | File exists |
| 6B.5 | Write `06-people-culture.md` | File exists |
| 6B.6 | `curl -I` every tool URL in all 5 playbooks | All 200 or logged |
| 6B.7 | Trademark scrub on all 5 | Zero matches |
| 6B.8 | Update `00-INDEX.md` to add 5 dept rows | File updated |
| 6B.9 | Write `role-tool-sop-matrix.md` (pivot table) | File exists |
| 6B.10 | Cross-check role count = 98 baseline + 12 new = 110 | Numbers match |
| 6B.11 | Add 12 new roles from analysis to relevant playbooks | 12 roles added |
| 6B.12 | Write `PHASE-6B-COMPLETE.md` | File exists |

**Phase 6 verification gate**: 8 files (1 INDEX + 6 playbooks + 1 matrix), 110 roles, all URLs verified, zero trademarks.

---

## Phase 7 — Procurement + cron grid + cash-flow (15-20 turns, 1-2 sessions)

| # | Task | Verification |
|---|------|--------------|
| 7.1 | Get pre-Phase-7 budget approval from Ivan | Approval documented |
| 7.2 | Write `/opt/data/agents/research/tool-stack-decisions.md` (Sections A-F) | File exists |
| 7.3 | Cost roll-up: defaults, upgrades, year-1 | Numbers documented |
| 7.4 | Cash-flow model: MRR + burn + new tools + 3/6/12-month runway | Numbers documented |
| 7.5 | FX exposure notes (Gs/USD; 15% historical depreciation) | Notes documented |
| 7.6 | Identify 3-5 vendor consolidations | Listed in Section D |
| 7.7 | Rank procurement by ROI | Listed in Section E |
| 7.8 | Pricing refresh (per AI-SDR 2026 reckoning) | Updated multiplier documented |
| 7.9 | Write `/opt/data/agents/scripts/cost-cap.sh` (per-agent daily + total) | `bash -n` passes |
| 7.10 | Test cost-cap: simulate over-cap | Script halts + alerts |
| 7.11 | Register cron `aiw-cost-cap-1h` at `0 * * * *` PYT | Cron visible |
| 7.12 | Run `grid.sh`, verify zero collisions | Zero collisions |
| 7.13 | Update `ORCHESTRATION.md` with all new cron IDs | All rows present |
| 7.14 | Write `PHASE-7-COMPLETE.md` | File exists |

**Verification gate**: Ivan budget approved + decisions doc + cost-cap tested + grid clean.

---

## Phase 8 — Constitution v0.2.0 + docs (15-20 turns, 2 sessions)

| # | Task | Verification |
|---|------|--------------|
| 8.1 | Read current `01-operations.md` (v0.1.0) | Read |
| 8.2 | Add Sub-roles, Sub-agents, Tooling, SOP sections | 4 new sections |
| 8.3 | Bump version 0.1.0 → 0.2.0 | Header updated |
| 8.4 | Repeat 8.1-8.3 for depts 2-6 (parallel) | All 6 at v0.2.0 |
| 8.5 | Read current `ORG-AGENTS.md` (v0.1.0) | Read |
| 8.6 | Update TL;DR, Department directory, Decision rights, Handoff matrix, Cadence map, State files, Agent design vocabulary | All 8 sections updated |
| 8.7 | Add ON-CALL section (Ivan primary, Kiki backup) | Section present |
| 8.8 | Add Cultural Rituals Preservation checklist | Checklist present |
| 8.9 | Bump version 0.1.0 → 0.2.0 | Header updated |
| 8.10 | Add CHANGELOG entry (≥5 substantive items) | Entry exists |
| 8.11 | Write `DEFERRED-ROLES.md` (12 missing roles + triggers) | File exists |
| 8.12 | Write `DEFERRED-AGENTS.md` (Tier 2/3 + triggers) | File exists |
| 8.13 | Write `REVIEW-2026-Q4.md` (30/60/90-day checklist) | File exists |
| 8.14 | Write `BURNOUT-SIGNAL-SPEC.md` (founder-bandwidth-watchdog) | File exists |
| 8.15 | Write `PHASE-8-COMPLETE.md` | File exists |

**Verification gate**: 6 specs at v0.2.0 + ORG-AGENTS v0.2.0 + CHANGELOG + deferred docs.

---

## Phase 9 — Operational disciplines + self-running (20-30 turns, 2-3 sessions)

### Phase 9A — Model fallbacks + gitignore spec (5-8 turns)

| # | Task | Verification |
|---|------|--------------|
| 9A.1 | Add fallback_model field to PROMPT-TEMPLATE.md | Template updated |
| 9A.2 | Add fallback to all 7 lead agents' PROMPT.md | 7 updated |
| 9A.3 | Audit current `.gitignore` | Audit complete |
| 9A.4 | Write `/opt/data/agents-v2/GITIGNORE-POLICY.md` | File exists |
| 9A.5 | Write `.gitignore` snippet for new repos | File exists |

### Phase 9B — Security + load + chaos tests (10-15 turns)

| # | Task | Verification |
|---|------|--------------|
| 9B.1 | Security review: list all side-effect actions across 7 agents | Risk matrix exists |
| 9B.2 | Load test: simulate 7 agents firing at once | All complete <5 min |
| 9B.3 | Chaos test: kill LLM API mid-run | Agent exits gracefully |
| 9B.4 | Chaos test: corrupt state file mid-run | Agent detects + reports |
| 9B.5 | Chaos test: malformed tool response | Agent retries or escalates |

### Phase 9C — Self-running milestone (5-7 turns)

| # | Task | Verification |
|---|------|--------------|
| 9C.1 | Write `/opt/data/agents-v2/SELF-RUNNING-CRITERIA.md` | File exists |
| 9C.2 | Run 7-day soak: all 7 agents deliver on schedule | Outbox files exist |
| 9C.3 | Count Ivan "is X live?" messages for 7 days | Number tracked |
| 9C.4 | If criteria met: write `SELF-RUNNING-ACHIEVED.md` | File exists |
| 9C.5 | If not: identify gap, add to DEFERRED or fix | Gap documented |
| 9C.6 | Write `PHASE-9-COMPLETE.md` (final) | File exists |

**Phase 9 verification gate**: All artifacts verified + self-running milestone achieved OR gap documented.

---

# Part 6 — The 5 mandatory patterns every agent conforms to

Every agent's PROMPT.md must include these 5 sections (or have them explicitly marked as N/A with reason).

### Pattern 1 — Hard Stops (action-level approval gates)

```yaml
hard_stops:
  - action: write_state_file
    require_approval: false
    rate_limit_per_run: 50
    description: "Agent writes to its own state.json"
  - action: send_external_message
    require_approval: true
    approved_human: ivan
    description: "Any outbound communication"
  - action: merge_pr
    require_approval: true
    approved_human: kiki
    rate_limit_per_run: 5
```

**Enforcement**: `hard-stop-wrapper.py` runtime wrapper. Hard rules in prompt text are NOT sufficient.

### Pattern 2 — Idempotency Contract

```
## Idempotency Contract
- Idempotency key: state.last_run + window
- Window: [24h for daily, 12h for biweekly, 7d for weekly]
- If duplicate: skip + log "duplicate_run"
- Override: state.override_possible=true (Ivan can force via manual trigger)
```

**Enforcement**: `idempotency-example.py` check before action.

### Pattern 3 — Context-Packaging Escalation

```json
{
  "escalation_context": {
    "reasoning_trace": "<last 500 tokens of chain-of-thought>",
    "tool_calls_made": [{"tool": "...", "args": {...}, "result": "..."}],
    "state_changes_intended": {"key": "old_val → new_val"},
    "why_escalated": "<one-line>",
    "what_tried_first": "<one-line>",
    "override_token": "<uuid>"
  }
}
```

**Enforcement**: every escalation event ships this payload.

### Pattern 4 — Reflection Loop (content-producing agents only)

```
## Reflection Loop (3 steps)
1. Draft output
2. Self-critique against criteria:
   - [criterion 1 specific to dept]
   - [criterion 2]
   - [criterion 3]
3. If score < 8/10: refine. If >= 8/10: write.
```

**Enforcement**: prompt structure, not code.

### Pattern 5 — Fallback Model

```
## Fallback Model
- Primary: minimax-m3 (or current)
- Fallback: litellm/primary
- Retry on 5xx: 3 attempts with exponential backoff
- If both fail: exit + alert (no silent halt)
```

**Enforcement**: agent runtime.

---

# Part 7 — Per-department work (the actual build)

This is the detailed playbook for each department. Each section: roles, agents, cadences, hard stops, SOPs.

## 7.1 — Operations / Management (cross-cutting, build first)

### Roles
- Operations Lead (Ivan)
- Repo Steward (sub-agent of management-coordinator)
- Asset Tracker (sub-agent of management-coordinator)
- Vendor Coordinator (Ivan, manual)
- Compliance Watchdog (sub-agent of finance-controller)
- Watchdog Engineer (sub-agent of engineering-roster)

### Agents (Tier 1)
- `management-coordinator` (Mon/Thu 17:00 PYT) — cross-repo stuck/stale/PR review
- `business-analyst` (Daily 06:30 PYT) — pipeline/revenue/sites snapshot
- `kiki-coach` (Fri 17:00 PYT) — weekly lesson

### Agents (Tier 2)
- `source-curator` (weekly) — source-materials freshness sweep
- `founder-bandwidth-watchdog` (weekly) — burnout signal per `BURNOUT-SIGNAL-SPEC.md`

### Hard stops (management-coordinator)
- write_state: no approval, rate 50/run
- comment_on_issue: require ivan
- close_issue: require ivan

### Hard stops (business-analyst)
- write_state: no approval, rate 50/run
- send_chat: no approval (delivers to origin)
- read_repo: no approval

### Hard stops (kiki-coach)
- write_state: no approval
- send_chat: no approval (lesson delivery)
- modify_curriculum: require kiki

### SOPs
- **Daily 06:00**: morning-brief cron (existing)
- **Daily 06:30**: business-analyst brief
- **Mon/Thu 17:00**: management-coordinator brief
- **Fri 17:00**: kiki-coach lesson
- **Every 15 min**: health.sh watchdog
- **Every 15 min (on-hours) / 30 min (off-hours)**: cron-heartbeat
- **Every 15 min**: state-validator
- **Every 6 hours**: state-snapshot
- **Hourly**: cost-cap

---

## 7.2 — Sales & Growth (build second)

### Roles
- Head of Sales (Ivan)
- SDR / Outbound Rep (sub-agent of sales-pipeline, deferred per D2)
- Account Executive (Ivan, closing)
- Proposal Writer (sub-agent: `proposal-drafter`)
- Marketing Manager (Ivan + `marketing-content-producer` agent)
- Multimedia Designer (sub-agent: `multimedia-producer`)
- Lead Enrichment Specialist (sub-agent: `lead-enrichment`)

### Agents (Tier 1)
- `sales-pipeline` (Daily 12:00 PYT) — inbound triage, ICP scoring

### Agents (Tier 2)
- `proposal-drafter` (on-demand, after discovery call) — drafts proposals
- `lead-enrichment` (Daily) — adds intent signals, scores leads
- `marketing-content-producer` (Mon/Wed/Fri) — blog posts, social
- `multimedia-producer` (on-demand) — video, graphics, podcast
- `customer-success` (Tier 3, weekly) — post-sale retention, deferred until 5+ clients

### Hard stops (sales-pipeline)
- write_state: no approval
- send_outreach: require ivan (hard rule from `b2b-cold-outreach-pitch` skill)
- update_deal_stage: no approval
- send_proposal: require ivan (per proposal pricing skill)

### Hard stops (proposal-drafter)
- write_draft: no approval
- send_proposal: require ivan
- apply_discount: require ivan (hard rule)

### SOPs
- **Daily 12:00**: sales-pipeline lead triage
- **Daily**: lead-enrichment (overnight data refresh)
- **Mon/Wed/Fri**: marketing-content-producer
- **On-demand**: proposal-drafter (triggered after discovery call booked)
- **On-demand**: multimedia-producer (triggered after content draft approved)
- **Weekly Friday 16:00**: pipeline summary (handoff to finance-controller)

### ICP validation (Phase 5 task per SA-1)
- 3 ICPs in `marketing-strategy/playbook.md`: Solo entrepreneur / SME ops manager / Corporate innovation lead
- Validation trigger: 30 days of lead data
- Refresh annually

### Conversion funnel targets (per SA-2)
- leads → calls: >40%
- calls → proposals: >60%
- proposals → signed: >30%
- Pipeline value coverage: 3x quarterly target

### Test deal: richar-ruiz
- Use as canary for entire pipeline
- Track conversion metrics specifically
- Surface in every sales-pipeline brief until signed

---

## 7.3 — Marketing (sub-function of Sales at Tier 1, promotes to own dept at Tier 3)

Per Session 1 cheatsheet: "Marketing splits from Sales at Tier 3 (>10 recurring clients OR >$2K marketing budget)."

For Tier 1: Marketing = sub-function of Sales, with 2 dedicated agents.

### Roles (in this phase)
- Marketing Manager (Ivan)
- Content Producer (`marketing-content-producer` agent)
- Multimedia Designer (`multimedia-producer` agent)

### Roles (deferred to Tier 3)
- Brand Manager
- SEO Specialist
- Email Marketing Specialist
- Paid Ads Specialist (FORBIDDEN: trademark banlist on Plataforma de Redes, Plataforma de videos cortos, etc.)
- Community Manager
- Event Coordinator
- Partnerships Manager

### Hard stops (marketing-content-producer)
- write_state: no approval
- publish_post: require ivan (per trademark banlist — never auto-publish)
- modify_brand_voice: require ivan

### SOPs
- **Mon/Wed/Fri**: marketing-content-producer (3 posts/week)
- **On-demand**: multimedia-producer

---

## 7.4 — Engineering & Delivery (build fourth)

### Roles
- CTO/Eng Lead (Kiki)
- Backend / Frontend / Full-stack Engineer (Kiki, consolidated)
- DevOps / SRE (sub-agents)
- QA Engineer (automated test suite = CRON_WORKFLOW)
- Security Engineer (sub-agent)
- AI Safety Engineer (Tier 2, per OWASP 2026)

### Agents (Tier 1)
- `engineering-roster` (Tue/Fri 17:00 PYT) — deploy health, PR queue, Kiki workload

### Agents (Tier 2)
- `devops-monitor` (every 30 min) — Docker Swarm, Traefik, CF Workers
- `qa-automation-runner` (on-PR) — runs test suite
- `security-watchdog` (every 30 min) — scans for vulnerabilities, watches for exposed credentials

### Hard stops (engineering-roster)
- write_state: no approval
- merge_pr: no approval if auto-mergeable, require kiki otherwise
- deploy_prod: require kiki (hotfix may skip with logged reason)
- rollback: no approval (logged)
- force_push: require ivan (per aiw-git-safety skill)

### SOPs
- **Tue/Fri 17:00**: engineering-roster brief
- **Every 30 min**: devops-monitor
- **Every 30 min**: security-watchdog
- **On-PR**: qa-automation-runner
- **Every 15 min**: existing site-health (already running)

### Stack reality (per `04-engineering-delivery.md` lines 86-95)
- Hostinger VPS (38.9.96.179) — primary prod
- Servarica Host A — secondary
- Traefik v3.5.3 reverse proxy
- Docker Swarm (not K8s)
- CF Worker + R2 for static deploys
- Vercel 403 — DO NOT attempt deploys

---

## 7.5 — Finance & Legal (build fifth)

### Roles
- CFO/Controller (Ivan)
- Accountant (external contractor, annual)
- Bookkeeper (sub-agent of finance-controller)
- AP/AR Specialist (sub-agent)
- Procurement Officer (Ivan, manual for now)
- Legal Counsel (external contractor, retainer)
- Tax Specialist (external accountant)
- Pricing Analyst (Ivan + sub-agent)
- Compliance Officer (Tier 3, deferred until first EU client per D3)

### Agents (Tier 1)
- `finance-controller` (Fri 18:00 PYT) — weekly close, runway, contracts

### Agents (Tier 2)
- `accounting-automation` (Daily) — categorizes expenses, generates invoices
- `tax-receipt-tracker` (Weekly) — tracks receipts for tax filing

### Hard stops (finance-controller)
- write_state: no approval
- send_invoice: require ivan
- apply_refund: require ivan
- sign_contract: require ivan (hard rule, can't be automated)
- modify_pricing: require ivan

### SOPs
- **Fri 18:00**: finance-controller weekly close
- **Daily**: accounting-automation
- **Weekly**: tax-receipt-tracker
- **On-trigger**: EU client → HARD-STOP until Compliance Officer filled

### Compliance hard-stop rule
> No EU client contract until `DEFERRED-ROLES.md` Compliance Officer trigger met (filled by named person, not Ivan wearing the hat).

### Cash-flow model (Phase 7 task 7.4)
- Current: $240/mo MRR, $400-600/mo burn
- After Phase 7: +$200/mo new tools = $600-800/mo burn
- Runway at current: many months
- Runway after Phase 7: 3-4 months if MRR doesn't grow
- Trigger to reduce tool spend: if MRR < $400/mo for 60 days

### FX exposure (Phase 7 task 7.5)
- Gs/USD historical: ~15% depreciation 2025-2026
- New SaaS contracts in USD: priced at spot rate, no hedge
- Recommendation: avoid 12-month USD commitments; prefer monthly billing

---

## 7.6 — Research & Education (build sixth)

### Roles
- Research Lead (Ivan)
- Researcher (Ivan + research-tracker agent)
- Writer / Editor (Ivan + sub-agent)
- Citation / Bibliography Specialist (Tier 2, sub-agent)
- Course Designer (Ivan)
- Course Producer (Tier 2, sub-agent)
- Subject Matter Expert (external contractors)
- Research Engineer (Tier 2)
- Publication Coordinator (Tier 2)
- Source Curator (Tier 2, owns source-materials/ per Q4)

### Agents (Tier 1)
- `research-tracker` (Sun 18:00 PYT) — thesis status, publications, courses

### Agents (Tier 2)
- `citation-checker` (on-demand) — verifies every citation in research output
- `thesis-tracker` (Daily 06:00) — fine-grained thesis progress (existing `thesis-daily-tick`)
- `course-producer` (Weekly) — slides + transcript generation
- `source-curator` (Weekly) — source-materials freshness sweep (per Q4)

### Hard stops (research-tracker)
- write_state: no approval
- update_thesis_metadata: no approval
- submit_arxiv: require ivan
- publish_course_module: require ivan + kiki (technical review)

### SOPs
- **Sun 18:00**: research-tracker weekly thesis checkpoint
- **Daily 06:00**: thesis-tracker (existing thesis-daily-tick)
- **Weekly**: course-producer
- **Weekly**: source-curator
- **On-demand**: citation-checker (before any external publication)

### Thesis integration
- `/opt/data/thesis-active/` is the source
- `research-tracker` reads `THESIS_STATE.md` top 50 lines
- thesis-tracker reads `/opt/data/thesis-active/` git log
- Thesis milestone schema in `state/research.json`:
  ```json
  {
    "thesis": {
      "chapter": 3,
      "chapter_title": "Methodology",
      "last_commit": "2026-08-12",
      "target_date": null,
      "blocker": null
    }
  }
  ```

### Source-materials triage (Phase 6 task per RE-1)
- Current: 30+ files in `/opt/data/source-materials/`
- Triage: classify each as canonical/superseded/draft
- Add naming convention: `{topic}/{source}.md`
- Add retirement policy: superseded by newer source = move to `/archive/`

---

## 7.7 — People & Culture (build seventh)

### Roles
- Head of People (Ivan + Kiki, co-owned)
- Recruiter (deferred until first FTE hire)
- Onboarding Specialist (deferred)
- Performance Coach (`kiki-coach` agent for Kiki)
- Recognition Lead (periodic rituals)

### Agents (Tier 1)
- `kiki-coach` (Fri 17:00 PYT) — weekly lesson

### Agents (Tier 2)
- `founder-bandwidth-watchdog` (Weekly) — burnout signal per `BURNOUT-SIGNAL-SPEC.md`

### Hard stops (kiki-coach)
- write_state: no approval
- send_chat (lesson delivery): no approval
- modify_curriculum: require kiki

### SOPs
- **Fri 17:00**: kiki-coach lesson
- **Weekly**: founder-bandwidth-watchdog
- **On milestone**: recognition ritual (per `06-people-culture.md` lines 68-75)

### Burnout signal spec (per `BURNOUT-SIGNAL-SPEC.md`)
- Track: hours-worked (calendar density), chat sentiment (informal), deadline clustering
- Threshold: 70+ hrs/week sustained 3 weeks → page Ivan
- Trigger: any founder reports "burned out" in chat → check-in
- Escalation: if no recovery in 2 weeks → suggest PTO

### Cultural rituals (PRESERVE in constitution v0.2.0)
1. First signed contract in new ICP → LinkedIn post
2. Thesis chapter published → celebration
3. Major deploy win → engineering notes
4. Kiki milestone → kiki-coach notes in next lesson

### Curriculum refresh (Phase 5 task per PE-3)
- Current 8 topics: Git rebase, App Router stack trace, CODEOWNERS, env vars, Tailwind v4, CF Worker traces, Docker Swarm deploy logs, Husky pre-commit
- Add (Phase 5): agent ops track — PROMPT.md patterns, eval gates, hard stops, idempotency, cron schedules, agent observability

---

# Part 8 — Verification gates (one per phase)

| Phase | Gate | Pass criteria |
|-------|------|---------------|
| **0** | Setup complete | 8 decisions + 12 backups + 5 dirs + handoff |
| **1** | P0 cron errors fixed | 3 jobs green + storage unified |
| **2** | Infra proven | snapshot/validate/heartbeat all tested with race/duplicate/rate-limit |
| **3** | Patterns locked | 4 patterns + 1 template + 1 verifier, end-to-end verified |
| **4** | First agent reference | business-analyst conforms to template, 3-day soak |
| **5** | 6 agents replicated | All conform + 6 cron jobs + grid clean + 1-day soak each |
| **6** | Playbook catalog | 8 files + 110 roles + all URLs verified + zero trademarks |
| **7** | Procurement + grid + cash-flow | Ivan budget approved + decisions doc + cost-cap + grid clean |
| **8** | Constitution bumped | 6 specs v0.2.0 + ORG-AGENTS v0.2.0 + CHANGELOG + deferred docs |
| **9** | Operational disciplines + self-running | All verified + self-running achieved OR gap documented |

---

# Part 9 — AI-timeline reality (how this runs in practice)

### The discipline

> **One phase = 1-2 AI sessions.** Phases sized by turns (8-50 turns), not days.

### Session shape

A typical session looks like:
1. Read `PHASE-(N-1)-COMPLETE.md` (the handoff from last session)
2. Execute phase tasks (5-30 turns)
3. Verify each task (1 step per task)
4. Write `PHASE-N-COMPLETE.md` handoff
5. Report status, stop, wait for Ivan's "continue"

### What fits in one session

- **Small phase** (10-15 turns): Phase 0, Phase 1, Phase 4
- **Medium phase** (15-30 turns): Phase 1B, Phase 3, Phase 7, Phase 8
- **Large phase** (30-50 turns): Phase 2, Phase 5, Phase 6, Phase 9

Large phases split into sub-phases within themselves (e.g., Phase 2 = 2A + 2B + 2C).

### Token budget per phase

- Phase 0-1: ~30K tokens
- Phase 2: ~50K tokens
- Phase 3: ~40K tokens
- Phase 4: ~30K tokens
- Phase 5: ~80K tokens (7 agents × ~12K each)
- Phase 6: ~70K tokens (6 playbooks + matrix)
- Phase 7: ~30K tokens
- Phase 8: ~30K tokens
- Phase 9: ~40K tokens
- **Total**: ~400K tokens

### Calendar estimate

- 17-22 sessions at 1-2 sessions/day = 9-22 calendar days
- Realistic with Ivan reviews + model rate limits + retries: 15-20 calendar days
- 30-day post-rollout loop adds 30 days for self-running validation

### Ivan reviews per phase

| Phase | Reviews needed | Time per review |
|-------|----------------|-----------------|
| 0 | 1 (decisions) | 5 min |
| 1 | 0 (auto-verified) | — |
| 2 | 0 (auto-verified) | — |
| 3 | 1 (pattern sanity check) | 10 min |
| 4 | 1 (first brief read) | 5 min |
| 5 | 6 (one per agent brief) | 5 min each = 30 min |
| 6 | 1 (playbook INDEX review) | 15 min |
| 7 | 1 (budget approval) | 20 min |
| 8 | 1 (constitution ratification) | 30 min |
| 9 | 1 (self-running criteria) | 15 min |
| **Total** | **13 reviews** | **~2.5 hours** |

### Failure modes I expect

| Mode | Likelihood | Defense |
|------|-----------|---------|
| Model rate limit mid-session | Medium | Retry with backoff; if persists, stop + handoff |
| Jobs.json corruption during edit | Low | Phase 0 backups + lockfile |
| Agent PROMPT.md format drift | Medium | Template verifier per agent (Phase 5) |
| Trademark slippage | Medium | Per-artifact scrub in every phase |
| Playbook URL goes stale | Medium | `curl -I` per URL in Phase 6 |
| Cron collision from Phase 5 adds | Medium | `grid.sh` after every cron add |
| Ivan offline for 2+ days | Low | Plan pauses at phase boundary, no harm |
| Budget overrun in Phase 7 | Low | Pre-Phase-7 approval gate |

---

# Part 10 — Decisions already made (no need to re-ask)

Per Ivan's directive: "you decide on the answers, you built everything, not me."

### D1 — Per-agent daily cost cap
**$1/day per agent, $10/day total.** Override possible for content agents (sales-pipeline, kiki-coach, research-tracker) up to $3/day during reflection loop.

### D2 — Sales priority order
**Inbound-first.** Outbound sequencing deferred until inbound saturates. Trigger to add outbound: 20+ inbound leads/week sustained 4 weeks.

### D3 — Compliance Officer role
**Named role in `DEFERRED-ROLES.md`. Ivan wears the hat for now.** Hard-stop on EU client contracts until role is filled by named person (not Ivan alone).

### D4 — Storage path
**`/opt/data/agents-v2/` as new sibling dir** (not inside existing `/opt/data/agents/`, not a new repo).

### D5 — Backup policy
**Gitignored + 6-hour snapshot cron + manual archive.** State files NOT in version control (contain secrets).

### D6 — Canonical idempotency pattern
**`state.last_run + window check`.** Per-agent window: 24h daily, 12h biweekly, 7d weekly. Override_possible=true with manual Ivan trigger.

### D7 — Hard-stop enforcement
**PROMPT.md prose + runtime wrapper (`hard-stop-wrapper.py`).** Both. Prompt text is documentation; wrapper is enforcement.

### D8 — Template-first vs template-after
**Template AFTER first agent.** Phase 3 produces the template from `business-analyst` reference (gold copy). Reason: writing template first without a real instance produces a generic template that doesn't fit real agents.

### Q1 — agents-v2 location
**New dir `/opt/data/agents-v2/`** (sibling of existing).

### Q2 — When to add sub-agents
**Trigger = lead agent's brief exceeds 500 words for 2 consecutive weeks.** Per-agent trigger table documented in `SUB-AGENT-TRIGGER.md`.

### Q3 — Eval-gate scope
**POC on `business-analyst` only.** Document pattern. Defer full rollout to 30-day post-rollout loop.

### Q4 — Source-materials ownership
**Research dept owns policy. `source-curator` agent ships in Tier 2** (Phase 5 follow-on). Trigger: source-materials > 50 files.

### Q5 — When to write eval-gate infra
**After Phase 8 lands, as first item of 30-day loop.**

### Token budget per phase
**50K cap.** Over → defer to next phase.

### Phase 4 soak length
**3 days, not 7.** Phase 5 has its own 1-day soak per agent.

### Verifier model
**Same model, different prompt + skill.** Budget reality.

### Self-running milestone trigger
**7 days all-green + 0 "is X live?" messages/week.** Matches user's stated frustration pattern.

### Hard-stop on EU clients
**Until Compliance Officer role filled by named person** (per D3).

### Chaos test depth
**3 scenarios: LLM down, corrupt state, malformed tool response.** Enough to catch documented failure modes.

---

# Part 11 — What this plan cannot do

The plan cannot:
- **Hire a real human** for any role (Ivan's decision, not mine)
- **Sign a real contract** (Ivan's authority)
- **Spend real money** without Ivan's approval (Phase 7 gate)
- **Make decisions that affect people's lives** (FTE hire, EU client, etc.)
- **Replace Ivan's judgment** on values, mission, strategy
- **Run without Ivan's "continue"** between phases (by design)

The plan CAN:
- Wire agents to do mechanical work
- Maintain the agent layer autonomously
- Surface decisions for Ivan to make
- Audit itself for compliance (trademark, hard stops, idempotency)
- Self-test its own infrastructure (chaos tests, load tests)
- Detect and report failures within minutes (heartbeat)

---

# Final note

When Ivan says **"go"**, I execute Phase 0 (8-12 turns, 1 session).

Phase 0 takes ~5 minutes of AI time and produces 1 decisions doc + 12 backups + 5 directories + 1 handoff doc.

Then I stop. Wait for Ivan's "continue" or "phase 1".

The plan cannot run end-to-end without Ivan's "continue" between phases. **This is by design** — series-first discipline, AI-aware checkpoints, and respect for Ivan's authority.

---

**Document path**: `/opt/data/agents-v2/PLAN-v4.md`
**File size**: comprehensive (single document)
**Last updated**: 2026-08-14
**Version**: 4.0
**Status**: Ready for execution
