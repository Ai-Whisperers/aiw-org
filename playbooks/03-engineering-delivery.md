# 03 — Engineering & Delivery Playbook

> Department charter + roles + agents + tooling + SOPs for Engineering.
> **Last updated**: 2026-08-14

---

## Engineering & Delivery — Department Charter

**Mission**: Ship client sites, maintain infra uptime, keep the ParaguAI Builder running, deploy changes safely. Engineering is where Kiki owns end-to-end.

**Head**: Kiki (CTO/Co-Founder & Technical Director)
**Sub-functions**: AI Safety (Tier 2)

---

## Roles (24 roles)

| # | Role | Tier | Status |
|---|------|------|--------|
| 4.1 | CTO/VP Engineering | 🟢 T1 | Kiki |
| 4.2 | Engineering Manager | 🟠 T3 | deferred (need 5+ engineers first) |
| 4.3 | Frontend Engineer | 🟢 T1 | Kiki (consolidated) |
| 4.4 | Backend Engineer | 🟢 T1 | Kiki (consolidated) |
| 4.5 | Full-stack Engineer | 🟢 T1 | Kiki (consolidated) |
| 4.6 | Mobile Engineer | 🟠 T3 | deferred (no mobile product) |
| 4.7 | DevOps / SRE Engineer | 🟢 T1 | sub-agent: devops-monitor |
| 4.8 | QA Engineer | 🟢 T1 | automated test suite (CRON_WORKFLOW) |
| 4.9 | Security Engineer | 🟢 T1 | sub-agent: security-watchdog |
| 4.10 | ML Engineer | 🟠 T3 | deferred (no ML product) |
| 4.11 | Data Engineer | 🟠 T3 | deferred (no data product) |
| 4.12 | Solutions Architect | 🟠 T3 | deferred |
| 4.13 | Tech Writer | 🟡 T2 | deferred |
| 4.14 | Engineering Product Manager | 🟠 T3 | deferred |
| 4.15 | Platform Engineer | 🟠 T3 | deferred |
| 4.16 | Release Manager | 🟠 T3 | Kiki + sub-agent |
| 4.17 | Site Reliability Engineer (SRE) | 🟠 T3 | promote from DevOps when scale demands |
| 4.18 | Database Administrator (DBA) | 🟡 T2 | sub-agent |
| 4.19 | Network Engineer | 🟠 T3 | deferred |
| 4.20 | UI/UX Designer | 🟡 T2 | deferred |
| 4.21 | Product Designer | 🟠 T3 | deferred |
| 4.22 | Engineering Operations Specialist | 🟠 T3 | deferred |
| 4.23 | Build / Release Engineer | 🟠 T3 | deferred |
| 4.24 | AI Safety Engineer | 🟢 T1 | sub-agent: ai-safety-engineer |

---

## Sub-agents (Tier 2)

| Agent | Cadence | Mission |
|-------|---------|---------|
| `engineering-roster` | Tue+Fri 17:00 PYT | Deploy health, PR queue, Kiki workload |
| `devops-monitor` | Every 30 min | Docker Swarm, Traefik, CF Workers |
| `qa-automation-runner` | On-PR | Runs test suite |
| `security-watchdog` | Every 30 min | Scans for vulnerabilities, watches for exposed credentials |
| `ai-safety-engineer` | Every 30 min | OWASP LLM Top 10 compliance, hard-stop enforcement |

---

## Tooling

### CTO / Engineering Lead (Kiki)
- **Code editor**: Cursor
- **Version control**: GitHub (`Ai-Whisperers/` org)
- **CI/CD**: GitHub Actions
- **Code review**: `gh pr review` + humans
- **Pre-commit**: husky + lint-staged

### DevOps / SRE
- **Containers**: Docker + Docker Swarm
- **Reverse proxy**: Traefik v3.5.3
- **Object storage**: Cloudflare R2
- **Static deploys**: CF Worker + R2
- **Backups**: Rclone to R2

### Frontend / Backend
- **Framework**: Next.js (App Router)
- **CSS**: Tailwind v4
- **State**: React Query
- **Testing**: Playwright + Vitest

