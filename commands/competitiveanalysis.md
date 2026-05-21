---
description: Per-outcome competitive scorecard — top-2-box satisfaction for each named competitor + the 20%-better target your product needs to hit to win share. (Ch 22 + Ch 28)
argument-hint: <path to survey CSV> [--competitors "a,b,c"]
---

# /competitiveanalysis — Where does each competitor win or lose?

## What this is doing (plain English)

You don't compare features. You compare how well each competitor satisfies each desired outcome — from the customer's point of view. This skill produces a table that shows, per outcome:

- How important the outcome is
- Overall satisfaction
- Satisfaction with each named competitor
- The 20%-better target your new product must hit to win meaningful share

From this table you read four things at a glance:
1. **Where each competitor wins** (DeWalt beats Makita on bevel-angle setting)
2. **Where the whole market fails** (no competitor scores >3 on debris-in-face — richest attack)
3. **Where you should attack** (high importance, no competitor close to the ceiling, you have a technical path)
4. **Where to strip cost** (competitors score high but importance is low — overserved features)

## What you need before running this

- The survey CSV must have `sat_<competitor>_<outcome_id>` columns (added during `/generatesurvey` when you name competitors)
- At least **2 named competitors** — otherwise there's no comparison

If only one or zero competitors in the data, the skill refuses and tells you to re-field with competitor blocks.

## What you'll get back

- `competitive_table.csv` — importance, overall sat, opp + sat per competitor + best-competitor-sat + 20%-better target
- `competitive_summary.md` — where each competitor wins, where the market fails, attack list, strip-cost list
- Per-competitor radar charts of top 20 outcomes

## The 20% rule explained

Strategyn's empirical switching threshold: to win meaningful share on an underserved outcome, your product must satisfy it **~20% better** than the best competing solution. Anything under 5% better is "stuck in the middle"; customers won't switch. The acceptance criteria in `/outcometospec` use this number.

## What runs after this

`/choosestrategy` (uses the competitive table + landscape + WTP to recommend posture).
`/outcometospec` (acceptance criteria use best-competitor sat × 1.2 as the aspirational target).

---

Invoke the `competitiveanalysis` skill. Runs `python scripts/opportunity_scorer.py --survey <csv> --outcomes <netted.csv> --competitors "<list>" --out-dir analysis-out/`. Refuse to proceed if <2 competitor sat blocks exist. Surface the four "what this table tells you" buckets explicitly.
