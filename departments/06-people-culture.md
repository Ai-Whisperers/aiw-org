# Department 6 — People & Culture

**Head**: Ivan + Kiki (co-owned)
**Lead agent**: `kiki-coach` (Fri 17:00 PYT)
**Version**: 0.2.0
**Last updated**: 2026-08-14

---

## Mission

Make sure both founders (Ivan + Kiki) and any future hires stay sharp, healthy, and growing. People & Culture is small in headcount but huge in leverage — Ivan's bandwidth and Kiki's growth are the company's most precious resources.

## What this department owns

- **Kiki's weekly skill development** — `kiki-coach` agent
- **Contractor onboarding** — when AI Whisperers hires freelance help
- **Founder bandwidth audit** — Ivan + Kiki hours/week on billable vs internal
- **Cultural artifacts** — how the org makes decisions (per `ORG-AGENTS.md` constitution)
- **Recognition** — when a milestone lands (signed contract, thesis chapter, deploy win)
- **NEW v0.2.0**: founder-bandwidth-watchdog (Tier 2)
- **NEW v0.2.0**: Burnout signal detection
- **NEW v0.2.0**: Curriculum refresh (added 3 agent-ops topics)

## What this department does NOT own

- Pricing / contracts (Finance & Legal)
- Code review (Engineering)
- Sales scripts (Sales)
- **HR sub-functions** until first FTE hire (per Session 1 cheatsheet)

## Decision rights (v0.2.0)

| Action | Authority |
|--------|-----------|
| Kiki picks lesson topic | Kiki |
| Hire a contractor < $500/mo | Ivan + Kiki |
| Hire a contractor > $500/mo | Ivan + Kiki (joint sign-off) |
| PTO / time off | Person themselves |
| Recognize a milestone (public post) | Person being recognized |
| **NEW**: Halt agent emitting cognitive noise | Ivan (page on burnout signal) |
| **NEW**: Trigger founder check-in | Ivan on bandwidth > 70 hrs/wk sustained 3 wks |

## Sub-roles (v0.2.0 — 8 roles from ROLES-INVENTORY.md)

| # | Role | Tier |
|---|------|------|
| 6.1 | Head of People / VP HR | 🟢 T1 |
| 6.2 | Recruiter | 🔴 T4 (deferred) |
| 6.3 | Onboarding Specialist | 🔴 T4 (deferred) |
| 6.4 | Performance Coach | 🟢 T1 |
| 6.5 | Recognition Lead | 🟢 T1 |
| 6.6 | Compensation Specialist | 🔴 T4 (deferred) |
| 6.7 | People Operations Specialist | 🟠 T3 (deferred) |
| 6.8 | Learning & Development Manager | 🟠 T3 (deferred) |

## Sub-agents (v0.2.0)

| Agent | Cadence | Class |
|-------|---------|-------|
| `kiki-coach` | Fri 17:00 PYT | CONTENT (reflection) |
| `founder-bandwidth-watchdog` (NEW) | Weekly | OPERATIONAL |

## Inputs the lead agent reads

1. `/opt/data/agents/state/kiki.json` (SQLite) — last 4 lessons + feedback + current_focus
2. `/opt/data/agents/kiki-coach/KIKI-CHARTER.md` — domain bounds (NEVER violate)
3. Kiki's recent commits in `Ai-Whisperers/company`, `marketing-strategy`, `cursor-standards` (last 7d)
4. Current topic she picked (in kiki.json under `current_focus`)
5. `/opt/data/agents/kiki-coach/curriculum.md` — full topic queue

## Curriculum (v0.2.0 — 11 topics)

1. Git rebase vs. merge in a 2-person team
2. Reading a Next.js App Router stack trace
3. Writing a CODEOWNERS file that actually owns
4. Env vars: when .env.local vs GH Secret vs CF Worker
5. Tailwind v4 design tokens vs inline styles
6. Reading a CF Worker trace — KV, R2, subrequest limits
7. Docker Swarm deploy logs: the 5 lines that matter
8. Pre-commit hooks: husky + lint-staged + what to actually lint
9. **NEW** Agent ops: PROMPT.md patterns (hard stops, idempotency)
10. **NEW** Eval gates: golden trajectories for agent testing
11. **NEW** Cron schedules: PYT/UTC, off-hours density

## Cadence

| Time | What |
|------|------|
| Fri 17:00 PYT | kiki-coach lesson |
| Weekly | founder-bandwidth-watchdog |
| On milestone | Recognition ritual (LinkedIn post, internal note) |

## Cultural artifacts (PRESERVE in any plan rewrites)

Per `06-people-culture.md` lines 68-75:
1. First signed contract in new ICP → LinkedIn post
2. Thesis chapter published → celebration
3. Major deploy win → engineering notes
4. Kiki milestone → kiki-coach notes in next lesson

**These are NOT gamified metrics. They're rituals.**

## Burnout signal spec (per BURNOUT-SIGNAL-SPEC.md)

Tracks:
- Hours-worked (calendar density)
- Chat sentiment (informal)
- Deadline clustering

**Threshold**: 70+ hrs/week sustained 3 weeks → page Ivan
**Trigger**: any founder reports "burned out" in chat → check-in
**Escalation**: if no recovery in 2 weeks → suggest PTO

## State schema (`state/people.json`)

```json
{
  "last_run": null,
  "kiki_lesson_streak_weeks": 0,
  "kiki_total_lessons_completed": 0,
  "contractors_active": [],
  "contractor_onboarding_queue": [],
  "founder_bandwidth_audit": {
    "ivan": {"billable_hours_week": null, "internal_hours_week": null},
    "kiki": {"billable_hours_week": null, "internal_hours_week": null}
  },
  "milestones_recent": []
}
```

## Escalation triggers

- Kiki misses 2 weeks in a row → pause curriculum, send check-in (no auto-resume)
- Contractor not delivering after 14d → Ivan direct (don't auto-renew)
- Founder bandwidth > 70 hrs/week sustained 3+ weeks → Ivan emergency brief
- Conflict between Ivan and Kiki on a decision → escalate to written decision record

## On-call rotation

Per Gap-audit (deferred but documented):
- Ivan = primary
- Kiki = backup
- Cycle: monthly
- Documented in: `/opt/data/agents/ON-CALL.md` (TODO)

## What's NOT in this department

- HR policies (no full-time employees yet)
- Performance reviews (2 founders, no reports)
- Compensation (Ivan sets, no negotiation needed)
- Public hiring posts (none planned — the org runs lean)

**When AI Whisperers hires its first employee (not contractor), this department expands.**

## Cross-references

- Constitution: `/opt/data/agents/departments/ORG-AGENTS.md` (v0.2.0)
- Playbook: `/opt/data/agents-v2/playbooks/06-people-culture.md`
- Agent spec: `/opt/data/agents-v2/agents/kiki-coach/PROMPT.md`
- Burnout spec: `/opt/data/agents-v2/BURNOUT-SIGNAL-SPEC.md`

---

## CHANGELOG

- v0.2.0 (2026-08-14): added 8 sub-roles, founder-bandwidth-watchdog, 3 new curriculum topics (agent ops track), Burnout signal spec, Cross-references.
- v0.1.0 (2026-08-13): initial ratification.
