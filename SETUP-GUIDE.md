# AI Whisperers — Complete Management & Agent Setup Guide

> Built 2026-08-13 by Erebus. The complete "what's needed, what's built, what to do" reference for the management layer at AI Whisperers Paraguay EAS.
>
> **Read this once** — then use `/opt/data/agents/ORCHESTRATION.md` as the day-to-day reference.

---

## How to use this guide

This is organized in **7 layers**, each answering a different question:

| Layer | Question |
|-------|----------|
| 1 | What is the management layer supposed to do? |
| 2 | What agents/departments do we need? |
| 3 | What Hermes infrastructure do we need? |
| 4 | What data/state do the agents need? |
| 5 | What skills + repos + tools? |
| 6 | What cron jobs run when? |
| 7 | What's still TODO vs DONE? |

---

## §1 The Philosophy

The org layer follows **3 principles** (also called "AGENTS.md discipline"):

1. **Every recurring decision has exactly one owner** (human or agent). No ambiguity.
2. **Cross-department handoffs go through `state/*.json` files**, not direct chat. Auditable.
3. **Escalation, not autonomy**: anything outside decision rights gets surfaced to Ivan at next brief. Agents don't silently act.

If you remember nothing else, remember those 3.

---

## §2 The Org Structure

### 6 departments + 3 cross-cutting roles

```
                          ┌─────────────────────┐
                          │  Board (Ivan)        │
                          │  - Direction          │
                          │  - Approves >USD 500  │
                          │  - Signs contracts    │
                          └──────────┬───────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
       ┌────────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
       │ business-       │  │ management-     │  │ health.sh       │
       │ analyst (daily) │  │ coordinator     │  │ (every 5m)      │
       │                 │  │ (Mon+Thu)       │  │                 │
       └────────┬────────┘  └────────┬────────┘  └─────────────────┘
                │                    │
   ┌────────────┴────────────────────┴────────────────────────────┐
   │                                                               │
┌──▼─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────▼────┐
│Operations  │ │Finance & │ │Sales &   │ │Engr &    │ │Research  │ │People & │
│            │ │Legal     │ │Growth    │ │Delivery  │ │Education │ │Culture  │
│ management-│ │ finance- │ │ sales-   │ │ eng-     │ │ research-│ │ kiki-   │
│ coord      │ │ control- │ │ pipeline │ │ roster   │ │ tracker  │ │ coach   │
│ (Mon+Thu)  │ │ ler (Fri)│ │ (daily)  │ │(Tue+Fri) │ │ (Sun)    │ │ (Fri)   │
└────────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └─────────┘
```

### Each department has

| Component | Where it lives | Owner |
|-----------|---------------|-------|
| **Mission** | `departments/0N-<name>.md` | Ivan ratified |
| **Lead agent prompt** | `agents/<dept>-lead/PROMPT.md` | Erebus authored, Ivan approved |
| **Cron job** | `hermes cron list` | wired 2026-08-13 |
| **State file** | `agents/state/<dept>.json` | agent writes |
| **Outbox** | `agents/<dept>-lead/outbox/` | agent writes daily/weekly |
| **Decision rights matrix** | `ORG-AGENTS.md` | Ivan approved |
| **Escalation triggers** | `departments/0N-<name>.md` | |

### Department head + lead agent + cadence

| # | Dept | Head | Lead agent | Cron ID | Cadence |
|---|------|------|-----------|---------|---------|
| 1 | Operations | Ivan | management-coordinator | `46c5ae172d63` | Mon+Thu 17:00 PYT |
| 2 | Finance & Legal | Ivan | finance-controller | `40a68cdf432b` | Fri 18:00 PYT |
| 3 | Sales & Growth | Ivan | sales-pipeline | `0e5db79fbca9` | Daily 09:00+12:00 PYT |
| 4 | Engineering & Delivery | Kiki | engineering-roster | `3f0e7fd1898e` | Tue+Fri 17:00 PYT |
| 5 | Research & Education | Ivan | research-tracker | `3b0045bd89e0` | Sun 18:00 PYT |
| 6 | People & Culture | Kiki | kiki-coach | `eeca3ecd40ed` | Fri 17:00 PYT |
| Cross | Business intelligence | Ivan | business-analyst | `8a264667e4ac` | Daily 06:30 PYT |
| Cross | Morning brief | Ivan | morning-brief | `31e08c310e01` | Daily 06:00 PYT |
| Cross | Platform health | Ivan | health.sh | — | Every 5m |

