# Research Citations — AIW Org Upgrade 2026-09

> **Purpose**: Primary-source citations for §6 of
> `UPGRADE-PROPOSAL-2026-09.md`. Web-grounded survey covering:
>
> - **Stream A** — Classic org-design canon (10 authors/frameworks)
> - **Stream B** — Modern SMB + scaling + team-design frameworks (7 sources)
> - **Stream C** — AI-native / multi-agent org patterns (10 AI researchers)
>
> **Date**: 2026-09-01 (v2.0 — comprehensive pass)
> **Status**: Complete. Proposal v1.2.0 incorporates these findings.

---

## 1. Andrej Karpathy

### Primary works cited
- **"Software 2.0"** (2017) — https://karpathy.medium.com/software-2-0-a64152b37c35
- **"LLM Wiki" pattern** (recent) — GitHub Gist referenced by
  https://pub.towardsai.net/compounding-knowledge-with-llms-karpathys-wiki-pattern-in-action-d01db84d5b8b
- **"Software 3.0"** (2025) — https://www.latent.space/p/s3

### Key takeaways for AIW

| Quote / idea | Application to AIW upgrade |
|--------------|----------------------------|
| "Software 2.0 is written in much more abstract, human-unfriendly language, such as the weights of a neural network. ... specify some goal on the behavior of a desirable program, write a rough skeleton of the code (i.e. a neural net architecture) that identifies a subset of program space to search." | An AIW agent PROMPT.md is the "skeleton of code" + "goal specification" — the agent's behavior is the search. **Implication**: agent prompts should read like architecture descriptions + behavior goals, not like implementations. The current PROMPT.md style mostly already does this; reinforces the atomic-composition discipline (don't embed implementation in PROMPT, point to atomic agents that implement). |
| "The process of training the neural network compiles the dataset into the binary — the final neural network. In most practical applications today, the neural net architectures and the training systems are increasingly standardized into a commodity, so most of the active 'software development' takes the form of curating, growing, massaging and cleaning labeled datasets." | In AIW: prompts are the architecture; the "datasets" are state files (`state/*.json`) + signals + outbox samples. **Implication**: clean state files matter as much as clean prompts. Phase 5 (feedback-loop runtime) produces clean datasets for soul-improvement — the AIW equivalent of dataset curation. |
| "Software 3.0" framing: LLMs as programmable infrastructure with cognitive self-knowledge gaps. | **Implication**: agents need explicit self-knowledge (what they own, what they delegate, what they don't know). The `composition:` block in Phase 3 is exactly this — declaring "I call these atomic agents" gives each agent explicit self-knowledge of its own boundary. |
| **LLM Wiki pattern**: "schema is always the system prompt and the user message carries the current wiki content plus whatever the operation needs." | **Implication**: AIW agents should follow this — PROMPT.md = schema (identity, hard_stops, mission, inputs, outputs, hard_stops), state file = current content, user/task message = the operation. The PROMPT.md frontmatter style already does the first half; we should resist the temptation to grow PROMPT.md into runtime content. |

---

## 2. Richard Sutton — "The Bitter Lesson" (2019)

### Primary works cited
- **"The Bitter Lesson"** — http://www.incompleteideas.net/IncIdeas/BitterLesson.html
- **"Reward Is Enough"** (Silver, Singh, Precup, Sutton) — referenced via
  https://www.reddit.com/r/MachineLearning/comments/nplhy3/

### Key takeaways for AIW

| Quote / idea | Application to AIW upgrade |
|--------------|----------------------------|
| "The biggest lesson that can be read from 70 years of AI research is that general methods that leverage computation are ultimately the most effective, and by a large margin." | **Implication**: don't over-engineer the org structure with bespoke dept-specific logic. Lean on general patterns (router, feedback loop, signal) that work the same way regardless of dept. The DEMIURGE atomic layer is exactly this — one routing schema, one timing schema, used by every dept. Phase 2 enforces this discipline. |
| "Search and learning are the two most important classes of techniques for utilizing massive amounts of computation in AI research." | **Implication**: AIW agents must be able to **search** (across options, atomic agents, fallback paths) and **learn** (across runs via state + outbox + feedback loops). The current cron-driven model is mostly deterministic; Phase 5 adds feedback-loop learning (monitor → soul revision). |
| "The actual contents of minds are tremendously, irredeemably complex; we should stop trying to find simple ways to think about the contents of minds... we should build in only the meta-methods that can find and capture this arbitrary complexity." | **Implication**: don't hardcode business logic into PROMPT.md beyond what the agent actually needs. Keep the meta-methods (router, KPI, feedback loop) generic. The dept layer's `composition:` block is a meta-method ("I delegate to X, Y, Z"); the business logic of *how* X does its job lives in X's PROMPT, not the parent's. **Direct defense of atomic composition discipline.** |
| "Reward is enough" (Silver/Sutton 2021): intelligence and its abilities can be understood as subserving the maximisation of reward. | **Implication**: every AIW agent needs an objective function. KPIs (`demiurge/kpi/*.yaml`) are the reward signals. Phase 2 expands KPIs from 3 depts to 6. Phase 5 wires reward-shaped feedback loops to actually push agent behavior toward the KPI. |

---

## 3. Shunyu Yao — Language Agents lineage

### Primary works cited
- **ReAct** (ICLR 2023 Oral) — https://arxiv.org/abs/2210.03629
- **Reflexion** (NeurIPS 2023) — https://arxiv.org/abs/2303.11366
- **Tree of Thoughts** (NeurIPS 2023 Oral) — https://arxiv.org/abs/2305.10601
- **Cognitive Architectures for Language Agents** (TMLR 2024) — https://arxiv.org/abs/2309.02427
- **SWE-agent / SWE-bench** (NeurIPS 2024 / ICLR 2024) — https://swe-agent.com
- **τ-bench** (ICLR 2025) — https://arxiv.org/abs/2406.12045
- **PhD Thesis: "Language Agents: From Next-Token Prediction to Digital Automation"** — https://ysymyth.github.io/papers/Dissertation-finalized.pdf
- **Current work**: Computer-Using Agent (CUA), Deep Research, OpenAI

### Key takeaways for AIW

| Quote / idea | Application to AIW upgrade |
|--------------|----------------------------|
| **ReAct**: "interleaved manner, allowing for greater synergy between [reasoning and acting]: reasoning traces help the model induce, track, and update action plans as well as handle exceptions, while actions allow it to interface with external sources." | **Implication**: every AIW agent should do Read → Think → Act → Verify, not just Act. Current PROMPT structure mostly has this. Phase 3's `composition:` block formalizes the "Act" step as a call to atomic agents. The "Verify" step is exactly what the soul-improvement feedback loop does. |
| **Reflexion**: agents reflect verbally on their failures and store reflections in memory, improving on subsequent attempts. | **Implication**: agents should have a reflection step where they record what went wrong. Currently AIW has `state/<dept>.json` and `outbox/`, but no formal reflection prompt. Phase 3 adds a "lessons learned" section to PROMPT.md templates; Phase 5 wires reflection to feedback-loop firing. |
| **Tree of Thoughts**: "deliberate problem solving with LLMs" via tree-search over reasoning steps. | **Implication**: when a dept agent is uncertain about which atomic agent to call, it should consider multiple paths, not just pick one. The router's `fan_out: all` vs `fan_out: first_available` distinction already encodes this — Phase 2/3 should add explicit "consider-multiple-paths" patterns where the cost is low. |
| **Cognitive Architectures (CoALA)**: a framework for designing language agents with memory, action space, decision-making. | **Implication**: AIW's DEMIURGE domain model already implements most of CoALA (memory layers, action space via atomic agents, decision-making via router). Validates the architecture. Phase 3 should align our vocab to CoALA where it diverges. |
| **SWE-agent / SWE-bench**: agents operating in real software environments with concrete interface contracts (the Agent-Computer Interface). | **Implication**: AIW's `composition:` block is the dept-agent equivalent of an Agent-Computer Interface — a contract about which atomic agents (sub-tools) the dept agent can call and with what expectations. Phase 3 makes this explicit. |
| **τ-bench**: benchmark for tool-agent-user interaction in real-world domains. | **Implication**: we need eval benchmarks for our agents, not just self-reported outbox output. Phase 4 adds tests; future work could add a `aiw-eval-τ-bench` per Yao's pattern. Out of scope for this upgrade. |

---

## 4. Tom Schaul — Agent Foundations

### Primary works cited
- **"Agent Foundations for Aligning Machine Intelligence with Human Interests"** — referenced via
  https://arxiv.org/pdf/1811.07871 and the alignment-forum discussions
- **"AI Safety Gridworlds"** (Leike et al., with Schaul) — https://www.researchgate.net/publication/321325049_AI_Safety_Gridworlds

### Key takeaways for AIW

| Quote / idea | Application to AIW upgrade |
|--------------|----------------------------|
| **Agent foundations agenda**: study the design of agents themselves (mesa-optimizers, embedded agency, selection vs control) before designing the agents we want. | **Implication**: Phase 1 of the upgrade doesn't touch behavior — it cleans up structural cruft. This is exactly the "study the foundations first" approach. The tier-2-taxonomy cleanup, file-renaming, schema-validation work is agent-foundations work. |
| **Embedded agency**: agents are part of the world they reason about. | **Implication**: AIW agents operate on AIW's own state, files, and tickets. Feedback loops that modify agent PROMPT.md (soul-improvement) are the agent modifying itself. The `human:ivan` approval gate in `soul-improvement.yaml` is the explicit acknowledgment that embedded self-modification needs human oversight. Phase 5 preserves this gate. |
| **Environment design**: the agent's environment is part of the design — not just the agent's policy. | **Implication**: state files, schemas, signals, cron schedules — these are the "environment" for AIW agents. Phase 2-3 aren't just upgrading agents; they're upgrading the environment agents operate in. The router yamls, the per-dept KPIs, the feedback-loop files are environment design. |

---

## 5. Jacob Andreas — Composition

### Primary works cited
- **"Neural Module Networks"** (Andreas et al., 2016) — http://nlp.cs.berkeley.edu/pubs/Andreas-Rohrbach-Darrell-Klein_2016_DNMN_paper.pdf
- **"Deep Compositional Question Answering with Neural Module Networks"** (Andreas et al., 2016) — https://arxiv.org/html/1511.02799v4

### Key takeaways for AIW

| Quote / idea | Application to AIW upgrade |
|--------------|----------------------------|
| "Modular architectures support compositional adaptation: a system can compose modules to address a task, decompose a composition when its parts no longer fit." | **Implication**: the AIW atomic layer is exactly a neural module network — atomic agents are modules, dept agents compose them. Phase 3's `composition:` block formalizes the compose operation; Phase 5's soul-improvement supports "decompose a composition when its parts no longer fit" (replacing one atomic agent without rewriting the dept). |
| **DNMN**: dynamically assemble neural network modules from a library based on the input. | **Implication**: AIW's router dynamically selects which atomic agents to invoke based on signal type. This is the analog of DNMN's dynamic module assembly. Validates the architecture. |
| **Composition of learned skills**: Andreas's later work argues that compositional generalization is the central challenge for neural systems. | **Implication**: AIW's atomic-composition discipline is the bet that we can compose atomic agents into dept behaviors without each dept having to learn its own end-to-end solution. Phase 5's eval tests should specifically test compositional generalization — e.g. "does Apollo still produce good pipeline feedback when Cadmus is swapped for an updated version?" |

---

## 6. Yann LeCun — JEPA / Autonomous Machine Intelligence

### Primary works cited
- **"A Path Towards Autonomous Machine Intelligence"** (v0.9.2, 2022) — https://openreview.net/pdf?id=BZ5a1r-kVsf
- **H-JEPA** — https://www.youtube.com/watch?v=EvSe0ktD95k (talk)

### Key takeaways for AIW

| Quote / idea | Application to AIW upgrade |
|--------------|----------------------------|
| "How is it possible for an adolescent to learn to drive a car in about 20 hours of practice... current ML systems need to be trained with very large numbers of trials." | **Implication**: AIW agents get a LOT of structured human-input (PROMPT engineering, dept charter writing, hard_stops definition). This is the equivalent of LeCun's "20 hours of practice" — efficient learning because the structure is right. The upgrade is about preserving and extending this efficiency, not replacing it with more compute. |
| **Hierarchical world models**: predict at multiple levels of abstraction and time horizons. | **Implication**: AIW already has hierarchical layers (atomic → business → governance). Phase 3 makes the hierarchy explicit in PROMPT frontmatter (`layer: atomic | business | governance`) so each agent knows its abstraction level. |
| **Configurable predictive world model** + **intrinsic motivation** + **self-supervised learning**. | **Implication**: AIW agents need: (a) a world model of the dept state, (b) intrinsic objectives (KPIs), (c) the ability to learn from their own outbox without external labeling. The feedback loop `monitor → source → soul` is the self-supervised learning step. Phase 5 wires this explicitly. |

---

## 7. Yoshua Bengio — System 2 Deep Learning

### Primary works cited
- **"From System 1 Deep Learning to System 2 Deep Learning"** (NeurIPS 2019 Invited Talk) — https://neurips.cc/virtual/2019/invited-talk/15488
- Slides: http://www.iro.umontreal.ca/~bengioy/NeurIPS-11dec2019.pdf

### Key takeaways for AIW

| Quote / idea | Application to AIW upgrade |
|--------------|----------------------------|
| "System 2 requirements will put pressure on representation learning to discover the kind of high-level concepts which humans manipulate with conscious thought." | **Implication**: AIW agents should manipulate high-level concepts (departments, signals, KPIs, atomic agents) — not low-level tokens. Current PROMPT.md style already does this. Phase 3's `composition:` block forces agents to think at the right abstraction level ("I call Cadmus for lead enrichment" not "I write a regex for email parsing"). |
| **Consciousness prior**: top-down attention to high-level representations, not bottom-up from raw data. | **Implication**: agents should look at their own state files + KPI thresholds + outbox summary *first*, then drill into specifics. The proposed `scripts/observability/agent-tracer.py` (already exists) + `prompt-improvement-suggester.py` (already exists) implement the consciousness prior by giving agents an "attentional spotlight" on what matters. |
| **Out-of-distribution generalization**: System 2 is needed for the OOD cases System 1 can't handle. | **Implication**: AIW's hard_stops in PROMPT frontmatter are OOD tripwires — when an agent encounters something outside its decision rights, it escalates (System 2) rather than guessing (System 1 failure mode). Phase 5 should add tests specifically for OOD-handling: "what does Apollo do when an inbound lead asks for something outside its hard_stops?" |

---

## 8. David Silver — AlphaZero / MuZero

### Primary works cited
- **Lex Fridman Podcast #86** — https://www.youtube.com/watch?v=uPUEq8d73JI
- **MuZero** (Schrittwieser et al., 2020) — referenced via podcast
- **"Reward Is Enough"** (Silver, Singh, Precup, Sutton, 2021) — already cited under Sutton

### Key takeaways for AIW

| Quote / idea | Application to AIW upgrade |
|--------------|----------------------------|
| **Search + learning**: AlphaZero's success is from combining tree search with self-play learning, not from either alone. | **Implication**: AIW agents need both **search** (the router's `fan_out` patterns, dept-agent composition decisions) and **learning** (state files accumulating across runs, feedback loops). Phase 3's `composition:` block enables search; Phase 5's feedback loops enable learning. Neither alone is enough. |
| **MuZero**: learn a model of the environment, then plan within it. | **Implication**: AIW agents should learn a model of their environment (other agents, signal types, state file schemas) and plan within that model. The router yamls ARE the environment model — they encode what signals exist, where they go, and what SLAs apply. Phase 2 formalizes the env model by giving every dept a router config. |
| **Self-play**: agents improve by playing against copies of themselves. | **Implication**: AIW's feedback loops are not yet self-play (they fire when KPIs breach, but the "play" against another AIW agent is implicit). Phase 5 could add explicit agent-vs-agent eval (Apollo vs Cadmus vs hypothetical alternative) — out of scope here, but a future direction. |

