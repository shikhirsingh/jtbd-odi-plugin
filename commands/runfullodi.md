---
description: "MASTER ORCHESTRATOR. Run every phase of an ODI engagement end-to-end (Phase I → VII, Ch 29). Two modes: `real` (pauses for human interviews + survey fielding) or `rehearsal` (synthetic respondents, stamped SYNTHETIC). Guarantees all six Table 30.1 artifacts + all seven front-matter capabilities. Aliases: /fullodi."
argument-hint: <initial input — draft job statement, product description, or business context> [--mode real|rehearsal]
---

# /runfullodi (aka /fullodi) — Run the entire engagement

## What this is doing (plain English)

This is the one command that walks you through the whole ODI method — every phase, every gate, every artifact — from "I have an idea" to "here are the six deliverables a team can act on."

It runs each sub-skill in the right order, validates between phases, and ends with `/createodicanvas` + `/exportdeliverables`. If any required prior step hasn't been done, it pauses and prompts you.

## The two modes

| Mode | What happens | Use when |
|---|---|---|
| **`real`** (default) | Calls every sub-skill but **pauses at human-action checkpoints** — recruiting interviews, fielding the survey, picking the target segment. Total wall-clock: 4–8 weeks. Decision-grade output. | Real engagement with budget for n=300+ survey |
| **`rehearsal`** | Replaces recruiting + fielding with `/run-synthetic-survey`. Total wall-clock: 30–60 minutes. Every output stamped SYNTHETIC. **Cannot be used to make decisions.** | Hypothesis generation, instrument stress-testing, team training |

If you don't pass `--mode`, the skill assumes `real` and asks before proceeding.

## What you need before running this

Just an initial input — could be a draft job statement, a product description, or a paragraph about the business problem. Examples:

- `"I want my customers — tradesmen who use power saws — to cut wood faster and safer"`
- `"We make wireless earbuds for runners; can't decide which features for v2"`
- `"Help my customers listen to music while on the go"`

The skill will prompt you for everything else (interview transcripts, competitors, reason-to-believe, cost constraints) at the right time.

## What you'll get back

After completion: a `deliverables/` folder + zip containing all six Table 30.1 artifacts + Canvas + exec summary + coverage report.

A phase-by-phase log showing what was produced at each checkpoint.

A coverage table showing both:
- ✅ Each of the 6 artifacts present
- ✅ Each of the 7 front-matter capabilities enabled

## The 7 phases

```
I.   Initiate              — /preflight → /definejob → /identifycustomers → /buildjobmap
II.  Uncover Needs         — /generatescreener → (recruit + interview) → /extractoutcomes ×N → /netoutcomes → /validateoutcomes → /hypothesizecomplexity
III. Quantify              — /generatesurvey → (pilot + field) → /computescores
IV.  Discover Hidden       — /runsegmentation → /competitiveanalysis
V.   Market Strategy       — /choosestrategy → /generatevalueprop
VI.  Product Strategy      — /buildroadmap → /outcometospec ×N
VII. Hand-off              — /createodicanvas → /exportdeliverables
```

## Hard guarantees

- Cannot declare success unless all 6 artifacts are present + all 7 capabilities are enabled
- In `real` mode, pauses for interviews and survey fielding — never silently substitutes synthetic
- In `rehearsal` mode, stamps SYNTHETIC on every output
- Refuses to proceed past Phase V if `/choosestrategy` places you in the Discrete cell (trap)
- Gates: `/generatesurvey` requires `/validateoutcomes` to pass

## What runs after this

Once the deliverables are shipped to stakeholders — schedule the 6-month post-launch `/computescores` re-run to measure success against artifact 6.

---

Invoke the `runfullodi` skill. If user pastes just a few words, ask for context before defaulting to real mode. Walk every phase. Surface every gate. Pause at human checkpoints in real mode; never silently substitute synthetic. End with `/exportdeliverables` and surface the coverage table.
