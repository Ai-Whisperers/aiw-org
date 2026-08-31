# Package Index — AI Whisperers Departments

> Master index of all 6 per-department packages.
> Each package is independently deployable so customers can pick
> "just the sales agents" or "just the coaching product" without copying
> the whole mono-repo.
> **Last updated**: 2026-08-26

---

## All packages at a glance

| # | Package | Size | Files | Lead agent | Department head |
|---|---------|------|-------|------------|-----------------|
| 1 | [`packages/finance/`](./packages/finance/) | 92 KB | 11 | `finance-controller` | Ivan |
| 2 | [`packages/sales/`](./packages/sales/) | 108 KB | 12 | `sales-pipeline` | Ivan |
| 3 | [`packages/operations/`](./packages/operations/) | 104 KB | 12 | `management-coordinator` | Ivan |
| 4 | [`packages/coaching/`](./packages/coaching/) | 96 KB | 11 | `kiki-coach` | Ivan + Kiki |
| 5 | [`packages/engineering/`](./packages/engineering/) | 104 KB | 12 | `engineering-roster` | Kiki |
| 6 | [`packages/research/`](./packages/research/) | 112 KB | 12 | `research-tracker` | Ivan |
| | **TOTAL** | **~616 KB** | **70** | | |

---

## Package → use case mapping

### When a customer wants to…

**Track cash flow, contracts, compliance, and procurement**
→ Use [`packages/finance/`](./packages/finance/)

**Capture leads, draft outreach, score ICPs, generate proposals, run marketing content**
→ Use [`packages/sales/`](./packages/sales/)

**Coordinate org-wide ops: cross-repo review, daily business snapshot, AI-ops, OKRs, source curation, burnout watch**
→ Use [`packages/operations/`](./packages/operations/)

**Run a coaching product: weekly lessons for a co-founder, thesis tracking, course module production, customer lifecycle, conversion funnel**
→ Use [`packages/coaching/`](./packages/coaching/)

**Ship client sites, monitor Docker Swarm / Traefik / CF Worker, run QA, scan for security threats, verify hard stops, run chaos tests**
→ Use [`packages/engineering/`](./packages/engineering/)

**Drive a thesis, verify citations before publication, produce course modules, track OKRs, scan the funding landscape**
→ Use [`packages/research/`](./packages/research/)

### Full-stack deployments (combine multiple packages)

| Customer type | Combine packages |
|---------------|------------------|
| **Solo founder / consultancy** (wants ops + sales + finance + coaching) | operations + sales + finance + coaching |
| **Product studio** (wants engineering + operations + finance) | engineering + operations + finance |
| **Research org** (wants research + coaching) | research + coaching |
| **Full AI Whisperers clone** | ALL 6 |

---

## Package contents (uniform structure)

Every package ships with:

```
<PACKAGE>/
├── README.md                              ← install + agents + skills to load
├── LICENSE                                ← MIT
├── CHANGELOG.md                           ← version history + source provenance
├── agents/<agent-name>/PROMPT.md          ← one per agent (with frontmatter)
├── schemas/<dept>.schema.json             ← state JSON schema
├── state/<dept>.json.template             ← empty state template
└── playbooks/<dept-relevant>.md           ← dept charter + role matrix + SOPs
```

---

## Agents shipped per package

### Finance (5 agents)
- `finance-controller` (lead, OPERATIONAL, Fri 18:00 PYT)
- `accounting-automation` (OPERATIONAL, daily 07:00 PYT)
- `tax-receipt-tracker` (OPERATIONAL, Sun 08:00 PYT)
- `procurement-tracker` (OPERATIONAL, Mon 09:00 PYT)
- `compliance-monitor` (OPERATIONAL, Mon 08:00 PYT)

