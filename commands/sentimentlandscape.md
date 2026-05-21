---
description: SYNTHETIC ACCELERATOR — Build a pre-survey "hypothesis opportunity landscape" from public sentiment + mined data. DIRECTIONAL ONLY — never replaces /computescores on real data.
argument-hint: <path to mined-outcomes.csv>
---

# /sentimentlandscape — Pre-survey hypothesis landscape

## What this is doing (plain English)

You've mined public posts about your job. This skill turns those posts into a *hypothesis* about what your real opportunity landscape will look like — before you spend $30k on a panel.

For each candidate outcome it computes:
- A **proxy importance** (frequency, engagement, urgency-language density, cross-source agreement)
- A **proxy satisfaction** (sentiment in posts, workaround complexity, switching language)
- A **hypothesis opportunity score** using the real ODI formula
- A **confidence score** (≥0.7 high; 0.4–0.7 medium; <0.4 don't trust)

You use the output to:
1. **Decide which interviews to commission first** — focus on the outcomes the public data is loudest about
2. **Stress-test your draft outcome list** — outcomes everyone online has settled on (low gap) probably aren't where your innovation lives
3. **Build a board-ready directional view** while the real survey is being fielded

## What you need before running this

- `mined-outcomes.csv` from `/mineoutcomes`
- (Optional) the netted outcomes list, if you already have one — the skill maps mined data onto your locked outcomes

## What you'll get back

- `hypothesis_landscape.csv` — per outcome: proxy importance, proxy satisfaction, hypothesis opp, classification (suffixed `_HYPOTHESIS`), confidence, supporting quote count
- `hypothesis_landscape.png` — same shape as the real landscape but watermarked SYNTHETIC
- `hypothesis_landscape.md` — written summary with recommended next moves

## Critical guardrails

- Every score is labeled `opp_hypothesis`, never `opportunity`
- Classifications carry the `_HYPOTHESIS` suffix
- Outcomes with confidence <0.4 are excluded from the top-line summary
- SYNTHETIC watermark on every output (including the PNG)

## What runs after this

This skill informs `/generatesurvey` (which outcomes to definitely include, which to maybe drop, which complexity factors to probe). Then field the real survey and run `/computescores` on the real data for decision-grade results.

The skill refuses to chain into `/generatevalueprop`, `/buildroadmap`, `/choosestrategy`, or `/outcometospec`.

---

Invoke the `sentimentlandscape` skill. Stamp SYNTHETIC. Never call output "opportunity scores" — they are "hypothesis opportunity scores." Refuse to chain into decision-grade skills.
