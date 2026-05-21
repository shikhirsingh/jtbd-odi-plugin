---
description: "PHASE V — Place your data on the Jobs-to-be-Done Growth Strategy Matrix and recommend a posture (Differentiated / Dominant / Disruptive / Discrete / Sustaining) per target segment, with explicit data justification. (Ch 23–24) Alias: /growthmatrix."
argument-hint: [--segment <segment_id>]
---

# /choosestrategy — Which growth posture is your data telling you to take?

## What this is doing (plain English)

Every offering takes one of five postures, defined by two questions: (a) does it get the job done better than alternatives? (b) is it more or less expensive?

This skill reads your opportunity landscape + segments + WTP + competitive picture and tells you which posture fits — and which to avoid.

The five postures:

| Posture | Job-done quality | Price | Wins when |
|---|---|---|---|
| **Differentiated** | Better | Premium | Underserved market + high WTP |
| **Dominant** | Better | Lower | Real cost breakthrough |
| **Disruptive** | Worse | Much lower | Overserved market + non-consumers |
| **Discrete** | Worse | Higher | Captive demand — **trap. Exit.** |
| **Sustaining** | Slightly better | Slightly lower | Incumbent share-defense |

## What you need before running this

- `opportunity_scores.csv` from `/computescores`
- Segments from `/runsegmentation`
- (Strongly recommended) competitive table from `/competitiveanalysis`
- (Strongly recommended) WTP analysis from `/computescores`
- **From you (interactive)**: do you have a structural cost advantage? (Required before the skill will recommend Dominant.) This isn't optional — the skill will ask.

If you don't have WTP data, the pricing band will be omitted and the skill tells you to re-field.

## What you'll get back

- `strategy_recommendation.md` — one posture per target segment, with data justification per cell
- `growth_matrix.png` — the 5-cell matrix with your data points placed
- Pricing band (from WTP)
- Alternative postures if the recommendation isn't a clean fit
- **Discrete warning** — if any segment places into Discrete, the skill labels it a trap, NOT a celebration, and recommends exit

## What runs after this

For each chosen segment: `/generatevalueprop --segment <id>` → `/buildroadmap` → `/outcometospec` per shipping outcome.

---

Invoke the `choosestrategy` skill. ASK the user (don't assume): do you have a structural cost advantage? Required before recommending Dominant. For multi-segment engagements, recommend ONE posture per segment — not a single posture for the whole market. If WTP data is missing, omit the pricing band and tell the user explicitly.
