---
name: exportdeliverables
description: Bundle the engagement into a single shippable package containing exactly the six artifacts from Table 30.1 of the ODI handbook — Ranked opportunity list, Outcome-based segments, Strategic posture, Outcome-based value proposition, Outcome-attack roadmap, Engineering specs. Plus the ODI Canvas cover sheet, an executive summary, and a final coverage report against the "What you'll be able to do after running this" checklist in the front matter. Aliased as /packageproject.
when_to_use: User asks to "ship", "package", "export", or "hand off" the engagement. Triggered by "/exportdeliverables", "/packageproject", "package the project", "final deliverable", "hand-off". Also called by /runfullodi as its final step.
trigger_phrases:
  - /exportdeliverables
  - /packageproject
  - "ship the project"
  - "package the deliverables"
  - "hand off the engagement"
inputs:
  - all prior engagement outputs (skill auto-discovers from standard out-dirs)
  - "target audience for the package: exec / PM / engineering / mixed (default: mixed)"
  - "format: zip / folder / pdf-bundle (default: folder + zip)"
outputs:
  - deliverables/ folder containing the 6 artifacts + canvas + exec summary + coverage report
  - deliverables.zip
  - coverage_report.md — proves all six Table 30.1 artifacts are present AND all six front-matter capabilities are enabled
chains_to: []
helpers:
  - scripts/deliverables_exporter.py
---

# /exportdeliverables — The Six-Artifact Bundle

This skill produces **the six things the ODI handbook says you must walk out of an engagement with** (Table 30.1):

| # | Artifact | Produced by | Used by |
|---|---|---|---|
| 1 | **Ranked opportunity list** | /computescores → opportunity_scores.csv | PM — decides what to build first |
| 2 | **Outcome-based segments** | /runsegmentation → segments.csv + per-segment landscapes | Marketing + sales — targeting |
| 3 | **Strategic posture** | /choosestrategy → strategy_recommendation.md + growth_matrix.png | Leadership — investment alignment |
| 4 | **Outcome-based value proposition** | /generatevalueprop → valueprop.json + marketing variants | Marketing copy + sales talk track |
| 5 | **Outcome-attack roadmap** | /buildroadmap → roadmap.csv + roadmap.md | PM — planning |
| 6 | **Engineering specs** | /outcometospec ×N → spec sheets | Engineering — build |

Plus:

- **ODI Canvas** (`/createodicanvas`) — the cover sheet executives actually read.
- **Executive summary** — 1 page; the project's findings in business language.
- **Coverage report** — proves the engagement enables every capability listed in the front matter ("What you'll be able to do after running this"):

| # | Capability (front-matter) | How this engagement enables it |
|---|---|---|
| 1 | Know exactly what to build to win the market | Ranked opportunity list (artifact 1) + per-segment landscapes (artifact 2) |
| 2 | Identify the specific customer segment that will buy first | Outcome-based segments (artifact 2) profiled by complexity factors |
| 3 | Price into the WTP band you actually have | /choosestrategy.pricing_band derived from survey WTP block (artifact 3) |
| 4 | Hand engineering a measurable target | Engineering specs (artifact 6) with the 20%-better acceptance criteria |
| 5 | Write marketing copy that lands | Value prop + marketing variants (artifact 4) |
| 6 | Choose the right strategic posture with evidence | Growth Strategy Matrix placement (artifact 3) |
| 7 | Run it again, faster | Reusable outcome library + survey instrument exported with the package |

## How to run

1. **Discover** the artifacts in the project's working tree. Standard locations:
   - `analysis-out/opportunity_scores.csv` (+ per-segment variants)
   - `analysis-out/segments.csv`, `analysis-out/segmentation_audit.json`, `analysis-out/landscape_segment_*.png`
   - `analysis-out/competitive_table.csv` (if exists)
   - `strategy-out/strategy_recommendation.md`, `strategy-out/growth_matrix.png`
   - `valueprop-out/valueprop.json`
   - `roadmap-out/roadmap.csv`, `roadmap-out/roadmap.md`
   - `spec-out/outcometospec-*.json` and matching .md
   - `canvas-out/canvas.png`, `canvas-out/canvas.md`
   - `survey-out/` (the survey instrument, for re-use)
   - `netted-outcomes.csv` (the outcome library, for re-use)
