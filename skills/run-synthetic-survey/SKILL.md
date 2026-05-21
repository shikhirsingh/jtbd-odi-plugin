---
name: run-synthetic-survey
description: ONE-COMMAND ORCHESTRATOR. For a given job, run the full synthetic pipeline — mine public data → hypothesize complexity factors → synthesize 5–8 grounded personas → have each persona "take" an ODI survey (importance + satisfaction + profiling) → output a synthetic_survey.csv that drops straight into /computescores and /runsegmentation. SYNTHETIC — generates hypotheses, NEVER replaces n=300–600 real respondents.
when_to_use: Founder or product team wants a fast, evidence-anchored first cut on opportunity scoring and segmentation before commissioning real research. Triggered by "/run-synthetic-survey", "synthetic survey", "virtual respondents", "fake the survey".
trigger_phrases:
  - /run-synthetic-survey
  - "synthetic survey"
  - "virtual respondents"
  - "run the synthetic pipeline"
inputs:
  - the locked job statement (verb + object + clarifier)
  - optional: existing netted-outcomes.csv (otherwise the orchestrator runs /mineoutcomes + /netoutcomes internally)
  - n_personas (DEFAULT 10; range 6–20). Higher persona count = more archetype-level distinctions. Statistical power is bounded by persona count, NOT by row count.
  - n_responses_per_persona (default 60; range 30–120). Adds within-persona variation; does NOT add independent observations.

  > **⚠️ Sample-size honesty (read this).** Tony Ulwick's method requires n=300–600 REAL respondents because each is an independent observation drawn from the actual population. A synthetic run with 10 personas × 60 rows = 600 rows, but statistically you have **10 archetype-level signals**, not 600. The 60-row spread per persona is noise around the persona's locked biases — it does not give you statistical power. /computescores will compute opportunity scores normally, but the resulting numbers reflect persona design choices, not a real population distribution.
  >
  > If decision-grade output matters, use **/researchpath** (real n=300-600 survey on mined outcomes) or **/runfullodi --mode real** (real interviews + real survey). /run-synthetic-survey is hypothesis-only.
outputs:
  - personas.json (the 5–8 grounded personas)
  - synthetic_survey.csv (the exact schema /computescores expects)
  - mined-outcomes.csv + source-evidence.md (if mining was run)
  - hypothesis-summary.md (what to do next)
  - SYNTHETIC banner stamped on every artifact
chains_to:
  - /computescores
  - /runsegmentation
  - /createodicanvas (canvas stamped SYNTHETIC)
  - /exportdeliverables (rehearsal bundle stamped SYNTHETIC; capability coverage report still produced)
refuses_to_chain_to_without_real_data:
  - /generatevalueprop
  - /buildroadmap
  - /outcometospec
  - /choosestrategy
delegates_to:
  - agent: data-miner
  - agent: outcome-formatter
  - agent: persona-synthesizer
  - agent: virtual-respondent (one invocation per persona)
helpers:
  - scripts/mine_sources.py
  - scripts/synthetic_survey_generator.py
  - scripts/survey_generator.py
  - scripts/opportunity_scorer.py
  - scripts/canvas_generator.py
  - scripts/deliverables_exporter.py
---

# /run-synthetic-survey — The Virtual Respondent Panel

## Plain-English preamble (for newcomers)

> One command. End-to-end synthetic ODI pipeline. For a given job statement:
>
> 1. Mines public data (Reddit, app store reviews, Amazon, Quora, …)
> 2. Nets and validates the mined candidates
> 3. Hypothesizes complexity factors
> 4. Synthesizes 5–8 grounded personas (each anchored in ≥2 verbatim public quotes)
> 5. Builds the full survey instrument
> 6. Has each persona "take" the survey via N sampled draws
> 7. Outputs a CSV in the exact schema `/computescores` expects
>
> **Wall-clock: 30–60 minutes.** Cost: LLM tokens only.
>
> **What it is NOT:** a replacement for the real survey. Synthetic survey data reflects LLM training biases, not market reality. Use it for hypothesis generation, instrument stress-testing, and prioritizing real-interview recruitment. **Cannot drive roadmap, pricing, or value-prop decisions.**
>
> Plain-English alias: `/synthsurvey`. The skill refuses to chain `/generatevalueprop`, `/buildroadmap`, `/outcometospec`, or `/choosestrategy` from synthetic data.