### What each department delivers

**Operations (mgmt-coord)** — 200-400 words, 5 sections: Stuck/at-risk · Stale repos · PR review · Thesis one-liner · Decisions for Ivan.

**Finance & Legal** — 200-400 words, 4 sections: Cash position · Revenue this week · Pending contracts · Compliance flags.

**Sales & Growth** — 150-300 words, 4 sections: New leads · Hot conversations · Stalled deals · Today's outreach queue.

**Engineering & Delivery** — 200-400 words, 5 sections: Deploy health · PR review queue · Kiki's workload · Infra incidents · Tools/decisions for Kiki.

**Research & Education** — 200-400 words, 5 sections: Thesis status · Publications pipeline · Course backlog · Research-to-product · Blockers for Ivan.

**People & Culture** — 400-700 words, 5 sections: Concept · Worked example · Exercise · Stretch · Sources (lesson format).

**Business analyst (cross)** — 150-300 words, 4 sections: Pipeline · Revenue direction · Site & infra health table · Today (max 3 actions).

---

## §3 Hermes Infrastructure

### What you need installed

```
✓ hermes-agent v0.13.0+
✓ state.db SQLite (47MB, 246 sessions)
✓ Toolsets enabled (web, terminal, file, vision, image_gen, bfl, tts, skills, todo, memory, session_search, clarify, delegation, cronjob, computer_use)
✗ video, video_gen (disabled — not needed)
✗ x_search (disabled — not needed)
✗ stt (disabled — not needed)
✗ homeassistant, spotify, yuanbao (disabled — not relevant)
```

### Profiles (TODO: create per-department)

Hermes profiles are **isolated configuration sandboxes**. You want one profile per department so an agent in one dept can't accidentally read another dept's state.

```bash
hermes profile create operations --clone
hermes profile create finance
hermes profile create sales
hermes profile create engineering
hermes profile create research
hermes profile create people
hermes profile create executive  # for board-level (Ivan)
```

**Recommendation**: For a 2-person org, **one profile is fine**. Use `HERMES_KANBAN_BOARD` env var to isolate per-department kanban boards when needed.

### MCP servers (TODO: configure)

MCPs are how agents connect to external tools. **Currently zero MCPs configured**. To wire:

```bash
hermes mcp add stripe --url https://mcp.stripe.com         # Finance
hermes mcp add hubspot --url https://mcp.hubspot.com     # Sales
hermes mcp add github --command "npx @modelcontextprotocol/server-github"  # Engineering
hermes mcp add cf-workers --command "npx @cloudflare/mcp-server-cloudflare"  # Engineering
hermes mcp add postgres --command "npx @modelcontextprotocol/server-postgres"  # Engineering
hermes mcp add notion --command "npx @notion/mcp-server-notion"  # Sales + Research
```

**Minimum useful MCPs for AI Whisperers**:
- `github` (Engineering + Ops): issue/PR/repo CRUD
- `cloudflare` (Engineering): Workers/R2/D1/KV
- `postgres` (Engineering): paragu-ai-platform DB
- `stripe` (Finance): when you add payments
- `linear` (Ops): kanban-style work tracking

### Memory (TODO: configure Qdrant)

Hermes memory uses **Qdrant vector DB** on Host A (`38.9.96.179:6333`). The skill `mem0.md` already documents the setup. Status:

```
✓ mem0 container on Host B (port 8000)
✓ Qdrant on Host A (collection: mem0, 384-dim)
✓ Anthropic key for fact extraction
✗ Memory write_approval: currently false → set to true for sensitive data
✗ memory_char_limit: 2200 (already set)
```

**Recommended config change**:
```yaml
memory:
  memory_enabled: true
  write_approval: true  # so Ivan reviews before facts are stored
  provider: mem0  # use the Qdrant-backed mem0
```

### Security (already configured correctly)

```yaml
security:
  redact_secrets: true
  tirith_enabled: true  # URL safety check
  website_blocklist:
    enabled: false       # ← CHANGE TO TRUE
    domains: []
    shared_files: []
```

**Critical**: enable `website_blocklist.enabled: true` to enforce the trademark banlist. Currently set to `false`. Fix this:

```bash
hermes config set security.website_blocklist.enabled true
```

### Approvals (already configured correctly)

```yaml
approvals:
  mode: manual       # Ivan approves destructive ops
  timeout: 60
  cron_mode: allow   # cron agents can act without per-action approval
```

---

## §4 State + Memory

### 8 state files (the org's memory)

```
/opt/data/agents/state/
├── analyst.json       # business-analyst decisions + open_questions
├── coord.json         # management-coordinator open_stuck + decisions_for_ivan
├── finance.json       # NEW — deals, burn, runway, contracts pending
├── sales.json         # NEW — leads in flight, funnel, outreach queue
├── engineering.json   # NEW — deploy health, error budget, Kiki workload
├── research.json      # NEW — thesis chapter, publications, monetization
├── people.json        # NEW — Kiki lesson streak, contractors, bandwidth
├── kiki.json          # kiki-coach state (existing)
└── kiki-prep.json     # kiki-coach data prep (existing, generated by prep.sh)
```

**Rolling caps** (per department spec):
- analyst: decisions ≤ 8, open_questions ≤ 5
- coord: open_stuck ≤ 10, decisions_for_ivan ≤ 3
- finance: deals_open ≤ 10, compliance_flags ≤ 5
- sales: leads_in_flight (no cap), outreach_queue_today ≤ 5, stalled_deals ≤ 5
- engineering: lists ≤ 10
- research: lists ≤ 8
- people: Kiki streak (no cap)
- kiki-coach: lessons_delivered rolls at 8

### Cross-agent handoff protocol

When agent A needs action from agent B:

1. A writes to its state file
2. A writes a handoff entry to B's state file (if cross-department)
3. B reads its state file on next run
4. B produces output that references the handoff
5. Handoff is logged, owner assigned, deadline set

**Hard rule**: handoff without owner = bug. Flag it.

### Source-of-truth for the org

| Topic | Canonical source |
|-------|------------------|
| Company narrative | `Ai-Whisperers/company/README.md` |
| Services menu (28 items) | `Ai-Whisperers/company/blob/main/Company/services/README.md` |
| Pricing | `Ai-Whisperers/marketing-strategy/02-PRICING.md` |
| ICPs | `Ai-Whisperers/marketing-strategy/marketing-playbook.md` |
| 20-competitor analysis | `Ai-Whisperers/company/blob/main/Company/competitors/README.md` |
| Rubicón EAS deal | `/opt/data/build/rubicon-eas/propuesta/PROPUESTA-COMERCIAL.md` |
| Thesis state | `/opt/data/thesis-active/THESIS_STATE.md` |
| Org constitution | `/opt/data/agents/departments/ORG-AGENTS.md` |
| 1000 discovery questions | `/opt/data/agents/research/1000-company-questions.md` |
| 188 internal questions | `/opt/data/agents/research/188-questions-for-ivan.md` |
| Strategy | `/opt/data/agents/research/STRATEGY.md` |

---

## §5 Skills Stack

### Skills installed (51 total, 20 relevant to management)

