---
name: outcometospec
description: Translate a single underserved outcome into a SUITE of ready-to-ship engineering artifacts — the 5-field spec sheet, Agile user stories, a full PRD document, a Linear/Jira-importable JSON, an ADR for technical decisions, and a success-metric dashboard query. Implements Chapter 28 (handbook) extended with team-ready formats.
when_to_use: User has a roadmap (or just a top outcome) and asks for the engineering spec, PRD, or "how do I build this". Triggered by "/outcometospec", "spec this outcome", "PRD for", "engineering brief for".
trigger_phrases:
  - /outcometospec
  - "spec this outcome"
  - "PRD for"
  - "engineering brief"
  - "acceptance criteria"
  - "how do I build this"
  - "translate this outcome into a spec"
  - "write engineering spec"
  - "what does engineering need"
  - "convert outcome to user story"
  - "what's the measurable target"
  - "how do we know we're done"
  - "ship-ready spec"
inputs:
  - the outcome statement (verbatim from netted-outcomes CSV)
  - opportunity score for the outcome
  - target segment(s) where it scores ≥10
  - current product's top-2-box satisfaction for the outcome
  - best competitor's top-2-box satisfaction for the outcome
  - product constraints (cost, mass, regulatory, manufacturing)
outputs:
  - "**5-field spec sheet** (Ch 28): outcome / solution concepts / acceptance criteria / success metric / engineering brief"
  - "**Agile user story** (As X, I want Y, so that Z) with INVEST-checked acceptance criteria"
  - "**Full PRD document** in Markdown — Background / Problem / Goals / Non-goals / Acceptance / Success metrics / Risks / Open questions / Out-of-scope / Rollout"
  - "**Linear/Jira-importable JSON** — issue title, description, story points estimate, labels, acceptance criteria as a checklist"
  - "**ADR (Architecture Decision Record)** if the outcome requires a technical choice between solution concepts"
  - "**Success-metric dashboard query** — a hypothetical analytics query that would tell you if the outcome moved post-launch"
  - "**All artifacts share the same outcome_id** so they cross-link"
chains_to: []
---

# /outcometospec — Outcome → Engineering Spec

## Plain-English preamble (for newcomers)

> A ranked list of outcomes is NOT something an engineer can build. This skill is the bridge.
>
> For ONE outcome, you produce the same 5-row artifact:
> 1. **Outcome statement** (verbatim) + opp score + target segment
> 2. **Solution concepts** (2–4 candidates)
> 3. **Acceptance criteria** — measurable, in physical/behavioral units, calibrated against the 20%-better target
> 4. **Success metric** — how you'll know post-launch you moved the outcome
> 5. **Engineering brief** — plain-language what-to-build (4–8 sentences)
>
> **The 20% rule baked in:** Strategyn's empirical switching threshold. To win share, your product must satisfy the outcome ≥20% better than the best competitor. The skill computes that number from `/competitiveanalysis` data and uses it to set the acceptance threshold.
>
> Acceptance criteria must be in **measurable units**, never adjectives. "Make it feel safer" is rejected. "<5% face-zone debris in n=10 trials" is accepted.
>
> Produce 5–12 of these per release.

---

This is the chapter most JTBD treatments skip. The translation pattern is straightforward once you've done it three times.

## The 5-field artifact (Table 28.1)

| Field | What it captures |
|---|---|
| 1. **Outcome statement** | The full outcome from the survey, with opp score + target segment(s). |
| 2. **Solution concept(s)** | One or more candidate ways to satisfy the outcome — features, components, services. Usually 2–4. |
| 3. **Acceptance criteria** | The measurable threshold that says "this outcome is now satisfied." Same units as the metric. |
| 4. **Success metric** | How you'll know post-launch whether you actually moved the outcome. Often telemetry; sometimes a follow-up survey. |
| 5. **Engineering brief** | Plain-language description of what to build. Inputs to PRD, design spec, tickets. |

## Acceptance criteria — the 20% rule (Chapter 28 + Chapter 22)

You have three numbers from your survey:

| Number | Use |
|---|---|
| Your current product's top-2-box satisfaction | **Baseline.** Start here. |
| Best competitor's top-2-box satisfaction | **Parity target.** Minimum your new product must hit. |
| Best competitor's satisfaction × ~1.2 (20% better rule) | **Aspirational target.** Empirical switching threshold. |

