# Phase 6 — Refinement (Fix Execution Gaps Before Tier Expansion)

> **Date**: 2026-09-01
> **Trigger**: Ivan's question "continue with other tiers or refine?" + AI's honest audit finding.
> **Decision**: REFINE ONLY. Fix 3 execution gaps before expanding.

---

## Why refine instead of expand

Phase 5 made the **docs** structurally complete (5/5 + 28 sub-agent monitors + 4 new PROMPTs). But Ivan asked the right question, and the audit revealed:

| Gap | Severity | What |
|-----|----------|------|
| **A** | HIGH | 17 of 18 new sub-agent monitors have no cron wiring. They are PROMPT.md files that exist but **no LLM cron invokes them**. |
| **B** | MEDIUM | PROMPT-monitor.md files reference `/opt/data/agents/state/*` paths when real state is at `/opt/data/state/*`. |
| **C** | MEDIUM | Some monitors reference files that may not exist (e.g., `eval-per-agent.json` lives at `/opt/data/state/` not `/opt/data/agents/state/`). |

**Adding Tier-3/4 depts on top of an execution-broken foundation** would multiply the debt. Better to fix these now (cheap, fast) than later (expensive, after more monitors are added).

---

## Plan

### Gap A — Wire the 17 unwired sub-agent monitors to cron jobs

The existing 21 monitor crons are **LLM-driven jobs** with a `prompt:` field that says:
> "Read `/opt/data/agents/04-engineering/engineering-roster/PROMPT-monitor.md` for full threshold rules. Watch state files..."

For each new sub-agent monitor that has no cron:
1. Create a cron job with:
   - `name: aiw-{subagent}-monitor-{cadence}`
   - `prompt: Read /opt/data/agents/{path}/{subagent}/PROMPT-monitor.md...`
   - `schedule: 30m` for 30-min cadence, `daily` for daily
2. Match the cadence of the existing crons (daily for non-engineering; 30min for engineering sub-agents)

### Gap B — Fix state-path references in PROMPT-monitor.md

Change all `/opt/data/agents/state/*.json` references to `/opt/data/state/*.json`.

This is a sed across all 18 new monitor files. The pattern is consistent.

### Gap C — Verify file existence claims

For each "Files watched" table in each monitor, verify the file actually exists. If not, either:
- Mark the metric as "deferred until file exists" (MEDIUM-only)
- Or remove the metric

The most likely offender: `eval-per-agent.json` (referenced by `ai-safety-engineer` and `eval-gate-runner` monitors).

---

## Out of scope (for this phase)

- Building Tier-3 depts (deferred per doctrine)
- Tuning threshold values (needs real cron data)
- Adding more sub-agent monitors (Phase 5 already at 100%)

---

## Success criteria

By end of Phase 6:
- All 18 sub-agent PROMPT-monitor.md have a wired cron job in `jobs.json`
- All references to state files point to `/opt/data/state/*`
- Smoke gate still 100% pass
- 1 feedback doc capturing what worked / didn't
- 1 commit

Estimated time: 30-45 minutes.