| Skill | Used by | Purpose |
|-------|---------|---------|
| **aiw-git-safety** | All agents | Force-push protection, branch hygiene |
| **aiw-ops-discipline** | All cron agents | Tone: terse, no fluff |
| **aiw-management-agents** (NEW) | All setup | Rollout pattern |
| **company-landscape-research** | research-tracker | Research N companies |
| **autonomous-ai-agents** | kiki-coach, engineering-roster | Spawning agents |
| **paraguai-proposal-pricing** | sales-pipeline | Compliance-scrubbed proposals |
| **trademark-compliance-scrub** | sales-pipeline, finance | Hostinger banlist enforcement |
| **b2b-cold-outreach-pitch** | sales-pipeline | Outreach templates |
| **prospect-dossier-pii-sanitization** | sales-pipeline | Sanitize before external |
| **client-site-build-workflow** | engineering-roster | Greenfield sites |
| **client-site-deploy** | engineering-roster | Single-site deploy |
| **client-site-kickoff** | sales-pipeline | 200-question intake |
| **client-vps-provisioning** | engineering-roster | Managed VPS |
| **thesis-active-autonomy** | research-tracker, kiki-coach | Thesis agent protocol |
| **research-integrity-protocol** | research-tracker | Citation rigor |
| **vps-aiw-deploy-pipeline** | engineering-roster | CF Worker + R2 |
| **vps-aiw-client-sites** | engineering-roster | Site audits |
| **vps-knowledge** | engineering-roster | Hostinger/Servarica/CF |

### Skills to consider adding

| Skill | Why |
|-------|-----|
| **mem0** | Already exists as skill, needs provider config |
| **arxiv** | Research-tracker pulls arxiv for thesis chapter 5 |
| **grounded-citations** | Research-tracker citations need grounding |
| **kanban-codex-lane** | When you wire kanban for cross-project tasks |
| **hermes-runtime-ops** | Cron / config / state hygiene |

### Toolsets per department (TODO: configure)

Currently all cron jobs share the default toolset. For tighter security:

```
Department: Operations
  toolsets: [terminal, file, code_execution, session_search, skills, cronjob]
  skills:   [aiw-ops-discipline, aiw-git-safety, vps-knowledge]

Department: Finance & Legal
  toolsets: [terminal, file, code_execution, web, skills]
  skills:   [paraguai-proposal-pricing, trademark-compliance-scrub, prospect-dossier-pii-sanitization]

Department: Sales & Growth
  toolsets: [terminal, file, code_execution, web, skills, delegation]
  skills:   [b2b-cold-outreach-pitch, paraguai-proposal-pricing, trademark-compliance-scrub]

Department: Engineering & Delivery
  toolsets: [terminal, file, code_execution, skills, delegation, web]
  skills:   [vps-aiw-deploy-pipeline, vps-aiw-client-sites, vps-knowledge, aiw-git-safety, aiw-deploy-discipline]

Department: Research & Education
  toolsets: [terminal, file, code_execution, web, skills, session_search]
  skills:   [thesis-active-autonomy, research-integrity-protocol, grounded-citations, company-landscape-research]

Department: People & Culture
  toolsets: [terminal, file, code_execution, skills]
  skills:   [kiki-coach curriculum file]
```

To enforce toolset restrictions per cron job, edit the prompt or use Hermes profile separation.

---

## §6 Schedule

### Cron grid (PYT = UTC-4 winter, UTC-3 summer)

```
     Mon        Tue        Wed        Thu        Fri        Sat        Sun
───── ────────── ────────── ────────── ────────── ────────── ────────── ──────────
06:00 morning    morning    morning    morning    morning    morning    morning
06:30 analyst    analyst    analyst    analyst    analyst    analyst    analyst
09:00 sales      sales      sales      sales      sales      sales      sales
11:00 ci-mon    ─          ─          ci-mon     ─          ─          ─
12:00 rbl-check rbl-check   rbl-check   rbl-check   rbl-check   rbl-check   rbl-check
12:00 sales      sales      sales      sales      sales      sales      sales
17:00 coord      eng        ─          coord      eng+kiki   ─          ─
18:00 ─          ─          ─          ─          finance    ─          research
23:00 ─          ─          ─          ─          ─          ─          thesis-maint
```

