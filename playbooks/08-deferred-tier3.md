# 08 — Deferred Tier-3 Departments (with Promotion Triggers)

> 12-15 departments that don't exist yet. Each has a quantitative trigger for promotion to standalone.
> **Last updated**: 2026-08-14

---

## Reading guide

- Each dept: trigger to activate, roles, agent candidates, hard stops
- Promotion = the dept splits out from its parent cross-cutting concern OR gets created from scratch
- Until promoted, the function is absorbed into an existing dept

---

## Currently-absorbed Tier-3 depts (no promotion trigger hit)

### Customer Success (absorbed in Sales)
- **Trigger**: 5+ recurring clients
- **Parent**: Sales & Growth dept
- **Roles**: CSM Lead, Onboarding Specialist, Account Manager, Renewals Manager, Customer Education, Support Engineer
- **Agent candidates**: `customer-health-scorer` (already in plan as Tier 2)

### Marketing (independent) (absorbed in Sales)
- **Trigger**: >$2K/mo marketing budget OR 10+ clients
- **Parent**: Sales & Growth dept (currently sub-function)
- **Roles**: Brand Manager, SEO Specialist, Email Marketing Specialist, Paid Ads Specialist (TRADEMARK-BANNED), Social Media Manager (TRADEMARK-RESTRICTED), Community Manager, Event Coordinator, Partnerships Manager
- **Agent candidates**: `marketing-content-producer`, `multimedia-producer` (already Tier 2)

### Procurement (independent) (absorbed in Finance)
- **Trigger**: Active vendors > 10 OR SaaS spend > $1K/mo
- **Parent**: Finance & Legal dept
- **Roles**: Procurement Manager, Vendor Manager, Contract Negotiator, Renewal Specialist
- **Agent candidates**: `procurement-tracker` (already Tier 2)

---

## Tier-3 depts requiring future trigger

### Compliance (standalone) (currently Ivan wearing hat)
- **Trigger**: First EU client OR $50K MRR
- **Roles**: Compliance Officer (currently Ivan), Privacy Counsel/DPO, Regulatory Affairs Specialist
- **Agent candidates**: `compliance-monitor` (currently Tier 2, promotes to Tier 3 lead)
- **Hard-stop rule**: NO EU contracts until this dept is filled

### Investor Relations
- **Trigger**: First external investor
- **Roles**: IR Manager, Fundraising Lead, Board Liaison
- **Agent candidates**: `ir-monitor` (tracks cap table, runway, deck status)

### Chief of Staff
- **Trigger**: Ivan coord hours > 50/week
- **Roles**: Chief of Staff, Executive Assistant, Board Prep Specialist
- **Agent candidates**: `executive-brief-generator` (auto-generates board updates)

### Treasury
- **Trigger**: $100K+ cash OR debt instruments
- **Roles**: Treasurer, Banking Specialist, FX Manager, Investment Manager
- **Agent candidates**: `treasury-monitor` (tracks cash, FX exposure, runway scenarios)

### Internal Audit
- **Trigger**: $1M+ revenue
- **Roles**: Internal Audit Lead, Compliance Auditor, Risk Analyst
- **Agent candidates**: `audit-runner` (scheduled compliance + control checks)

### Trust & Safety
- **Trigger**: Ship consumer AI product
- **Roles**: T&S Lead, Content Moderator, Misuse Specialist, Policy Writer
- **Agent candidates**: `t-s-monitor` (scans for misuse patterns)

### DevRel
- **Trigger**: ParaguAI Builder has public API
- **Roles**: DevRel Manager, Developer Advocate, Community Manager, Tech Writer
- **Agent candidates**: `devrel-content-producer`, `api-docs-monitor`

### Workplace Operations
- **Trigger**: Open physical office
- **Roles**: Workplace Manager, Office Coordinator, IT Support
- **Agent candidates**: `workplace-monitor` (sensor + access management)

