# Coach Agents — Internal Coaching Product

> **Status**: Live production. 11 agents. 13 cron jobs. Zero downtime target.

This directory contains the **internal AIW coaching product** — the agents that coach Ivan, Kiki, and the org. It is the production runtime layer for coaching inside the AIW organization.

---

## What's in this directory

### Production agents (14)

These are the live agents — each has a `PROMPT.md` and an `outbox/` of historical briefs. They run on cron schedules.

#### Coach-* (11) — coaching product agents
| Agent | Cron | Mission |
|---|---|---|
| `coach-cohort-facilitator` | planned | Cohort-based learning facilitator (planned) |
| `coach-conversion-agent` | planned | Coaching conversion (planned) |
| `coach-ivan` | Sun 21:00 | Self-coaching for Ivan (Kiki as coach) |
| `coach-kiki` | Fri 21:00 | Self-coaching for Kiki |
| `coach-lead-agents` | 1st 22:00 | Coaches lead agents on GROW |
| `coach-lead-finder` | Wed 13:00 | Lead-finding coaching |
| `coach-onboarding` | live poller */5m | Customer/FTE onboarding |
| `coach-org` | quarterly | Org-wide coaching |
| `coach-practitioner` | planned | Practitioner coaching |
| `coach-renewal-manager` | 1st 09:00 | Renewal coaching |
| `coach-roi-tracker` | Fri 16:00 | ROI coaching |

#### Coaching-* (3) — coaching-adjacent content + quality + research
| Agent | Cron | Mission |
|---|---|---|
| `coaching-content-curator` | Mon 14:00 | Curates coaching content calendar |
| `coaching-quality-reviewer` | every 30m | Reviews coaching output quality |
| `coaching-research-intelligence` | Wed 13:00 | Coaching research signal collection |

### Cron jobs (13)

All defined in `/opt/data/cron/jobs.json`:
- `aiw-kiki-coach-weekly`
- `aiw-coach-ivan`
- `aiw-coach-kiki`
- `aiw-coach-org`
- `aiw-coach-lead-agents`
- `aiw-coaching-content-curator`
- `aiw-coaching-quality-reviewer` (every 30 min)
- `aiw-coaching-research-intelligence`
- `aiw-coach-renewal-manager`
- `aiw-coach-roi-tracker`
- `aiw-coach-lead-finder`
- `aiw-coach-onboarding-poller` (*/5m — live WhatsApp→coaching)
- `aiw-coaching-monitor-30min`

---

## What is NOT in this directory

### The distributable Coaching package

`growth-coaching` repo at `packages/coaching/` is a **separate artifact** — the **distributable** coaching product that paying customers deploy. It contains 5 agents (`kiki-coach`, `thesis-tracker`, `course-producer`, `coaching-customers`, `conversion-funnel`) plus playbooks, schemas, and a state template.

**Why this is separate:**
- **agent-infra** = the AIW org's own runtime (agents, cron, state, scripts)
- **growth-coaching** = the product deliverable line (6 packages customers can pull)

Mixing them in one repo conflates "internal staff tool" with "external customer product" — different audiences, different lifecycles, different access controls.

| Layer | Repo | Audience | Update cadence |
|---|---|---|---|
| This `coach/` (org-internal) | `agent-infra` (this repo) | AIW team | Continuous, runtime |
| `packages/coaching/` (distributable) | `growth-coaching` | Paying customers | Per release |

---

## How to add a new coach agent

1. Create `coach/<new-agent-name>/PROMPT.md` using the standard 12-section template
2. Add `outbox/` subdir
3. Register cron job in `/opt/data/cron/jobs.json` (use any `aiw-coach-*` cron as template)
4. Update this README with the new row
5. Push — the cron-guard will pick up the new job on next `cron-sync`

---

## Future repo split (when you're ready)

When the time comes to physically split this directory into its own repo (`Ai-Whisperers/coaching-agents`), the steps are:

```bash
# 1. Create the new repo on GitHub (private)
gh repo create Ai-Whisperers/coaching-agents --private --description "Internal AIW coaching product — coaches Ivan, Kiki, leads, and FTEs"

# 2. In a fresh clone of agent-infra, filter history to just the coach/ subtree
git clone git@github.com:Ai-Whisperers/agent-infra.git coaching-agents-split
cd coaching-agents-split
git filter-repo --path coach/ --path-rename '':
git remote add new git@github.com:Ai-Whisperers/coaching-agents.git
git push new --all

# 3. Update the runtime layer:
#    a. Re-register 13 cron jobs with new prompt paths
#    b. Update 258+ script + state-file references from /opt/data/agents/coach/ to /opt/data/coaching-agents/
#    c. Move /opt/data/state/contexts/coach-*/ to the new repo
#    d. Update coord.json outbox paths
#    e. Update /opt/data/scripts/coach-onboarding-poller.py
#    f. Smoke-test: run coach-onboarding-poller for 1h, verify no errors

# 4. Remove coach/ from agent-infra once the new repo is live
git -C agent-infra rm -r coach/
git -C agent-infra commit -m "coach: migrated to Ai-Whisperers/coaching-agents"
```

**Effort estimate**: 4-6 hours of careful mechanical work + 24-48h of monitoring. **Do NOT do this without smoke-testing every cron job in staging first.**

The current directory layout (everything in `coach/` here) is the prerequisite for that future split — `git mv` into a subdirectory today means the split tomorrow is one `git filter-repo` command away instead of a fragile multi-file rewrite.

---

## See also

- `/opt/data/agents/analysis/DEPT-AGENTS-ROLES-COMPLETE.md` — Tier-5 Coaching section (canonical roster)
- `/opt/data/agents/analysis/ORGANIGRAM.md` — full dept→role→agent tree
- `/opt/data/agents-v2/packages/coaching/` — the distributable product (in `growth-coaching` repo)
- `/opt/data/cron/jobs.json` — all cron jobs (search `coach` for the 13 above)
- `/opt/data/scripts/coach-onboarding-poller.py` — live WhatsApp→coaching poller