Watchdogs (silent unless firing):
- `site-health` — every 15m
- `thesis-watchdog` — every 15m (was erroring, fixed below)
- `evo-poll-watchdog` — every 5m
- `health.sh` — manual (`bash /opt/data/agents/scripts/health.sh`)

### Cron job registry (17 total)

| Job ID | Name | Schedule | Mode | Last status |
|--------|------|----------|------|-------------|
| `76bf40a127c4` | site-health | every 15m | script | ✓ ok |
| `c5b50e0eab17` | repo-ci-monitor | `0 11 * * *` | script | ✓ ok |
| `13291663f55b` | rbl-check | `0 12 * * *` | script | ✓ ok |
| `31e08c310e01` | morning-brief | `0 10 * * *` | agent | ✓ just fixed |
| `c314dab9382c` | ometzdental-weekly-refresh | `0 6 * * 1` | script | ✓ ok |
| `135a7c018ccb` | thesis-daily-tick | `0 6 * * *` | script+skill | ⚠️ needs fix |
| `79a6d5141085` | thesis-weekly-review | `0 18 * * 0` | agent+skill | ⚠️ needs fix |
| `d26e7a70ca07` | thesis-git-maintenance | `0 23 * * 0` | script+skill | ⚠️ needs fix |
| `1b1d22e181b6` | thesis-watchdog | every 15m | agent+skill | ⚠️ needs fix |
| `7d741fffe312` | evo-poll-watchdog | every 5m | script | ✓ ok |
| `8a264667e4ac` | aiw-business-analyst-daily | `30 10 * * *` | agent+skill | — not yet run |
| `46c5ae172d63` | aiw-management-coord-biwk | `0 21 * * 1,4` | agent+skill | — not yet run |
| `eeca3ecd40ed` | aiw-kiki-coach-weekly | `0 21 * * 5` | agent+skill | — not yet run |
| `0e5db79fbca9` | aiw-sales-pipeline-daily | `0 13,16 * * *` | agent+skill | — not yet run |
| `40a68cdf432b` | aiw-finance-controller-weekly | `0 21 * * 5` | agent+skill | — not yet run |
| `3f0e7fd1898e` | aiw-engineering-roster-biwk | `0 20 * * 2,5` | agent+skill | — not yet run |
| `3b0045bd89e0` | aiw-research-tracker-weekly | `0 21 * * 0` | agent+skill | — not yet run |

**17 jobs total. 4 need model pinning fix** (see §7).

---

## §7 Status + Next Steps

### Status (2026-08-13)

| Component | Status |
|-----------|--------|
| Org structure (6 departments) | ✓ DONE |
| Department specs (6 files) | ✓ DONE |
| Constitution (ORG-AGENTS.md) | ✓ DONE |
| Lead agent PROMPTs (7) | ✓ DONE |
| Cron jobs created (7 new) | ✓ DONE |
| State files (8 schemas) | ✓ DONE |
| Scripts (org-pulse, health, kiki-prep, grid) | ✓ DONE |
| Cross-department handoff protocol | ✓ DONE |
| Outbox examples (seeded) | ✓ DONE |
| Decision rights matrix | ✓ DONE |
| `morning-brief` cron (fixed model drift) | ✓ JUST FIXED |
| 4 thesis cron jobs (model drift) | ⚠️ NEEDS FIX |
| MCP servers | ✗ NOT CONFIGURED |
| Per-profile Hermes configs | ✗ NOT CONFIGURED |
| Website blocklist (trademark) | ✗ DISABLED — must enable |
| `hermes project` workspaces | ⚠️ PARTIAL (3 exist) |
| Internal-questionnaire answers (188) | ✗ PENDING — Ivan |
| Rubicón EAS contract | ✗ PENDING — Ivan |
| CF Worker webhook (`WEBHOOK_URL`) | ✗ PENDING — Kiki |
| Real revenue / cost data in state files | ✗ PENDING — Ivan |