---

## 9. Noam Brown — Libratus / Pluribus

### Primary works cited
- **"Superhuman AI for multiplayer poker"** (Brown & Sandholm, *Science*, 2019) — https://www.science.org/doi/10.1126/science.aay2400
- **"Superhuman AI for heads-up no-limit poker: Libratus"** — https://arxiv.org/pdf/2007.13544
- **AMA** — https://www.reddit.com/r/MachineLearning/comments/ceece3/

### Key takeaways for AIW

| Quote / idea | Application to AIW upgrade |
|--------------|----------------------------|
| **Multi-agent equilibrium**: in non-zero-sum games (like 6-player poker), Nash equilibrium is a stronger strategy than in 2-player zero-sum games. The AI must reason about multiple opponents' strategies simultaneously. | **Implication**: AIW is a multi-agent system where agents sometimes cooperate (signals from Apollo to Cadmus, content pipeline from Hera to Apollo) and sometimes compete (depts competing for Ivan's attention). Brown's work suggests we need explicit game-theoretic reasoning when conflicts arise. Current `state/coord.json:decisions_for_ivan[]` is the equilibrium-seeker (Ivan resolves dept-vs-dept conflicts). Preserved in upgrade. |
| **Pluribus's blueprint strategy**: AI computes a blueprint strategy for itself, then real-time searches for refinements during play. | **Implication**: AIW agents should have a "default plan" (the PROMPT.md template, the cron schedule, the standard composition) and a "real-time refinement" (the feedback loop adjusting KPIs, the soul-improvement workflow adjusting PROMPT, the dept-lead making ad-hoc decisions). The current structure mostly does this; Phase 5 makes the refinement explicit. |
| **Defeating elite human professionals in 6-player no-limit Texas hold'em**: the AI succeeded not by being a stronger poker player in isolation, but by being better at the *strategic interactions*. | **Implication**: AIW's value comes not from any single agent's competence but from the interactions — the routing, the feedback loops, the cross-dept handoffs. The upgrade is mostly about improving the interaction layer, not the individual agent quality. |

