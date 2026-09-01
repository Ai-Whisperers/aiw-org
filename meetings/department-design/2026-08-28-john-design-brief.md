# 2026-08-28 — John design brief

| | |
|---|---|
| **Date** | 2026-08-28 |
| **Kind** | design |
| **Present** | John; Kiki (and house context). Ivan not required for this record |
| **Recording** | TurboScribe `08-28-2026 11.24` (truncated at 30 min — **not** stored here) |
| **Scribe** | Codified 2026-09-01 from transcript + this folder’s rules |
| **Status** | ratified into [`DECISIONS.md`](DECISIONS.md) DD-01–DD-07 |

## Objective

How to structure departments, roles, and Hermes agents so the company can run and later sell **focused** capability — not one general Hermes.

## What was decided (substance)

- Security key cycling is real work but **not** a blocker to start department design; later ritual / automation.
- Scan of existing repos is enough to start **product administration** (what we sell), not more coding first.
- The role most missing is **product owner / product management**, not more developers. Engineering is “fine.”
- PO defines the product, target, in/out. Sales bring wishes; PO is the decision node. Standardize; do not fork a product per client.
- Conflicting roles are healthy (pushback). Price/cost pressure belongs in sales, not as “yes” from engineering.
- Name agents like people (examples in the room: finance nickname, Selena-style sales). Easier than role titles.
- After departments/roles exist, **generate Hermes profiles from the MD files**.
- Agents should not “all talk to each other” in one soup. Message + **commit to repo**. Memory = cloneable admin; watch client-data leak across clones.
- Same shape for every department/role (templates). MD is OK until a DB is needed.
- **Tools per agent/dept**, not every skill loaded for everyone. PO does not need coding tools.
- Status questions (“what did Ivan commit?”) go to **the right agent**, not to Ivan.
- Missing questions = missing role/agent — **identify**, only build what you need now.
- A general Hermes “does too much.” Sellable unit is closer to **a department** (yearly, improvements) than a toy bot. Sales pitch: it looks easy after years of scars; buyer can learn the hard way or with you.

## What was explicitly not decided

- Exact product list and who the human PO is.
- Which community tools to install (John pointed at a mail/list; “wood” tooling — follow the list, don’t invent SKUs here).
- Pricing of department SKUs (do not invent numbers in this record).

## Topic splits

### Org / departments

Primary content of this session. See DECISIONS DD-01–DD-07.

### Engineering / Hermes

File edit in Hermes vs secrets: don’t pass passwords to the model; cycle keys later. Out of department-design except as “ops hygiene.”

## Open actions (as of 2026-09-01)

| Action | Owner | Due |
|---|---|---|
| Close DD-O1–O3 (human PO, agent shape, product list) | Ivan + Kiki | next Magic Tower / design session |
| Audit tool whitelists vs “PO has no coding tools” | Ivan | with Qualis/Safina, not a new dept |

## Follow-up

Weekly the same day scheduled a **Monday** board session to write departments/roles/agents. That board is [2026-08-magic-tower-board.md](2026-08-magic-tower-board.md).
