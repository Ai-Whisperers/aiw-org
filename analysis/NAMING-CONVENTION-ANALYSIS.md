# Naming Convention Analysis — Research & Recommendations

> **Generated**: 2026-08-31
> **Subject**: Critique of the current Greek-mythology (DEMIURGE) + portmanteau (heritage) naming scheme, with researched alternatives and a final recommendation.

---

## TL;DR (the recommendation)

**Stop using Greek mythology. Switch to a domain-based nomenclature with the rule "One name = one role, name is a noun, name reveals purpose."**

The current DEMIURGE scheme has **3 critical problems** (see Analysis below). The recommended replacement is the **NORTH STAR convention** (see Recommendation). It is **semantic, memorable, conflict-free, and inlineable in code/logs/dashboards** without needing a lookup table.

---

## Analysis: What the current naming scheme does well

1. **It's memorable.** Apollo, Hera, Thoth — recognizable from one read.
2. **It groups nicely by pantheon role** (Apollo/Hera/Athena = lead gods; Cadmus/Metis/Clio = helpers).
3. **It has an internal logic** (each name hints at the agent's purpose via Greek myth).
4. **It produces single-word names** that are easy to type.

---

## Analysis: What the current naming scheme does badly

### Problem 1 — **Disambiguation nightmare** (the killer)

Multiple agents share the same root myth in different contexts. To "know what Clio means", you need the LOOKUP TABLE:

| Myth | Multiple associations |
|---|---|
| **Clio** | muse of history AND customer signal collector AND... |
| **Iris** | goddess of rainbow AND community monitor AND... |
| **Apollo** | god of many things (sun, music, prophecy, medicine) AND sales lead |
| **Hermes** | god of many things (messengers, thieves, travel, commerce) AND router |
| **Athena** | goddess of wisdom AND war AND crafts — already used for product discovery AND could be AI safety |
| **Artemis** | NOT in our roster but plausible for security ops |
| **Dionysus** | NOT in our roster but plausible for community/marketing |
| **Prometheus** | NOT in our roster but plausible for engineering/AI safety |

In a multi-agent system, **ambiguous names cause routing errors**. If "Hermes" routes revenue but logs say `Hermes.warn("security alert")` because someone added a Hermes-2 later, you've corrupted your own observability.

**Severity**: HIGH. This will break once you have 50+ agents.

### Problem 2 — **Cultural bias**

Greek mythology:
- Excludes non-Western traditions
- Westerners memorize via Roman names (the user-facing names like "Apollo" are actually Roman)
- Newcomers can't infer function without studying Greek myth

For an org in Paraguay (Paraguay-Geodata) with LATAM customer base, Greek myth is **culturally foreign**. Pick a myth that's globally relevant.

**Severity**: MEDIUM. Doesn't break anything, but it's not inclusive.

### Problem 3 — **No semantic ordering**

In logs, you see `Kronos` and `Apollo` and `Iris` — but there's no alphabetical or functional order. You can't grep a name and know what dept it belongs to.

**Severity**: MEDIUM. Makes grep tooling harder.

### Problem 4 — **Clio collision with itself**

The original Greek Clio is "muse of history." But your `clio-customer-signal-collector` is the agent that GATHERS signals. The historical muse WRITES history. These are different functions. Calling the signal collector "Clio" is **a misnomer** — it would more accurately be Clio + Hermes combined (gathering + delivering).

**Severity**: MEDIUM. This will confuse new operators.

### Problem 5 — **Naming pressure for future depts**

When you need names for new depts:
- DevRel: Apollo? Hermes? Already taken.
- Investor Relations: Plutus? Hermes? Ploutos?
- T&S: Themis? Already taken (classifier).
- CISO: Athena? Already taken.

You're going to **run out of Greek gods** by dept 12, then start using minor gods, then mythological concepts, then it gets weird.

**Severity**: HIGH. This is a scaling problem.

### Problem 6 — **No relation to the codebase**

You have repos like `aiw-agent-apollo-sales-lead`. The package name (`apollo-sales-lead`) embeds both the Greek name AND the function. So the actual code identifier is:
- `apollo-sales-lead` — readable
- `calliope-content-producer` — readable
- `themis-document-classifier` — readable

But the **identifier** in code (the symbol you call) is the full hyphenated thing. The Greek name itself is decorative. So:
- **In code/logs**: long hyphenated strings (`apollo-sales-lead`)
- **In conversation**: Greek name (`Apollo`)

This creates **two parallel naming systems**, which defeats the purpose of having human names.

**Severity**: HIGH.

---

## Research: Better naming conventions (alternatives I considered)

### Option A — **Roman-named numbered agents** (NASA/ESA style)

```
MERCURY-01, MERCURY-02, MERCURY-03
```

- Pro: Battle-tested in mission-critical systems
- Con: Boring. Loses the soul of DEMIURGE.

### Option B — **Function-first compound names** (CHEF/Ansible style)

```
lead-sales, content-producer, signal-collector
```

- Pro: Self-documenting in logs
- Con: Long. No personality. Reads like config, not identity.

### Option C — **Element-based naming** (Apple A-series / Cisco router style)

```
A1 (sales lead), A2 (content), A3 (community), A4 (router)
K1 (knowledge classifier), K2 (knowledge archivist)
```

- Pro: Compact, scales forever, clear dept letter prefix
- Con: Generic. No personality.

### Option D — **NORTH STAR convention** (RECOMMENDED)

**Rule**: One name = one role. Name is a single English word that describes the function. The name is the role, not the agent — when you replace an agent, the name stays.

Format: `function-name` lowercase (single word where possible, hyphen-separated if multi-word).

```
NORTH (overall orchestrator)
├── SALES
│   ├── sales-pipeline-lead
│   ├── sales-enrichment
│   └── sales-proposal-drafter
├── MARKETING
│   ├── marketing-strategy
│   ├── marketing-content
│   └── marketing-community
├── PRODUCT
│   ├── product-discovery
│   └── product-signal-collector
├── OPERATIONS
│   ├── operations-lead
│   ├── operations-coordinator
│   ├── operations-bizops
│   └── operations-business-analyst
├── AIOPS
│   └── aiops-coordinator
├── COMPLIANCE
│   └── compliance-monitor
├── ROUTING
│   └── router-revenue
├── MONITORING
│   └── health-monitor
├── KNOWLEDGE
│   ├── knowledge-classifier
│   ├── knowledge-archivist
│   ├── knowledge-miner
│   ├── knowledge-router
│   ├── knowledge-quality
│   └── knowledge-recordings
└── SCANNING (cross)
    ├── literature-scanner
    └── community-scanner
```

**Why this works**:
1. **The name IS the function** — anyone who sees `sales-pipeline-lead` knows what it does
2. **Department prefix** — every name starts with the dept (SALES, MARKETING, OPERATIONS, etc.) so grep works
3. **Function suffix** — every name ends with the role (lead, collector, monitor, router, scanner)
4. **Scales forever** — adding `MARKETING/PR-15` is fine
5. **No name collisions possible** — names are unique by construction (dept-prefix + function-suffix)
6. **In logs and code**, the name reads naturally: `marketing-content: posted blog draft`
7. **No culture war** — uses English, accessible to anyone who speaks the language
8. **Migration is mechanical** — `sales-pipeline` → `sales-pipeline-lead`, just adds `-lead` suffix
9. **Readable in plain text, JSON, YAML, K8s, Slack, everywhere**

### Option E — **Astronomy/Mythology from OTHER cultures**

- **Arabic**: Jinn (sustained Arabic mythology, no overlaps)
- **Hindu**: Devas (Indra, Agni, Varuna, Saraswati) — clean domains
- **Norse**: Asgard (Odin, Thor, Frigg, Freyja)
- **Japanese**: Kami (Amaterasu, Susanoo, Tsukuyomi)
- **Egyptian**: Anubis, Ra, Thoth — but Thoth is already in your roster

Each has tradeoffs. None solves Problem 1 (disambiguation).

### Option F — **ASTRONOMY** (real-world, scales forever, no collisions)

```
Sirius, Vega, Polaris, Rigel, Capella, Proxima, Betelgeuse
```

- Pro: Real, scientific, 100s of named objects
- Pro: Can group by constellation (sales dept = Lyra, marketing = Orion, etc.)
- Pro: No cultural bias
- Con: Some have awkward pronun (Betelgeuse, Procyon)
- Con: Not really "purpose-revealing" — Sirius is just a star

### Option G — **Martian moons + planets** (NASA nomenclature)

```
Phobos, Deimos (Mars's moons)
Europa, Ganymede, Io, Callisto (Jupiter's)
Titan, Rhea, Iapetus (Saturn's)
```

- Pro: Clean (no Greek myth overlap)
- Pro: 200+ named objects
- Pro: Cultural neutrality
- Con: Same as Astronomy — names don't reveal function

---

## Comparison matrix

| Approach | Disambig | Scale | Memorable | Reveals function | Cultural neutral | Migration cost |
|---|---|---|---|---|---|---|
| **Current (DEMIURGE)** | Poor | Will fail at ~30 | Yes | Sort of | No | (already done) |
| Roman + numbers | Excellent | Infinite | Mediocre | No | No | High |
| Function-first compound | Excellent | Infinite | Mediocre | Yes | Yes | Medium |
| Element + number | Excellent | Infinite | Mediocre | No | Yes | High |
| **NORTH STAR** | Excellent | Infinite | Good | Yes | Yes | Low |
| Non-Greek myth | Poor | Will fail at ~20 | Yes | Sort of | Partial | High |
| Astronomy | Excellent | Infinite | Good | No | Yes | High |
| Martian moons | Excellent | Infinite | Good | No | Yes | High |

---

## The NORTH STAR convention in detail

### Naming rule

```
{dept-prefix}-{function-suffix}
```

**Examples**:
- `marketing-content` — Marketing dept, content production function
- `marketing-strategy` — Marketing dept, strategy function
- `marketing-community` — Marketing dept, community engagement function
- `sales-pipeline-lead` — Sales dept, pipeline management (lead role)
- `sales-enrichment` — Sales dept, lead enrichment
- `sales-proposal-drafter` — Sales dept, proposal drafting
- `product-discovery-lead` — Product dept, discovery lead
- `product-signal-collector` — Product dept, signal collection
- `operations-lead` — Operations dept, operations lead
- `operations-coordinator` — Operations dept, coordination function
- `operations-bizops` — Operations dept, bizops analytics
- `operations-business-analyst` — Operations dept, business analysis
- `aiops-coordinator` — AI Ops dept, agent ops coordination
- `compliance-monitor` — Compliance dept, monitoring
- `router-revenue` — Routing dept, revenue routing
- `health-monitor` — Monitoring dept, health monitoring
- `knowledge-classifier` — Knowledge dept, classification
- `knowledge-archivist` — Knowledge dept, archiving
- `knowledge-miner` — Knowledge dept, extraction/mining
- `knowledge-router` — Knowledge dept, delivery routing
- `knowledge-quality` — Knowledge dept, quality assessment
- `knowledge-recordings` — Knowledge dept, media processing
- `literature-scanner` — Cross-cutting dept, literature scanning
- `community-scanner` — Cross-cutting dept, community scanning
- `compliance-monitor` — Compliance dept, monitoring

### Department codes

| Code | Department |
|---|---|
| `sales` | Sales & Growth |
| `marketing` | Marketing |
| `product` | Product Discovery |
| `operations` | Operations |
| `aiops` | AI Ops |
| `compliance` | Compliance |
| `router` | Routing |
| `monitoring` | Health Monitoring |
| `knowledge` | Knowledge Management |
| `cross` | Cross-cutting |
| `finance` | Finance & Legal (heritage) |
| `engineering` | Engineering & Delivery (heritage) |
| `research` | Research & Education (heritage) |
| `people` | People & Culture (heritage) |

### Identity = function, not agent

**This is the killer insight**: when you replace an agent (different LLM, different infra, different team), the **name doesn't change** because the name is the FUNCTION, not the agent instance.

Example:
- 2026: `marketing-content` is run by Erebus (Mistral) on cron `0 10 * * 1,3,5`
- 2027: `marketing-content` is run by GPT-5 on the same cron, or by a human after promotion
- The name `marketing-content` stays. The implementation changes.

This is exactly how good engineering systems work (`auth-service` stays the same even if you rewrite it in Rust).

### How logs look

```
[2026-08-31 10:00:01] marketing-content: drafted 3 blog posts from brief
[2026-08-31 10:00:05] marketing-content: drafted 3 blog posts from brief
```

You can grep `marketing-content:` and get all activity from that function. No lookup table needed.

### How dashboards look

```yaml
agents:
  - name: marketing-content
    schedule: "0 10 * * 1,3,5"
    owner: ivan
    status: active
    
  - name: sales-pipeline-lead
    schedule: "0 12 * * *"
    owner: ivan
    status: active
```

### Tier 2/3/4 dept naming (cross-cutting and deferred)

When a cross-cutting concern promotes to standalone, just rename it as a department:

| Tier | When promoted | New name |
|---|---|---|
| 2 | Knowledge Mgmt promotes to standalone | `knowledge-manager` (lead) |
| 3 | Customer Success promotes | `customer-success-lead`, `customer-success-renewal`, `customer-success-nps` |
| 4 | M&A dept promotes | `ma-deal-sourcer`, `ma-diligence-runner` |

---

## Migration path from DEMIURGE → NORTH STAR

### Mapping

| DEMIURGE | NORTH STAR |
|---|---|
| Apollo (apollo-sales-lead) | `sales-pipeline-lead` |
| Cadmus (cadmus-lead-enrichment) | `sales-enrichment` |
| Metis (metis-proposal-drafter) | `sales-proposal-drafter` |
| Hera (hera-marketing-lead) | `marketing-strategy` |
| Calliope (calliope-content-producer) | `marketing-content` |
| Iris (iris-community-monitor) | `marketing-community` |
| Athena (athena-product-discovery-lead) | `product-discovery-lead` |
| Clio (clio-customer-signal-collector) | `product-signal-collector` |
| Kronos (kronos-operations-lead) | `operations-lead` |
| management-coordinator (operations) | `operations-coordinator` |
| business-analyst (operations) | `operations-business-analyst` |
| bizops-tracker (operations) | `operations-bizops` |
| ai-ops-coordinator | `aiops-coordinator` |
| compliance-monitor | `compliance-monitor` |
| Hermes (hermes-router-revenue) | `router-revenue` |
| Argus (argus-health-monitor) | `health-monitor` |
| Thoth (thoth-literature-scanner) | `literature-scanner` |
| Echo (echo-community-scanner) | `community-scanner` |
| Themis (themis-document-classifier) | `knowledge-classifier` |
| Mnemosyne (mnemosyne-document-archivist) | `knowledge-archivist` |
| Hephaestus (hephaestus-document-miner) | `knowledge-miner` |
| Pheme (pheme-document-router) | `knowledge-router` |
| Peitho (peitho-language-quality) | `knowledge-quality` |
| Orpheus (orpheus-recordings-agent) | `knowledge-recordings` |
| (heritage) engineering-roster | `engineering-lead` |
| (heritage) devops-monitor | `engineering-devops` |
| (heritage) qa-automation-runner | `engineering-qa` |
| (heritage) security-watchdog | `engineering-security` |
| (heritage) ai-safety-engineer | `ai-safety` |
| (heritage) scope-intake | `engineering-scope-intake` |
| (heritage) delivery-tracker | `engineering-delivery` |
| (heritage) feasibility-gate | `engineering-feasibility` |
| (heritage) chaos-test-runner | `engineering-chaos` |
| (heritage) finance-controller | `finance-controller` |
| (heritage) accounting-automation | `finance-accounting` |
| (heritage) tax-receipt-tracker | `finance-tax` |
| (heritage) procurement-tracker | `finance-procurement` |
| (heritage) kiki-coach | `people-coach` |
| (heritage) founder-bandwidth-watchdog | `people-bandwidth-watchdog` |
| (heritage) research-tracker | `research-tracker` |
| (heritage) thesis-tracker | `research-thesis` |
| (heritage) citation-checker | `research-citations` |
| (heritage) course-producer | `research-courses` |
| (heritage) okr-tracker | `research-okr` |
| (heritage) funding-coordinator | `research-funding` |
| (heritage) source-curator | `research-sources` |

**Migration is mechanical** — every name follows `{dept}-{function}`. No lookup table needed.

### Migration steps

1. **Update all PROMPT.md files** (24 DEMIURGE + 23 heritage = 47 files)
2. **Update all agent.yaml files** (DEMIURGE 24 files)
3. **Update all repo-manifest.yaml files** (DEMIURGE 24 files)
4. **Update scripts** that reference old names (scripts/, cron jobs, dashboards)
5. **Update constitution files** (constitution/01-06-*.md, README.md)
6. **Update analysis files** in `/opt/data/scratchpad/analysis/`
7. **Update prompts/, tickets/, sources/, departments/** files
8. **Add redirect aliases** so old names still work for one release cycle
9. **Cutover**: remove old aliases, commit + push

**Total**: ~150 files to rename. Can be done with `sed`/search-replace in a single script.

---

## What if we don't migrate?

The DEMIURGE scheme will continue to work for ~30 agents. After that:
- You'll run out of unambiguous Greek myth names
- New operators will struggle to remember what each name does
- Logs will become ambiguous when names overlap in meaning
- You'll accumulate lookup tables in PRs and tribal knowledge

For a 47-agent org, **now is the right time** to switch — it's the inflection point before the cost grows.

---

## Final recommendation

**Adopt NORTH STAR convention.** Use `{dept-prefix}-{function-suffix}` for every agent name. Names are lowercase, hyphenated, and self-documenting. Migration is mechanical via search-replace.

If you want to keep some personality, **add a surname suffix** for marketing (e.g., `marketing-content-calliope` or `marketing-content.muse`) — but the canonical identifier stays the function name.

The single biggest gain: **your logs become self-documenting**. `marketing-content: posted 3 blog posts` — anyone reading the log knows what's happening without needing to look up who Calliope is.

---

## Appendix: Other naming ideas I considered but rejected

| Idea | Why rejected |
|---|---|
| Color-based (Red1, Blue2) | Can't scale to 47. Color blindness accessibility. |
| Animal-based (Falcon, Hawk) | Not function-revealing. |
| Tree-based (Oak, Pine, Maple) | Not function-revealing. |
| Element-based (Helium, Neon) | Same problem as astronomy. |
| Maker names (Atlas, Forge, Delta) | Same disambiguation problem as mythology. |
| Acronym soup (SLP, MKT, OPS) | Not memorable, not human. |
| Numeric (1, 2, 3) | Loses all context. |
| GIVEN-FAMILY naming (current heritage scheme) | Cute but doesn't scale. |

**The fundamental tension**: memorable names = mythology/personal (subjective). Function-revealing names = domain-prefixed (objective). NORTH STAR picks the second.

---

## Comparison: how each tier maps in each scheme

### Current DEMIURGE

```
Sales Dept (lead: Apollo):
├── Apollo (lead)
├── Cadmus (enrichment)
└── Metis (proposals)
```

### NORTH STAR

```
Sales Dept (lead: sales-pipeline-lead):
├── sales-pipeline-lead
├── sales-enrichment
└── sales-proposal-drafter
```

### Which is clearer?

If you see `sales-pipeline-lead: scored 2 hot leads today` in a log, you know:
1. It's the sales pipeline lead agent
2. It scored 2 hot leads
3. That's good news

If you see `Apollo: scored 2 hot leads today`, you have to:
1. Look up what Apollo is
2. Look up what Apollo does
3. Then you know it's the sales pipeline lead scored 2 hot leads

**NORTH STAR wins on clarity.**

---

## What about the user's original request for "human-like names"?

NORTH STAR doesn't preclude human names. You can add a nickname/alias field:

```yaml
agent:
  id: sales-pipeline-lead
  nickname: apollo    # for informal conversation
  schedule: "0 12 * * *"
  owner: ivan
```

Then:
- **In code, logs, dashboards**: `sales-pipeline-lead` (canonical, function-revealing)
- **In conversation**: "Apollo" (familiar, easy to say)

You get the best of both worlds.

**This is the final recommendation**: NORTH STAR canonical IDs + optional nickname aliases.

---

## What I recommend you do (concrete steps)

1. **Don't migrate today** — your DEMIURGE scheme works for now
2. **Plan a NORTH STAR migration** for Q4 2026 when you have bandwidth
3. **Use NORTH STAR for any NEW agents** (skip Greek naming for new ones going forward)
4. **Add a `nickname` field** to existing agent.yaml files so DEMIURGE names remain usable in conversation
5. **Document the convention** in `constitution/00-naming-convention.md` so newcomers know the rule

The question is not whether to migrate. The question is **when** to migrate. My recommendation: Q4 2026.