Translate the percentage into a physical/behavioral threshold the engineer can build against, calibrated against what the survey defined as "satisfied."

> If competitive top-2-box satisfaction on this outcome is 31%, your acceptance criterion targets 50%+ (sat) — phrased as the physical metric that produces that. E.g., "<5% of cuts produce face-zone debris" rather than "50% top-2-box on the debris outcome."

## Outcome → user story conversion (Chapter 28)

```
Outcome: <verbatim outcome statement>
Opportunity score: <opp>
Target segment: <segment label + size %>

User story:
  As a <segment role>,
  I want to <action that achieves the outcome>
  (current best-in-class: <X>),
  so that <reason rooted in the customer's workflow>.

Acceptance criteria:
  - <criterion 1: measurable>
  - <criterion 2: measurable>
  - …

Tracking:
  - <how this is measured post-launch>
```

## How to run

1. **Load the outcome row** from the netted CSV or accept verbatim.
2. **Fetch competitive satisfaction numbers** if available.
3. **Propose 2–4 solution concepts.** Often the user (or /buildroadmap) has already chosen one — that's the lead concept; the alternates are documented.
4. **Compute the acceptance threshold** using the 20% rule. Translate into a physical/behavioral unit.
5. **Define the success metric.** Default: re-run the same outcome question in a 6-month follow-up survey; secondary: instrumented telemetry that maps to the outcome.
6. **Write the engineering brief** in 4–8 sentences. Include cost, mass, manufacturability, and any dependencies on other outcomes shipping in the same release.
7. **Append the dependency block.**

## Output — one per outcome

```markdown
## Outcome → Spec: <outcome_id> — <verbatim outcome>

**Opportunity:** <opp_score> | **Target segment:** <segment label> (<size %>)

### 1. Outcome statement
> <verbatim>

### 2. Solution concepts
- (a) <concept 1> — <one-line description>. **Shipping in v1.0.**
- (b) <concept 2> — <one-line description>. Alternate, deferred to v1.1.
- (c) <concept 3> — <one-line description>. Rejected because <reason>.

### 3. Acceptance criteria
In a controlled <test scenario> (n=<n_trials>, <params>):
- <measurable criterion 1>
- <measurable criterion 2>
Baseline (current product): <X>. Best competitor: <Y>. **Target: <Z (>= 20% better than Y)>.**

### 4. Success metric
- **Primary:** Re-run the same survey outcome question 6 months post-launch. Target: top-2-box satisfaction rises from <current> → <target> on the 0–10 normalized scale.
- **Secondary:** <instrumented telemetry or warranty / support metric>.

### 5. Engineering brief
<4–8 sentence plain-language description of what to build. Include component, geometry, cost target, mass budget, manufacturability and regulatory constraints.>

### Dependencies
- Other outcomes addressed by the same component: <id list>
- Partnerships required: <list>
- Regulatory / compliance considerations: <list>
```

And the JSON:

```json
{
  "skill": "outcometospec",
  "method_version": "ODI v2.4.2",
  "outcome_id": "E-15",
  "outcome_statement": "Minimize the likelihood that debris flies up into the user's face when guiding the blade along the cut line",
  "opportunity_score": 14.5,
  "target_segment": "A — Finish-cut tradesmen (44%)",
  "spec": {
    "solution_concepts": [
      {"id": "a", "name": "Integrated dust extraction port", "shipping": "v1.0"},
      {"id": "b", "name": "Transparent forward debris shield", "shipping": "v1.0"},
      {"id": "c", "name": "Air-curtain assembly", "shipping": "rejected", "reason": "Cost"}
    ],
    "acceptance_criteria": {
      "test": "10 cuts of pine 2x6, 12-inch length, blade at 90°",
      "criteria": ["<5% of cuts result in any debris reaching the user's face zone (measurement plane 18in above and 6in forward of blade)"],
      "baseline_current_product": 0.38,
      "best_competitor": 0.31,
      "target": 0.05,
      "twenty_percent_rule_target_pct": 0.25
    },
    "success_metric": {
      "primary": "Re-run satisfaction question 6 months post-launch. Top-2-box satisfaction rises from 1.2 → 6.0+ (≈400% improvement).",
      "secondary": "Warranty claims for eye-related injuries (currently 14/year) drop to ≤2/year."
    },
    "engineering_brief": "Add a 1.5-inch debris extraction port aft of blade housing, compatible with standard 1.25-inch shop-vac hose. Add a 4mm polycarbonate forward shield, removable for blade changes, hinged on the housing. Both components must add ≤120g to the saw's total mass and must not interfere with bevel adjustment. Cost target: +$8 BOM at scale.",
    "dependencies": {
      "other_outcomes_addressed": ["E-12 (visibility through dust)"],
      "partnerships_required": [],
      "regulatory": ["UL 60745-2-5 compliance for chip-deflector geometry"]
    }
  },
  "user_story": "As a finish-cut tradesman, I want to make a cut without debris reaching my eyes (current: 38% of cuts contaminate the face zone vs. competitor 31%), so that I don't have to stop and clear safety glasses every few cuts.",
  "next_step": "Hand this to engineering; queue the post-launch survey now."
}
```