---

> ⚠️⚠️ **SYNTHETIC ACCELERATOR. NEVER A SUBSTITUTE FOR THE REAL SURVEY.** ⚠️⚠️
>
> The ODI handbook is explicit (Part IV, *What AI does NOT replace*):
> *"Do not use an LLM to simulate survey respondents. Synthetic survey data looks plausible and is dangerous: it tells you what the LLM thinks a customer would say, not what real customers actually rate."*
>
> This orchestrator runs that exact thing — *but only as a hypothesis generator*. Its outputs:
>
> - Are stamped SYNTHETIC on every file.
> - Use `opp_hypothesis` rather than `opp` in the schema.
> - Carry classifications suffixed `_HYPOTHESIS`.
> - Include an explicit "next step: validate with n ≥ 300 real respondents" instruction.
>
> Use this to:
> 1. **De-risk** the survey instrument before fielding (does the schema generate sensible numbers? Are there outcomes everyone "rates the same"? Probably a bad question).
> 2. **Prioritize interview lists** — which personas are most worth recruiting first.
> 3. **Stress-test** segmentation pipelines (does the synthetic data segment into interpretable groups? If not, refine complexity factors).
> 4. **Generate board-ready directional views** while the real survey is in field.
>
> Use this NOT to:
> - Justify any roadmap, pricing, or value-prop decision.
> - Replace real interviews or the n=300–600 fielded survey.

---

## ⚠️ What "n" actually means in a synthetic run

Before you run this, internalize this:

| What you'd hope it means | What it actually means |
|---|---|
| "I have 600 simulated respondents" | "I have 10 distinct archetypes, each repeated 60 times with noise" |
| "Equivalent to a real n=600 survey" | NOT equivalent. Real surveys draw 600 independent people from the actual population distribution. Synthetic draws 10 LLM-designed archetypes. |
| "Strategyn-style decision-grade scoring" | Hypothesis-grade only. Use it to inform what the real survey should ask, not to make roadmap or pricing decisions. |

**Why this matters in practice:** Suppose your real population has a long tail of unusual users with distinct unmet needs. A real n=600 survey will catch them (a few will appear in the sample). A 10-persona synthetic run will NOT — unless the LLM happened to design a persona for them. **Long-tail outcomes are systematically under-counted in synthetic runs.**

### The upgrade path (always offered)

The orchestrator's final output ALWAYS surfaces two upgrade options:

- **`/researchpath`** — keep the online-mining discovery phase, but field a REAL n=300-600 survey instead of synthesizing one. Decision-grade.
- **`/runfullodi --mode real`** — full method, with real interviews AND real survey.

If the user persists with synthetic and tries to chain `/generatevalueprop`, `/buildroadmap`, `/outcometospec`, or `/choosestrategy` downstream, those skills REFUSE and offer the upgrade path.

## The orchestration

```
/run-synthetic-survey "<job statement>"
   │
   ├── 1. Confirm job & job map (calls /definejob + /buildjobmap if missing)
   │
   ├── 2. Mine public data            ── agent: data-miner
   │        ↓
   ├── 3. Net candidates             ── agent: outcome-formatter
   │        ↓                          (calls /netoutcomes internally)
   ├── 4. Hypothesize complexity factors  (calls /hypothesizecomplexity)
   │        ↓
   ├── 5. Synthesize 10 personas      ── agent: persona-synthesizer
   │        ↓   each grounded in ≥3 mined posts; spread across complexity-factor space
   │
   ├── 6. Build the survey            (calls /generatesurvey internally)
   │        ↓
   ├── 7. Run each persona ×N samples ── agent: virtual-respondent (parallel)
   │        ↓   each generates a top-2-box-compatible 1–5 vector for imp + sat
   │
   ├── 8. Assemble synthetic_survey.csv
   │        ↓   columns identical to what /computescores expects
   │
   └── 9. Stamp SYNTHETIC banner + show the upgrade-to-real-survey CTA prominently
```

