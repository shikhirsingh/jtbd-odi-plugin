---
name: preflight
description: Run Ulwick's pre-flight checklist (Chapter 4). Determines whether ODI is the right tool for the situation in front of the user, BEFORE they commit time/budget. Asks 6 diagnostic questions and returns a go/no-go with explicit reasoning. Saves teams from spending 8 weeks on the wrong method.
when_to_use: User is considering ODI but hasn't committed. Triggered by "/preflight", "/odicheck", "is ODI right for this", "should I do ODI", "is this worth doing". Also invoked as step 5 of Phase I in /runfullodi.
trigger_phrases:
  - /preflight
  - /odicheck
  - "should I do ODI"
  - "is ODI right for this"
  - "is this worth doing ODI for"
  - "is this the right method"
  - "is ODI overkill"
  - "do I really need a survey"
  - "is this method overkill for me"
  - "we don't have budget for"
  - "we don't have time for"
  - "can I skip the survey"
  - "should we use ODI or"
inputs:
  - free-form description of the situation (problem the team is trying to solve, what's already known, time/budget constraints)
outputs:
  - go / no-go / lite verdict
  - per-criterion green/yellow/red against the Ch 4 checklist
  - if no-go: a recommended alternative method (CustDev / Lean Startup tests / classical market research / etc.)
  - if go: which entry point in the plugin to use (full / lite / rehearsal)
chains_to:
  - /odihelp (if user wants more nav after the verdict)
  - /definejob (if verdict = go)
  - /runliteodi (if verdict = lite)
---

# /preflight — Should you even do ODI?

> **Plain English:** ODI is powerful but it isn't always the right tool. Some problems don't need a $40k survey; some need something different entirely. This skill walks you through Tony Ulwick's Chapter 4 checklist and tells you honestly whether ODI fits your situation — *before* you spend the time and money.

## What this is doing

Ulwick is explicit that ODI is the right tool in some situations and the wrong tool in others. This skill scores your situation against his criteria. You answer 6 short questions; you get back a go / no-go / lite recommendation with reasoning.

## What you need before running this

Just a paragraph describing your situation. For example:

> "I'm a seed-stage founder building a B2B SaaS tool for HR teams to onboard remote employees. We've done 8 customer-discovery calls but no quantitative work. Budget for research is ~$15k. Timeline: I need direction in 4 weeks because we're choosing v1 features."

The skill will extract the relevant signals from that paragraph and may ask 1–2 follow-up questions.

## The 6 Ch 4 criteria

| # | Question | Green | Yellow | Red |
|---|---|---|---|---|
| 1 | **Is the problem at the front end of innovation?** (deciding what to build, not how to build it) | ✅ Yes — picking features, segments, positioning | 🟡 Mixed — some build, some discover | ❌ No — we already know what to build; we just need to ship faster |
| 2 | **Is there a stable, well-defined functional job?** | ✅ Yes — customers are clearly trying to accomplish X | 🟡 Sort of — the "job" is broad or fuzzy | ❌ No — pure new category with no analog |
| 3 | **Are there ≥ 5 million potential job executors?** (market size sanity check) | ✅ Yes | 🟡 Niche but defensible | ❌ Very thin market |
| 4 | **Do you have budget for n=300+ survey + 20–30 interviews?** (typical: $20k–$80k) | ✅ Yes — Full ODI | 🟡 Partial — Lite ODI only | ❌ No — alternative method or rehearsal only |
| 5 | **Do you have time for 4–8 weeks?** | ✅ Yes — Full ODI | 🟡 2–3 weeks — Lite ODI | ❌ < 2 weeks — alternative |
| 6 | **Will leadership respect the data when it conflicts with their gut?** | ✅ Yes — written commitment exists | 🟡 Probably | ❌ No — politics will override the data; don't waste the money |

## Where ODI clearly outperforms alternatives (Ch 4)

- Picking which **features** to ship on a roadmap that's drowning in candidates.
- Finding the **beachhead segment** in a fragmented market.
- Re-pricing in a market where your category-priced anchor is wrong.
- Setting **engineering acceptance criteria** ("how do we know we're done?").

## Where ODI is the wrong tool (Ch 4)

| Situation | Better tool |
|---|---|
| Pure new category, no analog (no one is even doing this yet) | Customer-discovery interviews + smoke tests (Lean Startup) |
| Pure UX / interaction design problem | Usability testing, design research |
| Build-quality / engineering velocity problem | DORA / engineering metrics |
| Brand / creative positioning without a functional job underneath | Brand research, semiotic analysis |
| You already know the job AND the outcomes; you just can't execute | Operations and project management |

## Output

```json
{
  "skill": "preflight",
  "method_version": "ODI v2.4.2",
  "verdict": "go | lite | rehearsal_only | no_go",
  "scores": [
    {"criterion": "front_end_of_innovation",      "score": "green",  "note": "User is choosing v1 features — front-end."},
    {"criterion": "stable_functional_job",        "score": "green",  "note": "Onboarding remote employees is a stable job."},
    {"criterion": "market_size",                  "score": "yellow", "note": "B2B HR — defensible but not massive; sample-size cost may be high."},
    {"criterion": "budget_for_full_quant",        "score": "yellow", "note": "$15k is short of full Full ODI; covers Lite or a small pilot."},
    {"criterion": "time_available",               "score": "yellow", "note": "4 weeks is tight for Full; Lite fits comfortably."},
    {"criterion": "leadership_will_respect_data", "score": "green",  "note": "Founder is single decision maker."}
  ],
  "recommendation": "Run Lite ODI now (/runliteodi). Plan a follow-up Full survey at Series A when budget grows.",
  "reasoning": "All criteria are green or yellow — no red. But your $15k budget + 4 week timeline doesn't fit Full ODI's panel costs and fielding window. Lite ODI gives you a directional read in 2–3 weeks; once you've validated direction with Lite, you can field a smaller, more targeted survey later.",
  "alternative_if_no_go": null,
  "next_step": "/runliteodi  (or /definejob if you want to start manually and decide later)."
}
```

## Hard rules

- The skill does not flatter the user. If the answer is "this isn't an ODI problem", it says so.
- Two reds → automatic no-go.
- One red on **criterion 6** (leadership won't respect the data) → automatic no-go with a "fix the political problem first" recommendation.
- Yellow on budget/time but no reds → recommend `/runliteodi`.
- All greens + adequate budget/time → recommend `/runfullodi --mode real`.
- Zero context provided → ask the user the diagnostic questions explicitly rather than guessing.
