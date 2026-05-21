---
description: "PHASE III ANALYSIS — Run the opportunity formula (Imp + max(Imp − Sat, 0)) on a cleaned survey CSV. Produces the ranked opportunity list, the Opportunity Landscape chart, the per-competitor table, and the WTP band. (Ch 19, 20 + Appendix B) Alias: /opportunitylandscape."
argument-hint: <path to cleaned survey CSV>
---

# /computescores — The opportunity formula in action

## What this is doing (plain English)

You've fielded your survey. You have ratings from real customers on importance and satisfaction for every outcome. This skill runs Ulwick's opportunity algorithm — `Opp = Importance + max(Importance − Satisfaction, 0)` — across every outcome and ranks them.

The math intentionally double-weights importance. An outcome that's "9 important, 5 satisfied" (gap = 4) scores 13.0. An outcome that's "3 important, -1 satisfied" (gap = 4) scores 3.0. Important-but-unmet beats unimportant-and-unmet even at the same gap.

Out the other side: a ranked list (which outcomes to attack first), the **Opportunity Landscape chart** (visual), and per-competitor satisfaction comparisons.

## What you need before running this

- **A cleaned survey CSV.** Either from a real fielded survey OR from `/run-synthetic-survey` (which will be stamped SYNTHETIC throughout).
  - Required columns: `respondent_id`, `quality_flag`, `imp_<outcome_id>` and `sat_<outcome_id>` per outcome
  - Optional: `sat_<competitor>_<outcome_id>` for competitive analysis, `wtp_*` for pricing band
- The **netted outcomes CSV** (for outcome labels)

If columns are missing or mislabeled, the skill refuses and tells you what's wrong.

## What you'll get back

- `opportunity_scores.csv` — every outcome ranked, with importance, satisfaction, opportunity, classification
- `opportunity_landscape.png` — the scatter chart (Underserved / Table-stakes / Appropriately-served / Overserved)
- `competitive_table.csv` (if competitor columns present)
- `wtp_analysis.json` (if WTP columns present)
- `opportunity_summary.md` — top-20 + strategy-implication paragraph

Plus a printed summary of the top 10 outcomes with their classifications.

## Reading the result

| Score range | Classification | What to do |
|---|---|---|
| ≥ 15 | Extreme opportunity | Top-priority innovation target |
| 12–15 | Low-hanging fruit | Strong candidate; short-term roadmap |
| 10–12 | Worth considering | Competitive battlefields |
| < 10 | Appropriately served | Not an innovation target |
| Sat > Imp | Overserved | Cost-reduction / disruption candidate |

If many outcomes score ≥ 10 → underserved market → Differentiated or Dominant strategy.
If many outcomes show Sat > Imp → overserved market → Disruptive strategy.

## Jargon you'll see

- **Top-2-box** — % of respondents who rated 4 or 5 on a 5-point scale. ODI scoring rule.
- **Opportunity** — `Imp + max(Imp − Sat, 0)`, on 0–20.
- **Landscape** — the Importance × Satisfaction chart.

## What runs after this

`/runsegmentation` (per-segment landscapes) → `/competitiveanalysis` → `/choosestrategy`.

If the input was synthetic, the skill stamps SYNTHETIC on every output and refuses to chain downstream decision-grade skills.

---

Invoke the `computescores` skill. Runs `python scripts/opportunity_scorer.py --survey <csv> --outcomes <netted.csv> --out-dir analysis-out/`. If the CSV came from `/run-synthetic-survey`, pass `--synthetic`. If competitor columns exist, pass `--competitors`. Surface the WTP band in the printed summary.