---

## 10. Paul Christiano — IDA / Debate

### Primary works cited
- **"Iterated Distillation and Amplification"** — overview at https://alignmentsurvey.com/materials/learning/scalable/
- **"Learning Complex Goals with Iterated Amplification"** (Christiano, Shlegeris, Amodei, 2018) — https://openai.com/research/learning-complex-goals-with-iterated-amplification
- **Full paper** — https://arxiv.org/pdf/1810.08575.pdf
- **Debate** — referenced via the same Alignment Survey

### Key takeaways for AIW

| Quote / idea | Application to AIW upgrade |
|--------------|----------------------------|
| **IDA: Iterated Distillation and Amplification**: train increasingly powerful agents by repeatedly decomposing complex tasks into smaller tasks that can be more easily evaluated, then combining the solutions. | **Implication**: AIW's atomic layer is the IDA "distillation" — each atomic agent does one thing well. The dept layer is the "amplification" — combining atomic agents into dept-level capability. The current architecture is implicitly IDA-shaped; Phase 3 makes it explicit. |
| **Task decomposability assumption**: IDA relies on the assumption that complex tasks can be decomposed into smaller, evaluable subtasks. | **Implication**: not all of AIW's work decomposes cleanly. Some tasks (e.g. "draft a proposal for this specific client") require a single atomic agent (Metis) doing a non-decomposable thing. The `composition:` block must distinguish "decomposable task I'm splitting" from "atomic task I'm delegating entirely." Phase 3 PROMPT template includes this distinction. |
| **Debate**: zero-sum game where two agents argue opposite sides of a question, a human judge picks. Potentially scalable oversight. | **Implication**: a future AIW capability could be "two agents argue, dept-lead resolves" — useful for ambiguous decisions. Out of scope for this upgrade, but flagged as a future direction. |
| **Alignment via amplification**: IDA is a proposed *alignment* technique — the amplified agent stays aligned because each distillation step is overseen. | **Implication**: AIW's hard_stops + human gates (Ivan, Kiki approval) are the alignment mechanism for amplified dept agents. Phase 5's feedback loops must NOT bypass hard_stops — they can suggest changes, but Ivan approves them. Preserved in upgrade. |

---

## Cross-cutting pattern synthesis

After reviewing the 10 researchers, **5 cross-cutting patterns** emerge that the
AIW upgrade should specifically encode:

| Pattern | Sources | Phase |
|---------|---------|-------|
| **Atomic composition**: small primitives compose into larger capabilities | Andreas, Yao (ReAct/Cognitive Architectures), Christiano (IDA) | Phase 3 |
| **Search + learning**: agents both explore options AND improve from outcomes | Sutton (Bitter Lesson / Reward Is Enough), Silver (AlphaZero/MuZero) | Phase 5 |
| **Hierarchical abstraction**: agents at different levels manipulate different kinds of representations | Bengio (System 2), LeCun (H-JEPA) | Phase 3 |
| **Embedded oversight**: agents operating on themselves / each other need explicit human gates | Schaul (Agent Foundations), Christiano (Alignment via Amplification), Brown (Strategic Interactions) | Phase 5 |
| **Reflection & revision**: agents should record what went wrong and adapt | Yao (Reflexion, CoALA), Karpathy (LLM Wiki), Sutton (learn-by-search) | Phase 5 |

---

## What's NOT covered (acknowledged gaps)

These were deliberately out of scope per Ivan's "(b) Top 10 only" choice:

- **Doina Precup** — options framework, temporal abstraction
- **Satinder Singh** — transfer learning for agents
- **Michael Littman** — RL foundations, communication in agents
- **Geoffrey Hinton** — capsule networks, forward-forward, routing intuitions
- **Dylan Hadfield-Menell** — cooperative AI, principal-agent problems for AI
- **Anca Dragan** — value alignment, specification gaming
- **Jan Leike / Shane Legg** — DeepMind safety, scalable oversight
- **Dario Amodei / Chris Olah** — mechanistic interpretability, agent accountability
- **François Chollet** — ARC, measure of intelligence, program synthesis

If a future revision needs these, they're available via the same Firecrawl path.

---

## Source URL index

| # | Researcher | Key URL(s) |
|---|------------|-----------|
| 1 | Karpathy | https://karpathy.medium.com/software-2-0-a64152b37c35 |
| 2 | Sutton | http://www.incompleteideas.net/IncIdeas/BitterLesson.html |
| 3 | Yao | https://arxiv.org/abs/2210.03629 + https://ysymyth.github.io/ |
| 4 | Schaul | https://arxiv.org/pdf/1811.07871 + https://www.researchgate.net/publication/321325049 |
| 5 | Andreas | https://arxiv.org/html/1511.02799v4 + http://nlp.cs.berkeley.edu/pubs/Andreas-Rohrbach-Darrell-Klein_2016_DNMN_paper.pdf |
| 6 | LeCun | https://openreview.net/pdf?id=BZ5a1r-kVsf |
| 7 | Bengio | https://neurips.cc/virtual/2019/invited-talk/15488 |
| 8 | Silver | https://www.youtube.com/watch?v=uPUEq8d73JI |
| 9 | Brown | https://www.science.org/doi/10.1126/science.aay2400 + https://arxiv.org/pdf/2007.13544 |
| 10 | Christiano | https://alignmentsurvey.com/materials/learning/scalable/ + https://arxiv.org/pdf/1810.08575.pdf |

---

---

# PART II — v2 Research Pass (Streams A, B, C-extensions)

