---
name: runsegmentation
description: Run outcome-based segmentation — factor analysis + k-means clustering on per-respondent opportunity scores — and profile each segment with complexity factors. Produces per-segment opportunity landscapes. Implements Chapter 21 + Appendix C.
when_to_use: User has a cleaned survey CSV (real or synthetic) and asks to find segments, run clusters, or profile the customer base. Triggered by "/runsegmentation", "segment the data", "cluster the respondents", "find the segments".
trigger_phrases:
  - /runsegmentation
  - "segment the respondents"
  - "cluster the data"
  - "find segments"
  - "per-segment landscape"
  - "find my beachhead"
  - "find the beachhead segment"
  - "who's my best customer"
  - "split the respondents"
  - "are there different customer groups"
  - "find the customer groups"
  - "identify customer types in my data"
  - "k-means"
  - "factor analysis"
inputs:
  - same survey CSV passed to /computescores
  - the netted outcomes CSV (for labels)
  - the list of profiling/complexity-factor column names (auto-detected from columns prefixed `profile_`)
outputs:
  - segments.csv — respondent_id → segment_id
  - per_segment_scores.csv — opportunity scores per outcome per segment
  - per_segment_landscape_<segment>.png — one landscape per segment
  - segment_profiles.md — what each segment is (size %, defining complexity factors, top 5 opportunities, strategic posture)
  - segmentation_audit.json — k tested, scree plot, elbow plot, chosen k, factor loadings
chains_to:
  - /generatevalueprop (per chosen target segment)
  - /buildroadmap (segment-aware)
helpers:
  - scripts/segmentation_engine.py (Appendix C + Ch 21 implementation: factor analysis + k-means + per-segment landscapes + complexity-factor profiling)
---

# /runsegmentation — Outcome-Based Segmentation

## Plain-English preamble (for newcomers)

> A single market-wide opportunity landscape hides the fact that different customer groups have **different unmet needs**. This skill finds those groups by clustering respondents on their unmet-outcome patterns (factor analysis → k-means), then explaining each cluster using your complexity-factor profiling questions.
>
> **Why ODI segments differently than other research:** demographic, firmographic, and psychographic segmentation rarely predict unmet-need differences. ODI segments by the unmet outcomes themselves — by *what people care about and what they're not getting*. Then complexity factors (situational variables like "how often do you make finish cuts") explain *why* the clusters exist.
>
> **What you get:** 2–5 segments, each with a name (based on complexity factor, not demographic), a size %, its own opportunity landscape, and its top underserved outcomes.

---

A market-wide opportunity landscape hides the fact that different groups of customers have different unmet needs. Outcome-based segmentation finds those groups by clustering respondents on their **opportunity-score patterns**, then profiling each cluster with **complexity factors** to explain why it exists.

> **Why traditional segmentation fails for innovation.** Demographics, firmographics, and psychographics don't reliably predict differences in unmet needs. A 28-year-old man in Montana and a 55-year-old woman in Florida frequently turn out to have identical unmet outcomes. The basis for innovation segmentation is the unmet outcomes themselves.

## The 4 characteristics of a good segmentation scheme (Table 21.1)

| Characteristic | What it means | What fails it |
|---|---|---|
| **Homogeneous** | Inside a segment, everyone agrees on which outcomes are under/over/appropriately served. | Demographic, "use-case", persona-based. |
| **Mutually exclusive** | Each segment's unmet-need pattern differs from every other's. | Use-case segments. |
| **Collectively exhaustive** | 100% of the population is classified. | Buyer-only segments. |
| **Actionable** | Each segment maps to a clear posture (Differentiated, Dominant, Disruptive, Sustaining). | "Fuzzy" narrative segments. |

Outcome-based segmentation satisfies all four by construction.

## The 5-step procedure (Chapter 21)

1. **Compute opportunity scores per respondent.** For each respondent, for each outcome, per-respondent top-2-box: 1 if rated 4 or 5, else 0, × 10. Then Opp = Imp + max(Imp − Sat, 0) per respondent per outcome.
2. **Choose segmentation criteria — keep only outcomes that DIFFERENTIATE.** Filter to outcomes where opportunity varies meaningfully across respondents. Outcomes everyone agrees are important (or everyone says are well-satisfied) cannot explain differences. Motorola used 11 of nearly 100 outcomes for clustering on this basis.
3. **Run factor analysis** on the differentiating subset. Reduce to a smaller number of latent factors (typically 5–15). Use the scree plot to pick the number of factors.
4. **Run k-means clustering** on the factor scores. Try k = 2 through 6. Pick k that yields both *statistical separation* (elbow) and *strategic interpretability* (the story holds).
5. **Profile each segment using complexity factors** (Chapter 17). The 1–3 complexity factors that explain why each segment exists are what you'll use to target it.

## Practical requirements

- **Sizable** — typically >10–15% of the market.
- **Reachable** — identifiable via some channel.
- **Explainable** — describable via 1–3 complexity factors, not a list of 30 outcomes.

