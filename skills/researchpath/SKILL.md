---
name: researchpath
description: A complete ODI engagement that REPLACES customer interviews with thorough online research, then fields a REAL n=300-600 survey on the mined outcomes. Output is decision-grade because the survey is real — only the candidate-discovery phase is shortened. Decision-grade where /run-synthetic-survey is hypothesis-only. Use when you have a job with an active online community (B2C, prosumer, developer tools) but can't recruit 20-30 interview participants in your timeline.
when_to_use: User explicitly says they want to skip interviews but still ship decision-grade outcomes. Triggered by /researchpath, "online research instead of interviews", "skip interviews", "no time for interviews but I want real data", "research-driven survey", "online research then survey".
trigger_phrases:
  - /researchpath
  - /onlinepath
  - /skipinterviews
  - "online research instead of interviews"
  - "skip interviews"
  - "no time for interviews"
  - "research-driven survey"
  - "online research then survey"
  - "I can't recruit interviewees but I want real data"
  - "research-only path"
inputs:
  - locked job statement (from /definejob or /brainstormjob)
  - target source list for online mining (defaults: reddit, amazon, app-store, quora)
  - whether budget exists for a real n=300-600 survey (yes/no — if no, route to /run-synthetic-survey instead)
outputs:
  - the full six Table 30.1 artifacts, decision-grade
  - explicit "this engagement used online research instead of interviews" note in the canvas + exec summary
  - data-provenance flag: `mixed_research_real_survey` — distinct from `synthetic` and from `interviews_plus_survey`
chains_to:
  - /exportdeliverables (the bundle)
delegates_to:
  - /mineoutcomes (heavy lifting on the discovery phase)
  - /netoutcomes, /validateoutcomes
  - /hypothesizecomplexity (from mined data, not interviews)
  - /generatescreener, /generatesurvey (REAL survey instrument)
  - human fielding (real respondents, n=300-600)
  - /computescores, /runsegmentation, /competitiveanalysis
  - /choosestrategy, /generatevalueprop, /buildroadmap, /outcometospec
  - /createodicanvas
---

# /researchpath — Skip the interviews, keep the rigor

## Plain-English preamble

> The handbook says: collect outcomes from 20–30 customer interviews, then field a survey to n=300–600 real respondents. Both phases matter — interviews discover the candidates; the survey gives statistical validity.
>
> **What if you can't recruit interview participants?** Common cases:
> - B2C product with millions of users who don't answer cold outreach
> - Pro-sumer / developer / hobbyist market where the conversation already happens publicly (Reddit, forums, Discord, GitHub)
> - 4-week timeline that doesn't allow scheduling 20+ interviews
>
> **You can substitute thorough online research for the interview phase** — Reddit, app-store reviews, Amazon reviews, forums, Quora, support ticket exports, customer-success transcripts. The mined data feeds /netoutcomes and /validateoutcomes just like interview data would.
>
> Then you field a **REAL survey** to n=300–600 real respondents. **That part is non-negotiable** — without it you don't have decision-grade scoring; you have a hypothesis.
>
> **This orchestrator IS decision-grade** because the survey is real. It's just the discovery phase that's shortened. The output's data-provenance flag is `mixed_research_real_survey` so artifacts make the substitution transparent.

## When this fits — and when it doesn't

| Situation | researchpath fits? |
|---|---|
| B2C app, active subreddit, app-store reviews available | ✅ Strong fit |
| Developer tools, GitHub discussions + Reddit + Stack Overflow | ✅ Strong fit |
| Prosumer hardware (audio, kitchen, fitness) with Amazon + niche forums | ✅ Strong fit |
| B2B SaaS where users post on Reddit + G2 + Trustpilot | ✅ OK fit (still better with 5–10 interviews if possible) |
| Enterprise / healthcare / regulated industries | ❌ Use full path — interviews are essential. Online data is too thin and selection-biased. |
| Niche B2B with no public conversation about the job | ❌ Use full path |
| You can recruit 20+ interviewees easily | ❌ Just use `/runfullodi` — interviews are richer than mining |

If the user is in the "doesn't fit" column, route them to `/runfullodi` or `/runliteodi`.

## The orchestration

```
/researchpath  (user provides locked job statement + confirms survey budget)
   │
   ├── Phase 0 — Eligibility check
   │     → confirm online research is actually viable for this job
   │     → if not: route to /runfullodi or /runliteodi
   │
   ├── Phase I — Customer types (still matters)
   │     → /identifycustomers (especially for B2B)
   │
   ├── Phase II — DISCOVERY (online instead of interviews)
   │     → /mineoutcomes — thorough pass; 500-800 candidates from 5+ sources
   │     → /hypothesizecomplexity --from-mined mined-outcomes.csv
   │     → /netoutcomes — same dedupe + clean process; aim for 60-120 outcomes
   │     → /validateoutcomes — same hard gate; refuse on `fail`
   │
   ├── Phase III — QUANTIFY (real survey — non-negotiable)
   │     → /generatescreener + /generatesurvey
   │     → human pilot (n=10-15)
   │     → human fielding to n=300-600 real respondents
   │     → /computescores on the real CSV
   │
   ├── Phase IV — ANALYZE (decision-grade)
   │     → /runsegmentation
   │     → /competitiveanalysis
   │
   ├── Phase V — STRATEGY
   │     → /choosestrategy
   │     → /generatevalueprop
   │
   ├── Phase VI — EXECUTE
   │     → /buildroadmap
   │     → /outcometospec ×N
   │
   └── Phase VII — PACKAGE
         → /createodicanvas (stamped "research-driven discovery + real survey")
         → /exportdeliverables (data_provenance: "mixed_research_real_survey")
```