---

## The full artifact suite produced (Ch 28 + team-ready formats)

For every outcome you spec, produce ALL of the following files into a `spec-out/<outcome_id>/` folder:

```
spec-out/E-15/
├── 01-spec-sheet.md           ← the 5-field artifact (Ch 28)
├── 02-user-story.md           ← Agile-ready story + INVEST acceptance criteria
├── 03-prd.md                  ← full PRD doc, Notion/Confluence-ready
├── 04-linear-import.json      ← drop into Linear via API or paste-in
├── 05-jira-import.json        ← Jira REST API-compatible
├── 06-adr.md                  ← only if there's a meaningful tech-choice between concepts
└── 07-dashboard-query.sql     ← the query that will tell you in 6 months if you moved the outcome
```

### Template — 02-user-story.md (Agile)

```markdown
# User Story — <outcome_id> · <one-line title>

**Traces to outcome:** <outcome_id> — <verbatim outcome statement>
**Opportunity score:** <opp>
**Target segment:** <segment label> (<size %>)
**Method anchor:** ODI v2.4.2, Ch 28

---

## Story

As a **<segment role>**,
I want to **<action that achieves the outcome>** (current best-in-class: <X>),
so that **<reason rooted in the customer's workflow>**.

## Acceptance criteria (INVEST-checked)

- [ ] <criterion 1 — measurable, in physical/behavioral units>
- [ ] <criterion 2>
- [ ] <criterion 3>

Baseline: <X> · Best competitor: <Y> · Target: ≥ <20%-better number>

## Definition of Done

- [ ] Implementation merged to main
- [ ] Telemetry instrumentation in place for the success metric (see 07-dashboard-query.sql)
- [ ] Post-launch follow-up survey question registered for 6-month re-measurement
- [ ] Cross-references updated in `roadmap.csv`

## Estimate

Story points: <2 / 3 / 5 / 8 / 13>
Confidence: <low / medium / high>
```

### Template — 03-prd.md (Notion-ready PRD)

```markdown
# PRD — <outcome_id> · <short title>

**Author:** <PM name> · **Date:** <today> · **Status:** Draft
**Traces to outcome:** <outcome_id> — <verbatim statement>
**Opportunity score:** <opp> · **Segment:** <label>

## 1. Background

<2–4 sentences. Why now. What we learned from the survey.>

## 2. Problem

Customers in the **<segment label>** segment are under-served on:
> <verbatim outcome statement>

Survey data: importance <X>, current-product satisfaction <Y>, best-competitor satisfaction <Z>. Opportunity score = <opp>.

## 3. Goals

- Primary: <move outcome satisfaction from Y → target>
- Secondary: <if applicable>

## 4. Non-goals

- <what's explicitly out of scope for this release>

## 5. Solution concept(s)

| # | Concept | Status |
|---|---|---|
| (a) | <concept 1> | Shipping in this PRD |
| (b) | <concept 2> | Alternate, deferred |
| (c) | <concept 3> | Rejected — <reason> |

## 6. Acceptance criteria

In <controlled test scenario> (n=<n>, <params>):
- <criterion 1 — measurable>
- <criterion 2 — measurable>

Baseline (current product): <X>. Best competitor: <Y>. **Target: ≥ <20%-better number>.**

## 7. Success metrics (post-launch)

- **Primary:** Re-run survey outcome question 6 months post-launch. Top-2-box satisfaction Y → target on the 0–10 normalized scale.
- **Secondary:** <instrumented telemetry — see 07-dashboard-query.sql>
- **Tertiary:** <warranty / support / NPS signal>

## 8. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <risk 1> | M | H | <mitigation> |

## 9. Open questions

- <Q1 the team needs to resolve before/during build>
- <Q2>

## 10. Out-of-scope / future

<adjacent outcomes that COULD be addressed by the same component but are deferred>

## 11. Rollout

- Phase 1 (alpha): <internal/dogfood plan>
- Phase 2 (beta): <segment A users, n=50>
- Phase 3 (GA): <full rollout>

## 12. Dependencies

- Component / system: <other outcomes addressed by the same component>
- Partnerships: <if any>
- Regulatory: <if any>

## Appendix — provenance

Generated by `/outcometospec <outcome_id>` from netted-outcomes CSV row <row#>, survey opportunity score <opp>, competitive table row <row#>. Re-generate at any time.
```

