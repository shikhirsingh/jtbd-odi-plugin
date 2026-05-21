---
description: Render the one-page ODI Canvas — a 9-cell board-ready summary that maps every cell to its source artifact. The cover sheet executives actually read. Alias: /canvas.
argument-hint: [--target-segment <segment_id>]
---

# /createodicanvas (aka /canvas) — The one-page summary

## What this is doing (plain English)

After running the full engagement, you have a dozen files spread across many folders. This skill assembles a single page that shows: the job, the target segment, the job map, the top underserved outcomes, the strategic posture, the value proposition, the top product moves, the pricing band, and the engineering acceptance criteria — every cell footnoted to the source file.

This is what gets printed for the board meeting. It is not a slide deck; it is a one-pager that fits on one wall poster.

## What you need before running this

The skill auto-discovers artifacts from standard locations:
- `analysis-out/opportunity_scores.csv` (+ per-segment variants)
- `analysis-out/segmentation_audit.json`
- `strategy-out/strategy_recommendation.json`
- `valueprop-out/valueprop.json`
- `roadmap-out/roadmap.csv`
- `spec-out/*.md` and `*.json`
- `analysis-out/wtp_analysis.json`

It also accepts an optional `--target-segment <id>` so the Canvas shows that segment's top outcomes (not market-wide).

Any cell with no source data is rendered as `_pending /<command>_` rather than fabricated.

## What you'll get back

- `canvas.md` (human-readable)
- `canvas.png` (printable)
- `canvas.html` (web-printable)
- `canvas.json` (machine-readable)

If any underlying artifact was synthetic, the Canvas is stamped SYNTHETIC top and bottom plus watermarked on the PNG.

## What runs after this

`/exportdeliverables` — the Canvas becomes the cover sheet of the final deliverables bundle.

---

Invoke the `createodicanvas` skill. Runs `python scripts/canvas_generator.py …`. Never fabricate cells — if data is missing, render `_pending_` and tell the user which command to run to fill the gap. Stamp SYNTHETIC if any source was synthetic.
