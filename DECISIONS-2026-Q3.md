# Decisions — AI Whisperers Org Buildout (2026 Q3)

> Single canonical decisions doc. All autonomous choices made by Erebus for Ivan.
> **Last updated**: 2026-08-14
> **Status**: Ratified (Ivan delegated "you decide, not me")

---

## Reading guide

- **D1-D8**: Phase 0 decisions (infrastructure + patterns)
- **Q1-Q5**: Earlier decisions (location, sub-agent trigger, eval-gate, source-materials, eval timing)
- **v5 NEW**: Storage, dept catalog, agent count decisions
- **Operational**: Token budget, soak length, milestone definition, hard-stops

---

## D1 — Per-agent daily cost cap

**Decision**: $1/day per agent. $10/day total budget. Content-producing agents (sales-pipeline, kiki-coach, research-tracker, marketing-content-producer, course-producer) get $3/day budget during reflection loop.

**Why**: SandBase 2026 cites this as the trap of always-on agents. Without a cap, a runaway loop can rack up $$ in hours.

**Override**: Manual trigger via state.json `override_possible=true` field.

**Enforcement**: `/opt/data/agents/scripts/cost-cap.sh` reads `state/cost-tracker.json`, halts over-budget agents.

---

## D2 — Sales priority order

**Decision**: **Inbound-first**. Outbound sequencing deferred.

**Trigger to add outbound**: 20+ inbound leads/week sustained 4 weeks.

**Why**: ToolDirectory 2026 — "the loud, outbound-first phase of this category peaked and then took a credibility hit. The money, the acquisitions, and the real production deployments in 2026 have moved toward inbound agents that work high-intent website traffic."

**Inbound sources (current)**:
- Rubicon EAS Worker form submissions (CF Worker)
- LinkedIn inbound (with explicit auth)
- Referral partner pings

**Outbound deferred**: cold email, LinkedIn DMs.

---

## D3 — Compliance Officer role

**Decision**: **Named role in `DEFERRED-ROLES.md`. Ivan wears the hat for now.**

**Hard-stop rule**: No EU client contracts accepted until Compliance Officer role is filled by named person (not Ivan alone).

**Why**: EU AI Act 2026 doesn't accept "the CEO is also the compliance officer" as documented ownership.

**Trigger to promote**: First EU client OR $50K MRR.

**What Ivan does now**:
- Trademark scrub on every public-facing asset
- Privacy review on any client contract
- GDPR/LGPD basic compliance

---

## D4 — Storage path

**Decision**: `/opt/data/agents-v2/` as **new sibling dir** of existing `/opt/data/agents/`. Not a new repo. Not inside existing.

**Existing structure preserved**:
- `/opt/data/agents/` — current ORG-AGENTS.md, dept specs, existing 3 agent PROMPT.md files
- `/opt/data/agents-v2/` — new work: patterns, specs, playbooks, prompts, backups, repos, db, scripts

**Why**: Clean separation. Existing ORG-AGENTS.md and agent files remain v0.1.0 archive. v0.2.0 work in new tree.

---

## D5 — Backup policy

**Decision**: **Gitignored state + 6-hour snapshot + manual archive**.

**State files** (`*.json`): NOT in version control. Contain secrets.
**Outbox files** (`outbox/*.md`): Committed to per-agent git repo.
**Logs** (`logs/*.jsonl`): Committed to per-agent git repo (retention 90 days).
**PROMPT.md**: Committed (canonical spec).
**Decisions/Lessons**: Committed (permanent memory).

**6-hour snapshot**: `aiw-state-snapshot-6h` cron at `0 */6 * * *` PYT.
**Manual archive**: `archive/ORG-AGENTS-v0.1.0-2026-08-13.md` (already exists).

---

## D6 — Idempotency contract pattern

**Decision**: **`state.last_run + window check`**.

**Pattern**:
```yaml
idempotency:
  key: state.last_run
  window:
    daily: 24h
    biweekly: 12h
    weekly: 7d
    on-demand: 5min
  duplicate_action: skip + log "duplicate_run"
  override: state.override_possible=true
```

**Example (business-analyst, daily)**:
- Window: 24h
- Check: `state.last_run < now - 24h` → proceed; else → skip + log
- Override: Ivan can manually trigger via `hermes cron run`

---

## D7 — Hard-stop enforcement

**Decision**: **PROMPT.md prose (documentation) + runtime wrapper (enforcement).**

**Why both**: Soft instructions ("confirm before deleting") failed in Kiro and OpenClaw incidents (NiteAgent 2026). Hard stops must be enforced in code, not just text.

**PROMPT.md prose**:
```yaml
hard_stops:
  - action: write_state
    require_approval: false
    rate_limit_per_run: 50
  - action: send_external_message
    require_approval: true
    approved_human: ivan
  - action: merge_pr
    require_approval: true
    approved_human: kiki
    rate_limit_per_run: 5
```

**Runtime wrapper**: `/opt/data/agents-v2/patterns/hard-stop-wrapper.py` checks every action before execution. Blocks if rule violated.

---

## D8 — PROMPT.md template order

**Decision**: **Template AFTER first reference agent, not before.**

**Why**: Writing template first without a real instance produces a generic template that doesn't fit real agents. Reference agent (business-analyst) becomes the gold copy. Template derived from it.

