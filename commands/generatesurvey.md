---
description: PHASE III — Build the full ODI survey instrument (screener, profiling, importance ratings, satisfaction ratings, optional WTP) from the validated outcomes. Outputs Markdown + Qualtrics + Typeform. (Ch 15–18 + Template 4)
argument-hint: <path to netted outcomes CSV>
---

# /generatesurvey — Build the survey for your panel provider

## What this is doing (plain English)

This is the most important deliverable of the whole project. Its design determines whether your opportunity scores are real or noise.

The survey has 4–6 sections:
1. **Screener** — filters out ineligible respondents (from `/generatescreener`)
2. **Profiling** — complexity factors + demographics (from `/hypothesizecomplexity`)
3. **Importance** — every outcome rated 1–5, grouped by job step
4. **Satisfaction** — same outcomes, same order, rated 1–5
5. **Competitive satisfaction** (optional) — per named competitor
6. **WTP** (optional) — pricing band at the end

Length budget: 25–40 minutes for 75–100 outcomes. The skill warns you if it crosses 45.

## What you need before running this

- **Netted outcomes CSV** (from `/netoutcomes`)
- **Validation must have passed** — `/validateoutcomes` verdict ≠ `fail`. The skill enforces this.
- (Optional but recommended) complexity factors from `/hypothesizecomplexity` — fed into the profiling block
- (Optional) 1–4 named competitors for the competitive satisfaction block
- (Optional) decision on whether to include WTP

If any required input is missing, the skill asks before generating.

## What you'll get back

- `survey.md` (human-readable for review)
- `survey.json` (machine schema)
- `survey.qsf-import.txt` (Qualtrics Advanced Format)
- `survey.typeform.json` (Typeform import)
- `field-map.csv` (every survey item ↔ source outcome ID, for QA + analysis)
- Recommended sample size + incentive + pilot instruction

## Jargon you'll see

- **Top-2-box** — percent of respondents who picked 4 or 5 on a 5-point scale. ODI uses this (not the mean) as the scoring rule.
- **WTP (willingness to pay)** — the pricing-band block. Place at the very end of the survey; never before the importance/satisfaction blocks (which it would contaminate).
- **Skip logic** — Strategyn's rule: ask each respondent to rate satisfaction only against the ONE competitor they actually use (selected in the screener). Don't ask everyone to rate every competitor — the survey gets too long.

## What runs after this

Pilot with n=10–15 → field to n=300–600 real respondents (panel provider takes 1–3 weeks) → clean the data → `/computescores`.

---

Invoke the `generatesurvey` skill. Refuse to proceed if `/validateoutcomes` hasn't been run successfully on the netted CSV. Ask the user (interactively) for competitor names + WTP decision + audience description if not provided.
