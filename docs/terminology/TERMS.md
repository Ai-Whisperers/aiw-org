# AI Whisperers — Authoritative Terminology

> **This file is authoritative. Add here first, use elsewhere second.**
>
> DEMIURGE-077 — Terminology Library v1
> Last updated: 2026-08-29

All agents, rules, prompts, schemas, and tickets defer to this file for definitions. No local redefinitions. No implicit meanings.

---

## 1. Org structure

```yaml
term: department
category: org_structure
definition: >
  A functional area of the company that mimics a real large-org department. Has a
  mission, role inventory, assigned agents, signal contracts, KPIs, and optional
  parent/child relationships. Identified by kebab-case id (e.g. marketing).
not_to_be_confused_with:
  functional_area: "Broader catalog grouping; a department is an instantiated org unit."
  role: "A responsibility within a department, not the department itself."
used_in:
  - "docs/demiurge/department-taxonomy-v1.md"
  - "docs/demiurge/schemas/role-department.md"
  - "departments/*/"
```

```yaml
term: sub-department
category: org_structure
definition: >
  A department nested under a parent department via parent_dept_id. Operates with
  its own mission and agents but inherits org context from the parent. Example:
  marketing as sub-dept under sales-growth playbook.
not_to_be_confused_with:
  department: "A top-level or standalone functional area without a parent."
used_in:
  - "docs/demiurge/department-taxonomy-v1.md"
  - "docs/demiurge/schemas/role-department.md"
```

```yaml
term: functional area
category: org_structure
definition: >
  A named domain of organizational responsibility used in the role catalog and
  taxonomy (e.g. Operations, Finance & Legal, AI Ops). May map 1:1 to a department
  or span multiple roles before a department is activated.
not_to_be_confused_with:
  department: "An activated org unit with agents, signals, and status; a functional area may exist only in inventory."
used_in:
  - "ROLES-INVENTORY.md"
  - "docs/demiurge/department-taxonomy-v1.md"
```

```yaml
term: tier
category: org_structure
definition: >
  Organizational priority level for departments. T1 = core canonical departments;
  T2 = cross-cutting support; T3 = deferred until promotion trigger; T4 = enterprise
  scale, out of scope at current size.
properties:
  - T1: "Core — Sales, Marketing, Engineering, etc."
  - T2: "Cross-cutting — AI Ops, RevOps, Compliance, etc."
  - T3: "Deferred — activated when promotion trigger fires"
  - T4: "Enterprise — documented in constitution, not in scope now"
not_to_be_confused_with:
  tier_coding: "Role-level readiness indicator (🟢/🟡/🟠/🔴), not department tier."
  urgency_tier: "Communication priority P0–P3, unrelated to org tier."
used_in:
  - "docs/demiurge/department-taxonomy-v1.md"
  - "docs/demiurge/schemas/role-department.md"
  - "ROLES-INVENTORY.md"
```

```yaml
term: status
category: org_structure
definition: >
  Lifecycle state of a department or role. Schema enum (role-department.md):
  skeleton, active, deferred. skeleton = defined but no active agents; active =
  agents running; deferred = catalogued, awaiting promotion trigger. Reserved
  values (plan vocabulary, not yet in all schemas): prototype = experimental build;
  archived = retired, read-only reference.
properties:
  - skeleton (schema)
  - active (schema)
  - deferred (schema)
  - prototype (reserved)
  - archived (reserved)
not_to_be_confused_with:
  agent_status: "draft | active | paused | deprecated — applies to agents, not departments."
used_in:
  - "docs/demiurge/department-taxonomy-v1.md"
  - "docs/demiurge/schemas/role-department.md"
```

```yaml
term: skeleton
category: org_structure
definition: >
  Department status meaning mission, role inventory, source catalog stub, and signal
  types are defined but no active agents run until a focused build session.
not_to_be_confused_with:
  prototype: "Experimental agent or dept build in progress, may have partial agents."
  deferred: "Catalogued for future activation; may lack full skeleton artifacts."
used_in:
  - "docs/demiurge/department-taxonomy-v1.md"
  - "docs/demiurge/schemas/role-department.md"
```

