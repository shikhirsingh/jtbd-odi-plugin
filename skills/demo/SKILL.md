---
name: demo
description: Show realistic worked-example outputs for a known job ("listen to music while on the go" or "cut a piece of wood in a straight line") WITHOUT running a real engagement. The "see before you commit" skill. Use when a user wants to see what the plugin actually produces before deciding to invest 4–8 weeks in a real engagement.
when_to_use: User says "show me an example", "what does the output look like", "demo", "I want to see before I commit", "what would this produce", "/demo".
trigger_phrases:
  - /demo
  - /example
  - "show me an example"
  - "what does the output look like"
  - "what would I get"
  - "before I commit"
  - "show me what this produces"
  - "show me what ODI looks like"
  - "give me a sample"
  - "what does a final deliverable look like"
  - "what would my output be"
  - "show me a worked example"
  - "I want to see before I"
  - "is this worth doing"
  - "what would this even look like"
inputs:
  - (optional) which worked example to show — "music" or "saw" (default: ask the user)
  - (optional) which artifact to focus on — landscape / segments / value prop / roadmap / canvas / all (default: all, summarized)
outputs:
  - sample versions of the six Table 30.1 artifacts using the worked example
  - clear "THIS IS A DEMO" stamping on every output so it's never mistaken for real engagement data
  - guidance on which command produced each artifact (so the user can mentally map "I'd run X to get this")
