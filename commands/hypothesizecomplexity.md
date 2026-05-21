---
description: Propose 8–15 "complexity factors" — the situational variables that explain why some job-executors struggle more than others — for the survey's profiling block. (Ch 17) Alias: /complexityfactors.
argument-hint: <job statement> [--from-mined mined-outcomes.csv]
---

# /hypothesizecomplexity (aka /complexityfactors) — What drives segmentation?

## What this is doing (plain English)

Your survey will have a profiling section with ≤15 questions. Most teams fill it with demographics (age, gender, geography). **Demographics rarely drive segmentation in ODI.** What does is **complexity factors** — situational variables like:

- Daily commute length
- Frequency of finish cuts
- Herd size
- Wound severity
- Setting (hospital vs. home care)

These are the variables that explain *why* some executors struggle more than others. Segmentation works by clustering on unmet outcomes, then explaining the clusters with complexity factors.

This skill proposes the candidates — grounded in your job map, your mined data, or your interview transcripts — ranked by expected segmentation power.

## What you need before running this

- A locked job statement + (recommended) job map
- (Optional) mined-outcomes.csv from `/mineoutcomes` — gives the skill grounding evidence
- (Optional) interview transcripts already processed by `/extractoutcomes` — same purpose

Without any grounding data, the skill works from the job map alone but with lower confidence.

## What you'll get back

- 8–15 candidate complexity factors, each with:
  - **Name** + proposed survey question wording + scale
  - **Rationale** — why it might drive segmentation, grounded in the job map / mined data / interviews
  - **Expected segmentation power** (high / medium / low)
  - **Expected segment hypothesis** — what kind of segment this factor might surface
- A recommended top-8-to-12 list for the survey
- Demographics to also collect for completeness (but expect them not to drive segmentation)

## Examples by job type

| Job | Likely complexity factors |
|---|---|
| Cut wood in a straight line | Frequency of finish cuts; bevel-cut frequency; cut length; dust environment |
| Reach a destination on time | Daily destinations; route familiarity; traffic consistency |
| Listen to music on the go | Commute length; listening environment; multi-device switch frequency; offline % |
| Treat a wound | Wound type/severity; setting; patient compliance; comorbidities |

## What runs after this

Feed the top 8–12 into `/generatesurvey` as the profiling block. After fielding, `/runsegmentation` will surface which factors actually explain the clusters.

---

Invoke the `hypothesizecomplexity` skill. Every candidate must be grounded in either the job map, a mined quote, an interview, or a known industry dimension. Refuse pure speculation. Rank by expected segmentation power.
