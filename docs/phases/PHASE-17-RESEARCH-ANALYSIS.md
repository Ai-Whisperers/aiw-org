# Research-Driven Analysis — Open Source AI Agent Ecosystem

> Compiled 2026-08-17 by Erebus for AI Whisperers Paraguay EAS
> Source: GitHub API searches, repo READMEs, Plataforma de video/community references

## Tier 1 — Repos To Study (HIGH RELEVANCE)

### 1. claw-empire (⭐ 1,353)
- Local-first, multi-provider (Modelo de IA Code, Codex, Gemini CLI, OpenCode, Kimi Code, GitHub Copilot, Antigravity)
- Pixel-art office UI — shows the company as a living visual
- LESSON: Our `/opt/data/dashboards/` could visualize the AIW org like this
- URL: https://github.com/GreenSheep01201/claw-empire

### 2. nicepkg/auto-company (⭐ 185)
- 14 AI agents (Bezos, Munger, DHH personas) brainstorm + write code + deploy
- Powered by Modelo de IA Code
- LESSON: We have 47 agents already — this is the "departments" version
- URL: https://github.com/nicepkg/auto-company

### 3. NikitaDmitrieff/auto-co-objetivo (⭐ 41)
- ~50 lines of bash that turns Modelo de IA Code into a self-running company
- "It's not a chatbot. It's not a framework. It's ~50 lines of bash."
- LESSON: Our cron-based approach is right; we have MORE than 50 lines
- URL: https://github.com/NikitaDmitrieff/auto-co-objetivo

### 4. Bennettxai/FounderOS-DEMO (⭐ 614)
- "One-person business as AI-assisted departments: comms, funnel, social, finances"
- 16 routes including /comms /funnel /social /finances /agents /tasks /skills
- LESSON: EXACTLY our model — we should map our agents to these routes
- URL: https://github.com/Bennettxai/FounderOS-DEMO

### 5. starmynd-org/infinite-brain-os (⭐ 241)
- Git-backed operating system for running a business with AI agents
- Plain Markdown + YAML, readable by any agent, owned by you
- LESSON: Our `state/*.json` IS the infinite brain — we just need to version it in git
- URL: https://github.com/starmynd-org/infinite-brain-os

### 6. humanlayer/12-factor-agents (⭐ 25,393)
- 12 principles for production-grade LLM agents
- "Most production agents are mostly deterministic code, with LLM steps sprinkled in"
- LESSON: Apply 12-factor audit to our 47 agents

| Factor | Our status | Gap |
|--------|-----------|-----|
| 1. NL to tool calls | ✅ | We use bash/curl/hermes |
| 2. Own your prompts | ✅ | PROMPT.md is ours |
| 3. Own your context window | ⚠️ 6/10 | Audit but not full context engineering |
| 4. Tools as structured outputs | ✅ | Cron + skills |
| 5. Unify execution state | ⚠️ 4/10 | State files split across 10 places |
| 6. Launch/Pause/Resume | ✅ | Cron pause/resume |
| 7. Contact humans with tool calls | ⚠️ 3/10 | WhatsApp not wired to agent prompts |
| 8. Own your control flow | ✅ | Cron schedules |
| 9. Compact errors into context | ✅ | cron runs records |
| 10. Small, focused agents | ✅ | 47 focused agents |
| 11. Trigger from anywhere | ⚠️ 5/10 | Only cron, no webhooks |
| 12. Stateless reducer | ⚠️ 6/10 | Some agents depend on state files |

### 7. mlflow/mlflow (⭐ 27,598)
- Open source AI engineering: trace, evaluate, monitor
- LESSON: Our `eval-gate.py` is our version of mlflow's evaluation harness
- URL: https://github.com/mlflow/mlflow

### 8. lmnr-ai/lmnr (⭐ 3,185)
- Laminar: open-source observability for AI agents (YC S24)
- LESSON: Our `cron-heartbeat` + `self-running-check.py` is our version
- URL: https://github.com/lmnr-ai/lmnr

## Tier 2 — Additional Observability Tools

| Repo | Stars | What it does | Apply to us |
|------|-------|--------------|-------------|
| Signoz | 31,897 | OpenTelemetry-native observability | Replace cron-heartbeat with OTel |
| RagaAI Catalyst | 16,148 | Agent AI observability | Add per-agent tracing |
| openlit | 2,708 | LLM Observability + GPU monitoring | Add cost tracking |
| apache/hertzbeat | 7,364 | AI-powered real-time observability | Multi-cluster monitoring |
| coze-dev/coze-loop | 5,698 | AI Agent Optimization Platform | A/B testing prompts |
| PhyAgentOS | 1,740 | Self-evolving AI OS | Self-improvement loops |
| MemoryOS | 1,556 | Memory OS for personalized agents | Per-coachee memory |

## Key Insights

### Insight 1: The Space Is Exploding But Immature

