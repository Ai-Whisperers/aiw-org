# AIW Remaining Tasks — Complete Wishlist (post-DEMIURGE merge, 2026-08-31)

> **Generated**: 2026-08-31, after merging `epic/DEMIURGE` into `main` of `growth-coaching`.
> **DEMIURGE is the source of truth** for the 24 active agents. Heritage agents (23) from the constitution keep portmanteau names until migrated.
> **Current state**: 759 files in main, 83 DEMIURGE tickets, 24 active agents, 22 incomplete tickets.

---

## Current state summary

| Metric | Value |
|---|---|
| Total DEMIURGE tickets | 83 |
| Completed tickets | 61 (73%) |
| Incomplete tickets | 22 (27%) |
| DEMIURGE agents active | 24 |
| Heritage agents awaiting migration | 23 |
| Departments in main | 32 dirs (16 real + 16 archive) |
| Tests | 23 |
| Source materials | 22 |
| Patterns | 8 |
| Total files in main | 759 |

### Incomplete DEMIURGE tickets (22)

| # | Ticket | Sprint | Status | Size | What |
|---|---|---|---|---|---|
| 1 | DEMIURGE-008 | Domain model | active | ? | review gate |
| 2 | DEMIURGE-015 | Sprint 1 | active | ? | review gate |
| 3 | DEMIURGE-033 | Sales dept | active | ? | activation review |
| 4 | DEMIURGE-041 | Sales dept | active | ? | activation review |
| 5 | DEMIURGE-047 | Sales dept | active | ? | activation review |
| 6 | DEMIURGE-054 | Sprint 6 | active | ? | observation window |
| 7 | DEMIURGE-068 | Sprint 6 | pending | ? | first sprint |
| 8 | DEMIURGE-070 | Phase 1 | (planned) | 45m | department taxonomy v2 |
| 9 | DEMIURGE-071 | Phase 1 | (planned) | 30m | fix doc-impl drift in README/ORGANIGRAM |
| 10 | DEMIURGE-072 | Phase 1 | (planned) | ? | inventory Ivan's Hermes dept profiles |
| 11 | DEMIURGE-073 | Phase 1 | (planned) | ? | define AI Org Platform dept |
| 12 | DEMIURGE-074 | Phase 2 | (planned) | ? | operations dept source research |
| 13 | DEMIURGE-077 | Phase 1 | (planned) | 90m | authoritative terminology library v1 |
| 14 | DEMIURGE-078 | Phase 1+3 | (planned) | 120m | document intelligence system + agents |
| 15 | DEMIURGE-082 | Phase 3 | pending | 30m | add migration annotations to legacy agents-prompts |
| 16-22 | (sprint gaps) | ? | ? | ? | missing ticket files for DEMIURGE-069, -083 |

---

# Wishlist — complete (organized by source)

## From P0-ADVISORY (5 secret leaks)

These are the critical operator actions that block everything else:

| # | Action | Time | Owner |
|---|---|---|---|
| 1 | Supabase dashboard → rotate service-role key | 5 min | Ivan |
| 2 | github.com/settings/tokens → revoke `ghp_u0Cs76...URyZ` | 1 min | Ivan |
| 3 | github.com/settings/tokens → revoke `ghp_Rfi9...6irj` | 1 min | Ivan |
| 4 | `gh repo edit --visibility private` on saskia-personal-context | 5 min | Ivan |
| 5 | Replace 16 R2 presigned URLs in rubicon-eas-website/worker.js | 2 hr | Kiki |

**Total: ~75 min operator work. All other work blocked on these.**

---

## From DEMIURGE roadmap (Phase 1 — current)

| # | Ticket | Action | Size |
|---|---|---|---|
| 6 | DEMIURGE-070 | Update `department-taxonomy-v1.md` to add 7 new depts + promote 6 partials | 45m |
| 7 | DEMIURGE-071 | Fix README/ORGANIGRAM drift (counts say "16 depts" but only 3 active) | 30m |
| 8 | DEMIURGE-072 | Inventory Ivan's Hermes dept profiles → stub agent.yaml per profile | TBD |
| 9 | DEMIURGE-073 | Define AI Org Platform as a meta-framework department | TBD |
| 10 | DEMIURGE-077 | Authoritative terminology library v1 | 90m |
| 11 | DEMIURGE-082 | Add migration annotations to legacy `agents-prompts/` files | 30m |

---

## From DEMIURGE roadmap (Phase 2 — Operations reference build)

