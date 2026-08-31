# Original Long-Form Department List

**Reconstructed from the conversation where it was condensed.**

When building the AI Whisperers org structure, the initial list was longer (16+ departments). It was condensed to fit a "1000-person view" — what a single founder would need to run a small-to-medium org.

This document preserves the **full long-form list** for reference, plus shows how each maps to our final agent structure.

---

## The Original Long-Form (20 Departments)

| # | Department | Description | Maps to (Final Agent) |
|---|-----------|-------------|----------------------|
| 1 | **Finance** | P&L, cost tracking, budgets | finance-controller |
| 2 | **Human Resources** | Hiring, onboarding, comp | people-hr |
| 3 | **Legal** | Compliance, contracts, IP | compliance-monitor |
| 4 | **Development** | Code, devops, builds | engineering-roster, devops-monitor |
| 5 | **QA** | Testing, eval, gates | qa-automation-runner, eval-gate-runner |
| 6 | **Operations** | Day-to-day, processes | ai-ops-coordinator |
| 7 | **Research** | Literature, citations | research-tracker, citation-checker |
| 8 | **Marketing** | Content, outreach, brand | marketing-content-producer |
| 9 | **Multimedia** | Images, video, audio | multimedia-producer |
| 10 | **Sales** | Pipeline, leads, close | sales-pipeline, lead-enrichment |
| 11 | **Procurement** | Vendor mgmt, contracts | procurement-tracker |
| 12 | **Content Management** | KB, docs, wikis | (folded into Marketing) |
| 13 | **Board of Directors** | Quarterly review | board-of-directors |
| 14 | **Cross-Cutting** | Org-wide concerns | (multiple: ai-safety, security) |
| 15 | **Customer Success** | Retention, LTV | coach-renewal-manager |
| 16 | **Data & Analytics** | Metrics, dashboards | bizops-tracker (partial) |
| 17 | **Security** | Already separate | security-watchdog |
| 18 | **Compliance** | Already separate | (folded into Legal) |
| 19 | **Product** | Strategic product direction | (covered by management-coordinator) |
| 20 | **Course / Education** | What we actually sell | coach-practitioner (the coaching product) |

---

## The Condensed 16-Department View

After removing duplicates and folding sub-concerns, we got:

| # | Department | Final Count |
|---|-----------|-------------|
| 1 | Finance | 3 agents |
| 2 | HR | 2 agents |
| 3 | Legal | 1 agent |
| 4 | Development | 5 agents |
| 5 | QA | 3 agents |
| 6 | Operations | 2 agents |
| 7 | Research | 4 agents |
| 8 | Marketing | 2 agents |
| 9 | Multimedia | 1 agent |
| 10 | Sales | 6 agents |
| 11 | Procurement | 1 agent |
| 12 | Accounting | 1 agent |
| 13 | Management | 6 agents |
| 14 | Board | 1 agent |
| 15 | Coaching (the product) | 8 agents |
| 16 | Cross-Cutting | 4 agents |

**Final: 16 departments, 51 agents.**

---

## Department Monitor Pattern (from the conversation)

> "Same like you're somebody that is monitoring, an agent that is monitoring the department, 'Hey, is this department running as it should be?' It's not executing the work, except if it's the controlling department."

**Concept:** A monitor agent that observes — it does NOT execute. It's the "Watcher of the Watchmen."

### Pattern Structure

```
[Department Agent]
       │
       ▼ (executing)
[Output, tickets, deliverables]
       │
       ▼ (observed)
[Department Monitor]
       │
       ├──► alert if SLA missed
       ├──► alert if budget exceeded
       ├──► alert if quality dropped
       └──► weekly summary to board-of-directors
```

### Implication for Our Org

We already have implicit monitors:
- **board-of-directors** — quarterly review of all departments
- **bizops-tracker** — KPI tracking
- **ai-ops-coordinator** — day-to-day ops oversight
- **self-running-check** — verifies the cron + webhook loop
- **eval-gate-runner** — quality gate for agent output
- **cost-monitor** — budget guardrail

**But we don't have a dedicated "dept-monitor" that watches each of the 16 departments individually.** That's a Phase 27 candidate.

---

## The "Roles vs Agents" Distinction

> "In principle, the role is independent of agents. You put the role independent of agents, and the different roles and skills put together from, 'Hey, do all these roles.'"