- Most repos are 6-12 months old
- Most use Modelo de IA Code as foundation
- Most have 14-24 agents (we have **47** — we're AHEAD)
- Almost none have eval-gate + self-running check (we DO — we're ahead)
- None have coaching product integration (we're UNIQUE here)

### Insight 2: The Missing Pieces In Our Build

| Missing piece | Reference | Effort |
|--------------|-----------|--------|
| Unified dashboard (comms, funnel, finances) | FounderOS | 1-2 weeks |
| Agent observability (Laminar-style) | lmnr | 3-5 days |
| WhatsApp human-in-loop | Factor 7 | 1 day |
| Webhook triggers | Factor 11 | 2-3 days |
| Git-backed state | infinite-brain-os | 1 day |
| Cost monitoring per agent | openlit | 2 days |
| Self-improvement loops | PhyAgentOS | 1 week |

### Insight 3: The 12-Factor Audit Reveals Gaps

Per-factor scores for our 47 agents:
- Factor 3 (Context window): 6/10
- Factor 5 (Unify execution state): 4/10 ← **biggest gap**
- Factor 7 (Contact humans): 3/10 ← **second biggest**
- Factor 11 (Trigger from anywhere): 5/10
- Factor 12 (Stateless reducer): 6/10

### Insight 4: The "1000-Person Corp" Model

Per John's message: we should be able to build what 1000-person corps have but can't maintain because of human constraints. With AI:

- Build 1000-person corp structure NOW (no maintenance cost)
- Run only the parts that generate revenue
- Archive/dormant the rest
- Reactivate as needed

**Concrete new departments we should add** (per FounderOS + user vision):

1. **/comms agent** — aggregates WhatsApp, email, Canal de comunicacion
2. **/funnel agent** — lead scoring + conversion tracking
3. **/social agent** — posting cadence + audience growth
4. **/content agent** — editorial calendar (already have marketing-content-producer)
5. **/roadmap agent** — quarterly planning
6. **/brain agent** — knowledge graph
7. **/integrations agent** — monitors connector health
8. **/analytics agent** — real numbers + sparklines

### Insight 5: The Cost Equation Nobody Talks About

Per auto-co-objetivo: **$1.80/cycle, ~30 cycles/day = $54/day/agent**

- With 47 agents at 1 cycle/day = **$84/day = $2,520/month**
- At 5 cycles/day = **$420/day = $12,600/month**
- Our current model (litellm/reasoning) is FREE only because Paraguay pays

**This is UNSUSTAINABLE long-term. Need:**
- Cost monitoring per agent per day
- Cost cap enforcement (per-agent, per-org)
- Cheaper models for non-critical tasks (Haiku for summaries, Sonnet for reasoning)
- Per-token latency tracking

### Insight 6: The Community Around This Is Real

There's a YC-style community forming around autonomous AI companies:
- `/r/LocalLLaMA` has threads on autonomous agents
- HackerNews has Show HN posts monthly
- Plataforma de video creators (Wes Roth, AI Street Talk, NetworkChuck) review these
- Red social/X has #AICompany #AgentArmy hashtags
- Reddit r/AIAgents r/AI_Agents

**We're positioned to be in this community. We should:**
1. Publish our agents-v2 repo as a case study
2. Write a blog post "How we built 47 agents for a 2-person company"
3. Submit to Show HN
4. Get community feedback to improve
5. Network with similar founders

## Recommended Implementation Path (Next 90 Days)

### Days 1-14: Foundation Gaps (12-factor compliance)

| Priority | Action | Reference |
|----------|--------|-----------|
| P0 | Factor 5: Unify state — central state.json + per-agent overrides | infinite-brain-os |
| P0 | Factor 7: WhatsApp human-in-loop for agents | Factor 7 |
| P0 | Factor 11: Webhook triggers for coach-onboarding | Factor 11 |
| P1 | Cost monitoring per agent per day | openlit |
| P1 | Per-token latency tracking | mlflow |

### Days 15-30: Unified Dashboard (FounderOS model)

Build `/org-monitor` dashboard with routes:
- `/` — Pulse (agent roster + last run + uptime)
- `/comms` — Unified inbox (WhatsApp, email)
- `/funnel` — Lead pipeline
- `/finances` — MRR + cost breakdown
- `/agents` — Per-agent stats
- `/tasks` — Task board
- `/skills` — Skill roster
- `/roadmap` — Quarterly plan

### Days 31-60: 1000-Person Corp Departments

Add the 8 new departments per Insight 4:
- /comms /funnel /social /content /roadmap /brain /integrations /analytics
- Each with PROMPT.md + cron job + skill stack
- Each with eval-gate compliance

### Days 61-90: Community + Validation

- Write blog post (English + Spanish)
- Submit Show HN
- Network on HN + Reddit + Red social
- Get feedback, iterate
- Open-source the eval-gate + self-running-check patterns

## What I'm Recommending You Do Right Now

Given the depth of research + your constraints, here's the priority:

1. **THIS WEEK**: Add Factor 7 (WhatsApp human-in-loop) — this unblocks real client work
2. **NEXT WEEK**: Add cost monitoring — the $12,600/month scenario is a real risk
3. **WEEK 3**: Build the unified dashboard — FounderOS-style
4. **WEEK 4+**: Add 8 new departments + community presence

The 12-factor audit is the right frame. Let me know which gap to close first.

---

*Sources: GitHub API (August 2026), 12-factor-agents v1.x, repo READMEs, Plataforma de video/community references*
*Compiled by Erebus for AI Whisperers Paraguay EAS, 2026-08-17*