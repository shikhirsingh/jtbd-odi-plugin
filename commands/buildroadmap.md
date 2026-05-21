---
description: PHASE VI — Generate the outcome-attack roadmap. Pair every underserved outcome with one of the 7 product moves (borrow / accelerate / partner / acquire / new feature set / new subsystem / ultimate-solution thinking) and a release slot. (Ch 27 + Template 5)
argument-hint: [--segment <segment_id>]
---

# /buildroadmap — From scored outcomes to a release plan

## What this is doing (plain English)

You have a ranked list of underserved outcomes. This skill turns that list into a roadmap, pairing each outcome with one of seven product moves and a release version (v1.0 / v1.x / v2.0 / Northstar).

The seven moves (Ch 27):

| # | Move | Means |
|---|---|---|
| 1 | **Borrow** | Adopt a feature from an adjacent category. Often fastest. |
| 2 | **Accelerate** | Pull a feature already in your pipeline forward. |
| 3 | **Partner / license** | Another company owns the IP — access via deal. |
| 4 | **Acquire** | The capability lives in a startup. Buy it. |
| 5 | **New feature set** | Build new features in your existing platform. Most common move. |
| 6 | **New subsystem / service** | New platform component or service. |
| 7 | **Ultimate solution** | "If cost and physics didn't matter" — long-term Northstar. |

A good roadmap uses a **mix**. If 70%+ of your outcomes get assigned to "Move 5 — new feature set," you're missing faster paths.

## What you need before running this

- `opportunity_scores.csv` from `/computescores`
- Chosen target segment(s) from `/choosestrategy` (default: the highest-WTP underserved segment)
- (Optional) value prop from `/generatevalueprop` for traceability
- **From you (interactive)**: existing pipeline items, known partnership candidates, build-vs-buy preferences

The skill refuses on synthetic data.

## What you'll get back

- `roadmap.csv` (Template 5 shape): outcome / opp / segment / move # / release / mechanism
- `roadmap.md` defensible release plan
- **Coverage analysis** — % of outcomes per move. Flags if Move 5 dominates.
- A warning if any roadmap line lacks a corresponding underserved outcome (non-outcome-justified features should be explicit, not silent)

## Hard rules baked in

- Every roadmap line traces to an outcome ID with an opportunity score
- v1.0 holds ≤ 7 outcomes (finite engineering velocity)
- Table-stakes outcomes (high imp + high sat) are included with a "must satisfy at parity" note even though they're not innovation targets

## What runs after this

`/outcometospec` — per v1.0 outcome, produce the engineering spec sheet.

---

Invoke the `buildroadmap` skill. Refuse on synthetic data. Walk every outcome with opp ≥ 10 and ASK the user about pipeline / partners / build-vs-buy. If user supplies non-outcome-justified features, surface them in a separate block — don't silently accept.