```yaml
term: activation trigger
category: org_structure
definition: >
  A measurable condition that promotes a Tier 2 department from skeleton to active.
  Example: executive-office activates when >5 active depts need CEO-office coordination.
not_to_be_confused_with:
  promotion_trigger: "Applies to Tier 3 departments; similar concept, different tier."
used_in:
  - "docs/demiurge/department-taxonomy-v1.md"
```

```yaml
term: promotion trigger
category: org_structure
definition: >
  A measurable condition that promotes a Tier 3 deferred department to full active
  status. Example: customer-success activates at 5+ recurring clients.
not_to_be_confused_with:
  activation_trigger: "Applies to Tier 2 cross-cutting departments."
used_in:
  - "docs/demiurge/department-taxonomy-v1.md"
  - "docs/demiurge/schemas/role-department.md"
  - "ROLES-INVENTORY.md"
```

```yaml
term: governance node
category: org_structure
definition: >
  A non-standard org unit for oversight rather than operations. The board of directors
  is a governance node — it reviews quarterly but is not a department with signals
  and agents in the standard sense.
used_in:
  - "docs/demiurge/department-taxonomy-v1.md"
```

---

## 2. Agent model

```yaml
term: agent
category: agent_model
definition: >
  The AI entity that performs work. Has a memorable name (not just a role ID), a
  soul, assigned roles, memory layers, skills, tools, and a cadence. Lives in its
  own git repo (aiw-agent-<id>).
properties:
  - id: "kebab-case, e.g. hera-marketing-lead"
  - name: "single memorable name, human-assigned"
  - status: "draft | active | paused | deprecated"
not_to_be_confused_with:
  role: "A function an agent holds; multiple agents may share a role."
  soul: "Immutable identity kernel; agent is the operational wrapper."
used_in:
  - "docs/demiurge/schemas/agent-soul.md"
  - "docs/demiurge/schemas/role-department.md"
```

```yaml
term: soul
category: agent_model
definition: >
  Immutable identity kernel separate from operational memory. Defines archetype,
  values, hard stops, prompt reference, model selection, and version. Changes
  require explicit soul revision ticket — not routine memory updates.
not_to_be_confused_with:
  episodic_memory: "What happened; git-backed run history."
  prompt: "Operational instructions; soul is the character constitution."
used_in:
  - "docs/demiurge/schemas/agent-soul.md"
  - "docs/demiurge/schemas/memory.md"
```

```yaml
term: archetype
category: agent_model
definition: >
  Behavioral classification embedded in a soul. Determines typical role fit and
  interaction style. One of: Strategist, Builder, Watchdog, Curator, Connector,
  Analyst, Coach.
not_to_be_confused_with:
  role: "Specific job function; archetype is character type."
used_in:
  - "docs/demiurge/schemas/agent-soul.md"
```

```yaml
term: lead agent
category: agent_model
definition: >
  The primary agent accountable for a department or domain. Holds the lead role,
  owns cadence for the dept, and is the escalation target for cross-dept signals.
  Example: hera-marketing-lead for Marketing.
not_to_be_confused_with:
  sub_agent: "Supports lead; does not own dept-level accountability."
used_in:
  - "docs/demiurge/schemas/role-department.md"
  - "demiurge/router/revenue-signals.yaml"
```

```yaml
term: sub-agent
category: agent_model
definition: >
  An agent that supports a lead agent within a department. Executes specialized
  tasks (scanning, drafting, monitoring) and reports findings via signals or
  artifacts. Does not own department-level KPIs or external escalation.
not_to_be_confused_with:
  lead_agent: "Owns dept accountability and cross-dept coordination."
used_in:
  - "docs/demiurge/schemas/agent-soul.md"
  - "docs/demiurge/schemas/memory.md"
```

```yaml
term: router
category: agent_model
definition: >
  Specialized agent that dispatches signals, enforces timing rules, and tracks
  quorum. Acts as the internal routing desk — determines who receives what, when,
  and whether SLA/quorum criteria are met.
not_to_be_confused_with:
  channel: "Communication pathway; router manages delivery over channels."
  agent: "Generic worker; router is a specialized dispatch role."
used_in:
  - "docs/demiurge/schemas/router-quorum.md"
  - "docs/demiurge/schemas/signal-channel.md"
  - "demiurge/router/revenue-signals.yaml"
```

