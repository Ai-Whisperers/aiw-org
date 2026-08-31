# Customer Deployment Template

> Version 1.0.0 · 2026-08-26 · Controlled deployment worksheet, not a public sales page.
> Sources: `TOOLING-TIERS.md`, `ORG-AGENTS.md`, `ROLLBACK-PLAYBOOK.md`, and the supplied coaching research briefs. Prices are planning anchors, refresh currency, tax, hosting, model, and support costs before signature.

## 1. Purpose and completion gate

Use this worksheet to qualify a customer, choose the smallest functioning org slice, record which roles are automated, price the scope, and move through Week 1 / Month 1 / Month 3 gates. The intake is deliberately broad: a 200-question pattern prevents architecture from being built on assumptions. “Complete” means every must-answer item has an owner, every data source has a classification, every integration has a test credential or an explicit deferred status, and the tier and role manifest are signed.

**Required hard stops**

- The customer authorises every connected data source and system.
- Personal data, credentials, client legal records, health information, and intimate coaching content never appear in public output.
- Personalized external messages require human approval; automated acknowledgements are allowed only within the approved flow.
- Never fabricate testimonials, metrics, team members, compliance claims, or pricing statements.
- Never publish numeric prices or internal identifiers on public surfaces.
- Run the trademark scan before releasing public or client-facing copy.
- The AI coach is non-evaluative, non-therapeutic, and not a source of licensed legal, medical, tax, or financial advice.
- A human operator can pause, inspect, correct, export, and delete a session.

Unknowns become tasks. A positive answer is not a decision until its evidence, owner, and date are recorded.

## 2. Customer decision record

| Field | Answer |
|---|---|
| Legal company / individual | |
| Trading name | |
| Country and primary operating region | |
| City, timezone, business hours | |
| Website and canonical production host | |
| Customer owner / decision maker | |
| Technical owner | |
| Privacy or legal contact | |
| Finance approver | |
| Incident contact and backup | |
| Preferred working language | |
| Secondary languages | |
| Headcount today / in 90 days | |
| Locations / jurisdictions | |
| Data residency requirement | |
| Desired go-live date | |
| Intended tier: Micro / Small / Medium | |
| Intended start date | |
| Intake version and last update | |

If headcount crosses a tier boundary, use the higher tier for the next billing cycle unless the contract says otherwise. A 5-person company may be placed in Small when the selected roles, departments, or compliance needs exceed Micro; record why.

## 3. The 200-question intake pattern

Answer in numbered clusters. The first item in each cluster is a blocker. For every “yes,” attach a source document or system record. For every “no,” name the owner and review date.

### A. Business and outcomes (A1–A20)

A1. What customer problem does the organization solve? A2. What outcome should be achieved in 90 days? A3. Which metric measures it? A4. What are the baseline and target? A5. Which team owns it? A6. What must remain human-owned? A7. Which work repeats weekly? A8. What is delayed by a founder bottleneck? A9. What is monthly request volume? A10. What are operating hours and service expectations? A11. Which teams need one source of truth? A12. Which decisions may be automated with review? A13. Which decisions require explicit approval? A14. What would stop the pilot? A15. What is the implementation budget? A16. Who approves a new integration? A17. Who approves an external report? A18. Which existing software is mandatory? A19. What can be retired? A20. What manual work should stop?

### B. Roles and operating model (B1–B20)

B1. Which departments exist? B2. Which are founder-led? B3. Which roles have no written process? B4. What needs daily attention? B5. What needs weekly attention? B6. What is monthly or quarterly? B7. Who receives the morning brief? B8. Who acts on escalations? B9. Who approves a proposal? B10. Who approves a purchase? B11. Who reviews coaching transcripts? B12. Who handles human coach escalation? B13. Who handles complaints? B14. Who owns the incident channel? B15. Who may change prompts? B16. Who may change schedules? B17. Who may rotate credentials? B18. Who is the backup approver? B19. Which automations are disabled at launch? B20. Which role is intentionally human-only?

### C. Data and systems inventory (C1–C20)

C1. List customer, lead, invoice, and staff systems. C2. Which is the canonical customer record? C3. Which is the canonical sales pipeline? C4. Which is the canonical finance ledger? C5. Which is the canonical people directory? C6. Which tools contain documents? C7. Which contain voice or video? C8. Which contain sensitive personal data? C9. Which have APIs? C10. Which require browser-only access? C11. Which export CSV or JSON? C12. Which offer read-only access? C13. Which accept webhooks? C14. Which credentials exist? C15. Where are credentials stored? C16. Which expire? C17. Which data must stay in the customer region? C18. Which may be processed in a secondary region? C19. What is each retention period? C20. What is the deletion and export procedure?