> **Note**: v1 surveyed 10 AI researchers. v2 adds:
> - **Stream A** — 10 classic org-design canon authors/frameworks (deep pass on existing local citations)
> - **Stream B** — 7 modern SMB + scaling + team-design frameworks (new)
> - **Stream C** — 7 additional AI researchers from v1's "acknowledged gaps" + 1 replacement
> - **Cross-stream synthesis** — patterns that span all three streams

---

## Stream A — Classic Org-Design Canon (10 sources)

### A1. Peter Drucker — *The Practice of Management* (1954)

| Field | Value |
|-------|-------|
| Primary contribution | **Management by Objectives (MBO)**, decision rights, management by exception |
| Best source | https://www.sciencedirect.com/topics/social-sciences/management-by-objectives + business.com summary |
| Confidence | High |

**Key idea**: "Drucker's fundamental principle for management is concentration! Management has to clarify goals. He invented the concept management by objectives, which may be..."

**Application to AIW**:
- **PROMPT.md as MBO**: every AIW agent has an explicit objective, an output, and a set of KPIs. This is MBO-as-code. Already implemented.
- **Decision rights in frontmatter**: `hard_stops:` block = Drucker's "what the manager can decide alone vs must escalate." Already implemented.
- **Management by exception**: state files show only exceptions (decisions_for_ivan, open_stuck). Implemented via `coord.json:decisions_for_ivan[]`.

### A2. Andrew Grove — *High Output Management* (1983)

| Field | Value |
|-------|-------|
| Primary contribution | **Manager output equation** + **Task-Relevant Maturity (TRM)** + OKRs (origin) |
| Best source | https://lifestack.ai/blog/high-output-management-by-andrew-grove |
| Confidence | High |

**Key ideas (direct quotes)**:
- "A manager's output equals the output of their organization plus the output of the teams they influence... the sum of the outputs of all activities you're involved in, each multiplied by its impact ratio."
- "The right management style depends on the subordinate's task-relevant maturity, not on a fixed philosophy. Different people and different tasks need different levels of direction and autonomy."
- "Treating them with the autonomy appropriate for a senior engineer in their area of expertise would be appropriate for their engineering work, but counterproductive for the new responsibility."