```yaml
term: hard stop
category: agent_model
definition: >
  An action boundary embedded in a soul that requires human approval before
  execution. Examples: send_external_message, merge_pr. Includes rate limits
  and designated approver (ivan, kiki, board).
not_to_be_confused_with:
  escalation: "SLA or quorum failure routing; hard stop is pre-action gate."
used_in:
  - "docs/demiurge/schemas/agent-soul.md"
```

```yaml
term: skill
category: agent_model
definition: >
  Hermes skill reference attached to an agent. A packaged capability (prompt +
  procedure) the agent can invoke. Has id, name, path, version, and required flag.
not_to_be_confused_with:
  tool: "External capability (MCP, API, script); skill is instruction-based."
used_in:
  - "docs/demiurge/schemas/agent-soul.md"
```

```yaml
term: tool
category: agent_model
definition: >
  External capability an agent can call: MCP server, script, API, or webhook.
  Credentials stored via BWS secret reference, never inline.
properties:
  - type: "mcp | script | api | webhook"
used_in:
  - "docs/demiurge/schemas/agent-soul.md"
```

```yaml
term: soul version
category: agent_model
definition: >
  Semver identifier bumped when an agent's character evolves (values, archetype,
  hard stops). Not incremented for routine memory or prompt tweaks. Tracked in
  Soul.version with created_at and updated_at timestamps.
not_to_be_confused_with:
  agent_status: "Operational lifecycle; soul version tracks identity evolution."
used_in:
  - "docs/demiurge/schemas/agent-soul.md"
  - "docs/demiurge/schemas/memory.md"
```

---

## 3. Communication & information types

> **Note:** Terms marked `[PENDING IVAN REVIEW]` are schema-derived drafts. Ivan owns
> final definitions for formality, tone, directionality, and urgency tier semantics.

```yaml
term: signal
category: communication
definition: >
  A discrete, typed message between agents or departments indicating a state change
  or requesting downstream action. Machine-processable, routed by the router agent,
  with structured payload, priority, and optional quorum requirement.
not_to_be_confused_with:
  notification: "Sent to inform a human; not intended to trigger agent logic."
  alert: "High-urgency signal requiring immediate response; subset of signal."
  artifact: "Durable stored object; signal may reference artifacts via payload."
used_in:
  - "docs/demiurge/schemas/signal-channel.md"
  - "departments/*/signals.yaml"
  - "demiurge/router/revenue-signals.yaml"
```

```yaml
term: signal type
category: communication
definition: >
  Department-level contract defining what a department emits or expects — not a
  single message instance. Specifies direction (in/out), payload schema, default
  priority, SLA, routing tags, and optional quorum. Example: marketing-content-ready.
not_to_be_confused_with:
  signal: "A single message instance with id, sender, recipients, and status."
used_in:
  - "docs/demiurge/schemas/role-department.md"
  - "departments/*/signals.yaml"
  - "demiurge/router/revenue-signals.yaml"
```

```yaml
term: channel
category: communication
definition: >
  A durable communication pathway signals travel through. Has members (agents or
  departments), a managing router, retention policy, and allowed signal types.
  Types: direct, group, dept, broadcast, cross_dept.
not_to_be_confused_with:
  message_board: "Async collaboration surface; channel is routing infrastructure."
  signal: "A single routed message; channel is the persistent pathway."
used_in:
  - "docs/demiurge/schemas/signal-channel.md"
  - "docs/demiurge/schemas/artifacts.md"
```

```yaml
term: message board
category: communication
definition: >
  A durable async collaboration surface for dept or group conversation. Maps to a
  Channel with type group or dept. Members post message, thread, note, and task
  artifacts; router manages delivery. Use for ongoing reference; use signals when
  time-bound routing, quorum, or SLA is required.
not_to_be_confused_with:
  channel: "Routing infrastructure; message board is the collaboration surface built on a channel."
  signal: "Time-bound routed message with SLA/quorum; message board is persistent async thread."
used_in:
  - "docs/demiurge/schemas/artifacts.md"
```

