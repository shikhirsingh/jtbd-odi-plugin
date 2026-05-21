---
description: HARD GATE — Validate the netted outcomes against Ulwick's 10 characteristics + Table 11.4 variability strips. /generatesurvey refuses to run if this verdict is `fail`. (Ch 11)
argument-hint: <path to netted-outcomes.csv from /netoutcomes>
---

# /validateoutcomes — The quality gate before the survey

## What this is doing (plain English)

You spent weeks netting 50–150 outcomes. Before you spend $40k fielding a survey on them, this skill checks every outcome against Ulwick's 10 quality characteristics (Ch 11, Table 11.2). One bad outcome = noisy data on that row, and you can't fix it after fielding.

It's a hard gate. `/generatesurvey` won't proceed if any outcome `fails` validation.

## What you need before running this

- The netted outcomes CSV (from `/netoutcomes`)

That's it. If you give the skill a path that doesn't exist, it'll ask.

## What you'll get back

- **A verdict**: `pass` / `conditional` / `fail`
- **A per-outcome scorecard** with 10 boolean columns + 5 variability-sin columns + severity (ok / warn / fail)
- **Suggested rewrites** for any failing outcomes (you choose to accept or modify)
- **Duplicate alerts** — pairs of outcomes the embedding model thinks might be duplicates (you decide if they should merge)

If you get a `fail`, the report tells you exactly which outcomes are broken and the suggested fix. Make the fix, re-net, re-validate. Loop until `pass` or `conditional`.

## The 10 characteristics being checked

1. **Stable over time** — still meaningful in 20 years (no current tech)
2. **Reveals a metric** — time / likelihood / frequency / etc.
3. **Devoid of solutions** — no product/brand/technology names
4. **Measurable**
5. **Controllable** (by the executor or product team)
6. **Actionable** (engineer/designer can attack it)
7. **One-dimensional** (no compound statements)
8. **Mutually exclusive** (no duplicates on the list)
9. **Customer-stated value**
10. **Useful across functions** (PM / marketing / engineering / sales)

## What runs after this

If `pass` or `conditional` → `/generatesurvey`
If `fail` → fix the failures, re-run `/netoutcomes` if needed, then re-run `/validateoutcomes`.

---

Invoke the `validateoutcomes` skill. Runs `python scripts/outcome_validator.py --outcomes <csv> --out validation-out/`. Prints the verdict + the failing outcomes prominently. If user tries to jump straight to `/generatesurvey` without running this, refuse.
