---
description: "PHASE VII FINAL — Bundle the engagement into EXACTLY the six Table 30.1 artifacts + Canvas + executive summary + coverage report. Refuses to ship if any artifact is missing. Aliases: /ship, /packageproject."
argument-hint: "[--project-dir .] [--zip]"
---

# /exportdeliverables (aka /ship, /packageproject) — Bundle the six artifacts

## What this is doing (plain English)

Every ODI engagement is supposed to walk out with exactly six artifacts (Table 30.1):

1. **Ranked opportunity list** (from `/computescores`)
2. **Outcome-based segments** (from `/runsegmentation`)
3. **Strategic posture** (from `/choosestrategy`)
4. **Outcome-based value proposition** (from `/generatevalueprop`)
5. **Outcome-attack roadmap** (from `/buildroadmap`)
6. **Engineering specs** (from `/outcometospec ×N`)

This skill bundles them into a single shippable `deliverables/` folder + zip, with the Canvas as the cover sheet, a 1-page executive summary, and a coverage report that proves every front-matter capability is enabled.

If any of the six is missing, the skill **refuses to ship** and tells you which command to run to fill the gap.

## What you need before running this

All six artifacts must exist in standard locations. The skill auto-discovers them.

If you've been running the commands in order (or used `/runfullodi`), they'll be there. If you skipped a step, the skill tells you which one and which command to run.

## What you'll get back

A `deliverables/` folder structured like:

```
deliverables/
├── 00_executive_summary.md
├── 00_odi_canvas.{md,png,html}
├── 01_ranked_opportunity_list/
├── 02_outcome_based_segments/
│   └── per_segment_landscapes/
├── 03_strategic_posture/
├── 04_outcome_based_value_proposition/
├── 05_outcome_attack_roadmap/
├── 06_engineering_specs/
├── appendix_a_survey_instrument/
├── appendix_b_outcome_library/
├── appendix_c_competitive_table/
└── coverage_report.md
```

Plus `deliverables.zip` and `deliverables_report.json` with the verdict.

## The coverage report explained

It proves two things:
- **All six Table 30.1 artifacts are present** (✅ per artifact)
- **All seven front-matter capabilities are enabled** (✅ per capability — know-what-to-build, identify-beachhead, price-into-WTP, engineering-measurable, marketing-lands, posture-with-evidence, repeatable-capability)

If the underlying data was synthetic, the entire bundle is stamped SYNTHETIC and the coverage verdict reads "directional only."

## What runs after this

Hand the bundle to stakeholders. Schedule the 6-month post-launch `/computescores` re-run to measure whether engineering actually moved the outcomes (the success metrics in artifact 6).

---

Invoke the `exportdeliverables` skill. Runs `python scripts/deliverables_exporter.py --project-dir <dir> --out-dir deliverables/`. REFUSE to declare success if any of the six artifacts is missing. List the missing artifacts + the command to run for each. Stamp SYNTHETIC if any source was synthetic.
