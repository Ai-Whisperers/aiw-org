# Schema: Source + SourceCatalog

> DEMIURGE-006

## Source

Literature or community content grounding a department or role.

```yaml
Source:
  id: string                # kebab-case slug
  title: string
  url: string
  type: enum                # book | paper | blog | community | framework | standard | podcast
  quality_rating: int       # 1-5
  quality_rationale: string # why this score
  departments: string[]     # dept ids informed
  roles: string[]           # role ids informed
  last_scanned: iso8601
  scan_frequency: duration
  key_insights: string[]    # extracted best practices
  tags: string[]
  language: string          # en | es | nl | multi
```

## Quality rating criteria (1–5)

| Score | Criteria |
|-------|----------|
| 5 | Authoritative, recent (<3y), evidence-based, directly applicable |
| 4 | Strong authority, minor gaps in recency or applicability |
| 3 | Useful practitioner content, mixed evidence |
| 2 | Anecdotal or outdated; use with caution |
| 1 | Unverified; do not ground roles on this alone |

### Scoring dimensions

Each source is scored on four dimensions (1–5 each); `quality_rating` = rounded average:

1. **Authority** — author/org reputation, peer review
2. **Recency** — published or updated within relevant window
3. **Applicability** — fits AI-native / SMB / our ICP context
4. **Evidence base** — data, case studies, reproducible methods

## SourceCatalog

Per-department collection of sources.

```yaml
SourceCatalog:
  id: string                # e.g. catalog-marketing
  department_id: string
  version: semver
  sources: string[]         # Source ids
  gap_notes: string[]       # what's missing vs literature
  last_gap_analysis: iso8601
  maintained_by: string     # agent id (literature scanner)
```

## Scanner outputs

Literature scanner and community scanner agents write to:

- `sources/<dept>/catalog.yaml`
- `sources/<dept>/gaps.md`
- `sources/<dept>/community-signals.md`

## Community source types

| type | Examples |
|------|----------|
| community | Reddit r/marketing, HN, Indie Hackers |
| blog | Lenny's Newsletter, Reforge, HubSpot blog |
| framework | Jobs-to-be-Done, GROW, SPIN Selling |
| standard | ITIL, DORA, ISO where relevant |

## Validation checklist

- [ ] Every active role has ≥1 source_basis with rating ≥3
- [ ] Catalog gap analysis run quarterly minimum
- [ ] URLs reachable (scanner logs failures)
- [ ] No credentials in source metadata