chains_to:
  - /odihelp (after demo — to route the user to their actual starting point)
  - /preflight (to check ODI fits their situation)
  - /runfullodi (if they're ready to commit)
---

# /demo — See what the plugin actually produces

> **Plain English:** Before you commit 4–8 weeks and $30k to a real ODI engagement, you probably want to see *what you'd actually get out the other end*. This skill walks you through realistic outputs for a known worked example (a Bosch CS20 circular saw OR a "listen to music on the go" headphones engagement) and shows you what each artifact looks like. Nothing is run; nothing is fielded. It's a tour, not an engagement.

## What this skill shows you

The user picks (or you ask) which worked example to walk through:

| Demo | Why pick this |
|---|---|
| **Bosch CS20** (Ulwick's canonical case) | Real B2B example with a documented Differentiated outcome — the one in the handbook |
| **Listen to music on the go** | Familiar B2C example, fewer industry-specific words |
| **Both side-by-side** | Compares B2B and B2C flavors of the method |

For the chosen demo, the skill walks through the six artifacts (Table 30.1) PLUS the Canvas:

1. **Job statement** (showing the iteration from a draft to a locked statement)
2. **Job map** (the 8 universal steps applied to the example)
3. **Sample outcome statements** (5–10 examples of the strict syntax, not all 75)
4. **Opportunity landscape** (sample of the ranked CSV; 3–4 example outcomes with their scores; ASCII landscape diagram)
5. **Segments** (2–3 segments with their complexity-factor profiles)
6. **Strategic posture** (Growth Matrix placement with reasoning)
7. **Value proposition** (the four-part sentence)
8. **Roadmap** (sample of the seven-moves table with 5 outcomes)
9. **One engineering spec sheet** (the 5-field artifact)
10. **The Canvas** (the one-pager)

Every output stamped clearly:

```
=================================================================
THIS IS A DEMO — These outputs are illustrative examples,
not real engagement results. The Bosch CS20 case is from the
ODI handbook; the music example is fabricated for teaching.
Use /odihelp to start a real engagement.
=================================================================
```

## How to run

1. **Ask the user which demo** unless they already specified.
2. **Walk through artifacts 1–10** in order. For each:
   - Show what it looks like (1–2 sentences + a sample of the actual output format)
   - Name the command that would produce it in a real engagement
   - Note what *they would need to provide* if they ran the real command
3. **End with a clear "what next?"** — either `/odihelp` (decide which path), `/preflight` (check if ODI is right for them), or `/runfullodi --mode rehearsal` (try the synthetic pipeline on their own job).

## Sample walkthrough — Bosch CS20

> *(This is the worked example from the ODI handbook. The numbers are real from the case study.)*

**Artifact 1 — Job statement** *(would be produced by `/definejob`)*
> **Cut a piece of wood in a straight line**
> ✓ 5/5 rules pass · ✓ 3/3 stability checks pass · status: locked

**Artifact 2 — Job map** *(would be produced by `/buildjobmap`)*
> 1. Define — Determine the appropriate cut path
> 2. Locate — Locate the right blade for the material
> 3. Prepare — Set the angle of the blade
> 4. Confirm — Confirm the cut path is clear
> 5. Execute — Guide the blade along the cut line
> 6. Monitor — Monitor the cut path during the cut
> 7. Modify — Adjust the blade or path mid-cut as needed
> 8. Conclude — Conclude the cut and store the tool

**Artifact 3 — Sample outcomes** *(would be produced by `/extractoutcomes` + `/netoutcomes`)*
> E-15 — Minimize the likelihood that debris flies up into the user's face when guiding the blade along the cut line
> E-12 — Minimize the likelihood of moving off the cut line when guiding the blade
> P-05 — Minimize the time it takes to set the angle of the blade
> E-08 — Minimize the likelihood that the cord snags on the material when making a long cut
> C-01 — Minimize the likelihood of dropping the saw when lowering it from a ladder
>
> *(In a real engagement you'd have 50–150 of these, validated by `/validateoutcomes` against the 10 characteristics.)*

**Artifact 4 — Ranked opportunity list** *(would be produced by `/computescores`)*

| ID | Outcome | Imp | Sat | Opp | Class |
|---|---|---|---|---|---|
| E-15 | …debris into user's face | 8.9 | 1.2 | 16.6 | extreme opportunity |
| E-12 | …moving off the cut line | 8.7 | 3.8 | 13.5 | low-hanging fruit |
| P-05 | …time to set blade angle | 8.6 | 4.1 | 13.0 | low-hanging fruit |
| E-08 | …cord snags | 8.2 | 3.7 | 12.7 | low-hanging fruit |
| C-01 | …dropping from ladder | 7.8 | 5.1 | 10.5 | worth considering |

ASCII landscape preview:
```
   10|             E-15
  Imp |        E-12 *
      |       P-05 *  *  E-08
    6 |          *      C-01
      |              *  *
    2 |   *  *  *
      +-----------------------
        0   2   4   6   8  10 Sat
```

> *(The diagonal line divides "served" (above) from "overserved" (below). The dashed terracotta line marks opportunity = 10.)*

**Artifact 5 — Segments** *(would be produced by `/runsegmentation`)*

| Segment | Size | Defining complexity factors | Posture |
|---|---|---|---|
| A — Finish-cut tradesmen | 44% | High finish_cut_freq, high bevel_freq | Differentiated |
| B — Quick-cut framers | 32% | High framing_cuts/week, low precision needs | Overserved → Disruptive |
| C — Occasional DIYers | 24% | Low overall frequency | Mostly table stakes |

**Artifact 6 — Strategic posture** *(would be produced by `/choosestrategy`)*
> **Segment A → Differentiated.** Evidence: 14 outcomes opp ≥ 10; WTP median $410 (high band); DeWalt + Makita both score <4 on top 6 outcomes.

**Artifact 7 — Value proposition** *(would be produced by `/generatevalueprop`)*

> For **tradesmen who frequently make finish cuts requiring bevel adjustments**, who are trying to **cut a piece of wood in a straight line**, the **Bosch CS20** helps them **minimize the time to set the blade angle, minimize the likelihood of moving off the cut line, and minimize the likelihood of debris obscuring the cut path**, unlike **DeWalt or Makita circular saws**, because of **its direct-connect adjustment mechanism, integrated dust extraction port, and visible cut line indicator**.

**Artifact 8 — Roadmap** *(would be produced by `/buildroadmap`)*

| Outcome | Opp | Move | Release | Mechanism |
|---|---|---|---|---|
| E-15 | 16.6 | 5 (new feature set) | v1.0 | Integrated dust port + LED cut-line |
| E-12 | 13.5 | 5 (new feature set) | v1.0 | Direct-line laser guide |
| P-05 | 13.0 | 1 (borrow) | v1.0 | Single-lever bevel from miter saws |
| E-08 | 12.7 | 3 (partner) | v1.1 | License flex-grip cord material |
| C-01 | 10.5 | 6 (new subsystem) | v1.1 | Tether-clip + matching belt-loop |

**Artifact 9 — One engineering spec sheet** *(would be produced by `/outcometospec`)*

> **Outcome E-15** — Minimize debris into user's face. Opp 16.6. Segment A.
> **Solution concept (a):** 1.5″ integrated dust extraction port aft of blade housing.
> **Acceptance criteria:** In a controlled test (n=10 cuts, pine 2x6, blade 90°): <5% of cuts produce face-zone debris. Baseline 38%, best competitor 31%, target ≤5% (20%+ better).
> **Success metric:** Top-2-box satisfaction rises 1.2 → 6.0+ in the 6-month post-launch survey.
> **Engineering brief:** Add 1.5″ port + 4mm polycarbonate forward shield. ≤120g added mass. +$8 BOM at scale.

**Artifact 10 — Canvas** *(would be produced by `/createodicanvas`)*
> A single page that pulls all of the above together with footnotes traceable to every source file. Designed for the board meeting.

## What to do after the demo

```
=== Now that you've seen the demo, three ways to proceed ===

1. /odihelp        — figure out which path (Full / Lite / Rehearsal) fits your situation
2. /preflight       — check whether ODI is the right tool for your problem at all
3. /runfullodi --mode rehearsal   — try the synthetic version on YOUR own job statement
                                    (30–60 min, hypothesis-only, no panel cost)
```

## Hard rules

- Always stamp the demo output with the clear "THIS IS A DEMO" banner.
- Bosch CS20 numbers come from the ODI handbook (real). Other examples are fabricated for teaching — say so.
- Never let demo output get confused with real engagement output.
- End every demo with the three clear "what next?" options.