**Concept:** A *role* is a single-responsibility function. An *agent* combines one or more roles + the skills to execute them.

### Example

- **Role:** "Find new coaching prospects"
- **Role:** "Send initial outreach"
- **Agent:** `coach-lead-finder` (combines both roles + skills)

This is exactly how `coach-conversion-agent` works:
- **Role:** "Score customer readiness"
- **Role:** "Generate email sequence"
- **Agent:** combines both into one PROMPT.md

### Implication

If we want a generic customer template, we should:
1. Define roles as separate files (independent of agents)
2. Combine roles into agents via PROMPT.md
3. Customer picks: "Which departments do I need?" → "Which roles in each?"
4. We auto-generate: "Here's your agent."

This is the **template-able agent factory** pattern.

---

## Tooling Tiers (1-5, 5-20, 20+)

> "You can have mid-range, like a 1-5 business company. What is the actual tooling that would be advised? Could be services, notebook, anything. Then 5-20, they have limited to no automation. Above 20, completely different. Then they have a lot of automation."

This is a separate document. Stubs here:

### Tier 1: Solo / 1-5 people
- **Tools:** Notion, Trello, WhatsApp, Evolution API, Cloudflare
- **AI Layer:** Hermes Agent (1 instance, 3-5 agents)
- **Cost:** $50-200/mo
- **Automation:** Basic (cron + 1 webhook)
- **Doc:** `/opt/data/agents-v2/docs/TOOLING-TIER-1.md` (TODO)

### Tier 2: Small / 5-20 people
- **Tools:** Notion, Linear, ClickUp, WhatsApp, Cloudflare, R2
- **AI Layer:** Hermes Agent + multiple instances + agent-org-framework
- **Cost:** $300-1000/mo
- **Automation:** Advanced (cron + webhooks + eval-gate)
- **Doc:** `/opt/data/agents-v2/docs/TOOLING-TIER-2.md` (TODO)

### Tier 3: Medium / 20+ people
- **Tools:** Jira (expensive), Linear Pro, Canal de comunicacion, Teams, Salesforce
- **AI Layer:** Multiple Hermes instances + orchestration layer
- **Cost:** $2000+/mo
- **Automation:** Enterprise (full)
- **Doc:** `/opt/data/agents-v2/docs/TOOLING-TIER-3.md` (TODO)

**Note:** The conversation explicitly says "I wouldn't advise using Jira, it's expensive."

---

## Generic Customer Template

> "Should be a template that customers can use later. 'Oh, you want to have marketing? Okay, you want to have these roles, which one do you want to have automated?' And then AI does its best."

### Template Structure (Stub)

```
{{company-name}}/
├── CUSTOMER-README.md          # How to use
├── departments/
│   ├── 01-marketing/           # Which roles?
│   │   ├── roles.md            # 5 marketing roles
│   │   └── agent.md            # Auto-generated by AI
│   ├── 02-sales/
│   ├── 03-finance/
│   └── ...
├── tooling-tier.md             # 1-5 / 5-20 / 20+
├── agents/                     # Auto-generated by AI
└── proxy/                      # Hermes-CLI proxy or BWS-bridge
```

**Status:** Not yet built. This is the **next big thing** if we want to sell AI Whisperers as a product, not just our coaching.

---

## Conversation Timestamp

This transcription was from a discussion between:
- **Speaker 1:** Ivan (CEO/Founder)
- **Speaker 2:** (Hermes/me — refers to a longer initial list of departments)
- **Speaker 3:** (additional voice — discussed tools, Jira, Teams, meetings)

---

## Summary

The conversation:
1. **Reconstructed** what the original 16+ department list was
2. **Captured** the "department monitor" pattern (watchers of watchers)
3. **Defined** the roles-vs-agents distinction
4. **Stubbed** the tooling tiers (1-5, 5-20, 20+)
5. **Stubbed** the generic customer template

These are **real gaps** in our current build. None is urgent, but all are documented for future work.

**Recommendation:** Don't build these now. They're configurational upgrades, not blockers. The 3 real blockers remain:
1. Send first prospect WhatsApp
2. Top up $20 OpenRouter
3. Run first free quick-win

After first customer + $500 MRR: build the tooling tiers + customer template as paid product.
