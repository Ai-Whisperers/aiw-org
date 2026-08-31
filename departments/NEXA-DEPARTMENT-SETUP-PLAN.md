# Nexa Paraguay — Complete Department + Agent Setup Plan

> **Status**: PLAN ONLY — do not implement until Ivan says **go**.
> **Prepared**: 2026-08-24 14:55 PYT
> **Author**: Erebus (autonomous planning per Ivan's two-phase directive)
> **Audience**: Ivan (CEO), Kyrian (CTO), Luana (content/operations), Sonia (Nexa founder)
> **Pattern source**: AIW agent-org-framework v0.2.0 + coaching-vertical-run Pattern C/D reference

---

## 0. Confirmations (decisions baked into this plan)

| # | Decision | Source | Locked? |
|---|---|---|---|
| D1 | **`nexaparaguay.com.py` is the canonical host** | Ivan directive 2026-08-24 | ✅ Yes |
| D2 | `/es/casos` should redirect to `/es/casos-de-exito#main-content` | Ivan directive 2026-08-24 | ✅ Yes (technical detail surfaced for Phase 2) |
| D3 | `nexa-paraguay` private repo holds research; `paragu-ai-platform/apps/nexa-paraguay/` is deployable | `apps/nexa-paraguay/README.md` | ✅ Pre-existing |
| D4 | No new "Nexa Inc." legal entity — Nexa is a client of AI Whisperers, not a sub-org | Org constitution v0.2.0 | ✅ Yes |
| D5 | We extend the AIW 6-dept + 8-cross-cutting model; we do NOT fork a parallel org | Org constitution v0.2.0 | ✅ Yes |
| D6 | All Nexa agents follow `/opt/data/agents-v2/prompts/PROMPT-TEMPLATE.md` v0.2.0 (12-section, 5 mandatory patterns) | Pre-existing | ✅ Yes |
| D7 | Model rule: every Nexa agent runs `model: reasoning`, `provider: litellm` | `ai-run-org-playbook` § "Model selection" | ✅ Yes |
| D8 | No auto-commit/push to `Ai-Whisperers/nexa-paraguay` (private); agents read the mirror only | `aiw-management-agents` § "Don't do" + README | ✅ Yes |
| D9 | Trademark banlist enforced on every Nexa public-facing file | Memory entry 2026-08-12 | ✅ Yes |
| D10 | No `$1,500` price leaks anywhere public | `CURRENT_STATE.md` | ✅ Yes — hard-stop on every agent |

---

## 1. Reading guide

1. **Why this is shaped this way** (departments, not sub-orgs) — §2
2. **What already runs for Nexa today** (the gap analysis) — §3
3. **The 18-agent manifest** (full table with cadence, owner, hard-stops) — §4
4. **Per-department what-changes-and-what-adds** — §5
5. **Tier-2 cross-cutting: Client Operations** (the new dept) — §6
6. **Phase 0 prerequisites** (the 3 things that must happen before any agent ships) — §7
7. **90-day build order** (12 agents across 6 phases) — §8
8. **Storage architecture** (per-agent git + SQLite + state.json) — §9
9. **Hard-stops manifest** (mechanical rules across all Nexa agents) — §10
10. **Eval-gate rules** (per-agent scoring) — §11
11. **Cost projection** (LLM + infra cost per agent per month) — §12
12. **Self-running declaration criteria** (Nexa-layer-specific) — §13
13. **PROMPT.md stubs** (one per agent, ~250 words each — see §14)
14. **Cron registration commands** (ready-to-paste bash) — §15
15. **Verification checklist** (must-pass before declaring Phase N done) — §16
16. **What I am NOT recommending** (the rejections) — §17
17. **Files this plan creates** (full inventory) — §18
18. **What I need from you** (the one question before "go") — §19

---

## 2. Why departments, not a separate org

Two reasons:

1. **Nexa has 1 client (Sonia) + 1 PT employee (Luana) + 1 internal founder advocate (Ivan)**. That is not large enough to sustain a 6-dept parallel org layer. The right shape is one **Nexa-tuned extension of the existing AIW agent layer**, where Nexa gets dedicated sub-agents inside the existing 6 departments plus one new Tier-2 cross-cutting department for client journey orchestration.

2. **The existing AIW agent layer already has 24 cron jobs, $0 marginal infra cost for adding sub-agents, and a battle-tested PROMPT template + eval-gate + storage architecture.** Fanning out a parallel org duplicates all of that for zero benefit.

So the architecture is:

```
AI Whisperers org (unchanged)
└── Nexa Paraguay client engagement (NEW — this plan)
    ├── Tier-1 dept extensions (6 existing depts gain Nexa sub-agents)
    └── Tier-2 cross-cutting: 07-nexa-client-operations (NEW dept file)
```

---

## 3. What already runs for Nexa today (the gap analysis)

### Already in place (untouched by this plan)

| What | Source | Owner today |
|---|---|---|
| Production site | `nexaparaguay.com.py` (Docker Swarm service `nexa-paraguay_web`, 2 replicas) | `devops-monitor` watches |
| Health check cron | `nexa-paraguay/scripts/health-check.sh` every 15 min | Generic `site-health` watchdog |
| Central CI | `.github/workflows/central.yml` filters `apps/nexa-paraguay/**` | Generic `engineering-roster` |
| Brand truth | `Ai-Whisperers/nexa-paraguay/docs/CURRENT_STATE.md` + `SOURCE_OF_TRUTH.md` | Manual / Luana |
| Compliance template | `src/compliance/aml-disclosure-nexa.template.md` (deployed, variables unfilled) | `compliance-monitor` (generic) |
| Lead capture (broken) | `/api/contact` + `/api/intake` + `/api/subscribe` → fall back to `console.log` | Nobody |
| Sales pipeline (generic) | `sales-pipeline` cron daily 09:00 + 12:00 PYT | Org-wide, not Nexa-tuned |
| Proposal drafter (generic) | `proposal-drafter` | Org-wide, not Nexa-tuned |
| Content production (generic) | `marketing-content-mon-wed-fri` | Org-wide, not Nexa-tuned |
| Brand assets archive | `public/_archive-images/` (139 MB), `public/_archive-sites/` (5 MB) | Untouched |

### The 8 gaps (and which agent closes each)

| # | Gap today | Agent that closes it (this plan) |
|---|---|---|
| G1 | Canonical host still says `nexaparaguay.com` in some places; DNS apex is parked at Shopify | `nexa-canonical-host-enforcer` |
| G2 | 4 orphan pricing pages (`/es/empresa /lifestyle /trust /inversor`) serve empty 200s | `nexa-orphan-page-killer` |
| G3 | `$1,500` price could leak into any deploy, sitemap, schema, image alt | `nexa-pricing-guard` |
| G4 | `/api/contact` + `/api/intake` write to Docker volumes; nobody follows up | `nexa-client-journey-agent` |
| G5 | No Nexa-specific lead scoring — generic sales-pipeline doesn't know "Dutch family relocating" | `nexa-icp-engine` |
| G6 | No Dutch market prospecting — Sonia's audience is Dutch/DE families, but the agent layer doesn't know | `nexa-dutch-market-scout` |
| G7 | No content integrity audit — site content drifts vs `content/{es,en,nl,de}.json` | `nexa-content-freshness` |
| G8 | No claim validation — stale macro stats (PIB growth, EU expat numbers) on the site go unchecked | `nexa-claim-validator` |

---

## 4. The 18-agent manifest (the full roster)

| # | Agent name | Dept / Tier | Cadence (PYT) | Owner | Model | Class | Phase |
|---|---|---|---|---|---|---|---|
| 01 | `nexa-pricing-guard` | 02-Finance | Daily 08:00 | Ivan | reasoning | FULL_AGENT | P1 |
| 02 | `nexa-orphan-page-killer` | 04-Engineering | Daily 08:30 | Kiki | reasoning | FULL_AGENT | P1 |
| 03 | `nexa-canonical-host-enforcer` | 04-Engineering | Daily 09:00 | Kiki | reasoning | FULL_AGENT | P1 |
| 04 | `nexa-content-freshness` | 01-Operations | Weekly Mon 10:00 | Luana | reasoning | FULL_AGENT | P2 |
| 05 | `nexa-claim-validator` | 05-Research | Weekly Wed 14:00 | Ivan | reasoning | FULL_AGENT | P2 |
| 06 | `nexa-build-monitor` | 04-Engineering | on-commit (paths-filter) | Kiki | reasoning | FULL_AGENT | P2 |
| 07 | `nexa-aml-monitor` | 02-Finance | Daily 11:00 + 17:00 | Ivan | reasoning | FULL_AGENT | P3 |
| 08 | `nexa-partner-registry` | 02-Finance | Weekly Fri 16:00 | Ivan | reasoning | FULL_AGENT | P3 |
| 09 | `nexa-client-invoicing` | 02-Finance | on-event (when client closes) | Ivan | reasoning | FULL_AGENT | P3 |
| 10 | `nexa-client-journey-agent` | 07-Client-Ops (NEW) | Daily 09:00 + on-event | Sonia/Ivan | reasoning | FULL_AGENT | P3 |
| 11 | `nexa-day1-protocol` | 07-Client-Ops | on-event (D0) | Sonia | reasoning | FULL_AGENT | P3 |
| 12 | `nexa-residency-tracker` | 07-Client-Ops | Weekly Tue 11:00 | Sonia | reasoning | FULL_AGENT | P3 |
| 13 | `nexa-icp-engine` | 03-Sales | Daily 09:00 (replaces generic slot) | Ivan | reasoning | FULL_AGENT | P4 |
| 14 | `nexa-dutch-market-scout` | 03-Sales | Daily 11:00 | Ivan | reasoning | FULL_AGENT | P4 |
| 15 | `nexa-proposal-drafter` | 03-Sales | on-event (after ICP score ≥ 7) | Ivan | reasoning | HITL_AGENT | P4 |
| 16 | `nexa-funnel-tracker` | 03-Sales | Weekly Mon 09:00 | Ivan | reasoning | FULL_AGENT | P5 |
| 17 | `nexa-content-engine` | 03-Sales | Weekly Wed 10:00 | Luana | reasoning | FULL_AGENT | P5 |
| 18 | `nexa-testimonial-curator` | 06-People | Quarterly | Sonia | reasoning | HITL_AGENT | P5 |

**Totals**: 18 new agents, 16 cron jobs (06 + 10 + 12 + 13 + 14 + 16 + 17 are cron; 09 + 11 + 15 are on-event).

**Model**: all `reasoning` per `ai-run-org-playbook` § "Model selection" (multi-tool batch every run).

**Fallback**: `litellm/primary` (Cerebras gpt-oss-120b) — never `MiniMax-M3` (silent 402).

---

## 5. Per-department what-changes-and-what-adds

### Department 1 — Operations (additions)

**New PROMPT.md files**:
- `/opt/data/agents/nexa-content-freshness/PROMPT.md`

**Modified**: `/opt/data/agents/departments/01-operations.md` — add Nexa sub-agent row + handoff matrix entries.

**State files added**:
- `/opt/data/agents/state/nexa-content-freshness.json`

**Business-analyst extension**: append a Nexa KPI block to the daily 06:30 brief (site traffic by locale, lead conversions, $/lead, retention).

### Department 2 — Finance & Legal (additions)

**New PROMPT.md files**:
- `/opt/data/agents/nexa-pricing-guard/PROMPT.md`
- `/opt/data/agents/nexa-aml-monitor/PROMPT.md`
- `/opt/data/agents/nexa-partner-registry/PROMPT.md`
- `/opt/data/agents/nexa-client-invoicing/PROMPT.md`

**Modified**: `/opt/data/agents/departments/02-finance-legal.md` — same as #1.

**State files added**:
- `/opt/data/agents/state/nexa-pricing-guard.json`
- `/opt/data/agents/state/nexa-aml-monitor.json`
- `/opt/data/agents/state/nexa-partner-registry.json`
- `/opt/data/agents/state/nexa-client-invoicing.json`
- `/opt/data/db/nexa-clients.db` (SQLite — client ledger)
- `/opt/data/db/nexa-partners.db` (SQLite — referral network)

### Department 3 — Sales & Growth (heaviest additions)

**New PROMPT.md files**:
- `/opt/data/agents/nexa-icp-engine/PROMPT.md`
- `/opt/data/agents/nexa-dutch-market-scout/PROMPT.md`
- `/opt/data/agents/nexa-proposal-drafter/PROMPT.md`
- `/opt/data/agents/nexa-funnel-tracker/PROMPT.md`
- `/opt/data/agents/nexa-content-engine/PROMPT.md`

**Modified**: `/opt/data/agents/departments/03-sales-growth.md` — add the 5 Nexa ICPs (Dutch family / DE family / NL investor / BE family / Iberian-Portuguese family) with budget bands per `marketing-strategy/playbook.md`.

**State files added**:
- `/opt/data/agents/state/nexa-icp-engine.json`
- `/opt/data/agents/state/nexa-dutch-market-scout.json`
- `/opt/data/agents/state/nexa-funnel-tracker.json`
- `/opt/data/agents/state/nexa-content-engine.json`
- `/opt/data/db/nexa-leads.db` (SQLite — inbound + outbound leads)
- `/opt/data/db/nexa-content-calendar.db` (SQLite — what we published when)

**Generic `proposal-drafter` vs Nexa-specific**: the Nexa proposal-drafter does NOT inherit the generic rate card — Nexa has no published price, no tiered packages, and a Dutch-default voice. Separate PROMPT.

### Department 4 — Engineering & Delivery (additions)

**New PROMPT.md files**:
- `/opt/data/agents/nexa-orphan-page-killer/PROMPT.md`
- `/opt/data/agents/nexa-canonical-host-enforcer/PROMPT.md`
- `/opt/data/agents/nexa-build-monitor/PROMPT.md`

**Modified**: `/opt/data/agents/departments/04-engineering-delivery.md` — same.

**State files added**:
- `/opt/data/agents/state/nexa-orphan-page-killer.json`
- `/opt/data/agents/state/nexa-canonical-host-enforcer.json`
- `/opt/data/agents/state/nexa-build-monitor.json`

**`nexa-build-monitor`** is special: it runs as a GitHub Actions workflow (not a cron), triggered by `paths-filter` on `apps/nexa-paraguay/**`. It runs typecheck → lint → build → image tag, and fails the deploy if any of the 3 currently-bypassed gates (`|| true`) fail. This is the only Nexa agent that lives in CI rather than cron.

### Department 5 — Research & Education (additions)

**New PROMPT.md files**:
- `/opt/data/agents/nexa-claim-validator/PROMPT.md`

**Modified**: `/opt/data/agents/departments/05-research-education.md` — same.

**State files added**:
- `/opt/data/agents/state/nexa-claim-validator.json`

### Department 6 — People & Culture (addition)

**New PROMPT.md files**:
- `/opt/data/agents/nexa-testimonial-curator/PROMPT.md`

**Modified**: `/opt/data/agents/departments/06-people-culture.md` — add Sonia + Luana to bandwidth map; add testimonial ritual to cultural artifacts.

**State files added**:
- `/opt/data/agents/state/nexa-testimonial-curator.json`

---

## 6. Tier-2 cross-cutting: 07-nexa-client-operations (NEW dept)

### Why this is a new dept file, not just a sub-agent

The client journey (inquiry → D0 → D+90 → D+180 → yearly anniversary) is **not owned by any existing department**:

- Sales stops at proposal close
- Operations doesn't know about per-client state
- Finance bills but doesn't orchestrate
- Engineering runs the site but doesn't know clients

So we create a 7th department file (`07-nexa-client-operations.md`) that owns the entire client lifecycle. It's still Tier-2 cross-cutting in the matrix (single-client today), but it's structurally a department.

### Department file location

`/opt/data/agents/departments/07-nexa-client-operations.md`

### Department charter

```
Mission: Orchestrate every Nexa client's journey from first WhatsApp ping to yearly anniversary.

Head: Sonia (founder/operator)
Lead agent: nexa-client-journey-agent (daily 09:00 PYT + on-event)
Sub-agents:
  - nexa-day1-protocol (on D0)
  - nexa-residency-tracker (weekly)
  - nexa-client-invoicing (on-event, also reports to Finance)
  - nexa-testimonial-curator (quarterly, also reports to People)

State files:
  - state/nexa-clients.json (master client ledger, capped 100 clients)
  - db/nexa-clients.db (per-client state, queryable)

Decision rights:
  - Send WhatsApp template acknowledgement → agent (Sonia approves template library)
  - Send personalised WhatsApp reply → HUMAN_ONLY (Sonia/Luana)
  - Close a client → Sonia (signed in next brief)
  - Promote client from inquiry → onboarding → residency → post-residency → anniversary → HITL_AGENT (state-transition requires human)
```

### PROMPT.md files for this dept

- `/opt/data/agents/nexa-client-journey-agent/PROMPT.md`
- `/opt/data/agents/nexa-day1-protocol/PROMPT.md`
- `/opt/data/agents/nexa-residency-tracker/PROMPT.md`

### Promotion trigger

The 07 dept stays Tier-2 (cross-cutting single-client) until one of:
- 5+ active clients in the journey at once (today: 0-2)
- A second full-time operator (Luana promoted beyond content)
- Sonia adds a second service vertical (e.g. business incorporation as a paid add-on)

When triggered: promote to Tier-1 in `ORG-AGENTS.md`.

---

## 7. Phase 0 prerequisites (3 things that must happen before any agent ships)

Per the gap analysis from the prior session, **3 host-level decisions are blocking every Nexa agent**. Until they're resolved, every agent fires on stale assumptions.

### P0.1 — Canonical host cutover

**Current state**:
- `nexaparaguay.com.py` returns 200 with the working site
- `nexaparaguay.com` returns 402 (Shopify parking page)
- Code/SEO metadata: `nexaparaguay.com.py` ✅
- README badges: `nexaparaguay.com` ❌
- Sonia's email signature: unknown (likely `.com`) ❌

**What to do**:
1. Update `apps/nexa-paraguay/README.md` line 9-23: replace `.com` aliases with `.com.py`
2. Update `apps/nexa-paraguay/site.json`: `domain: nexaparaguay.com.py` (already), `publicUrl: https://nexaparaguay.com.py` (already), remove `.com` from `alternateDomains`
3. Update Sonia's email signature (manual — Luana)
4. Update LinkedIn URL on the company page (manual — Luana)
5. Update Instagram bio (manual — Luana)
6. Add Traefik labels in `docker-compose.yml` if needed (Kiki)
7. Update Search Console to use `.com.py` as the canonical property (manual — Ivan)
8. Remove the `nexa-preview` Docker service preview alias from any `.com` references

**Files touched**:
- `apps/nexa-paraguay/README.md`
- `apps/nexa-paraguay/site.json`
- `apps/nexa-paraguay/docker-compose.yml`
- `apps/nexa-paraguay/src/app/sitemap.ts` (if it still emits `.com`)
- `apps/nexa-paraguay/src/lib/seo.ts`
- `apps/nexa-paraguay/public/robots.txt`

**Verification**:
```bash
# All canonical URLs across the repo point to .com.py
cd /opt/data/work/research-repos/paragu-ai-platform
grep -r "nexaparaguay\.com\b" apps/nexa-paraguay/src apps/nexa-paraguay/site.json apps/nexa-paraguay/public 2>/dev/null | grep -v node_modules
# Expected output: empty (no naked .com references; only .com.py allowed)
```

**Owner**: Ivan + Kiki + Luana (split above). **Estimated time**: 1 hour total, including Search Console.

### P0.2 — 4 orphan pricing pages: 410 or 301 to /servicios

**Current state**: `/es/empresa`, `/es/lifestyle`, `/es/trust`, `/es/inversor` all return HTTP 200 with empty shells (content was stripped 2026-06-15 per `NEXA_DECISIONS.md` Q1.1A, but the route configs were never deleted).

**What to do**:
1. Delete the 4 JSON configs from `apps/nexa-paraguay/nexa-pages/`:
   - `lifestyle.json`, `empresa.json`, `trust.json`, `inversor.json`
2. Delete the matching JSON blocks from `apps/nexa-paraguay/content/{es,en,nl,de}.json`
3. Replace the 4 catch-all pages in `apps/nexa-paraguay/src/app/[locale]/[slug]/page.tsx` with a check: if slug in [`empresa`, `lifestyle`, `trust`, `inversor`], `redirect('/' + locale + '/servicios', 301)`. Alternative: return `notFound()` which yields 404, but 301 preserves SEO equity better.
4. Test: `curl -I https://nexaparaguay.com.py/es/empresa` → 301 with `Location: /es/servicios`

**Files touched**:
- `apps/nexa-paraguay/nexa-pages/{empresa,lifestyle,trust,inversor}.json` (delete)
- `apps/nexa-paraguay/content/{es,en,nl,de}.json`
- `apps/nexa-paraguay/src/app/[locale]/[slug]/page.tsx`

**Verification**:
```bash
for slug in empresa lifestyle trust inversor; do
  curl -sI "https://nexaparaguay.com.py/es/$slug" | head -1
done
# Expected: 301 for all 4
```

**Owner**: Kiki (code) + Ivan (approval). **Estimated time**: 30 min.

### P0.3 — /es/casos → /es/casos-de-exito#main-content redirect

**Current state**: `/es/casos` returns 200 with the wrong page (the same generic "Servicios" shell as other orphan routes). Sonia wants it to redirect to the actual casos-de-exito page (which exists at 200, serving the testimonials hub).

**What to do**:
1. In `apps/nexa-paraguay/src/app/[locale]/[slug]/page.tsx`: add slug check for `casos`, redirect to `/${locale}/casos-de-exito#main-content` with 301.
2. Test: `curl -I https://nexaparaguay.com.py/es/casos` → 301 with `Location: /es/casos-de-exito#main-content`
3. Verify `main-content` ID exists on the destination page (the page's main wrapper should have `id="main-content"` for the fragment to scroll correctly).

**Files touched**:
- `apps/nexa-paraguay/src/app/[locale]/[slug]/page.tsx`
- `apps/nexa-paraguay/src/app/[locale]/casos-de-exito/page.tsx` (verify `id="main-content"` exists)

**Verification**:
```bash
curl -sI "https://nexaparaguay.com.py/es/casos" | head -3
# Expected: 301, Location: /es/casos-de-exito#main-content

curl -sSL "https://nexaparaguay.com.py/es/casos-de-exito" | grep -o 'id="main-content"' | head -1
# Expected: id="main-content"
```

**Owner**: Kiki. **Estimated time**: 15 min.

### Phase 0 done = ready for Phase 1

All three P0 items ship in **one deploy**, ~2 hours total wall-clock. Until they're live, every Nexa agent ships into an environment with contradictory SEO metadata and orphan 200s — the agents will keep firing loud alerts and the dashboards will look red.

---

## 8. 90-day build order (12 agents across 6 phases)

Phases are sized per `ai-run-org-playbook` § "AI-timeline assumptions are not human-timeline" — each phase fits in **1-2 AI sessions of ~90 turns**.

### Phase 1 — P1 hygiene ops (3 agents, days 1-7)

**Goal**: prove the agent model works on Nexa before any client-facing agent.

| # | Agent | Cron expr (PYT) | Wall-clock | New files |
|---|---|---|---|---|
| 1 | `nexa-pricing-guard` | `0 8 * * *` (08:00 daily) | 30 min | PROMPT.md + state.json + scan script |
| 2 | `nexa-orphan-page-killer` | `30 8 * * *` (08:30 daily) | 30 min | PROMPT.md + state.json + scan script |
| 3 | `nexa-canonical-host-enforcer` | `0 9 * * *` (09:00 daily) | 30 min | PROMPT.md + state.json + scan script |

**Phase 1 deliverable**: 3 cron jobs live, each firing daily. Outbox shows:
- `nexa-pricing-guard` → "0 leaks found" or "1 leak at /es/sitemap.xml line 47"
- `nexa-orphan-page-killer` → "0 orphans" or "1 orphan still 200: /es/empresa"
- `nexa-canonical-host-enforcer` → "All canonical URLs use .com.py" (after P0.1 ships)

**Phase 1 done criteria**:
- All 3 cron jobs register without error
- Each delivers a brief within 24h of registration
- `health.sh` reports green for all 3

### Phase 2 — Content + engineering quality (3 agents, days 8-21)

| # | Agent | Cadence | Wall-clock |
|---|---|---|---|
| 4 | `nexa-content-freshness` | `0 10 * * 1` (Mon 10:00 weekly) | 90 min |
| 5 | `nexa-claim-validator` | `0 14 * * 3` (Wed 14:00 weekly) | 90 min |
| 6 | `nexa-build-monitor` (CI workflow, not cron) | on every commit to `apps/nexa-paraguay/**` | 120 min |

**Phase 2 done criteria**:
- 4 weeks of clean content-freshness briefs (no missing-locale drift)
- 4 weeks of claim-validator briefs (stale stats flagged before they ship)
- 1+ green build via the new `nexa-build-monitor` workflow

### Phase 3 — Operations core (3 agents, days 22-45)

| # | Agent | Cadence | Wall-clock |
|---|---|---|---|
| 7 | `nexa-aml-monitor` | `0 11 * * *` + `0 17 * * *` (twice daily) | 60 min |
| 8 | `nexa-partner-registry` | `0 16 * * 5` (Fri 16:00 weekly) | 60 min |
| 9 | `nexa-client-journey-agent` | `0 9 * * *` + on-event (D0 etc) | 180 min (most complex) |
| 10 | `nexa-day1-protocol` | on-event (D0) | 90 min |
| 11 | `nexa-residency-tracker` | `0 11 * * 2` (Tue 11:00 weekly) | 90 min |
| 12 | `nexa-client-invoicing` | on-event (client closes) | 60 min |

**Phase 3 done criteria**:
- 1+ real client goes through the full journey (D-30 → D+90)
- Every state transition logged to `nexa-clients.db`
- Sonia confirms: "I'm not doing client coordination on WhatsApp anymore, the agent is"

### Phase 4 — Sales engine (3 agents, days 46-60)

| # | Agent | Cadence | Wall-clock |
|---|---|---|---|
| 13 | `nexa-icp-engine` | `0 9 * * *` (replaces generic sales slot) | 90 min |
| 14 | `nexa-dutch-market-scout` | `0 11 * * *` (daily) | 120 min |
| 15 | `nexa-proposal-drafter` | on-event (HITL) | 90 min |

**Phase 4 done criteria**:
- 10+ leads scored by ICP engine
- 1+ outbound proposal drafted and reviewed by Ivan
- Conversion funnel baseline established

### Phase 5 — Growth + retention (3 agents, days 61-75)

| # | Agent | Cadence | Wall-clock |
|---|---|---|---|
| 16 | `nexa-funnel-tracker` | `0 9 * * 1` (Mon 09:00 weekly) | 60 min |
| 17 | `nexa-content-engine` | `0 10 * * 3` (Wed 10:00 weekly) | 120 min |
| 18 | `nexa-testimonial-curator` | `0 14 1 1,4,7,10 *` (quarterly) | 60 min |

**Phase 5 done criteria**:
- 1 quarterly brief from `nexa-testimonial-curator` (with consent, not fabricated)
- Funnel math: `$ revenue / lead` baseline established
- 1 blog post + 1 LinkedIn carousel published via `nexa-content-engine`

### Phase 6 — Tune + self-running declaration (days 76-90)

No new agents. Activities:
- Tune cron cadences based on 60+ days of brief history
- Fill in eval-gate rules per agent (see §11)
- Run `/opt/data/agents-v2/scripts/self-running-check.py` for 7 consecutive days
- Write `/opt/data/agents/departments/NEXA-AGENT-LAYER-SELF-RUNNING.md` declaring v1.0.0

---

## 9. Storage architecture (3-layer per agent)

Per `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md`:

| Layer | Use | Nexa path |
|---|---|---|
| **L1: JSON** | Config + lightweight state + last-run + cap lists | `/opt/data/agents/state/nexa-*.json` |
| **L2: SQLite** | Queryable per-entity state (clients, leads, partners, claims) | `/opt/data/db/nexa-clients.db`, `/opt/data/db/nexa-leads.db`, `/opt/data/db/nexa-partners.db`, `/opt/data/db/nexa-claims.db` |
| **L3: Per-agent git repo** | Versioned memory, decision log, post-mortems | `/opt/data/git-repos/aiw-nexa-*/` (NOT auto-created) |

**L3 carve-out**: per the `ai-run-org-playbook` § "Don't do", L3 repos are NOT auto-created. After Phase 3 ships and the agent layer proves itself, Ivan approves creating `/opt/data/git-repos/aiw-nexa-agent-memory.git` and the daily `state.json` snapshots start committing there.

**Backup policy** (existing cron, covers all L2 DBs):
- `aiw-db-snapshot-daily` (02:00 PYT daily) — sqlite3 `.backup` to `/opt/data/state/snapshots/YYYY-MM-DD/`
- 90-day retention, R2 offsite weekly
- `aiw-state-snapshot-6h` — state/*.json rolled forward

---

## 10. Hard-stops manifest (mechanical rules across all 18 Nexa agents)

Every Nexa PROMPT.md must include this YAML block:

```yaml
hard_stops:
  # Trademark banlist (mechanical, no exceptions)
  - name: trademark_banlist
    description: never write banned brand tokens to any public surface
    enforcement: trademark-scrub.sh pre-write
    approved_human: ivan

  # Price leak prevention
  - name: price_privacy
    description: never publish "$1,500" or any numeric price in public artifacts
    scope: all PROMPT.md outputs that touch sitemap, schema.org, alt text, public pages
    approved_human: ivan

  # Honesty discipline
  - name: no_fabrication
    description: never fabricate testimonials, stats, team members, or metrics
    scope: all content-producing agents
    approved_human: ivan

  # PII protection
  - name: pii_hard_stop
    description: client names, family data, financial info never leave nexaparaguay-* dbs or outbox summaries
    enforcement: pre-write PII filter
    approved_human: ivan

  # Private repo boundary
  - name: no_private_repo_writes
    description: read mirror at paragu-ai-platform/apps/nexa-paraguay/docs/ only; never write to Ai-Whisperers/nexa-paraguay
    enforcement: paths-filter + git remote guard
    approved_human: ivan

  # Public WhatsApp messages require Sonia
  - name: whatsapp_human_only
    description: send WhatsApp template acknowledgement OK; personalised reply = HUMAN_ONLY
    approved_human: sonia

  # Spend cap per decision
  - name: spend_cap
    description: USD 50 single-tool-call = no approval; USD 50-500 surface in next brief; > USD 500 Ivan approval; > USD 5000 Ivan+Kiki
    enforcement: cost-tracker.json per-tick
    approved_human: ivan
```

---

## 11. Eval-gate rules (per-agent scoring)

Per `/opt/data/agents-v2/eval-gate.py`, every Nexa agent's outbox brief is scored. Rules per agent family:

### `nexa-pricing-guard` eval rules

- [ ] Sections present: scan_summary, leaks_found, affected_paths, severity, fix
- [ ] Word count 150-300
- [ ] No false positives (every flagged "leak" must include a grep-extractable URL)
- [ ] Trademark scrub pass

### `nexa-orphan-page-killer` eval rules

- [ ] Lists all 4 known orphan slugs
- [ ] For each: current HTTP status, expected (301/410), action
- [ ] Status code verified via curl, not assumed

### `nexa-canonical-host-enforcer` eval rules

- [ ] Lists canonical/hreflang/sitemap/robots.txt sources
- [ ] For each: domain referenced, expected `.com.py`, current
- [ ] Mismatches counted

### `nexa-content-freshness` eval rules

- [ ] Locale parity check (es/en/nl/de each present + non-empty)
- [ ] Per-locale key-set diff vs canonical
- [ ] No `"$1,500"` substring in any locale
- [ ] No banned brand tokens

### `nexa-claim-validator` eval rules

- [ ] Each claim has source URL + retrieval date
- [ ] Stale (>12 months) flagged separately from wrong
- [ ] No aspirational headline language ("growing fast", "leading", etc.)

### `nexa-build-monitor` eval rules

- [ ] Workflow run status (pass/fail)
- [ ] Bypassed-gate count (current: 3 in next.config.js + lint/typecheck with `|| true`)
- [ ] Per-bypass: link to issue or justification

### `nexa-client-journey-agent` eval rules

- [ ] Active client count + state distribution (inquiry/onboarding/residency/post-residency/anniversary)
- [ ] Overdue check-ins (any client > 7 days since last agent action)
- [ ] WhatsApp template usage (template_id + recipient)
- [ ] PII filter pass (no client names in outbox text)

### `nexa-icp-engine` eval rules

- [ ] Per-lead score (0-10) with rubric
- [ ] NO price field in any output (price-privacy hard-stop)
- [ ] Tier (family / investor / other) explicit

### Generic (apply to all)

- [ ] Length within 80-120% of target
- [ ] Citation present (URL or file path) for every claim
- [ ] Trademark scrub pass
- [ ] No `"$1,500"` substring in any output that touches public surfaces
- [ ] No banned brand tokens
- [ ] At least 1 actionable item per brief

---

## 12. Cost projection (per agent per month)

Per `ai-run-org-playbook` § "Cost equation":

| Item | Estimate |
|---|---|
| Avg LLM cost per agent run (reasoning model, ~110s, multi-tool) | ~$0.05-0.20 per short brief |
| Avg runs/day per agent | 1 (most) to 2 (twice-daily aml-monitor) |
| Nexa-specific agents total | 16 cron + 1 CI + 1 quarterly |
| Daily cost (all 18) | ~$3-5/day |
| Monthly cost (all 18) | ~$90-150/month |
| **Compared to** hiring 1 junior ops person | ~$800-1500/month |

**Cost cap**: hard-stop at $300/month Nexa-agent spend (alert at 80%, pause at 100%). Logged to `state/nexa-cost-tracker.json`. Daily watchdog: `nexa-cost-watchdog` (no new agent — reuses `cost-tracker.json` from `cost-monitor` skill).

---

## 13. Self-running declaration (Nexa-layer-specific)

Following `agents-v2/SELF-RUNNING-CRITERIA.md`, the Nexa agent layer is **"self-running v1.0.0"** when ALL of:

1. All 18 Nexa agents deliver reliably for 7 consecutive days
2. 0 Nexa-agent cron jobs in error state for the same period
3. 0 "is Nexa X live?" messages from Ivan in any 7-day window
4. **`nexa-canonical-host-enforcer`** reports 0 mismatches (Phase 0 done)
5. **`nexa-pricing-guard`** reports 0 leaks for 30 consecutive days
6. **`nexa-client-journey-agent`** has tracked at least 1 client through a full state transition without human intervention beyond HITL approvals

The first 3 conditions inherit from the org-level self-running declaration. The last 3 are Nexa-specific. Plus the standard 7-day observation window — no touching of PROMPT.md or cron schedules during the window.

---

## 14. PROMPT.md stubs (one per agent, ~250 words each)

Below: skeleton-level stubs showing what each PROMPT.md will contain. Full PROMPTs follow `/opt/data/agents-v2/prompts/PROMPT-TEMPLATE.md` v0.2.0.

### `nexa-pricing-guard` PROMPT.md (P1)

```yaml
name: nexa-pricing-guard
version: 0.2.0
schedule: "0 8 * * *  # 08:00 PYT daily"
owner: ivan
parent_spec: /opt/data/agents/departments/02-finance-legal.md
state_db: /opt/data/agents/state/nexa-pricing-guard.json
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: enforce CURRENT_STATE.md price-privacy rule by scanning all public Nexa surfaces for "$1,500" or any other numeric price.

**Inputs**: `/opt/data/work/research-repos/paragu-ai-platform/apps/nexa-paraguay/` (content/, src/, public/, site.json, nexa-pages/), `nexaparaguay.com.py/*` (live fetch).

**Output**: 150-300 words, sections `scan_summary / leaks_found / affected_paths / severity / fix_proposed`.

**Hard stops**: trademark_banlist, price_privacy, no_fabrication, pii_hard_stop.

**Idempotency**: daily 24h window; on re-run same day → skip + log `duplicate_run`.

**State schema**:
```json
{"last_run": null, "scans_completed": 0, "leaks_found_lifetime": 0, "last_leak_paths": []}
```

### `nexa-orphan-page-killer` PROMPT.md (P1)

```yaml
name: nexa-orphan-page-killer
version: 0.2.0
schedule: "30 8 * * *  # 08:30 PYT daily"
owner: kiki
parent_spec: /opt/data/agents/departments/04-engineering-delivery.md
state_db: /opt/data/agents/state/nexa-orphan-page-killer.json
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: enforce Phase 0.2 (orphan page 301) by probing the 4 known orphan slugs and reporting status drift.

**Inputs**: list of orphan slugs [`empresa`, `lifestyle`, `trust`, `inversor`], live HTTP probes.

**Output**: 100-250 words, table with slug/status/expected/action.

**Hard stops**: trademark_banlist, no_private_repo_writes.

**State schema**:
```json
{"last_run": null, "orphans_remaining": 4, "orphan_history": [{"date": "...", "empresa": 200, "lifestyle": 200, ...}]}
```

### `nexa-canonical-host-enforcer` PROMPT.md (P1)

```yaml
name: nexa-canonical-host-enforcer
version: 0.2.0
schedule: "0 9 * * *  # 09:00 PYT daily"
owner: kiki
parent_spec: /opt/data/agents/departments/04-engineering-delivery.md
state_db: /opt/data/agents/state/nexa-canonical-host-enforcer.json
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: enforce Phase 0.1 (canonical host = nexaparaguay.com.py) by scanning all canonical/hreflang/sitemap/robots references across the repo + live site.

**Inputs**: repo source + live fetch of `/robots.txt`, `/sitemap.xml`, `<link rel=canonical>`, JSON-LD `@id`.

**Output**: 200-400 words, table with source/domain/expected/current/match.

**Hard stops**: trademark_banlist.

**State schema**:
```json
{"last_run": null, "mismatches_lifetime": 0, "current_mismatches": [], "phase_0_1_done": false}
```

### `nexa-content-freshness` PROMPT.md (P2)

```yaml
name: nexa-content-freshness
version: 0.2.0
schedule: "0 10 * * 1  # Mon 10:00 PYT weekly"
owner: luana
parent_spec: /opt/data/agents/departments/01-operations.md
state_db: /opt/data/agents/state/nexa-content-freshness.json
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: detect drift between `content/{es,en,nl,de}.json` and what the live site actually renders; catch MT-seed leaks in German (per known gap).

**Inputs**: 4 locale JSONs, `nexa-pages/*.json`, live HTML for `/es /en /nl /de`.

**Output**: 300-500 words, sections `parity_summary / missing_keys / locale_drift / pricing_leak_check / fix_queue`.

**Hard stops**: trademark_banlist, price_privacy, no_fabrication.

**State schema**:
```json
{"last_run": null, "parity_score_es_en_nl_de": [1.0, 1.0, 1.0, 1.0], "missing_keys_lifetime": 0, "fix_queue": []}
```

### `nexa-claim-validator` PROMPT.md (P2)

```yaml
name: nexa-claim-validator
version: 0.2.0
schedule: "0 14 * * 3  # Wed 14:00 PYT weekly"
owner: ivan
parent_spec: /opt/data/agents/departments/05-research-education.md
state_db: /opt/data/agents/state/nexa-claim-validator.json
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: audit every numeric/quantitative claim on the public site (PIB growth, EU expat count, "single-digit inflation since 2020", etc.) against current public sources.

**Inputs**: `nexa-pages/*.json`, live site HTML, ddgs search helper.

**Output**: 300-600 words, sections `claim_inventory / verified / stale / wrong / aspirational_flags / fix_proposed`.

**Hard stops**: no_fabrication, research-integrity-protocol.

**State schema**:
```json
{"last_run": null, "claims_audited_lifetime": 0, "stale_claims": [], "wrong_claims": [], "aspirational_flags": []}
```

### `nexa-build-monitor` workflow YAML (P2)

```yaml
# /opt/data/work/research-repos/paragu-ai-platform/.github/workflows/nexa-build-monitor.yml
name: nexa-build-monitor
on:
  push:
    paths:
      - 'apps/nexa-paraguay/**'
  workflow_dispatch:

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Nexa typecheck (no || true)
        run: cd apps/nexa-paraguay && pnpm tsc --noEmit
      - name: Nexa lint (no || true)
        run: cd apps/nexa-paraguay && pnpm lint
      - name: Nexa build (no Turbopack, no || true)
        run: cd apps/nexa-paraguay && pnpm build
      - name: Scan for $1,500 leak
        run: |
          if grep -r '\$1,500\|\$1\.500\|1500' apps/nexa-paraguay/src apps/nexa-paraguay/content apps/nexa-paraguay/nexa-pages apps/nexa-paraguay/public 2>/dev/null; then
            echo "::error::Price leak detected"
            exit 1
          fi
      - name: Scan for trademark banlist
        run: bash /opt/data/agents-v2/patterns/trademark-scrub.sh apps/nexa-paraguay/
      - name: Bypass-gate report
        run: |
          bypass_count=$(grep -rn '|| true\|continue-on-error' apps/nexa-paraguay/next.config.js apps/nexa-paraguay/package.json 2>/dev/null | wc -l)
          echo "Bypassed gates in nexa config: $bypass_count"
          echo "::warning::Bypassed gates present" && [ "$bypass_count" -gt 0 ]
```

### `nexa-aml-monitor` PROMPT.md (P3)

```yaml
name: nexa-aml-monitor
version: 0.2.0
schedule: "0 11 * * * ; 0 17 * * *  # 11:00 + 17:00 PYT daily"
owner: ivan
parent_spec: /opt/data/agents/departments/07-nexa-client-operations.md
state_db: /opt/data/agents/state/nexa-aml-monitor.json
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: monitor `nexa-leads` + `nexa-submissions` Docker volumes for SEPRELAD flag patterns; surface template variables that need filling; alert if `compliance-monitor` discovers a new Paraguay regulation.

**Inputs**: `/opt/data/db/nexa-leads.db`, `/opt/data/db/nexa-clients.db`, AML template variables.

**Output**: 150-300 words, sections `submission_velocity / pattern_alerts / template_filling_queue / seprelad_news / actions`.

**Hard stops**: pii_hard_stop, no_fabrication.

### `nexa-partner-registry` PROMPT.md (P3)

```yaml
name: nexa-partner-registry
version: 0.2.0
schedule: "0 16 * * 5  # Fri 16:00 PYT weekly"
owner: ivan
parent_spec: /opt/data/agents/departments/02-finance-legal.md
state_db: /opt/data/db/nexa-partners.db
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: maintain the referral-network ledger — escribanos, real estate intermediaries, vehicle sellers, banks, notaries. Each entry: contact, commission rate, last transaction, dispute history, current status (active/dormant/blacklisted).

**Output**: 200-400 words, table with partner/type/commission/last_tx/status.

### `nexa-client-invoicing` PROMPT.md (P3, on-event)

```yaml
name: nexa-client-invoicing
version: 0.2.0
trigger: on_event  # fires when nexa-client-journey-agent transitions to "closed"
owner: ivan
parent_spec: /opt/data/agents/departments/02-finance-legal.md
state_db: /opt/data/db/nexa-clients.db
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: when a Nexa client closes, generate the SEPRELAD-compliant receipt ($1,500 base + any add-ons + commission splits) and write to client ledger.

**Output**: invoice JSON to `nexa-clients.db` + brief summary to outbox.

**Hard stops**: price_privacy (receipts go to private client DB, never public), no_fabrication.

### `nexa-client-journey-agent` PROMPT.md (P3, lead)

```yaml
name: nexa-client-journey-agent
version: 0.2.0
schedule: "0 9 * * *  # 09:00 PYT daily + on-event for state transitions"
owner: sonia  # with Ivan backup
parent_spec: /opt/data/agents/departments/07-nexa-client-operations.md
state_db: /opt/data/db/nexa-clients.db
state_json: /opt/data/agents/state/nexa-client-journey-agent.json
fallback_model: litellm/primary
model: reasoning
provider: litellm
class: HITL_AGENT  # all state transitions require human approval
```

**Mission**: orchestrate every Nexa client from first WhatsApp ping through yearly anniversary. Maintain client state machine: `inquiry → discovery → onboarding → day1 → residency → post_residency → anniversary → dormant`.

**Inputs**: `/opt/data/db/nexa-clients.db`, `/api/intake` submissions, `/api/contact` submissions, WhatsApp delivery reports (when wired), `state/finance.json` (closed deals).

**Output**: 300-600 words, sections `active_clients / state_distribution / overdue_checkins / pending_transitions / templates_sent / actions`.

**Hard stops**: pii_hard_stop (no client names in outbox text — use client_id), whatsapp_human_only (template acks OK; personalised replies = Sonia).

**State schema**:
```json
{
  "last_run": null,
  "active_clients": 0,
  "state_distribution": {"inquiry": 0, "discovery": 0, "onboarding": 0, "day1": 0, "residency": 0, "post_residency": 0, "anniversary": 0},
  "overdue_checkins": [],
  "pending_transitions": [],
  "templates_sent_today": 0
}
```

### `nexa-day1-protocol` PROMPT.md (P3, on-event)

```yaml
name: nexa-day1-protocol
version: 0.2.0
trigger: on_event  # fires when client transitions to "day1" state
owner: sonia
parent_spec: /opt/data/agents/departments/07-nexa-client-operations.md
state_db: /opt/data/db/nexa-clients.db
fallback_model: litellm/primary
model: reasoning
provider: litellm
class: HITL_AGENT
```

**Mission**: on D0, send client the day-1 welcome packet (translation checklist, document checklist, airport pickup logistics) and coordinate with Sonia for: airport pickup time, SIM chip purchase, Interpol → Migraciones route.

**Output**: checklist JSON + WhatsApp template acknowledgement + WhatsApp-style status board.

**Hard stops**: whatsapp_human_only (acknowledgement templates only).

### `nexa-residency-tracker` PROMPT.md (P3)

```yaml
name: nexa-residency-tracker
version: 0.2.0
schedule: "0 11 * * 2  # Tue 11:00 PYT weekly"
owner: sonia
parent_spec: /opt/data/agents/departments/07-nexa-client-operations.md
state_db: /opt/data/db/nexa-clients.db
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: for every client in `residency` state, log weekly progress (documents submitted, status, blockers), surface overdue cases to Sonia, generate client-facing WhatsApp check-ins.

**Output**: 200-400 words, sections `clients_in_residency / progress_summary / overdue / client_checkins_generated`.

### `nexa-icp-engine` PROMPT.md (P4)

```yaml
name: nexa-icp-engine
version: 0.2.0
schedule: "0 9 * * *  # 09:00 PYT daily (replaces generic sales slot)"
owner: ivan
parent_spec: /opt/data/agents/departments/03-sales-growth.md
state_db: /opt/data/db/nexa-leads.db
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: score every inbound lead (and outbound scout result) against the Nexa ICP rubric — nationality, family status, budget band, timeline, motivation source. Tier as family / investor / other. Score 0-10.

**Output**: 200-400 words, table with lead/score/tier/reasoning/next_action.

**Hard stops**: price_privacy (NO price field), no_fabrication.

### `nexa-dutch-market-scout` PROMPT.md (P4)

```yaml
name: nexa-dutch-market-scout
version: 0.2.0
schedule: "0 11 * * *  # 11:00 PYT daily"
owner: ivan
parent_spec: /opt/data/agents/departments/03-sales-growth.md
state_db: /opt/data/db/nexa-leads.db
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: search LinkedIn + Dutch/DE expat forums (Facebook groups, Reddit r/expats, iamexpat.nl) for signals matching the family-relocation persona. Output: scored leads with public profile URL + post excerpt + fit reason.

**Output**: 200-400 words, table with source/signal/lead_url/fit_score/next_action.

**Hard stops**: no_fabrication, pii_hard_stop (use post excerpts, not full user data).

### `nexa-proposal-drafter` PROMPT.md (P4, on-event)

```yaml
name: nexa-proposal-drafter
version: 0.2.0
trigger: on_event  # fires when nexa-icp-engine scores a lead >= 7
owner: ivan
parent_spec: /opt/data/agents/departments/03-sales-growth.md
state_db: /opt/data/db/nexa-leads.db
fallback_model: litellm/primary
model: reasoning
provider: litellm
class: HITL_AGENT  # Ivan reads every draft before send
```

**Mission**: draft a Nexa proposal in the client's locale (NL/DE/ES/EN/PT) using Sonia's voice ("Relax, I can help you") + "Acompañamiento de cerca" identity + cultural-bridge framing. NO price field. NO tiered packages.

**Output**: proposal markdown draft + outbox note `awaiting ivan review`.

**Hard stops**: price_privacy (NO price), no_fabrication, trademark_banlist.

### `nexa-funnel-tracker` PROMPT.md (P5)

```yaml
name: nexa-funnel-tracker
version: 0.2.0
schedule: "0 9 * * 1  # Mon 09:00 PYT weekly"
owner: ivan
parent_spec: /opt/data/agents/departments/03-sales-growth.md
state_db: /opt/data/db/nexa-leads.db
fallback_model: litellm/primary
model: reasoning
provider: litellm
```

**Mission**: weekly funnel report: NL site visits → /contacto submissions → WhatsApp first-reply → discovery call → $1,500 conversion (count, not price). Surface leak stage.

**Output**: 200-500 words, funnel table + leak analysis + recommendations.

**Hard stops**: no_fabrication, research-integrity-protocol.

### `nexa-content-engine` PROMPT.md (P5)

```yaml
name: nexa-content-engine
version: 0.2.0
schedule: "0 10 * * 3  # Wed 10:00 PYT weekly"
owner: luana
parent_spec: /opt/data/agents/departments/03-sales-growth.md
state_db: /opt/data/db/nexa-content-calendar.db
fallback_model: litellm/primary
model: reasoning
provider: litellm
class: HITL_AGENT
```

**Mission**: weekly produce 1 Dutch/NL-language blog post draft + 1 LinkedIn carousel outline + 1 Instagram reel script, all in Sonia's voice. Submit to Luana for review before any publish.

**Output**: 3 content drafts (markdown) + outbox summary `awaiting luana review`.

**Hard stops**: no_fabrication, trademark_banlist, price_privacy.

### `nexa-testimonial-curator` PROMPT.md (P5)

```yaml
name: nexa-testimonial-curator
version: 0.2.0
schedule: "0 14 1 1,4,7,10 *  # 1st of quarter months, 14:00 UTC"
owner: sonia
parent_spec: /opt/data/agents/departments/06-people-culture.md
state_db: /opt/data/db/nexa-clients.db
fallback_model: litellm/primary
model: reasoning
provider: litellm
class: HITL_AGENT
```

**Mission**: quarterly, identify clients past D+180 with documented consent, draft a testimonial request template (NL/DE/ES/EN). NEVER fabricate or paraphrase without consent. Submit to Sonia for approval.

**Output**: 150-300 words, candidate list + template drafts + consent verification status.

**Hard stops**: no_fabrication (explicit hard-stop per CURRENT_STATE.md), pii_hard_stop.

---

## 15. Cron registration commands (ready-to-paste, after "go")

```bash
# Phase 1 (3 jobs)
hermes cron create "0 8 * * *" --name "aiw-nexa-pricing-guard" \
  --prompt "$(cat /opt/data/agents/nexa-pricing-guard/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline

hermes cron create "30 8 * * *" --name "aiw-nexa-orphan-page-killer" \
  --prompt "$(cat /opt/data/agents/nexa-orphan-page-killer/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline

hermes cron create "0 9 * * *" --name "aiw-nexa-canonical-host-enforcer" \
  --prompt "$(cat /opt/data/agents/nexa-canonical-host-enforcer/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline

# Phase 2 (2 cron + 1 workflow)
hermes cron create "0 10 * * 1" --name "aiw-nexa-content-freshness" \
  --prompt "$(cat /opt/data/agents/nexa-content-freshness/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline

hermes cron create "0 14 * * 3" --name "aiw-nexa-claim-validator" \
  --prompt "$(cat /opt/data/agents/nexa-claim-validator/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills research-integrity-protocol,aiw-ops-discipline

# Phase 2 workflow (CI, not cron)
# File: /opt/data/work/research-repos/paragu-ai-platform/.github/workflows/nexa-build-monitor.yml
# (see §14 stub above)

# Phase 3 (3 cron + 3 on-event)
hermes cron create "0 11 * * *" --name "aiw-nexa-aml-monitor-am" \
  --prompt "$(cat /opt/data/agents/nexa-aml-monitor/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline,compliance-monitor

hermes cron create "0 17 * * *" --name "aiw-nexa-aml-monitor-pm" \
  --prompt "$(cat /opt/data/agents/nexa-aml-monitor/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline,compliance-monitor

hermes cron create "0 16 * * 5" --name "aiw-nexa-partner-registry" \
  --prompt "$(cat /opt/data/agents/nexa-partner-registry/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline

hermes cron create "0 9 * * *" --name "aiw-nexa-client-journey-agent" \
  --prompt "$(cat /opt/data/agents/nexa-client-journey-agent/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline,whatsapp-human-in-loop

hermes cron create "0 11 * * 2" --name "aiw-nexa-residency-tracker" \
  --prompt "$(cat /opt/data/agents/nexa-residency-tracker/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline,whatsapp-human-in-loop

# Phase 4 (2 cron + 1 on-event)
hermes cron create "0 9 * * *" --name "aiw-nexa-icp-engine" \
  --prompt "$(cat /opt/data/agents/nexa-icp-engine/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline,sales-pipeline

hermes cron create "0 11 * * *" --name "aiw-nexa-dutch-market-scout" \
  --prompt "$(cat /opt/data/agents/nexa-dutch-market-scout/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline,sales-pipeline

# Phase 5 (3 cron)
hermes cron create "0 9 * * 1" --name "aiw-nexa-funnel-tracker" \
  --prompt "$(cat /opt/data/agents/nexa-funnel-tracker/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline

hermes cron create "0 10 * * 3" --name "aiw-nexa-content-engine" \
  --prompt "$(cat /opt/data/agents/nexa-content-engine/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline,marketing-content-mon-wed-fri

hermes cron create "0 14 1 1,4,7,10 *" --name "aiw-nexa-testimonial-curator" \
  --prompt "$(cat /opt/data/agents/nexa-testimonial-curator/PROMPT.md)" \
  --model reasoning --provider litellm \
  --skills aiw-ops-discipline
```

**Total**: 16 cron jobs + 1 workflow file + 18 PROMPT.md files + 7 state.json + 5 SQLite DBs + 1 new dept file + 6 modified dept files + 1 modified README.

---

## 16. Verification checklist (must-pass before declaring each Phase done)

Per `ai-run-org-playbook` § "Verification checklist" + the `PROMPT-TEMPLATE.md` checks:

**Per agent before registration**:
- [ ] PROMPT.md has ≥12 `## ` sections (template check)
- [ ] Hard stops YAML is parseable (`python3 -c "import yaml; yaml.safe_load(open('PROMPT.md').read().split('```yaml')[1].split('```')[0])"`)
- [ ] Trademark scrub passes (`bash /opt/data/agents-v2/patterns/trademark-scrub.sh <PROMPT.md>`)
- [ ] Idempotency contract present (`grep "^## Idempotency contract"`)
- [ ] Context-payload present (`grep "^## Context-Packaging Escalation"`)
- [ ] Fallback model present (`grep "^## Fallback Model"`)
- [ ] Class declared (`grep -E "^## (Class|FULL_AGENT|HITL_AGENT|CRON_WORKFLOW|HUMAN_ONLY)"`)
- [ ] Model = `reasoning`, Provider = `litellm` (NOT `MiniMax-M3`, NOT `minimax-oauth`)

**After registration**:
- [ ] `hermes cron list | grep aiw-nexa` shows the new job with `state: scheduled`
- [ ] Seed one example outbox file
- [ ] `bash /opt/data/agents/scripts/health.sh` returns ✅
- [ ] First delivery lands in outbox within 24h
- [ ] Eval-gate scores the first brief ≥ 8/10

**Per Phase**:
- [ ] All agents in phase register cleanly
- [ ] All agents deliver for 7 consecutive days
- [ ] Cross-agent handoff matrix entries work (e.g. `nexa-client-journey-agent` → `nexa-aml-monitor`)
- [ ] No banned brand tokens in any outbox brief (run trademark-scrub on every outbox)
- [ ] No `"$1,500"` leak in any public-surface-adjacent brief

---

## 17. What I am NOT recommending (the rejections)

| Rejected option | Why |
|---|---|
| **Build a parallel Nexa org layer** (its own ORG-AGENTS, its own state tree, its own cron store) | Duplicates ~24 cron jobs, eval-gate, storage architecture, monitoring. Zero benefit for 1 client. The right shape is extension. |
| **Use model: fast for the P1 hygiene agents** (they look single-tool) | They run multi-step: read state + scan repo + grep + curl live site + diff + write outbox. That's 4-5 tool calls. **Use `reasoning`** per `ai-run-org-playbook`. |
| **Use model: primary or MiniMax-M3** | `primary` subscription expired (silent 402). `MiniMax-M3` is the global fallback, rate-limited. Use `reasoning` via litellm. |
| **Auto-commit to Ai-Whisperers/nexa-paraguay private repo** | Per `aiw-management-agents` § "Don't do": routine ops yes, git writes to a NEW repo no. Agents read the mirror only. |
| **Wire WhatsApp automated personalised replies** | `whatsapp_human_only` hard-stop. Templates OK; personalised = Sonia/Luana. |
| **Publish $1,500 anywhere, even in JSON-LD, even in alt text, even in error pages** | `price_privacy` hard-stop. Will fire the daily `nexa-pricing-guard` agent. |
| **Build testimonial fabrication paths** | `no_fabrication` hard-stop. Even "anonymized" testimonials without documented consent are fabricated. |
| **Generate fake team photos / stock photos as "Sonia and team"** | Same. Even if upstream assets exist in `_archive-images/`. |
| **Skip Phase 0 (canonical host + orphan pages + /casos redirect)** | Every downstream agent ships into a contradictory SEO environment. Phase 0 is 2 hours; cost of skipping it is months of accumulated drift. |
| **Build a custom ICP engine from scratch** | The 13-dimension Solstein M&A scoring exists already (`/opt/data/agents/research/`). Reuse it as a base; add 5 Nexa-specific dimensions. |
| **Add a 7th Tier-1 department** | Org constitution v0.2.0 hard-caps at 6 Tier-1 depts. `07-nexa-client-operations` stays Tier-2 cross-cutting until promotion trigger. |
| **Build marketing channels the user banned** (Meta ads, etc.) | Trademark banlist. Performance Marketing Manager is marked 🟠 T3 TRADEMARK-RESTRICTED in `03-sales-growth.md`. Skip entirely. |
| **Auto-deploy agent changes without Ivan approval** | Per `no auto-commit` rule, every cron job that triggers a deploy requires Ivan/Kiki review. |
| **L3 git repos for agents in Phase 1-5** | Defer until self-running criteria met (§13). Phase 6 only. |

---

## 18. Files this plan creates (full inventory)

### New constitution files

1. `/opt/data/agents/departments/NEXA-DEPARTMENT-SETUP-PLAN.md` ← **this file**
2. `/opt/data/agents/departments/07-nexa-client-operations.md` ← new dept file (Phase 3)

### Modified constitution files

3. `/opt/data/agents/departments/01-operations.md` (add Nexa sub-agent row)
4. `/opt/data/agents/departments/02-finance-legal.md` (same)
5. `/opt/data/agents/departments/03-sales-growth.md` (add Nexa ICPs)
6. `/opt/data/agents/departments/04-engineering-delivery.md` (same)
7. `/opt/data/agents/departments/05-research-education.md` (same)
8. `/opt/data/agents/departments/06-people-culture.md` (add Sonia+Luana bandwidth)
9. `/opt/data/agents/ORG-AGENTS.md` (add row to department directory, add cross-cutting references)

### New agent PROMPT.md files (18)

10-27. `/opt/data/agents/nexa-{pricing-guard,orphan-page-killer,canonical-host-enforcer,content-freshness,claim-validator,aml-monitor,partner-registry,client-invoicing,client-journey-agent,day1-protocol,residency-tracker,icp-engine,dutch-market-scout,proposal-drafter,funnel-tracker,content-engine,testimonial-curator,build-monitor}/PROMPT.md`

### New state JSON files (7)

28-34. `/opt/data/agents/state/nexa-{pricing-guard,orphan-page-killer,canonical-host-enforcer,content-freshness,claim-validator,partner-registry,client-journey-agent}.json`

### New SQLite DBs (5)

35. `/opt/data/db/nexa-clients.db`
36. `/opt/data/db/nexa-leads.db`
37. `/opt/data/db/nexa-partners.db`
38. `/opt/data/db/nexa-claims.db`
39. `/opt/data/db/nexa-content-calendar.db`

### New scripts (3 prep scripts)

40. `/opt/data/agents/scripts/nexa-pricing-guard-prep.sh`
41. `/opt/data/agents/scripts/nexa-site-scan.sh` (reused by 4 agents)
42. `/opt/data/agents/scripts/nexa-funnel-prep.sh`

### New CI workflow (1)

43. `/opt/data/work/research-repos/paragu-ai-platform/.github/workflows/nexa-build-monitor.yml`

### Phase 0 site fixes (P0.1-3, deploy as one)

44. `/opt/data/work/research-repos/paragu-ai-platform/apps/nexa-paraguay/README.md` (canonical host updates)
45. `/opt/data/work/research-repos/paragu-ai-platform/apps/nexa-paraguay/site.json` (`.com.py` canonical)
46. `/opt/data/work/research-repos/paragu-ai-platform/apps/nexa-paraguay/docker-compose.yml` (Traefik labels)
47. `/opt/data/work/research-repos/paragu-ai-platform/apps/nexa-paraguay/src/app/[locale]/[slug]/page.tsx` (orphan + /casos redirect)
48. Delete: `/opt/data/work/research-repos/paragu-ai-platform/apps/nexa-paraguay/nexa-pages/{empresa,lifestyle,trust,inversor}.json`
49. `/opt/data/work/research-repos/paragu-ai-platform/apps/nexa-paraguay/content/{es,en,nl,de}.json` (orphan block removal)

### Phase 6 self-running declaration

50. `/opt/data/agents/departments/NEXA-AGENT-LAYER-SELF-RUNNING.md` (when criteria met)

**Total new files**: 27 (excluding deletes and deploy artifacts).

---

## 19. What I need from you (the one question before "go")

The plan is complete. Per your two-phase workflow rule, I am **stopping here**.

You said: *"do all the agents and things we should setup, do eveyuthing first make a compelte detaild plan and then impleent it"*

So before I implement, two narrow confirmations:

**Q1**: Phase 0 = 2 hours of code (Kiki) + ~30 min of manual updates (Luana + Ivan for Search Console). **Do you want me to ship Phase 0 as part of the first deploy, or do Phase 0 first, observe, then start Phase 1 agents?**

- **Option A**: Ship Phase 0 + Phase 1 (the 3 P1 hygiene agents) in one deploy. Faster convergence, but couples two changes.
- **Option B**: Phase 0 first (code-only, observe 24h), then Phase 1 agents. Slower but each change is independently observable.

**Q2**: Sonia's email signature, LinkedIn page, and Instagram bio currently likely reference `nexaparaguay.com`. **Do you want me to draft the updated copy (signature + LinkedIn About + IG bio) and surface in the next brief for Luana to send, or is that strictly out-of-scope and Luana handles it herself?**

- **Option A**: I draft, surface for review, Luana sends.
- **Option B**: Out of scope. Phase 0 P0.1 is code-only.

---

Once you answer Q1 + Q2 (or just say **"go"** to take both as A), I will:

1. Ship Phase 0 + Phase 1 in one batch (~3-4 hours wall-clock including eval-gate + trademark scrub + health-check).
2. Surface the first 3 briefs (`nexa-pricing-guard`, `nexa-orphan-page-killer`, `nexa-canonical-host-enforcer`) within 24h.
3. Wait for your confirmation before Phase 2.

**Plan ready. Standing by for "go".**