### D. Privacy, security, and compliance (D1–D20)

D1. Is any data special-category or similarly sensitive? D2. Is health information processed? D3. Are beliefs, union membership, sexuality, or disability involved? D4. Is data about children or vulnerable people involved? D5. Is legal advice or strategy discussed? D6. Is medical advice discussed? D7. Is financial or tax advice discussed? D8. What is the lawful purpose? D9. Who is the controller? D10. Who is the processor? D11. What is the retention schedule? D12. Which consent language is approved? D13. Is explicit opt-in required per session? D14. May content be used for model improvement? Default: no. D15. May recordings be reviewed for quality? If yes, who may listen? D16. Is a data processing agreement required? D17. Is a transfer impact assessment required? D18. Who receives breach notification? D19. What is the incident severity matrix? D20. Who signs risk acceptance?

### E. Sales and marketing (E1–E20)

E1. What is the ideal customer profile? E2. Which lead sources are trusted? E3. How are leads scored? E4. Which pipeline stages exist? E5. Who qualifies a lead? E6. What may a bot request? E7. What may a bot never request? E8. Which messages are pre-approved? E9. Which require an editor? E10. What is the follow-up policy? E11. What is the opt-out policy? E12. How are proposals generated? E13. Which pricing rules may be automatic? E14. Which discounts require approval? E15. How are proposals versioned? E16. How is an account created? C17. How is a won or lost decision recorded? C18. What evidence is required for a case study? C19. Which public channels are approved? C20. Which paid acquisition channels are not approved?

### F. Finance, legal, and vendors (F1–F20)

F1. Which accounting periods are used? F2. Which tax or reporting rules apply? F3. Who prepares an invoice? F4. Who approves an expense? F5. Which recurring costs are monitored? F6. Which vendors are mandatory? F7. Which are optional? F8. What service levels apply? F9. Which contracts need renewal alerts? F10. Which purchases need quotes? F11. What is each approver’s limit? F12. What is the unpaid-invoice threshold? F13. Which legal documents are generated? F14. Which templates have counsel approval? F15. Which documents are client-confidential? F16. How are vendor incidents reported? F17. How is a vendor replaced? F18. Which records are audit-required? F19. How long are records retained? F20. Who signs final acceptance?

### G. People and coaching operations (G1–G20)

G1. Who participates? G2. Who is eligible? G3. What is the session language? G4. What is session length? G5. What is cadence? G6. Is it async text, live audio, or roleplay? G7. What is the first useful outcome? G8. Which goals suit coaching? G9. Which goals require a specialist or licensed professional? G10. What is the crisis escalation rule? G11. How is a human coach selected? G12. How is credential evidence collected? G13. What is the coach response target? G14. How is handoff performed? G15. How is a session summarized? G16. Who may read the summary? G17. How is participant feedback collected? G18. How are complaints handled? G19. How is a participant withdrawn? G20. What is the renewal and cancellation policy?

### H. Technology, resilience, and acceptance (H1–H20)

H1. Where will the runtime run? H2. Is a customer-managed VPS required? H3. Is EU residency required? H4. Is a database required per tenant? H5. How many tenants? H6. How many records? H7. How many agent calls daily? H8. What is live-call latency tolerance? H9. What transcription error rate is acceptable? H10. Which model providers are allowed? H11. Which must be avoided? H12. Which language pairs require tests? H13. How is quality measured? H14. How is cost measured? H15. How is output evaluated? H16. How are errors logged? H17. Who receives alerts? H18. What is the rollback trigger? H19. What is the recovery-time objective? H20. What evidence proves completion?

### I. Language and regional culture (I1–I20)

I1. What is the participant’s first language? I2. What is the organization’s default business language? I3. Is Spanish primary in Paraguay or the surrounding market? I4. Is Dutch preferred for the Netherlands or Belgium? I5. Is English required for cross-border teams? I6. Should one language be used throughout? I7. What happens when a participant code-switches? I8. Which terms require literal translation? I9. Which require cultural adaptation? I10. Is formal address appropriate? I11. Is direct feedback expected? I12. Is a slower, warmer opening appropriate? I13. Which goal and commitment terms are preferred? I14. Which regional examples should be removed? I15. Which should be added? I16. Who reviews Spanish? I17. Who reviews Dutch? I18. Who reviews English? I19. How is translation regression tested? I20. Which language is used for incident notices?

### J. Acceptance, measurement, and pilot close (J1–J20)

