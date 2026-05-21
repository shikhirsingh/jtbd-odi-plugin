---
description: Build the recruiting screener — the 5–10 questions a panel provider will use to filter for real job-executors / buyers / lifecycle-support people. Includes incidence estimate, quota plan, and incentive recommendation. (Ch 9 + Ch 15/18)
argument-hint: "[--customer-type executor|buyer|lifecycle] [--audience \"<description>\"]"
---

# /generatescreener — Who you're recruiting + how

## What this is doing (plain English)

Before you can interview or survey anyone, you need a **screener** — the 5–10 questions that filter out anyone who doesn't actually do the job, plus anyone who works for a competitor or won't pass an attention check.

In B2B you'll typically need **three different screeners** — one for each of the three customer types (executor / lifecycle support / buyer). They are NOT interchangeable.

This skill builds the screener including:
- The filter questions
- An estimated incidence rate (% of panel members who'll qualify)
- A quota plan (so you get enough completes per likely segment)
- Recommended incentive amount

## What you need before running this

- Your **locked job statement** from `/definejob`
- The **customer type** (executor / lifecycle / buyer — from `/identifycustomers`)
- An **audience description** (B2C consumer / B2B specialist / clinician / etc.)
- Optionally: named competitors for the "do you use…" routing logic

If the customer type isn't specified, the skill assumes executor and warns. If you're in B2B, run `/identifycustomers` first.

## What you'll get back

- `screener.md` (human-readable, paste into Qualtrics/Typeform)
- `screener.json` (machine schema)
- **Incidence estimate** — how many raw recruits the panel provider needs per qualified completion (often 5–10×)
- **Quota plan** — recommended distribution across hypothesized segments
- **Incentive recommendation** — per-completion $ band per Ch 18 (consumer: $5–25, B2B: $25–100, specialist: $100–500)

## What runs after this

If you're in real mode: hand the screener to your panel provider for a soft-launch of n=50. Then field the full sample.

After the survey is fielded, the next plugin step is `/computescores`.

---

Invoke the `generatescreener` skill. If `--customer-type` is missing, ask the user explicitly before generating — wrong screener for the wrong customer type is one of the most expensive mistakes in ODI. For B2B with purchase price > $5k, suggest running `/identifycustomers` first.
