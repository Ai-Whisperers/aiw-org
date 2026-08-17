# Management + Agent Setup — Upgrade Report (2026-08-13)

> Pure-internal upgrade pass. No client work. State after executing the 5-week action plan.
> This is the **operating state** of AI Whisperers' management layer as of now.

---

## What changed in this session

### ✓ Tier 1 — Critical fixes (DONE)

| # | Action | Result |
|---|--------|--------|
| 1 | **Enable website blocklist** (trademark banlist enforcement) | ✓ `security.website_blocklist.enabled = true` |
| 2 | **Fix `morning-brief` cron** (model drift) | ✓ re-pinned to `litellm/primary` |
| 3 | **Fix 4 thesis cron jobs** (same drift: `thesis-daily-tick`, `thesis-weekly-review`, `thesis-git-maintenance`, `thesis-watchdog`) | ✓ re-pinned via `hermes cron edit --model primary --provider litellm` |
| 4 | **Memory config** — set provider to `mem0` (Qdrant-backed), write_approval to `true` | ✓ both written |
| 5 | **Verify security.redact_secrets, memory_enabled, approvals.cron_mode** | ✓ all on |

### ✓ Tier 2 — Infrastructure (DONE)

| # | Action | Result |
|---|--------|--------|
| 6 | **Create 6 per-department profiles** | ✓ `operations`, `finance`, `sales`, `engineering`, `research`, `people` (all under `/opt/data/profiles/`) |
| 7 | **Create 8 per-project workspaces** | ✓ `aiw-org`, `aiw-clients`, `aiw-engineering`, `thesis-active`, `aiw-research`, `aiw-people`, `aiw-finance`, `aiw-sales` |
| 8 | **Attach folders to projects** | ✓ 14 folders bound across 11 projects |
| 9 | **Bind projects to kanban boards** | ✓ all 8 aiw-* projects bound |
| 10 | **Seed 12 starter kanban tasks** | ✓ cross-session task tracking active |

---

## Current operational state

### Config (`/opt/data/config.yaml`)

| Setting | Value | Notes |
|---------|-------|-------|
| `security.website_blocklist.enabled` | **true** | Trademark banlist now enforced |
| `security.redact_secrets` | true | Long-standing |
| `security.tirith_enabled` | true | URL safety check |
| `memory.memory_enabled` | true | |
| `memory.write_approval` | **true** | NEW — Ivan reviews before facts stored |
| `memory.provider` | **mem0** | NEW — Qdrant-backed vector memory |
| `memory.memory_char_limit` | 2200 | |
| `approvals.mode` | manual | Destructive ops require Ivan |
| `approvals.cron_mode` | allow | Cron agents run unsupervised |
| `approvals.mcp_reload_confirm` | true | |
| `agent.max_turns` | 90 | |
| `compression.threshold` | 0.5 | Auto-compact at 50% |
| `kanban.dispatch_in_gateway` | true | Auto-claim via gateway |
| `kanban.auto_decompose` | true | |

### Cron jobs (17 total)

| Job ID | Name | Schedule | Last status |
|--------|------|----------|-------------|
| `76bf40a127c4` | site-health | every 15m | ✓ ok |
| `c5b50e0eab17` | repo-ci-monitor | `0 11 * * *` | ✓ ok |
| `13291663f55b` | rbl-check | `0 12 * * *` | ✓ ok |
| `31e08c310e01` | morning-brief | `0 10 * * *` | (was error, just fixed) |
| `c314dab9382c` | ometzdental-weekly-refresh | `0 6 * * 1` | ✓ ok |
| `135a7c018ccb` | thesis-daily-tick | `0 6 * * *` | (was error, just fixed) |
| `79a6d5141085` | thesis-weekly-review | `0 18 * * 0` | — pending first run |
| `d26e7a70ca07` | thesis-git-maintenance | `0 23 * * 0` | — pending first run |
| `1b1d22e181b6` | thesis-watchdog | every 15m | (was error, just fixed) |
| `7d741fffe312` | evo-poll-watchdog | every 5m | ✓ ok |
| `8a264667e4ac` | aiw-business-analyst-daily | `30 10 * * *` | — pending first run |
| `46c5ae172d63` | aiw-management-coord-biwk | `0 21 * * 1,4` | — pending first run |
| `eeca3ecd40ed` | aiw-kiki-coach-weekly | `0 21 * * 5` | — pending first run |
| `0e5db79fbca9` | aiw-sales-pipeline-daily | `0 13,16 * * *` | — pending first run |
| `40a68cdf432b` | aiw-finance-controller-weekly | `0 21 * * 5` | — pending first run |
| `3f0e7fd1898e` | aiw-engineering-roster-biwk | `0 20 * * 2,5` | — pending first run |
| `3b0045bd89e0` | aiw-research-tracker-weekly | `0 21 * * 0` | — pending first run |