J1. Which three outcomes are success metrics? J2. What is the baseline period? J3. Who measures them? J4. What is acceptance test one? J5. What is test two? J6. What is test three? J7. What is the brief quality threshold? J8. What is the maximum failed-tick rate? J9. What is the maximum human review time? J10. What is support path one? J11. What is path two? J12. What is the incident channel? J13. How is a failed session corrected? J14. How is a bad coaching recommendation reported? J15. How is a privacy complaint investigated? J16. How is a correction made without rewriting history? J17. What is the pilot completion date? J18. Who decides renewal? J19. What evidence is required for an upsell? J20. What is explicitly out of scope?

## 4. Configuration knobs

Record every knob as `enabled`, `disabled`, or `deferred`. The tier definitions are in `TOOLING-TIERS.md`.

| Knob | Micro (1–5) | Small (5–20) | Medium (20+) | Customer choice |
|---|---|---|---|---|
| Functional agents | 4 | 12 | 47 full matrix, optional agents | |
| Departments | 3 | 6 | 16 surfaces | |
| Finance | business analyst | adds accounting and tax | adds controller/funding | |
| Sales | pipeline + enrichment | adds proposal and RevOps | adds conversion/renewal | |
| Operations | AI ops coordinator | adds bizops/procurement | adds coordinator, OKR, security, eval | |
| Marketing | disabled | content + multimedia | research, content, coaching content | |
| Research | disabled | research + source curator | research intelligence + citations | |
| People | disabled | people/HR | coaching and people leads | |
| Engineering | disabled | limited QA | roster, QA, drift, chaos opt-in | |
| Monitoring | heartbeat + safety | plus eval/compliance | four-writer cluster | |
| Webhook endpoints | 1 | 4 | 14+ | |
| MCP surface | 0–2 | 0–6 | 16 | |
| Cloudflare Workers | 0 | 2 | 6+ | |
| Data residency | customer default | customer default | EU pack when required | |
| Human coach network | no | no | add-on or dedicated partner | |
| EU/LATAM compliance pack | no | add-on | add-on or custom scope | |
| Chaos testing | off | off | opt-in | |

### “What roles do you want automated?” decision tree

1. Is the work a conversation with a person? If no, go to 2. If yes, go to 3.
2. Does it require professional judgment about law, medicine, tax, safety, hiring, firing, compensation, or performance? If yes, mark `HUMAN_ONLY`; otherwise go to 4.
3. Is it coaching, sales roleplay, intake, or follow-up? Coaching loads `coaching-conversation-framework`, `coaching-trilingual-glossary`, `coaching-privacy-protocol`, and the selected vertical profile. Add `coaching-coach-network` only for human handoff. Sales roleplay loads pipeline, proposal, RevOps, privacy, and compliance roles. Intake loads enrichment, privacy, and the vertical prompt. Follow-up uses a template acknowledgement unless a reviewed workflow is approved.
4. Is the task a repeatable decision with a measurable rule? If no, mark `HUMAN_ONLY` or `HITL_AGENT`.
5. Can it be checked by a deterministic test or human reviewer? If no, keep approval in the workflow. If yes, enable the relevant agent with an eval gate.
6. Does it touch personal, confidential, regulated, or cross-border data? If yes, load `coaching-privacy-protocol` and settle purpose, residency, retention, and deletion before test data is processed.
7. Is a human coach or live call needed? If yes, enable Pro-level capability, load `coaching-coach-network`, and define response and escalation SLAs.
8. Is the team above 20 or operating in multiple jurisdictions? If yes, use Medium and run full compliance, monitoring, and rollback review. Otherwise stay in the smallest package that covers the selected roles.

Every role manifest includes agent name, purpose, input, output, class (`FULL_AGENT`, `HITL_AGENT`, `CRON_WORKFLOW`, or `HUMAN_ONLY`), cadence, owner, provider, hard stops, data class, test, escalation path, rollback trigger, and evidence location.

## 5. Pricing calculator

### Inputs

| Input | Value |
|---|---|
| Team size | |
| Primary vertical | |
| Additional verticals | |
| Languages: ES / EN / NL | |
| Async, live, or both | |
| Human coach network | yes / no |
| EU data residency | yes / no |
| EU/LATAM compliance pack | yes / no |
| Custom methodology | yes / no |
| Dedicated private runtime | yes / no |
| Number of workers | |
| Monthly model budget | |
| Currency: PYG / USD / EUR | |

### Tier output

