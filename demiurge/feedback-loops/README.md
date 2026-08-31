# Feedback loop definitions

> DEMIURGE-050, DEMIURGE-051

## loop-pipeline-to-content

```yaml
id: loop-pipeline-to-content
trigger:
  type: signal
  condition: sales-pipeline-feedback received
action:
  type: update_source_catalog
  target: sources/marketing/catalog.yaml
output: Revised content priorities in Hera brief
owner_agent: hera-marketing-lead
```

## loop-pd-to-mkt

```yaml
id: loop-pd-to-mkt
trigger:
  type: signal
  condition: product-discovery-insight quorum_met
action:
  type: adjust_cadence
  target: calliope-content-producer
owner_agent: hera-marketing-lead
```

## loop-monitor-to-source

```yaml
id: loop-monitor-to-source
trigger:
  type: kpi_threshold
  condition: kpi-mkt-engagement < 0.15 OR kpi-pd-interviews < 2
action:
  type: update_source_catalog
  target: sources/*/gaps.md
owner_agent: thoth-literature-scanner
frequency: P1W
```

## loop-monitor-to-soul

```yaml
id: loop-monitor-to-soul
trigger:
  type: kpi_threshold
  condition: kpi-org-health-score < 0.7
action:
  type: revise_soul
  target: demiurge/agents/*/PROMPT.md
output: prompt-improvement-suggester draft for Ivan approval
owner_agent: argus-health-monitor
```

See [soul-improvement.yaml](soul-improvement.yaml).