## How to run

1. **Load survey CSV and netted outcomes CSV.** Apply quality filters.
2. **Call `scripts/segmentation_engine.py`** to build the per-respondent opportunity matrix and run the full Appendix C pipeline.
3. **Filter to differentiating outcomes.** Default: keep outcomes whose opportunity-score variance across respondents is in the top 50%. The user can override the threshold.
4. **Factor analysis.** Scree plot. Default: keep factors with eigenvalue > 1, or top n explaining 70%+ variance.
5. **K-means for k = 2..6.** Elbow plot. Default: pick the smallest k where increasing k reduces inertia by <15%. Show all candidates and let the human confirm.
6. **For chosen k, compute:** segment sizes, top opportunities per segment, complexity-factor profile per segment (one-way means/distributions of every profiling column by segment).
7. **For each segment, produce a per-segment opportunity landscape.**
8. **Emit:** segments.csv, per_segment_scores.csv, per_segment_landscape_*.png, segment_profiles.md, segmentation_audit.json.

## Output format

```json
{
  "skill": "runsegmentation",
  "method_version": "ODI v2.4.2",
  "job_statement": "...",
  "sample": {"respondents_used": 567},
  "differentiating_outcomes_used": 23,
  "factor_analysis": {
    "n_factors": 7,
    "variance_explained": 0.74,
    "scree_plot": "analysis-out/scree.png",
    "loadings_csv": "analysis-out/factor_loadings.csv"
  },
  "clustering": {
    "k_tested": [2,3,4,5,6],
    "elbow_plot": "analysis-out/elbow.png",
    "k_chosen": 3,
    "reason_for_k": "Drop from k=3 to k=4 reduces inertia by 11% — below the 15% threshold. k=3 yields three interpretable segments each >18% of sample."
  },
  "segments": [
    {
      "segment_id": "A",
      "label": "Finish-cut tradesmen",
      "size_pct": 0.44,
      "size_n": 250,
      "defining_complexity_factors": [
        {"factor": "finish_cut_frequency",   "segment_mean": 4.6, "overall_mean": 2.3, "delta": "+2.3 standard deviations"},
        {"factor": "bevel_cut_frequency",    "segment_mean": 3.9, "overall_mean": 1.8, "delta": "+2.1 sd"}
      ],
      "top_opportunities": [
        {"id": "P-05", "statement": "Minimize the time to set the angle of the blade", "importance": 9.1, "satisfaction": 3.6, "opportunity": 14.6},
        {"id": "E-12", "statement": "Minimize the likelihood of moving off the cut line", "importance": 9.0, "satisfaction": 3.8, "opportunity": 14.2}
      ],
      "strategic_posture": "Differentiated — clearly underserved, high WTP signal in profiling",
      "landscape_png": "analysis-out/landscape_segment_A.png"
    },
    {
      "segment_id": "B",
      "label": "Quick-cut framers",
      "size_pct": 0.32,
      "size_n": 181,
      "defining_complexity_factors": [
        {"factor": "framing_cuts_per_week", "segment_mean": 120, "overall_mean": 48, "delta": "+1.7 sd"}
      ],
      "top_opportunities": [...],
      "strategic_posture": "Overserved on precision features — Disruptive (cheaper, simpler) candidate"
    },
    {
      "segment_id": "C",
      "label": "Occasional DIYers",
      "size_pct": 0.24,
      "size_n": 136,
      "strategic_posture": "Mostly table-stakes — Sustaining"
    }
  ],
  "next_step": "Run /generatevalueprop --segment A. Or /buildroadmap to plan moves segment-by-segment."
}
```

## Worked example — Motorola radios (Chapter 21, Table 21.2)

Three previously-invisible segments emerged from outcome-based clustering of Motorola's radio market, each defined by a distinct cluster of unmet outcomes and *not* by industry (the old segmentation):

| Segment | % | Uniquely values | Who they are |
|---|---|---|---|
| Privacy | 40% | Discreet comms, record of comms, no intercepts | Federal/state police, security, covert ops |
| Emergency | 28% | Clear messages, few interruptions, glove-operable | Firefighters, life-threatening situations |
| Administrative | 32% | Few unimportant calls, quick confirmation, easy programming | Coast guard, locomotive engineers |

Motorola then shipped a shared platform (universally-valued outcomes) + segment-specific feature sets. 18% revenue growth in a stagnant market.

## Hard rules

- Don't segment with all outcomes — only the differentiating subset.
- Don't pick k from the elbow alone. Pick k that yields *both* statistical separation *and* a coherent story.
- Don't call a segment "actionable" unless it's reachable AND explainable in 1–3 complexity factors.
- Don't profile a segment using demographics if a complexity factor is available. Demographics are confirmatory, not explanatory.
- If the survey is synthetic, surface the SYNTHETIC banner on every output.
