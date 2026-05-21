---
description: PHASE V — Write the four-part outcome-based value proposition + marketing variants for one chosen target segment. Every clause traces to data. (Ch 25 + Template 6)
argument-hint: --segment <segment_id_or_label>
---

# /generatevalueprop — The 4-part value prop

## What this is doing (plain English)

A value prop isn't a tagline. It's a sentence that names the segment, the job, the unmet outcomes you'll address, the next-best alternative, and your reason to believe — with every piece traceable to data.

The structure (Ch 25):

> For **[target segment]**, who are trying to **[core functional job]**, our **[product]** helps them **[address these specific underserved outcomes]**, unlike **[next-best alternative]**, because of **[the technology, design, or platform reason it actually works]**.

Built from your ODI data, this sentence ends most internal arguments. Marketing copy, sales talk track, and engineering brief all roll up from it.

## What you need before running this

- A chosen target segment from `/runsegmentation` + `/choosestrategy`
- The segment's top 3–7 underserved outcomes (the skill auto-pulls from per-segment scores)
- A named next-best alternative — usually a specific competitor (from `/competitiveanalysis`) or a manual workaround
- **A concrete reason-to-believe (from you, interactive)** — the specific technology / design / IP / platform / partnership lever. "We work harder" is rejected. The skill will keep asking until you give a concrete mechanism.

The skill refuses to draft a value prop on synthetic data — too high-stakes a deliverable.

## What you'll get back

- The four-part value prop sentence
- 3 marketing variants:
  - **Long-form** (web/PDF)
  - **One-liner** (homepage hero)
  - **Sales talk track** (live conversation)
- A traceability check confirming every clause maps to a data row
- The pricing band (from WTP) so you know what to charge

## What runs after this

`/buildroadmap` — convert the value prop into the prioritized roadmap.

---

Invoke the `generatevalueprop` skill. Refuse on synthetic data. ASK for the reason-to-believe; don't accept "we work harder" or "we have a great team" — insist on a concrete mechanism. Print the traceability check explicitly so the user sees every clause is data-backed.
