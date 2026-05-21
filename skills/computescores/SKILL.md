---
name: computescores
description: Run the exact ODI opportunity algorithm — Opp = Importance + max(Importance − Satisfaction, 0), top-2-box on a 1–5 scale, normalized to 0–10 — over a survey response CSV. Produces a ranked opportunity table, the four-zone classification (extreme / low-hanging fruit / worth considering / appropriately served / overserved), the Opportunity Landscape plot, and competitive sub-tables. Implements Chapter 19, 20, 22 + Appendix B. Aliased as /opportunitylandscape.
when_to_use: User has a cleaned survey response CSV (real or synthetic) and asks for the opportunity scores, the landscape, or to "rank these outcomes". Triggered by "/computescores", "/opportunitylandscape", "score this", "build the landscape".
trigger_phrases:
  - /computescores
  - /opportunitylandscape
  - "opportunity scores"
  - "rank outcomes"
  - "landscape chart"
  - "score my survey"
  - "analyze my survey data"
  - "calculate the opportunity"
  - "which outcomes win"
  - "which features should I build"
  - "the survey is back"
  - "what do my responses mean"
  - "run the math on this"
  - "WTP analysis"
  - "willingness to pay"
inputs:
  - cleaned survey CSV with columns: respondent_id, screener_pass, quality_flag, profile_*, imp_<outcome_id>, sat_<outcome_id>, (optional) sat_<competitor>_<outcome_id>, (optional) wtp_*
  - the netted outcomes CSV (for labels)
outputs:
  - opportunity_scores.csv — every outcome with importance, satisfaction, gap, opportunity, classification
  - opportunity_landscape.png — the scatterplot (diagonal + opp=10 threshold line + labeled dots)
  - competitive_table.csv — per-competitor satisfaction per outcome (if data present)
  - markdown summary with top-20 opportunities, table-stakes, overserved outcomes, and a "what the landscape implies for strategy" paragraph
chains_to:
  - /runsegmentation (next: per-segment landscapes)
  - /generatevalueprop (after segmentation is done)
helpers:
  - scripts/opportunity_scorer.py (the canonical Appendix B implementation)
---

# /computescores — Opportunity Algorithm + Landscape

## Plain-English preamble (for newcomers)

> This skill runs Ulwick's **opportunity algorithm** on your survey CSV. Every outcome gets a score 0–20; the higher the score, the more under-served (and the more valuable to attack).
>
> The formula is: **Opportunity = Importance + max(Importance − Satisfaction, 0)**
>
> Both **Importance** and **Satisfaction** are computed as **top-2-box** — the percentage of respondents who rated 4 or 5 on a 5-point scale, then normalized to 0–10. So if 74% of people rated an outcome's importance 4 or 5, importance = 7.4.
>
> **Why double-weight importance?** Naive `gap = imp − sat` treats "9 important, 5 satisfied" and "3 important, -1 satisfied" the same (both gap = 4). The ODI formula scores them 13.0 and 3.0 respectively. Important-but-unmet beats unimportant-and-unmet at the same gap.
>
> **What you'll see in output:** ranked CSV, Opportunity Landscape chart, per-competitor table (if competitor columns present), WTP analysis (if WTP columns present), and a strategy-implication paragraph.

---

## The single formula at the heart of ODI

> **Opportunity = Importance + max( Importance − Satisfaction, 0 )**
>
> Both Importance and Satisfaction are the **percentage of respondents rating the outcome 4 or 5** on a 1–5 scale (top-2-box), then normalized to 0–10. So 74% top-2-box → 7.4.

Three properties:

1. **Importance is double-weighted.** An outcome at importance=9, sat=5 (gap=4) scores 13.0. An outcome at importance=3, sat=−1 (gap=4) scores only 3.0. *Important-but-unmet beats unimportant-and-unmet, even at the same gap.*
2. **max() caps the satisfaction effect at zero.** If sat > imp (overserved), the formula falls back to just Importance — no negative scores.
3. **Bounded 0–20.** Comparable across markets and across studies.

## Score thresholds (Chapter 19, Table 19.1)

| Range | Classification | Action |
|---|---|---|
| ≥ 15 | **Extreme opportunity** | Top-priority innovation targets. Often unlocks Differentiated or Dominant strategy. |
| 12 – 15 | **Low-hanging fruit** | Strong candidates. Highly attractive in most markets. |
| 10 – 12 | **Worth considering** | Attractive especially in clusters; competitive battlefields. |
| < 10 | **Appropriately served** | Not innovation targets. May still be table-stakes (high imp + high sat). |
| Satisfaction > Importance | **Overserved** | Cost-reduction / disruption candidates. |

## How the landscape reads (Chapter 20)

Four zones on the Importance × Satisfaction scatter:

| Zone | Where | Action |
|---|---|---|
| Underserved | High imp, low sat. Opp ≥ 10. | Innovation targets. |
| Table stakes | High imp, high sat. Opp < 10 because gap is small. | Match parity; don't over-invest. |
| Appropriately served | Moderate on both. | Match competitive parity. |
| Overserved | Sat > Imp. | Strip cost. Disruption zone. |

The composition tells you what strategies are even on the table:

- Many outcomes with Opp ≥ 10 → underserved market → Differentiated or Dominant
- Most outcomes Sat > Imp → overserved market → Disruptive
- Mixed → segment-specific Differentiated + Disruptive
- Mostly table-stakes → Sustaining or pivot

## How to run

1. **Load the survey CSV and the netted outcomes CSV.**
2. **Apply quality filters** — drop respondents whose `quality_flag` is set (Chapter 18 controls).
3. **Confirm column naming:** every outcome must have a matching `imp_<id>` and `sat_<id>` column. Refuse if mismatched.
4. **Call `scripts/opportunity_scorer.py`** with the cleaned CSV. It returns:
   - per-outcome top-2-box importance (0–10)
   - per-outcome top-2-box satisfaction (0–10)
   - opportunity score
   - classification (one of the five tiers above)
5. **Produce the landscape plot** (`scripts/opportunity_scorer.py --plot`).
6. **If competitive columns are present** (`sat_<competitor>_<id>`), produce the per-competitor table per outcome.
7. **Write the markdown summary** — top-20 opportunities, table-stakes, overserved outcomes, and a strategy-implication paragraph.

## Output

Save to `analysis-out/`:

```
analysis-out/
├── opportunity_scores.csv
├── opportunity_landscape.png
├── competitive_table.csv      (if applicable)
└── opportunity_summary.md
```

Return:

```json
{
  "skill": "computescores",
  "method_version": "ODI v2.4.2",
  "job_statement": "...",
  "sample": {
    "raw_respondents": 612,
    "after_quality_filters": 567,
    "drop_rate": 0.073,
    "drop_rate_warning": false
  },
  "scoring_method": {
    "scale": "1-5",
    "scoring_rule": "top-2-box (4 or 5), normalized to 0-10",
    "formula": "Opp = Importance + max(Importance - Satisfaction, 0)"
  },
  "outputs": {
    "scores_csv": "analysis-out/opportunity_scores.csv",
    "landscape_png": "analysis-out/opportunity_landscape.png",
    "competitive_csv": "analysis-out/competitive_table.csv",
    "summary_md": "analysis-out/opportunity_summary.md"
  },
  "summary": {
    "extreme_opportunity_count": 4,
    "low_hanging_fruit_count": 11,
    "worth_considering_count": 17,
    "appropriately_served_count": 49,
    "overserved_count": 15,
    "table_stakes_outcomes": ["E-03", "P-02", "..."],
    "top_3_opportunities": [
      {"id": "E-12", "statement": "...", "importance": 8.9, "satisfaction": 3.2, "opportunity": 14.6, "class": "low_hanging_fruit"},
      {"id": "P-05", "statement": "...", "importance": 8.6, "satisfaction": 4.1, "opportunity": 13.1, "class": "low_hanging_fruit"},
      {"id": "M-02", "statement": "...", "importance": 8.7, "satisfaction": 3.8, "opportunity": 13.6, "class": "low_hanging_fruit"}
    ],
    "strategy_implication": "Underserved market with 15 outcomes scoring above 10 — Differentiated or Dominant posture on the table. No overserved cluster large enough to support a Disruptive entrant. See /generatevalueprop next."
  },
  "next_step": "Run /runsegmentation on the same CSV to discover per-segment landscapes."
}
```

## Worked example (Chapter 19, Example 19.1 — Bosch CS20)

> 200 of 270 respondents (74% → 7.4) rated *"minimize the likelihood that the cut goes off track"* 4 or 5 for importance. Only 75 (28% → 2.8) rated their satisfaction with that outcome 4 or 5.
>
> Opp = 7.4 + max(7.4 − 2.8, 0) = 7.4 + 4.6 = **12.0** → "low-hanging fruit"
>
> Bosch attacked it directly with the CS20 — their best-selling N.A. circular saw for over a decade.

## Hard rules

- Never compute scores from means. Always top-2-box.
- Never silently drop respondents — surface every drop in the `sample` block.
- Never call something a "table-stakes outcome" unless importance ≥ 7.5 AND satisfaction ≥ 7.5.
- Never produce a competitive table that compares average means across competitors — show top-2-box per outcome per competitor.
- If the survey is synthetic, **prepend the SYNTHETIC banner to all outputs and add `"data_provenance": "SYNTHETIC — directional only, do not ship"`** to the JSON.