2. **Validate the coverage table.** If any of the six artifacts is missing, flag it loudly and offer to run the missing skill. Do not silently ship an incomplete bundle.
3. **Build the executive summary** — 1 page max:
   - Job statement
   - Target segment (size, complexity profile)
   - Strategic posture
   - Top 3 underserved outcomes (with opp scores)
   - Headline number from value prop
   - Top 3 roadmap moves and their releases
   - One sentence on pricing band
   - One sentence on next step
4. **Render the ODI Canvas** if not already produced.
5. **Build the coverage report** mapping each front-matter capability to the artifact that enables it.
6. **Call `scripts/deliverables_exporter.py`** which assembles the folder + zip.
7. **If any underlying artifact is from synthetic data**, the entire bundle is stamped with the SYNTHETIC banner and the coverage report carries a "validate with n ≥ 300 real respondents" instruction.

## Output

The skill produces this folder structure:

```
deliverables/
├── 00_executive_summary.md
├── 00_odi_canvas.{md,png,html}
├── 01_ranked_opportunity_list/
│   ├── opportunity_scores.csv
│   ├── opportunity_landscape.png
│   └── opportunity_summary.md
├── 02_outcome_based_segments/
│   ├── segments.csv
│   ├── segmentation_audit.json
│   └── per_segment_landscapes/
│       ├── landscape_segment_A.png
│       ├── landscape_segment_B.png
│       └── landscape_segment_C.png
├── 03_strategic_posture/
│   ├── strategy_recommendation.md
│   ├── growth_matrix.png
│   └── pricing_band.md
├── 04_outcome_based_value_proposition/
│   ├── valueprop.md
│   ├── valueprop.json
│   └── marketing_variants.md
├── 05_outcome_attack_roadmap/
│   ├── roadmap.csv
│   └── roadmap.md
├── 06_engineering_specs/
│   ├── E-15_spec.md
│   ├── E-12_spec.md
│   ├── P-05_spec.md
│   └── ...
├── appendix_a_survey_instrument/
│   └── survey.{md,json,qsf-import.txt,typeform.json}
├── appendix_b_outcome_library/
│   └── netted-outcomes.csv
├── appendix_c_competitive_table/
│   └── competitive_table.csv
└── coverage_report.md
```

Return:

```json
{
  "skill": "exportdeliverables",
  "method_version": "ODI v2.4.2",
  "data_provenance": "real | synthetic",
  "table_30_1_artifacts": {
    "1_ranked_opportunity_list": {"present": true, "path": "deliverables/01_ranked_opportunity_list/"},
    "2_outcome_based_segments":  {"present": true, "path": "deliverables/02_outcome_based_segments/"},
    "3_strategic_posture":       {"present": true, "path": "deliverables/03_strategic_posture/"},
    "4_value_proposition":       {"present": true, "path": "deliverables/04_outcome_based_value_proposition/"},
    "5_attack_roadmap":          {"present": true, "path": "deliverables/05_outcome_attack_roadmap/"},
    "6_engineering_specs":       {"present": true, "path": "deliverables/06_engineering_specs/", "n_specs": 7}
  },
  "front_matter_capabilities_enabled": {
    "1_know_what_to_build":     {"enabled": true, "via": "artifact 1 + artifact 2"},
    "2_identify_beachhead":     {"enabled": true, "via": "artifact 2 (with complexity-factor profile)"},
    "3_price_into_wtp_band":    {"enabled": true, "via": "artifact 3 (pricing_band derived from survey WTP)"},
    "4_engineering_measurable": {"enabled": true, "via": "artifact 6"},
    "5_marketing_lands":        {"enabled": true, "via": "artifact 4 (with variants)"},
    "6_strategic_posture_evidence": {"enabled": true, "via": "artifact 3 + Growth Matrix"},
    "7_repeatable":             {"enabled": true, "via": "appendix B outcome library + appendix A survey instrument"}
  },
  "missing_artifacts": [],
  "outputs": {
    "folder": "deliverables/",
    "zip":    "deliverables.zip",
    "coverage_report": "deliverables/coverage_report.md"
  },
  "next_step": "Hand to stakeholders. Then schedule the 6-month post-launch /computescores re-run to measure whether engineering hit the success metrics in artifact 6."
}
```

## Hard rules

- Refuse to ship if any of the six artifacts is missing. Tell the user which skill to run.
- Refuse to ship if /validateoutcomes was never run against the outcome library (or was run and failed).
- If any artifact is synthetic, the whole bundle is stamped SYNTHETIC and the coverage report's verdict is "directional only".
- The coverage report's 7-row capabilities table must show "enabled: true" for every row before the skill declares success.
