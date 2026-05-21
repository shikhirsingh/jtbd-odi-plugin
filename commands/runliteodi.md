---
description: "Qualitative-only ODI (no survey). Produces a directional opportunity hypothesis + 2–4 qualitative archetypes from 8–15 real interviews. (Ch 4 \"Lite ODI\") Decision-support only, not decision-grade. Alias: /lite."
argument-hint: <folder of interview transcripts>
---

# /runliteodi (aka /lite) — Qualitative-only ODI

## What this is doing (plain English)

You don't have $40k or 8 weeks for a full ODI engagement. You can still get meaningful direction from real interviews alone — Lite ODI runs the qualitative phase to its full depth, then produces a *directional* read on which outcomes are likely most under-served.

It's not a substitute for the survey. The output is decision-support, not decision-grade. Treat it as a structured hypothesis.

## When Lite ODI fits

✅ Pre-product or pre-seed startup with <$10k research budget
✅ Time crunch (<3 weeks)
✅ Brand-new category where panel providers don't have your audience yet
✅ You'll follow up with a real survey at the next funding milestone

❌ You're about to commit a major roadmap or pricing decision (need Full ODI)
❌ Regulated industry (medical, financial)

## What you need before running this

- 8–15 real qualitative interview transcripts (5 is too few even for Lite)
- A locked job statement and job map
- (Optional) mined data from `/mineoutcomes` to triangulate

If you have <8 transcripts, the skill asks if you really want to proceed — qualitative reads from <8 interviews are statistically unstable.

## What you'll get back

- `lite_opportunity_hypothesis.md` — rank-ordered outcomes by qualitative salience (frequency across interviews × urgency language × workaround complexity)
- `lite_segments.md` — 2–4 qualitative archetypes (NOT outcome-based clusters; named by complexity factor)
- `lite_canvas.md` — Lite version of the ODI Canvas, stamped QUALITATIVE / DIRECTIONAL ONLY
- A recommendation for which 8–12 outcomes a future survey should validate first

Every output is stamped "LITE / QUALITATIVE — DIRECTIONAL ONLY".

## What Lite ODI does NOT give you

- Top-2-box opportunity scores (no quantitative data)
- Statistically defensible segments
- Pricing bands (no WTP without survey)
- Engineering acceptance criteria with the 20%-better number

If you need any of those, you need Full ODI. The skill refuses to chain to `/generatevalueprop`, `/buildroadmap`, or `/outcometospec`.

## What runs after this

When you have budget, run `/generatesurvey` on the Lite outcome list + `/computescores` on the survey results → upgrade to decision-grade.

---

Invoke the `runliteodi` skill. Refuse to chain into value-prop / roadmap / spec skills. Every output stamped QUALITATIVE / DIRECTIONAL ONLY. Recommend the upgrade path to Full ODI explicitly.
