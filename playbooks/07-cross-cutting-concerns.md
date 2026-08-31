# 07 — Cross-Cutting Concerns (Tier 2)

> Cross-cutting concerns that span all 6 canonical departments.
> **Last updated**: 2026-08-14

---

## What are cross-cutting concerns?

Functions that don't belong to a single department but touch all of them. At our 2-person scale, they're sub-functions of existing depts (with named owners). Promote to standalone dept when triggers hit.

---

## 1. AI Ops (Tier 2 cross-cutting)

**Mission**: Keep the agent layer itself healthy — patterns, eval gates, agent observability.

**Owner**: Kiki (CTO)
**Promote to standalone dept when**: Agent count > 10 OR chaos test failures > 1/month

**Roles**:
- AI Ops Lead (Kiki)
- Agent Reliability Engineer (Tier 2)
- MLOps Engineer (Tier 3)
- LLMOps Engineer (Tier 3)
- Prompt Engineer (Tier 2)
- AI Evaluator (Tier 2)

**Sub-agents**:
- `ai-ops-coordinator` (Daily 09:00 PYT)
- `eval-gate-runner` (On-agent-run)
- `chaos-test-runner` (Weekly)

**Tooling**:
- **Eval framework**: Custom (golden trajectories + auto-eval)
- **Observability**: Per-agent logs in `/opt/data/agents/<agent>/logs/`
- **Hard-stop enforcement**: `hard-stop-wrapper.py` runtime

**SOPs**:
- Daily 09:00 PYT: ai-ops-coordinator (agent health check)
- Weekly: chaos-test-runner (3 scenarios per analysis)
- On-agent-run: eval-gate-runner (when shipped)

**Hard stops**:
- Cannot disable hard-stop enforcement
- Cannot modify eval-gate ground truth without approval

---

## 2. Compliance (Tier 2 cross-cutting, NAMED ROLE)

**Mission**: Own the compliance program (GDPR, LGPD, EU AI Act, trademark).

**Owner**: Ivan (wearing the hat per D3)
**Promote to standalone dept when**: First EU client OR $50K MRR

**Roles**:
- Compliance Officer (Ivan wearing the hat)
- Privacy Counsel / DPO (Tier 3, when EU clients)
- Trademark Specialist (Tier 2)
- Regulatory Affairs Specialist (Tier 3)

**Sub-agents**:
- `compliance-monitor` (Weekly)

**Tooling**:
- `trademark-compliance-scrub` skill (existing)
- `trademark-scrub.sh` script (mechanical banlist check)
- EU AI Act compliance: manual tracking

**SOPs**:
- Weekly: compliance-monitor (regulatory change watch)
- On-every-artifact: trademark-scrub.sh
- On-new-vendor: compliance review (manual)

**Hard-stop rule (per D3)**:
> **No EU client contracts accepted until Compliance Officer role is filled by a named person (not Ivan alone).**

---

## 3. Knowledge Management (Tier 2 cross-cutting)

**Mission**: Curate source-materials/ as the org's canonical citation source.

**Owner**: Research dept (policy) + `source-curator` agent (mechanical)
**Promote to standalone dept when**: source-materials/ > 100 files OR second knowledge-heavy vertical

**Roles**:
- Knowledge Manager (Tier 2)
- Content Curator (Tier 2)
- Citation Specialist (Tier 1, embedded in Research dept)
- Taxonomy Architect (Tier 3)

**Sub-agents**:
- `source-curator` (Weekly freshness sweep)

**Tooling**:
- Storage: `/opt/data/source-materials/` (Markdown)
- Citation engine: Zotero (per Research dept)
- Discovery: Grep + manual review

**SOPs**:
- Weekly: source-curator sweeps for stale content
- On-add: Ivan approves
- On-retire: Ivan approves

**Naming convention**: `{topic}/{source}.md`

---

## 4. RevOps (Tier 2 cross-cutting)

**Mission**: Optimize the funnel from lead → cash.

**Owner**: Sales dept (sub-function)
**Promote to standalone dept when**: Pipeline value > $500K OR sales team > 5

**Roles**:
- RevOps Lead (Tier 2)
- Sales Ops Analyst (Tier 2)
- Marketing Ops Manager (Tier 2)
- BI Analyst (Tier 2)
- Data Steward (Tier 3)

**Sub-agents**:
- `pipeline-analyzer` (Daily)

**Tooling**:
- CRM: EspoCRM (OSS)
- BI: Metabase (OSS)
- Attribution: Manual + Plausible

**SOPs**:
- Daily: pipeline-analyzer (funnel metrics)
- Weekly: funnel review (Ivan + agent)
- Monthly: conversion target check

**Conversion targets (per analysis B3 SA-2)**:
- leads → calls: > 40%
- calls → proposals: > 60%
- proposals → signed: > 30%
- Pipeline coverage: 3x quarterly target

---

## 5. BizOps (Tier 2 cross-cutting)

**Mission**: Cross-functional analytics, OKR tracking, executive decision support.

**Owner**: Operations dept (sub-function)
**Promote to standalone dept when**: Ivan's coord hours > 30/week

