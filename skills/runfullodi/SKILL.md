---
name: runfullodi
description: MASTER ORCHESTRATOR. Runs the full ODI engagement end-to-end — every phase from job definition through engineering spec — and guarantees the six Table 30.1 artifacts and all front-matter capabilities are produced. The skill walks the user through Phases I–VII of Chapter 29, calling each sub-skill in order, gating on validations, and ending with /exportdeliverables. Supports two modes — real (commissions and waits for real human research) and rehearsal (uses synthetic respondents only, with hypothesis-only stamping throughout).
when_to_use: User wants the entire engagement coordinated by the plugin, or asks for "the full thing", "the whole engagement", "do it all". Triggered by "/runfullodi", "/fullodi", "run the whole engagement", "complete ODI engagement". The most powerful single command in the plugin.
trigger_phrases:
  - /runfullodi
  - /fullodi
  - "run the whole engagement"
  - "complete ODI engagement"
  - "do the full ODI"
inputs:
  - mode: "real" (default — pauses for real interviews and real survey) or "rehearsal" (uses /run-synthetic-survey end-to-end, marked SYNTHETIC)
  - initial input: a draft job statement, product description, or business context
outputs:
  - the full deliverables/ folder (the six Table 30.1 artifacts + canvas + exec summary + coverage report)
  - phase-by-phase progress log
  - explicit checkpoints where the orchestrator pauses for human action (in "real" mode)
chains_to:
  - /exportdeliverables (always — as the final step)
---

# /runfullodi — The Master Orchestrator

This skill runs the full Chapter 29 process (84 steps, compressed into the 30 high-value moves). It is the **only** plugin skill that guarantees, end-to-end, that every front-matter capability is enabled and every Table 30.1 artifact is produced.

## The two modes

| Mode | What it does | When to use |
|---|---|---|
| **real** | Calls all sub-skills, but **pauses at each human-in-the-loop checkpoint** — recruiting, interview scheduling, survey fielding, segmentation review. Total wall-clock: 4–8 weeks. | A real engagement with real budget for interviews + panel. |
| **rehearsal** | End-to-end synthetic — uses /run-synthetic-survey in place of recruiting + fielding. Total wall-clock: 30–60 minutes. Every output stamped SYNTHETIC. | Pre-budget hypothesis-generation, instrument stress-testing, training a team on the method. |

## The phased flow (Ch 29)

### Phase I — Initiate (real: 1 week / rehearsal: <5 min)

1. `/definejob` — produce the locked job statement.
2. **Identify three customer types** (executor / lifecycle / buyer) — interactive.
3. `/buildjobmap` — produce the 8-step universal job map.
4. **Pre-flight check** (Ch 4) — confirm ODI is the right tool. Abort if not.

✓ Checkpoint: job + job map + customer types locked.

### Phase II — Uncover Needs (real: 2 weeks / rehearsal: <10 min)

5. `/generatescreener` for the job executor (and for buyers if B2B).
6. **In real mode:** human recruits 20–30 executors + 5–10 buyers + 5–10 lifecycle support; runs interviews. Orchestrator pauses here.
   **In rehearsal mode:** `/mineoutcomes` + `/hypothesizecomplexity` produce a synthetic substitute.
7. `/extractoutcomes` per transcript (real) OR auto-extract from mined data (rehearsal).
8. `/netoutcomes` — 50–150 clean outcomes.
9. `/validateoutcomes` — hard gate. If fail, return to step 8.
10. **Capture related jobs, emotional/social, consumption-chain, financial** — Ch 12, 13 (interactive).

✓ Checkpoint: 50–150 validated outcomes; complexity-factor hypotheses captured.

### Phase III — Quantify (real: 2–3 weeks / rehearsal: <10 min)

11. `/generatesurvey` (uses /generatescreener's output as Section 1, /hypothesizecomplexity's output as Section 2).
12. **In real mode:** pilot n=10–15; clean; field to n=300–600. Orchestrator pauses for fielding.
    **In rehearsal mode:** `/run-synthetic-survey` produces synthetic_survey.csv.
13. **Apply fraud / quality controls** (Ch 18).
14. `/computescores` — produces opportunity_scores.csv, opportunity_landscape.png, the strategy-implication paragraph.

✓ Checkpoint: **Artifact 1 — Ranked opportunity list** produced.

### Phase IV — Discover Hidden Opportunities (real: 2–3 days / rehearsal: <5 min)