### Sales (6 agents)
- `sales-pipeline` (lead, CONTENT, daily 12:00 PYT)
- `proposal-drafter` (CONTENT, on-demand)
- `lead-enrichment` (OPERATIONAL, daily 08:00 PYT)
- `marketing-content-producer` (CONTENT, Mon/Wed/Fri)
- `multimedia-producer` (CONTENT, on-demand)
- `revops-pipeline-analyzer` (OPERATIONAL, daily 11:00 PYT)

### Operations (6 agents)
- `management-coordinator` (lead, OPERATIONAL, Mon+Thu 17:00 PYT)
- `business-analyst` (OPERATIONAL, daily 06:30 PYT)
- `ai-ops-coordinator` (OPERATIONAL, daily 09:00 PYT)
- `bizops-tracker` (OPERATIONAL, Sun 17:00 PYT)
- `source-curator` (OPERATIONAL, Sun 09:00 PYT)
- `founder-bandwidth-watchdog` (OPERATIONAL, Sun 18:00 PYT)

### Coaching (5 agents)
- `kiki-coach` (lead, CONTENT, Fri 17:00 PYT)
- `thesis-tracker` (OPERATIONAL, daily 06:00 UTC)
- `course-producer` (CONTENT, Sun 10:00 PYT)
- `coaching-customers` (OPERATIONAL, daily 09:00 PYT)
- `conversion-funnel` (OPERATIONAL, daily 10:00 PYT)

### Engineering (6 agents)
- `engineering-roster` (lead, OPERATIONAL, Tue+Fri 17:00 PYT)
- `devops-monitor` (OPERATIONAL, every 30 min)
- `qa-automation-runner` (OPERATIONAL, on-PR)
- `security-watchdog` (OPERATIONAL, every 30 min)
- `ai-safety-engineer` (OPERATIONAL, every 30 min)
- `chaos-test-runner` (OPERATIONAL, Sun 03:00 PYT)

### Research (6 agents)
- `research-tracker` (lead, CONTENT, Sun 18:00 PYT)
- `citation-checker` (CONTENT, on-demand)
- `thesis-tracker` (OPERATIONAL, daily 06:00 UTC)
- `course-producer` (CONTENT, Sun 10:00 PYT)
- `okr-tracker` (OPERATIONAL, Sun 17:00 PYT)
- `funding-coordinator` (OPERATIONAL, Mon 09:00 UTC)

**Total**: 34 agents across 6 packages (some duplication: `thesis-tracker` and `course-producer` ship in both research and coaching packages because they support thesis work and course production from either angle).

---

## Skills to load (by package)

Each package's README lists the exact skills. Quick map:

| Package | Skills |
|---------|--------|
| finance | `paraguai-proposal-pricing`, `trademark-compliance-scrub`, `prospect-dossier-pii-sanitization`, `aiw-ops-discipline` |
| sales | `b2b-cold-outreach-pitch`, `paraguai-proposal-pricing`, `trademark-compliance-scrub`, `prospect-dossier-pii-sanitization`, `social-media`, `creative`, `media` |
| operations | `aiw-ops-discipline`, `aiw-git-safety`, `diagramming`, `github-auto-merge-permissive-protection`, `org-repo-audit`, `trademark-compliance-scrub`, `research-integrity-protocol` |
| coaching | 18 coaching skills (see coaching/README.md) + `thesis-active-autonomy`, `academic-thesis-paper-first`, `media`, `creative`, `aiw-ops-discipline` |
| engineering | 21 skills incl. `aiw-deploy-discipline`, `aiw-git-safety`, `vps-aiw-*`, `client-site-*`, `github-pr-workflow`, `cloudflare-tunnel-zero-trust-expose`, `live-site-triage`, `red-teaming`, `evolution-api-destructive-ops`, `code-hygiene-ci-gardening`, `devops`, `mcp`, `supabase-2026-secret-proxy`, `vps-knowledge` |
| research | `thesis-active-autonomy`, `academic-thesis-paper-first`, `evaluating-llms-harness`, `data-science`, `research`, `research-integrity-protocol`, `grounded-citations`, `media`, `creative`, `aiw-ops-discipline` |

---