### Immediate fix list (4 cron jobs in error)

The 4 thesis cron jobs failed because the global model/provider config drifted. Fix:

```bash
cronjob action=update job_id=135a7c018ccb provider=litellm model=primary
cronjob action=update job_id=79a6d5141085 provider=litellm model=primary
cronjob action=update job_id=d26e7a70ca07 provider=litellm model=primary
cronjob action=update job_id=1b1d22e181b6 provider=litellm model=primary
```

(Just fixed `morning-brief` with `31e08c310e01`. The other 4 need same fix.)

### 5 actions to take this week

| # | Action | Owner | Time |
|---|--------|-------|------|
| 1 | Pin the 4 thesis cron jobs to current model | Ivan (or Erebus) | 5 min |
| 2 | Enable website blocklist (`security.website_blocklist.enabled: true`) | Ivan | 1 min |
| 3 | Sign Rubicón EAS contract | Ivan | 30 min |
| 4 | Wire Rubicón EAS Worker webhook (`wrangler secret put WEBHOOK_URL`) | Kiki | 15 min |
| 5 | Fill the 188 internal questions | Ivan + Kiki | 90 min |

### 5 actions to take this month

| # | Action | Owner | Time |
|---|--------|-------|------|
| 6 | Create the 6 `hermes project` workspaces | Ivan | 30 min |
| 7 | Add 3-5 MCP servers (github, cf-workers, postgres, notion, linear) | Ivan | 1 hour |
| 8 | Build per-profile toolsets in config.yaml | Ivan | 1 hour |
| 9 | Populate `/opt/data/source-materials/` with real per-topic content | Ivan | 2-3 hours |
| 10 | Write 3 case studies (ometzdental, montanaro-py, rubicon-eas) | Ivan + Kiki | 4 hours |

### 5 actions to take this quarter

| # | Action | Owner | Time |
|---|--------|-------|------|
| 11 | NL pilot outreach (10 Dutch companies) | Ivan | 1 week |
| 12 | EU AI Act consulting offer published | Ivan | 1 week |
| 13 | paraguay-supermercados API monetization | Ivan | 2 weeks |
| 14 | Build the trilingual 6-month wedge strategy (deeper than STRATEGY.md) | Ivan + Erebus | 1 session |
| 15 | Quarterly board deck auto-generated from state files | Ivan | 1 day |

---

## Quick-reference: the 5 files you read most often

1. **`/opt/data/agents/ORCHESTRATION.md`** — day-to-day reference for what's running
2. **`/opt/data/agents/departments/ORG-AGENTS.md`** — decision rights + handoff matrix
3. **`/opt/data/agents/research/STRATEGY.md`** — 90-day plan + LATAM market
4. **`/opt/data/agents/research/188-questions-for-ivan.md`** — your homework
5. **`/opt/data/agents/research/PROMPT-ANALYSIS.md`** — what you've been asking + what's done

## Quick-reference: the 5 commands you run most often

```bash
# What's running?
hermes cron list

# Are all agents healthy?
bash /opt/data/agents/scripts/health.sh

# What's the schedule grid?
bash /opt/data/agents/scripts/grid.sh

# Fix a cron job (model drift):
cronjob action=update job_id=<ID> provider=litellm model=primary

# Pause/resume an agent:
hermes cron pause <job_id>
hermes cron resume <job_id>
```

---

Last updated: 2026-08-13 by Erebus. 17 cron jobs, 6 departments, 8 state files, 7 agent specs. ~60% built; ~40% pending your input.

Want me to:
1. **Fix the 4 thesis cron jobs right now** (5 min, the `cronjob update` calls)?
2. **Enable the website blocklist** (1 min)?
3. **Build the 6 `hermes project` workspaces** (30 min)?
4. **Generate the 90-day calendar with the cron grid mapped to real dates**?

Say which and I'll do it.