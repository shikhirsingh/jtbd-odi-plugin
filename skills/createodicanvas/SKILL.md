---
name: createodicanvas
description: Produce the one-page ODI Canvas — a unified, board-ready summary of the entire engagement on a single sheet. Pulls together the job statement, job map, target segment, top underserved outcomes, strategic posture, value proposition, top roadmap moves, and engineering acceptance criteria, with every cell traced back to the source artifact. Pure synthesis skill — no new method content, only assembly.
when_to_use: User asks for "the canvas", "the one-pager", "the deck-ready summary", or invokes /createodicanvas after at least the opportunity landscape exists. Also auto-invoked by /runfullodi and /exportdeliverables.
trigger_phrases:
  - /createodicanvas
  - "ODI canvas"
  - "one-page summary"
  - "exec summary of the project"
inputs:
  - job statement (from /definejob)
  - job map (from /buildjobmap)
  - opportunity_scores.csv (from /computescores)
  - segments output (from /runsegmentation) — optional but recommended
  - value prop (from /generatevalueprop) — optional
  - roadmap CSV (from /buildroadmap) — optional
  - any /outcometospec sheets — optional
  - strategic posture (from /choosestrategy) — optional
outputs:
  - canvas.md — single-page rendered version
  - canvas.png (rendered via scripts/canvas_generator.py)
  - canvas.json — machine-readable
  - canvas.html — printable
chains_to:
  - /exportdeliverables (canvas is one of the bundled artifacts)
helpers:
  - scripts/canvas_generator.py
---

# /createodicanvas — The Unified ODI Canvas

A single page that names the segment, the job, the underserved outcomes, the posture, the value prop, and the build plan — every cell footnoted back to its source artifact. Every ODI engagement should end with one. It is the artifact executives actually read.

## The 9-cell layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. Job statement (Ch 6)              │ 2. Target segment (Ch 21)         │
│    + 3 stability checks              │    + size % + complexity profile  │
├─────────────────────────────────────────────────────────────────────────┤
│ 3. Job map (Ch 7) — 8 steps in ideal sequence                            │
├─────────────────────────────────────────────────────────────────────────┤
│ 4. Top 7 underserved outcomes (Ch 19)│ 5. Strategic posture (Ch 23–24)   │
│    each with opp score + class       │    one of D/D/D/D/Sustaining      │
├─────────────────────────────────────────────────────────────────────────┤
│ 6. Outcome-based value proposition (Ch 25) — 4-part fill-in              │
├─────────────────────────────────────────────────────────────────────────┤
│ 7. Top 5 product moves (Ch 27)       │ 8. WTP band + price posture       │
│    outcome / move / release          │    from survey WTP block          │
├─────────────────────────────────────────────────────────────────────────┤
│ 9. Engineering acceptance criteria (Ch 28) — top 3 outcomes ship-ready   │
└─────────────────────────────────────────────────────────────────────────┘
```

Every cell carries a footnote citing the source artifact (filename + section) so a reader can drill down.

## How to assemble

1. **Load every available source artifact.** If a cell can't be filled (e.g., no /choosestrategy yet), render a placeholder *"Pending: /choosestrategy"* — don't fabricate.
2. **For cells 4 and 9**, use the *target segment's* top outcomes (per-segment landscape), not the overall.
3. **For cell 6**, copy the exact /generatevalueprop output. Do not rewrite.
4. **For cell 7**, pull top 5 rows of the roadmap CSV, prioritized by `opportunity × release_proximity`.
5. **Validate traceability.** Every numeric or claim must trace to a row in a source file.
6. **Stamp synthetic banner** if any underlying artifact was produced from synthetic data.
7. **Call `scripts/canvas_generator.py`** to render the visual outputs.

## Output

```json
{
  "skill": "createodicanvas",
  "method_version": "ODI v2.4.2",
  "data_provenance": "real | synthetic",
  "cells": {
    "1_job_statement": {"value": "Cut a piece of wood in a straight line", "source": "definejob.json#full_statement", "stability_check_passed": true},
    "2_target_segment": {"id": "A", "label": "Finish-cut tradesmen", "size_pct": 0.44, "complexity_profile": ["high finish_cut_frequency", "high bevel_cut_frequency"], "source": "runsegmentation.json#segments.A"},
    "3_job_map":       {"steps": [...], "source": "buildjobmap.json#job_map"},
    "4_top_outcomes":  {"rows": [{"id": "E-15", "statement": "...", "opp": 16.6, "class": "extreme_opportunity"}, ...], "source": "opportunity_scores_segment_A.csv"},
    "5_strategic_posture": {"value": "Differentiated", "reason": "14 outcomes opp >= 10 in segment A; WTP band high", "source": "choosestrategy.json"},
    "6_value_prop":    {"value": "For ...", "source": "valueprop.json#value_prop"},
    "7_top_moves":     {"rows": [...], "source": "roadmap.csv"},
    "8_wtp_band":      {"low": 285, "median": 410, "high": 540, "currency": "USD", "source": "opportunity_scores.csv#wtp_analysis"},
    "9_acceptance":    {"rows": [...], "source": "outcometospec-*.json"}
  },
  "missing_cells": [],
  "outputs": {
    "markdown": "canvas-out/canvas.md",
    "png":      "canvas-out/canvas.png",
    "html":     "canvas-out/canvas.html",
    "json":     "canvas-out/canvas.json"
  },
  "next_step": "Use the canvas as the cover sheet for /exportdeliverables, which produces all six Table 30.1 artifacts as a single bundle."
}
```

## Hard rules

- Every cell value must trace to a real source file row. No fabrication.
- If the underlying data is synthetic, the canvas carries the SYNTHETIC banner top-and-bottom.
- A canvas with >2 placeholder cells gets a warning: "Engagement is <70% complete; canvas is partial."
- Never invent a strategic posture if /choosestrategy hasn't been run; leave cell 5 empty.
