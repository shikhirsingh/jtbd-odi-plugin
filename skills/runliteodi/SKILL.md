---
name: runliteodi
description: "Run the qualitative-only Lite ODI engagement — the \"no survey\" path described in Chapter 4 (\"The lite version: qualitative-only ODI\"). Produces a directional opportunity hypothesis from interviews alone (no quant). Useful when budget or timeline precludes a 300–600 person survey but the team still needs a defensible prioritization read."
when_to_use: User explicitly asks for lite ODI, says "we can't field a survey", or invokes /runliteodi. Also triggered by "/runliteodi", "qualitative ODI only", "ODI without survey", "no panel budget".
trigger_phrases:
  - /runliteodi
  - "lite ODI"
  - "qualitative-only ODI"
  - "ODI without a survey"
  - "no panel budget"
inputs:
  - locked job statement + job map
  - 8–15 qualitative interview transcripts (recommended — Lite ODI runs on a smaller n than the full method)
  - "optional: mined-outcomes.csv from /mineoutcomes (to triangulate)"
outputs:
  - lite_opportunity_hypothesis.md — directional rank-ordered opportunities with explicit "qualitative only" disclaimer
  - lite_segments.md — narrative segments (NOT outcome-based clusters — qualitative archetypes, named & limited)
  - lite_canvas.md — the ODI Canvas filled in at lite-confidence
  - explicit notice that the result is decision-support, not decision-grade
chains_to:
  - /generatesurvey (if the team later decides to validate quantitatively)
  - /exportdeliverables (lite variant)
---

# /runliteodi — The Qualitative-Only Lite ODI Path

> "Sometimes the budget or the timeline doesn't permit a full ODI engagement. Lite ODI runs the qualitative phase to its full depth, then produces a *directional* prioritization read — without the statistical defensibility of the survey. Use it as decision support, not decision-grade." (Ch 4)

## When Lite ODI is the right call

| Situation | Lite ODI |
|---|---|
| Pre-product / pre-seed startup with <$10k research budget | ✅ |
| Time crunch (<3 weeks) but a real job to investigate | ✅ |
| Brand-new category where panel providers don't yet have the audience | ✅ |
| You already plan to follow up with a real survey in 3–6 months | ✅ |
| You're going to commit to a major roadmap based on the result | ❌ Run the full survey |
| You're setting pricing or board-level positioning | ❌ Run the full survey |
| Regulated industry (medical, financial) | ❌ Run the full survey |

## What Lite ODI gives you

- **A rank-ordered hypothesis** of unmet outcomes (using interview salience, urgency language, frequency across executors as proxies for the importance/satisfaction gap).
- **2–4 qualitative archetypes** (named groups based on observed differences in pains/contexts/workarounds) — *not* outcome-based segments, which require quantitative cluster analysis.
- **A lite version of the ODI Canvas** explicitly stamped "QUALITATIVE / LITE — DIRECTIONAL ONLY".

## What Lite ODI does NOT give you

- ❌ Top-2-box opportunity scores
- ❌ Statistically defensible segments
- ❌ Per-segment landscapes with reliable subgroup n
- ❌ Pricing bands grounded in WTP
- ❌ Engineering acceptance criteria with the 20%-better number

If you need any of those, you need the full path.

## How to run

1. **Confirm 8–15 qualitative transcripts are loaded** (5 is too few, even for lite).
2. **Run /extractoutcomes on each transcript.** Collect raw candidates.
3. **Run /netoutcomes** to dedupe and clean — same syntax bar as the full path.
4. **Rank candidates** by a *qualitative* salience proxy:
   - Frequency across transcripts (how many distinct interviewees mentioned this outcome)
   - Urgency language density (count of high-urgency phrases in supporting quotes)
   - Workaround complexity (the more complex the workaround, the more underserved)
   - Cross-source agreement if /mineoutcomes was also run
   Salience score = frequency × 0.4 + urgency × 0.3 + workaround × 0.2 + mining_confirmation × 0.1, normalized 0–10.
5. **Identify 2–4 qualitative archetypes** based on observed differences in complexity factors. Name each by complexity factor, not demographic.
6. **Render the Lite ODI Canvas** with explicit stamping.
7. **Recommend** which 8–12 real survey questions would most quickly confirm/reject the hypothesis if a future survey is fielded.

## Output

```json
{
  "skill": "runliteodi",
  "method_version": "ODI v2.4.2 (lite path, Ch 4)",
  "engagement_type": "qualitative_only_lite",
  "confidence_level": "directional",
  "decision_grade": false,
  "job_statement": "...",
  "n_interviews": 11,
  "raw_outcomes_extracted": 178,
  "netted_outcomes": 64,
  "ranked_hypothesis": [
    {"id": "E-15", "statement": "...", "salience_score": 9.4, "interviewees_mentioning": 9, "supporting_quotes": 14,
     "hypothesis_class": "likely_underserved", "next_step_to_confirm": "Field the standard imp/sat block on this outcome to n>=300"}
  ],
  "qualitative_archetypes": [
    {"label": "Long-commute multi-device user", "interviewees_count": 4, "complexity_signature": ["high device-switching", "high offline %"]},
    {"label": "Gym / high-motion user", "interviewees_count": 3, "complexity_signature": ["high physical motion", "sweat tolerance"]},
    {"label": "Casual walker", "interviewees_count": 4, "complexity_signature": ["short sessions", "single device"]}
  ],
  "outputs": {
    "lite_canvas": "lite-out/lite_canvas.md",
    "ranked_hypothesis_md": "lite-out/lite_opportunity_hypothesis.md",
    "archetypes_md": "lite-out/lite_segments.md"
  },
  "disclaimer": "All outputs are QUALITATIVE / DIRECTIONAL ONLY. Use for early-stage decision support. Not statistically defensible. Field n>=300 via /generatesurvey + /computescores to upgrade to decision-grade.",
  "recommended_confirmation_survey": {
    "minimum_n": 180,
    "minimum_outcomes_to_field": 24,
    "minimum_complexity_factors_to_field": 5,
    "next_step": "/generatesurvey on the netted-outcomes.csv produced by this lite run."
  }
}
```

## Hard rules

- Every output carries the **LITE / QUALITATIVE — DIRECTIONAL ONLY** stamp.
- Salience scores are never called "opportunity scores."
- Qualitative archetypes are never called "outcome-based segments."
- Lite ODI cannot legitimately produce a value prop, a roadmap, or engineering acceptance criteria — refuse if the user tries to chain those directly. (The full path requires real survey data.)
- The skill always recommends the path to upgrade to decision-grade.
