---
description: STEP 1 — Write the one-sentence functional job statement. Verb + object + optional clarifier. Validates against Ulwick's 5 rules and 3 stability checks. (Ch 6)
argument-hint: <a draft job statement OR a product description OR just a problem you're trying to solve>
---

# /definejob — Step 1 of an ODI engagement

## What this is doing (plain English)

It's writing the single most important sentence in your project: **what the customer is trying to get done**.

You'd think this is easy. It isn't. Most teams get it wrong the first three tries because they smuggle in product names, emotions, situations, or company perspective. ODI is uncompromising here — get this sentence wrong and every downstream step (the survey, the scores, the strategy) is contaminated.

This skill writes the candidate sentence, scores it against Ulwick's 5 rules + 3 stability checks, and iterates with you until it passes.

## What you need before running this

Just describe your situation. Any of these works as input:
- A draft job statement: `"I want to help people listen to music while on the go"`
- A product description: `"We make wireless earbuds for runners"`
- A problem: `"My customers can't figure out which playlist to use"`

If you give nothing, the skill will ask.

## What you'll get back

- One clean job statement in strict syntax (verb + object + clarifier)
- A scorecard against the 5 rules and 3 stability checks (pass/fail per rule, with reasoning)
- 1–3 alternative framings at different levels of abstraction (narrower / broader) — so you can pick the right altitude
- Status: `draft` (keep iterating) or `locked` (ready for the next step)

Plan to iterate 3–10 times. The skill won't lock prematurely.

## Jargon you'll see

- **Verb + object + clarifier** — the strict format. "Listen to music while on the go." Not "music-listening" (noun); not "listen quickly to music" (adjective); not "use my app to listen" (smuggled solution).
- **Stability check** — does the statement still make sense in 20 years (no current tech), across countries, regardless of solution?
- **Functional job** — purely about what the customer is doing, stripped of emotions/social desires/situations.

## What runs after this

Once status = `locked`, the skill will tell you to run:
- `/identifycustomers` next (especially for B2B — three customer types matter)
- then `/buildjobmap`

---

Invoke the `definejob` skill with whatever the user provided. After every iteration, print the rules-check table and abstraction alternatives. If user input is missing or only a single word, ASK for context rather than guessing the job.
