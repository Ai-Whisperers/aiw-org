# BURNOUT-SIGNAL-SPEC.md

> Specification for `founder-bandwidth-watchdog` agent (Tier 2, People & Culture).
> **Last updated**: 2026-08-14

---

## Purpose

Detect early signs of founder burnout and trigger Ivan check-in before crisis.

## What it monitors

### Signal 1 — Hours-worked (calendar density)
- **Source**: Buscador principal Calendar API (Ivan's primary calendar)
- **Metric**: Hours of scheduled events per week, per founder
- **Threshold**: 70+ hours/week sustained 3 weeks → ALERT

### Signal 2 — Chat sentiment (informal)
- **Source**: Recent chat messages (Telegram, WhatsApp bridge)
- **Metric**: Keyword scan for burnout indicators
- **Indicators**:
  - "burned out", "exhausted", "can't do this", "too much"
  - Negative sentiment shift (manual review)
  - Frequency of late-night messages (post 23:00 PYT)

### Signal 3 — Deadline clustering
- **Source**: Agent brief reports, git commit patterns
- **Metric**: Number of overlapping high-priority items in 7-day window
- **Threshold**: 5+ P0/P1 items in one week → ALERT

### Signal 4 — Decision latency
- **Source**: Time between Ivan prompt and Ivan response
- **Metric**: Average response time (excluding sleep hours 23:00-07:00 PYT)
- **Threshold**: > 4 hours avg for 3 consecutive days → ALERT

---

## Thresholds (configurable)

```yaml
burnout_signals:
  hours:
    weekly_threshold: 70
    sustained_weeks: 3
    sample_window_days: 7

  sentiment:
    keyword_threshold: 2  # 2+ keywords in 1 week
    sentiment_window_days: 14

  deadlines:
    weekly_threshold: 5
    priority_filter: [P0, P1]

  response_latency:
    avg_threshold_hours: 4
    sustained_days: 3
    exclude_hours: [23, 24, 0, 1, 2, 3, 4, 5, 6]  # sleep hours
```

---

## Trigger logic

```python
def check_burnout(founder: str, signals: dict) -> dict:
    alerts = []

    # Signal 1: Hours
    if signals["hours"]["weekly_avg"] >= 70:
        if signals["hours"]["sustained_weeks"] >= 3:
            alerts.append({
                "signal": "hours",
                "severity": "high",
                "message": f"{founder}: {signals['hours']['weekly_avg']} hrs/week sustained {signals['hours']['sustained_weeks']} weeks"
            })

    # Signal 2: Sentiment (keyword scan)
    if signals["sentiment"]["keyword_count"] >= 2:
        alerts.append({
            "signal": "sentiment",
            "severity": "medium",
            "message": f"{founder}: burnout keywords detected {signals['sentiment']['keyword_count']}x in last 14d"
        })

    # Signal 3: Deadlines
    if signals["deadlines"]["weekly_count"] >= 5:
        alerts.append({
            "signal": "deadlines",
            "severity": "medium",
            "message": f"{founder}: {signals['deadlines']['weekly_count']} P0/P1 items this week"
        })

    # Signal 4: Response latency
    if signals["response_latency"]["avg_hours"] >= 4:
        if signals["response_latency"]["sustained_days"] >= 3:
            alerts.append({
                "signal": "response_latency",
                "severity": "high",
                "message": f"{founder}: avg response {signals['response_latency']['avg_hours']} hrs sustained {signals['response_latency']['sustained_days']} days"
            })

    return {
        "founder": founder,
        "alerts": alerts,
        "needs_checkin": any(a["severity"] == "high" for a in alerts),
        "needs_pause": sum(1 for a in alerts if a["severity"] == "high") >= 2,
    }
```

---

## Actions

| Severity | Action |
|----------|--------|
| **medium** | Log to `state/people.json` `founder_bandwidth_audit`, surface in next kiki-coach brief |
| **high** (1 signal) | Page Ivan via Telegram, suggest PTO check-in |
| **high** (2+ signals) | Page Ivan + Kiki, suggest immediate workload reduction |
| **critical** (sustained 4+ weeks) | Emergency brief to board, propose interim measures |

---

## Cadence

- Weekly: agent runs (Sunday 18:00 PYT)
- Monitors: hours-worked (continuous via cron), sentiment (weekly scan), deadlines (from brief inputs), latency (rolling 7d)

---

## Privacy

- **No content scan**: keyword scan only, not full message analysis
- **Local-only**: sentiment scan runs on local files, no external API
- **Opt-in**: founders explicitly agree to monitoring
- **Audit trail**: every check logged in `state/people.json` `burnout_checks` table

---

## Limitations

- Calendar API requires Buscador principal OAuth setup (deferred until agent build)
- Chat sentiment requires bridge access to Telegram/WhatsApp history
- Latency signal requires foundation model context (more complex)
- False positives possible (high workload ≠ burnout; one-off vs sustained)

---

## Future enhancements

- [ ] ML-based sentiment scoring (replace keyword scan)
- [ ] Cross-reference with health app data (steps, sleep) — opt-in
- [ ] Historical baseline (compare current week to 90-day average)
- [ ] Team-level signal (if we hire)

---

## Cross-references

- `/opt/data/agents/departments/06-people-culture.md` (v0.2.0)
- `/opt/data/agents-v2/playbooks/06-people-culture.md`
- `/opt/data/agents-v2/DECISIONS-2026-Q3.md` (no PII scan rule)