## Persona grounding rules (delegated to persona-synthesizer)

Each persona MUST be grounded in real mined data. Each persona has:

- A name (a label, not a real person).
- A complexity-factor vector (5–8 dims, scored on the same scale as the survey profiling questions).
- A short narrative grounded in **2–5 verbatim quotes** from `source-evidence.md`. These quotes are kept attached to the persona for downstream audit.
- A coarse sentiment style ("frustrated power user", "happy occasional user", "skeptical pro", "loyal early adopter", "switcher who left").
- A consistency anchor: a list of importance and satisfaction biases the persona should keep across all 60-ish synthetic responses (e.g., "always rates queue-management outcomes high importance; rates them low satisfaction since they switched from Spotify").

Personas span the complexity-factor space — DO NOT generate 6 personas that are minor variations of the same archetype. The persona-synthesizer is required to maximize cross-persona diversity on the complexity vector.

## Virtual-respondent rules (delegated to virtual-respondent)

Each virtual respondent:

- Receives the persona profile + the survey JSON.
- Produces a JSON line: respondent_id, persona_id, profiling answers, imp_<outcome_id> ratings (1–5), sat_<outcome_id> ratings (1–5), and optional WTP answers.
- Within a persona, samples ratings from a small distribution around the persona's locked biases (so that 60 respondents from the same persona produce a believable spread, not 60 identical rows).
- For any outcome where the persona has no grounded basis to rate (no related mined quotes, no plausible inference), returns a "don't_know" flag.

Result: n_personas × n_responses_per_persona total rows, with persona_id retained so analysis can audit which persona drives any cluster.

## Output schema (matches /computescores)

```csv
respondent_id,persona_id,screener_pass,quality_flag,
profile_commute_min,profile_listening_env,profile_offline_pct,...,
imp_D-01,imp_D-02,...,imp_C-04,
sat_D-01,sat_D-02,...,sat_C-04,
wtp_q1,wtp_q2,wtp_q3
SYN-0001,P-01-frustrated_commuter,1,,42,quiet_transit,40,...,5,4,...,2,1,...,12,15,4
SYN-0002,P-01-frustrated_commuter,1,,55,quiet_transit,55,...,5,5,...,1,2,...,18,22,5
...
```

Note: `quality_flag` is always blank for synthetic respondents (no real-data fraud risks). Real surveys use this column; we leave it for compatibility.

## Output

```json
{
  "skill": "run-synthetic-survey",
  "method_version": "ODI v2.4.2",
  "data_provenance": "SYNTHETIC — directional only, do not ship",
  "job_statement": "Listen to music while on the go",
  "pipeline_steps": [
    {"step": "mine", "skill": "/mineoutcomes", "candidates_extracted": 134},
    {"step": "net", "skill": "/netoutcomes", "netted_outcomes": 88},
    {"step": "hypothesize_complexity", "skill": "/hypothesizecomplexity", "factors": 9},
    {"step": "personas", "agent": "persona-synthesizer", "n_personas": 6},
    {"step": "survey_build", "skill": "/generatesurvey", "items": 88, "length_minutes_est": 28},
    {"step": "respondents", "agent": "virtual-respondent", "n_respondents": 360}
  ],
  "personas": [
    {"id": "P1", "label": "Long-commute audiophile switcher", "n_responses": 60, "grounded_quotes": 4},
    {"id": "P2", "label": "Gym-first sweat-resistant fan",     "n_responses": 60, "grounded_quotes": 3},
    {"id": "P3", "label": "Driver who wants glanceable controls", "n_responses": 60, "grounded_quotes": 5},
    {"id": "P4", "label": "Occasional walker, satisfied with default", "n_responses": 60, "grounded_quotes": 3},
    {"id": "P5", "label": "Multi-device power user (laptop ↔ phone ↔ TV)", "n_responses": 60, "grounded_quotes": 4},
    {"id": "P6", "label": "Hearing-aid pairing user", "n_responses": 60, "grounded_quotes": 2}
  ],
  "outputs": {
    "personas_json": "synthetic-out/personas.json",
    "synthetic_survey_csv": "synthetic-out/synthetic_survey.csv",
    "mined_outcomes_csv": "synthetic-out/mined-outcomes.csv",
    "source_evidence_md": "synthetic-out/source-evidence.md",
    "hypothesis_summary_md": "synthetic-out/hypothesis-summary.md"
  },
  "guardrails_applied": {
    "synthetic_banner_on_every_artifact": true,
    "schema_uses_opp_hypothesis": true,
    "real_survey_validation_instruction": "Field n>=300 real respondents per ODI v2.4.2 Ch 16 before any decision.",
    "respondent_count_disclaimer": "360 'rows' = 6 personas × 60 sampled variations. NOT 360 real humans."
  },
  "next_steps_hypothesis_only": [
    "Run /computescores synthetic-out/synthetic_survey.csv to see the hypothesized opportunity landscape.",
    "Run /runsegmentation synthetic-out/synthetic_survey.csv to see if the synthetic data clusters into interpretable segments.",
    "Use the result to refine the survey instrument and prioritize which real interviews to commission first."
  ],
  "upgrade_to_decision_grade": [
    {"command": "/researchpath", "what_it_does": "Keep the online mining discovery; field a REAL n=300-600 survey instead of synthesizing. Decision-grade output. 2-3 weeks for fielding.", "cost": "$5k-$15k panel"},
    {"command": "/runfullodi --mode real", "what_it_does": "Full method with real interviews AND real survey. Decision-grade. 4-8 weeks.", "cost": "$20k-$80k"}
  ],
  "sample_size_note": "10 personas × 60 = 600 rows, but statistically you have ~10 archetype-level signals. NOT equivalent to a real n=600 survey. Long-tail outcomes are systematically under-counted."
}
```