**Snapshot**: 5 ✓ ok · 4 ✗ just fixed (waiting next tick) · 8 — pending first run

### Profiles (7)

| Profile | Status | Use |
|---------|--------|-----|
| `default` | running | Catch-all |
| `engineering` | stopped | Engineering + delivery dept agent runs |
| `finance` | stopped | Finance dept agent runs |
| `operations` | stopped | Ops dept agent runs |
| `people` | stopped | Kiki-coach + people dept |
| `research` | stopped | Research dept + thesis agents |
| `sales` | stopped | Sales dept + outreach |

Profiles are cloned from default but use the **same config** for now. To specialize (different toolset per profile), edit `/opt/data/profiles/<name>/config.yaml`.

### Projects (11 total, 14 folders)

| Project | Folders |
|---------|---------|
| `home` | 1 (default) |
| `thesos` | 1 (existing) |
| `rubicon-eas` | 1 (existing) |
| `aiw-org` | `/opt/data/agents`, `/opt/data/source-materials` |
| `aiw-clients` | `/opt/data/build`, `/opt/data/build/monorepo-sparse` |
| `aiw-engineering` | `/opt/data/scripts` |
| `thesis-active` | `/opt/data/thesis-active` |
| `aiw-research` | `/opt/data/agents/research` |
| `aiw-people` | `/opt/data/agents/kiki-coach` |
| `aiw-finance` | `/opt/data/agents/finance-controller` |
| `aiw-sales` | `/opt/data/agents/sales-pipeline`, `/opt/data/richar-ruiz-outreach` |

Use: `hermes project use <name>` to make a project the active context.

### Kanban (12 tasks seeded)

All ready, on default board. Open with `hermes kanban list --board default` or web UI.

| Task | Project | Assignee | Body |
|------|---------|----------|------|
| Sign Rubicón EAS contract | aiw-org | ivan | Send propuesta to client |
| Fill 188 internal questions | aiw-org | ivan | 90-min session with Kiki |
| Wire CF Worker webhook for rubicon-eas-lead | aiw-org | kiki | wrangler secret put WEBHOOK_URL |
| Commit /opt/data/agents/ to GitHub | aiw-org | ivan | Pick target repo |
| Fix thesis-daily-tick error state | aiw-engineering | ivan | Pin model to primary |
| Add MCP server: github | aiw-engineering | ivan | hermes mcp add github |
| Add MCP server: cloudflare | aiw-engineering | ivan | hermes mcp add cf-workers |
| Populate finance.json state with real numbers | aiw-finance | ivan | First week of operation |
| Send Richar Ruiz first contact | aiw-sales | ivan | Use b2b-cold-outreach-pitch skill |
| Pick first 3 kiki-coach topics | aiw-people | kiki | From curriculum.md |
| Update THESIS_STATE.md | thesis-active | ivan | Per research-tracker weekly |
| Populate source-materials/ with real content | aiw-research | ivan | 2-3 hours of focused work |

### State files (org memory)

`/opt/data/agents/state/` — 9 files, 1996 bytes total.

| File | Bytes | Purpose |
|------|-------|---------|
| analyst.json | 156 | business-analyst decisions |
| coord.json | 91 | mgmt-coord open_stuck |
| engineering.json | 198 | engineering-roster state |
| finance.json | 221 | finance-controller state |
| kiki-prep.json | 238 | kiki-coach data prep |
| kiki.json | 223 | kiki-coach state |
| people.json | 363 | people-culture state |
| research.json | 269 | research-tracker state |
| sales.json | 237 | sales-pipeline state |

### Agent specs (3 PROMPT.md files)

- `/opt/data/agents/business-analyst/PROMPT.md`
- `/opt/data/agents/management-coordinator/PROMPT.md`
- `/opt/data/agents/kiki-coach/PROMPT.md`

Plus 4 more agent prompts embedded in cron jobs (sales-pipeline, finance-controller, engineering-roster, research-tracker) — but their standalone PROMPT.md files haven't been written yet. If you want them as files, say so and I'll extract them.