```yaml
term: direction
category: communication
definition: >
  SignalType contract field indicating whether a signal type is received (in) or
  emitted (out) by a department. Dept-relative perspective on a single signal
  contract, not org-wide flow classification.
not_to_be_confused_with:
  directionality: "Org-wide information-flow classification (inbound/outbound/internal/cross-dept/org-wide); direction is per-dept signal contract only."
used_in:
  - "docs/demiurge/schemas/role-department.md"
  - "departments/*/signals.yaml"
```

```yaml
term: reaction
category: communication
definition: >
  An agent's response to a signal. Records who reacted, when, what action was taken
  (ack, approve, reject, delegate, complete), optional payload, and whether the
  response was within SLA.
used_in:
  - "docs/demiurge/schemas/signal-channel.md"
  - "docs/demiurge/schemas/router-quorum.md"
```

```yaml
term: priority
category: communication
definition: >
  Urgency level on a signal instance. normal = next cadence slot or within 4h;
  urgent = within 1h, notify if unacked; critical = immediate dispatch, escalate
  at 30m.
properties:
  - normal
  - urgent
  - critical
not_to_be_confused_with:
  urgency_tier: "P0–P3 classification for information types; broader than signal priority."
used_in:
  - "docs/demiurge/schemas/signal-channel.md"
  - "departments/*/signals.yaml"
```

```yaml
term: routing_tags
category: communication
definition: >
  String labels on a signal that hint to the router how to dispatch it. Dispatch
  rules match on routing_tags (AND logic). Example: [content, pipeline], [insight, validation].
used_in:
  - "docs/demiurge/schemas/signal-channel.md"
  - "docs/demiurge/schemas/router-quorum.md"
  - "departments/*/signals.yaml"
```

```yaml
term: quorum
category: communication
definition: >
  Reaction criteria that must be met before a signal is considered handled. Defines
  required_count, optional required_agents, time_window, and fallback behavior
  (escalate, auto_resolve, alert, expire).
not_to_be_confused_with:
  SLA: "Time limit for first reaction; quorum is completion criteria."
used_in:
  - "docs/demiurge/schemas/router-quorum.md"
  - "docs/demiurge/schemas/signal-channel.md"
```

```yaml
term: dispatch rule
category: communication
definition: >
  Router configuration specifying who receives a signal based on signal_type,
  routing_tags, and optional priority floor. Includes fan_out strategy:
  all, first_available, or round_robin.
used_in:
  - "docs/demiurge/schemas/router-quorum.md"
```

```yaml
term: broadcast
category: communication
definition: >
  Signal type scoped to an entire department or org. dept_broadcast = agent to
  whole dept; org-wide broadcast reaches all departments. Used for announcements,
  not bilateral requests.
not_to_be_confused_with:
  cross_dept_signal: "Dept-to-dept message with specific recipients; broadcast is one-to-many."
used_in:
  - "docs/demiurge/schemas/signal-channel.md"
```

```yaml
term: cross_dept signal
category: communication
definition: >
  Signal type sent from one department to another. Requires routing_tags and
  follows cross-dept dispatch rules. Example: marketing-content-ready from
  Marketing to Sales.
not_to_be_confused_with:
  broadcast: "One-to-many within or across org; cross_dept is targeted dept-to-dept."
  direct: "Agent-to-agent, not department-scoped."
used_in:
  - "docs/demiurge/schemas/signal-channel.md"
  - "departments/*/signals.yaml"
```

```yaml
term: SLA
category: communication
definition: >
  Service level agreement — maximum time allowed for a reaction to a signal before
  escalation. Defined per signal type or routing tag via timing rules. Expressed
  as ISO 8601 duration (e.g. PT2H = 2 hours).
not_to_be_confused_with:
  quorum: "Completion criteria (who must react); SLA is time limit."
  cadence: "Scheduled agent run frequency; SLA is response deadline."
used_in:
  - "docs/demiurge/schemas/router-quorum.md"
  - "departments/*/signals.yaml"
```

