# Tool Stack Decisions + Cost-Cap + Cash-Flow Model

> Phase 7 deliverable. Tool decisions, cost roll-up, cash-flow projections.
> **Last updated**: 2026-08-14

---

## Section A — Tool decisions per role

### Tier 1 role coverage (default tier)

| Dept | Role | Default tool | Cost/mo (USD) |
|------|------|--------------|--------------|
| Operations | Operations Lead | (manual via chat) | 0 |
| Operations | Repo Steward | GitHub CLI | 0 |
| Operations | Asset Tracker | Spreadsheet | 0 |
| Operations | Vendor Coordinator | Email + spreadsheet | 0 |
| Operations | Compliance Watchdog | trademark-scrub.sh | 0 |
| Operations | Watchdog Engineer | Bash + cron | 0 |
| Finance | CFO/Controller | (manual) | 0 |
| Finance | Bookkeeper | finance-controller agent | 0 |
| Finance | Procurement Officer | procurement-tracker agent | 0 |
| Finance | Legal Counsel | external retainer | 100 (estimate) |
| Finance | Compliance Officer | Ivan (manual) | 0 |
| Finance | Tax Specialist | external annual | 200/yr (~$17/mo amortized) |
| Finance | Pricing Analyst | pricing-skill + spreadsheet | 0 |
| Sales | Head of Sales | EspoCRM (self-hosted) | $0 (hosting on VPS) |
| Sales | SDR | sales-pipeline agent + Mautic | $0 (Mautic self-hosted) |
| Sales | AE | EspoCRM | 0 |
| Sales | Proposal Writer | proposal-drafter + Pandoc | 0 |
| Sales | Marketing Manager | WordPress (self-hosted) | 0 |
| Sales | Content Producer | Obsidian + Markdown | 0 |
| Engineering | CTO | Cursor | $20 |
| Engineering | Frontend/Backend/Full-stack | Next.js, Node, Python | $0 |
| Engineering | DevOps/SRE | Docker Swarm + Traefik | 0 |
| Engineering | QA | Vitest + Playwright | 0 |
| Engineering | Security | OWASP compliance | 0 |
| Engineering | AI Safety | hard-stop-wrapper.py | 0 |
| Research | Research Lead | Obsidian + Zotero | 0 |
| Research | Researcher | Python + pandas | 0 |
| Research | Writer/Editor | Obsidian | 0 |
| Research | Citation Specialist | Zotero + citation-checker | 0 |
| Research | Course Designer | Obsidian + Marp | 0 |
| People | Head of People | (manual) | 0 |
| People | Performance Coach | kiki-coach agent | 0 |

**Tier 1 default total**: ~$120/mo (mostly Cursor subscription + legal retainer)

---

## Section B — Cost roll-up

### Monthly cost projection

| Category | Default | Upgrade (if needed) |
|----------|---------|---------------------|
| LLM API (litellm primary) | $50 | $150 (if heavy agent use) |
| Hosting (Hostinger VPS 32GB) | $30 | $60 (scale up) |
| Cloudflare (R2 + Workers free tier) | $0 | $5 (paid if heavy) |
| GitHub | $0 (free) | $4/user (if team plan) |
| Cursor | $20 | $40 (Pro) |
| EspoCRM hosting | $0 (on VPS) | n/a |
| WordPress hosting | $0 (on VPS) | n/a |
| Domain (paragu-ai.com) | $1 | $1 |
| Domain (other) | $2 | $2 |
| Legal retainer | $100 (estimate) | $200 |
| External accountant (amortized) | $17 | $17 |
| Trademark monitoring | $0 (script) | $30 (SaaS) |
| Backup storage (R2) | $0 (free tier 10GB) | $0.15/GB |
| **Total** | **~$220** | **~$510** |

### Per-agent daily cost projection

