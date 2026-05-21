---
description: PHASE VII — Convert ONE underserved outcome into a SUITE of ship-ready artifacts — the 5-field engineering spec, Agile user story with INVEST acceptance criteria, full PRD doc, Linear/Jira-importable JSON, optional ADR, and a success-metric SQL query. Everything traces to the same outcome ID. (Ch 28 + team-ready formats)
argument-hint: <verbatim outcome statement OR outcome_id>
---

# /outcometospec — One outcome → 7 ship-ready artifacts

## What this is doing (plain English)

A ranked outcome list isn't something an engineering team can build. This skill is the bridge — and it doesn't just produce a single spec sheet anymore. For ONE outcome, it generates **a whole folder of artifacts** ready to drop into your tools:

```
spec-out/<outcome_id>/
├── 01-spec-sheet.md         ← the 5-field Ch 28 artifact
├── 02-user-story.md         ← Agile story + INVEST acceptance criteria
├── 03-prd.md                ← full PRD, Notion/Confluence-ready
├── 04-linear-import.json    ← drops into Linear via API or paste
├── 05-jira-import.json      ← Jira REST API-compatible
├── 06-adr.md                ← Architecture Decision Record (only if there's a real tech choice)
└── 07-dashboard-query.sql   ← post-launch telemetry query for the success metric
```

All artifacts share the same `outcome_id` so PR descriptions, Linear tickets, Notion PRDs, and dashboards cross-link cleanly.

## What you need before running this

- The outcome statement (verbatim from the netted CSV) OR an outcome ID
- The outcome's opportunity score, importance, and satisfaction (auto-pulled from `/computescores`)
- Best competitor's satisfaction (auto-pulled from `/competitiveanalysis` if it exists)
- **From you (interactive)**: product constraints — cost, mass, regulatory, manufacturing — and your project/issue tracker keys (Linear project name, Jira PROJECTKEY) for the import-ready outputs

The skill refuses on synthetic data.

## What you'll get back

Seven files (six if no real tech choice between solution concepts) in `spec-out/<outcome_id>/`. Plus a single JSON summary that lists each artifact and its path.

The acceptance criteria in EVERY artifact include the 20%-better number, computed automatically from best-competitor satisfaction × 1.2 (capped at 10).

## What runs after this

Run this once per outcome shipping in v1.0 (typically 5–12 outcomes). Then `/createodicanvas` for the one-pager and `/exportdeliverables` for the bundle.

---

Invoke the `outcometospec` skill. Refuse on synthetic data. ASK the user for product constraints + their Linear/Jira project keys before generating import-ready files. Compute the 20%-better number explicitly. Produce ALL seven (or six) artifacts into `spec-out/<outcome_id>/` — never just the spec sheet.
