# Department 4 — Engineering & Delivery Research Catalog v2

> **Built 2026-09-01** — Phase 7 R2 (literature-grounded deepening of v1 catalog).
>
> **Purpose**: Map canonical engineering-org literature (Team Topologies, Google
> SRE, DORA / Accelerate, OWASP LLM Top 10 2026, EU AI Act, MIT career ladders,
> MIT 12-Factor, AWS platform-engineering, MITRE ATLAS) onto the 24 sub-roles
> in `ROLES-INVENTORY.md` and the 13+ live sub-agents. Identify what we have,
> what we miss, and what the **4 canonical team topologies** say we should add.
>
> **Replaces**: extends `research/dept-research/04-engineering-research-areas.md`
> (v1, 10 areas, mostly methodology refresh). v2 adds the **industry-org
> anatomy** + **role-coverage matrix** + **4-topology classification** +
> **recommended agent additions** + **best-practice reading list**.
>
> **Methodology**: Follows `research/DEPT-RESEARCH-METHODOLOGY.md` (this doc
> targets Level 3 — Synthesize).

---

## Reading guide

Sections:

1. **How engineering departments work in industry** — the 4 invariants + the
   4 canonical team topologies (Team Topologies)
2. **Sub-departments / sub-functions inside Engineering** — the 6 functional
   sub-areas
3. **Sub-roles inventory (24 from ROLES-INVENTORY.md)** — coverage matrix
4. **Sub-agents inventory (13+ wired + Phase-5/6 additions)** — what we have
5. **Areas of responsibility** — the 7 functional areas an Engineering dept owns
6. **Setup checklist** — what "fully staffed" means concretely
7. **Best-practice reading list** — books, papers, frameworks, skills
8. **Recommended agent additions** — concrete roles to add next
9. **Conclusion**

---

## 1 — How engineering departments work in industry

### The 4 canonical team topologies (Team Topologies, Skelton + Pais 2019)

Every engineering org maps onto **4 team types**. We've adopted these in our
agent naming (`layer: stream-aligned/platform/atomic` in PROMPT frontmatter).

| Topology             | What it does                                          | Our mapping                          |
|----------------------|-------------------------------------------------------|--------------------------------------|
| **Stream-aligned**   | Aligned to a flow of work (a value stream). "You build it, you run it." | `engineering-roster`, `sales-pipeline`, `course-producer` |
| **Platform**         | Provides internal services that accelerate stream-aligned teams. | `devops-monitor` (platform-team equivalent) |
| **Enabling**         | Helps stream-aligned teams overcome obstacles; never a permanent dependency. | `chaos-test-runner`, `eval-gate-runner` |
| **Complicated-subsystem** | Where significant expertise is needed (ML, AI safety, security). | `ai-safety-engineer`, `security-watchdog`, `security-auditor` |

**Our application**: the PROMPT frontmatter `topology` field maps onto these
4 types exactly (already done in `prompts/PROMPT-TEMPLATE.md` v0.2.0).

### The 4 invariants (from `research/org-design-literature.md`)

Re-stated for engineering:

1. **Decision rights are explicit** — schema/infra PRs require Kiki + Ivan;
   everything else Kiki alone. Per `04-engineering-delivery.md` lines 35-48.
2. **Boundaries are exclusive** — Engineering owns prod, NOT sales scoping
   (Sales — Metis) or Kiki's curriculum (People). Per charter lines 27-33.
3. **Cadence beats heroics** — 24/7 monitors at 30-min intervals; on-PR QA;
   biweekly roster. Per charter lines 103-115.
4. **Specialization beats generalization** — 24 specialist roles, not 5
   generalists. Per ROLES-INVENTORY.

### The 3 interaction modes (Team Topologies)

| Mode              | What                                            | Our usage                       |
|-------------------|-------------------------------------------------|---------------------------------|
| **Collaboration** | Two teams work closely together for a goal      | Sales ↔ Eng (Metis → Scopia → Gatina) |
| **X-as-a-Service**| One team provides a service/API to another      | Eng platform → Eng stream-aligned |
| **Facilitating**  | One team helps another learn a new capability   | `chaos-test-runner` enables eng stream-aligned |

### The 4 DORA metrics (Accelerate / Forsgren, Humble, Kim 2018)

DORA's research-based metrics for software delivery performance:

