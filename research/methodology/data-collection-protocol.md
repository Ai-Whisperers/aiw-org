# Data Collection Protocol

> **Built 2026-09-01** — Phase 7 R6 (methodology docs).
>
> **Purpose**: Standardize how Research dept collects data. Ensures
> reproducibility, ethics compliance, and data quality across thesis chapters,
> course research, and citation tracking.

---

## 4-Phase Protocol

### Phase 1 — Planning (before collection)

| Item | Required |
|---|---|
| Research question (PICO-S) | ✅ |
| Data sources identified | ✅ |
| Collection method documented | ✅ |
| Sample size justified (power analysis) | ✅ |
| IRB / ethics approval (if human subjects) | ✅ |
| Consent process (if personal data) | ✅ |
| Data storage plan (where, encryption, retention) | ✅ |
| Privacy review (PII, GDPR/LGPD if applicable) | ✅ (LGPD LATAM-only) |

**Output**: Data collection plan (1-2 pages)

### Phase 2 — Collection

#### Sources

**Primary** (collected by us):
- Surveys
- Interviews
- Experiments
- Field observations
- Code repositories

**Secondary** (already exists):
- Public datasets
- APIs
- Published papers

#### Methods

| Method | Best for | Sample size | Time |
|---|---|---|---|
| Survey | Attitudes, prevalence | 30-200 | 2-4 weeks |
| Interview | Depth, motivation | 5-20 | 1-3 weeks |
| Experiment | Causality | 20-100 per condition | 4-12 weeks |
| Field observation | Context, behavior | 5-20 sites | 4-8 weeks |
| Code analysis | Patterns, practices | 10-50 repos | 2-6 weeks |

#### Quality controls

- Pilot test before full rollout
- Inter-rater reliability (kappa > 0.7 for qualitative coding)
- Test-retest reliability for surveys (r > 0.7)
- Document all deviations from plan

### Phase 3 — Storage & security

#### File naming convention

```
data/
├── raw/                  # immutable raw data, read-only
│   ├── YYYY-MM-DD-{source}-{id}.csv
│   └── README.md          # collection metadata
├── processed/            # cleaned, derived data
│   └── YYYY-MM-DD-{source}-{transform}.csv
├── analysis/             # results, figures
└── metadata/             # schemas, codebooks
    ├── schema.yaml
    ├── codebook.md
    └── ethics-approval.pdf
```

#### Security

| Class | Encryption | Access | Retention |
|---|---|---|---|
| Public | None | All | Indefinite |
| Internal | At-rest | Research team | 5 years |
| Confidential (PII) | At-rest + in-transit | Named only | 3 years + anonymize |
| Sensitive (health/financial) | Strong encryption | Ivan only | Per ethics approval |

#### LGPD (Brazil) / LATAM-only compliance

- AIW is LATAM-focused, NOT first-world
- Skip GDPR requirements unless explicitly required by client
- LGPD (Brazil): required for Brazilian data subjects
- Paraguay: lighter framework, follow internal policies
- **DO NOT** build GDPR-Article-30-style consent pipelines unless a client requires it

### Phase 4 — Analysis & sharing

#### Analysis

- Pre-register hypotheses if confirmatory
- Use version control for analysis code
- Document transformations (data lineage)
- Report effect sizes, not just p-values
- Acknowledge limitations

#### Sharing

- Anonymize before sharing outside team
- Use standard formats (CSV, JSON, Parquet)
- Include README with column descriptions
- Choose license (CC-BY-4.0 for open data preferred)

---

## Output template

Every data collection produces:

```markdown
# Data Collection: [TOPIC]

**Date**: YYYY-MM-DD
**Collector**: [name]
**Research question**: [PICO-S]

## Method

[Method description, sample size, dates]

## Ethics

- IRB approval #: [number]
- Consent process: [description]
- Data sovereignty: [PAR/LATAM/EU]

## Storage

- Path: data/raw/YYYY-MM-DD-{topic}/
- Encryption: [yes/no]
- Access: [who]

## Quality controls

- Pilot: [yes/no, n=X]
- Inter-rater: [kappa]
- Test-ret: [r]

## Issues encountered

- [issue 1]

## Files

- [file 1]: [description]
```

---

## Tools

- **Agent**: `research-associate` (when activated)
- **Scripts**: `data-collection-protocol.md`, `data-anonymization.py`
- **Storage**: `/opt/data/work/research-repos/{thesis-name}/data/`

---

## AIW-specific (GeoData v2)

- **Data sources**: Public Paraguay geospatial datasets + surveys
- **LGPD compliance**: Not required (Paraguay data, not Brazilian)
- **Consent**: Survey-based, online consent form
- **Retention**: 5 years post-defense

---

## Version history

- v0.1.0 (2026-09-01): Initial protocol

**Owner**: research-engineer
**Review cadence**: per-project
**Last reviewed**: 2026-09-01

---

## Sources & Standards

This protocol draws on:

- **PRISMA 2020 Statement** (Page et al., BMJ 2021;372:n71) — systematic-review reporting standard. <https://www.bmj.com/content/372/bmj.n71>
- **Cochrane Handbook for Systematic Reviews of Interventions** (Higgins et al., 2023, ch. 5: planning data collection). <https://training.cochrane.org/handbook>
- **FAIR Guiding Principles** (Wilkinson et al., Sci Data 2016;3:160018) — Findable, Accessible, Interoperable, Reusable. <https://doi.org/10.1038/sdata.2016.18>
- **OECD Frascati Manual 2015** — standard definitions for R&D inputs/outputs. <https://doi.org/10.1787/9789264239012-en>