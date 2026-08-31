# AI Whisperers — Master Upgrade Changelog (2026-08-13 → 2026-08-23)

> **Canonical, single-source rollup of every upgrade, install, setup, configuration, and refactor we've executed on the AIW operational layer.**
>
> **Repo:** [github.com/Ai-Whisperers/agents-v2](https://github.com/Ai-Whisperers/agents-v2) (this file) + `/opt/data/agents/` companion repo (legacy Tier 1-4 reports)
> **Date range:** 2026-08-13 (Tier 1 baseline) → 2026-08-23 (current state, 3 cron ticks ago)
> **Author:** Erebus (autonomous Hermetic ops), consolidated by Erebus on 2026-08-23
> **Status:** Living document. Updated whenever a wave of upgrades completes.

---

## TL;DR — what changed in 10 days

| Surface | 2026-08-13 baseline | 2026-08-23 current | Delta |
|---------|---------------------|---------------------|-------|
| **Cron jobs** | 17 | **83** | +66 (+388%) |
| **Agent PROMPT.md files** | 3 | **49** | +46 |
| **Profiles** | 7 | **9** (added `ivan`, `kiki`) | +2 |
| **MCP servers (enabled)** | 14 | **25 enabled / 41 registered** | +11 enabled |
| **Total skills** | 56 (relevant subset) | **298** | +232 |
| **Dashboards** | 1 (org.html) | **7** (org + 6 dept pages) | +6 |
| **Phase reports** | 0 | **24** (PHASE-0 through PHASE-24) | +24 |
| **Eval-gate pass rate** | n/a | **86.6%** (17/17 PASS 2026-08-17) | new |
| **12-factor agent audit avg** | n/a | **9.0/10** | new |
| **Active cron scripts** | 0 | **22** (`/opt/data/agents/scripts/` + `/opt/data/agents-v2/scripts/`) | +22 |
| **State files** | 9 dept | **18 dept + sqlite migrating** | +9 |
| **Webhook receivers** | 0 | **1** (port 8081, Factor 11) | +1 |
| **LLM cost / month** | unmonitored | **~$293/mo** (cost-monitor) | new |

---

## Wave 1 — Tier 1 critical fixes (2026-08-13, documented in `agents/UPGRADE-REPORT.md`)

5 fixes, all done. Status carried forward.

| # | Fix | Result |
|---|-----|--------|
| 1 | Enable `security.website_blocklist` (trademark banlist) | ✓ on |
| 2 | Fix `morning-brief` cron model drift | ✓ re-pinned to `litellm/primary` |
| 3 | Fix 4 thesis cron jobs (same drift) | ✓ re-pinned |
| 4 | Memory config: `provider=mem0`, `write_approval=true` | ✓ written |
| 5 | Verify `security.redact_secrets`, `memory_enabled`, `approvals.cron_mode` | ✓ all on |

## Wave 2 — Tier 2 infrastructure (2026-08-13)

- 6 per-department profiles: `operations`, `finance`, `sales`, `engineering`, `research`, `people`
- 8 per-project workspaces (now 11 total — added `home`, `thesos`, `rubicon-eas`)
- 14 folders bound across 11 projects
- 8 kanban boards bound
- 12 starter kanban tasks seeded

## Wave 3 — MCP server integration (2026-08-13, `MCP-UPGRADE-REPORT.md`)

Started: 0 MCP servers. Finished that day: **14 enabled**. Now (2026-08-23): **25 enabled / 41 registered**.

Key additions since 2026-08-13:
- `social-graph-mcp` (Plataforma de Redes Graph API) — added for social listening
- `mcp_jupyter`, `mcp_numpy`, `mcp_pandoc`, `mcp_pdf` — research workflow
- `mcp_server_git`, `mcp_server_time`, `mcp_server_obsidian`, `mcp_server_qdrant` — knowledge
- `mcp_server_spotify`, `mcp_server_trello`, `mcp_server_anki` — personal/learning
- `mcp__mindstone_mcp_server_hubspot` — CRM (enabled)
- `twilio_mcp` — SMS gateway (enabled)
- 16 registered but **disabled** (notion, jira, sentry, redis, sendgrid, canal de comunicacion, asana, todoist, shopify, resend, pasarela de pagos, redis-mcp, easy-mcps, appwrite, apify, alife) — deferred until specific use case

## Wave 4 — Tier 3 / Tier 4 dashboards (2026-08-13, `TIER3-UPGRADE-REPORT.md`, `TIER4-UPGRADE-REPORT.md`)

- Per-profile `disabled_toolsets` blocks (6 dept profiles, 5-16 toolsets each)
- 22 source-material files in `/opt/data/source-materials/`
- 6 per-dept dashboards + 1 org dashboard
- HTTP server (`dashboard-server.py`) port 8765 — live state API
- Filter/sort/search UI on all tables
- 7-day history tracking with SVG sparkline
- Daily snapshot cron

## Wave 5 — Org buildout v0.2.0 + v0.3.0 (2026-08-14 to 2026-08-15, `agents-v2/PHASE-0` through `PHASE-5`)

- Initial 6 dept specs + `ORG-AGENTS.md` constitution
- 7 lead agents built (business-analyst, management-coordinator, kiki-coach, sales-pipeline, finance-controller, engineering-roster, research-tracker)
- Per-agent git repos planned (now consolidated to monorepo)
- SQLite schema for 11 DBs
- Hard-stops YAML schema pattern
- Idempotency contract pattern
- Trademark-scrub mechanical script
- 3-layer storage architecture (git + SQLite + Qdrant)
- 15 failure modes documented
- 5 actors / 7 threats threat model
- Per-phase rollback playbook

## Wave 6 — Infrastructure scripts + cron wiring (2026-08-14, `agents-v2/PHASE-2`)

- `state-snapshot.sh` — atomic state snapshots (6h cron)
- `validate-state.py` — schema validator (15m cron)
- `cron-heartbeat.sh` — rate-limited heartbeat (onhours/offhours)
- `db-snapshot.py` — daily DB snapshot
- First snapshots: `state/snapshots/2026-08-14T20-25-52Z/`

## Wave 7 — v0.3.0 expansion (2026-08-15, `PHASE-5.5`, `PHASE-6`, `PHASE-7`, `PHASE-8`)

22 new agents added in v0.3.0 push:
- `accounting-automation`, `bizops-tracker`, `chaos-test-runner`, `compliance-monitor`, `course-producer`, `citation-checker`, `devops-monitor`, `eval-gate-runner`, `founder-bandwidth-watchdog`, `lead-enrichment`, `marketing-content-producer`, `multimedia-producer`, `okr-tracker`, `procurement-tracker`, `proposal-drafter`, `qa-automation-runner`, `revops-pipeline-analyzer`, `security-watchdog`, `tax-receipt-tracker`, `thesis-tracker`

Plus deferred-roles.md and deferred-agents.md to manage what NOT to build.

## Wave 8 — Self-running + eval-gate (2026-08-15, `PHASE-13`, `PHASE-16`)

- `self-running-check.py` — verifies cron + state + audit + costs every 30min
- `eval-gate.py` — 9-check scorer (eval-per-agent)
- Eval-gate POC for business-analyst: 7/9 PASS on live brief
- Eval-gate cron integrated into 30+ agents
- Reasoning model swap (some agents to higher-tier model)

## Wave 9 — Coaching company buildout (2026-08-15 to 2026-08-17, `PHASE-14`, `PHASE-15`)

- 7 internal coaching agents (coach-ivan, coach-kiki, coach-org, coach-lead-agents, coaching-content-curator, coaching-quality-reviewer, coaching-research-intelligence)
- 7 external coaching agents (coach-practitioner, coach-cohort-facilitator, coach-onboarding, coach-renewal-manager, coach-roi-tracker, coach-lead-finder, coach-conversion-agent)
- 15 coaching skills (GROW + CLEAR + Sunstein + ICF + behavior change)
- Trilingual support (English / Spanish / Dutch)
- 5 verticals (Legal, Dental, RE, Beauty/Wellness, SMB Founder)
- 17/17 PASS eval-gate on 2026-08-17

## Wave 10 — 12-factor closure + observability (2026-08-19 to 2026-08-21, `PHASE-17` through `PHASE-22`)

### Phase 17 (research)
- Analyzed 15+ open-source AI agent repos
- 7 strategic insights synthesized

### Phase 18 (Factor 7 — WhatsApp human-in-loop)
- `whatsapp-send.py` — outbound messaging (Evolution API)
- `whatsapp-human-in-loop` skill
- 14 coaching agents have escalation triggers
- ⚠️ **Trademark incident (2026-Q1):** Original `mensajeconnect.paragu-ai.com` flagged by Hostinger as phishing impersonation. Renamed to **`messaging` / `whatsapp`** at v0.20 (commit `6c9a0208d`). Trademark banlist now mechanically enforced across all surfaces.

### Phase 19 (Factor 11 — Webhook triggers)
- `webhook-receiver.py` on port 8081
- `coach-onboarding-poller.py` (every 5 min)
- Cron job for auto-onboarding (legacy vendor-compatible payload schema supported)

### Phase 20 (Factor 5 — Unified execution state)
- `org-state.json` — single source of truth (47 agents tracked)
- `build-org-state.py` — hourly rebuild
- 47 agent PROMPT.md updated with Factor 5 section

### Phase 21 (Remaining 12-factor gaps)
- Factor 3: `build-agent-context.py`
- Factor 9: `compact-errors.py` (errors.json with compact form)
- Factor 12: 14 agents marked stateless (reducer pattern)
- Cost monitoring: `cost-monitor.py` (~$293/mo estimated)
- Agent tracing: latency + tokens per agent
- Eval trending: 30-day pass rate
- Org dashboard: 8 FounderOS-style routes
- Skill deprecation: 90-day workflow
- WhatsApp templates: 6 files

### Phase 22 (Loop complete)
- `self-running-check-v2.py` (uses org-state)
- State auto-commit to git
- Eval per-agent (from criteria)
- Eval auto-trigger on new briefs
- Eval report (markdown)
- Cost alerts (WhatsApp at $1000/mo)
- Audit fix script (HIGH items → 0)
- Intake form (HTML → webhook)

### Phase 24 (Plan review + 2 gap-fillers)
- `people-hr-weekly` (Monday 22:00 UTC)
- `board-of-directors-quarterly` (1st of Jan/Apr/Jul/Oct)

## Wave 11 — Thesis + funding integration (2026-08-22 to 2026-08-23)

- `thesis-tracker-daily` — links thesis to org funding
- `funding-coordinator` + `funding-weekly-sweep` + `funding-daily-check`
- `aiw-thesis-tracker-daily` cron
- 30min watchdogs: `devops-monitor-30min`, `security-watchdog-30min`, `ai-safety-engineer-30min`, `coaching-quality-reviewer`, `founder-bandwidth-watchdog-weekly`
- `mcp-health-check` cron
- Drift detector weekly
- Security audit biweekly

## Wave 12 — Operational hardening (ongoing, latest in `/opt/data/state/org-state.json`)

Recent discoveries and fixes (from cron briefs 2026-08-23):
- **`/opt/data/agents/` has NO git remote** — committed locally only; needs `git remote add origin https://github.com/Ai-Whisperers/agents.git` once org decides on repo name
- **9 missing scripts** in jobs.json — they exist at `/opt/data/agents-v2/scripts/` and `/opt/data/home/.hermes/scripts/` but jobs.json references `/opt/data/scripts/` → path-guard fix needed
- **HTTP 402 cluster** — 14 cron jobs blocked by Cerebras (11) + Mistral (3) billing; `$20 OpenRouter topup` unblocks
- **rubicon-eas SSL flap** — Worker route missing despite deploy
- **Cron drift +30m23s** (39h45m10s total) — heartbeat watchdog catches it
- **Founder bandwidth pressure** — Ivan timezone PYT = UTC-4

---

## File map (what lives where, after all waves)

```
/opt/data/agents/                                     # legacy Tier 1-4 reports repo (NO remote)
├── UPGRADE-REPORT.md             Tier 1 baseline (2026-08-13)
├── TIER3-UPGRADE-REPORT.md       Tier 3 internal (2026-08-13)
├── TIER4-UPGRADE-REPORT.md       Tier 4 followup (2026-08-13)
├── MCP-UPGRADE-REPORT.md         MCP inventory (2026-08-13)
├── HERMES-UPSTREAM-ISSUES.md     Hermes upstream bugs (2026-08-13)
├── HERMES-UPGRADE-CHANGELOG.md   ↗ pointer to MASTER-UPGRADE-CHANGELOG
├── SETUP-GUIDE.md               master reference
├── ORCHESTRATION.md              what's running day-to-day
├── ORG-AGENTS.md                constitution
├── DECISIONS-2026-Q3.md          16 ratified decisions
├── GAP-AUDIT-2026-08-13.md       initial gap audit
├── DEFERRED-AGENTS.md            what not to build
├── DEFERRED-ROLES.md             roles we're not hiring
├── REVIEW-2026-Q4.md            Q4 review
├── ON-CALL.md                   who's on call
├── DASHBOARD-AUTH.md            dashboard auth spec
├── rename-map.json              session rename map (post-2026-08-21)
├── sessions-to-rename.json
├── [49 agent dirs]              each with PROMPT.md + outbox/
├── dashboards/                  7 dashboards
├── departments/                 6 dept specs + ORG-AGENTS
├── research/                    research artifacts
├── schemas/                     9 dept JSON schemas
├── scripts/                     7 infra scripts
├── state/                       18 dept + snapshots/ + history/
└── .git/                        local only (no remote)

/opt/data/agents-v2/                                   # canonical org-buildout repo (HAS remote)
├── README.md                    v0.2.0 entry point
├── MASTER-UPGRADE-CHANGELOG.md  ↗ THIS FILE (canonical cumulative view)
├── INDEX.md                     master artifact navigation
├── PLAN-v5.md                   master plan, 11 phases
├── DECISIONS-2026-Q3.md         mirror of /opt/data/agents/
├── ROLES-INVENTORY.md           ~135 roles, 30 functional areas
├── STORAGE-ARCHITECTURE.md      3-layer model
├── FAILURE-MODES.md             15 modes + 3 chaos tests
├── THREAT-MODEL.md              5 actors, 7 threats
├── ROLLBACK-PLAYBOOK.md         per-phase rollback
├── BURNOUT-SIGNAL-SPEC.md       founder bandwidth spec
├── SELF-RUNNING-CRITERIA.md     verification definition
├── PHASE-0-COMPLETE.md          …through PHASE-24 (24 phase reports)
├── constitution/                canonical charter + dept specs + archive
├── patterns/                    hard-stops, idempotency, sqlite-schema, trademark-scrub
├── prompts/                     master 12-section PROMPT template
├── agents/                      46 agent dirs (mirrored to /opt/data/agents/)
├── agents-prompts/              canonical PROMPT.md sources
├── playbooks/                   per-dept ops playbooks
├── research/                    research artifacts
├── scripts/                     22 operational scripts
│   ├── eval/                    eval-gate, per-agent, trending, report
│   ├── cost/                    cost-monitor, cost-alerts, cost-cap
│   ├── state/                   build-org-state, snapshot, migrate-to-sqlite
│   ├── observability/           agent-tracer, context-builder
│   ├── webhook/                 webhook-receiver, coach-onboarding-poller
│   ├── whatsapp/                whatsapp-send, templates
│   ├── errors/                  compact-errors
│   ├── dashboard/               org-dashboard, dept-dashboards
│   ├── context/                 build-agent-context
│   ├── deprecation/             skill deprecation workflow
│   ├── backup-drill.sh
│   ├── eval-gate-runner.sh
│   ├── self-running-check.py    + v2
│   ├── migrate_state_to_sqlite.py
│   └── db-snapshot.py
├── state/                       runtime state (mirrored to /opt/data/state/)
├── eval/                        eval artifacts
├── templates/                   HTML templates (intake, email, dashboard)
├── tests/                       44 unit tests
├── dashboard/                   Python dashboard renderer
├── .github/                     CI workflows
└── .git/                        local + remote (origin: github.com/Ai-Whisperers/agents-v2)

/opt/data/hermes-agent/                              # NousResearch upstream (HAS remote, diverged)
└── (git pull needed; main is 1 ahead of origin, 3634 behind)

/opt/data/state/                                      # runtime state (sqlite migrating)
├── org-state.json               Factor 5 single source of truth
├── eval-per-agent.json          per-agent PASS/FAIL rolling
├── eval-trending.json           30-day pass rate
├── cost-tracker.json            per-agent LLM spend
├── agent-stats.json
├── agent-traces.jsonl           per-call latency/tokens
├── auto-eval-log.jsonl
├── coaching-customers.json
├── conversion-attempts.json
├── customers.json
├── errors.json                  compact errors
├── escalations/
├── gateway.heartbeat
├── gateway.lifecycle.json
├── org-state-history/           hourly snapshots
├── prompt-improvements.md       auto-detected prompt gaps
├── webhook-log.json
└── chaos.last_run

/opt/data/profiles/                                   # 9 hermes profiles
├── default/         (running)
├── engineering/     (stopped, 5 disabled toolsets)
├── finance/         (stopped, 15 disabled)
├── ivan/            (stopped, NEW — personal Ivan profile)
├── kiki/            (stopped, NEW — personal Kiki profile, nvidia-llama-8b)
├── operations/      (stopped, 16 disabled)
├── people/          (stopped, 14 disabled)
├── research/        (stopped, 6 disabled)
└── sales/           (stopped, 9 disabled)

/opt/data/profiles/<name>/config.yaml                 # agent.disabled_toolsets per dept
```

---

## Verification — quick commands

```bash
# Cron health (should show 83 jobs, 6+ ok)
hermes cron list

# Agent count (should show 49 PROMPT.md)
find /opt/data/agents -maxdepth 2 -name "PROMPT.md" | wc -l

# MCP inventory (should show ~41 registered, 25 enabled)
hermes mcp list

# Profile inventory (should show 9)
hermes profile list

# 12-factor audit (should show 9.0/10 avg)
python3 /opt/data/agents-v2/eval/eval-gate.py --audit

# Eval trending (should show 86.6% from 2026-08-17)
cat /opt/data/state/eval-trending.json | python3 -m json.tool | head -20

# Cost tracker (should show ~$293/mo)
cat /opt/data/state/cost-tracker.json | python3 -m json.tool | head -10

# Org state (single source of truth, Factor 5)
cat /opt/data/state/org-state.json | python3 -m json.tool | head -30

# Self-running check
python3 /opt/data/agents-v2/scripts/self-running-check-v2.py
```

---

## What still needs to happen (carry-forward)

1. **Wire `/opt/data/agents/` to a remote** — decide between `Ai-Whisperers/agents` (public) or `Ai-Whisperers/agents-internal` (private)
2. **Fix jobs.json paths** — 9 cron jobs reference `/opt/data/scripts/` but scripts live at `/opt/data/agents-v2/scripts/` and `/opt/data/home/.hermes/scripts/`
3. **HTTP 402 cluster** — top up `$20 OpenRouter` to unblock 14 Cerebras/Mistral cron jobs
4. **rubicon-eas Worker route** — SSL flap indicates Worker route missing on `rubiconeas.paragu-ai.com`
5. **Org-context cron drift** — 39h45m10s; heartbeat watchdog catches but doesn't auto-correct
6. **First real customer** — coaching product has 0 buyers; needs Iván's first WhatsApp outreach
7. **Trademark banlist enforcement** — Hermes v0.20 already renamed `whatsapp` → `messaging` locally; verify public-facing surfaces are clean

---

## How to read this document

| You want to… | Read this section |
|---------------|-------------------|
| Understand the current state in 30s | TL;DR table |
| Trace a single upgrade wave | Wave 1-12 sections |
| Find which repo owns what | File map |
| Run a health check | Verification commands |
| See what's still left | Carry-forward section |
| Update this document | Edit `MASTER-UPGRADE-CHANGELOG.md` in `agents-v2`, commit + push |
| Find the source for a specific number | Wave 1 = `agents/UPGRADE-REPORT.md` etc. — each wave links to its source |

---

## History of this document

- **2026-08-23** — v1.0 created by Erebus on Iván's request "analyze all the upgrades we have on hermes and all things we setuped all the updates we did all the things we upgraded on all sessions and make sure our repo that describes this is updated we should a few analyze all of them and update them and document and pass em the links". Consolidates 4 stale `agents/UPGRADE-REPORT*.md` files + 24 `agents-v2/PHASE-*.md` files + 7 cron-discovered gaps into one canonical view.

---

**Document path:** `/opt/data/agents-v2/MASTER-UPGRADE-CHANGELOG.md`
**GitHub mirror:** https://github.com/Ai-Whisperers/agents-v2/blob/master/MASTER-UPGRADE-CHANGELOG.md
**Last updated:** 2026-08-23 by Erebus
