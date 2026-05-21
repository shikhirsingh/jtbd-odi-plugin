---
description: "PHASE II FINAL — Dedupe + clean 300–600 raw candidate outcomes into the final 50–150 survey-ready outcomes (Template 3, Ch 14). Alias: /refineoutcomes."
argument-hint: <path to raw outcomes CSV OR folder of /extractoutcomes outputs>
---

# /netoutcomes (aka /refineoutcomes) — Clean the outcomes list

## What this is doing (plain English)

After running `/extractoutcomes` on each interview, you'll have 300–600 raw candidates. Most are duplicates with different wording, some are compound ("time AND effort"), some embed product names, some have vague adjectives. This skill compresses the raw pile into a clean, deduped, well-formed list of 50–150 — the list that will go into your survey.

"Netting" is Ulwick's term (Ch 14). It's a 7-step process. The skill walks every step and logs every merge / split / rewrite / drop so the human reviewer can audit.

## What you need before running this

- One or more raw candidate CSVs from `/extractoutcomes` (or the synthetic equivalent from `/mineoutcomes`)
- The locked job statement + job map (for context)

If you have >500 raw candidates, the skill will call `scripts/netting_helper.py` to do embedding-based first-pass dedupe before the LLM walks each cluster.

## What you'll get back

- A single CSV in Template-3 shape: `id, job_step, direction, metric, object_of_control, clarifier, full_statement`
- An audit log of every operation (merges, splits, rewrites, drops) with reasoning
- A balance check warning if any in-scope job-map step has < 3 outcomes or > 25 outcomes
- Total in the **50–150 range** (less = under-covered interviews; more = unmanageable survey length)

## Jargon you'll see

- **Netting** — the dedupe + clean process. Just "refining."
- **Compound statement** — bundles two outcomes ("time AND effort"). Split into two.
- **Embedded solution** — names a product/brand/technology ("the laser guide drifts"). Strip and generalize.
- **Variability strip** — Table 11.4 sins. Non-canonical direction verbs, vague adjectives, inconsistent nouns.

## What runs after this

- `/validateoutcomes` is **required next**. It's a hard gate — `/generatesurvey` refuses to run if any outcome fails the 10 characteristics.

---

Invoke the `netoutcomes` skill. If the raw set is >500 candidates, run `python scripts/netting_helper.py --raw <input> --out clusters.json` first to get embedding-clusters + sin-flags, then walk the LLM through each cluster to pick the canonical statement. After completion, point user to `/validateoutcomes` (mandatory) before `/generatesurvey`.