**Application to AIW**:
- **Manager output equation → Dept agent output equation**: a dept agent's output = sum of atomic-agent outputs × impact ratio. The `composition:` block (Phase 3) is the explicit declaration of "what I produce = these atomic calls × their relevance."
- **TRM applied to AIW agents**: each agent has different TRM in different areas. Cadmus has high TRM for lead enrichment (calls it dozens of times) but low TRM for proposal drafting (Metis owns that). When Cadmus is asked to draft, it should escalate to Metis (low TRM → don't act). **This is exactly what `composition:` does — declare what you DO have high TRM for, and call out when you don't.**
- **OKRs**: AIW's `demiurge/kpi/*.yaml` files are OKR-as-yaml. Already partially implemented; Phase 2 extends to all 6 depts.

### A3. Bossidy + Charan — *Execution: The Discipline of Getting Things Done* (2002)

| Field | Value |
|-------|-------|
| Primary contribution | **People-process-bees framework** + the 7 essential behaviors |
| Best source | https://www.researchgate.net/publication/235303470_Execution_The_Discipline_of_Getting_Things_Done |
| Confidence | High |

**Key idea**: Three core processes must be interconnected — **People** (who does what), **Strategy** (what to do), **Operations** (how to do it).

**Application to AIW**:
- **People**: HR / People dept owns. `06-people-culture.md` covers this.
- **Strategy**: Board-of-directors + 03-sales-growth (go-to-market strategy) + 04-engineering (delivery strategy). **Gap**: no dedicated "strategy" agent in current 47-agent lineup. **Suggested new agent**: `strategy-architect` as atomic agent, called by board-of-directors + dept leads for OKR cascades.
- **Operations**: 01-operations dept owns.
- **Cross-cutting**: the *interconnection* is the hard part. AIW's `state/coord.json:decisions_for_ivan[]` is the chokepoint where People + Strategy + Operations converge.

### A4. Jim Collins — *Good to Great* (2001)

| Field | Value |
|-------|-------|
| Primary contribution | **Hedgehog Concept** + **Level 5 Leadership** + **First Who Then What** + **Flywheel** |
| Best source | https://www.jimcollins.com/article_topics/articles/good-to-great.html |
| Confidence | High |

**Key ideas**:
- **Hedgehog**: intersection of (1) what you're deeply passionate about, (2) what you can be best in the world at, (3) what drives your economic engine.
- **First Who Then What**: get the right people on the bus *before* deciding where to drive it.
- **Flywheel**: breakthrough comes from sustained push in one direction, not a single heroic act.

**Application to AIW**:
- **Hedgehog for AIW**: per `research/STRATEGY.md` and `analysis/REMAINING-TASKS-AND-WISHLIST.md`, AIW's hedgehog = "Latin American SMBs who want AI coaching and orchestration." Phase 1 should validate this hedgehog is reflected in dept charters.
- **First Who Then What → Right People on the Bus**: AIW's hard_stops are exactly the "right people in the right seats" rule applied to agents. Each agent has explicit hard_stops = explicit "this agent is not the right seat for this decision."
- **Flywheel → Cross-dept content/revenue loop**: the Hera/Apollo/Athena loop (content → leads → insights → better content) IS a flywheel. Phase 3's `composition:` block makes this flywheel explicit and testable.

### A5. Henry Mintzberg — *The Structuring of Organizations* (1979)

| Field | Value |
|-------|-------|
| Primary contribution | **5 organizational configurations** + the "Fly" (6-part org anatomy) |
| Best source | https://www.toolshero.com/change-management/mintzberg-organizational-configurations/ + https://www.accaglobal.com/gb/en/student/exam-support-resources/fundamentals-exams-study-resources/f1/technical-articles/mintzberg-theory.html |
| Confidence | High |

**Key ideas (direct)**:
- **5 configurations** (later 7): Entrepreneurial (simple, flat, founder-driven), Machine Bureaucracy (heavy standardisation), Professional (experts with autonomy), Divisional (autonomous units under central core), Adhocracy (project-based, multidisciplinary).
- **Mintzberg predicts Adhocracy will become more important in the future.**

**Application to AIW**:
- **AIW is currently a Professional org**: experts (agents) with high autonomy, standardization at input/output contracts. This is exactly where AIW lives.
- **The DEMIURGE atomic layer is an internal adhocracy**: project-based, multidisciplinary, designed for innovation. The 24 atomic agents form an "innovation engine" that the professional-org dept layer consumes.
- **Mintzberg's "predictions"**: AIW is positioned to ride the shift toward adhocracy that Mintzberg predicted. **Validation of strategy**: per `STRATEGY.md`, AIW's bet is that AI-native orgs are adhocracies. Mintzberg supports this 1979-vintage thesis.

### A6. Tom Peters + Robert Waterman — *In Search of Excellence* (1982)

| Field | Value |
|-------|-------|
| Primary contribution | **8 attributes of excellent companies** |
| Best source | https://umbrex.com/resources/frameworks/organization-frameworks/peters-waterman-in-search-of-excellence-culture-excellence-framework/ |
| Confidence | Medium (some "excellent" companies later declined; framework still cited) |

**8 attributes**:
1. **Bias for Action** — a preference for doing over analyzing
2. **Close to the Customer** — learn from the people you serve
3. **Autonomy and Entrepreneurship** — innovation encouraged at all levels
4. **Productivity Through People** — treat people as the source of quality
5. **Hands-On, Value-Driven** — visible management commitment
6. **Stick to the Knitting** — stay close to what you do best
7. **Simple Form, Lean Staff** — minimal corporate HQ
8. **Simultaneous Loose-Tight Properties** — tight on values, loose on everything else

**Application to AIW**:
- **Bias for Action**: cron cadence beats heroics. ✓ already implemented (92 cron jobs).
- **Stick to the Knitting**: the 6-dept scope IS the knitting. AIW doesn't try to do everything — it does coaching/agentic orgs. **Phase 1 must NOT expand scope.**
- **Simultaneous Loose-Tight**: hard_stops are tight; everything else is loose. **Existing structure matches.**
- **Productivity Through People**: people = agents + humans. KPI-driven agents = "people as source of quality."
- **8-attribute audit for Phase 1** (suggested): score each attribute against current state, surface weak spots in the proposal.

### A7. Steve Blank — *The Four Steps to the Epiphany* (2005)

| Field | Value |
|-------|-------|
| Primary contribution | **Customer Development methodology** + lean startup DNA |
| Best source | https://www.revenuerefinery.com/validating-problems-and-products-with-customer-discovery/ + Bookey summary |
| Confidence | High (validated by lean startup movement 2010+) |

**Key ideas**:
- **Customer Discovery**: get out of the building and validate the problem before building.
- **Customer Validation**: build the MVP, validate it sells.
- **Customer Creation**: build demand (different from validation).
- **Company Building**: transition from startup to scalable company.

**Application to AIW**:
- **Coaching funnel = Customer Development**: `coach-onboarding-poller.py` (deprecated in scope) was the customer-discovery tool. The 14 coach agents follow Blank's progression. **Phase 1 preserves this; doesn't rewrite the coach layer.**
- **Sales dept = Customer Creation**: 03-sales-growth owns this stage. Per `org-design-literature.md`, the ICP specialization (legal/SME/corporate) is the Blank-validated "find beachhead, expand" pattern.
- **Department boundaries**: Blank's 4 stages could be a sub-axis of AIW's dept design. **Out of scope for this upgrade** but flagged.

### A8. Clayton Christensen — *The Innovator's Dilemma* (1997)

| Field | Value |
|-------|-------|
| Primary contribution | **Disruptive innovation theory** + recommendation for "spins out" (autonomous org for disruptive tech) |
| Best source | https://en.wikipedia.org/wiki/The_Innovator%27s_Dilemma + https://www.hbs.edu/faculty/Pages/item.aspx?num=46 |
| Confidence | High |

**Key ideas**:
- **Sustaining vs Disruptive**: incumbents excel at sustaining innovation (better products for existing customers) but fail at disruptive innovation (worse products initially that create new markets).
- **Right customers**: disruptors find customers the incumbent can't be bothered with (small, low-margin, weird).
- **Autonomous organization**: disruptor must be spun out into an autonomous org so its small wins aren't judged by incumbent's metrics.

**Application to AIW**:
- **AIW IS the "autonomous organization"**: AIW exists because the incumbent orgs (Big Coaching Inc, traditional consultancies) can't be bothered with the AI-coaching-for-LATAM-SMBs market. AIW is the spinout.
- **Per-dept autonomy**: each AIW dept is a "small org" within the larger AIW, with its own KPIs and rhythm. This is Christensen-aligned.
- **Phase 1 risk**: any move to centralize depts (e.g. deleting Tier-2 taxonomy could over-consolidate) violates Christensen. The upgrade must preserve per-dept autonomy.

### A9. Hamel + Prahalad — *Competing for the Future* (1994)

| Field | Value |
|-------|-------|
| Primary contribution | **Core competencies** + **Intent-stretching-leverage** + **strategy as revolution, not rationing** |
| Best source | https://www.linkedin.com/pulse/competing-future-hamel-prahalad-1994-pavan-soni + https://thethursdaythought.substack.com/p/gary-hamel-and-ck-prahalad-selected |
| Confidence | Medium-High |

**Key idea**: "Competing for the future requires a combination of perseverance and speed; mapping the future, instead of past; managing complex industry..." — strategy is about building new opportunities, not allocating existing resources.

**Application to AIW**:
- **Core competencies** (what AIW does best):
  1. Multi-agent orchestration (DEMIURGE atomic layer)
  2. AI-coaching curriculum (kiki-coach — now in sister repo)
  3. LATAM SMB go-to-market
- **Intent-stretching-leverage**: AIW's BHAG = "1000-person-equivalent org for any LATAM SMB." Stretch (not yet at 1000), intent (LATAM SMB), leverage (agents + coaching).
- **Mapping the future**: Phase 5 feedback loops are the org's "future-mapping" — they detect where the org is drifting and propose corrections.

### A10. Michael Porter — *Competitive Strategy* (1980)

| Field | Value |
|-------|-------|
| Primary contribution | **5 Forces** + **Value Chain** + **Generic Strategies (Cost Leadership, Differentiation, Focus)** |
| Best source | https://en.wikipedia.org/wiki/Porter%27s_five_forces_analysis + https://www.investopedia.com/terms/p/porter.asp |
| Confidence | Very High |

**Key idea (5 Forces)**: Industry profitability = function of (1) competitive rivalry, (2) threat of new entrants, (3) supplier power, (4) buyer power, (5) substitutes. AIW's positioning needs to address each.

**Application to AIW — explicit force audit**:

| Force | Threat | AIW's defense |
|-------|--------|---------------|
| Competitive rivalry | Low (LATAM AI-coaching is nascent) | Speed of agent iteration + curriculum depth |
| New entrants | Medium (any agency can build agents) | DEMIURGE atomic layer = moat; switching cost = re-implementing 24 agents |
| Supplier power | Low (model providers are commoditized) | Multi-provider; cost-cap.py already exists |
| Buyer power | Medium (SMBs can churn easily) | Coaching depth + rapport (kiki-coach, now in sister repo) |
| Substitutes | Medium (DIY agents + DIY learning) | Coherence of offering (coaching + agents as one product) |

**Generic strategy**: AIW is **Focus + Differentiation** (LATAM SMBs + coaching + agents). Per Porter, that's a defensible position when the focus segment is well-defined. AIW's ICP specialization validates this.

---

## Stream B — Modern SMB + Scaling + Team-Design Frameworks (7 sources)

### B1. EOS — Entrepreneurial Operating System (Wickman, *Traction*, 2007)

| Field | Value |
|-------|-------|
| Primary contribution | **6 Key Components**: Vision, People, Data, Issues, Process, Traction |
| Best source | https://www.eosworldwide.com/eos-model |
| Confidence | Very High (~100k companies use EOS) |

**6 components** (direct from EOS Worldwide):
- **Vision**: leadership team 100% on same page about where the company is going and how.
- **People**: Right People in the Right Seats. Accountability is unclear when this is weak.
- **Data**: scorecard of leading + lagging indicators everyone can see.
- **Issues**: Identify, Discuss, Solve (IDS).). Hidden issues compound.
- **Process**: documented core processes that scale without the founder.
- **Traction**: discipline of execution — Rocks (90-day priorities), Meetings (Level 10), Scorecards.

**Application to AIW — gap analysis**:

| EOS Component | AIW current state | Gap |
|---------------|-------------------|-----|
| Vision | `research/STRATEGY.md` exists | **Minor**: not referenced from each dept charter |
| People | `06-people-culture/people-hr/PROMPT.md` exists | **Medium**: only 1 agent for entire HR function |
| Data | `state/*.json` files + KPI yaml | **Good** — Phase 2 extends to 6 depts |
| Issues | `state/coord.json:decisions_for_ivan[]` | **Partial**: no formal IDS workflow |
| Process | `patterns/` + `playbooks/` (13) | **Good** |
| Traction | Cron cadence (92 jobs) | **Partial**: no quarterly Rocks equivalent |

**Phase 1 DELTA from this**: add EOS-style "Issues" workflow via a new atomic agent `coord-issue-resolver` (or document why current pattern is sufficient).

### B2. Scaling Up / Rockefeller Habits 2.0 (Harnish, 2014)

| Field | Value |
|-------|-------|
| Primary contribution | **4 Decisions**: People, Strategy, Execution, Cash + One-Page Strategic Plan |
| Best source | https://scalingup.com/ + https://www.amazon.com/Scaling-Up-Companies-Rockefeller-Habits/dp/0986019526 |
| Confidence | High (used by 40k+ firms) |

