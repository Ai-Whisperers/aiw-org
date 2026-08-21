# Ivan todo — Session Migration Index

> **Purpose:** Drop every heavy work session into one file so you can paste issues into the `ivan-todo` project / Linear / Notion at your own pace.
> **Generated:** 2026-08-18
> **Source DB:** `/opt/data/state.db` — 2,856 non-empty sessions, **115 non-cron work sessions** ranked by message count.

## How to use this file

1. Open the Hermes `ivan-todo` project (`p_e7991380` in projects.db).
2. Each entry below has: `#msgs #tools | title | @session-link | goal | outcome | suggested label`.
3. Paste the ones you want into the project. The ones marked 🟢 are highest value.

---

## 🟢 Tier A — Heavy work sessions (>500 msgs) — **move these first**

### 1. Hermes Implementation Analysis — 1,466 msgs / 755 tools
- **Link:** @session:default/20260814_204100_41af5b
- **Started:** 2026-08-14 20:41 UTC
- **Goal:** "analyze this and explain if we have this implemented in our repo. analyze all internal zips and all relevant data etc. hermes-improvements.zip"
- **Outcome:** Deep study of the Eneve `.cursor/` framework as a reference for our agent layer — extracting patterns to map onto our Hermes architecture.
- **Sugg. label:** `arch-review`, `hermes-internals`

### 2. Department Organization Deep Dive — 1,117 msgs / 546 tools
- **Link:** @session:default/20260814_191200_39bfe6
- **Started:** 2026-08-14 19:12 UTC
- **Goal:** Recording-driven department analysis (Finance, HR, Legal). What we have built, what's missing.
- **Outcome:** Inventory of 47 agent PROMPT.md, 191 skills, 61 cron jobs, 6 dept profiles, 11 projects, 14 bound folders.
- **Sugg. label:** `org-design`, `departments`

### 3. Code Review and Merge — 1,059 msgs / 549 tools
- **Link:** @session:default/20260813_172952_440ed1
- **Started:** 2026-08-13 17:29 UTC
- **Goal:** Work on `IvanWeissVanDerPol/ligare-poly` (privacy-first mobile PWA for polycules).
- **Outcome:** `max_concurrent_children: 3`, max spawn depth 1, orchestrator enforcement — agent config wired.
- **Sugg. label:** `ligare-poly`, `code-review`

### 4. Missing HERMES-PROMPT Documentation — 990 msgs / 459 tools
- **Link:** @session:default/20260811_035727_ffb58ac2
- **Started:** 2026-08-11 03:57 UTC
- **Goal:** Read docs/HERMES-PROMPT.md in ligare-poly and execute Step 1.
- **Outcome:** PR #19 ready to merge — CI green, 9 new files, 1113 insertions. Built AGENT-OPERATIONS.md (4-state protocol) and companion docs.
- **Sugg. label:** `ligare-poly`, `docs`

### 5. Thesis — 892 msgs / 434 tools
- **Link:** @session:default/20260810_224134_82fad0
- **Started:** 2026-08-10 22:42 UTC
- **Goal:** `IvanWeissVanDerPol/satellite-paraguay` — what to work on?
- **Outcome:** 12-week roadmap committed; cron fleet green; Supabase proxy deployed. Three threads: commit roadmap, deploy Supabase proxy, recover cron jobs.
- **Sugg. label:** `thesis`, `roadmap`

### 6. Nexa Paraguay Website Analysis — 880 msgs / 452 tools
- **Link:** @session:default/20260814_193938_52a5e9
- **Started:** 2026-08-14 19:39 UTC
- **Goal:** "let's work on nexa paraguay, analyze what we have in the website"
- **Outcome:** Live site fully updated — Menú button + 52px centered logo + dropdown across ES/EN/PT locales. All 4 routes verified (Home, Services, Data Policy, Feedback).
- **Sugg. label:** `nexa`, `client-site`

### 7. Email Access (no title) — 692 msgs / 274 tools
- **Link:** @session:default/20260817_121634_4fefaf
- **Started:** 2026-08-17 12:16 UTC
- **Goal:** "CAN YOU ACCESS MY EMAILS AND SEND MAILS ON MY BEHALF?"
- **Outcome:** Himalaya CLI installed; inbox dir created at `/opt/data/.hermes/inbox/`; one-liner script for Servarica noVNC.
- **Sugg. label:** `email`, `infra`

### 8. Domain Registration for Rubicón EAS — 620 msgs / 375 tools
- **Link:** @session:default/20260810_202155_cf05d6
- **Started:** 2026-08-10 20:25 UTC
- **Goal:** Erebus-style agency brief turned into Rubicón EAS intake — full setup plan.
- **Outcome:** Rubicón EAS website repo + 638 KB of marketing/outreach (PLAYBOOK.md, 60-file Ometz reference, 54 templates, 3 scripts, red-colegas CRM live at rubiconeas.paragu-ai.com/red-colegas).
- **Sugg. label:** `rubicon-eas`, `marketing`