| Team size | Tier | Agents | Monthly anchor | Setup anchor |
|---|---:|---:|---:|---:|
| 1–5 | Micro | 4 functional | $250 / €350 / ₲1,800,000 | $250 / €350 / ₲1,800,000 |
| 5–20 | Small | 12 functional | $600 / €900 / ₲4,500,000 | $500 / €700 / ₲3,600,000 |
| 20+ | Medium | 47 total, optional agents | $2,000 / €2,800 / ₲14,400,000 | $1,000 / €1,400 / ₲7,200,000 |

These anchors come from `TOOLING-TIERS.md` §§2–4. Medium pricing scales at $80/employee/month above the 20-employee baseline, capped at +$2,000 in the source; validate the local-currency equivalent with finance before signature.

### Vertical planning anchors

| Vertical | Quick-win | S / setup ladder | M | L | Market |
|---|---|---:|---:|---:|---|
| Dental | free audit/mock sessions | ₲500K | ₲1.2M setup + ₲400K/mo | ₲2.5M setup + ₲900K/mo | Paraguay |
| Beauty/wellness | free booking-confirmation audit | ₲300K | ₲800K setup + ₲250K/mo | ₲1.5M setup + ₲500K/mo | Paraguay / LATAM |
| Legal | free triage audit | ₲2M | ₲4.5M setup + ₲1.3M/mo | ₲9M setup + ₲2.5M/mo | Paraguay |
| Real estate | free intake/SalesFlow audit | €500 | €1,200 setup + €350/mo | €2,500 setup + €800/mo | Netherlands / EU |
| E-commerce | separate scope required | $300-style anchor | $800 setup + $250/mo | $1,500 setup + $500/mo | USD / cross-border |

The e-commerce anchor is explicitly labelled a planning reference because the supplied research’s fifth vertical is fitness/education, not e-commerce. Do not promise a unique e-commerce price without a written scope.

### Coaching subscription cross-check

| Plan | Setup | Seat/month | Minimum | Typical use |
|---|---:|---:|---:|---|
| A · Coach Lite | $500 | $200 | 5 | async ES+EN, GROW, ICF-aligned |
| B · Coach Pro | $2,000 | $500 | 10 | trilingual, live calls, hybrid escalation, CBT patterns |
| C · Coach Enterprise | $10,000 | $1,500 | 50 | EU controls, custom methodology, dedicated coach, EU residency |

`monthly subscription = active seats × seat price`; add setup, approved compliance, private runtime, and human-coach fees separately. Quote in one currency. The research’s working references are approximately 7,300 PYG/USD and 0.92 EUR/USD; refresh them before quote.

**Output:** `Recommended tier:`, `Setup fee:`, `Base monthly:`, `Seats:`, `Seat price:`, `Seat monthly:`, `Compliance:`, `Runtime:`, `Human coach:`, `Model budget:`, `Contingency:`, `First invoice:`, `Renewal total:`, `Currency:`, `Rate/date:`, `Approver:`.

## 6. Onboarding timeline

### Week 1 — Safety and first useful loop

Day 1: assign owner, confirm jurisdiction, collect the intake, classify data, and stop unsafe requirements. Day 2: choose tier and roles, complete the manifest, and name system owners. Day 3: configure the canonical host, state, schedules, secrets, and rollback contacts. Day 4: load methodology, vertical, language, privacy, and hard stops. Day 5: use synthetic data and run the quick-win audit. Day 6: test approval, pause, delete, export, and escalation. Day 7: run evaluation and decide continue, reduce, or stop.

**Exit:** one useful deliverable, zero unresolved critical data risks, healthy first tick, no public release, and a named human owner.

### Month 1 — Stabilize

Train the team, run language tests, establish weekly briefs, add only approved integrations, review regulated-decision boundaries, test one agent and one state-file rollback, and record adoption, quality, latency, and human-review metrics.

**Exit:** 14 days without a critical incident, stable canonical data, working human approval, and a go/no-go decision.

### Month 3 — Prove and govern

Compare outcomes with baseline, remove low-value agents, review privacy, language, coach load, and role fit, decide whether to add a department, second vertical, live calls, or EU residency, and run a full security, privacy, eval, and rollback review.

**Exit:** accepted value evidence, no unresolved critical privacy finding, reproducible rollback, named owner for every enabled role, and signed next-quarter scope.

## 7. Customization limits

**Configurable:** brand, language, time zone, business hours, prompts, output, cadence, escalation destination, approved data sources, vertical vocabulary, goal templates, and report recipients. All changes pass privacy, trademark, eval, and human-approval gates.

