---
name: generatescreener
description: Build the qualitative and quantitative recruiting screener for the engagement — the questions that filter for true job executors, buyers, and lifecycle support staff. Implements Chapter 9 (qualitative screener) + Section 1 of Chapter 15 / Chapter 18 (survey screener). Produces a panel-provider-ready screener doc with disqualification logic, quotas, attention checks, and recommended incentive bands.
when_to_use: User is recruiting interviewees, building the survey, or asks "how do I screen for X". Triggered by "/generatescreener", "build the screener", "panel screener", "qualify respondents". Also called automatically by /generatesurvey to populate Section 1.
trigger_phrases:
  - /generatescreener
  - "build the screener"
  - "panel screener"
  - "qualify respondents"
inputs:
  - locked job statement
  - target customer types (job executor / buyer / lifecycle support — Ch 5)
  - target audience description (B2C consumer / B2B specialist / clinician / etc.)
  - named competitors (optional — for "do you use…" disqualifier and for skip-logic into competitive sat blocks)
  - desired sample n and segment quotas (if known)
outputs:
  - screener.md — human-readable
  - screener.json — machine schema
  - quota plan — recommended distribution across complexity-factor buckets
  - incentive recommendation (consumer / B2B / specialist — Table 18.2)
  - estimated incidence rate (rough — % of general population that will qualify)
chains_to:
  - /generatesurvey (uses this as Section 1)
---

# /generatescreener — Build the Recruiting Screener

A screener is a tightly-built sequence of 5–10 questions that filters out anyone who doesn't actually execute the job, who works for a competitor, or who can't pass a basic attention check. **Disqualify in the first 60–90 seconds** — you don't want to pay panel fees for completions you'll throw out.

## The three customer types you screen for separately (Ch 5)

| Type | Who | How to screen |
|---|---|---|
| **Job executor** | The person who personally performs the functional job | Frequency + recency of doing the job + access to a real solution |
| **Lifecycle support** | The person who installs, maintains, trains, repairs, disposes | Role + lifecycle-phase responsibility |
| **Purchase decision maker (buyer)** | The person who picks and pays | Role + final-say authority in a recent purchase |

If your engagement is B2B, run **separate** screeners and **separate** interviews/surveys for each type. Mixing them in one pool is mistake #4 of the twelve.

## The standard screener block (5–10 Qs)

| # | Question type | Purpose |
|---|---|---|
| 1 | Frequency of performing the job | Qualifies executor; sets minimum threshold (e.g., ≥ monthly) |
| 2 | Recency (last time they did it) | Filters out lapsed users |
| 3 | Current solution used | Disqualifies "none of the above"; routes to competitive sat skip-logic |
| 4 | Role / occupation (B2B) or relationship to the job (B2C) | Filters out off-target audiences |
| 5 | Employment in market research / advertising / by [competitors] | Standard contamination disqualifier |
| 6 | Decision authority (for buyer screener only) | Filters lifecycle/end-user from the buyer pool |
| 7 | Attention check ("select 4") | Drops careless completers |
| 8 | (Optional) complexity-factor quota gate | Caps each segment quota to the planned distribution |

## Incidence-rate sanity check

Before fielding, estimate the % of a generic panel that will pass. If your screener has 5 disqualification gates each filtering 70%, your gross-to-net is ~0.7⁵ ≈ 17% — and you'll need to recruit ~6× more raw respondents than your target n. This affects cost dramatically.

Share the estimated incidence with the panel provider — they'll quote based on it.

## Incentive bands (Table 18.2)

| Audience | Suggested |
|---|---|
| Consumer (general) | $5–25 |
| Professional B2B | $25–100 |
| Specialists (clinicians, executives, niche roles) | $100–500 |

Underpaying produces straight-lined data; the dollars saved cost more in noise than they save in panel fees.

## Quota plan

If you already have hypothesized complexity factors (from /hypothesizecomplexity), generate a quota plan that ensures each likely segment gets enough completes for subgroup analysis:

| Segment | Min completes for analysis | Target % of sample |
|---|---|---|
| Largest hypothesized | 80 | 30–40% |
| Mid-sized | 60 | 25–30% |
| Smallest viable | 50 | 15–20% |

## How to run

1. **Confirm customer type** the screener is for (executor / buyer / lifecycle).
2. **Pull the locked job statement** and the planned competitor list.
3. **Build the 5–8 question screener** using the templates above.
4. **Estimate incidence rate** (rough — multiply gate-pass rates).
5. **Build the quota plan** if complexity factors are known.
6. **Recommend an incentive** appropriate to the audience.
7. **Emit screener.md + screener.json** ready to paste into Qualtrics, Typeform, or a panel-provider's screener UI.

## Output

```json
{
  "skill": "generatescreener",
  "method_version": "ODI v2.4.2",
  "customer_type": "job_executor",
  "job_statement": "Cut a piece of wood in a straight line",
  "screener": [
    {"id": "SC1", "text": "In the past 3 months, how often have you used a power saw to cut wood?",
     "type": "single_select",
     "options": ["Multiple times a week", "Weekly", "Monthly", "Less than monthly", "Never"],
     "disqualify_if": ["Never", "Less than monthly"]},
    {"id": "SC2", "text": "When did you last make a finish or precision cut?",
     "type": "single_select",
     "options": ["This week", "This month", "This quarter", "This year", "Never"],
     "disqualify_if": ["Never"]},
    {"id": "SC3", "text": "Which brand of circular saw do you use most often?",
     "type": "single_select",
     "options": ["DeWalt", "Makita", "Milwaukee", "Bosch", "Ryobi", "Other", "I don't use a circular saw"],
     "disqualify_if": ["I don't use a circular saw"]},
    {"id": "SC4", "text": "Which best describes your trade?",
     "type": "single_select",
     "options": ["Carpenter / finish carpenter", "Framer", "General contractor", "Roofer", "Cabinet maker", "DIY only", "Other"],
     "disqualify_if": ["DIY only"],
     "note": "DIY-only respondents are valid for the consumer arm of this study; remove from disqualify for that arm."},
    {"id": "SC5", "text": "Are you employed in market research, advertising, or by Bosch, DeWalt, Makita, Milwaukee, or Ryobi?",
     "type": "yes_no",
     "disqualify_if": ["Yes"]},
    {"id": "SC6", "text": "To confirm you are reading carefully, please select '4'.",
     "type": "scale_1_5",
     "attention_check_value": 4}
  ],
  "incidence_estimate": {
    "expected_pass_rate": 0.18,
    "implied_gross_recruit_per_completion": 5.5,
    "note": "Strict trade-pro screener; expect ~5x raw-to-completes ratio. Share this number with the panel provider."
  },
  "quota_plan": [
    {"segment_hypothesis": "Finish-cut tradesmen",   "target_pct": 0.40, "min_completes": 160},
    {"segment_hypothesis": "Quick-cut framers",      "target_pct": 0.30, "min_completes": 120},
    {"segment_hypothesis": "Occasional DIYers (consumer arm)", "target_pct": 0.30, "min_completes": 120}
  ],
  "incentive_recommendation": {"band": "professional_b2b", "amount_usd": 75, "rationale": "Trade-pro audience; long survey (~30 min)."},
  "outputs": {
    "markdown": "screener-out/screener.md",
    "json": "screener-out/screener.json"
  },
  "next_step": "Hand to panel provider for soft-launch (n=50). Then field full sample."
}
```

## Hard rules

- Always include the "employed by competitor / market research" disqualifier — it's the cheapest single drop you'll have.
- Always include exactly one attention check in the screener.
- Always estimate incidence and surface gross-to-net ratio — costs explode without it.
- Never combine job-executor and buyer screeners. Two separate docs.
- If the user is recruiting from their own customer database (not a panel), drop the incidence question and replace incentive with "thank-you note + $10 credit / specialty acknowledgment."