### Template — 04-linear-import.json

```json
{
  "title": "<outcome_id> — <short title> · <release>",
  "description": "<short summary, includes link to 03-prd.md>\n\n**Traces to outcome:** <outcome_id> — <verbatim>\n**Opp:** <opp>\n**Target segment:** <label>\n\n**Acceptance criteria:**\n- [ ] <criterion 1>\n- [ ] <criterion 2>",
  "labels": ["odi", "<segment_label>", "<release>", "move-<n>"],
  "estimate": <story_points>,
  "priority": <0=urgent | 1=high | 2=medium | 3=low>,
  "cycleName": "<release>",
  "projectName": "<roadmap>",
  "links": [{"label": "PRD", "url": "spec-out/<outcome_id>/03-prd.md"}]
}
```

### Template — 05-jira-import.json (Jira REST API shape)

```json
{
  "fields": {
    "project": {"key": "<PROJECTKEY>"},
    "summary": "<outcome_id> — <short title>",
    "description": "<short summary + acceptance criteria>",
    "issuetype": {"name": "Story"},
    "labels": ["odi", "<segment_label>", "<release>"],
    "customfield_10016": <story_points>,
    "customfield_10000": "<epic-link if applicable>"
  }
}
```

### Template — 06-adr.md (only if there's a meaningful tech choice)

```markdown
# ADR — <outcome_id> · <decision title>

Status: Proposed · Date: <today>

## Context

<which solution concepts are being chosen between, and why>

## Decision

We will ship **<concept a>** in v1.0. <concept b> is deferred; <concept c> is rejected.

## Rationale

<3–6 sentences citing the survey data, cost constraints, and the 20%-better target>

## Consequences

- + <positive consequence>
- + <positive consequence>
- − <tradeoff>

## Alternatives considered

- <concept b> — <why deferred>
- <concept c> — <why rejected>
```

### Template — 07-dashboard-query.sql

```sql
-- Post-launch success-metric query for outcome <outcome_id>
-- Run 6 months after v1.0 ships to measure outcome movement.
-- Target: <metric> ≥ <target_threshold>

SELECT
  date_trunc('week', event_time) AS week,
  COUNT(*)                       AS attempts,
  AVG(CASE WHEN <success_condition> THEN 1.0 ELSE 0.0 END) AS success_rate,
  -- the outcome's measurable threshold from acceptance criteria:
  -- e.g., success_condition = "face_zone_debris_detected = false"
FROM <relevant_event_table>
WHERE
  segment_id = '<target_segment>'
  AND release_version >= 'v1.0'
GROUP BY 1
ORDER BY 1 DESC;
```

---

## Hard rules

- Acceptance criteria must be in measurable units, never adjectives. "Make it feel safer" is rejected. "<5% of cuts produce face-zone debris" is accepted.
- The 20% better number is computed and shown in every artifact.
- Keep the verbatim outcome statement at the top of every artifact — it is the traceability anchor.
- 5–12 of these spec suites per release is the target. More than 12 → triage the roadmap.
- ALL artifacts in `spec-out/<outcome_id>/` share the same `outcome_id` — so PR descriptions, Linear tickets, PRD, and ADR cross-link cleanly.
- ADR (06) is OPTIONAL — only produce it if there's a genuine tech decision between alternatives. If the concept is obvious, skip it.