## Hypothesis-summary.md template

```
================================================================
⚠️  SYNTHETIC HYPOTHESIS REPORT — DIRECTIONAL ONLY — DO NOT SHIP
================================================================

# /run-synthetic-survey — Hypothesis Report

Job: <job statement>
Generated: <timestamp>
Personas: <n>
Synthetic rows: <n>
Outcomes evaluated: <n>

## ⚠️ What this is and isn't

This report uses LLM-simulated respondents grounded in public online data.
It is NOT a real survey. Treat it as a structured hypothesis.

To produce decision-grade results, field the survey to n >= 300 real
respondents per ODI v2.4.2, Chapter 16. The CSV produced by this
orchestrator drops directly into /computescores, but the resulting
landscape carries `_HYPOTHESIS` classifications, not real scores.

## Top hypothesized opportunities

1. [E-12] Minimize the likelihood of moving off the cut line — opp_h = 13.8 ★
   Grounded in 42 mined quotes; high cross-source agreement.
   Recommend: Probe this outcome heavily in the first 5 real interviews.

[…]

## Hypothesized segments (preview — run /runsegmentation for full output)
- Cluster of personas P1 + P5 → "long-commute power users" — underserved on offline reliability.
- Cluster of P2 + P3 → "in-motion specialists" — underserved on glanceability and environmental fit.
- Cluster of P4 + P6 → "settled / specialty users" — mostly table stakes.

## Recommended next moves
- [ ] Commission 8–12 real qualitative interviews, prioritized as: 4 from P1-like profiles, 2 each from P2/P3/P5.
- [ ] Refine the netted outcome list before fielding — see drop/add suggestions in section 4.
- [ ] Field the real survey to n = 400–600 using the persona-derived screener quotas as targets.
================================================================
```

## Hard rules

- Stamp the SYNTHETIC banner on every artifact, including the CSV.
- Always include the persona_id column in synthetic_survey.csv so analyses can audit which persona is driving which result.
- Personas must each be grounded in ≥ 2 verbatim mined quotes. If grounding fails, the persona is rejected and a new one is generated or that persona slot is dropped.
- Never report the "respondent count" without immediately clarifying it's persona-sampled rows.
- Never call the resulting scores "opportunity scores" — they are "hypothesis opportunity scores."
- If the user attempts to chain /generatevalueprop or /buildroadmap directly off synthetic results, REFUSE and remind them to validate with n ≥ 300 first.