### QA
- **Test runner**: Vitest (unit), Playwright (E2E)
- **Coverage**: 95% lines / 90% branches in `src/lib`
- **CI gates**: typecheck + invariant checker + tests + build

### Security
- **Secret management**: GitHub Actions secrets (`LIGARE_*`)
- **Scanning**: OWASP LLM Top 10 compliance for agents
- **Access**: CODEOWNERS file per repo

---

## Stack reality (per `04-engineering-delivery.md` lines 86-95)

- **Hostinger VPS** (38.9.96.179) — primary prod, 32GB RAM, 387GB disk
- **Servarica Host A** — secondary infra
- **Traefik v3.5.3** reverse proxy with auto-LE
- **Docker Swarm** orchestrator (NOT K8s)
- **CF Worker + R2** for static deploys
- **Vercel 403** — DO NOT attempt deploys there

---

## SOPs

### Daily
- Tue+Fri 17:00 PYT: engineering-roster cron

### Continuous
- Every 30 min: devops-monitor
- Every 30 min: security-watchdog
- Every 30 min: ai-safety-engineer
- Every 15 min: site-health (existing, on Engineering ownership)

### On-PR
- qa-automation-runner (test suite)
- Pre-commit: husky + lint-staged
- GitHub Actions: typecheck + build

### Monthly
- Quarterly: stack review, dependency updates

---

## Hard stops (Engineering dept)

| Action | Authority |
|--------|-----------|
| Merge PR (no breaking changes) | Kiki or designated reviewer |
| Merge PR (schema change, infra) | Kiki + Ivan |
| Hotfix deploy to prod | Kiki (logged, Ivan notified) |
| Rollback deploy | Kiki (logged) |
| New tool subscription < $50/mo | Kiki |
| New tool subscription > $50/mo | Kiki + Ivan |
| Add new client repo to deploy pipeline | Kiki |
| Deprecate / archive a repo | Kiki (logs to engineering.json) |
| Edit canonical narrative / pricing docs | Ivan only |

---

## State schema (`state/engineering.json`)

```json
{
  "last_run": null,
  "deploys_7d": [],
  "open_prs": [],
  "stale_repos_7d": [],
  "incidents_72h": [],
  "kiki_commits_7d": 0,
  "infra_costs_monthly_usd": null,
  "tools_pending_decision": []
}
```

---

## Skills stack

- `vps-aiw-deploy-pipeline` — CF Worker + R2 deploys
- `vps-aiw-static-deploy` — static site deploys
- `vps-aiw-dns-fix` — Cloudflare 522s
- `vps-aiw-client-sites` — audit live sites
- `vps-aiw-autonomous-ops` — VPS ops
- `client-site-deploy` — single client site deploy
- `client-site-build-workflow` — greenfield build
- `client-site-kickoff` — 200-question intake
- `client-vps-provisioning` — managed VPS for clients
- `github-pr-workflow` — PR lifecycle
- `github-code-review` — review PRs
- `aiw-deploy-discipline` — verify topology before deploy
- `aiw-git-safety` — git safety for autonomous work

---

## Escalation triggers

- Production site down > 5 min → page Kiki + Ivan immediately
- Data loss / DB corruption → Kiki + Ivan same-minute
- Credential rotation needed → Ivan (per aiw-git-safety)
- Repo needs force-push → Ivan approval required
- New client > $5K signed → confirm scope with Ivan

---

## AI Safety protocol (per OWASP LLM Top 10 2026)

- **Hard stops** — enforced via `hard-stop-wrapper.py` at runtime
- **Eval gates** — golden trajectories + auto-eval on every agent run
- **Prompt injection** — all untrusted input sanitized before reaching LLM
- **Excessive agency** — LLM cannot bypass hard stops
- **Supply chain** — agents only have access to scoped tools

---

## See also

- `/opt/data/agents/departments/04-engineering-delivery.md` (canonical charter)
- `/opt/data/agents-v2/agents/engineering-roster/PROMPT.md` (agent spec)
- `/opt/data/vps-knowledge/` (VPS knowledge)