### Department specs (6 files in `/opt/data/agents/departments/`)

- `01-operations.md`
- `02-finance-legal.md`
- `03-sales-growth.md`
- `04-engineering-delivery.md`
- `05-research-education.md`
- `06-people-culture.md`
- `ORG-AGENTS.md` (constitution)

### Skills (56 total, 23 relevant to management)

The relevant ones for management/agent work:

`aiw-git-safety`, `aiw-ops-discipline`, `aiw-management-agents`, `autonomous-ai-agents`, `hermes-desktop-plugins`, `mcp`, `thesis-active-autonomy`, `trademark-compliance-scrub`, `research-integrity-protocol`, `company-landscape-research`, `paraguai-proposal-pricing`, `b2b-cold-outreach-pitch`, `prospect-dossier-pii-sanitization`, `client-site-build-workflow`, `client-site-deploy`, `client-site-kickoff`, `client-vps-provisioning`, `vps-aiw-deploy-pipeline`, `vps-aiw-static-deploy`, `vps-aiw-client-sites`, `vps-knowledge`, `github`, `github-clone-pitfalls`

### MCP servers

**None configured.** To add:

```bash
hermes mcp add github --command "npx @modelcontextprotocol/server-github"
hermes mcp add cf-workers --command "npx @cloudflare/mcp-server-cloudflare"
hermes mcp add postgres --command "npx @modelcontextprotocol/server-postgres"
hermes mcp add notion --command "npx @notion/mcp-server-notion"
```

These are blocked on **6 missing skills** that need to be installed first (npx/npm). Recommended to do via `hermes skills install` or directly on the host.

---

## What's still missing (next upgrade pass)

### Tier 3 — Skipped this session

| # | Action | Why skipped | Time to do |
|---|--------|-------------|------------|
| 11 | Add 3-5 MCP servers | Needs npm install + network | 1-2 hours |
| 12 | Per-profile toolset config | Each profile needs a unique config.yaml section | 1-2 hours |
| 13 | Populate `/opt/data/source-materials/` with real per-topic content | Internal-only, depends on what you want tracked | 2-3 hours |
| 14 | Build per-department dashboards | HTML page per dept aggregating state files | 4-6 hours |
| 15 | Auto-generate quarterly board deck from state files | Single Python script + template | 1 day |

### Tier 4 — Already in the queue as kanban tasks

| Task | Owner | Board |
|------|-------|-------|
| Sign Rubicón EAS contract | ivan | aiw-org |
| Fill 188 internal questions | ivan | aiw-org |
| Wire CF Worker webhook | kiki | aiw-org |
| Commit /opt/data/agents/ | ivan | aiw-org |
| Add MCP server: github | ivan | aiw-engineering |
| Add MCP server: cloudflare | ivan | aiw-engineering |
| Populate finance.json with real numbers | ivan | aiw-finance |
| Send Richar Ruiz first contact | ivan | aiw-sales |
| Pick first 3 kiki-coach topics | kiki | aiw-people |
| Update THESIS_STATE.md | ivan | thesis-active |
| Populate source-materials/ | ivan | aiw-research |

---

## What you should read next

1. **`/opt/data/agents/SETUP-GUIDE.md`** — the master reference (23KB, 7 layers)
2. **`/opt/data/agents/ORCHESTRATION.md`** — what's running day-to-day
3. **`/opt/data/agents/departments/ORG-AGENTS.md`** — decision rights
4. **`/opt/data/agents/research/188-questions-for-ivan.md`** — your homework
5. **This file** — what just changed

## Quick commands to verify

```bash
hermes cron list                          # see all 17 jobs
hermes config get security.website_blocklist.enabled  # should be true
hermes profile list                        # 7 profiles
hermes project list                        # 11 projects, 14 folders
hermes kanban list --board default         # 12 ready tasks
bash /opt/data/agents/scripts/health.sh    # agent health
```

---

## Rollback / undo

If anything breaks from this session:

```bash
# Disable blocklist (if it breaks something)
hermes config set security.website_blocklist.enabled false

# Revert memory config
hermes config set memory.provider ""
hermes config set memory.write_approval false

# Delete a project
hermes project archive <name>

# Delete a profile
hermes profile delete <name>

# Remove a cron job
hermes cron remove <job_id>
```

---

Last updated: 2026-08-13 by Erebus. Tier 1 + Tier 2 of the management+agent upgrade plan executed. Tier 3-4 remain.