**Roles**:
- BizOps Lead (Tier 2)
- Strategy Analyst (Tier 3)
- Operations Analyst (Tier 2)

**Sub-agents**:
- `bizops-tracker` (Weekly)
- `okr-tracker` (Weekly)

**Tooling**:
- Dashboards: `/opt/data/agents/dashboards/` (existing)
- Analytics: Plausible (web) + custom (agent)

**SOPs**:
- Weekly: bizops-tracker (cross-functional snapshot)
- Weekly: okr-tracker (OKR progress)
- Monthly: executive brief

---

## 6. Customer Success (Tier 2 sub-function → Tier 3 dept)

**Mission**: Post-sale retention, expansion, renewal.

**Owner**: Sales dept (sub-function)
**Promote to standalone dept when**: 5+ recurring clients

**Roles**:
- CSM Lead (Tier 3)
- Onboarding Specialist (Tier 3)
- Account Manager (Tier 3)
- Renewals Manager (Tier 3)
- Customer Education Specialist (Tier 3)
- Support Engineer (Tier 3)

**Sub-agents**:
- `customer-health-scorer` (Tier 2)

**Tooling**:
- Helpdesk: FreeScout (OSS) or osTicket (OSS)
- Knowledge base: BookStack (OSS)
- Customer portal: Custom

**SOPs**:
- Quarterly business review (QBR)
- Monthly check-in (active accounts)
- Health score weekly

---

## 7. AI Safety (Tier 2 sub-function of Engineering)

**Mission**: Prevent Kiro-class incidents (agent runs amok with elevated perms).

**Owner**: Kiki
**Always active** (every agent needs safety, regardless of size)

**Roles**:
- AI Safety Engineer (Tier 1, sub-agent: ai-safety-engineer)
- AI Red Team (Tier 3, when scaled)
- AI Evaluator (Tier 2, shared with AI Ops)
- AI Ethics Specialist (Tier 3, when regulated)

**Sub-agents**:
- `ai-safety-engineer` (Every 30 min)

**Tooling**:
- Hard stops: `hard-stop-wrapper.py`
- Eval gates: golden trajectories
- Threat model: `/opt/data/agents-v2/THREAT-MODEL.md`

**SOPs**:
- Every 30 min: ai-safety-engineer (OWASP LLM Top 10 check)
- Weekly: chaos tests (per FAILURE-MODES.md)
- Quarterly: threat model review

**OWASP LLM Top 10 2026 mitigations**:
- LLM01 Prompt Injection: All untrusted input sanitized
- LLM02 Insecure Output Handling: Hard stops in wrapper
- LLM03 Training Data Poisoning: N/A (no fine-tuning)
- LLM04 Model DoS: Cost cap + rate limits
- LLM05 Supply Chain: Scoped tool access
- LLM06 Sensitive Info Disclosure: Session DB + wa_bridge logs NEVER read
- LLM07 Insecure Plugin Design: Hard-stop table validated
- LLM08 Excessive Agency: Hard stops non-overridable by LLM
- LLM09 Overreliance: Citation discipline, no hallucinated URLs
- LLM10 Model Theft: N/A (not self-hosted)

---

## 8. Procurement (Tier 2 cross-cutting)

**Mission**: Vendor evaluation, contract negotiation, renewal management.

**Owner**: Ivan (manual) + `procurement-tracker` agent
**Promote to standalone dept when**: Active vendors > 10 OR SaaS spend > $1K/mo

**Roles**:
- Procurement Manager (Tier 2)
- Vendor Manager (Tier 2)
- Contract Negotiator (Tier 2)
- Renewal Specialist (Tier 2)

**Sub-agents**:
- `procurement-tracker` (Weekly)

**Tooling**:
- Vendor list: spreadsheet
- Contract storage: `/opt/data/contracts/` (gitignored)
- Renewal calendar: cron-driven alerts

**SOPs**:
- Weekly: procurement-tracker (renewals due in 30d)
- Monthly: vendor cost review
- On-new-vendor: Ivan + Kiki joint approval

---

## Cross-cutting promotion triggers (consolidated)

| Trigger | Promote to |
|---------|-----------|
| Agent count > 10 | AI Ops → standalone |
| First EU client | Compliance → standalone |
| $50K MRR | Compliance → standalone |
| source-materials/ > 100 files | Knowledge Mgmt → standalone |
| Pipeline > $500K | RevOps → standalone |
| 5+ sales reps | RevOps → standalone |
| 5+ recurring clients | Customer Success → standalone |
| Ivan coord hours > 30/week | BizOps → standalone |
| Active vendors > 10 | Procurement → standalone |
| SaaS spend > $1K/mo | Procurement → standalone |
| Always active | AI Safety (never standalone, just grows) |

---

## See also

- `/opt/data/agents-v2/PLAN-v5.md` Part 2 (org chart)
- `/opt/data/agents-v2/THREAT-MODEL.md` (AI Safety)
- `/opt/data/agents-v2/FAILURE-MODES.md` (chaos test scenarios)
- `/opt/data/agents-v2/ROLES-INVENTORY.md` (full role catalog)