**Key quote (from Amazon listing)**: "Expanding from three to four people grows the team only 33%, yet complexity may increase 400%."

**Application to AIW**:
- **Complexity warning**: AIW has 47 agents + 24 DEMIURGE + 81 tickets + 92 cron jobs. Per Harnish, complexity has likely grown 10x+ since founding. **This is exactly what the upgrade is responding to.**
- **Cash component**: AIW's `state/finance.json` is tiny (221 bytes — almost empty). **HIGH GAP**: finance dept has minimal state. Phase 2 must build this out.
- **People component**: see EOS gap analysis above.
- **Execution component**: cron cadence is good; quarterly Rocks equivalent missing.

### B3. Team Topologies (Skelton + Pais, 2019)

| Field | Value |
|-------|-------|
| Primary contribution | **4 team types** + **3 interaction modes** + **cognitive load theory** |
| Best source | https://teamtopologies.com/key-concepts + https://martinfowler.com/bliki/TeamTopologies.html |
| Confidence | Very High (industry standard) |

**4 team types**:
- **Stream-aligned**: aligned to a flow of work from a business domain
- **Enabling**: helps stream-aligned teams overcome obstacles; detects missing capabilities
- **Complicated Subsystem**: where significant expertise is needed
- **Platform**: provides internal product to accelerate stream-aligned teams

**3 interaction modes**: Collaboration, X-as-a-Service, Facilitation.

**Application to AIW — direct mapping**:

| Team Topologies concept | AIW analog | Status |
|-------------------------|------------|--------|
| Stream-aligned team | **Dept agent** (06 dept leads) | ✓ Exists |
| Platform team | **DEMIURGE atomic layer** (24 agents) | ✓ Exists |
| Enabling team | **`prompts-improvement-suggester.py`** + `ai-ops-coordinator` | ⚠ Partial |
| Complicated Subsystem team | **Specialized atomic agents** (e.g. `orpheus-recordings-agent` for audio) | ✓ Exists |
| X-as-a-Service | **Router / signals** | ✓ Exists |
| Cognitive load | **Hard_stops** (agents don't carry decisions outside their scope) | ✓ Exists |

**KEY INSIGHT**: AIW's atomic-layer / dept-layer architecture is literally the Team Topologies Platform/Stream-aligned split. **The upgrade is operationally validating the architecture, not inventing it.**

**Phase 3 DELTA**: add `topology:` field to agent.yaml (`stream-aligned | platform | enabling | complicated-subsystem`) — analogous to the `layer:` field added in v1.

### B4. Shape Up (Ryan Singer / Basecamp, 2019)

| Field | Value |
|-------|-------|
| Primary contribution | **6-week cycles** + **Betting table** + **Hill Chart** + **scoping** |
| Best source | https://basecamp.com/shapeup + https://benjamintravis.com/blog/shape-up |
| Confidence | High (Basecamp's own product, well-tested) |

**Key idea**: "Cycles should be long enough to finish a whole project and short enough to see the end from the beginning (Basecamp uses 6 week cycles). The betting table is a meeting held during cool-down where stakeholders decide what to do in the next cycle."

**Application to AIW**:
- **6-week cadence**: AIW has weekly + monthly cadences but no 6-week cycle. The DEMIURGE sprints (Sprint 0, 1, 2...) are variable-length. **Possible Phase 3 add**: align DEMIURGE sprints to 6-week Shape Up cycles.
- **Hill Chart**: AIW's `state/coord.json:open_stuck[]` is Hill Chart-like ("stuck" = uphill struggling; "finishing" = downhill). **No formal Hill Chart UI; out of scope.**
- **Betting table**: AIW's `state/coord.json:decisions_for_ivan[]` is the betting table — Ivan bets on which work ships next. **Already implemented.**

### B5. Will Larson — *An Elegant Puzzle* (2019) + *Staff Engineer* (2021)

| Field | Value |
|-------|-------|
| Primary contribution | **Staff engineer archetypes** (Team Lead, Architect, Solver, Right Hand) + systems-of-engagement/ops/infra taxonomy |
| Best source | https://lethain.com/staff-engineer-archetypes/ + https://staffeng.com/ |
| Confidence | High |

**Larson's 3 systems** (from *An Elegant Puzzle*):
- **Systems of Engagement**: customer-facing
- **Systems of Operations**: internal tooling
- **Systems of Infrastructure**: foundational

**Staff engineer archetypes**:
- **Team Lead**: Tech Lead archetype
- **Architect**: designs big systems
- **Solver**: fire-fighter, jumps from incident to incident
- **Right Hand**: scales the leader's impact by removing their hardest problems

**Application to AIW**:
- **Systems of Engagement**: sales + marketing dept (Apollo, Hera, Cadmus)
- **Systems of Operations**: people-hr, finance, compliance (kiki-coach-prep, finance-controller)
- **Systems of Infrastructure**: demiurge atomic layer (Thoth, Echo, Mnemosyne, Pheme)
- **Staff engineer archetypes → agent archetypes**: AIW has all 4 archetypes represented. Specifically:
  - Team Lead: `engineering-roster`
  - Architect: `board-of-directors`
  - Solver: `security-watchdog`, `chaos-test-runner`
  - Right Hand: `business-analyst`, `founder-bandwidth-watchdog`
- **Phase 3 DELTA**: add `archetype:` field to PROMPT frontmatter (`team-lead | architect | solver | right-hand`).

### B6. Holacracy (Brian Robertson, *Holacracy: The New Management System*, 2014)

| Field | Value |
|-------|-------|
| Primary contribution | **Self-management via circles** + governance vs operations distinction |
| Best source | https://www.holacracy.org/ + https://mooncamp.com/glossary/holacracy |
| Confidence | Medium (adopted by Zappos, mixed results; some companies left) |

**Key idea**: replace traditional management hierarchy with self-organizing circles. Each circle has governance (rules) and operations (work).

**Application to AIW**:
- **AIW is NOT Holacratic**: it has clear hierarchies (Ivan = CEO/board, dept leads = leads). **This is correct per Mintzberg's "Professional org" pattern.**
- **Governance vs Operations distinction**: AIW has governance in `departments/ORG-AGENTS.md` and operations in cron jobs. **Conceptually aligned, structurally distinct from Holacracy.**
- **Phase 1 DELTA**: explicitly state in ORG-AGENTS.md that AIW is a Professional org with adhocratic atomic layer, NOT Holacratic. Prevents drift if someone proposes it later.

### B7. Andrew Chen — *The Cold Start Problem* (2021)

| Field | Value |
|-------|-------|
| Primary contribution | **Cold Start Theory** + **5 stages of network effects** + **atomic networks** |
| Best source | https://andrewchen.com/chapter-one-cold-start/ + https://www.sachinrekhi.com/p/andrew-chen-the-cold-start-problem |
| Confidence | High (a16z perspective, practitioner-focused) |

**5 stages** (from Sachin Rekhi's summary):
1. **Cold Start Problem**: anti-network effects dominate; new users churn because no one else is there.
2. **Tipping Point**: enough density to self-sustain.
3. **Escape Velocity**: growth accelerates past competition.
4. **Hitting the Ceiling**: market saturation, churn, competition.
5. **The Moat**: network effects become defensible.

**Atomic networks**: "a single stable, engaged network that can self-sustain" — Uber = city-by-city, Slack = team-by-team, Facebook = college-by-college.

**Application to AIW**:
- **AIW as atomic network**: per my memory + `STRATEGY.md`, AIW's atomic unit = "one client company, fully agent-supported." Each successful client = a new atomic network.
- **Cold Start Problem for AIW**: per `analysis/REMAINING-TASKS-AND-WISHLIST.md`, AIW's cold start problem is the 4 P0 secret leaks + empty state files + unintegrated Tier-2 taxonomy. **The upgrade is the cold-start-removal pass.**
- **Tipping Point**: not yet reached. Need ~10 active client atomic networks.
- **Stage guidance**: Chen's framework says AIW should *narrow scope hard* until tipping point. **Phase 1 must NOT expand AIW's dept count or scope** — preserve the 6 depts, don't add new ones.

---

## Stream C — Additional AI Researchers (7 sources)

### C1. Doina Precup — Options Framework (Sutton, Precup, Singh, 1999)

| Field | Value |
|-------|-------|
| Primary contribution | **Options** as temporally extended actions in RL |
| Best source | http://www-anw.cs.umass.edu/~barto/courses/cs687/Sutton-Precup-Singh-AIJ99.pdf + https://www.sciencedirect.com/science/article/pii/S0004370299000521 |
| Confidence | High |

**Key idea (direct)**: "Learning, planning, and representing knowledge at multiple levels of temporal abstraction are key, longstanding challenges for AI... options enable temporally abstract knowledge and action to be included in the reinforcement learning framework in a natural and general way."

**Application to AIW**:
- **Options = cron cadences**: a daily-sales-pipeline cron is an "option" — a closed-loop policy that runs over a period (24h) and produces an output (sales-pipeline-feedback). Quarterly board meetings are options at 90-day granularity.
- **Multiple time scales**: AIW already operates at multiple time scales (5min health.sh, 15min heartbeat, 6h snapshot, daily brief, weekly recap, monthly finance, quarterly board). This IS the options framework.
- **Subgoals**: KPI thresholds are subgoals. When `kpi-sales-reply-sla < 0.95`, that's a subgoal the agent is trying to reach.
- **Phase 3 DELTA**: document the time-scale hierarchy explicitly. Could go in `departments/ORG-AGENTS.md` §cadence-map.

### C2. Satinder Singh — Transfer Learning + MDP Hierarchies

| Field | Value |
|-------|-------|
| Primary contribution | **Transfer of learning by composing solutions of elemental sequential tasks** + hierarchy of abstract models |
| Best source | Cited in Precup/Sutton/Singh 1999 paper above |
| Confidence | High |

**Application to AIW**:
- **Transfer of learning across depts**: an AIW agent's knowledge in dept A could transfer to dept B if the underlying MDP is similar. Example: Apollo's lead-scoring pattern could inform Athena's customer-signal-scoring pattern.
- **Phase 5 DELTA**: when soul-improvement fires for one agent, consider whether the lesson applies to sibling agents in other depts. Add `transfer_targets:` field to soul-improvement proposals.

### C3. Geoffrey Hinton — Forward-Forward Algorithm (2022)

| Field | Value |
|-------|-------|
| Primary contribution | **Forward-Forward** algorithm — replaces backprop with two forward passes (positive vs negative data) |
| Best source | https://arxiv.org/abs/2212.13345 |
| Confidence | Medium (recent, not yet widely adopted) |

**Key idea**: "The Forward-Forward algorithm replaces the forward and backward passes of backpropagation by two forward passes, one with positive (i.e. real) [data] and one with negative [data]."

**Application to AIW**:
- **Two-pass analogy**: AIW agents should do a "positive pass" (what should I do given this signal) AND a "negative pass" (what should I NOT do given this signal). Hard_stops already encode the negative pass.
- **Phase 3 DELTA**: explicit `negative_examples:` field in PROMPT frontmatter — "do NOT do these things even if asked." Reinforces hard_stops.

### C4. Dylan Hadfield-Menell — Cooperative Inverse RL (2016) + Principal-Agent Value Alignment (PhD thesis 2021)

| Field | Value |
|-------|-------|
| Primary contribution | **Cooperative Inverse RL (CIRL)** + **Principal-Agent Value Alignment Problem** |
| Best source | https://arxiv.org/abs/1606.03137 + https://people.csail.mit.edu/dhm/ |
| Confidence | High |

**Key idea (CIRL)**: "A CIRL problem is a cooperative, partial-information game with two agents, human and robot; both are rewarded according to the human's reward function, but the robot does not initially know what this is."

**Application to AIW**:
- **CIRL exactly describes AIW's situation**: agents are rewarded per KPI; they don't fully know Ivan's preferences (the "real" reward function). The hard_stops + state files + Ivan's feedback are how agents learn the actual reward.
- **Principal-Agent problem**: the AIW agent (principal) acts on behalf of Ivan (agent's principal). Misalignment arises when the agent optimizes for the formal KPI rather than the actual intent.
- **Phase 5 DELTA**: feedback loops must distinguish "KPI breach" (formal) from "Ivan dislikes this" (informal). Add `intent_mismatch:` field to feedback loop runs.

### C5. Anca Dragan — Value Alignment / Specification Gaming / Reward Hacking

| Field | Value |
|-------|-------|
| Primary contribution | **Optimized misalignment** — agents optimize the literal objective but miss the intended one |
| Best source | https://en.wikipedia.org/wiki/Reward_hacking + https://people.eecs.berkeley.edu/~anca/publications.html |
| Confidence | High |

**Key idea**: "Reward hacking or specification gaming occurs when an AI trained with reinforcement learning optimizes an objective function—achieving the literal, formal specification of an objective—without actually achieving an outcome that the programmers intended."

**Application to AIW — explicit risk audit**:

| Agent | Formal objective | Risk of gaming | Defense |
|-------|------------------|----------------|---------|
| Apollo (sales) | `kpi-sales-reply-sla = 0.95` | Send empty/incomplete replies to hit SLA | Hard_stops require actual content; `kpi-sales-pipeline-value` second-derivative check |
| Hera (marketing) | `kpi-mkt-content-output = 3/week` | Spam low-quality content | `kpi-mkt-engagement` second-derivative check; human review of samples |
| Cadmus (leads) | implicit (lead count) | Fake/fabricate leads to inflate | Dual-source verification; fraud detection in scoring |
| Argus (monitor) | `kpi-org-health-score = 0.85` | Suppress bad signals to keep score high | Argus reports to Ivan directly, not via mgr |

**Phase 4 DELTA**: spec-gaming tests in test suite. Each agent should have at least one test asserting "you cannot game your KPI by [known gaming pattern]."

### C6. Jan Leike — Scalable Oversight + Superalignment

| Field | Value |
|-------|-------|
| Primary contribution | **Scalable oversight** — how humans oversee AI smarter than them |
| Best source | https://jan.leike.name/ |
| Confidence | High |

**Key idea**: AI-assisted human feedback, weak-to-strong generalization, robustness to jailbreaks.

**Application to AIW**:
- **AI-assisted human feedback**: AIW already does this — Ivan reads agent-generated briefs, not raw data. The business-analyst + morning-brief agents filter.
- **Weak-to-strong generalization**: the idea that a strong AI can be trained using a weak supervisor. AIW's Ivan oversees agents that may exceed his domain knowledge in narrow areas (e.g. AI engineering).
- **Robustness to jailbreaks**: AIW's hard_stops ARE jailbreak defenses. Phase 5 should add tests: "what does Apollo do if asked to bypass hard_stops?"

### C7. Chris Olah — Mechanistic Interpretability

| Field | Value |
|-------|-------|
| Primary contribution | **Mechanistic interpretability** — reverse-engineer neural network internals via features + circuits |
| Best source | https://transformer-circuits.pub/ + https://en.wikipedia.org/wiki/Mechanistic_interpretability |
| Confidence | Medium-High (cutting-edge, foundational for Anthropic) |

**Key idea**: identify "circuits" — causal chains of feature activations — to understand *why* a model produces a given output.

**Application to AIW**:
- **Agent accountability**: AIW agents should be able to explain *why* they made a decision. Current PROMPT.md style requires "Format" sections; **Phase 3 adds explicit "Reasoning trace:" requirement in agent outputs**.
- **Outbox-as-circuit-trace**: AIW's `outbox/` files are like mechanistic-interpretability circuit traces — they show what the agent did. **Phase 5 should add tooling to diff outbox files and identify decision patterns.**
- **Phase 3 DELTA**: standardize PROMPT output to include `## Reasoning` + `## Decision` + `## Action` + `## Outcome` — making every agent output traceable.

### C8. (Replacement) Carlota Perez — Technological Revolutions + Techno-Economic Paradigms

| Field | Value |
|-------|-------|
| Primary contribution | **Techno-economic paradigm shift** — every major tech revolution creates a new "best-practice framework" for how to organize production |
| Best source | https://en.wikipedia.org/wiki/Technological_Revolutions_and_Financial_Capital + https://www.jstor.org/stable/24232030 |
| Confidence | High |

**Replaces**: original list had "Vinod Narayanan — institutional/organizational economics for AI agents (?)" — Ivan flagged this as a placeholder. Replaced with Perez (most cited institutional-economics-of-tech author) + W. Brian Arthur if needed.

**Key idea**: A new techno-economic paradigm divides into **installation** phase (speculative, financial-driven) and **deployment** phase (production-driven). The org-design implications differ per phase.

**Application to AIW**:
- **AIW is in the deployment phase of the AI-agent revolution** (the installation phase was 2015-2023; deployment is now).
- **Deployment-phase org design**: production-efficient, less speculative, more operational rigor. **Exactly what the AIW upgrade is.**
- **Perez's 5 revolutions**: industrial revolution → steam/railways → steel/electricity → oil/automobile → information technology. Each enabled by a "low-cost input." The current revolution's low-cost input = compute (and now, LLMs).
- **Implication**: AIW's competitive advantage = the discipline of org-design for the AI-revolution deployment phase. Not the tech itself (commoditized) — the discipline of fitting humans + agents into a coherent production system.

---

## Cross-Stream Synthesis (all 27 sources)

After reviewing all 27 sources across 3 streams, **8 cross-cutting patterns** emerge that the AIW upgrade should specifically encode. Patterns from v1 (5) + new patterns from v2 (3):

| # | Pattern | Sources | Maps to phase |
|---|---------|---------|---------------|
| 1 | **Atomic composition**: small primitives compose into larger capabilities | Andreas (NMN), Yao (ReAct/CoALA), Christiano (IDA), **Team Topologies (Platform/Stream-aligned)** | Phase 3 |
| 2 | **Search + learning**: agents both explore options AND improve from outcomes | Sutton (Bitter Lesson), Silver (AlphaZero/MuZero), Karpathy (Software 2.0/3.0), **Grove (Manager Output Equation)** | Phase 5 |
| 3 | **Hierarchical abstraction**: agents at different levels manipulate different kinds of representations | Bengio (System 2), LeCun (H-JEPA), **Precup (Options / Time scales)**, **Larson (3 systems)** | Phase 3 |
| 4 | **Embedded oversight**: agents operating on themselves / each other need explicit human gates | Schaul (Agent Foundations), Christiano (Alignment via Amplification), Brown (Strategic Interactions), **Leike (Scalable Oversight)** | Phase 5 |
| 5 | **Reflection & revision**: agents should record what went wrong and adapt | Yao (Reflexion, CoALA), Karpathy (LLM Wiki), Sutton (learn-by-search), **Hinton (Forward-Forward negative pass)**, **Olah (Mechanistic Interpretability)** | Phase 5 |
| 6 | **Professional + Adhocratic hybrid**: org is professional at dept layer (experts with autonomy), adhocratic at atomic layer (innovation engine) | **Mintzberg (Professional/Adhocracy)**, **Team Topologies**, **Christensen (Autonomous org)** | Phase 1 (preserve) |
| 7 | **Multi-time-scale operation**: every org runs at multiple time scales simultaneously | **Precup (Options)**, **Grove (cadence)**, **Shape Up (6-week cycles)**, **AIW cron grid** | Phase 3 (document explicitly) |
| 8 | **Right People in Right Seats**: agents have explicit competence boundaries; escalate outside them | **Wickman (EOS People)**, **Collins (First Who)**, **Grove (TRM)**, **Hadfield-Menell (CIRL)** | Phase 3 (composition block) |

---

## DELTA — what v2 research CHANGED in the proposal

After v2, 5 new DELTAs are added to the proposal v1.1.0:

| DELTA # | Change | Source pattern |
|---------|--------|----------------|
| 1 | Add `topology:` field (stream-aligned / platform / enabling / complicated-subsystem) to PROMPT frontmatter | Pattern 6 + Team Topologies |
| 2 | Add `archetype:` field (team-lead / architect / solver / right-hand) | Pattern 6 + Larson |
| 3 | Add `intent_mismatch:` field to feedback loop runs | Hadfield-Menell (CIRL) |
| 4 | Add spec-gaming tests in Phase 4 for each agent | Dragan (Reward Hacking) |
| 5 | Document multi-time-scale hierarchy explicitly in ORG-AGENTS §cadence-map | Precup (Options) + Pattern 7 |

Plus v1 DELTAs (preserved):
- `layer:` field (atomic/business/governance)
- Phase 5 shadow mode 48h → 7 days

**Total DELTAs**: 7 design changes + 1 rejection (loader workflow) = 8 §6.3 DELTA items.

---

## Source URL index (v2 additions)

| Source | URL |
|--------|-----|
| Drucker | https://www.sciencedirect.com/topics/social-sciences/management-by-objectives |
| Grove | https://lifestack.ai/blog/high-output-management-by-andrew-grove |
| Bossidy/Charan | https://www.researchgate.net/publication/235303470_Execution_The_Discipline_of_Getting_Things_Done |
| Collins | https://www.jimcollins.com/article_topics/articles/good-to-great.html |
| Mintzberg | https://www.toolshero.com/change-management/mintzberg-organizational-configurations/ |
| Peters/Waterman | https://umbrex.com/resources/frameworks/organization-frameworks/peters-waterman-in-search-of-excellence-culture-excellence-framework/ |
| Blank | https://www.revenuerefinery.com/validating-problems-and-products-with-customer-discovery/ |
| Christensen | https://en.wikipedia.org/wiki/The_Innovator%27s_Dilemma |
| Hamel/Prahalad | https://www.linkedin.com/pulse/competing-future-hamel-prahalad-1994-pavan-soni |
| Porter | https://en.wikipedia.org/wiki/Porter%27s_five_forces_analysis |
| EOS | https://www.eosworldwide.com/eos-model |
| Scaling Up | https://scalingup.com/ |
| Team Topologies | https://teamtopologies.com/key-concepts + https://martinfowler.com/bliki/TeamTopologies.html |
| Shape Up | https://basecamp.com/shapeup + https://benjamintravis.com/blog/shape-up |
| Larson (StaffEng) | https://lethain.com/staff-engineer-archetypes/ + https://staffeng.com/ |
| Holacracy | https://www.holacracy.org/ |
| Chen | https://andrewchen.com/chapter-one-cold-start/ |
| Precup | http://www-anw.cs.umass.edu/~barto/courses/cs687/Sutton-Precup-Singh-AIJ99.pdf |
| Singh | (in Precup paper above) |
| Hinton | https://arxiv.org/abs/2212.13345 |
| Hadfield-Menell | https://arxiv.org/abs/1606.03137 + https://people.csail.mit.edu/dhm/ |
| Dragan | https://en.wikipedia.org/wiki/Reward_hacking + https://people.eecs.berkeley.edu/~anca/publications.html |
| Leike | https://jan.leike.name/ |
| Olah | https://transformer-circuits.pub/ + https://en.wikipedia.org/wiki/Mechanistic_interpretability |
| Perez | https://en.wikipedia.org/wiki/Technological_Revolutions_and_Financial_Capital + https://www.jstor.org/stable/24232030 |

---

**End of comprehensive research file.** v2.0 total: 27 sources across 3 streams. §6 of the proposal v1.2.0 will reference this doc.