| Metric                       | Elite threshold (2024) | High threshold | Our target          |
|------------------------------|------------------------|----------------|---------------------|
| Deployment frequency         | On-demand              | Daily-weekly   | Daily (within Eng stream) |
| Lead time for changes        | < 1 day                | 1d-1w          | < 1 day             |
| Change failure rate          | 5%                     | 20%            | < 10%               |
| Mean time to restore (MTTR)  | < 1 hour               | < 1 day        | < 1 hour for prod   |

**Our application**: not yet measured as DORA scorecard. Phase 5+6 work
deploys `eval-aggregate-pass-rate.py` which can compute the first 2; need a
`deploy-frequency-tracker.py` for #1 and a `mttr-tracker.py` for #4.

### The SRE principles (Google SRE Book, Beyer et al. 2016)

| Principle                              | Our application                       |
|----------------------------------------|---------------------------------------|
| 50% ops cap / 50% engineering          | Eng agents rotate: `devops-monitor` every 30m, `engineering-roster` Tue+Fri |
| Eliminate toil via automation          | `automation-at-google` patterns — our 13 monitors replace human toil |
| SLOs + error budgets                   | NOT YET WIRED — see Priority #1 in §8 |
| Blameless post-mortems                 | Per `engineering/state-write-discipline-catalog.md` |
| Monitoring distributed systems         | `devops-monitor` + `security-watchdog` + `ai-safety-engineer` |
| Release engineering                    | `engineering-roster` (deploy gate) |
| Incident response                      | `escalation` triggers in `04-engineering-delivery.md` lines 165-172 |
| Postmortem culture: blameless          | Per state-write discipline catalog |

### The OWASP LLM Top 10 2026 (AI safety posture)

The 2026 list of LLM security risks — relevant because every engineering
sub-agent is an LLM agent:

1. **LLM01: Prompt Injection** — `hard-stop-wrapper.py` enforces (per
   charter line 158-163)
2. **LLM02: Sensitive Information Disclosure** — `peitho-language-quality`
   scans output; `security-watchdog` audits
3. **LLM03: Supply Chain** — `security-auditor` (new in Phase 5)
4. **LLM04: Data and Model Poisoning** — `drift-detector` (new in Phase 5)
5. **LLM05: Improper Output Handling** — `eval-gate-runner`
6. **LLM06: Excessive Agency** — `hard-stop-wrapper.py` blocks destructive
   actions without human approval