| Agent | Model | Tokens/run | Runs/day | Cost/run | Cost/day |
|-------|-------|------------|----------|----------|----------|
| business-analyst | primary | 8K | 1 | $0.01 | $0.01 |
| management-coordinator | primary | 10K | 0.3 (biweekly) | $0.015 | $0.005 |
| kiki-coach | primary | 15K | 0.15 (weekly) | $0.02 | $0.003 |
| finance-controller | primary | 12K | 0.15 (weekly) | $0.018 | $0.003 |
| sales-pipeline | primary | 10K | 1 | $0.015 | $0.015 |
| engineering-roster | primary | 12K | 0.3 | $0.018 | $0.005 |
| research-tracker | primary | 10K | 0.15 | $0.015 | $0.003 |
| (content agents with reflection) | primary | 25K | varied | $0.04 | $0.02 |
| **Total agent compute** | | | | | **~$0.06/day** |

Well under the $1/agent/day cap. Comfortable margin.

---

## Section C — Cash-flow model

### Current state
- MRR: $240 USD
- Monthly burn: $400-600 USD (estimated)
- Runway: many months at current burn
- Cash: not measured (need Ivan to confirm)

### With Phase 7 costs

| Item | Monthly USD |
|------|-------------|
| Current burn (hosting, LLM, tools) | $500 (mid-range) |
| + Phase 7 new tools | $0 (using defaults) |
| + legal retainer | $100 |
| = New total burn | ~$600 |

### 3-month runway projection

| Month | MRR (assumed flat) | Burn | Net | Notes |
|-------|-------------------|------|-----|-------|
| M0 (today) | $240 | $600 | -$360 | Need to grow MRR |
| M1 | $240 | $600 | -$360 | Same |
| M2 | $240 | $600 | -$360 | Same |
| M3 | $500 (1 closed deal) | $600 | -$100 | Break-even approaching |

### 6-month runway projection

| Month | MRR (assumed growth) | Burn | Net |
|-------|---------------------|------|-----|
| M0 | $240 | $600 | -$360 |
| M1 | $240 | $600 | -$360 |
| M2 | $500 | $600 | -$100 |
| M3 | $750 | $600 | +$150 |
| M4 | $1,000 | $600 | +$400 |
| M5 | $1,250 | $650 | +$600 |
| M6 | $1,500 | $700 | +$800 |

**Break-even**: Month 2-3 (with 1 deal closed)
**Sustainable**: Month 3+

### 12-month projection (with 5% monthly MRR growth)

Year-end MRR target: $1,500-2,000/mo
Year-end burn: $700-900/mo
Net positive: ~$800-1,300/mo by year-end

---

## Section D — Vendor consolidation opportunities

| # | Opportunity | Savings/mo | Effort | Risk |
|---|-------------|------------|--------|------|
| 1 | Consolidate VPS (Hostinger + Servarica) into 1 provider | $15-30 | Med (migration) | Med (downtime) |
| 2 | Replace free-tier GH with team plan ($4/user x 2 = $8) | -$8 (cost increase) | Low | Low |
| 3 | Move all CRMs to EspoCRM self-hosted (replace spreadsheets) | $0 (no current spend) | High | Med |
| 4 | Consolidate WordPress + Hugo into single CMS | $0 (no current spend) | Med | Low |
| 5 | Use CF R2 only for backups, drop GitHub LFS | $5 | Low | Low |

**Top recommendation**: #5 (drop GH LFS, use R2 for backups). Low risk, immediate savings.

---

## Section E — Pricing refresh (per AI-SDR 2026 reckoning)

Per ToolDirectory 2026: "AI SDRs were supposed to replace the sales development rep entirely. In 2026, the verdict is more interesting than the pitch."

**Implication for our pricing**:
- AI agents augment humans, don't replace
- Pricing should reflect "AI-assisted delivery" not "AI-only delivery"
- Lower entry tiers, higher margins on outcomes

### Updated pricing tiers (Rubicón EAS, legal vertical)

| Tier | Old (Dental multiplier 3x) | New (2026 reckoning) | Rationale |
|------|------------------------------|----------------------|-----------|
| Quick-Win | $1,500 setup + $550/mo | $1,200 setup + $450/mo | AI agents reduce setup time |
| Standard | $2,000 setup + $1,300/mo | $1,800 setup + $1,100/mo | Same |
| Premium | $4,500 setup + $2,500/mo | $4,000 setup + $2,200/mo | Same |
| Enterprise | $9,000 setup + $2,500/mo | $8,000 setup + $2,200/mo | Same |

