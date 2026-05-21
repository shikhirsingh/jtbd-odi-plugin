---
description: Identify the three ODI customer types (executor / lifecycle / buyer) for your job. Critical for B2B — skipping the buyer is how most B2B ODI engagements fail. (Ch 5)
argument-hint: "[--job \"<locked job statement>\"] [--context \"B2B SaaS | B2C consumer | medical device | …\"]"
---

# /identifycustomers — Who do I interview?

Invoke the `identifycustomers` skill.

Required input:
- The locked job statement (from /definejob; if missing, ask the user or invoke /definejob first)
- Market context (B2C / B2B / hybrid; industry; rough price point)

The skill asks 2–3 follow-ups to decide whether the executor / lifecycle / buyer are three different people or collapse to one.

For B2B with purchase price > $5k, the skill refuses to skip the buyer — that's where most engagements fail.