### 9. Hermes Gateway Session Sharing — 563 msgs / 235 tools
- **Link:** @session:default/20260814_172613_18157b
- **Started:** 2026-08-14 17:26 UTC
- **Goal:** "help me get credentials to log into hermes from another device i need the token"
- **Outcome:** Multi-profile gateway with `multiplex_profiles: true` — `/p/ivan/v1`, `/p/kiki/v1` (200 OK each, 401 cross-key). Sandbox-blocked on `cloudflared tunnel login` — needs laptop-side manual run.
- **Sugg. label:** `hermes-internals`, `gateway`

### 10. WhatsApp Hermes Setup Complete — 551 msgs / 282 tools
- **Link:** @session:default/20260810_160940_128456
- **Started:** 2026-08-10 16:09 UTC
- **Goal:** "lets setup whatsapp so it works for hermes"
- **Outcome:** WA bridge fully operational — nexa-paraguay group replies in 9.0s, all groups routing. Pipeline status: live.
- **Sugg. label:** `wa-bridge`, `infra`

### 11. Client Hosting Setup — 542 msgs / 239 tools
- **Link:** @session:default/20260812_185111_9e55d3
- **Started:** 2026-08-12 18:51 UTC
- **Goal:** Inventory 6 priority client sites (hidrobaby-spa, portas-barber, arnos, cronos-academy, estudio-medieval, scott-tatuajes) under `*.paragu-ai.com`; apex www; LiteLLM proxy.
- **Outcome:** Per-client AI metering design via LiteLLM — token counts, cost per model.
- **Sugg. label:** `clients`, `hosting`

### 12. Server and Device Inventory Analysis — 512 msgs / 259 tools
- **Link:** @session:default/20260812_170308_22aed8
- **Started:** 2026-08-12 17:03 UTC
- **Goal:** "analyze the servers i have and explain all devices servers etc we have"
- **Outcome:** Host A production audit — Alertmanager churn diagnosed (telegram chat_id 400, not critical); Qdrant internal, no fix needed.
- **Sugg. label:** `infra`, `inventory`

---

## 🟡 Tier B — Medium sessions (100–500 msgs) — pick the relevant ones

### 13. Session Audit (no title) — 403 msgs / 191 tools
- **Link:** @session:default/20260814_220615_3340fb
- **Started:** 2026-08-14 22:06 UTC
- **Goal:** "can you clean or hide sessions that are just test of the AI to the AI not really sent by me"
- **Outcome:** Audit complete — 28,257 messages across 2,183 sessions, 0 orphan messages, FTS5 fully indexed. Healthy.
- **Sugg. label:** `housekeeping`, `audit`

### 14. Management Agents and Automation Setup — 342 msgs / 171 tools
- **Link:** @session:default/20260813_161650_05a284
- **Started:** 2026-08-13 16:16 UTC
- **Goal:** "analyze the org and help us with management agents and automations"
- **Outcome:** 6-department org, 22 cron jobs (was 17), 9 state files + schemas, live dashboard, 14 MCP servers, 12 kanban tasks seeded.
- **Sugg. label:** `org-design`, `agents`

### 15. Connecting Hermes Desktop Systems — 335 msgs / 176 tools
- **Link:** @session:default/20260817_124424_516da7
- **Started:** 2026-08-17 12:44 UTC
- **Goal:** Kiki needs to connect local Hermes Desktop to remote gateway.
- **Outcome:** SSH key check procedure; CF Access gate pending; LLM credits out. Pending: tunnel + CF Access.
- **Sugg. label:** `kiki`, `gateway`

### 16. Instagram Access Options — 317 msgs / 188 tools
- **Link:** @session:default/20260817_122135_35596c
- **Started:** 2026-08-17 12:21 UTC
- **Goal:** "can you access instagram?"
- **Outcome:** Social-graph MCP installed at `/opt/data/integrations/social-graph-mcp/`, MCP handshake verified.
- **Sugg. label:** `integrations`, `social-graph`

### 17. Funding Plan Analysis — 296 msgs / 139 tools
- **Link:** @session:default/20260814_194524_4bb1d7
- **Started:** 2026-08-14 19:45 UTC
- **Goal:** Funding mentioned in @session:`default/20260814_191200_39bfe6`
- **Outcome:** Subagent did 48 API calls, integrated 17 platforms → updated alternative-investors catalog pushed to GitHub.
- **Sugg. label:** `funding`, `research`

### 18. GeoData Project Status Check — 271 msgs / 148 tools
- **Link:** @session:default/20260814_004536_4b8874
- **Started:** 2026-08-14 00:45 UTC
- **Goal:** "SEARCH FOR THE GEODATA PROJECT WEBSITE AND MAKE SURE ITS LIVE. ANALYZE ALL REPOS IN THE ORG"
- **Outcome:** Browser console errors traced to orphaned JS in old Service Worker (`paraguay-geodata-v8`). Audit + deploy + fix complete.
- **Sugg. label:** `geodata`, `thesis`

