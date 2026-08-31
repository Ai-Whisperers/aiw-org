# Research Citations — AIW Org Upgrade 2026-09

> **Purpose**: Primary-source citations for the §6.3 mapping in
> `UPGRADE-PROPOSAL-2026-09.md`. Web-grounded survey of 10 AI researchers
> whose published work is most relevant to multi-agent orchestration, atomic
> composition, feedback loops, evaluation, and org-design-as-code.
>
> **Date**: 2026-09-01
> **Status**: Complete. Phase 1 greenlight pending Ivan.

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

**End of working research file.** §6.3 of the proposal will reference this doc.