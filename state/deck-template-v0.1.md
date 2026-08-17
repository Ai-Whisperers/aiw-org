# Deck Template — Ai-Whisperers (v0.1)

> **10 slides, ~15 minutes.** Adapt for each accelerator / investor pitch. Keep the structure stable; vary the metrics slide and the ask slide.

---

## Slide 1 — Cover

```
AI-WHISPERERS
Paraguay's first AI-native consulting firm.

Deploying agentic operations for Latin American SMBs.

[LOGO]
[Team: Ivan + Kiki + 7 agents]
```

## Slide 2 — Problem

```
The $300K consulting tax
─────────────────────────
LATAM SMBs can't afford McKinsey.
But they still need finance, sales, engineering, research.

Result: single-founder burnout.
Or: no ops function at all.

→ 50M+ LATAM SMBs underserved by AI-native ops.
```

## Slide 3 — Solution

```
7 lead AI agents. 30 days to deploy.
─────────────────────────────────────
┌─────────────────────────┐
│ Business Analyst       │ ─── daily brief for founder
│ Finance Controller     │ ─── cash flow + runway
│ Sales Pipeline         │ ─── inbound + outbound
│ Engineering Roster     │ ─── deploy + cost health
│ Research Tracker       │ ─── thesis + courses
│ Kiki Coach             │ ─── onboarding + training
│ Mgmt Coordinator       │ ─── weekly cross-repo
└─────────────────────────┘
Open-source infra · near-zero marginal cost.
```

## Slide 4 — Demo

```
[SCREENSHOT: business-analyst outbox brief from /opt/data/agents/business-analyst/outbox/]
[SCREENSHOT: sales-pipeline inbound triage brief]
[SCREENSHOT: finance-controller weekly close]
```

## Slide 5 — Traction

```
90 days · $0 → $240 MRR
──────────────────────
▸ MRR: $240/mo
▸ Customer: Rubicón EAS (legal-tech, Paraguay)
▸ Pipeline: 1 named prospect (richar-ruiz)
▸ Agents: 7 lead agents in production
▸ Stack: Cloudflare · n8n · LiteLLM · Evolution API
▸ Compute burn: $400-600/mo (offset by week-1 credits)
```

## Slide 6 — Business model

```
Three tiers · outcome-based pricing
────────────────────────────────────
A · Setup Gs. 1.5M + Gs. 550k/mo    — Solo entrepreneur
B · Setup Gs. 2M + Gs. 1.3M/mo      — SME ops manager
C · Setup Gs. 4.5M + Gs. 2.5M/mo    — Corporate innovation

(Rubicon EAS pricing benchmark: legal LTV 10-50x dental)
```

## Slide 7 — Market

```
LATAM SMB AI-native ops
────────────────────────
▸ TAM: 50M+ LATAM SMBs (PY, AR, BR, MX, CO, CL)
▸ SAM: 2M+ digitally-active SMBs in primary 6 countries
▸ SOM: 50K+ SMBs with founder-burnout signal + consulting budget
▸ Why now: AI agent tech mature, LATAM underfunded, OSS infra cheap
```

## Slide 8 — Team

```
Ivan              Kiki              7 lead AI agents
─────             ─────             ────────────────
Founder / CEO     Co-Founder /      Production-deployed
                  Tech Director     
AI / agent        AI engineering    Finance · Sales · Eng
systems           curriculum        Research · Coach · Mgmt
10+ yrs           [X] yrs           
PY-based          PY-based          PYT (UTC-4)
```

## Slide 9 — Ask

```
[ADAPT PER APPLICATION]
─────────────────────────────────────
For Y Combinator: "$500K for 7% to scale to $5K MRR + first FTE"
For Cloudflare:  "$250K in compute credits to deploy 12 agents at full capacity"
For EU grants:   "€150K to fund EU presence + Compliance Officer"
For IDB Lab:     "$50K to pilot agent-org with 3 LATAM SMBs"
```

## Slide 10 — Appendix (optional)

```
▸ Agent org chart (7 lead + future sub-agents)
▸ Tech stack diagram (Cloudflare Workers → n8n → LiteLLM → agents)
▸ Customer case study (Rubicón EAS — legal lead gen pipeline)
▸ Roadmap: month 3 / 6 / 9 / 12 milestones
▸ Competitive matrix vs traditional consulting, in-house ops, off-shore BPO
```

---

## Versioning

- **v0.1** (current): 2026-08-14
- Update cadence: quarterly, or whenever MRR / pipeline changes materially
- Each application creates a fork of this deck (e.g., `deck-yc-2026q3.pdf`)
- Track in `state/funding.json` → `deck_version`

## Tooling

- Build with: Pitch.com, Google Slides, Figma, Canva
- Export to PDF for sharing
- Host on paragu-ai.com/deck/ for permanent link
- Always watermark with "Confidential — [Program name] application"

## Trademark discipline

- NEVER use banned brand tokens in slide titles, body, or speaker notes
- NEVER reference banned brand products by name (use "Cloudflare Workers" not the parent company name)
- ALWAYS scrub before sending (run `trademark-compliance-scrub` skill)
- ALWAYS use "Ai-Whisperers" (or chosen clean application org name) consistently