## Cross-package dependencies (when stacking packages)

```
                  ┌─────────────────────────────────────────┐
                  │        coaching (kiki-coach)            │
                  │        └─ uses research.thesis-tracker  │
                  └──────────────────┬──────────────────────┘
                                     │ (curriculum, courses)
                                     ▼
                  ┌─────────────────────────────────────────┐
                  │        research (research-tracker)      │
                  └──────┬──────────────────────┬───────────┘
                         │                      │
   ┌─────────────────────┘                      └─────────────────────┐
   │                                                                   │
   ▼                                                                   ▼
┌────────────────────────┐                  ┌────────────────────────┐
│  operations            │◀────────────────▶│  sales                 │
│  (mgmt-coordinator)    │   (handoffs)      │  (sales-pipeline)      │
│  (business-analyst)    │                  │  (revops-analyzer)     │
└──────────┬─────────────┘                  └──────────┬─────────────┘
           │                                            │
           │ (infra, deploys, costs)                    │
           ▼                                            │
┌────────────────────────┐                               │
│  engineering           │◀──────────────────────────────┘
│  (engineering-roster)  │   (proposals, deals signed)
│  (devops-monitor)      │
└──────────┬─────────────┘
           │ (vps bills, infra costs)
           ▼
┌────────────────────────┐
│  finance               │
│  (finance-controller)  │
│  (procurement-tracker) │
└────────────────────────┘
```

---

## Hard-stop governance (every package)

Every `PROMPT.md` ships with a `hard_stops:` YAML block. All external actions
require explicit human approval:

| Action type | Authority |
|-------------|-----------|
| Send external artifact / publish / proposal | Ivan (HITL) |
| Sign contract | Ivan only |
| Merge PR (no breaking) | Kiki or designated reviewer |
| Merge PR (schema / infra) | Kiki + Ivan |
| Force-push any repo | Ivan only |
| Sign EU client contract | HARD-STOP until Compliance Officer named (per D3) |
| Disable hard-stop wrapper | Ivan + Kiki |
| Modify eval-gate ground truth | Ivan only |

---

## Trademark compliance

Every package passes `/opt/data/scripts/trademark-scan.py` with **0 hits**
on the 30-token banlist. Verified 2026-08-26 at package split time.

If a future package edit introduces a banned token, the script exits 1 with
per-file / per-line breakdown. Carve-outs are listed in
`/opt/data/scripts/trademark-scan.py` (HTML5 `<meta>` tags, `footer-meta`
CSS class, Evolution API mentions, Hostinger incident quotes, etc.).

---

## Upgrade path

The mono-repo at `/opt/data/agents-v2/` remains the source of truth. To
regenerate a single package after a source update:

```bash
# 1. Edit the source files in /opt/data/agents-v2/constitution/ or
#    /opt/data/agents-v2/playbooks/ or /opt/data/agents-v2/agents-prompts/

# 2. Copy the updated source into the package
cp /opt/data/agents-v2/constitution/02-finance-legal.md \
   /opt/data/agents-v2/packages/finance/playbooks/finance-legal.md

# 3. Update the package CHANGELOG.md with the version bump

# 4. Re-scan
python3 /opt/data/scripts/trademark-scan.py /opt/data/agents-v2/packages/finance/

# 5. Commit
cd /opt/data/agents-v2 && git add packages/finance/ && git commit -m "feat(finance): refresh playbook v0.3.0"
```

---

## See also

- [`/opt/data/agents-v2/INDEX.md`](./INDEX.md) — master index of all artifacts
- [`/opt/data/agents-v2/PACKAGE-INDEX.md`](./PACKAGE-INDEX.md) — this file
- [`/opt/data/agents-v2/constitution/`](./constitution/) — source of truth for dept specs
- [`/opt/data/agents-v2/playbooks/`](./playbooks/) — source of truth for dept playbooks
- [`/opt/data/agents-v2/agents-prompts/`](./agents-prompts/) — source of truth for agent specs