```yaml
term: escalation
category: communication
definition: >
  Routing a signal or artifact to a higher authority when SLA is breached, quorum
  fails, or a hard stop requires human decision. Target is an agent id or
  human:ivan. Recorded as escalation artifact type.
not_to_be_confused_with:
  hard_stop: "Pre-action approval gate; escalation is post-failure routing."
  alert: "Notification of urgency; escalation is formal handoff."
used_in:
  - "docs/demiurge/schemas/router-quorum.md"
  - "docs/demiurge/schemas/artifacts.md"
```

```yaml
term: urgency tier
category: communication
status: "[PENDING IVAN REVIEW]"
definition: >
  Classification of information urgency across the org. Draft mapping from schemas:
  P0 = immediate (maps to critical priority); P1 = same-day (maps to urgent);
  P2 = weekly/default (maps to normal); P3 = async/no deadline.
properties:
  - P0: "Immediate — critical priority, 30m escalation"
  - P1: "Same-day — urgent priority, 1h SLA"
  - P2: "Weekly — normal priority, 4h SLA (default)"
  - P3: "Async — no SLA, next cadence slot"
not_to_be_confused_with:
  priority: "Signal-instance enum (normal/urgent/critical); urgency tier is org-wide classification."
  tier: "Org structure level T1–T4; unrelated."
used_in:
  - "tickets/DEMIURGE-077-terminology-lib/plan.md"
```

```yaml
term: formality level
category: communication
status: "[PENDING IVAN REVIEW]"
definition: >
  Draft placeholder. Degree of formality in communication output. Proposed values:
  formal (external/client-facing), semi-formal (cross-dept professional),
  informal (internal agent-to-agent). Ivan to confirm definitions and usage rules.
properties:
  - formal
  - semi-formal
  - informal
used_in:
  - "tickets/DEMIURGE-077-terminology-lib/plan.md"
```

```yaml
term: tone
category: communication
status: "[PENDING IVAN REVIEW]"
definition: >
  Draft placeholder. Communicative intent of a message. Proposed values: directive
  (command/instruction), advisory (recommendation), informational (facts only),
  confirmatory (acknowledgment/validation). Ivan to confirm definitions.
properties:
  - directive
  - advisory
  - informational
  - confirmatory
used_in:
  - "tickets/DEMIURGE-077-terminology-lib/plan.md"
```

```yaml
term: directionality
category: communication
status: "[PENDING IVAN REVIEW]"
definition: >
  Draft placeholder. Org-wide classification of information flow direction.
  Proposed values: inbound (external → org), outbound (org → external), internal
  (within dept), cross-dept (between departments), org-wide (all departments).
  Distinct from SignalType.direction (in | out), which is dept-relative on a
  single signal contract. Ivan to confirm mapping to signal types and artifact
  visibility.
properties:
  - inbound
  - outbound
  - internal
  - cross-dept
  - org-wide
not_to_be_confused_with:
  direction: "Per-dept signal contract field (in | out); directionality is org-wide flow classification."
used_in:
  - "tickets/DEMIURGE-077-terminology-lib/plan.md"
  - "departments/*/signals.yaml"
```

```yaml
term: notification
category: communication
status: "[PENDING IVAN REVIEW]"
definition: >
  Draft placeholder. A message sent to inform a human of state or outcome. Not
  intended to trigger agent logic or routing. Ivan to confirm distinction from
  signal and alert.
not_to_be_confused_with:
  signal: "Machine-processable event that triggers agent routing."
  alert: "High-urgency subset requiring immediate human attention."
used_in:
  - "tickets/DEMIURGE-077-terminology-lib/plan.md"
```

```yaml
term: alert
category: communication
status: "[PENDING IVAN REVIEW]"
definition: >
  Draft placeholder. High-urgency communication requiring immediate response.
  Subset of signal when machine-routed; may also be human-facing. Ivan to confirm
  relationship to priority=critical and P0 urgency tier.
not_to_be_confused_with:
  notification: "Informational to human; no urgency requirement."
  escalation: "Formal handoff after failure; alert is the urgency signal itself."
used_in:
  - "tickets/DEMIURGE-077-terminology-lib/plan.md"
```

---

## 4. Documents & knowledge