### Fraud / Risk
- **Trigger**: $500K+ payment volume
- **Roles**: Fraud Analyst, Risk Manager, Chargeback Specialist
- **Agent candidates**: `fraud-detector` (analyzes transaction patterns)

### Compensation & Benefits
- **Trigger**: First FTE hire
- **Roles**: Comp & Benefits Manager, Equity Specialist, Payroll Admin
- **Agent candidates**: `comp-monitor` (salary band tracking)

### People Operations (HR)
- **Trigger**: 5+ FTEs
- **Roles**: People Ops Partner, HR Generalist, Benefits Admin
- **Agent candidates**: `people-ops` (onboarding workflow, benefits tracking)

### DEI / Belonging
- **Trigger**: 10+ employees (and values-aligned)
- **Roles**: DEI Specialist, ER Lead
- **Agent candidates**: (none — sensitive human work)

### Public Relations
- **Trigger**: Launch flagship brand OR media interest
- **Roles**: PR Manager, Media Liaison, Spokesperson
- **Agent candidates**: `press-monitor` (tracks media mentions)

### Government Relations
- **Trigger**: Regulated vertical
- **Roles**: GovRel Manager, Lobbyist, Compliance Liaison
- **Agent candidates**: `regulatory-monitor` (gov announcement watch)

---

## Tier-4 enterprise depts (NOT in scope at our scale)

### Internal Communications
- **Trigger**: 50+ people
- **Roles**: Internal Comms Manager, Newsletter Editor

### M&A / Corp Dev
- **Trigger**: Acquisitions planned
- **Roles**: Corp Dev Lead, M&A Analyst

### Chief Data Officer (CDO)
- **Trigger**: Data-driven product
- **Roles**: CDO, Data Strategy Lead

### Chief AI Officer (CAIO)
- **Trigger**: Enterprise AI (per Futureproofing.dev 2026)
- **Roles**: CAIO, AI Strategy Lead

### Diversity & Inclusion Lead
- **Trigger**: 25+ employees (and values-aligned)

---

## Promotion mechanism

When a trigger fires:

1. **Create dedicated PROMPT.md** at `/opt/data/agents/<new-dept>/PROMPT.md`
2. **Add cron job** to `jobs.json` with appropriate cadence
3. **Add state file** at `/opt/data/state/<new-dept>.json`
4. **Move roles from cross-cutting concern** to dedicated dept spec
5. **Bump ORG-AGENTS.md** version (v0.3.0 → v0.4.0 etc.)
6. **Update INDEX.md** in playbooks/

**Estimated effort per promotion**: ~2 hours of agent + 1 hour of Ivan review.

---

## Promotion calendar (predicted)

Based on analysis + cheatsheet thresholds:

| Dept | Likely trigger timeline | Expected year |
|------|--------------------------|---------------|
| Customer Success | 5+ clients | Q4 2026 |
| Marketing (independent) | $2K/mo marketing budget | Q1 2027 |
| Procurement (independent) | 10+ vendors OR $1K/mo SaaS | Q2 2027 |
| Compliance (standalone) | First EU client | Q2 2027 |
| Treasury | $100K+ cash | Q3 2027 |
| Investor Relations | First external investor | Q4 2027 |
| Chief of Staff | Ivan coord > 50 hrs | Q1 2028 |
| Internal Audit | $1M+ revenue | Q2 2028 |
| Trust & Safety | Consumer AI launch | Q3 2028 |
| DevRel | Public API | Q4 2028 |
| Fraud / Risk | $500K+ payment volume | Q4 2028 |
| Workplace | Open office | (not planned) |
| Comp & Benefits | First FTE | Q2 2029 |
| People Ops | 5+ FTEs | Q3 2029 |
| PR | Brand launch | (not planned) |

---

## See also

- `/opt/data/agents-v2/PLAN-v5.md` Part 2 (org chart with all tiers)
- `/opt/data/agents-v2/ROLES-INVENTORY.md` (full role catalog)
- `/opt/data/agents-v2/playbooks/07-cross-cutting-concerns.md` (parent functions)