| # | Ticket | Action | Size |
|---|---|---|---|
| 12 | DEMIURGE-074 | Operations dept source research: signal-driven ops frameworks | TBD |
| 13 | DEMIURGE-075 (DONE) | Define operations dept skeleton | 60m |
| 14 | DEMIURGE-076 (DONE) | Design Kronos ops lead + Hermes router wiring | 45m |
| 15 | DEMIURGE-079 (DONE) | Migrate operations legacy agents to DEMIURGE standard | 120m |
| 16 | DEMIURGE-080 (DONE) | Normalize signal schemas and routing tags | 120m |

---

## From DEMIURGE roadmap (Phase 3 — Meta-agent framework)

| # | Ticket | Action |
|---|---|---|
| 17 | DEMIURGE-078 | Document intelligence system + 5 agents (Themis, Mnemosyne, Hephaestus, Peitho, Pheme, Orpheus) |
| 18 | DEMIURGE-081 (DONE) | Wire knowledge-mgmt dept attribution and routing |
| 19 | NEW | Extract "Department Researcher" meta-agent (parameterized Thoth + Echo) |
| 20 | NEW | Extract "Department Decorator" meta-agent |
| 21 | NEW | Extract "Department Finder" meta-agent |
| 22 | NEW | Extract "Department Coach" meta-agent |
| 23 | NEW | Extract "Role Finder" meta-agent |
| 24 | NEW | Extract "Role Researcher" meta-agent |
| 25 | NEW | Extract "Role Decorator" meta-agent |

---

## From DEMIURGE roadmap (Phase 4 — Scale all departments)

Per `ROADMAP-DEPT-EXPANSION.md`, 1 session per dept in order:

| # | Dept | Trigger / Why now |
|---|---|---|
| 26 | Operations | Phase 2 reference build |
| 27 | Engineering | Revenue stack needs eng support |
| 28 | Finance & Legal | First paying customers require invoicing |
| 29 | AI Ops | Agent layer grows, needs dedicated ops |
| 30 | Customer Success | After first 5 recurring clients |
| 31 | RevOps | After $2K MRR |
| 32 | Research | Ongoing — knowledge backbone |
| 33 | People | After first FTE |
| 34 | Compliance | After first EU client |
| 35 | Knowledge Mgmt | After 100+ source files |
| 36 | Product Management | When roadmap has >3 parallel tracks |
| 37 | Data Science | When data volume justifies |
| 38 | Business Development | First partnership deal |
| 39 | Design / Creative | First design hire |
| 40 | Executive Office | When >5 active depts need coordination |
| 41+ | PMO, Field Services, etc. | On trigger |

---

## From active sprint gaps (incomplete tickets need completion)

| # | Ticket | What's needed |
|---|---|---|
| 42 | DEMIURGE-008 | Domain model review gate (markers missing → complete) |
| 43 | DEMIURGE-015 | Sprint 1 review gate |
| 44 | DEMIURGE-033 | Marketing dept activation review (close-out) |
| 45 | DEMIURGE-041 | Sales dept activation review (close-out) |
| 46 | DEMIURGE-047 | Sales department activation review |
| 47 | DEMIURGE-054 | Observation window definition (close-out) |
| 48 | DEMIURGE-068 | First sprint definition (close-out) |
| 49 | DEMIURGE-069 | Create ticket (currently missing files) |
| 50 | DEMIURGE-083 | Create ticket (currently missing files) |

---

## From agent naming cleanup

| # | Action | Notes |
|---|---|---|
| 51 | Migrate all 23 heritage agents to DEMIURGE standard | Need full PROMPT.md + agent.yaml + repo-manifest.yaml per agent |
| 52 | Decide: keep portmanteau names alongside Greek names, or fully replace? | User choice |
| 53 | Update DEPT-AGENTS-ROLES-COMPLETE.md as agents migrate | Keep in sync |
| 54 | Delete legacy `agents-prompts/` directory once all migrated | Cleanup |

---

## From `agents/` legacy repo (agent-infra)

| # | Action | Notes |
|---|---|---|
| 55 | Sync ORG-AGENTS.md to v0.3.0 (current says v0.2.0 in charter, but 3 new agents exist) | 47 → 47+3 = 50 agents |
| 56 | Add 3 new v0.3.0 engineering agents to handoff matrix: scope-intake, delivery-tracker, feasibility-gate | |
| 57 | Decide on Tier 2 cross-cutting concerns mapping (8 already in agent-infra handoff matrix) | |

---

## From `growth-coaching` DEPT CHARTER updates

| # | Action |
|---|---|
| 58 | Update `constitution/01-operations.md` to reflect DEMIURGE Operations dept (Kronos as lead) |
| 59 | Update `constitution/02-finance-legal.md` to add DEMIURGE Kronos overlap or note Kronos is for finance |
| 60 | Update `constitution/03-sales-growth.md` to reflect 3 DEMIURGE sales agents (Apollo, Cadmus, Metis) |
| 61 | Update `constitution/04-engineering-delivery.md` to clarify v0.3.0 vs DEMIURGE agent boundary |
| 62 | Update `constitution/05-research-education.md` to reference DEMIURGE Thoth + Hephaestus overlap |
| 63 | Update `constitution/06-people-culture.md` to mention DEMIURGE Echo + Iris as community scouts |

