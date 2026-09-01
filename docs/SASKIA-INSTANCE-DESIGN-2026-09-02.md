# Saskia Instance — Design (Phase "Kernel", WS-6)

> **Status**: Design only. **No deployment. No cron registration. No writes to Saskia's systems.**
> **Date**: 2026-09-02
> **Frame**: Saskia is opening a café/restaurant. She gets her own instance: **not** a Project-inside-AIW, **not** AIW's six departments replicated. A restaurant-shaped agent organization, built on the kernel (see `docs/KERNEL-DESIGN-2026-09-02.md`).
> **Inputs read**: `/opt/data/agents-v2/plans/` (general AIW planning); HERMES-ANSWERS-2026-09-02 (live host context); `departments/NEXA-DEPARTMENT-SETUP-PLAN.md` (closest existing precedent — read for kernel input, NOT as a template to copy).

---

## 1. The strategic shift

**What this design replaces**: the prior "Project inside AIW" brief would have made Saskia a Project that AIW's existing agents attached to (e.g. `delivery-tracker` and `qa-automation-runner` pointing at her repo). **That is wrong.** Saskia doesn't want AIW's agents pointed at her repo. She wants *her own organization* — agents that run *her* restaurant's digital operations, calibrated to *her* rhythms, with hard-stops that match *her* risk tolerance, on infrastructure *she* controls.

**What this design proposes instead**: a **Saskia-instance** built from the kernel (WS-5 deliverable). AIW provides the kernel + a one-time design/bind pass; Saskia runs the instance; AIW connects only for periodic check-ins.

---

## 2. Restaurant-shaped departments

Do **NOT** copy AIW's six departments. A café/restaurant has a fundamentally different operational shape. Candidates per the brief and one pass of research:

| Department | What it owns | Cadence | Why not AIW's |
|---|---|---|---|
| **Front-of-House** | Reservations, walk-in queue, seating plan, guest waitlist, host stand | Real-time + every-15-min sync | NOT analogous to AIW's `02-finance-legal` |
| **Kitchen & Service** | Menu engineering, prep sheets, dish costing, allergen matrix | Daily prep cycle, weekly menu review | NOT analogous to `04-engineering-delivery` |
| **Suppliers & Purchasing** | Vendor list, order cadence, lead-time tracking, price negotiation, freshness rotation | Daily 06:00 ordering, weekly reconciliation | NOT analogous to any AIW dept |
| **Guest Experience** | Post-visit follow-up, loyalty program, gift cards, complaints remediation | Post-transaction + weekly aggregation | Distinct — AIW has no customer-facing dept |
| **Marketing & Reputation** | Social content, review monitoring (Google, TripAdvisor), local SEO, photos | Daily posts, weekly review sweep | NOT analogous to AIW's `03-sales-growth` (that dept sells to OTHER businesses) |
| **Staff Scheduling** | Shift scheduling, payroll inputs, training matrix, role coverage | Weekly scheduling + per-shift callouts | NOT analogous to `01-operations` |
| **Bookkeeping & Compliance** | Daily revenue, supplier invoices, tax prep, health-dept compliance | Daily close, monthly reconciliation | Sector-specific |

**Department count**: 7. (Could merge `Guest Experience` into `Marketing & Reputation`; could split `Kitchen` from `Service`. This design locks 7 for v0.1; can adjust during enumeration phase.)

**Each dept gets**: 2–4 agents + 1 dept-lead. **Total agent roster: ~20 agents across 7 depts.** Plus 1 `saskia-lead` (the equivalent of Erebus for AIW) for cross-dept coordination.

---

## 3. Agent roster (skeleton)

