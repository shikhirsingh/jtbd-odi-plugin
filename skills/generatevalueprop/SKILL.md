---
name: generatevalueprop
description: Draft the four-part outcome-based value proposition for a chosen segment, plus marketing variants. Implements Chapter 25 + Template 6.
when_to_use: User has segmentation results and asks for "the value prop", "positioning", or invokes /generatevalueprop. Requires: segment selection, top underserved outcomes for that segment, identified next-best alternative, technical/design reason-to-believe.
trigger_phrases:
  - /generatevalueprop
  - "write the value prop"
  - "positioning statement"
  - "value proposition"
  - "how should we position"
  - "what should our pitch be"
  - "marketing message"
  - "homepage copy"
  - "sales talk track"
  - "what's our angle"
  - "what makes us different"
  - "differentiation"
inputs:
  - selected target segment (from /runsegmentation)
  - top 3–7 underserved outcomes for that segment (with opportunity scores)
  - next-best alternative (from competitive analysis or user input)
  - reason to believe — the specific technology / design / platform decision
outputs:
  - the canonical 4-part value proposition sentence (Chapter 25 template)
  - 3 marketing variants (long-form, one-liner, sales-talk-track)
  - a check that every clause traces back to ODI data
chains_to:
  - /buildroadmap
---

# /generatevalueprop — The Outcome-Based Value Proposition

## Plain-English preamble (for newcomers)

> A value prop is not a tagline. It's a **four-part sentence** that names the target segment, the functional job, the underserved outcomes you'll address, the next-best alternative, and your reason to believe — with every clause traceable to data.
>
> Built from real ODI data, the sentence ends most internal arguments. Marketing copy, sales talk track, and engineering brief all roll up from it.
>
> **Format (Ch 25):**
> *For [segment], who are trying to [job], our [product] helps them [underserved outcomes], unlike [alternative], because of [reason to believe].*
>
> **The "reason to believe" must be a concrete mechanism.** "We work harder" is rejected. The skill insists on a specific technology / design / IP / partnership lever.
>
> **Refuses on synthetic data** — too high-stakes a deliverable.

---

The value prop is not a tagline. It's a sentence that **names the segment, the job, the unmet outcomes you'll address, and your reason to believe**. Built from the data, it ends most internal arguments.

## The four-part structure (Chapter 25)

```
For [target segment],
who are trying to [core functional job],
our [product] helps them [address these specific underserved outcomes],
unlike [next-best alternative],
because of [the technology, design, or platform reason it actually works].
```

## Where every piece comes from (Table 25.1)

| Component | Source in your ODI data |
|---|---|
| **Target segment** | The outcome-based segment chosen in /runsegmentation, profiled by complexity factors. |
| **Core functional job** | The job statement from /definejob. |
| **Underserved outcomes addressed** | Top 3–7 outcomes by opportunity score *within the target segment*. |
| **Next-best alternative** | The competitor or workaround the survey identified as most-used in this segment. |
| **Reason to believe** | The specific technology / design / platform decision that lets you satisfy those outcomes >20% better. |

## The 20% rule (Chapter 22)

> "Significantly better" — Strategyn's empirical rule from years of post-launch tracking — means your product must satisfy the underserved outcome roughly **20% better** than competing solutions to win meaningful share. Anything under 5% better is "stuck in the middle"; customers won't switch.

The reason-to-believe must therefore name a mechanism that plausibly clears that 20% bar. "We tried harder" doesn't count.

## How to run

1. **Read the segment profile.** Confirm size, complexity-factor profile, and strategic posture (Differentiated / Dominant / Disruptive / Sustaining).
2. **List the segment's top 7 underserved outcomes** (opp ≥ 10, sorted desc).
3. **Identify the next-best alternative.** Default: the competitor with the highest market share *inside this segment* (from the survey "which do you use most often" question). Fallback: the dominant manual workaround.
4. **Ask the user for the reason-to-believe** if not supplied. Concrete technology, geometry, design, IP, platform decision, or partnership. Refuse "we have a better team" / "we work harder."
5. **Fill the four-part template.**
6. **Generate three marketing variants** (long, one-liner, sales talk track) — all naming outcomes in the segment's own language.
7. **Run a traceability check** — every clause must trace back to ODI data.

## Output

```json
{
  "skill": "generatevalueprop",
  "method_version": "ODI v2.4.2",
  "job_statement": "Cut a piece of wood in a straight line",
  "segment": {"id": "A", "label": "Finish-cut tradesmen", "size_pct": 0.44},
  "value_prop": "For tradesmen who frequently make finish cuts requiring bevel adjustments, who are trying to cut a piece of wood in a straight line, our Bosch CS20 helps them minimize the time to set the blade angle, minimize the likelihood of moving off the cut line, and minimize the likelihood of debris obscuring the cut path, unlike DeWalt or Makita circular saws, because of its direct-connect adjustment mechanism, integrated dust extraction port, and visible cut line indicator.",
  "marketing_variants": {
    "long_form": "If you live and die by clean finish cuts and bevel adjustments — and the gap between a 7-second blade-angle reset and a 30-second one defines whether you finish before the client gets back — the Bosch CS20 was built around the three outcomes our research showed are most underserved across the trade: setting the angle without picking up a tool, keeping the blade tracking the line, and seeing what you're cutting through the dust. We did it with a direct-connect single-lever bevel, an integrated dust port, and an LED cut-line you can actually see.",
    "one_liner": "Finish cuts at 20% the setup time — Bosch CS20.",
    "sales_talk_track": "If you do a lot of finish work or bevels, the part of the day you lose isn't cutting — it's re-setting the saw between cuts and re-cutting when you drift off the line. The CS20 collapses those two into one motion. The bevel lever locks in 7 seconds; the LED keeps the line visible through dust; the dust port plugs into your shop-vac. We're not asking you to switch on price; we're asking you to switch on time-to-finish."
  },
  "traceability_check": {
    "segment_named": true,
    "job_named": true,
    "underserved_outcomes_traced": [
      {"clause": "minimize the time to set the blade angle", "outcome_id": "P-05", "opp_in_segment": 14.6},
      {"clause": "minimize the likelihood of moving off the cut line", "outcome_id": "E-12", "opp_in_segment": 14.2},
      {"clause": "minimize the likelihood of debris obscuring the cut path", "outcome_id": "E-15", "opp_in_segment": 14.5}
    ],
    "next_best_alternative_evidence": "DeWalt named by 52% of segment A in 'most used' question",
    "reason_to_believe_concrete": true
  },
  "next_step": "Run /buildroadmap to convert the value prop into the prioritized outcome-attack plan."
}
```

## Hard rules

- Every clause traces to data — fail traceability_check loudly if it doesn't.
- Reason-to-believe must be a specific technology / design / platform / IP decision, not an attitude.
- Never name the segment by demographics if a complexity-factor label is available. "Finish-cut tradesmen" beats "Men 30–55" every time.
- The value prop is segment-specific. If the user asks for "the value prop" without naming a segment, refuse and tell them to choose one first.