```yaml
term: artifact
category: documents_knowledge
definition: >
  A first-class durable object produced, consumed, or referenced by agents. Has
  type, title, body, author, owner, status, priority, tags, refs, and visibility.
  Signals carry pointers to artifacts; message boards surface them.
not_to_be_confused_with:
  signal: "Time-bound routed message; artifact is persistent stored content."
  document: "Generic term; artifact is the schema-defined type in this system."
used_in:
  - "docs/demiurge/schemas/artifacts.md"
  - "docs/demiurge/schemas/signal-channel.md"
```

```yaml
term: note
category: documents_knowledge
definition: >
  Artifact type for quick capture, context, or meeting scratch. Stored in
  notes/YYYY-MM-DD-<slug>.md in episodic memory. Low ceremony, no validation required.
not_to_be_confused_with:
  thought: "Hypothesis not yet validated; note is factual capture."
  finding: "Validated observation with evidence refs."
used_in:
  - "docs/demiurge/schemas/artifacts.md"
  - "docs/demiurge/schemas/memory.md"
```

```yaml
term: task
category: documents_knowledge
definition: >
  Artifact type for an owned work item with a defined outcome. Dept or cross-agent
  scope. Has required owner, common due date, often links to KPI. Completion may
  trigger a feedback loop. Lives in operational SQLite while open; snapshots to
  episodic git on done.
not_to_be_confused_with:
  todo: "Smaller agent-local action item; task is dept-scoped work."
used_in:
  - "docs/demiurge/schemas/artifacts.md"
  - "docs/demiurge/schemas/memory.md"
```

```yaml
term: todo
category: documents_knowledge
definition: >
  Artifact type for a small actionable item, often agent-local or sub-task of a
  task. Optional due date. Closes locally without triggering feedback loops.
used_in:
  - "docs/demiurge/schemas/artifacts.md"
```

```yaml
term: thought
category: documents_knowledge
definition: >
  Artifact type for a hypothesis, raw reasoning, or unvalidated idea. Stored in
  thoughts/. Promoted to finding only when evidence refs are attached.
not_to_be_confused_with:
  finding: "Validated observation; thought lacks required evidence."
  learning: "Distilled lesson after action; thought is pre-validation."
used_in:
  - "docs/demiurge/schemas/artifacts.md"
```

```yaml
term: finding
category: documents_knowledge
definition: >
  Artifact type for a validated observation from scan or research. Requires ≥1
  source or signal ref. Promotion path: thought → finding → learning → decision.
used_in:
  - "docs/demiurge/schemas/artifacts.md"
```

```yaml
term: learning
category: documents_knowledge
definition: >
  Artifact type for a distilled lesson after action. Feeds feedback loops and
  optionally source key_insights. Not every thought becomes a learning.
used_in:
  - "docs/demiurge/schemas/artifacts.md"
```

```yaml
term: decision
category: documents_knowledge
definition: >
  Artifact type recording a choice with rationale. Append-by-commit in decisions/;
  never force-pushed. May follow from a learning or escalation.
used_in:
  - "docs/demiurge/schemas/artifacts.md"
```

```yaml
term: brief
category: documents_knowledge
definition: >
  Artifact type for structured output such as campaign brief, pipeline summary, or
  product insight. Stored in outbox/ or briefs/ in episodic memory.
not_to_be_confused_with:
  report: "Periodic summary; brief is event-triggered structured output."
used_in:
  - "docs/demiurge/schemas/artifacts.md"
  - "departments/*/signals.yaml"
```

```yaml
term: report
category: documents_knowledge
definition: >
  Artifact type for periodic summaries: health checks, KPI dashboards, scan results.
  Stored in reports/ in episodic memory.
used_in:
  - "docs/demiurge/schemas/artifacts.md"
```

```yaml
term: source
category: documents_knowledge
definition: >
  Literature or community content that grounds a department or role. Has title, url,
  type (book, paper, blog, community, framework, standard, podcast), quality rating
  (1–5), departments/roles informed, and key insights.
not_to_be_confused_with:
  citation: "Reference to a source within a document; source is the cataloged entity."
  artifact: "Agent-produced content; source is external input material."
used_in:
  - "docs/demiurge/schemas/source-catalog.md"
```