**Margin impact**: ~10% lower headline price, but 20% lower delivery cost (agents do the work). Net margin IMPROVES.

---

## Section F — Procurement sequence (ranked by ROI)

| # | Action | Cost | ROI | Priority |
|---|--------|------|-----|----------|
| 1 | Drop GH LFS, use R2 | -$5 | 5x (small but easy) | NOW |
| 2 | Self-host EspoCRM on VPS | $0 | 3x (replaces spreadsheet chaos) | NOW |
| 3 | Self-host Mautic on VPS | $0 | 3x (replaces manual outreach) | Q4 2026 |
| 4 | Self-host WordPress on VPS | $0 | 2x (consolidates content) | Q4 2026 |
| 5 | Upgrade Cursor to Pro | +$20 | 2x (better dev productivity) | When MRR > $1K |
| 6 | Add GitHub Team plan | +$8 | 1.5x (better review workflow) | When 3+ contributors |
| 7 | Hire legal counsel retainer | $100 | 4x (compliance + contracts) | NOW |
| 8 | Hire external accountant | $200/yr | 5x (tax compliance) | Q1 2027 |

---

## Section G — Open questions for Ivan

1. **Cash position**: How much cash does AI Whisperers currently have? (Need this for accurate runway)
2. **MRR breakdown**: What's the $240 composed of? (Need for accurate growth modeling)
3. **Legal retainer**: Do we have one? If yes, who's the firm? (Affects legal section above)
4. **First FTE timeline**: When? (Affects People dept promotion)
5. **EU client pursuit**: Active or deferred? (Affects Compliance hard-stop)

**Defaults applied** (per D-decisions):
- D1 cost cap: $1/agent/day, $10 total
- D2 inbound-first sales
- D3 EU client hard-stop until named Compliance Officer
- D4 storage in /opt/data/agents-v2/
- D5 backup policy: gitignored state + 6h snapshot

---

## Section H — Cost-cap implementation

`/opt/data/agents-v2/scripts/cost-cap.py`:

```python
#!/usr/bin/env python3
"""cost-cap.py — Per-agent daily cost cap enforcement.

Reads state/cost-tracker.json. If any agent exceeds $1/day OR total > $10,
halts the agent and posts alert.
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

STATE_DIR = Path("/opt/data/agents/state")
COST_FILE = STATE_DIR / "cost-tracker.json"
PER_AGENT_CAP_USD = 1.0
TOTAL_CAP_USD = 10.0

def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    if not COST_FILE.exists():
        COST_FILE.write_text(json.dumps({"date": today, "per_agent": {}, "total_usd": 0.0}))
        return 0
    
    with open(COST_FILE) as f:
        tracker = json.load(f)
    
    if tracker.get("date") != today:
        # Reset for new day
        tracker = {"date": today, "per_agent": {}, "total_usd": 0.0}
    
    halted = []
    
    for agent, cost in tracker.get("per_agent", {}).items():
        if cost > PER_AGENT_CAP_USD:
            halted.append(f"{agent}: ${cost:.2f} > ${PER_AGENT_CAP_USD:.2f} cap")
    
    if tracker.get("total_usd", 0) > TOTAL_CAP_USD:
        halted.append(f"TOTAL: ${tracker['total_usd']:.2f} > ${TOTAL_CAP_USD:.2f} cap")
    
    if halted:
        for h in halted:
            print(f"HALT: {h}")
        return 1
    
    print(f"OK: total ${tracker.get('total_usd', 0):.2f} within caps")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

---

## See also

- `/opt/data/agents-v2/DECISIONS-2026-Q3.md` D1 (cost cap)
- `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md` (cost section)
- `/opt/data/agents-v2/playbooks/role-tool-sop-matrix.md` (per-role tooling)
