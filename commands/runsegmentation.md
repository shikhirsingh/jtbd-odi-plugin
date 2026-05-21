---
description: PHASE IV — Find customer segments by clustering respondents on their unmet-outcome patterns (factor analysis + k-means), then profile each segment by complexity factors. (Ch 21 + Appendix C)
argument-hint: <path to cleaned survey CSV>
---

# /runsegmentation — Find the segments

## What this is doing (plain English)

A market-wide opportunity landscape hides the fact that different groups of customers have wildly different unmet needs. Segmentation finds those groups.

ODI segments **by unmet outcomes** (not by demographics, not by use case). The math:
1. Compute every respondent's opportunity score per outcome
2. Filter to outcomes that **differentiate** (high variance across respondents)
3. Factor-analyze those into 5–15 latent factors
4. K-means cluster the respondents on those factor scores
5. Profile each cluster using your complexity-factor profiling questions

The output: 2–5 segments, each defined by which outcomes they care about and which complexity factors explain why. Each segment gets its own opportunity landscape.

## What you need before running this

- The same survey CSV passed to `/computescores`
- The netted outcomes CSV
- `profile_*` columns in the survey CSV (the complexity-factor profiling questions from `/generatesurvey`)

## What you'll get back

- `segments.csv` — every respondent's segment assignment
- `per_segment_landscape_<segment>.png` — landscape per segment
- `opportunity_scores_segment_<segment>.csv` — top outcomes per segment
- `segmentation_audit.json` — scree plot, elbow plot, chosen k, factor loadings, per-segment complexity-factor profile

The skill walks you through:
1. Confirming the differentiating subset of outcomes
2. Reviewing the scree plot and choosing n_factors
3. Reviewing the elbow plot and choosing k
4. Naming each segment by its dominant complexity factor (not by demographics)

## Jargon you'll see

- **Differentiating outcomes** — outcomes where opportunity varies a lot across respondents. Strategyn's Motorola study used only 11 of nearly 100 outcomes for clustering.
- **Factor analysis** — reduces many correlated outcomes to a smaller number of latent factors.
- **K-means** — clusters respondents on the factor scores.
- **Complexity factor** — situational variable (commute length, herd size, finish-cut frequency) that explains why a segment exists.
- **Scree plot** — chart of factor eigenvalues; helps pick how many factors to keep (default: eigenvalue > 1).
- **Elbow plot** — chart of k vs. inertia; helps pick k (default: smallest k where the marginal drop in inertia is < 15%).

## What runs after this

`/competitiveanalysis` (if competitor columns exist) → `/choosestrategy` (per-segment posture recommendation) → `/generatevalueprop` (per chosen target segment).

---

Invoke the `runsegmentation` skill. Runs `python scripts/segmentation_engine.py --survey <csv> --outcomes <netted.csv> --out-dir analysis-out/`. Walk the user through the scree + elbow choices. Name each segment by complexity factor, not demographic. Stamp SYNTHETIC if input was synthetic.