---

## From repo hygiene / cleanup

| # | Action | Notes |
|---|---|---|
| 64 | Decide what to do with the v1-legacy `agents/` repo now that DEMIURGE is canonical | Archive? Merge? Keep for cron jobs? |
| 65 | Clean up PHASE-* docs (PHASE-0 through PHASE-25) — superseded by DEMIURGE work | Mark as historical or delete |
| 66 | Migrate PACKAGE-INDEX.md (currently orphaned from DEMIURGE structure) | Replace with demiurge/agents/README.md |
| 67 | Standardize all `agents-prompts/*.md` files (some say "Erebus Agent" which is wrong) | Should be the named agent |
| 68 | Add CODEOWNERS to growth-coaching (currently missing) | Each dept needs an owner |

---

## From MCP and integrations

| # | Action |
|---|---|
| 69 | Verify all 16 MCP integrations still working post-merge |
| 70 | Document MCP server ownership (which agent owns which MCP) |
| 71 | Test `hermes-router-revenue` against actual Hermes routing |

---

## From tests + eval

| # | Action |
|---|---|
| 72 | Run all 23 tests in `tests/` against the merged code (need to verify nothing broke) |
| 73 | Add eval-gate for the new DEMIURGE agents (24 active agents need eval criteria) |
| 74 | Add chaos test for `hermes-router-revenue` (the new router) |
| 75 | Add integration tests for the document intelligence pipeline (Orpheus → Themis → ... → Pheme) |

---

## From sources + content

| # | Action |
|---|---|
| 76 | Verify all 22 source files in `sources/` are properly catalogued |
| 77 | Add Latam seed sources (Paraguay, Argentina, Brazil) for LATAM growth |
| 78 | Add Spanish-language coaching source catalog |

---

## From prompts + patterns

| # | Action |
|---|---|
| 79 | Document the `prompts/PROMPT-TEMPLATE.md` if it exists as a reusable template |
| 80 | Promote the 8 `patterns/` to a `_patterns/` library in agent-infra |
| 81 | Wire the trademark-scrub pattern to pre-commit hook |
| 82 | Wire the secret-leak-check pattern to pre-commit hook |

---

## From community + revenue stack

| # | Action |
|---|---|
| 83 | Verify the 8 community files in `community/` are valid LATAM-targeted materials |
| 84 | Translate remaining English content to Spanish (es-py) |
| 85 | Add Dutch (nl) variant per coaching service tier |

---

## From monitoring + observability

| # | Action |
|---|---|
| 86 | Wire `argus-health-monitor` to Prometheus or similar metrics |
| 87 | Add Grafana dashboard for the 24 DEMIURGE agents |
| 88 | Set up alerting on `hermes-router-revenue` failures |

---

## From runbooks + operations

| # | Action |
|---|---|
| 89 | Runbook: what to do when an agent's cron stops |
| 90 | Runbook: how to add a new DEMIURGE agent |
| 91 | Runbook: how to migrate a heritage agent to DEMIURGE |
| 92 | Runbook: what to do when a hard-stop fires |

---

## From schema + state

| # | Action |
|---|---|
| 93 | Add agent.yaml schema doc (formal spec) |
| 94 | Add repo-manifest.yaml schema doc |
| 95 | Add signal schema doc (per DEMIURGE-007) |
| 96 | Add router schema doc (per DEMIURGE-005) |
| 97 | Add quorum schema doc (per DEMIURGE-005) |

---

## From backups + data lifecycle

| # | Action |
|---|---|
| 98 | Add automated backup of all DEMIURGE state files |
| 99 | Add retention policy (how long to keep old outbox files) |
| 100 | Add disaster recovery runbook |

---

## From monitoring cron

| # | Action |
|---|---|
| 101 | Wire cron-store drift detector (existing cron-sync.sh + hook) |
| 102 | Wire state-validate.py on every cron tick |
| 103 | Wire org-state.json freshness check (warn if >5 min stale) |

---

## From agent-infra / growth-coaching unification

| # | Action |
|---|---|
| 104 | Decide: merge agent-infra into growth-coaching, or keep as separate repos? |
| 105 | If kept separate: bidirectional state-sync between them |
| 106 | If merged: what's the migration path for 1500+ cron outbox files |

---

## Dogfood / meta improvements