```yaml
term: source catalog
category: documents_knowledge
definition: >
  Per-department collection of sources with version, gap notes, and maintainer
  agent (literature scanner). Every active role should have ≥1 source_basis with
  rating ≥3.
used_in:
  - "docs/demiurge/schemas/source-catalog.md"
  - "docs/demiurge/schemas/role-department.md"
```

```yaml
term: citation
category: documents_knowledge
definition: >
  A reference to a source within a document, finding, or artifact. Distinct from
  the source entity itself. Citation discipline owned by Citation/Bibliography
  Specialist role.
not_to_be_confused_with:
  source: "The cataloged external material; citation is the in-document pointer."
used_in:
  - "ROLES-INVENTORY.md"
  - "docs/demiurge/schemas/source-catalog.md"
```

```yaml
term: nugget
category: documents_knowledge
definition: >
  A valuable piece of information embedded in a document that may be left
  intentionally unextracted. Distinct from key_insights (deliberately extracted)
  and findings (validated with refs). Used in document intelligence classification.
used_in:
  - "tickets/DEMIURGE-077-terminology-lib/plan.md"
  - "tickets/DEMIURGE-078 (document intelligence)"
```

---

## 5. Operational

```yaml
term: cadence
category: operational
definition: >
  Schedule defining when and how often an agent acts. Types: scheduled (cron),
  on_signal (router wake), on_demand (human/agent invoke), continuous (watchdog).
  Includes timezone, time_slot (on_hours/off_hours), and idempotency window.
not_to_be_confused_with:
  SLA: "Response deadline for signals; cadence is agent run schedule."
  heartbeat: "Periodic liveness check; cadence is full work run."
used_in:
  - "docs/demiurge/schemas/feedback-kpi-cadence.md"
  - "docs/demiurge/schemas/agent-soul.md"
```

```yaml
term: heartbeat
category: operational
definition: >
  Periodic liveness check for agents. on_hours: every 30 min (06:00–22:00 PYT);
  off_hours: every 15 min (23:00–05:00 PYT). Distinct from full cadence runs.
used_in:
  - "docs/demiurge/schemas/feedback-kpi-cadence.md"
```

```yaml
term: episodic memory
category: operational
definition: >
  Memory layer 2 — what happened. Git-backed per-agent history: outbox, briefs,
  notes, thoughts, findings, lessons, decisions, reports, boards, tasks/done.
  Retention default 365 days. Atomic writes, one outbox file per run per day.
not_to_be_confused_with:
  operational_memory: "Current state in SQLite; episodic is committed history."
  soul: "Identity kernel; never overwritten in episodic layer."
used_in:
  - "docs/demiurge/schemas/memory.md"
```

```yaml
term: community memory
category: operational
definition: >
  Memory layer 2.5 — what we know collectively. Git-backed shared repos (not
  per-agent). Fed by Echo, promoted findings, dept leads, humans. Scope: department,
  cross_dept, or org. Agents read on every run; write via promotion rules.
not_to_be_confused_with:
  episodic_memory: "Per-agent personal history."
  source_catalog: "External literature; community memory is org-produced knowledge."
used_in:
  - "docs/demiurge/schemas/memory.md"
  - "docs/demiurge/schemas/community-memory.md"
```

```yaml
term: operational memory
category: operational
definition: >
  Memory layer 3 — current state. SQLite per agent: idempotency, state_snapshots,
  tasks, todos, board_index, escalations, entity-specific tables. Daily backup
  snapshot. Schema validated every 15 min.
not_to_be_confused_with:
  episodic_memory: "Historical git commits; operational is live mutable state."
used_in:
  - "docs/demiurge/schemas/memory.md"
  - "docs/demiurge/schemas/artifacts.md"
```

```yaml
term: semantic memory
category: operational
definition: >
  Memory layer 4 — cross-agent RAG (deferred). Qdrant-backed vector search over
  episodic and community content. Activation trigger: source catalog >50 entries
  OR eval-gate needs golden trajectories.
not_to_be_confused_with:
  episodic_memory: "Git-backed text history; semantic is vector-indexed retrieval."
used_in:
  - "docs/demiurge/schemas/memory.md"
```

