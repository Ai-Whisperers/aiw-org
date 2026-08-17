# DEFERRED-AGENTS.md

> Agent candidates that aren't built yet. Triggers for promotion to T2 lead agent.
> **Last updated**: 2026-08-14

---

## Currently deferred (Tier 2 - planned in Phase 5+)

These agents will be built as the agent layer scales. Each has a trigger that adds them.

| Agent | Dept | Trigger | Build in |
|-------|------|---------|----------|
| `ai-ops-coordinator` | Operations | NOW (Phase 5) | ✅ Built |
| `bizops-tracker` | Operations | NOW | ✅ Built |
| `compliance-monitor` | Finance | NOW | ✅ Built |
| `source-curator` | Research | source-materials > 50 | Phase 5 follow-on |
| `founder-bandwidth-watchdog` | People | NOW | ✅ Built |
| `accounting-automation` | Finance | NOW | ✅ Built |
| `tax-receipt-tracker` | Finance | NOW | ✅ Built |
| `procurement-tracker` | Finance | Active vendors > 5 | NOW |
| `ai-safety-engineer` | Engineering | NOW | ✅ Built |
| `devops-monitor` | Engineering | NOW | ✅ Built |
| `qa-automation-runner` | Engineering | On-PR | ✅ Built |
| `security-watchdog` | Engineering | NOW | ✅ Built |
| `proposal-drafter` | Sales | NOW | ✅ Built |
| `lead-enrichment` | Sales | NOW | ✅ Built |
| `marketing-content-producer` | Sales | NOW | ✅ Built |
| `multimedia-producer` | Sales | NOW | ✅ Built |
| `citation-checker` | Research | NOW | ✅ Built |
| `thesis-tracker` | Research | NOW | existing thesis-daily-tick |
| `course-producer` | Research | NOW | ✅ Built |
| `customer-health-scorer` | Sales (CS) | 5+ clients | Tier 3 dept promotion |

---

## Tier 3 deferred agents (new depts)

| Agent | Dept | Trigger | Build in |
|-------|------|---------|----------|
| `cs-monitor` | Customer Success | 5+ clients | Q4 2026 |
| `ir-monitor` | Investor Relations | First external investor | Q4 2027 |
| `executive-brief-generator` | Chief of Staff | Ivan coord > 50 hrs | Q1 2028 |
| `treasury-monitor` | Treasury | $100K+ cash | Q3 2027 |
| `audit-runner` | Internal Audit | $1M+ revenue | Q2 2028 |
| `t-s-monitor` | Trust & Safety | Consumer AI launch | Q3 2028 |
| `devrel-content-producer` | DevRel | Public API | Q4 2028 |
| `workplace-monitor` | Workplace | Open office | (not planned) |
| `fraud-detector` | Fraud / Risk | $500K+ payment volume | Q4 2028 |
| `comp-monitor` | Compensation | First FTE | Q2 2029 |
| `people-ops` | People Ops | 5+ FTEs | Q3 2029 |
| `press-monitor` | PR | Brand launch | (not planned) |
| `regulatory-monitor` | Gov Relations | Regulated vertical | (not planned) |

---

## Tier 4 enterprise (NOT planned at our scale)

- AI Red Team
- Chief AI Officer (CAIO) - when 50+ engineers
- Chief Data Officer (CDO) - when data product
- Internal Communications Manager - when 50+ people
- M&A / Corp Dev - when acquisitions planned

---

## Agent promotion checklist

When a trigger fires for a new agent:

1. **Create directory**: `/opt/data/agents/<agent-name>/`
2. **Write PROMPT.md** from `/opt/data/agents-v2/prompts/PROMPT-TEMPLATE.md` (12 sections)
3. **Add Hard Stops table** (3-5 dept-specific actions)
4. **Add Idempotency Contract** (window per cadence)
5. **Add Context-Packaging Escalation** (6-field payload)
6. **Add Reflection Loop** (content agents only)
7. **Add Fallback Model**
8. **Create state file** at `/opt/data/db/<agent>.db` (SQLite)
9. **Create outbox dir** with .gitkeep + seed outbox
10. **Validate**: hard-stop-wrapper.py, trademark-scrub.sh, idempotency-check.py
11. **Register cron job** in jobs.json
12. **Run grid.sh** verify zero collisions
13. **Manual run** to verify outbox delivery
14. **Update ORCHESTRATION.md** with new agent
15. **Bump constitution** to v0.X.1

**Estimated effort per agent**: 30-60 minutes (mechanical).

---

## Cross-references

- `/opt/data/agents-v2/ROLES-INVENTORY.md` — roles
- `/opt/data/agents-v2/playbooks/07-cross-cutting-concerns.md` — Tier 2 cross-cutting
- `/opt/data/agents-v2/playbooks/08-deferred-tier3.md` — Tier 3 dept triggers
- `/opt/data/agents/DEFERRED-ROLES.md` — roles (this file = agents)
