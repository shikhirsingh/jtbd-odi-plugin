---
name: choosestrategy
description: Map the opportunity landscape + segments + WTP + competitive picture onto the Jobs-to-be-Done Growth Strategy Matrix (Ch 23–24) and recommend one of the five postures — Differentiated, Dominant, Disruptive, Discrete, Sustaining — with explicit data justification. Aliased as /growthmatrix.
when_to_use: User has /computescores + /runsegmentation results (ideally + /competitiveanalysis) and asks "what's our strategy?" or "where do we sit on the matrix?". Triggered by "/choosestrategy", "/growthmatrix", "what strategy", "growth posture", "Disruptive or Differentiated?". Auto-invoked by /runfullodi and /exportdeliverables.
trigger_phrases:
  - /choosestrategy
  - /growthmatrix
  - "what strategy"
  - "growth posture"
  - "Differentiated or Dominant"
  - "should we be disruptive"
  - "pricing strategy"
  - "how should we price"
  - "what's our growth strategy"
  - "premium or budget"
  - "where do we sit on the matrix"
  - "are we disruptive"
  - "are we differentiated"
inputs:
  - overall opportunity_scores.csv
  - per-segment opportunity scores
  - segments output (sizes + complexity profiles)
  - competitive table (optional)
  - WTP data from the survey (recommended)
  - company context: cost-structure advantages, existing channel power, technology IP (asked interactively if not supplied)
outputs:
  - strategy_recommendation.md — chosen posture + 1–3 alternative postures + the data justification per cell
  - growth_matrix.png — the matrix figure with your data point(s) placed
  - one strategy per targeted segment (if more than one segment is in scope)
chains_to:
  - /generatevalueprop (per chosen segment + posture)
  - /buildroadmap (posture shapes which moves to favor)
  - /exportdeliverables (artifact #3 of the six)
---

# /choosestrategy — Pick Your Growth Posture from the Data

> "Every offering takes one of five postures defined by two questions: does it get the job done *better* than alternatives, and is it *more or less expensive*?" (Ch 23)

## The five postures (Ch 23 + Ch 24)

| Posture | Job-done quality | Price | Wins when |
|---|---|---|---|
| **Differentiated** | Better | Premium | Underserved buyers willing to pay more (Tesla, iPhone, Cordis stent) |
| **Dominant**     | Better | Lower (real cost breakthrough) | Wins every segment. Rare — requires both. |
| **Disruptive**   | Worse  | Much lower | Overserved buyers + non-consumers (Southwest, Vanguard, Canva) |
| **Discrete**     | Worse  | Higher | Survives only via captive demand (airport food, prison phones). **Trap.** Exit. |
| **Sustaining**   | Slightly better | Slightly lower | Incumbent's share-defense move. Maintenance, not growth. |

## Reading the landscape into postures (Table 23.1)

| Landscape signal | Postures on the table |
|---|---|
| Many outcomes with opp ≥ 10 (underserved) | **Differentiated** or **Dominant**. Customers will pay for better. |
| Most outcomes sat > imp (overserved) | **Disruptive**. Strip cost; bring in non-consumers. |
| Mixed (some segments underserved, others overserved) | **Differentiated + Disruptive aimed at different segments** through different brands/lines. |
| Mostly table stakes; few opp ≥ 10 | **Sustaining** (defend share via efficiency) or pivot to a new market. |

## How to choose between Differentiated and Dominant

You can only credibly claim Dominant if you have a **real cost breakthrough** — IP, manufacturing scale, supply-chain leverage, platform economics — that lets you ship "better and cheaper" simultaneously. Absent that, default to **Differentiated** until the cost advantage actually exists.

## How WTP enters

- Underserved segment + high WTP band → Differentiated.
- Underserved segment + low WTP band → Dominant (only if cost breakthrough) or pivot.
- Overserved segment + low WTP band → Disruptive.
- Overserved segment + high WTP band → look for a different segment; the customer is paying without getting value, which is unstable.

## How to run

1. **Read the overall landscape.** Count outcomes by classification; assess overall underserved vs overserved tilt.
2. **For each segment**, read its per-segment landscape and WTP profile. Different segments may take different postures.
3. **Pull competitive picture** if available. Note which competitor is "stuck in the middle" and which has the cost advantage.
4. **Ask the user** (interactive): cost-structure advantages, channel power, technology IP. Without this, you can't choose between Differentiated and Dominant credibly.
5. **Place the recommendation on the matrix.** One posture per target segment. Show alternatives.
6. **Render `growth_matrix.png`** with your placement.
7. **Document the data justification** for every part of the recommendation. No "gut" reasoning.

## Output

```json
{
  "skill": "choosestrategy",
  "method_version": "ODI v2.4.2",
  "recommendations": [
    {
      "segment": {"id": "A", "label": "Finish-cut tradesmen", "size_pct": 0.44},
      "posture": "Differentiated",
      "alternative_postures": ["Dominant — only if BOM cost reduction of >25% achievable"],
      "data_justification": {
        "landscape": "14 outcomes opp >= 10 (underserved market signal)",
        "wtp": "Median WTP $410, p75 $540 — high-WTP band",
        "competitive": "DeWalt + Makita both score < 4.0 on top 6 underserved outcomes; market collectively failing",
        "cost_structure_confirmed_with_user": "No structural cost advantage claimed; default to Differentiated"
      },
      "implied_moves_emphasis": [
        "Move 1 (Borrow) — fast 20%-better moves for top 2 outcomes",
        "Move 5 (New feature set) — primary mechanism for top 5 underserved outcomes",
        "Move 6 (New subsystem) — for ladder-safety outcome"
      ],
      "pricing_band": {"low_usd": 285, "median_usd": 410, "high_usd": 540, "anchor": "WTP p25-p75 of segment A"}
    },
    {
      "segment": {"id": "B", "label": "Quick-cut framers", "size_pct": 0.32},
      "posture": "Sustaining",
      "data_justification": {
        "landscape": "Only 2 outcomes opp >= 10; most are table stakes or overserved",
        "wtp": "Median WTP $180 — price-sensitive",
        "note": "Defend share via efficiency; this segment is not the growth bet."
      }
    },
    {
      "segment": {"id": "C", "label": "Occasional DIYers (consumer arm)", "size_pct": 0.24},
      "posture": "Disruptive",
      "data_justification": {
        "landscape": "8 outcomes sat > imp — overserved signal",
        "wtp": "Median WTP $95 — willing to pay less for simpler product",
        "competitive": "Competitor products are over-featured for this segment",
        "candidate_play": "Stripped-down SKU at ~40% price reduction; aim at non-consumers and casual users"
      }
    }
  ],
  "outputs": {
    "markdown": "strategy-out/strategy_recommendation.md",
    "png": "strategy-out/growth_matrix.png"
  },
  "next_step": "Run /generatevalueprop --segment A (the primary growth bet). Optional second pass: /generatevalueprop --segment C for the disruptive variant."
}
```

## Hard rules

- Refuse to recommend **Dominant** without a user-confirmed real cost breakthrough.
- Flag any segment that places into **Discrete** with a "this is a trap — exit" warning rather than a celebration.
- The recommendation must trace every claim back to a row in the source files.
- If WTP data is missing, the pricing band is omitted and the report explicitly says "pricing band requires WTP block in the survey — re-field with /generatesurvey --wtp."
- If multiple segments are in scope, recommend **one posture per segment** — not a single posture for the whole market.