15. `/runsegmentation` — factor + k-means + per-segment landscapes.
16. **Profile segments** with complexity factors (auto, part of step 15).
17. `/competitiveanalysis` if competitor columns present.

✓ Checkpoint: **Artifact 2 — Outcome-based segments** produced. Plus competitive scorecard.

### Phase V — Market Strategy (real: 3–5 days / rehearsal: <5 min)

18. `/choosestrategy` — Growth Matrix placement per segment; pricing band from WTP.
19. **Choose target segment(s)** — interactive (the user owns this decision).
20. `/generatevalueprop --segment <chosen>` — per chosen segment.

✓ Checkpoint: **Artifacts 3 (Strategic posture) and 4 (Value proposition)** produced.

### Phase VI — Product Strategy (real: 3–5 days / rehearsal: <5 min)

21. `/buildroadmap` — 7-move outcome-attack plan.
22. `/outcometospec` per outcome shipping in v1.0 (typically 5–12 specs).

✓ Checkpoint: **Artifacts 5 (Roadmap) and 6 (Engineering specs)** produced.

### Phase VII — Execution & Hand-off (real: 1 week / rehearsal: <2 min)

23. `/createodicanvas` — the unified one-pager.
24. `/exportdeliverables` — bundle all six artifacts + canvas + exec summary + coverage report.

✓ Final: **All six Table 30.1 artifacts produced; all front-matter capabilities enabled.**

## How to run

The skill executes the phases sequentially. At each checkpoint:

- Confirm the prior step's output is on disk.
- Pause if the mode is "real" and the next step requires human action (interview recruiting, survey fielding, segment selection).
- Skip the pause if mode is "rehearsal" — but stamp SYNTHETIC on everything downstream.
- Update the in-progress engagement log with the timestamp and the artifact path.

## Output

```json
{
  "skill": "runfullodi",
  "method_version": "ODI v2.4.2",
  "mode": "real | rehearsal",
  "engagement_id": "2026-05-jtbd-bosch-cs20",
  "phases": [
    {"phase": "I — Initiate", "status": "complete", "artifacts": ["job_statement.json", "job_map.json"]},
    {"phase": "II — Uncover Needs", "status": "complete", "artifacts": ["screener.json", "netted-outcomes.csv", "validation_report.csv"]},
    {"phase": "III — Quantify", "status": "complete", "artifacts": ["survey.json", "opportunity_scores.csv", "opportunity_landscape.png"]},
    {"phase": "IV — Discover Hidden Opportunities", "status": "complete", "artifacts": ["segments.csv", "per_segment_landscapes/", "competitive_table.csv"]},
    {"phase": "V — Market Strategy", "status": "complete", "artifacts": ["strategy_recommendation.md", "growth_matrix.png", "valueprop.json"]},
    {"phase": "VI — Product Strategy", "status": "complete", "artifacts": ["roadmap.csv", "outcometospec-E-15.md", "..."]},
    {"phase": "VII — Hand-off", "status": "complete", "artifacts": ["canvas.png", "deliverables.zip"]}
  ],
  "table_30_1_coverage": {
    "1_ranked_opportunity_list": true,
    "2_outcome_based_segments": true,
    "3_strategic_posture": true,
    "4_value_proposition": true,
    "5_attack_roadmap": true,
    "6_engineering_specs": true
  },
  "front_matter_capability_coverage": {
    "1_know_what_to_build": true,
    "2_identify_beachhead": true,
    "3_price_into_wtp_band": true,
    "4_engineering_measurable": true,
    "5_marketing_lands": true,
    "6_strategic_posture_evidence": true,
    "7_repeatable_capability": true
  },
  "deliverables_path": "deliverables/",
  "deliverables_zip": "deliverables.zip",
  "data_provenance": "real | synthetic",
  "next_step": "If mode = rehearsal: commission real interviews + survey, then re-run /runfullodi mode=real. If mode = real: schedule the 6-month post-launch re-survey to measure success metrics in artifact 6."
}
```

## Hard rules

- Cannot declare success unless **all 6** Table 30.1 artifacts are present AND **all 7** front-matter capabilities are enabled (the coverage report says so).
- In "real" mode, must pause for interviews and survey fielding — never silently substitute synthetic.
- In "rehearsal" mode, every output is stamped SYNTHETIC and the final summary's `next_step` instructs the user to upgrade to real data.
- If `/validateoutcomes` fails, /generatesurvey is blocked — return to /netoutcomes.
- Refuses to chain past Phase V if the chosen strategy is "Discrete" — calls that out as a trap and instructs the team to find an exit before committing roadmap.