## What's gained, what's lost vs. classic interviews

### What's gained
- 2–3 weeks shaved off Phase II (no recruiting, no scheduling, no transcription)
- Broader sampling — mining hits 500+ public posters vs. 20–30 interviewees
- Pre-existing context — public posts are often more candid than interview answers (people aren't being recorded by a researcher)

### What's lost
- **Extreme-user outcomes** — the lead/lag users that don't post publicly. Critical in some categories (industrial, specialty). Acceptable in B2C / prosumer.
- **Probing follow-ups** — an interviewer can ask "tell me more about that" — mining can't.
- **Buyer perspective in B2B** — public posts are mostly executors. Buyers don't blog about TCO. **If B2B, do 5–8 buyer interviews even on the researchpath.**

The skill must surface these tradeoffs explicitly in Phase 0.

## How to run

### Phase 0 — Eligibility check (interactive)

```
Before I run /researchpath, three quick checks:

1. Is your category publicly discussed online?
   Examples of YES: B2C apps, developer tools, prosumer hardware
   Examples of NO:  enterprise compliance tools, specialty medical, niche B2B

   → If NO, run /runfullodi instead. Mining will be too thin.

2. Do you have budget + timeline for a real n=300-600 survey?
   (Typically $5k-25k panel cost, 2-3 weeks fielding.)

   → If NO, run /run-synthetic-survey instead (hypothesis-only path).

3. Is this B2B?
   → If YES, you'll still want 5-8 BUYER interviews even on researchpath.
     Mining captures executors well; buyers don't post publicly.
     I'll add this as an explicit hybrid step.
```

If all three check out, proceed. Otherwise reroute.

### Phase II — Mine thoroughly (this is where the research depth matters)

Default `/mineoutcomes` quotas for researchpath are HIGHER than for hypothesis-only runs:

| Source | Default cap | researchpath cap |
|---|---|---|
| Reddit | 200 | **500** |
| Amazon reviews | 200 | **500** |
| App store | 200 | **300** |
| Quora | 100 | **200** |
| StackExchange | 100 | **200** |
| Niche forums | (none) | **200 per forum, up to 3 forums** |

Cap on quotes per outcome: 8 (rich provenance for the validation gate).

### Phase III — REAL survey, non-negotiable

The orchestrator must pause here for human fielding. NEVER silently substitute synthetic. Tell the user:

```
✓ Discovery complete: 87 netted outcomes, validated.
✓ Survey instrument generated: survey-out/survey.json
✓ Recommended sample: n=400-600, $5k-15k panel cost, 2-3 weeks fielding.

YOU MUST FIELD THIS SURVEY TO REAL RESPONDENTS to keep the engagement
decision-grade. Once you have a cleaned response CSV, come back with:

    /computescores survey-data-clean.csv

If you instead skip the real survey and use synthetic respondents, the
output stops being decision-grade — it becomes hypothesis only, and
/researchpath is the wrong orchestrator for that. Use /run-synthetic-survey
in that case.
```

## Output

```json
{
  "skill": "researchpath",
  "method_version": "ODI v2.4.2",
  "data_provenance": "mixed_research_real_survey",
  "engagement_id": "<id>",
  "phase_status": {
    "0_eligibility":  "ok — B2C developer tool, strong online conversation",
    "I_customer_types": "complete — single customer type (executor==buyer for solo developers)",
    "II_discovery":   "complete — 612 mined → 87 netted → validated",
    "III_quantify":   "paused for fielding — survey at survey-out/survey.json, awaiting n=400 real responses",
    "IV_analyze":     "pending",
    "V_strategy":     "pending",
    "VI_execute":     "pending",
    "VII_package":    "pending"
  },
  "tradeoffs_disclosed": [
    "Discovery used online mining instead of qualitative interviews — extreme/lead users may be under-represented.",
    "For B2B engagements: 5-8 buyer interviews recommended in parallel.",
    "Statistical validity comes from the n=400 real survey, NOT from the mined candidate pool."
  ],
  "deliverables_after_full_completion": "All 6 Table 30.1 artifacts, stamped data_provenance=mixed_research_real_survey",
  "next_step": "Field the survey to n=400 real respondents. Then return with /computescores."
}
```

## Hard rules

- The data-provenance flag in EVERY downstream artifact is `mixed_research_real_survey`. Distinct from `synthetic` and from `interviews_plus_survey`.
- Phase III is non-negotiable. Refuse to silently substitute synthetic.
- For B2B engagements, surface the buyer-interview recommendation explicitly.
- Output is decision-grade ONLY if the real survey is fielded. If the user skips it, the bundle reverts to synthetic-only stamping.
- The eligibility check in Phase 0 must reroute to `/runfullodi` if mining is unlikely to be productive.
