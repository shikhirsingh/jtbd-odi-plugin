---
description: SYNTHETIC PIPELINE — Mine public data → synthesize 10 grounded personas → simulate an ODI survey. HYPOTHESIS-GENERATION ONLY. Statistical validity is bounded by persona count (~10 archetypes), NOT by total row count. Long-tail outcomes are systematically under-counted. Use /researchpath for decision-grade output without interviews. Alias: /synthsurvey.
argument-hint: "<job statement>" [--n-personas 10] [--n-responses-per-persona 60]
---

# /run-synthetic-survey (aka /synthsurvey) — The virtual respondent panel

## What this is doing (plain English)

For a given job, the orchestrator runs the full ODI pipeline end-to-end but **replaces real respondents with LLM-simulated ones**. Wall-clock: 30–60 minutes.

It produces a CSV with the same shape `/computescores` expects from a real survey.

## ⚠️ Honest sample-size disclosure

This output looks like a real survey but **isn't statistically equivalent to one**:

```
What you see:  10 personas × 60 sampled rows = 600 "respondents"
What you have: ~10 archetype-level signals (the 60 sampled rows
               are noise around each persona's locked biases)
```

A real n=600 survey draws 600 independent humans from the population. This draws 10 LLM-designed archetypes and samples noise around each. **Long-tail outcomes that don't fit one of the 10 personas are systematically under-counted.**

## When to use this vs. alternatives

| Goal | Use |
|---|---|
| Quick hypothesis before any real research | **`/run-synthetic-survey`** |
| Stress-test a draft outcome list | **`/run-synthetic-survey`** |
| Decide which real interviews to commission first | **`/run-synthetic-survey`** |
| Decision-grade scoring but no time for interviews | **`/researchpath`** (online research → REAL survey) |
| Full decision-grade engagement | **`/runfullodi --mode real`** |

## What this is NOT

The handbook is explicit (Part IV): synthetic data is NEVER a substitute for the real survey. The plugin enforces this — `/generatevalueprop`, `/buildroadmap`, `/outcometospec`, and `/choosestrategy` REFUSE to chain off synthetic data. They'll route you to `/researchpath` or `/runfullodi --mode real` instead.

## What you need before running this

- A job statement (a draft is fine — the skill will lock it via `/definejob`)
- (Optional) n_personas (default **10**, up from 6; range 6–20). More personas = more archetype-level distinctions.
- (Optional) n_responses_per_persona (default 60; range 30–120). Adds within-persona variance, NOT statistical power.

## What you'll get back

- `synthetic-out/personas.json` — the 10 grounded personas (each anchored in ≥3 mined quotes)
- `synthetic-out/synthetic_survey.csv` — full schema with `persona_id` column for audit
- `synthetic-out/mined-outcomes.csv` + `source-evidence.md`
- `synthetic-out/hypothesis-summary.md` — what to do next + the upgrade-to-real-survey CTA

Every output stamped **SYNTHETIC**. The summary surfaces TWO clear upgrade options:
1. `/researchpath` — keep the mining, field a real survey
2. `/runfullodi --mode real` — full method

## What runs after this

The CSV can drop into `/computescores` and `/runsegmentation` directly (both will stamp outputs SYNTHETIC). But `/generatevalueprop`, `/buildroadmap`, `/outcometospec`, `/choosestrategy` will refuse — they require real-data validation.

---

Invoke the `run-synthetic-survey` skill. Default n_personas to 10 (up from 6). Always surface the sample-size honesty disclosure in the response. Always end with the two upgrade options. Stamp SYNTHETIC. Delegate to the 4 subagents in sequence.