| Dept | Agent | Class | Cadence | Sub-agent reads | Writes to |
|---|---|---|---|---|---|
| Front-of-House | `saskia-foh-reservations` | HITL_AGENT | real-time + 15min | reservation apps, walk-in tablet | `state/reservations.json`, outbox |
| Front-of-House | `saskia-foh-waitlist` | HITL_AGENT | real-time | reservation apps | `state/waitlist.json` |
| Kitchen & Service | `saskia-kitchen-menu-engineer` | FULL_AGENT | weekly | sales data, supplier prices | `outbox/menu-proposals.md` (HITL approval before menu change) |
| Kitchen & Service | `saskia-kitchen-prep-coordinator` | CRON_WORKFLOW | daily 04:00 | bookings (next day), menu | `outbox/prep-sheet-*.md` |
| Suppliers | `saskia-supplier-orders` | CRON_WORKFLOW | daily 06:00 | inventory, supplier catalog, par levels | `state/orders.json`, supplier order outbox (HITL before send) |
| Suppliers | `saskia-supplier-price-watch` | FULL_AGENT | weekly | supplier catalogs, market data | `outbox/price-changes.md` |
| Guest Experience | `saskia-guest-followup` | HITL_AGENT | real-time (post-visit) | reservations, POS | `state/followups.json`, follow-up messages (HITL) |
| Marketing | `saskia-marketing-content` | HITL_AGENT | 3×/week | menu, events, season | social-media outbox (HITL before post) |
| Marketing | `saskia-marketing-reviews` | FULL_AGENT | hourly | Google reviews, TripAdvisor | `state/reviews.json`, alert on 1-star (HITL reply before send) |
| Marketing | `saskia-marketing-local-seo` | FULL_AGENT | weekly | Google Business Profile, photos | (audit only; HITL on any change) |
| Staff | `saskia-staff-scheduler` | HITL_AGENT | weekly + on-demand | availability, role matrix | schedule outbox (HITL before publish) |
| Bookkeeping | `saskia-bookkeeping-revenue` | CRON_WORKFLOW | daily close | POS | `state/revenue.json` |
| Bookkeeping | `saskia-bookkeeping-invoices` | HITL_AGENT | per-supplier-order | supplier orders | payment outbox (HITL before pay) |
| Cross-dept | `saskia-lead` | FULL_AGENT | daily 18:00 | state/* across depts | weekly digest to Saskia + AIW check-in |
| (Owner-only) | (Saskia personally) | HUMAN_ONLY | ad-hoc | her own state | approvals only |

**Total**: 14 agents + 1 lead + Saskia herself. **20** in the v0.1 design was an over-estimate; **14 + lead** is the realistic minimum.

---

## 4. The boundary (what crosses, what doesn't)

### What Saskia's instance does **autonomously** (no AIW, no manual)
- Daily revenue close (`saskia-bookkeeping-revenue`)
- Inventory-based supplier ordering (CRON_WORKFLOW; HITL before send)
- Hourly review watch + 1-star alerts
- Reservation/waitlist updates
- Daily prep sheets

### What needs **Saskia's approval** (HITL)
- Replying to any 1- or 2-star review publicly
- Sending any customer-facing message (post-visit follow-up)
- Posting any social-media content
- Publishing any menu change
- Sending any supplier order
- Paying any supplier invoice
- Publishing any staff schedule
- Any action touching money, public surface, or staff

### What **AIW** sees (cross-instance visibility)
- The weekly digest to Saskia (per opt-in)
- Aggregate health metric: cron success rate, decision-queue saturation, hard-stop-blocked attempts (counts only, not content)
- **NO** restaurant content (recipes, prices, reservations, guest data) crosses to AIW
- **NO** AIW agent can read Saskia's state

### What **never** crosses
- Customer PII (name + phone + email) — stays in Saskia-state
- Supplier pricing — stays in Saskia-state
- Staff salary data — stays in Saskia-state
- Health-dept compliance docs — stays in Saskia-state

This boundary is **hard-coded** by the kernel's HOST-ONLY.md contract and the per-instance `shell-sandbox` model.

---

## 5. Safety model — DIFFERENT from AIW

**Critical**: AIW's ADR-0004 #4 accepted R1 (hard-stops unenforced) for **AIW's own org**. That calculus **does NOT apply** to Saskia's instance. Saskia's agents will:
- Send public messages (reviews, social posts)
- Process payments (supplier invoices)
- Schedule staff (legal liability)
- Touch health-dept compliance (legal liability)

**Mandatory hard-stop enforcement** is a v0.1 deployment precondition for Saskia-instance. Three layers:

| Layer | Mechanism | Verified by |
|---|---|---|
| **Static gates in prompts** | `hard_stops:` block in every PROMPT.md listing each destructive action + `require_approval: true` | `lint-prompts.py` enforces presence |
| **Runtime check** | `patterns/hard-stop-wrapper.py` invoked from cron executor (per AIW-built kernel primitive) | NOT yet wired in AIW; required before Saskia deploy |
| **Outbox-mediated writes** | Destructive actions write to `outbox/<dept>/<agent>/` and require human review before the action executes (not just before the agent proposes) | Outbox gate (per kernel mechanism) |

**Outbox-mediated** is the strongest model and is what Saskia needs. AIW currently does *outbox-as-delivery* but not *outbox-as-gate*. The kernel's v0.1 must add the gate primitive; AIW does not need to enable it for itself, but the kernel must provide it for instances that want it.

**If the kernel doesn't ship with outbox-gate enforcement in v0.1**, Saskia-instance deployment must include that wiring as a kernel + AIW joint deliverable. **This is the single most important safety item for the kernel extraction.**

---

## 6. Cadence — restaurant, not software company

The brief is explicit about this: **"cuisines suited to a restaurant's rhythm — daily prep cycles, weekly ordering, seasonal menus — not a software org's sprint cadence."**

| Rhythm | Examples |
|---|---|
| **Real-time** | Reservation changes, walk-in alerts, payment confirmations |
| **Hourly** | Review-monitor scan, POS reconciliation |
| **Daily** | 04:00 prep coordination, 06:00 supplier ordering, 18:00 end-of-day revenue close, 22:00 reservation-lookahead |
| **Weekly** | Sunday: supplier reconciliation + menu-cost review; Tuesday: staff schedule release |
| **Monthly** | Bookkeeping close, tax-prep handoff, marketing analytics |
| **Seasonal** | Menu refresh (4×/year), loyalty program re-engagement |

**Anti-pattern to avoid**: AIW's pattern of 30min monitors + many overlapping crons. Saskia's instance should be **fewer crons, longer cycles, more real-time**. She has 1 human, not a department.

**Cron count target**: ~20 crons total (1 per agent × most, plus 5–6 cross-cutting). Comparable to NEXA (24 crons per §3 of that plan, scaled down for fewer depts).

---

## 7. Data store + state model

Per kernel v0.1:
- **JSON state files** under `state/<dept>/<agent>.json` (kernel default)
- **SQLite migration optional** per-instance (Saskia v0.1 stays JSON; she has 14 agents, JSON is fine)
- **Schemas**: kernel provides `state.schema.json`; per-instance `saskia-state.schema.json` extends
- **Outbox**: `outbox/<dept>/<agent>/YYYY-MM-DD-<topic>.md`; gated via outbox gate
- **Backups**: kernel outbox-rotation policy (≥90d archive); Saskia-deployable via simple cron to local NAS or BWS-backed cloud

---

## 8. Risks specific to Saskia-instance

| Risk | L×I | Tier | Mitigation |
|---|---|---|---|
| Public review reply auto-sent that is wrong | 5×5 | CRITICAL | Outbox gate + Saskia must approve before send |
| Supplier order sent with wrong item/qty | 4×5 | CRITICAL | Outbox gate + Saskia must approve |
| Staff schedule published with wage/law error | 3×5 | HIGH | Outbox gate; weekly template review by Saskia |
| Customer PII leaks via state mirror | 4×4 | HIGH | HOST-ONLY.md declares state-private; AIW never reads |
| Cross-instance LLM call (Saskia → AIW state) | 5×4 | HIGH | Kernel enforces per-instance `shell-sandbox`; no shared state |
| Hard-stops unenforced at kernel level → all bets off | 5×5 | CRITICAL | WS-5 deliverable must include outbox-gate primitive |
| POS payment-system integration error | 3×5 | HIGH | Outbox gate + Saskia-defined rate limits |
| Menu engineered without allergen matrix | 4×5 | CRITICAL | `saskia-kitchen-menu-engineer` hard-stop: writes to outbox only; never touches menu-board system |

---

## 9. What this design does NOT include (deliberate)

- **No actual deployment** of any agent or cron for Saskia.
- **No writes** to any Saskia-controlled system (`/opt/data/agents-v2/plans/`, `saskia-app`/`saskia-personal-context` repos, Google Business, POS, social accounts).
- **No commitment** to particular POS, reservation, supplier, or social platforms.
- **No mention of revenue, costs, or business metrics for Saskia** — this is design only.
- **No timeline** — when/whether to deploy is Ivan's call.

---

## 10. Open questions for Ivan (before any deployment)

| # | Question |
|---|---|
| Q1 | Is the kernel outbox-gate mechanism a v0.1 deliverable, or v0.2? (It affects whether WS-5 is fully done before WS-6 begins.) |
| Q2 | Does Saskia's instance run on her own hardware/cloud, or hosted by AIW? (Affects HOST-ONLY.md and kernel infrastructure assumptions.) |
| Q3 | Which POS system? Which reservation system? Which social accounts? (Per-instance inputs to bootstrap.) |
| Q4 | Who is the "approved_human" for HITL_AGENT approval in Saskia's instance? Just Saskia, or also a manager she hires? |
| Q5 | Saskia's comfort with AIW having **any** aggregate-metric visibility (cron success rate) vs **zero** visibility (strict isolation). |
| Q6 | Does she want a weekly AIW digest "what your org did this week" or only on-demand check-in? |
| Q7 | What's the menu language mix — Spanish only, or Spanish + Guaraní, or Spanish + English (tourists)? (Affects PROMPT and tone defaults.) |

These are gating for **deployment**. The design itself stands without answers to them — but the answers shape which bootstrap inputs the script gets called with.

---

## 11. The relationship to the kernel extraction (WS-5)

Saskia-instance **requires**:
- `kernel/patterns/hard-stop-wrapper.py` (de-AIW'd from AIW's)
- `kernel/scripts/outbox-gate.sh` (NEW primitive — outbox-as-gate)
- `kernel/scripts/bootstrap-instance.sh` (working)
- `kernel/templates/PROMPT-TEMPLATE.md` (parameterized for restaurant context)
- `kernel/research/DEPT-RESEARCH-METHODOLOGY.md` (already kernel, no change)
- `kernel/CONVENTIONS.md` (12-section spec with HITL_AGENT class support — already in PROMPT-TEMPLATE)

Saskia-instance **does NOT need**:
- `kernel/departments/*` — instance-level (Saskia's departments are restaurant, not AIW's six)
- `kernel/state/coord.json` — instance-level (Saskia has her own state)
- `kernel/agents/*` — instance-level

The kernel provides the **structural skeleton**. The bootstrap script populates the **content**.

---

## 12. Verification of this design (not of a deploy)

| Verification | How |
|---|---|
| Department set is restaurant-shaped | Compare against §2's 7-dept candidate list (research this turn) |
| No deployment happened | `find /opt/data/instances/saskia -type f 2>/dev/null` returns empty |
| No crons registered | `saskia-*` absent from `/opt/data/.hermes/cron/jobs.json` |
| No AIW-Prompts were touched | `git diff -- '*.PROMPT*'` on this commit: only docs/ |
| No writes to Saskia-controlled paths | `git status` clean; no `/opt/data/agents-v2/plans/*` modifications |
| This doc is reviewable | `docs/SASKIA-INSTANCE-DESIGN-2026-09-02.md` exists in repo |

---

## 13. Next operator-session asks

When the kernel v0.1 is approved + deployed, the next session would do:

1. Read this design doc + Kernel design doc + existing engagement at `/opt/data/agents-v2/plans/`.
2. Wait for operator answers to §10's 7 questions.
3. Run `kernel/scripts/bootstrap-instance.sh saskia --source ./kernel` against a clean `/opt/data/instances/saskia/` (instance directory, not AIW's tree).
4. Smoke-test the bootstrap (see kernel design §4).
5. Hand the empty skeleton to operator + Saskia's 7 answers as the inputs.
6. **Stop.** Do not auto-deploy.

**We are not in that session.** This is a design doc.