### 19. Bitwarden Access Options — 283 msgs / 115 tools
- **Link:** @session:default/20260817_161818_244ad8
- **Started:** 2026-08-17 16:18 UTC
- **Goal:** "can you access bitwarden?"
- **Outcome:** `bw` CLI v2026.6.0 installed; inbox dir created; BWS access token saved.
- **Sugg. label:** `integrations`, `secrets`

### 20. GitHub Commits and Deployment Prep — 262 msgs / 132 tools
- **Link:** @session:default/20260810_154422_7d6d02
- **Started:** 2026-08-10 15:44 UTC
- **Goal:** Paragu-ai-platform commit history review + deploy.
- **Outcome:** Sync state all green — GitHub → Host A → Image → Container → Public, end-to-end verified.
- **Sugg. label:** `deploy`, `github`

### 21. AI Coaching Company Research — 237 msgs / 155 tools
- **Link:** @session:default/20260814_200344_e56856
- **Started:** 2026-08-14 20:03 UTC
- **Goal:** "research also coaching companies for companies and all relevant things in our repos"
- **Outcome:** Sunstein & Solstein Inventory v2 (~28KB, ~600 lines) at `/opt/data/agents/research/sunstein-solstein-inventory-v2.md`.
- **Sugg. label:** `coaching`, `research`

### 22. Saskia/WhatsApp Gateway Connect — 235 msgs / 97 tools (whatsapp)
- **Link:** @session:default/20260813_163144_10b5240b
- **Started:** 2026-08-13 16:31 UTC
- **Goal:** Saskia asked for credentials to connect via gateway.
- **Outcome:** Server-side health 100% (5/5 ALIVE probes, port 22 listening) — but client-side connectivity issues.
- **Sugg. label:** `kiki`, `gateway`

### 23. Richar Ruiz Outreach Repo Analysis — 208 msgs / 119 tools
- **Link:** @session:default/20260812_171637_05c023
- **Started:** 2026-08-12 17:16 UTC
- **Goal:** `https://github.com/Ai-Whisperers/richar-ruiz-outreach` — analyze all of this
- **Outcome:** Commit `e85dadd`, pushed — 13 files, 521 insertions, 77 deletions. Sanitized 12 corporate client names (Bayer, Itaú, Siegfried, Tigo, Heisecke, Atlas, Suramericana, Cadiem).
- **Sugg. label:** `sales`, `outreach`

### 24. WhatsApp Status Check — 203 msgs / 88 tools
- **Link:** @session:default/20260812_175218_7ca5ed
- **Started:** 2026-08-12 17:52 UTC
- **Goal:** "is whatsapp online?"
- **Outcome:** Operation interrupted (model 0.3s elapsed). Reopened status.
- **Sugg. label:** `wa-bridge`

### 25. Server Access Confirmed — 187 msgs / 66 tools
- **Link:** @session:default/20260817_175723_7acd78
- **Started:** 2026-08-17 17:57 UTC
- **Goal:** "do you have access to the servarica servers etc"
- **Outcome:** BWS token validation — token non-functional at Bitwarden API (invalid_client). Likely needs refresh.
- **Sugg. label:** `infra`, `secrets`

---

## 🔵 Tier C — Lower priority (50–150 msgs) — review case-by-case

These are listed in /opt/data/state.db but didn't crack top 25. Total ~75 more sessions. The notable ones by title:

| msgs | title | link |
|---:|---|---|
| 151 | Hermes Installation and Setup Guide | @session:default/20260812_180213_xxx |
| 131 | SSH Connection Troubleshooting | @session:default/20260817_164600_xxx |
| 125 | Model Configuration Fix | @session:default/20260814_184600_xxx |
| 121 | Email Address Search Results Discrepancy | @session:default/20260817_121300_xxx |
| 73 | Kikia's Hermes Desktop Access | @session:default/20260817_160500_xxx |

(Full DB query: `sqlite3 /opt/data/state.db "SELECT id, title, message_count FROM sessions WHERE source != 'cron' AND message_count > 50 ORDER BY message_count DESC"`)

---

## ⚪ Tier D — Skip these

- All 2,723 cron watchdog sessions (thesis-watchdog, evo-poll-watchdog, aiw-security-watchdog-30min, etc.) — they're polling infrastructure, not real work.
- 100+ sub-100-msg desktop/TUI/whatsapp noise sessions — empty user messages, 1-2 message exchanges.

---

## Suggested `Ivan todo` groupings (label prefixes)

| Group | Sessions |
|---|---|
| `arch-review` | #1 |
| `org-design` | #2, #14 |
| `ligare-poly` | #3, #4 |
| `thesis` | #5, #18 |
| `nexa` | #6 |
| `email` | #7 |
| `rubicon-eas` | #8 |
| `hermes-internals` | #1, #9 |
| `wa-bridge` | #10, #24 |
| `clients` | #11 |
| `infra` | #12, #25 |
| `housekeeping` | #13 |
| `kiki` | #15, #22 |
| `integrations` | #16, #19 |
| `funding` | #17 |
| `geodata` | #18 |
| `deploy` | #20 |
| `coaching` | #21 |
| `sales` | #23 |

---

*Last generated: 2026-08-18 18:30 UTC — pull from `state.db` again to refresh.*
