# 06 — People & Culture Playbook

> Department charter + roles + agents + tooling + SOPs for People & Culture.
> **Last updated**: 2026-08-14

---

## People & Culture — Department Charter

**Mission**: Make sure both founders (Ivan + Kiki) and any future hires stay sharp, healthy, and growing. People & Culture is small in headcount but huge in leverage — Ivan's bandwidth and Kiki's growth are the company's most precious resources.

**Head**: Ivan + Kiki (co-owned)
**Deferred**: HR sub-functions until first FTE hire

---

## Roles (8 roles)

| # | Role | Tier | Status |
|---|------|------|--------|
| 6.1 | Head of People / VP HR | 🟢 T1 | Ivan + Kiki |
| 6.2 | Recruiter | 🔴 T4 | deferred (no FTE hires planned) |
| 6.3 | Onboarding Specialist | 🔴 T4 | deferred (no FTE hires) |
| 6.4 | Performance Coach | 🟢 T1 | sub-agent: kiki-coach |
| 6.5 | Recognition Lead | 🟢 T1 | Ivan (periodic rituals) |
| 6.6 | Compensation Specialist | 🔴 T4 | deferred (Ivan sets, no negotiation) |
| 6.7 | People Operations Specialist | 🟠 T3 | deferred (5+ FTEs trigger) |
| 6.8 | Learning & Development Manager | 🟠 T3 | deferred (5+ FTEs trigger) |

---

## Sub-agents (Tier 2)

| Agent | Cadence | Mission |
|-------|---------|---------|
| `kiki-coach` | Fri 17:00 PYT | Weekly lesson for Kyrian |
| `founder-bandwidth-watchdog` | Weekly | Burnout signal detection |

---

## Tooling

### Head of People (Ivan + Kiki)
- **Communication**: Telegram (Ivan ↔ Erebus), WhatsApp bridge
- **Calendar**: Buscador principal Calendar (visible to both)
- **Time tracking**: (none — manual estimate per analysis B6 P3)
- **Recognition rituals**: LinkedIn posts, milestone notes

### Performance Coach
- **Tool**: `kiki-coach` agent + Obsidian for notes
- **Curriculum**: 11-topic queue (8 code + 3 agent ops)

### Recognition Lead
- **Tool**: LinkedIn posts + Canal de comunicacion messages
- **Tracked in**: `state/people.json` `milestones_recent`

---

## SOPs

### Weekly
- Fri 17:00 PYT: kiki-coach lesson
- Weekly: founder-bandwidth-watchdog (burnout signal)

### Monthly
- (none — 2 founders, no HR processes)

### On milestone
- Recognition ritual (per `06-people-culture.md` lines 68-75):
  1. First signed contract in new ICP → LinkedIn post (Sales drafts, Ivan approves)
  2. Thesis chapter published → Research tracker flags for celebration
  3. Major deploy win → Engineering roster notes
  4. Kiki milestone → kiki-coach notes in next lesson

### Annually
- (none)

---

## Hard stops (People dept)

| Action | Authority |
|--------|-----------|
| Kiki picks lesson topic | Kiki |
| Hire contractor < $500/mo | Ivan + Kiki |
| Hire contractor > $500/mo | Ivan + Kiki (joint sign-off) |
| PTO / time off | Person themselves |
| Recognize a milestone (public post) | Person being recognized |

---

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

---

## Kiki-coach curriculum (11 topics)

1. Git rebase vs. merge in a 2-person team
2. Reading a Next.js App Router stack trace
3. Writing a CODEOWNERS file that actually owns
4. Env vars: when .env.local vs GitHub Actions secret vs CF Worker
5. Tailwind v4 design tokens vs inline styles
6. Reading a CF Worker trace — KV, R2, subrequest limits
7. Docker Swarm deploy logs: the 5 lines that matter
8. Pre-commit hooks: husky + lint-staged + what to actually lint
9. **Agent ops**: PROMPT.md patterns (hard stops, idempotency)
10. **Eval gates**: golden trajectories for agent testing
11. **Cron schedules**: PYT/UTC, off-hours density

---

## Burnout signal spec (per BURNOUT-SIGNAL-SPEC.md)

Tracks:
- Hours-worked (calendar density)
- Chat sentiment (informal)
- Deadline clustering

**Threshold**: 70+ hrs/week sustained 3 weeks → page Ivan
**Trigger**: any founder reports "burned out" in chat → check-in
**Escalation**: if no recovery in 2 weeks → suggest PTO

---

## Cultural artifacts (PRESERVE in any plan rewrites)

Per `06-people-culture.md` lines 68-75:
1. First signed contract in new ICP → LinkedIn post
2. Thesis chapter published → celebration
3. Major deploy win → engineering notes
4. Kiki milestone → kiki-coach notes in next lesson

**These are NOT gamified metrics. They're rituals.**

---

## Escalation triggers

- Kiki misses 2 weeks in a row → pause curriculum, send check-in (no auto-resume)
- Contractor not delivering after 14d → Ivan direct (don't auto-renew)
- Founder bandwidth > 70 hrs/week sustained 3+ weeks → Ivan emergency brief (burnout risk)
- Conflict between Ivan and Kiki on a decision → escalate to written decision record (not chat)

---

## What's NOT in this department

- HR policies (no full-time employees yet — premature)
- Performance reviews (2 founders, no reports)
- Compensation (Ivan sets, no negotiation needed)
- Public hiring posts (none planned — the org runs lean)

**When AI Whisperers hires its first employee (not contractor), this department expands.**

---

## Founder bandwidth audit

Manual estimate (per analysis B6 PE-3):
- Ivan: ~50 hrs/week split between billable and internal
- Kiki: ~50 hrs/week split between billable and internal
- Trigger for Chief of Staff role: > 50 hrs/week on coordination (per Metaintro 2026)

---

## See also

- `/opt/data/agents/departments/06-people-culture.md` (canonical charter)
- `/opt/data/agents-v2/agents/kiki-coach/PROMPT.md` (agent spec)
- `/opt/data/agents-v2/BURNOUT-SIGNAL-SPEC.md` (founder-bandwidth-watchdog spec)
