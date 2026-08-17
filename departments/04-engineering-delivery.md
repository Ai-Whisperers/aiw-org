# Department 4 — Engineering & Delivery

**Head**: Kiki (CTO)
**Lead agent**: `engineering-roster` (Tue/Fri 17:00 PYT)
**Version**: 0.2.0
**Last updated**: 2026-08-14

---

## Mission

Ship client sites, maintain infra uptime, keep the ParaguAI Builder running, deploy changes safely. Engineering is where Kiki owns end-to-end.

## What this department owns

- **Production sites** — nexa-paraguay.com.py, ometzdental.com, + 17+ live client sites in Docker Swarm
- **CI/CD pipelines** — GitHub Actions workflows per repo, deploy to VPS
- **VPS operations** — Docker Swarm, Traefik, CF Workers, Postgres, Qdrant, mem0
- **Build pipeline** — ParaguAI Builder (multi-tenant SaaS)
- **Code quality** — pre-commit hooks, lint-staged, review queues
- **Observability** — site-health checks, Grafana/Prometheus if/when set up
- **Incident response** — rollback authority for Kiki, escalation for Ivan
- **NEW v0.2.0**: AI Safety (sub-function) — OWASP LLM compliance
- **NEW v0.2.0**: Storage architecture (per-agent git repos + SQLite)

## What this department does NOT own

- Sales scoping (Sales — Kiki only reviews)
- Pricing (Finance & Legal)
- Kiki's learning curriculum (People & Culture)
- Thesis code (Research & Education)

## Decision rights (v0.2.0)

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
| **NEW**: Disable hard-stop wrapper | require Ivan + Kiki |
| **NEW**: Modify eval-gate ground truth | require Ivan |

## Sub-roles (v0.2.0 — 24 roles from ROLES-INVENTORY.md)

| # | Role | Tier |
|---|------|------|
| 4.1 | CTO/Eng Lead | 🟢 T1 |
| 4.2 | Engineering Manager | 🟠 T3 |
| 4.3 | Frontend Engineer | 🟢 T1 |
| 4.4 | Backend Engineer | 🟢 T1 |
| 4.5 | Full-stack Engineer | 🟢 T1 |
| 4.6 | Mobile Engineer | 🟠 T3 |
| 4.7 | DevOps / SRE | 🟢 T1 |
| 4.8 | QA Engineer | 🟢 T1 |
| 4.9 | Security Engineer | 🟢 T1 |
| 4.10 | ML Engineer | 🟠 T3 |
| 4.11 | Data Engineer | 🟠 T3 |
| 4.12 | Solutions Architect | 🟠 T3 |
| 4.13 | Tech Writer | 🟡 T2 |
| 4.14 | Engineering PM | 🟠 T3 |
| 4.15 | Platform Engineer | 🟠 T3 |
| 4.16 | Release Manager | 🟠 T3 |
| 4.17 | SRE | 🟠 T3 |
| 4.18 | DBA | 🟡 T2 |
| 4.19 | Network Engineer | 🟠 T3 |
| 4.20 | UI/UX Designer | 🟡 T2 |
| 4.21 | Product Designer | 🟠 T3 |
| 4.22 | EngOps Specialist | 🟠 T3 |
| 4.23 | Build/Release Engineer | 🟠 T3 |
| 4.24 | **AI Safety Engineer** | 🟢 T1 (NEW in v0.2.0) |

## Sub-agents (v0.2.0)

| Agent | Cadence | Class |
|-------|---------|-------|
| `engineering-roster` | Tue+Fri 17:00 PYT | OPERATIONAL |
| `devops-monitor` | Every 30 min | OPERATIONAL |
| `qa-automation-runner` | On-PR | OPERATIONAL |
| `security-watchdog` | Every 30 min | OPERATIONAL |
| `ai-safety-engineer` (NEW) | Every 30 min | OPERATIONAL |

## Inputs the lead agent reads

1. `hermes cron list` filtered to Engineering jobs
2. `gh api search/issues?q=org:Ai-Whisperers+is:open+is:pr`
3. `gh api orgs/Ai-Whisperers/repos --paginate` — last 7d
4. `/opt/data/logs/site-health.log` — HTTP checks
5. `/opt/data/logs/deploy-*.log` — recent deploys
6. Kiki's recent commits (`/opt/data/db/kiki-prep.db`)
7. `/opt/data/db/coord.db` — cross-repo stuck items
8. **NEW**: `/opt/data/agents-v2/cron-heartbeat-alerts.log`

## Cadence (v0.2.0)

| Time | What |
|------|------|
| Tue+Fri 17:00 PYT | engineering-roster brief |
| Every 30 min | devops-monitor, security-watchdog, ai-safety-engineer |
| Every 15 min | site-health (existing) |
| Every 15 min | state-validate, cron-heartbeat |
| On-PR | qa-automation-runner |
| Daily 02:00 | db-snapshot |

## Stack reality (per `04-engineering-delivery.md` lines 86-95)

- **Hostinger VPS** (38.9.96.179) — primary prod, 32GB RAM, 387GB disk
- **Servarica Host A** — secondary
- **Traefik v3.5.3** reverse proxy, auto-LE
- **Docker Swarm** orchestrator (NOT K8s)
- **CF Worker + R2** for static deploys
- **Vercel 403** — DO NOT attempt deploys there

## Skills stack (v0.2.0)

- `vps-aiw-deploy-pipeline` — CF Worker + R2
- `vps-aiw-static-deploy` — static sites
- `vps-aiw-dns-fix` — CF 522s
- `vps-aiw-client-sites` — audit live sites
- `vps-aiw-autonomous-ops` — VPS ops
- `client-site-deploy` — single site deploy
- `client-site-build-workflow` — greenfield
- `client-site-kickoff` — 200-question intake
- `client-vps-provisioning` — managed VPS for clients
- `github-pr-workflow` — PR lifecycle
- `github-code-review` — review PRs
- `aiw-deploy-discipline` — verify topology
- `aiw-git-safety` — git safety
- **NEW** (from AI Safety): `hard-stop-wrapper.py`, eval-gate pattern

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

## AI Safety protocol (per OWASP LLM Top 10 2026)

- **Hard stops** — enforced via `hard-stop-wrapper.py` at runtime
- **Eval gates** — golden trajectories + auto-eval
- **Prompt injection** — all untrusted input sanitized
- **Excessive agency** — LLM cannot bypass hard stops

## Escalation triggers

- Production site down > 5 min → page Kiki + Ivan immediately
- Data loss / DB corruption → Kiki + Ivan same-minute
- Credential rotation needed → Ivan (per aiw-git-safety)
- Repo needs force-push → Ivan approval required
- New client > $5K signed → confirm scope with Ivan before scheduling
- **NEW**: Hard-stop blocked an action → log to escalations table

## Cross-references

- Constitution: `/opt/data/agents/departments/ORG-AGENTS.md` (v0.2.0)
- Playbook: `/opt/data/agents-v2/playbooks/03-engineering-delivery.md`
- Agent spec: `/opt/data/agents-v2/agents/engineering-roster/PROMPT.md`
- AI Safety: `/opt/data/agents-v2/THREAT-MODEL.md`

---

## CHANGELOG

- v0.2.0 (2026-08-14): added 24 sub-roles (incl. AI Safety Engineer), 5 sub-agents (incl. ai-safety-engineer), AI Safety protocol, Storage architecture, Cross-references.
- v0.1.0 (2026-08-13): initial ratification.