**Tier-limited:** Micro is a small finance/sales/operations loop, not a full compliance, research, people, or coaching organization. Small adds marketing, research, accounting/tax, procurement, people/HR, two workers, and more evaluation, not the full matrix. Medium enables broad surfaces and optional coaching/compliance but still cannot claim licensed legal, medical, tax, employment, or performance-evaluation authority. Live human calls and a dedicated coach require Pro/Enterprise capability and the coach-network protocol. EU residency, full controls, custom methodology, and white-label infrastructure require approved scope.

**Not configurable:** turning the system into therapy or a licensed professional; silently broadening retention; sending personalized messages without review; fabricating proof; bypassing hard stops; moving regulated data to an unapproved region; or representing alignment as accreditation. “ICF-aligned” maps the design to published competencies; it is not ICF accreditation. “Compliance-ready” means implemented controls and documentation; it is not a legal opinion.

## 8. Risk disclosures

The statement of work must disclose: AI output can be wrong, incomplete, biased, mistranslated, or unsuitable; coaching can surface distress and must escalate; special-category and confidential data increase breach impact; cross-border processing creates transfer and residency risk; provider, speech, or model outages can delay sessions; language coverage is not equal across dialects and domains; automation creates false confidence; integrations, credentials, schedules, and state can drift; and pricing can change with usage, residency, tax, support, and human-coach cost. The research’s eight-month average enterprise ROI latency is not a customer guarantee.

The system is not a complete replacement for a mature internal system. The customer must accept a human fallback, pause path, limited pilot, explicit scope, and measurable outcomes.

**Risk fields:** `ID`, `description`, `likelihood`, `impact`, `mitigation`, `owner`, `acknowledgement`, `review date`, `stop trigger`.

## 9. Acceptance and sign-off

- [ ] 200-question intake reviewed by owner and technical lead.
- [ ] Data inventory and classifications approved.
- [ ] Tier and role manifest signed.
- [ ] One-currency quote has a current rate and date.
- [ ] Approval, pause, delete, export, and escalation paths tested.
- [ ] Synthetic-data tests pass before live data.
- [ ] Language tests pass for selected languages.
- [ ] Trademark scan passes for public/client artifacts.
- [ ] Rollback tested and snapshot location recorded.
- [ ] No agent makes licensed professional decisions.
- [ ] Week 1, Month 1, and Month 3 criteria accepted.
- [ ] Risks acknowledged.

Customer owner: `__________________` Date: `____________`  
Technical owner: `__________________` Date: `____________`

## 10. Source register

- `coaching-skills-gap-audit.md` §§2–5: gap analysis, tier distinction, product requirements, and intake pattern.
- `coaching-funnel-playbook.md` §§2–5: funnel, five profiles, S/M/L ladder, product SKUs, and risks.
- `coaching-strategic-implications.md` §§1–5: market context, productized SKUs, pricing, positioning, and mitigations.
- `TOOLING-TIERS.md` §§2–6: Micro/Small/Medium counts, departments, setup, monitoring, maintenance, anchors, and hard stops.
- `ORG-AGENTS.md` §§1–7: 47-agent roster, producer/consumer dependencies, escalation, cron paths, and onboarding.
- `ROLLBACK-PLAYBOOK.md` §§1–5: snapshots, atomic restore, cron disable, deployment rollback, RTO, and post-rollback verification.

Regulatory language is an operational checklist, not legal advice. Obtain qualified counsel review before EU, medical, employment, education, or cross-border deployment and record the applicable law and guidance version.

## Common pitfalls

1. Treating intake as a formality instead of evidence gathering.
2. Choosing Medium because more agents appear more valuable.
3. Enabling a role without input, output, owner, test, and rollback.
4. Letting a free quick-win become an unapproved full deployment.
5. Assuming model fluency without customer-language tests.
6. Quoting local currency without date and rate.
7. Calling the system compliant, accredited, therapeutic, or authoritative.
8. Sending external copy or personalized messages without review.
9. Adding a second vertical before the first is measurable.
10. Reporting anecdotes while ignoring failed ticks, incidents, and withdrawals.

## Verification checklist

- [ ] 15–25 KB size band.
- [ ] Every must-answer question has an owner or deferred date.
- [ ] Every enabled role has class, cadence, owner, test, and escalation.
- [ ] Tier is justified by headcount plus actual coverage.
- [ ] Pricing is complete, consistent, dated, and one-currency.
- [ ] Week 1 / Month 1 / Month 3 criteria are testable.
- [ ] Limits and risks are acknowledged.
- [ ] Claims point to the source register.
- [ ] Public/client outputs pass trademark scan.
