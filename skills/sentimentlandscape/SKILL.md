---
name: sentimentlandscape
description: Generate a directional "hypothesis opportunity landscape" from public online sentiment — before any real survey has been fielded. Maps mined posts onto candidate outcomes and infers approximate importance/satisfaction proxies. SYNTHETIC — never replaces /computescores on real data.
when_to_use: User wants a fast pre-survey gut-check on which outcomes will likely score as opportunities, to inform interview prioritization and survey-instrument design. Triggered by "/sentimentlandscape", "hypothesis landscape", "what will score high", "pre-survey landscape".
trigger_phrases:
  - /sentimentlandscape
  - "hypothesis landscape"
  - "pre-survey landscape"
  - "what will score high"
inputs:
  - mined-outcomes.csv (from /mineoutcomes)
  - source-evidence.md
  - the netted outcomes CSV (if available)
outputs:
  - hypothesis_landscape.csv — per outcome: directional importance proxy, satisfaction proxy, gap, and a "likely classification" label
  - hypothesis_landscape.png — same scatter shape as the real landscape but visibly marked SYNTHETIC
  - hypothesis_landscape.md — what this implies for the survey design and interview priorities
chains_to:
  - /generatesurvey (use the hypothesis landscape to choose which complexity factors to test)
  - /run-synthetic-survey (full pipeline; this skill is a lighter-weight variant)
---

# /sentimentlandscape — Pre-Survey Hypothesis Landscape

## Plain-English preamble (for newcomers)

> Mining + sentiment analysis on public data → a *hypothesis* version of the Opportunity Landscape, before you've fielded a real survey.
>
> Per candidate outcome, the skill computes:
> - **Proxy importance** from frequency + engagement + urgency language + cross-source agreement
> - **Proxy satisfaction** from sentiment + workaround complexity + switching language
> - **Hypothesis opportunity** using the real formula
> - **Confidence** score 0–1 (≥0.7 trust; 0.4–0.7 hint; <0.4 don't trust)
>
> Used to decide which interviews to commission first and to stress-test your draft outcome list. **Cannot replace** `/computescores` on real data — refuses to chain to decision-grade downstream skills.

---

> ⚠️ **SYNTHETIC — DIRECTIONAL ONLY — DO NOT SHIP.** This produces a *hypothesis* about what the real opportunity landscape will look like, derived from public sentiment, not from a fielded survey. Its purpose is to prioritize where to invest interview time and to pressure-test the netted outcome list before the survey is built.

Use this when:
- You've mined data and want a quick view of which outcomes look most underserved.
- You want to decide which 3 outcomes are likely top-priority before committing $30k to a panel.
- You need a board-ready "we have data" view before the survey returns.

Never use this:
- To justify a roadmap.
- To set pricing.
- To replace the survey.

## Method — how to fake a landscape responsibly

For each candidate outcome you produce two proxy scores:

### Importance proxy (0–10)

A blend of:

1. **Frequency** — how often does the underlying pain show up across mined posts (normalized)?
2. **Engagement signal** — upvotes/likes/replies on posts that contain this pain (normalized)?
3. **Urgency language** — fraction of posts using high-urgency words ("can't believe…", "deal-breaker", "every single time", "always…", swear words).
4. **Cross-source agreement** — does the pain show up across 2+ sources (Reddit + Amazon + Twitter)?

Each component scored 0–1; importance_proxy = mean × 10.

### Satisfaction proxy (0–10)

A blend of:

1. **Sentiment in posts mentioning the outcome** (neutral/positive / negative on a 0–1 scale).
2. **Workaround presence** — are people describing complicated workarounds (low satisfaction) or have settled solutions (high)?
3. **Switching language** — "switched from", "moved to", "gave up on" implies dissatisfaction.

satisfaction_proxy = blended × 10.

### Hypothesized opportunity

`Opp_hypothesis = importance_proxy + max(importance_proxy - satisfaction_proxy, 0)`

Classify into the same five tiers (extreme / low-hanging fruit / worth considering / appropriately served / overserved).

## Reliability check

For each outcome, compute a *confidence score* in [0, 1]:

- ≥ 0.7 → high confidence the real survey will produce a similar verdict
- 0.4–0.7 → medium; treat as a hint
- < 0.4 → low; do not rely on this classification at all

Factors that lower confidence:
- Fewer than 5 mined quotes touching the outcome
- All quotes from a single source
- High variance in sentiment within the supporting quotes
- Outcome wording the mining couldn't anchor to specific posts

## Output

`hypothesis_landscape.csv`:

```csv
outcome_id,outcome_statement,importance_proxy,satisfaction_proxy,opp_hypothesis,classification_hypothesis,confidence,n_supporting_quotes,sources
E-12,Minimize the likelihood of moving off the cut line,8.6,3.4,13.8,low_hanging_fruit_HYPOTHESIS,0.78,42,"reddit,amazon-reviews,trustpilot"
```

`hypothesis_landscape.md` — a written summary including:

- Top 5 hypothesized opportunities (sorted by opp_hypothesis × confidence)
- Outcomes the public data is silent on (low n; survey is the only way to find out)
- Outcomes that look overserved per the public data — disruption hypotheses
- Recommended adjustments to the netted outcome list (add, drop, refine)
- Recommended adjustments to the interview screener and questions (which complexity factors to probe in real interviews)

JSON:

```json
{
  "skill": "sentimentlandscape",
  "method_version": "ODI v2.4.2",
  "data_provenance": "SYNTHETIC — directional only, do not ship",
  "job_statement": "...",
  "input_outcomes": 96,
  "supported_outcomes": 71,
  "unsupported_outcomes": 25,
  "summary": {
    "high_confidence_low_hanging_fruit": [
      {"id": "E-12", "outcome": "...", "opp_h": 13.8, "confidence": 0.78}
    ],
    "high_confidence_extreme": [],
    "high_confidence_overserved": [
      {"id": "M-04", "outcome": "Minimize the time to manually skip ads between songs", "imp_h": 5.2, "sat_h": 7.8, "confidence": 0.71, "note": "Posts indicate most users have settled on premium subscriptions; market is overserved on workaround pain."}
    ],
    "needs_survey_to_resolve": ["E-22", "P-07", "D-09"]
  },
  "outputs": {
    "csv": "hypothesis_landscape.csv",
    "png": "hypothesis_landscape.png",
    "md":  "hypothesis_landscape.md"
  },
  "guardrail_check": {
    "synthetic_banner_applied": true,
    "do_not_ship_marked": true,
    "validation_required": "n >= 300 real respondents"
  },
  "recommended_actions": [
    "Add candidate outcomes for [list] that emerged from mining but aren't yet on the netted list.",
    "Drop candidate outcomes [list] that have <5 supporting quotes and no interview source — too speculative to survey.",
    "In real interviews, probe complexity factors X, Y, Z (the variables most associated with negative-sentiment posts in mining)."
  ],
  "next_step": "Use this to shape /generatesurvey. Then field. Then /computescores. Only the latter is decision-grade."
}
```

## Hard rules

- Stamp the SYNTHETIC banner on every output.
- Never publish hypothesis-landscape scores as "ODI opportunity scores" — they are always labeled `opp_hypothesis` and the classifications carry the suffix `_HYPOTHESIS`.
- Confidence < 0.4 outcomes must be excluded from the top-line summary.
- Do not chart a hypothesis landscape without the explicit "SYNTHETIC" watermark in the figure title.