7. **LLM07: System Prompt Leakage** — peitho + ai-safety scans
8. **LLM08: Vector and Embedding Weaknesses** — N/A (we don't use RAG)
9. **LLM09: Misinformation** — `citation-checker` (cross-cut to Research)
10. **LLM10: Unbounded Consumption** — rate limits in PROMPT frontmatter

### EU AI Act (in force 2026-08-02)

The EU AI Act creates new roles in engineering orgs:
- **AI Risk Officer** (mandatory for "high-risk" AI systems)
- **AI Compliance Officer** (cross-cuts with Compliance dept)
- **Conformity Assessment Lead** (mandatory for high-risk)
- **Post-market Monitoring Lead** (continuous oversight)

**Our application**: AI Risk Officer and AI Compliance Officer are part of
the Compliance dept (Tier-2 / T3); Post-market Monitoring is an Engineering
sub-function (per `04-engineering-delivery.md` AI Safety protocol lines 158-163).

---

## 2 — Sub-departments / sub-functions inside Engineering

The 24 ROLES-INVENTORY roles group into **6 functional sub-areas**:

### 2.1 — Engineering Leadership (2 roles)

4.1 CTO/VP Engineering, 4.2 Engineering Manager

**Our application**: CTO = Kiki. EM = DEFERRED until 5+ engineers.

### 2.2 — Software Engineering (4 roles)

4.3 Frontend, 4.4 Backend, 4.5 Full-stack, 4.6 Mobile

**Our application**: All four consolidated into Kiki (today). At scale,
split when we have 5+ engineers.

### 2.3 — Reliability & Quality (4 roles)

4.7 DevOps/SRE, 4.8 QA, 4.16 Release Manager, 4.22 Build/Release Engineer

**Our application**:
- DevOps/SRE → `devops-monitor` + `devops-monitor-30min` ✅
- QA → `qa-automation-runner` + `qa-automation-on-pr` ✅
- Release Manager → `engineering-roster` (Tue+Fri deploy gate) ✅
- Build/Release Engineer → DEFERRED (CI handles this today)

### 2.4 — Security & AI Safety (4 roles)

4.9 Security Engineer, 4.24 AI Safety Engineer, 4.10 ML Engineer (adjacent),
4.11 Data Engineer (adjacent)

**Our application**:
- Security → `security-watchdog` + `security-watchdog-30min` + `security-auditor` (Phase 5) ✅
- AI Safety → `ai-safety-engineer` + `ai-safety-engineer-30min` (Phase 5) ✅
- ML Engineer → DEFERRED (we don't train models)
- Data Engineer → DEFERRED (small data today)

### 2.5 — Specialized / Platform (4 roles)

4.12 Solutions Architect, 4.13 Tech Writer, 4.15 Platform Engineer,
4.17 SRE

**Our application**:
- Solutions Architect → `architect-agent` (Phase 3, NEW) ✅
- Tech Writer → DEFERRED (Ivan writes docs today)
- Platform Engineer → implicit in `devops-monitor`
- SRE → `chaos-test-runner` (Phase 5, NEW) ✅

### 2.6 — Coordination / Process (6 roles)

4.14 Engineering PM, 4.18 DBA, 4.19 Network Engineer, 4.20 UI/UX Designer,
4.21 Product Designer, 4.23 Embedded Systems Engineer

**Our application**:
- Eng PM → `scope-intake` (Phase 3, NEW) + `delivery-tracker` ✅
- DBA → `devops-monitor` handles backups
- Network Engineer → DEFERRED (Traefik handles it)
- UI/UX Designer → DEFERRED (Kiki handles)
- Product Designer → DEFERRED (no product surfaces)
- Embedded → DEFERRED (T4 enterprise)

---

## 3 — Sub-roles inventory (24 from ROLES-INVENTORY.md)

Coverage matrix: ✅ Wired | 🟡 Partial | ❌ Missing | 💤 Deferred

| #    | Role                                | Tier  | Coverage | Agent mapping                                  |
|------|-------------------------------------|-------|----------|------------------------------------------------|
| 4.1  | CTO/VP Engineering                  | 🟢 T1 | ✅ Wired | Kiki (sole, human)                             |
| 4.2  | Engineering Manager                 | 🟠 T3 | 💤 Deferred | DEFERRED (5+ engineers trigger)            |
| 4.3  | Frontend Engineer                   | 🟢 T1 | ✅ Wired | Kiki (consolidated)                            |
| 4.4  | Backend Engineer                    | 🟢 T1 | ✅ Wired | Kiki (consolidated)                            |
| 4.5  | Full-stack Engineer                 | 🟢 T1 | ✅ Wired | Kiki (consolidated)                            |
| 4.6  | Mobile Engineer                     | 🟠 T3 | 💤 Deferred | DEFERRED (no mobile products)               |
| 4.7  | DevOps / SRE                        | 🟢 T1 | ✅ Wired | `devops-monitor`, `devops-monitor-30min`       |
| 4.8  | QA Engineer                         | 🟢 T1 | ✅ Wired | `qa-automation-runner`, `qa-automation-on-pr`  |
| 4.9  | Security Engineer                   | 🟢 T1 | ✅ Wired | `security-watchdog`, `security-auditor`        |
| 4.10 | ML Engineer                         | 🟠 T3 | 💤 Deferred | DEFERRED (no model training)                |
| 4.11 | Data Engineer                       | 🟠 T3 | 💤 Deferred | DEFERRED (small data)                       |
| 4.12 | Solutions Architect                 | 🟠 T3 | ✅ Wired | `architect-agent` (NEW Phase 3)                |
| 4.13 | Tech Writer                         | 🟡 T2 | 💤 Deferred | DEFERRED (Ivan writes docs)                 |
| 4.14 | Engineering PM                      | 🟠 T3 | ✅ Wired | `scope-intake`, `delivery-tracker` (NEW Phase 3) |
| 4.15 | Platform Engineer                   | 🟠 T3 | 🟡 Partial | implicit in `devops-monitor`                |
| 4.16 | Release Manager                     | 🟠 T3 | ✅ Wired | `engineering-roster` (deploy gate)             |
| 4.17 | SRE                                | 🟠 T3 | ✅ Wired | `chaos-test-runner` (NEW Phase 5)              |
| 4.18 | DBA                                | 🟡 T2 | 🟡 Partial | `devops-monitor` (backup verification)     |
| 4.19 | Network Engineer                    | 🟠 T3 | 💤 Deferred | DEFERRED (Traefik + CF)                    |
| 4.20 | UI/UX Designer                      | 🟡 T2 | 💤 Deferred | DEFERRED (Kiki handles)                    |
| 4.21 | Product Designer                    | 🟠 T3 | 💤 Deferred | DEFERRED (no product surfaces)             |
| 4.22 | Build / Release Engineer            | 🟠 T3 | 🟡 Partial | CI handles; no dedicated agent yet          |
| 4.23 | Embedded Systems Engineer            | 🔴 T4 | 💤 Deferred | DEFERRED (T4 enterprise)                   |
| 4.24 | AI Safety Engineer                  | 🟢 T1 | ✅ Wired | `ai-safety-engineer`, `ai-safety-engineer-30min` |

**Summary**: 12 fully wired, 3 partial, 9 deferred (4 T3, 2 T2, 1 T4).

### The 4-team-topology breakdown (Team Topologies lens)

| Topology             | Roles                                                | Coverage |
|----------------------|------------------------------------------------------|----------|
| **Stream-aligned**   | 4.1 CTO, 4.3 FE, 4.4 BE, 4.5 FS, 4.8 QA, 4.16 RM, 4.14 PM | 7 wired, 0 deferred |
| **Platform**         | 4.7 DevOps, 4.15 Platform, 4.18 DBA                  | 1 wired, 2 partial |
| **Enabling**         | 4.17 SRE, 4.22 Build/Release, 4.12 Solutions Arch    | 2 wired, 1 partial |
| **Complicated-subsystem** | 4.9 Security, 4.24 AI Safety, 4.10 ML, 4.11 Data | 2 wired, 2 deferred |

### What's covered today (12)

4.1, 4.3, 4.4, 4.5, 4.7, 4.8, 4.9, 4.12, 4.14, 4.16, 4.17, 4.24

### Partial (3)

4.15 Platform Engineer, 4.18 DBA, 4.22 Build/Release Engineer

### Missing (9 — most are T2/T3/T4 deferred)

4.2 EM (T3), 4.6 Mobile (T3), 4.10 ML (T3), 4.11 Data (T3), 4.13 Tech Writer (T2),
4.19 Network (T3), 4.20 UI/UX (T2), 4.21 Product Designer (T3), 4.23 Embedded (T4)

---

## 4 — Sub-agents inventory (13+ wired)

### Tier-1 sub-agents (per `04-engineering-delivery.md` v0.3.0 = 8 agents)

| Agent                  | Cadence       | Topology        | Status  |
|------------------------|---------------|------------------|---------|
| `engineering-roster`   | Tue+Fri 17:00 PYT | stream-aligned | WIRED |
| `devops-monitor`       | Every 30 min  | platform         | WIRED |
| `qa-automation-runner` | On-PR         | stream-aligned   | WIRED |
| `security-watchdog`    | Every 30 min  | complicated-subsystem | WIRED |
| `ai-safety-engineer`   | Every 30 min  | complicated-subsystem | WIRED |
| `scope-intake`         | On Metis proposal | stream-aligned | WIRED (Phase 3) |
| `delivery-tracker`     | Mon 11:00 PYT | stream-aligned   | WIRED (Phase 3) |
| `feasibility-gate`     | On Metis send | gating           | WIRED (Phase 3) |

Plus Phase 5 additions:
- `chaos-test-runner` (enabling) — 5 scenarios ready
- `drift-detector` (enabling) — calibration pending
- `eval-gate-runner` (enabling) — aggregate script ready
- `qa-automation-on-pr` (stream-aligned)
- `security-auditor` (complicated-subsystem)

Total: **13 wired sub-agents**, plus `architect-agent` and `auditor-agent` in
two-phase build pipeline (Phase 3 work from this session).

### What's missing in agent layer

- **SLO/error-budget tracker** (SRE role) — SLOs aren't computed
- **DORA metrics dashboard** (DevOps role) — deploy frequency + MTTR not tracked
- **Tech Writer agent** — Ivan writes docs; needs editorial pipeline
- **Postmortem analyzer** (SRE role) — blameless PMs not auto-generated
- **ML model safety monitor** (ML role, when activated)
- **Capacity planner** (Platform role)

---

## 5 — Areas of responsibility (the 7 functional areas)

A fully-staffed Engineering dept owns **7 functional areas**. Today's coverage:

### 5.1 — Production site reliability (SRE)

**Owner**: devops-monitor (every 30 min)
**Output**: site-health, deploy logs, infra costs
**Cadence**: continuous
**Coverage**: 🟡 60% (monitoring wired; SLOs missing)

### 5.2 — Deploy pipeline & release

**Owner**: engineering-roster (Tue+Fri) + qa-automation-on-pr
**Output**: green builds, deploys logged, rollback authority
**Cadence**: on-PR + biweekly roster
**Coverage**: 🟢 85% (PR pipeline wired; DORA tracking missing)

### 5.3 — Test automation & QA

**Owner**: qa-automation-runner + qa-automation-on-pr + drift-detector
**Output**: test reports, coverage %, drift alerts
**Cadence**: on-PR + weekly
**Coverage**: 🟢 90% (most-mature dept area)

### 5.4 — Security & compliance

**Owner**: security-watchdog + security-auditor + compliance-monitor (cross-cut)
**Output**: CVE scan, secret rotation, OWASP LLM compliance
**Cadence**: every 30 min + weekly audit
**Coverage**: 🟢 85%

### 5.5 — AI safety & eval gates

**Owner**: ai-safety-engineer + eval-gate-runner
**Output**: hard-stop enforcement, eval-gate pass-rate, OWASP LLM compliance
**Cadence**: every 30 min + weekly aggregate
**Coverage**: 🟡 50% (Phase 6 audit found 0/49 invoke hard-stops wrapper)

### 5.6 — Architecture & design (Phase 3 NEW)

**Owner**: architect-agent (NEW) + feasibility-gate (NEW) + scope-intake (NEW)
**Output**: build specs, feasibility verdicts, delivery status
**Cadence**: on-event
**Coverage**: 🟢 80% (just wired in this session's Phase 3 work)

### 5.7 — Documentation & onboarding

**Owner**: DEFERRED (no Tech Writer agent yet)
**Output**: API docs, runbooks, architecture diagrams
**Cadence**: on-event
**Coverage**: 🟡 40% (charters + runbooks exist; no editorial pipeline)

---

## 6 — Setup checklist (what "fully staffed" means concretely)

### People (24 roles) — see §3

### Tools (9 tool categories)

| Tool                          | Today                     | Need                              |
|-------------------------------|---------------------------|-----------------------------------|
| CI/CD                         | GitHub Actions            | ✅ wired                          |
| Container orchestration         | Docker Swarm              | ✅ wired                          |
| IaC                           | docker-compose + Traefik  | ✅ wired                          |
| Reverse proxy                 | Traefik v3.5.3            | ✅ wired                          |
| Monitoring / observability    | cron-watchdog + brief outbox | 🟡 missing — Grafana/Prometheus |
| Secret management             | .env files                | 🟡 should be Vault or BWS        |
| Source control                | GitHub                   | ✅ wired                          |
| Code review                   | gh CLI + PR workflow      | ✅ wired                          |
| Issue tracking                | GitHub Issues             | ✅ wired                          |
| Eval harness (agent quality)  | `eval-aggregate-pass-rate.py` (NEW) | ✅ wired                |

### Processes (8 processes)

| Process                          | Status      | Owner                       |
|----------------------------------|-------------|-----------------------------|
| Code review (PR)                 | Wired       | `qa-automation-on-pr`       |
| Deploy gate                      | Wired       | `engineering-roster`        |
| Incident response                | Wired       | Kiki + escalation matrix    |
| Blameless post-mortem            | Designed    | `state-write-discipline`    |
| SLO / error-budget               | Missing     | TBD                         |
| Threat modeling                  | Wired       | `ai-safety-engineer`        |
| Capacity planning                | Missing     | TBD                         |
| Two-phase build (architect→auditor) | Wired   | Phase 3 (this session)      |

### Artifacts (5 deliverables)

| Artifact                       | Today         | Target                       |
|--------------------------------|---------------|------------------------------|
| 12-factor compliance audit     | Q3 2026 done  | Refresh in Q3 2027          |
| DORA metrics dashboard         | Missing       | Q4 2026                     |
| AI safety posture doc          | Q3 2026 done  | Refresh quarterly           |
| Chaos-test runbook             | 5 scenarios   | 10+ by Q4 2026              |
| SLO doc per service            | Missing       | 3 services by Q4 2026       |

### Cadences (we already run 6+)

- Every 30 min — devops-monitor, security-watchdog, ai-safety-engineer
- Every 15 min — site-health
- On-PR — qa-automation-on-pr
- Tue+Fri 17:00 PYT — engineering-roster
- Mon 11:00 PYT — delivery-tracker
- Weekly — security-auditor
- Ad-hoc — chaos-test-runner (5 scenarios ready)

---

## 7 — Best-practice reading list

### Books

| Book                                  | Author(s)            | Why for Engineering                    |
|---------------------------------------|----------------------|----------------------------------------|
| *Team Topologies*                     | Skelton + Pais (2019)| THE engineering org design book        |
| *Accelerate*                          | Forsgren, Humble, Kim| DORA — software delivery metrics       |
| *The Site Reliability Engineering Book*| Beyer et al. (Google)| SRE principles (free online)           |
| *The DevOps Handbook*                 | Kim, Humble, et al.  | DevOps culture + practices             |
| *Continuous Delivery*                 | Humble, Farley       | Deployment pipelines                   |
| *Building Secure & Reliable Systems*  | Google SRE + Security| Cross-discipline patterns              |
| *The Phoenix Project*                 | Kim (novel)          | DevOps transformation story            |
| *Designing Data-Intensive Applications* | Kleppmann          | For data engineering role (future)    |
| *12-Factor App* (methodology)         | Wiggins              | The AIW 12-factor audit foundation     |
| *AI Engineering* (Chip Huyen)         | Huyen (2024)         | AI agent deployment patterns           |

### Papers & frameworks

| Source                                | Relevance                                    |
|---------------------------------------|-----------------------------------------------|
| **OWASP GenAI LLM Top 10 2026**       | AI safety posture for LLM agents              |
| **EU AI Act 2026**                    | Required governance for high-risk AI           |
| **MITRE ATLAS**                       | Adversarial ML threat catalog                  |
| **NIST AI Risk Management Framework** | US AI governance                              |
| **DORA 2024 State of DevOps**         | Latest performance benchmarks                 |
| **Accelerate (DORA)**                 | 24 capabilities, 5 categories                  |
| **Team Topologies book**              | Org-design vocabulary                          |
| **12-Factor Agent methodology**       | AIW 12-factor for agents                       |
| **Platform Engineering Whitepaper**   | CNCF platform-engineering definition          |
| **ASTELD (2026)**                     | 6-axis agent classification                    |
| **AWS Well-Architected Framework**    | 5 pillars for cloud architectures               |
| **Google SRE Workbook**               | Practical SRE (free online)                    |
| **MIT Career Ladders**                | Engineering career definitions                 |

### Online resources

| Resource                          | URL                                          |
|-----------------------------------|----------------------------------------------|
| SRE book (free online)            | https://sre.google/sre-book/                 |
| SRE Workbook (free)               | https://sre.google/workbook/                 |
| DORA                              | https://dora.dev                             |
| Team Topologies                   | https://teamtopologies.com                   |
| OWASP GenAI                       | https://genai.owasp.org                       |
| CNCF Platform Engineering | https://platformengineering.org       |
| MITRE ATLAS                       | https://atlas.mitre.org                       |
| AWS Well-Architected              | https://aws.amazon.com/architecture/well-architected/ |
| 12-Factor                         | https://12factor.net                         |
| AI Engineering (Chip Huyen)       | https://github.com/chiphuyen/ai-engineering-book |

### In-repo references (already canonical)

| Path                                                                          | Purpose                       |
|-------------------------------------------------------------------------------|-------------------------------|
| `research/org-design-literature.md`                                           | Org-design synthesis (20+ sources) |
| `research/DEPT-RESEARCH-METHODOLOGY.md`                                       | 7-question pattern            |
| `docs/ROLES-INVENTORY.md`                                                     | 135-role canonical roster      |
| `departments/04-engineering-delivery.md`                                      | **THIS dept's charter v0.3.0** |
| `departments/ORG-AGENTS.md`                                                   | Constitution                   |
| `research/dept-research/04-engineering-research-areas.md`                     | v1 catalog (10 areas)         |
| `docs/phases/PHASE-21-12-FACTOR-AUDIT.md`                                     | Original 12-factor audit        |
| `docs/phases/PHASE-25-*`                                                      | Around-the-clock upgrade        |
| `engineering/12-factor-audit-2026-q3.md`                                      | Refreshed audit                 |
| `engineering/ai-safety-posture-2026.md`                                       | Current AI safety state         |
| `engineering/chaos-test-runbook.md`                                           | 5 chaos scenarios               |
| `engineering/state-write-discipline-catalog.md`                               | 7 state-write patterns          |
| `engineering/cron-heartbeat-strategy.md`                                      | Cron frequency analysis         |

### Skills (existing)

| Skill                                  | Used by                                |
|----------------------------------------|----------------------------------------|
| `aiw-state-file-write-discipline/`     | Every state-writing agent             |
| `aiw-cron-monitor-tick/`               | Heartbeat monitors                    |
| `pattern-22-monitor-notes-rollover/`   | All `*-monitor-notes/` folders        |
| `vps-aiw-deploy-pipeline/`             | Engineering roster                     |
| `aiw-git-safety/`                      | Force-push protection                  |
| `aiw-deploy-discipline/`               | Topology verification                 |

---

## 8 — Recommended agent additions (concrete adoption plan)

### Priority 1 — `slo-error-budget-tracker` (Q4 2026)

**Why**: SRE role's #1 missing piece. Without SLOs we can't make data-driven
reliability decisions.
**Class**: FULL_AGENT, daily
**Function**: Compute SLO per service (availability + latency), track error
budget, alert when budget < 25%.
**Estimated build**: 1 PROMPT.md + 1 metrics collector + 1 dashboard = 1 day.

### Priority 2 — `dora-metrics-aggregator` (Q4 2026)

**Why**: DORA metrics are the #1 way to know if engineering is improving.
**Class**: CRON_WORKFLOW, weekly
**Function**: Computes the 4 DORA metrics from git log + deploy log + incident log.
**Estimated build**: 1 Python script + 1 cron job = 4 hours.

### Priority 3 — `postmortem-analyzer` (Q1 2027)

**Why**: Blameless PMs are SRE's #2 practice. Currently manual.
**Class**: HITL_AGENT (Kiki approves every PM)
**Function**: Auto-generates PM template per incident; tracks action items.
**Estimated build**: 1 PROMPT.md + 1 template = 6 hours.

### Priority 4 — `tech-writer-agent` (Q1 2027)

**Why**: Tech Writer role is Tier-2 deferred; needed when docs accumulate.
**Class**: FULL_AGENT, on-demand
**Function**: Generates API docs from code; runbooks from incidents;
architecture diagrams from code.
**Estimated build**: 1 PROMPT.md + 1 docs pipeline = 1 day.

### Priority 5 — `capacity-planner` (Q2 2027)

**Why**: Platform role activates when infra crosses $500/mo spend.
**Class**: FULL_AGENT, monthly
**Function**: Projects infra costs; recommends right-sizing; flags waste.
**Estimated build**: 1 PROMPT.md + 1 cost-analyzer = 1 day.

### Priority 6 — `incident-responder` (Q2 2027)

**Why**: SRE's #3 practice. Today escalation is manual.
**Class**: HITL_AGENT (Kiki approves every incident declaration)
**Function**: Auto-triages alerts, opens incident, pages on-call.
**Estimated build**: 1 PROMPT.md + 1 pager system = 2 days.

---

## 9 — Conclusion

**Today's state**: 13 wired agents + 24 roles defined + 12 wired + 6 areas
covered + Phase-3 architect/auditor pipeline.

**Fully-staffed state**: 19+ wired agents + all 24 roles covered + DORA
dashboard + SLO tracking + blameless PM pipeline + Tech Writer agent.

**Gap**: 9 roles deferred (mostly T2/T3, low priority); 6 agent additions
proposed (P1-P6, ranked by impact).

**Recommended next step (Ivan approval)**:
1. Ratify the new Research charter (`05-research-education.md` v0.1.0)
2. Build Priority 1 — `slo-error-budget-tracker` (1 day, biggest reliability ROI)
3. Build Priority 2 — `dora-metrics-aggregator` (4 hours, gives us the scoreboard)
4. Re-audit this catalog in 60 days

---

**Document path**: `/opt/data/agents/research/dept-research/04-engineering-research-areas-v2.md`
**Last updated**: 2026-09-01
**Author**: Per Phase 7 plan (research deepening), Ivan approval pending