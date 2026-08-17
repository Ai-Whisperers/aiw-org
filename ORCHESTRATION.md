# AI Whisperers — Management Agents & Automation

> The operating layer between Erebus (general agent) and the company's daily work.
> Three roles. Each is a focused agent prompt + cron schedule + state file.

---

## TL;DR — what's running

| Agent | Schedule | Role | Owner |
|-------|----------|------|-------|
| **business-analyst** | Daily 06:30 PYT | Mines all signals, produces one-page business briefing | Ivan reads daily |
| **management-coordinator** | Mon/Thu 18:00 PYT | Tracks open work across repos, surfaces blockers | Ivan reads 2×/wk |
| **kiki-coach** | Friday 17:00 PYT | Teaches Kyrian (co-founder) one new skill per week | Kyrian reads 1×/wk |

Each agent has:
- **Prompt** — `/opt/data/agents/<agent>/PROMPT.md`
- **State** — `/opt/data/agents/state/<agent>.json` (decisions, focus shifts, open questions)
- **Output** — delivered to origin chat at scheduled time, archived in `/opt/data/agents/<agent>/outbox/`

---

## Why these three

The org currently has **10 cron jobs** (4 thesis tickers, 3 watchdogs, 2 weekly refresh, 1 morning brief). What's missing:

1. **A business lens** — Ivan is the only one who knows if we're winning. The morning brief shows infrastructure; nobody tracks *pipeline health, conversion rate, MRR direction, content performance*. Business-analyst closes that gap.
2. **Cross-repo work tracking** — 17 active repos + thesis + outreach. Without a coordinator, work dies in stale branches. Management-coordinator is the hub that knows "what's open, who's blocked, what to ship next."
3. **Knowledge transfer to Kyrian** — Ivan's domain expertise is concentrated in his head. Kiki-coach makes it a weekly ritual: one concept, one example, one exercise. The agent never replaces Ivan — it scaffolds Kyrian to ask better questions.

---

## Architecture

```
                     ┌─────────────────────────┐
                     │  /opt/data/agents/      │
                     │  ├─ business-analyst/   │
                     │  ├─ management-coord./  │
                     │  └─ kiki-coach/         │
                     │      ├─ PROMPT.md       │
                     │      ├─ outbox/         │  ← dated .md briefs
                     │      └─ lessons/        │  ← kiki only
                     └────────────┬────────────┘
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │  /opt/data/agents/state │
                     │  ├─ analyst.json        │  ← rolling 7-day decisions
                     │  ├─ coord.json          │  ← open issues + owners
                     │  └─ kiki.json           │  ← learning log
                     └────────────┬────────────┘
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │  hermes cron jobs       │
                     │  (agent-driven prompts) │
                     └─────────────────────────┘
```

Cron job IDs (canonical):
- `aiw-business-analyst-daily` — `0 10:30 * * *` (06:30 PYT, after morning-brief at 06:00)
- `aiw-management-coord-biwk` — `0 21 * * 1,4` (17:00 PYT Mon/Thu)
- `aiw-kiki-coach-weekly` — `0 21 * * 5` (17:00 PYT Fri)

---

## Inputs each agent reads

| Agent | Reads | Doesn't read |
|-------|-------|--------------|
| **business-analyst** | cron logs, GH commit activity, lead-pipeline data (rubicon-eas-lead), site health (site-health cron), live-site HTTP checks | session DB (too noisy), wa_bridge logs (privacy) |
| **management-coordinator** | GH issues/PRs across all 17 repos, `paragu-ai-platform` todo board, thesis tick state, agent-tasks/ from marketing-strategy | infra metrics (those go to analyst), session content |
| **kiki-coach** | Kyrian's recent commits in `company`, `marketing-strategy`, `cursor-standards` repos; her session DB; lesson library | Ivan's private sessions, anything from her private repos without consent |

---

## Output contract (each agent)

Every agent writes to `/opt/data/agents/<agent>/outbox/YYYY-MM-DD.md` AND delivers to chat:

- **Length**: 150-300 words, no padding
- **Structure**: 3-5 sections max, scannable in 30 seconds
- **No emojis in headlines** (style per CLAUDE.md in `company`)
- **Cite sources**: every claim links to a path or URL
- **Action items end with `→` and owner**

If the agent has nothing actionable, it returns a one-liner: `✅ All clear — no fires today, [reason]`.

---

## Update protocol

- **Adding a new agent**: create `<agent>/PROMPT.md`, register cron job, append to this file's "What's running" table.
- **Editing an agent**: bump version in the prompt header + add a CHANGELOG line at the bottom of the prompt file.
- **Removing an agent**: `hermes cron remove <job-id>` first, then delete the directory.

---

## Health monitoring

Run `bash /opt/data/agents/scripts/health.sh` to verify all three agents delivered in the last 7 days. Wire it into the morning brief as a one-liner.

Last updated: 2026-08-13 (initial rollout)