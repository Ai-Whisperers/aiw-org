# Standard Roles Glossary — All Departments

> The master inventory of standard roles per department. Mapped to our 6 canonical
> departments (Operations / Finance-Legal / Sales-Growth / Engineering-Delivery /
> Research-Education / People-Culture). Used by Sessions 2-7 of the dept-buildout
> workflow to size role coverage, pick tools, and design SOPs.

**Last updated**: 2026-08-14
**Sources**: `roles-glossary.md` synthesis from org-design literature. See
`/opt/data/source-materials/topics/org-design/INDEX.md` for provenance.

---

## Reading guide

- One section per department (alphabetical role order)
- Per role: title, 1-line definition, reports to, supervises, tier-coverage (Tier 1 / 2 / 3 / 4)
- Mapping to **our** canonical 6 depts (we collapse Ivan's 15 named departments)
- Color coding: 🟢 Tier 1 (we staff now), 🟡 Tier 2 (next 6 months), 🟠 Tier 3 (12+ months), 🔴 Tier 4 (50+ people)

---

# Department 1 — Operations (15 roles)

The meta-department: keeps the platform itself alive. Doesn't ship product — makes sure every other department can ship.

| # | Role | Definition | Reports to | Supervises | Tier |
|---|------|------------|-----------|------------|------|
| 1.1 | **Operations Lead** | Owns the day-to-day of the org. Sets cadence, runs standups (in our case: cron triggers), clears blockers. | Board | All dept coordinators | 🟢 T1 |
| 1.2 | **Repo Steward** | Maintains GitHub repos: hygiene, archiving stale repos, CODEOWNERS, README currency. | Operations Lead | — | 🟢 T1 |
| 1.3 | **Asset Tracker** | Maintains the inventory of all company assets: repos, domains, skills, infra, IP, licenses. | Operations Lead | — | 🟢 T1 |
| 1.4 | **Vendor Coordinator** | Manages vendor relationships: SaaS subscriptions, contractors, service providers. | Operations Lead | — | 🟢 T1 |
| 1.5 | **Compliance Watchdog** | Monitors regulatory + trademark compliance across all surfaces. Triggers the `trademark-compliance-scrub` skill. | Operations Lead | — | 🟢 T1 |
| 1.6 | **Workplace / Office Manager** | Manages physical office (when we have one). Currently not applicable. | Operations Lead | — | 🔴 T4 |
| 1.7 | **Watchdog Engineer** | Owns the watchdog layer (site-health, cron liveness, alert routing). | Operations Lead | — | 🟢 T1 |
| 1.8 | **IT Support Specialist** | Internal IT: laptop provisioning, SSO, access control. Currently Kiki. | Operations Lead | — | 🟡 T2 |
| 1.9 | **Project Manager** | Owns project plans, dependencies, cross-team coordination. | Operations Lead | — | 🟡 T2 |
| 1.10 | **Program Manager** | Manages a portfolio of related projects (vs. PM who owns one). | Operations Lead | Project Managers | 🟠 T3 |
| 1.11 | **Chief of Staff** | Right hand to the CEO. Manages calendar, board prep, internal comms. | CEO / Board | — | 🟠 T3 |
| 1.12 | **Internal Communications Manager** | Owns internal messaging cadence, all-hands, announcements. | Chief of Staff | — | 🟠 T3 |
| 1.13 | **Business Continuity Manager** | Owns disaster recovery, incident response, runbook maintenance. | Operations Lead | — | 🟡 T2 |
| 1.14 | **Travel & Events Coordinator** | Books travel, runs company events. | Operations Lead | — | 🔴 T4 |
| 1.15 | **Procurement Specialist** | Sourcing, vendor evaluation, contract negotiation. (See also 2.6.) | Operations Lead OR Finance Lead | — | 🟡 T2 |

---

# Department 2 — Finance & Legal (18 roles)

Money + contracts + compliance. The only dept with hard USD thresholds.

| # | Role | Definition | Reports to | Supervises | Tier |
|---|------|------------|-----------|------------|------|
| 2.1 | **CFO / Controller** | Owns all financial decisions. Signs off on contracts above threshold. | Board | Bookkeeper, Procurement | 🟢 T1 |
| 2.2 | **Accountant** | Monthly close, P&L, balance sheet, bank reconciliation. | CFO | — | 🟡 T2 |
| 2.3 | **Bookkeeper** | Day-to-day transactions, AP/AR, expense categorization. | CFO OR Accountant | — | 🟢 T1 |
| 2.4 | **AP Specialist** | Accounts Payable — bills, vendor payments. | Bookkeeper | — | 🟡 T2 |
| 2.5 | **AR Specialist** | Accounts Receivable — invoices, collections. | Bookkeeper | — | 🟡 T2 |
| 2.6 | **Procurement Officer** | Vendor sourcing, contract negotiation, renewals. | CFO | — | 🟢 T1 |
| 2.7 | **Legal Counsel** | Contract review, IP protection, regulatory advice. | CFO | — | 🟢 T1 (external contractor) |
| 2.8 | **Compliance Officer** | Owns compliance program (GDPR, LGPD, trademark, etc.). | CFO OR Legal Counsel | — | 🟡 T2 |
| 2.9 | **Tax Specialist** | Quarterly tax filings, year-end returns, transfer pricing. | CFO | — | 🟢 T1 (external accountant) |
| 2.10 | **Contract Drafter** | Drafts NDAs, MSAs, SOWs, employment contracts. | Legal Counsel | — | 🟢 T1 |
| 2.11 | **Payroll Specialist** | Runs payroll for FTEs and contractors. | Bookkeeper | — | 🔴 T4 (no FTEs yet) |
| 2.12 | **Treasurer** | Manages cash, banking, FX, investments. | CFO | — | 🟠 T3 |
| 2.13 | **FP&A Analyst** | Financial planning & analysis: forecasts, budgets, unit economics. | CFO | — | 🟠 T3 |
| 2.14 | **Internal Auditor** | Audits internal controls, expense policy compliance. | CFO | — | 🟠 T3 |
| 2.15 | **Data Protection Officer (DPO)** | Required when handling EU personal data at scale. | CFO OR Legal Counsel | — | 🟠 T3 |
| 2.16 | **Billing Specialist** | Issues invoices, manages recurring billing, collections. | Bookkeeper OR AR Specialist | — | 🟡 T2 |
| 2.17 | **Insurance Specialist** | Manages business insurance: E&O, liability, cyber. | CFO | — | 🟡 T2 |
| 2.18 | **Pricing Analyst** | Maintains pricing benchmarks, runs pricing experiments. | CFO | — | 🟢 T1 |

---

# Department 3 — Sales & Growth (16 roles)

The only revenue-producing dept. Everything else is cost.

| # | Role | Definition | Reports to | Supervises | Tier |
|---|------|------------|-----------|------------|------|
| 3.1 | **Head of Sales / CRO** | Owns the entire revenue function. Sets quotas, signs off on discounts. | Board | AE, SDR, Marketing | 🟢 T1 |
| 3.2 | **SDR (Sales Development Rep)** | Outbound: cold emails, LinkedIn DMs, lead qualification. | Head of Sales | — | 🟢 T1 |
| 3.3 | **Account Executive (AE)** | Inbound + outbound closing: discovery calls, demos, proposals. | Head of Sales | — | 🟢 T1 |
| 3.4 | **Sales Engineer** | Technical pre-sales: demos, scoping, technical Q&A. | Head of Sales | — | 🟡 T2 |
| 3.5 | **Customer Success Manager (CSM)** | Owns post-sale retention, expansion, renewal. | Head of Sales OR COO | — | 🟠 T3 (split from Operations) |
| 3.6 | **Proposal Writer** | Drafts proposals, SOWs, pricing. | Head of Sales | — | 🟢 T1 |
| 3.7 | **Marketing Manager** | Owns marketing strategy, channel mix, content calendar. | Head of Sales | Content Producer | 🟢 T1 |
| 3.8 | **Content Producer** | Writes blog posts, social media, case studies. | Marketing Manager | — | 🟡 T2 |
| 3.9 | **Multimedia Designer** | Video, podcast, graphics, motion design. | Marketing Manager | — | 🟡 T2 |
| 3.10 | **Brand Manager** | Owns brand identity, positioning, voice. | Marketing Manager | — | 🟠 T3 |
| 3.11 | **SEO Specialist** | Owns SEO strategy, keyword research, technical SEO. | Marketing Manager | — | 🟡 T2 |
| 3.12 | **Paid Ads Specialist** | Runs paid acquisition: Google, LinkedIn, Meta (banned for us), TikTok. | Marketing Manager | — | 🟠 T3 |
| 3.13 | **Email Marketing Specialist** | Lifecycle email, drip campaigns, list management. | Marketing Manager | — | 🟡 T2 |
| 3.14 | **Community Manager** | Owns community channels: Discord (banned), forums, social. | Marketing Manager | — | 🟠 T3 |
| 3.15 | **Partnerships Manager** | Manages referral partners, channel partners, integration partners. | Head of Sales | — | 🟡 T2 |
| 3.16 | **Event Coordinator** | Runs webinars, conferences, trade shows. | Marketing Manager | — | 🟠 T3 |

---

# Department 4 — Engineering & Delivery (24 roles)

Where Kiki owns end-to-end. The largest dept by role count because engineering has the most specialization.

| # | Role | Definition | Reports to | Supervises | Tier |
|---|------|------------|-----------|------------|------|
| 4.1 | **CTO / VP Engineering** | Owns all technical decisions. Signs off on schema/infra PRs. | Board | All engineers | 🟢 T1 |
| 4.2 | **Engineering Manager** | Manages a team of engineers: 1:1s, performance, growth. | CTO | Engineers | 🟠 T3 |
| 4.3 | **Backend Engineer** | Server-side: APIs, databases, services. | CTO | — | 🟢 T1 (consolidated in Kiki) |
| 4.4 | **Frontend Engineer** | Client-side: UI, UX, browser code. | CTO | — | 🟢 T1 (consolidated in Kiki) |
| 4.5 | **Full-stack Engineer** | Both backend and frontend. | CTO | — | 🟢 T1 (consolidated in Kiki) |
| 4.6 | **Mobile Engineer** | iOS, Android, React Native, Flutter. | CTO | — | 🔴 T4 (no mobile product yet) |
| 4.7 | **DevOps / SRE Engineer** | Infrastructure, CI/CD, monitoring, incident response. | CTO | — | 🟢 T1 |
| 4.8 | **QA Engineer** | Test automation, manual QA, acceptance criteria. | CTO | — | 🟢 T1 (automated test suite) |
| 4.9 | **Security Engineer** | AppSec, infra security, incident response for breaches. | CTO | — | 🟢 T1 |
| 4.10 | **Data Engineer** | Data pipelines, ETL, data warehouse. | CTO | — | 🔴 T4 (no data product yet) |
| 4.11 | **ML Engineer** | Model training, fine-tuning, inference pipelines. | CTO | — | 🟡 T2 (per-project basis) |
| 4.12 | **Solutions Architect** | Designs custom solutions for clients. | CTO | — | 🟠 T3 |
| 4.13 | **Tech Writer** | Owns documentation: API docs, user guides, runbooks. | CTO | — | 🟡 T2 |
| 4.14 | **Engineering Product Manager** | Bridges engineering and product/business. | CTO | — | 🟠 T3 |
| 4.15 | **Platform Engineer** | Internal developer platform: tooling, environments, golden paths. | CTO | — | 🟠 T3 |
| 4.16 | **Release Manager** | Owns release process: versioning, rollouts, rollback decisions. | CTO OR DevOps | — | 🟠 T3 |
| 4.17 | **Site Reliability Engineer (SRE)** | Specialized DevOps focused on SLOs, error budgets, on-call. | CTO | — | 🟠 T3 |
| 4.18 | **Database Administrator (DBA)** | Owns database operations: backups, performance, schema migrations. | DevOps OR Backend | — | 🟡 T2 |
| 4.19 | **Network Engineer** | Network architecture, firewalls, VPN. | DevOps | — | 🟠 T3 |
| 4.20 | **UI/UX Designer** | Designs user interfaces, runs usability tests. | CTO OR Marketing | — | 🟡 T2 |
| 4.21 | **Product Designer** | End-to-end product design: research, UI, prototyping. | CTO | — | 🟠 T3 |
| 4.22 | **Engineering Operations Specialist** | Improves engineering process: metrics, tools, culture. | Engineering Manager | — | 🟠 T3 |
| 4.23 | **Build / Release Engineer** | Owns build pipelines, artifact management. | DevOps | — | 🟠 T3 |
| 4.24 | **Embedded Systems Engineer** | Firmware, hardware integration. | CTO | — | 🔴 T4 |

---

# Department 5 — Research & Education (12 roles)

The flagship asset dept: thesis, courses, IP. Ivan's domain.

| # | Role | Definition | Reports to | Supervises | Tier |
|---|------|------------|-----------|------------|------|
| 5.1 | **Research Lead** | Sets research agenda, owns flagship outputs (thesis, paper). | Board | Researchers, Writers | 🟢 T1 |
| 5.2 | **Researcher** | Performs the research: literature review, experiments, analysis. | Research Lead | — | 🟢 T1 |
| 5.3 | **Writer / Editor** | Turns research into papers, articles, blog posts. | Research Lead | — | 🟢 T1 |
| 5.4 | **Academic Liaison** | Submits to journals/conferences, manages peer review. | Research Lead | — | 🟡 T2 |
| 5.5 | **Citation / Bibliography Specialist** | Owns citation discipline, reference management. | Writer / Editor | — | 🟢 T1 (sub-agent) |
| 5.6 | **Course Designer** | Designs course curriculum: modules, lessons, exercises. | Research Lead | — | 🟢 T1 |
| 5.7 | **Course Producer** | Produces course content: video, slides, transcripts, worksheets. | Course Designer | — | 🟡 T2 |
| 5.8 | **Instructional Designer** | Specialist in pedagogy: learning objectives, assessments. | Course Designer | — | 🟠 T3 |
| 5.9 | **Subject Matter Expert (SME)** | Domain expert contracted for specific course modules. | Course Designer | — | 🟡 T2 (contractor) |
| 5.10 | **Research Engineer** | Builds tools used in research: eval harnesses, data pipelines. | Research Lead OR CTO | — | 🟡 T2 |
| 5.11 | **IP / Patent Specialist** | Manages patents, trademarks for IP. | Research Lead OR Legal Counsel | — | 🟠 T3 |
| 5.12 | **Publication Coordinator** | Manages publications pipeline: submissions, embargoes, versioning. | Research Lead | — | 🟡 T2 |

---

# Department 6 — People & Culture (8 roles)

Small now, but designed to scale. Currently Ivan + Kiki only; expands at first FTE hire.

| # | Role | Definition | Reports to | Supervises | Tier |
|---|------|------------|-----------|------------|------|
| 6.1 | **Head of People / VP HR** | Owns all people decisions: hiring, growth, culture. | Board | Recruiter, Coach | 🟢 T1 (Ivan + Kiki co-owned) |
| 6.2 | **Recruiter** | Owns hiring pipeline: sourcing, screening, interviewing. | Head of People | — | 🔴 T4 (no FTE hires yet) |
| 6.3 | **Onboarding Specialist** | Designs + runs new-hire onboarding program. | Head of People | — | 🔴 T4 |
| 6.4 | **Performance Coach** | Coaches individuals on growth, goals, feedback. | Head of People | — | 🟢 T1 (`kiki-coach` for Kiki) |
| 6.5 | **Recognition Lead** | Owns milestone recognition, rituals, cultural artifacts. | Head of People | — | 🟢 T1 (deferred to periodic rituals) |
| 6.6 | **Compensation Specialist** | Designs comp bands, bonus plans, equity grants. | Head of People OR CFO | — | 🔴 T4 |
| 6.7 | **People Operations Specialist** | HRIS, benefits administration, time off tracking. | Head of People | — | 🟠 T3 |
| 6.8 | **Learning & Development Manager** | Owns training budget, learning paths, certifications. | Head of People | — | 🟠 T3 |

---

# Cross-Department / Cross-Cutting Roles (5 roles)

These roles span departments and report to the Board or to multiple dept heads.

| # | Role | Definition | Reports to | Supervises | Tier |
|---|------|------------|-----------|------------|------|
| X.1 | **CEO / Managing Director** | Ultimate decision-maker. Sets strategy, signs contracts. | Board | All dept heads | 🟢 T1 (Ivan) |
| X.2 | **CTO** | Technical strategy, architecture decisions. | Board | Engineering dept | 🟢 T1 (Kiki) |
| X.3 | **Board of Directors** | Governance, ratification, cap table. | — | CEO | 🟢 T1 (Ivan + Kiki) |
| X.4 | **Independent Board Director** | External advisor, audit committee. | Board | — | 🔴 T4 (added pre-Series A) |
| X.5 | **Executive Assistant** | Calendar, travel, admin support for CEO. | CEO | — | 🟠 T3 |

---

# Coverage stats

| Dept | Total roles | Tier 1 (staffed now) | Tier 2 (next 6mo) | Tier 3 (12mo+) | Tier 4 (50+) |
|------|-------------|---------------------|-------------------|----------------|--------------|
| Operations | 15 | 7 | 4 | 3 | 1 |
| Finance & Legal | 18 | 7 | 5 | 4 | 2 |
| Sales & Growth | 16 | 5 | 5 | 5 | 1 |
| Engineering & Delivery | 24 | 7 | 3 | 10 | 4 |
| Research & Education | 12 | 5 | 4 | 2 | 1 |
| People & Culture | 8 | 3 | 0 | 2 | 3 |
| Cross-cutting | 5 | 3 | 0 | 1 | 1 |
| **TOTAL** | **98** | **37** | **21** | **27** | **13** |

(98 ≥ 80 target ✅)

---

# Mapping to our canonical 6 departments (Ivan's 15 → our 6)

This is the explicit mapping Ivan asked for ("the 15 departments I named, where do they go?").

| Ivan named | Maps to | Role | Why merged |
|------------|---------|------|------------|
| Finance | Dept 2 (Finance & Legal) | 2.1-2.18 | Direct match |
| HR | Dept 6 (People & Culture) | 6.1-6.8 | Deferred until first FTE |
| Legal | Dept 2 (Finance & Legal) | 2.7, 2.10, 2.15 | Shared spend thresholds |
| Development | Dept 4 (Engineering & Delivery) | 4.1-4.24 | Direct match |
| QA | Dept 4 | 4.8 | A role inside Engineering |
| Operational | Dept 1 (Operations) | 1.1-1.15 | Direct match |
| Research | Dept 5 (Research & Education) | 5.1-5.12 | Direct match |
| Management | Cross-cutting | X.1, X.2 | A layer above depts |
| Board | Cross-cutting | X.3, X.4 | 2 people = board |
| Inventory | Dept 1 | 1.3 (Asset Tracker) | A SOP, not a dept |
| Buying / Procurement | Dept 2 | 2.6 (Procurement Officer) | A SOP, not a dept |
| Accounting | Dept 2 | 2.2, 2.3 (Accountant, Bookkeeper) | A SOP, not a dept |
| Marketing | Dept 3 (Sales & Growth) | 3.7-3.16 | Same ICP as sales |
| Multimedia | Dept 3 | 3.9 | Marketing deliverable |
| OpSec | Dept 4 | 4.9 (Security Engineer) | A specialist inside Engineering |

---

# See also

- `/opt/data/source-materials/topics/org-design/literature.md` — strategic synthesis
- `/opt/data/source-materials/topics/org-design/INDEX.md` — source provenance
- `/opt/data/source-materials/topics/org-design/cheatsheet.md` — org-size decision table
- `/opt/data/agents/departments/ORG-AGENTS.md` — our constitutional state
- Session 2 (next): builds the Role × Tool × SOP catalog from this glossary
