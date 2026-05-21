---
name: competitiveanalysis
description: Run outcome-based competitive analysis — per-outcome top-2-box satisfaction for each named competitor — and surface where each competitor wins, where the market is collectively failing, where to attack, and where to strip cost. Implements Chapter 22 (and the 20%-better rule from Ch 28).
when_to_use: User has /computescores output AND the survey included competitive satisfaction blocks for ≥2 named products. Triggered by "/competitiveanalysis", "competitive scorecard", "where do competitors win", "where should we attack". Also auto-invoked by /choosestrategy and /exportdeliverables.
trigger_phrases:
  - /competitiveanalysis
  - "competitive scorecard"
  - "competitive analysis"
  - "where do we beat the competition"
inputs:
  - survey CSV with sat_<competitor>_<outcome_id> columns
  - opportunity_scores.csv (for opp + class anchor)
  - netted outcomes CSV (for labels)
  - your own product name (optional — to compare your current product against competitors)
outputs:
  - competitive_table.csv — per outcome: importance, overall sat, opp, plus sat per competitor
  - competitive_summary.md — where each competitor wins, where the market fails, top "attack" outcomes, "strip-cost" outcomes (overserved by competitors)
  - per-competitor scorecards (PNG) — radar chart of the top 20 outcomes for each competitor
chains_to:
  - /choosestrategy (uses competitive picture + landscape to recommend posture)
  - /outcometospec (acceptance criteria use the best-competitor sat as parity target)
helpers:
  - scripts/opportunity_scorer.py --competitors (computes the table)
---

# /competitiveanalysis — Outcome-Based Competitive Picture

> Don't compare feature lists. Compare how well each competitor satisfies each desired outcome — from the customer's point of view. (Ch 22)

## What this produces (Table 22.1 shape)

| Outcome | Imp | Sat (overall) | Opp | Sat — DeWalt | Sat — Makita | Sat — Yours |
|---|---|---|---|---|---|---|
| Minimize likelihood that debris flies into the user's face | 8.9 | 3.2 | 14.5 | 3.1 | 3.3 | 1.2 |
| Minimize likelihood of moving off the cut line | 8.7 | 3.8 | 13.5 | 4.2 | 3.4 | 3.6 |
| Minimize time to set the angle of the blade | 8.6 | 4.1 | 13.0 | 5.0 | 3.6 | 3.9 |
| Minimize likelihood of snagging the cord | 8.2 | 3.7 | 12.7 | 3.8 | 3.6 | 3.5 |

## Four things the table reveals (Ch 22)

1. **Where each competitor wins** (e.g., DeWalt beats Makita on bevel-angle setting).
2. **Where the whole market is failing** — any outcome where every competitor scores low. These are the *richest* attack opportunities because no one has solved it.
3. **Where you should attack** — high importance + low satisfaction across competitors + a plausible technical path for you.
4. **Where to strip cost** — outcomes where a competitor scores high but importance is low (overserved). Don't replicate that capability.

## The 20% rule (Ch 22 + Ch 28)

> "Significantly better" — Strategyn's empirical rule — means your product must satisfy the underserved outcome roughly **20% better** than competing solutions to win meaningful share. Anything under 5% better is "stuck in the middle"; customers won't switch.

For every outcome you plan to attack, this skill computes the **best-competitor sat + 20%** as the *minimum aspirational target* for your product on that outcome. This number flows into /outcometospec acceptance criteria.

## Table stakes vs. underserved

For each outcome, classify it relative to *your* (planned or current) product:

- **Table stakes**: high importance + competitor sat ≥ 7.5. You must score ≥ parity or you lose anyway.
- **Underserved & winnable**: high importance + best-competitor sat < 6 + plausible technical path. *Attack*.
- **Underserved & hard**: high importance + best-competitor sat already > 7 (close to ceiling). Hard to differentiate; consider partnerships.
- **Overserved**: sat > importance across competitors. *Strip cost*.

## How to run

1. **Verify competitor columns exist** in the survey CSV — pattern `sat_<competitor>_<outcome_id>`. If none, refuse.
2. **Call** `python scripts/opportunity_scorer.py --survey <csv> --outcomes <netted> --competitors "<a>,<b>" --out-dir analysis-out/`
3. **Compute the 20%-better target** for each outcome row: `target = min(10, best_competitor_sat × 1.2)`.
4. **Classify each outcome** into table stakes / underserved & winnable / underserved & hard / overserved.
5. **Render a per-competitor radar chart** of the top 20 outcomes (showing where each competitor sits relative to the others).
6. **Emit competitive_summary.md** with the four-bullet read of the table (the four things above).

## Output

```json
{
  "skill": "competitiveanalysis",
  "method_version": "ODI v2.4.2",
  "competitors_analyzed": ["DeWalt", "Makita", "Milwaukee"],
  "n_outcomes": 75,
  "outputs": {
    "csv": "analysis-out/competitive_table.csv",
    "summary_md": "analysis-out/competitive_summary.md",
    "radar_pngs": ["analysis-out/competitive_radar_DeWalt.png", "..."]
  },
  "summary": {
    "where_each_competitor_wins": {
      "DeWalt":   [{"outcome_id": "P-05", "sat": 5.0, "next_best": 3.6, "delta": 1.4}],
      "Makita":   [{"outcome_id": "E-19", "sat": 4.8, "next_best": 3.6, "delta": 1.2}]
    },
    "market_collectively_failing": [
      {"outcome_id": "E-15", "imp": 8.9, "best_competitor_sat": 3.3, "opp": 14.5,
       "note": "All competitors below 3.5 — no one is solving this. Richest attack."}
    ],
    "you_should_attack": [
      {"outcome_id": "E-15", "best_competitor_sat": 3.3, "twenty_pct_target_sat": 4.0, "physical_target": "<5% of cuts produce face-zone debris"}
    ],
    "strip_cost_candidates": [
      {"outcome_id": "M-04", "imp": 5.2, "best_competitor_sat": 7.8, "note": "Market overserves; do not replicate."}
    ],
    "table_stakes_outcomes": [
      {"outcome_id": "E-01", "imp": 9.5, "best_competitor_sat": 8.2, "must_match_at_or_above": 8.2}
    ]
  },
  "next_step": "Feed table_stakes_outcomes + you_should_attack into /outcometospec (acceptance criteria use these numbers directly). Feed the summary into /choosestrategy."
}
```

## Hard rules

- If <2 competitor sat blocks exist, refuse and tell the user the survey didn't capture competitive data.
- Strategyn's one-product-per-respondent rule: each respondent only rated *their* used product. The script handles this by subsetting respondents per competitor and computing top-2-box on each subset.
- Never declare a competitor "loses" on an outcome without a sample of ≥30 respondents who use it (statistical floor).
- The 20%-better number is the *minimum* aspirational target, not a forecast.
