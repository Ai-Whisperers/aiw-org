# 30 Areas of Research — AI Whisperers Paraguay EAS

> Compiled 2026-08-13 by Erebus for Ivan Weiss Van der Pol.
> 30 distinct research areas, grouped by strategic purpose. Each one has:
> - **Why**: the decision it informs
> - **Method**: how to actually do the research
> - **Output**: what artifact it produces
> - **Owner**: who in the org does it (per the 6-department framework)
> - **Cadence**: when to do it (once / quarterly / ongoing)

---

## Reading guide

- **Areas 1-6**: Internal company research — what AI Whisperers already knows about itself
- **Areas 7-12**: External market research — what AI Whisperers needs to know about its world
- **Areas 13-16**: Personal/professional development — what Ivan and Kiki need to grow
- **Areas 17-24**: Industry/technology research — what AI Whisperers needs to stay current on
- **Areas 25-28**: Thesis-specific — for P1 GeoData v2 (the master's thesis)
- **Areas 29-30**: Optional/exploratory — moonshot research, only if time permits

**Total time budget**: if you allocate 2 hours/week per area, full rotation is 60h. Realistically: do the 8 marked 🔴 HIGH first (Areas 1, 2, 7, 11, 17, 25, 13, 18), then layer the others as capacity allows.

---

# Group 1: Internal company research (6)

These areas study AI Whisperers itself — past decisions, current state, latent opportunities.

## 1. 🔴 Past session retrospectives 🔴

| | |
|---|---|
| **Why** | You have ~33MB of session DB with months of work. Almost none of it is queryable. Find recurring patterns: what you shipped, what blocked you, who you talked to. |
| **Method** | Use `session_search` (built into Hermes) over the last 90 days of sessions. Cluster by topic. Tag recurring client names, recurring decisions, recurring tools. |
| **Output** | `scratchpad/retrospectives/2026-Q2-summary.md` (one per quarter). Lists: top 10 topics worked on, top 5 blockers, top 3 things to never do again. |
| **Owner** | Ivan + business-analyst agent |
| **Cadence** | Quarterly (1st week of Jan/Apr/Jul/Oct) |

## 2. 🔴 Customer archaeology 🔴

| | |
|---|---|
| **Why** | You have 17+ deployed client sites and outreach to dozens more prospects. The pattern of who actually bought (vs. who ghosted) is your real ICP — possibly different from the one in `marketing-strategy/playbook.md`. |
| **Method** | Mine: (a) signed contracts (if any), (b) `marketing-strategy/agent-tasks/` outreach logs, (c) CF Worker `rubicon-eas-lead` form submissions, (d) WhatsApp conversation patterns (with consent). Look for: what triggered purchase, who referred them, how long the cycle was. |
| **Output** | `company/Company/icps/data-driven-icps-2026.md` — updated ICPs based on actual conversions, not theory. |
| **Owner** | sales-pipeline agent + Ivan |
| **Cadence** | Every 6 months |

## 3. Margin + cost reality check

| | |
|---|---|
| **Why** | The pricing in `marketing-strategy/02-PRICING.md` is theoretical. Real margin per project depends on: hours actually worked, infra costs, contractor costs, tool subscriptions. Without this, you're pricing blind. |
| **Method** | For each of the last 5 client projects: extract hours (from git activity, session DB, calendar), tools used, infra cost (cloud bill share), total billed. Compute actual margin. |
| **Output** | `company/Company/finance/margin-analysis-2026.md` — table per project with cost, price, margin %, lessons learned. |
| **Owner** | finance-controller agent |
| **Cadence** | Once (after 5+ projects), then refresh quarterly |

## 4. Tool stack audit

| | |
|---|---|
| **Why** | You're spending USD ~400-600/mo on tools (Hermes infra, Cloudflare, GitHub, OpenAI/Anthropic APIs, Cursor, etc.). Some may be redundant or underused. |
| **Method** | List every active subscription. For each: last 30 days usage, monthly cost, alternative cost. Flag anything < 20% utilization. |
| **Output** | `scratchpad/audits/tool-stack-2026.md` — recommendations to keep / drop / downgrade. |
| **Owner** | finance-controller + Kiki |
| **Cadence** | Annually + on demand |

## 5. Repo hygiene sweep

| | |
|---|---|
| **Why** | You have 17+ active repos and several archived. Some are stale (>30d no push), some are misnamed, some have broken CI. Without a sweep, drift accumulates. |
| **Method** | Run `org-pulse.sh` (already exists) for repo state. For each repo > 30d idle: ask "should this be archived, revived, or left?". For each active repo: check CI status, CODEOWNERS, README currency. |
| **Output** | `scratchpad/audits/repo-hygiene-2026.md` — per-repo disposition decisions. |
| **Owner** | management-coordinator agent + engineering-roster |
| **Cadence** | Quarterly |

## 6. Org constitution review (the agent layer itself)

| | |
|---|---|
| **Why** | `/opt/data/agents/departments/ORG-AGENTS.md` was just drafted. After 30 days of operation, some departments will be too quiet (over-automated), some too noisy (under-disciplined). You need to adjust. |
| **Method** | Read every outbox file the 7 agents have produced. Look for: which briefs did Ivan actually read? Which were ignored? Which escalated too often / not enough? |
| **Output** | `agents/departments/CHANGELOG-2026-Q3.md` — what to add/cut/re-tune. |
| **Owner** | management-coordinator agent + Ivan |
| **Cadence** | Monthly for first 3 months, then quarterly |

---

# Group 2: External market research (6)

What AI Whisperers needs to know about its world to compete.

## 7. 🔴 Competitor deep-dive 🔴

| | |
|---|---|
| **Why** | `company/Company/competitors/README.md` lists 20 competitors, but most haven't been re-checked since 2025. Competitors pivot, get acquired, raise huge rounds, or die. Your positioning depends on knowing who's actually live. |
| **Method** | For each of the 20: visit their site, check their recent blog, check Crunchbase for new rounds, check LinkedIn for new hires. Update or remove stale entries. |
| **Output** | Refresh `company/Company/competitors/README.md` with current state. Add new competitors surfaced from `200-ai-companies.md`. |
| **Owner** | sales-pipeline agent + Ivan |
| **Cadence** | Annually + on event |

## 8. Paraguay/LATAM AI market sizing

| | |
|---|---|
| **Why** | You're pricing Rubicón EAS at multipliers ~3x Ometz Dental because "legal client LTV is 10-50x higher". But what's the actual addressable market? Is there 10 dental clinics × 5 law firms = real TAM, or are there 100? |
| **Method** | Search: Paraguay AI service providers, LATAM AI consulting market, Paraguay law firm size. Read public INC report (Industria Nacional del Cemento has market data). Look at how many Paraguay businesses have > 50 employees. |
| **Output** | `scratchpad/research/paraguay-ai-tam.md` — bottom-up TAM estimate by vertical (legal, dental, retail). |
| **Owner** | Ivan + sales-pipeline |
| **Cadence** | Once, refresh if Rubicón EAS hits first sale |

## 9. Pricing benchmark refresh

| | |
|---|---|
| **Why** | Your `paraguai-proposal-pricing` skill has Dental × 3 multipliers. But real LATAM AI pricing in 2026 may have shifted (more providers, lower entry tiers). |
| **Method** | Survey 10 LATAM AI agencies (public pricing pages, RFP responses). Build a per-vertical rate card. Compare against your prices. |
| **Output** | Updated rates in `marketing-strategy/02-PRICING.md`. Decision: hold / raise / discount specific tiers. |
| **Owner** | finance-controller + Ivan |
| **Cadence** | Annually |

## 10. Partner / supplier mapping

| | |
|---|---|
| **Why** | You depend on: Hostinger (VPS), Cloudflare (DNS/Workers/R2), GitHub (repo + CI), Evolution API (Hermes bridge), OpenAI/Anthropic (LLMs). What's your contingency if any one fails? |
| **Method** | For each critical vendor: contract terms, SLA, alternative provider (AWS for Hostinger? Supabase for self-hosted Postgres?). Build a matrix. |
| **Output** | `scratchpad/research/vendor-risk-matrix.md` — single points of failure + mitigation. |
| **Owner** | engineering-roster + Ivan |
| **Cadence** | Annually + on vendor event (price hike, outage) |

## 11. 🔴 Hostinger incident monitoring 🔴

| | |
|---|---|
| **Why** | Hostinger suspended `srv1396188.hstgr.cloud` 2026-Q1 over `mensajeconnect.paragu-ai.com` flagged as phishing. They could do it again — and you'd lose prod overnight. The trademark banlist exists because of this. |
| **Method** | Weekly: scan your public-facing assets for any banned trademark (mensaje, paypal, google, etc.). Quarterly: re-read Hostinger TOS, check if there's a more lenient provider (Servarica is your second VPS — is it enough?). |
| **Output** | `scratchpad/audits/hostinger-compliance-weekly.md` (auto-generated from a script) + decision record if TOS changes. |
| **Owner** | Ivan + trademark-compliance-scrub skill |
| **Cadence** | Weekly (auto) + quarterly review |

## 12. Lead-pipeline deep-dive

| | |
|---|---|
| **Why** | Rubicón EAS Worker has been live since 2026-08-10 but `WEBHOOK_URL` to n8n is still not configured. Until it is, leads go nowhere. This is a single-blocker that prevents revenue. |
| **Method** | Configure webhook (one-time), then every Monday review: how many leads came in, ICP match, response rate, conversion. Identify what's blocking conversion. |
| **Output** | `state/sales.json` weekly updates + monthly retrospective in `scratchpad/sales/monthly-2026-MM.md`. |
| **Owner** | sales-pipeline agent |
| **Cadence** | Daily triage, weekly review, monthly retrospective |

---

# Group 3: Personal/professional development (4)

What Ivan and Kiki need to grow.

## 13. 🔴 Kiki's growth path 🔴

| | |
|---|---|
| **Why** | Kiki is the Co-Founder & Technical Director. The kiki-coach weekly lesson cycle is the engine for her growth. But the curriculum (8 weeks) was guessed — not based on a real assessment of her current skill graph. |
| **Method** | Self-assessment (Kiki) + peer review (Ivan reviews her last 30d of PRs) + skill graph (compare to industry standard for "Tech Director at AI services co"). Build a 12-month roadmap. |
| **Output** | `agents/kiki-coach/curriculum.md` updated with a real 12-month path + monthly milestones. |
| **Owner** | kiki-coach agent + Kiki + Ivan |
| **Cadence** | Quarterly review |

## 14. Ivan's bandwidth audit

| | |
|---|---|
| **Why** | You wear multiple hats — CEO, sales, engineering review, thesis, infrastructure ops. Without measurement, burnout is the failure mode. The `people.json` already has a placeholder for this. |
| **Method** | Track 2 weeks: every hour tagged (billable / internal / thesis / family / sleep). Identify the categories that consume > 40h/week. Decide what to cut or delegate. |
| **Output** | `state/people.json` populated + `scratchpad/research/ivan-bandwidth-2026-Q3.md` — recommendation to delegate/cut. |
| **Owner** | Ivan + people dept agent (when built) |
| **Cadence** | Twice yearly |

## 15. Network mapping

| | |
|---|---|
| **Why** | Your network (Kiki, Claudio Acosta, Richar Ruiz, the Paraguay AI/tech scene, YC/AI community) is mostly invisible to you as a graph. Mapping it surfaces: who can introduce you to whom, who's been cold for too long, who's a referral source. |
| **Method** | Export LinkedIn connections (CSV). Graph it: who knows whom, who's in LATAM AI, who's a potential partner vs. customer vs. investor. Identify 3 dormant relationships to revive. |
| **Output** | `scratchpad/research/network-graph-2026.md` — visual map + 3 reactivation targets. |
| **Owner** | Ivan |
| **Cadence** | Annually |

## 16. Credential / certification landscape

| | |
|---|---|
| **Why** | Ivan's CV lists ISTQB, Hexawise, "AI For Everyone". What certifications would unlock bigger deals (legal vertical: bar admission? healthcare: HIPAA cert? cloud: AWS Architect?)? What would Kiki benefit from (Terraform Associate? Kubernetes CKA?)? |
| **Method** | Survey 5 target verticals (legal, healthcare, dental, retail, SaaS) — what certs do they expect from vendors? Map to your team gaps. |
| **Output** | `scratchpad/research/cert-roadmap-2027.md` — top 3 certs to pursue for Ivan, top 3 for Kiki. Cost + time + ROI. |
| **Owner** | Ivan + Kiki |
| **Cadence** | Once, refresh if verticals change |

---

# Group 4: Industry/technology research (8)

What AI Whisperers needs to stay current on.

## 17. 🔴 AI model landscape monitoring 🔴

| | |
|---|---|
| **Why** | Foundation models shift every 3-6 months. GPT-5, Claude 4, Gemini 3, Llama 4, Mistral Large 3, DeepSeek V4 — each shifts which provider you use for which task. You can't afford to be paying for an inferior model because you didn't notice a release. |
| **Method** | Use the `blogwatcher` skill + arxiv alerts + a weekly cron that checks OpenAI/Anthropic/Mistral changelogs. Build a model comparison matrix (cost, latency, capability per task). |
| **Output** | `scratchpad/research/model-landscape-2026-MM.md` (monthly) — what changed, what to switch to. |
| **Owner** | business-analyst agent |
| **Cadence** | Weekly auto + monthly synthesis |

## 18. 🔴 Tooling evolution 🔴

| | |
|---|---|
| **Why** | The agent framework space is moving fast. CrewAI, AutoGen (now Microsoft Agent Framework), LangGraph, LlamaIndex, MetaGPT — each ships major versions monthly. Your tech stack assumptions decay. |
| **Method** | Track release notes for top 10 agent frameworks. Run quarterly benchmark: same task, same model, different framework — measure reliability + DX. |
| **Output** | `scratchpad/research/agent-framework-qN-2026.md` — what to adopt, what to keep, what to drop. |
| **Owner** | engineering-roster agent |
| **Cadence** | Quarterly |

## 19. MCP / interop protocol maturity

| | |
|---|---|
| **Why** | MCP (Model Context Protocol) is becoming the standard for tool integration. Anthropic, Microsoft, OpenAI all adopted it in 2025. If you ship MCP servers (you do — see your skills), you're betting on this becoming default. Worth tracking. |
| **Method** | Read the MCP spec quarterly. Check how many tools ship MCP. Check if any competitor emerges (OpenAI's "Agents SDK" tools protocol, Google's AG-UI). |
| **Output** | `scratchpad/research/mcp-maturity-2026-QN.md` — confidence in MCP, what to add to your servers. |
| **Owner** | engineering-roster |
| **Cadence** | Quarterly |

## 20. Regulatory + compliance landscape

| | |
|---|---|
| **Why** | AI regulation is in motion: EU AI Act (2026 enforcement), Paraguay data protection, US state laws (CA SB 1047, Colorado AI Act). Selling to legal/healthcare clients means you inherit their compliance burden. |
| **Method** | Subscribe to AI regulation newsletters. Track: EU AI Act high-risk classifications, Paraguay Ley 1682/2001 (data protection), any sector-specific rules. |
| **Output** | `scratchpad/research/ai-regulation-2026.md` — what applies to AI Whisperers, what to surface to clients. |
| **Owner** | finance & legal dept + Ivan |
| **Cadence** | Semi-annually |

## 21. Open-source AI dependency audit

| | |
|---|---|
| **Why** | You depend on: Hermes (Nous), Next.js (Vercel), Cursor, pnpm, etc. Any of these could pivot in a way that breaks you (Vercel suspended your account — you can't deploy there). What's the blast radius if your top 3 OSS dependencies disappear? |
| **Method** | List top 20 OSS deps. For each: license, contributor count, business model, project health (commit frequency, issue closure rate). Flag any single-point-of-failure. |
| **Output** | `scratchpad/research/oss-dependency-health-2026.md` — risk per dep + mitigation. |
| **Owner** | engineering-roster |
| **Cadence** | Annually |

## 22. Paraguay / LATAM tech ecosystem events

| | |
|---|---|
| **Why** | You have to show up where the buyers are. PYData, ParaguayJS, AI meetups in Asunción, Montevideo, Buenos Aires, São Paulo. Sponsorships, talks, presence = leads. |
| **Method** | Calendar: list every AI/tech/dev event in LATAM for the next 6 months. Identify the 3 highest-ROI to attend or sponsor. |
| **Output** | `scratchpad/research/latam-events-2026-QN.md` — calendar + decisions. |
| **Owner** | sales-pipeline + Ivan |
| **Cadence** | Semi-annually |

## 23. Customer reference research

| | |
|---|---|
| **Why** | You ship work for clients but rarely write case studies / testimonials. The 20+ deployed sites are your social proof — they just don't say it in the format buyers want. |
| **Method** | For 3 past clients: ask for a 15-min interview, capture 3 specific outcomes (X% time saved, $Y cost cut, Z hours/week freed). Write a 1-page case study each. |
| **Output** | `company/docs/case-studies/06-NN-client-name.md` — formatted per the existing case-study template. |
| **Owner** | sales-pipeline + Ivan |
| **Cadence** | Once per completed project |

## 24. Hiring market for "AI engineer"

| | |
|---|---|
| **Why** | When you do hire (first engineer, first contractor), the LATAM AI talent market has its own salary bands, freelance rates, availability. You don't want to underpay or miss top talent. |
| **Method** | Survey 5 LATAM AI companies (or remote-first ones hiring in LATAM): salary bands, equity norms, contractor rates. Compare to what you can afford. |
| **Output** | `scratchpad/research/latam-ai-talent-2026.md` — rate bands + hiring decision. |
| **Owner** | Ivan (when hiring decision nears) |
| **Cadence** | When hiring — not before |

---

# Group 5: Thesis-specific research (4)

P1 GeoData v2 — your master's thesis on Paraguayan cartography. These four areas feed directly into the thesis chapters.

## 25. 🔴 Literature review (chapter-spanning) 🔴

| | |
|---|---|
| **Why** | The thesis needs a defensible literature review across cartography, GIS, Paraguayan geography, data quality. Right now this is the bottleneck for chapter 1 + chapter 2. |
| **Method** | Use `arxiv` skill + Google Scholar + Paraguay IGN catalog. For each chapter, identify 20-30 papers. Build `REFERENCES.bib` (already exists). Synthesize per chapter. |
| **Output** | `thesis-active/REFERENCES.bib` (growing) + per-chapter lit review sections. |
| **Owner** | research-tracker agent + thesis-active-autonomy skill + Ivan |
| **Cadence** | Ongoing (every thesis tick) |

## 26. Paraguay primary data sources

| | |
|---|---|
| **Why** | Chapter 3 (Methodology) and chapter 4 (Results) depend on getting real Paraguay data: census, IGN maps, municipal boundaries, indigenous territory records. Knowing what's available offline vs. needing formal request is critical. |
| **Method** | Inventory every public Paraguay data source (DGEEC, IGN, MADES, INDERT, INFONA, municipal data). For each: access method, format, license, last update. |
| **Output** | `thesis-active/DATA_MANIFEST.md` (already exists — verify currency) + `data/` directory populated. |
| **Owner** | Ivan + thesis agent |
| **Cadence** | Once, refresh as new data appears |

## 27. Comparable country case studies

| | |
|---|---|
| **Why** | Paraguay is N=1 for the thesis. To make the conclusions generalizable, you need comparators: how did Uruguay, Chile, Costa Rica handle similar data modernization? Did their methods generalize? |
| **Method** | Pick 3 comparable countries. For each: their national mapping agency, their open data strategy, their data quality issues. 1-page case each. |
| **Output** | `thesis-active/case-studies/{uruguay,chile,costa-rica}.md` — small comparative analyses. |
| **Owner** | research-tracker agent |
| **Cadence** | Once |

## 28. Thesis-to-product conversion path

| | |
|---|---|
| **Why** | The thesis is itself a research output, but also potentially a product (consulting, paid data API, course on Paraguay cartography). Mapping this early lets you design chapter 5 (conclusions) to support the product angle. |
| **Method** | Survey: who would pay for "Paraguay cartographic data quality assessment"? What format (report, API, course, consulting)? 5 potential customers interviewed. |
| **Output** | `scratchpad/research/thesis-product-path-2026.md` — viable monetization options. |
| **Owner** | research-tracker + Ivan |
| **Cadence** | Once at chapter 4 completion |

---

# Group 6: Optional / exploratory (2)

## 29. Open-source contribution strategy

| | |
|---|---|
| **Why** | Your `agentic-schemas` repo is MIT-licensed, 20 patterns, interactive viz. It's an asset most agencies don't have. But it's not getting contributions, stars, or forks at scale. Why? And is that the goal? |
| **Method** | Compare against top-50 MIT AI agent repos on GitHub. What's their release cadence, contribution flow, monetization? Decide: is agentic-schemas a "showcase repo" (no contributors needed) or "ecosystem repo" (need contributors)? |
| **Output** | Decision: keep as showcase OR invest in contributors. Specific actions either way. |
| **Owner** | Ivan |
| **Cadence** | Once |

## 30. Personal moonshot — what's next for you?

| | |
|---|---|
| **Why** | In 3-5 years, AI Whisperers could be: (a) acquired by a Paraguayan conglomerate, (b) a 20-person studio dominating LATAM AI services, (c) a thesis + consulting practice, (d) pivoted to a SaaS product, (e) something you haven't imagined. Researching this is strategic career planning. |
| **Method** | Read 5 founder memoirs (Patrick McKenzie, Hiten Shah, Joel Gascoigne, etc.). Talk to 3 founders who exited similar companies. Sketch 3 plausible futures + the bet each requires. |
| **Output** | `scratchpad/research/ivan-5-year-thesis.md` — 3 scenarios, the bets required, the decision criteria. |
| **Owner** | Ivan (personal, not org) |
| **Cadence** | Annually (1 weekend reflection) |

---

# Summary table

| # | Area | Why it matters | Owner | Cadence | Priority |
|---|------|---------------|-------|---------|----------|
| 1 | Past session retrospectives | Pattern mine your own work | Ivan + analyst | Quarterly | 🔴 HIGH |
| 2 | Customer archaeology | Real ICP from real conversions | Sales + Ivan | 6 months | 🔴 HIGH |
| 3 | Margin reality check | Price honestly | Finance | Once + q | |
| 4 | Tool stack audit | Cut waste | Finance + Kiki | Yearly | |
| 5 | Repo hygiene sweep | Reduce drift | Coord + Eng | Quarterly | |
| 6 | Org constitution review | Tune the agents | Coord + Ivan | Monthly → Quarterly | |
| 7 | Competitor deep-dive | Know who's live | Sales + Ivan | Yearly | 🔴 HIGH |
| 8 | Paraguay AI TAM | Know the market | Ivan + Sales | Once | |
| 9 | Pricing benchmark refresh | Don't underprice | Finance + Ivan | Yearly | |
| 10 | Vendor risk mapping | Single points of failure | Eng + Ivan | Yearly | |
| 11 | Hostinger incident monitoring | Avoid repeat suspension | Ivan + skill | Weekly + Quarterly | 🔴 HIGH |
| 12 | Lead-pipeline deep-dive | Revenue blocker | Sales | Daily + Monthly | |
| 13 | Kiki's growth path | Her compounding skill | Kiki + Ivan | Quarterly | 🔴 HIGH |
| 14 | Ivan's bandwidth audit | Avoid burnout | Ivan | 6 months | |
| 15 | Network mapping | Unlock intros | Ivan | Yearly | |
| 16 | Certification landscape | Unlock verticals | Ivan + Kiki | Once | |
| 17 | AI model landscape monitoring | Don't pay for inferior | Analyst | Weekly + Monthly | 🔴 HIGH |
| 18 | Tooling evolution | Stack decay | Eng | Quarterly | 🔴 HIGH |
| 19 | MCP maturity | Bet on the right protocol | Eng | Quarterly | |
| 20 | Regulatory landscape | Sell to regulated | Legal + Ivan | 6 months | |
| 21 | OSS dependency audit | Blast radius | Eng | Yearly | |
| 22 | LATAM tech events | Show up where buyers are | Sales + Ivan | 6 months | |
| 23 | Customer reference research | Convert work to proof | Sales + Ivan | Per project | |
| 24 | LATAM AI talent market | When hiring | Ivan | When hiring | |
| 25 | Thesis literature review | Chapter 1+2 | Research + Ivan | Ongoing | 🔴 HIGH |
| 26 | Paraguay primary data sources | Chapter 3+4 | Ivan + thesis | Once | |
| 27 | Comparable country case studies | Generalize thesis | Research | Once | |
| 28 | Thesis-to-product path | Monetize research | Research + Ivan | Once | |
| 29 | Open-source contribution strategy | Optimize agentic-schemas | Ivan | Once | |
| 30 | Personal moonshot (5-year) | Strategic life design | Ivan | Yearly | |

**8 areas marked HIGH priority** — start there. The other 22 are real but lower urgency.

---

## Practical execution

**If you only have 1 hour this week** → Area 1 (session retrospective) or Area 11 (hostinger compliance check) — both are quick wins.

**If you have a half-day this week** → Areas 1, 11, 12 (lead-pipeline fix), 25 (thesis lit review).

**If you're allocating a research day** → Pick 1 from each of Groups 1, 2, 5 (internal + external + thesis).

**If you want to wire this into the org** → Add 1-2 of these as cron-driven agent outputs. The `research-tracker` weekly cron could own Areas 17, 25. The `business-analyst` daily could check Area 11 weekly.

---

Last updated: 2026-08-13 (initial research agenda)
Next review: 2026-09-13 (after 30 days — what got done, what was useless, what's missing)