| # | Action |
|---|---|
| 107 | Use DEMIURGE itself to manage DEMIURGE work (Kronos runs ops on the ops team) |
| 108 | Add eval-gate to DEMIURGE-081 (knowledge-mgmt wiring) — score every migration |
| 109 | Self-running-check should verify all 24 DEMIURGE agents produce expected output |

---

## Business / revenue work

| # | Action |
|---|---|
| 110 | Get first paying customer (per DEMIURGE-068) |
| 111 | Convert Latam seed to first 5 leads |
| 112 | Close M-tier GROW coaching at $500/mo |
| 113 | Onboard first customer via `coach-onboarding` |

---

## Tier 3 + 4 dept promotion triggers (waiting)

These auto-trigger as the org hits size:

| # | Trigger | Becomes |
|---|---|---|
| 114 | 5+ recurring clients | Customer Success dept |
| 115 | >$2K/mo marketing OR 10+ clients | Marketing (independent) dept |
| 116 | Active vendors > 10 OR SaaS spend > $1K/mo | Procurement (independent) dept |
| 117 | First EU client OR $50K MRR (HARD-STOP) | Compliance (standalone) dept |
| 118 | First external investor | Investor Relations dept |
| 119 | Ivan coord hours > 50/week | Chief of Staff dept |
| 120 | $100K+ cash OR debt instruments | Treasury dept |
| 121 | $1M+ revenue | Internal Audit dept |
| 122 | Ship consumer AI product | Trust & Safety dept |
| 123 | ParaguAI Builder has public API | DevRel dept |
| 124 | Open physical office | Workplace Operations dept |
| 125 | $500K+ payment volume | Fraud / Risk dept |
| 126 | 10+ employees | Compensation & Benefits dept |
| 127 | First FTE hire | People Operations (HR) dept |
| 128 | 10+ employees | DEI / Belonging dept |
| 129 | Launch flagship brand | Public Relations dept |
| 130 | Regulated vertical | Government Relations dept |
| 131 | 50+ people | Internal Communications dept |
| 132 | Acquisitions planned | M&A / Corp Dev dept |
| 133 | Data-driven product | Chief Data Officer dept |
| 134 | Enterprise AI | Chief AI Officer dept |
| 135 | 25+ employees | Diversity & Inclusion Lead dept |

---

## Summary

- **Critical (P0)**: 5 items (75 min)
- **DEMIURGE Phase 1 (current)**: 6 items (~5 hr)
- **DEMIURGE Phase 2 (Operations)**: 5 items, 3 done, 2 partial
- **DEMIURGE Phase 3 (Meta-agents)**: 9 items
- **DEMIURGE Phase 4 (Scale)**: 16 items (1 session each)
- **Sprint gap completion**: 9 items
- **Naming cleanup**: 4 items
- **Legacy repo sync**: 3 items
- **Charter updates**: 6 items
- **Repo hygiene**: 5 items
- **MCP/integrations**: 3 items
- **Tests + eval**: 4 items
- **Sources + content**: 3 items
- **Prompts + patterns**: 4 items
- **Community + revenue**: 3 items
- **Monitoring + observability**: 3 items
- **Runbooks**: 4 items
- **Schema + state**: 5 items
- **Backups + data lifecycle**: 3 items
- **Cron monitoring**: 3 items
- **Agent-infra / growth-coaching unification**: 3 items
- **Dogfood / meta**: 3 items
- **Business / revenue**: 4 items
- **Tier 3/4 triggers (waiting)**: 22 items

**Total: 135 wishlist items**, organized by source and priority.

**Immediate priority** (this week): items 1-5 (P0 secrets) + items 6-11 (DEMIURGE Phase 1) + item 51 (start heritage agent migration).

**Medium-term** (next sprint): items 12-50 (complete Phase 2/3, finish sprint gaps).

**Long-term** (next quarter): items 51-135 (cleanup, scale, business triggers).

---

## Reference

- `/opt/data/scratchpad/analysis/DEPT-AGENTS-ROLES-COMPLETE.md` — canonical roster (DEMIURGE + heritage + Tier 2/3/4)
- `/opt/data/scratchpad/analysis/P0-ACTION-CHECKLIST.md` — operator action checklist
- `/opt/data/scratchpad/analysis/P0-SECURITY-ADVISORY.md` — security leaks detail
- `github.com/Ai-Whisperers/growth-coaching/tree/epic/DEMIURGE` — DEMIURGE branch (now merged into main)
- `github.com/Ai-Whisperers/growth-coaching/blob/main/ROADMAP-DEPT-EXPANSION.md` — DEMIURGE roadmap
- `github.com/Ai-Whisperers/growth-coaching/blob/main/tickets/` — 81 ticket dirs