```yaml
term: feedback loop
category: operational
definition: >
  Self-improvement cycle linking a trigger (KPI threshold, signal, schedule) to an
  action (update source catalog, revise soul, adjust cadence, escalate human).
  The more loops active, the better agents perform over time.
not_to_be_confused_with:
  signal: "One-time routed message; feedback loop is recurring improvement cycle."
used_in:
  - "docs/demiurge/schemas/feedback-kpi-cadence.md"
  - "docs/demiurge/schemas/artifacts.md"
  - "demiurge/router/revenue-signals.yaml"
```

```yaml
term: eval gate
category: operational
definition: >
  Quality checkpoint before an agent action or soul change is promoted to active.
  Includes eval harness, golden trajectories, and pass/fail criteria. Owned by
  AI Ops and AI Safety roles.
not_to_be_confused_with:
  hard_stop: "Human approval gate; eval gate is automated quality check."
  quorum: "Signal reaction criteria; eval gate is pre-promotion validation."
used_in:
  - "docs/demiurge/schemas/feedback-kpi-cadence.md"
  - "ROLES-INVENTORY.md"
```

```yaml
term: KPI
category: operational
definition: >
  Key performance indicator for a role or department. Has formula, target, current
  value, unit, measurement cadence, and feedback_trigger linking to a feedback loop
  when thresholds are breached.
used_in:
  - "docs/demiurge/schemas/feedback-kpi-cadence.md"
  - "docs/demiurge/schemas/role-department.md"
```

---

## 6. Roles

```yaml
term: role
category: roles
definition: >
  A function or responsibility within a department. Has title, tier (lead/senior/mid/
  junior/deferred), responsibilities, KPIs, source basis, and agent assignments.
  Multiple agents may share a role; one agent may hold multiple roles.
not_to_be_confused_with:
  agent: "The AI entity doing work; role is the job function assigned."
  archetype: "Soul character type; role is operational job title."
used_in:
  - "docs/demiurge/schemas/role-department.md"
  - "ROLES-INVENTORY.md"
```

```yaml
term: function
category: roles
definition: >
  A domain of work or capability area (e.g. demand generation, pipeline analytics).
  Broader than a single role; a department's mission spans multiple functions
  implemented by its roles.
not_to_be_confused_with:
  role: "Specific assigned job with KPIs and agent; function is the capability domain."
used_in:
  - "ROLES-INVENTORY.md"
  - "tickets/DEMIURGE-077-terminology-lib/plan.md"
```

```yaml
term: responsibility
category: roles
definition: >
  A specific obligation listed under a role. One role may have multiple
  responsibilities. Distinct from function (broader domain) and KPI (measurable
  outcome).
used_in:
  - "docs/demiurge/schemas/role-department.md"
  - "ROLES-INVENTORY.md"
```

```yaml
term: tier coding
category: roles
definition: >
  Visual readiness indicator for roles in the inventory. 🟢 T1 = active now;
  🟡 T2 = next 6 months; 🟠 T3 = 12+ months; 🔴 T4 = enterprise. Distinct from
  department tier (T1–T4 org structure).
not_to_be_confused_with:
  tier: "Department org level; tier coding is role readiness timeline."
  urgency_tier: "Communication priority P0–P3."
used_in:
  - "ROLES-INVENTORY.md"
  - "tickets/DEMIURGE-077-terminology-lib/plan.md"
```

---

## Planned v1.1 terms

Terms listed in DEMIURGE-077 plan scope but deferred to a follow-up pass or DEMIURGE-078:

| Category | Deferred terms |
|----------|----------------|
| Agent model | monitor, scanner, coach, decorator, finder, researcher |
| Communication | request, inform, acknowledgment, timing rule |
| Documents & knowledge | document, spec, plan, transcript, research, synthesis, derived attribute, given attribute, bibliography |
| Operational | cron, soul improvement, reflection |

Add here first when defined; do not define locally in schemas or tickets.

---

## Index

| Category | Term count |
|----------|------------|
| Org structure | 9 |
| Agent model | 10 |
| Communication & information types | 20 |
| Documents & knowledge | 14 |
| Operational | 9 |
| Roles | 4 |
| **Total** | **66** |

Terms marked `[PENDING IVAN REVIEW]`: urgency tier, formality level, tone, directionality, notification, alert.