**Process**:
1. Phase 4: Write business-analyst PROMPT.md (12 sections)
2. Phase 4: Save as `PROMPT.md.reference` (gold)
3. Phase 3: Template = gold copy with placeholders
4. Phase 5: New agents derive from template

---

## Q1 — agents-v2 location

**Decision**: New sibling dir, not new repo. See D4.

---

## Q2 — Sub-agent promotion trigger

**Decision**: **500-word / 2-week threshold per lead agent.**

**Per-agent trigger table**:

| Lead agent | Add sub-agent when... |
|------------|----------------------|
| business-analyst | Pipeline section exceeds 200 words |
| management-coordinator | Stuck items exceed 10 |
| kiki-coach | Curriculum queue exceeds 4 weeks backlog |
| finance-controller | Deals open exceed 5 |
| sales-pipeline | Lead volume exceeds 20/week |
| engineering-roster | Deploy health section exceeds 200 words |
| research-tracker | Thesis + courses combined exceed 400 words |

---

## Q3 — Eval-gate scope

**Decision**: **POC on `business-analyst` only.** Document pattern. Defer full rollout to 30-day post-rollout loop.

**Cost**: ~1 day for POC vs ~2 weeks for full rollout. 14x cheaper.

---

## Q4 — Source-materials ownership

**Decision**: **Research dept owns policy. `source-curator` agent (Tier 2) ships in Phase 5 follow-on.**

**Trigger to ship**: source-materials/ > 50 files.

**Cadence**: Weekly freshness sweep by agent. Ivan approves any add/retire.

---

## Q5 — When to write eval-gate infra

**Decision**: **After Phase 8 lands, as first item of 30-day post-rollout loop.**

**Rationale**: Phase 8 produces stable v0.2.0. 30 days of real data = enough material for golden trajectories.

---

## v5 NEW decisions (added 2026-08-14)

### V5-1 — Storage architecture

**Decision**: **Per-agent git repos (17+) + SQLite DBs (11).** 3-layer model.

**Per-agent repo structure**:
```
aiw-agents-<name>/
├── PROMPT.md
├── README.md
├── CHANGELOG.md
├── outbox/{date}.md
├── logs/{date}.jsonl
├── memories/{topic}.md
├── decisions/{date}.md
├── lessons/{topic}.md
├── eval/{golden}.json
└── .gitignore (excludes state/, db/)
```

**Per-agent SQLite DB**:
- `/opt/data/db/<agent>.db`
- Schema: leads/outreach_log (operational), decisions (semantic), idempotency (control), state_snapshots (history)

**Qdrant (deferred to Tier 2)**: semantic memory for RAG, ships when source-materials > 50 files.

### V5-2 — Functional areas

**Decision**: **30 functional areas** (6 Tier 1 + 8 Tier 2 cross-cutting + 12 Tier 3 deferred + 4 Tier 4 enterprise).

**Reasoning**: 6-dept model was too compressed. Real org needs ~30 functional areas.

### V5-3 — Role count

**Decision**: **~135 roles** (vs Session 1's 98).

**Reasoning**: Full literature sweep surfaced 25+ additional roles (FP&A, BDR, Renewals Manager, Channel Sales, Product Marketing, ML Engineer, Data Engineer, Engineering Manager, Privacy Counsel/DPO, etc.).

### V5-4 — Agent count

**Decision**: **~40-50 agents** (vs v4's ~25).

**Reasoning**: 7 Tier 1 leads + ~14 Tier 2 sub-agents + ~8 Tier 2 cross-cutting + ~15 Tier 3 deferred.

### V5-5 — Build order

**Decision**: Management → Sales → Marketing → Engineering → Finance → Research → People.

**Reasoning**: Ivan's directive + dependency chain + revenue-first within non-mgmt.

---

## Operational decisions

### OP-1 — Token budget per phase

**Decision**: **50K tokens cap per phase.** Over → defer to next phase.

### OP-2 — Phase 4 soak length

**Decision**: **3 days, not 7.** Phase 5 has its own 1-day soak per agent.

### OP-3 — Verifier model

**Decision**: **Same model, different prompt + skill.** Budget reality.

### OP-4 — Self-running milestone definition

**Decision**: **7 days all-green + 0 "is X live?" messages/week.**

### OP-5 — EU client hard-stop

**Decision**: **Until Compliance Officer role filled by named person** (per D3).

### OP-6 — Chaos test scenarios

**Decision**: **3 scenarios**: (a) LLM down, (b) corrupt state, (c) malformed tool response.

### OP-7 — Trademark scrub frequency

**Decision**: **Every artifact, every phase.** Not just playbooks.

### OP-8 — Phase 6 split (1-version-good principle)

**Decision**: **Phase 6A: 1 reference playbook + INDEX.** Phase 6B: 5 replicated. Enforces the discipline.

### OP-9 — Hard-stops are non-overridable by LLM

**Decision**: Wrapper enforces. LLM cannot talk itself past hard stops.

### OP-10 — Cron-heartbeat off-hours cadence

**Decision**: **Off-hours (23:00-06:00 PYT): every 15 min.** On-hours (06:00-23:00 PYT): every 30 min.

---

## What Ivan needs to know

These decisions are binding until Ivan explicitly changes them. If any are wrong, the 90-day review (Phase 9 + 30 days) is the natural correction point.

**No re-asking required.** The plan proceeds with these defaults.

---

**Document path**: `/opt/data/agents/DECISIONS-2026-Q3.md`
**Status**: Ratified
**Last updated**: 2026-08-14
