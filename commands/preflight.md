---
description: Ulwick's pre-flight checklist (Ch 4) — should you even do ODI? Saves teams from spending 8 weeks on the wrong method.
argument-hint: <free-form paragraph describing your situation, OR no args for interactive prompts>
---

# /preflight — Is ODI right for this?

Invoke the `preflight` skill.

Required input from the user:
- Their problem in 1 paragraph (what are they trying to decide?)
- Budget for research (rough $ range)
- Timeline (weeks until decision)

If any of those are missing, ASK before scoring. Don't fake-score on missing info.

Return: verdict (`go` / `lite` / `rehearsal_only` / `no_go`) + per-criterion green/yellow/red against Ch 4 + next-step command.

Be honest. If ODI isn't the right tool, say so and recommend an alternative.
