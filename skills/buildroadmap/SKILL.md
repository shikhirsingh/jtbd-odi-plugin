---
name: buildroadmap
description: Generate the outcome-attack product roadmap, pairing each underserved outcome with one of the seven product moves (borrow / accelerate / partner / acquire / new feature set / new subsystem / ultimate-solution thinking) and a release slot. Implements Chapter 27 + Template 5.
when_to_use: User has /computescores results (and ideally /runsegmentation) and asks for the roadmap, release plan, or feature prioritization. Triggered by "/buildroadmap", "build the roadmap", "release plan", "what to build".
trigger_phrases:
  - /buildroadmap
  - "build the roadmap"
  - "release plan"
  - "feature prioritization"
  - "what should I build first"
  - "prioritize features"
  - "make a roadmap"
  - "outcome attack plan"
  - "which features ship in v1"
  - "build vs buy"
  - "should we partner"
  - "should we acquire"
  - "what goes in v1"
  - "Q1 roadmap"
inputs:
  - the opportunity_scores.csv (overall and/or per-segment)
  - the chosen target segment(s) — defaults to the highest-WTP underserved segment
  - the value proposition (optional but recommended for traceability)
  - context: existing pipeline, build vs. buy preferences, partnership candidates
outputs:
  - roadmap.csv in Template-5 shape (Outcome | Opp | Segment(s) | Move | Release | Mechanism)
  - roadmap.md as a defensible release plan with reasoning
  - 7-product-moves coverage analysis (which moves are over-used / under-used)
chains_to:
  - /outcometospec (one per outcome shipping in next release)
---

# /buildroadmap — Outcome-Attack Roadmap

## Plain-English preamble (for newcomers)

> Take the ranked underserved outcomes and convert them into a release plan. For each outcome, pick **one of seven product moves**:
>
> 1. **Borrow** a feature from an adjacent category (often fastest)
> 2. **Accelerate** something already in the pipeline
> 3. **Partner / license** for capability you don't own
> 4. **Acquire** a startup that has the capability
> 5. **Devise a new feature set** in the existing platform (most common)
> 6. **Devise a new subsystem or service**
> 7. **Conceptualize the ultimate solution** (long-term Northstar)
>
> Then slot each outcome into a release (v1.0 / v1.x / v2.0 / Northstar).
>
> A good roadmap uses a **mix** of moves. If 70%+ are "new feature set" (move 5), you're missing faster paths.

---

> "The most useful single document the project produces is a roadmap that pairs each underserved outcome with the move you'll use to address it and the release in which it'll ship." (Chapter 27)

## The seven product moves (Table 27.1)

| # | Move | Means |
|---|---|---|
| 1 | **Borrow features from other offerings** | Adopt a feature from an adjacent category that addresses one of your underserved outcomes. Often fastest. |
| 2 | **Accelerate the existing pipeline** | You already have a feature in development that hits an underserved outcome. ODI moves it forward. |
| 3 | **Partner or license** | Another company owns IP or a component that addresses your outcome. Access via partnership/license. |
| 4 | **Acquire** | The capability lives in a startup. ODI scoring gives a quantitative basis for which targets are worth what. |
| 5 | **Devise a new feature set** | Build new features inside the existing platform. Most common move. |
| 6 | **Devise new subsystems or services** | New platform component, ancillary service, consumption-chain offering. |
| 7 | **Conceptualize the ultimate solution** | "If cost and physics didn't matter, what would the optimal product be?" Sets the long-term north star. |

A good roadmap **uses a mix**. If you're devising new feature sets (move 5) for every outcome, you're probably ignoring faster paths.

## How to assign moves to outcomes

Walk each underserved outcome (Opp ≥ 10) and ask, in order:

1. **Is there an adjacent category solving this already?** → Move 1 (borrow).
2. **Is something already in our pipeline that addresses this?** → Move 2 (accelerate).
3. **Does someone else own a critical component or IP?** → Move 3 (partner) or Move 4 (acquire).
4. **Does it require new platform capability?** → Move 6 (subsystem) or Move 5 (new feature set).
5. **Is this an outcome no current product is close to satisfying?** → Capture it as a Move 7 "ultimate-solution" thought-experiment target for the long-term roadmap, and pick the best of moves 1–6 for the next release.

## Release slotting

Suggested default tiers:

| Release | Criteria |
|---|---|
| v1.0 | Outcomes opp ≥ 12 + table-stakes outcomes (must satisfy at parity) + 2–3 outcomes addressed via Move 1 (fast borrow) |
| v1.x | Outcomes opp 10–12 + dependencies addressed via partnerships (Move 3) |
| v2.0 | Move 6 platform plays + acquisitions if announced |
| Northstar | Move 7 ultimate-solution targets |

This is just a default. The user can override.

## How to run

1. **Load opportunity_scores.csv.** Filter to outcomes with opp ≥ 10 (the underserved set).
2. **Also include table-stakes outcomes** (high importance + high satisfaction): the product must satisfy them at competitor parity even if they're not innovation drivers.
3. **For each outcome, propose a move (1–7)** with a one-line mechanism description. Ask the user for build-vs-buy preferences, known partnership candidates, and current pipeline.
4. **Slot each outcome into a release** (v1.0, v1.x, v2.0, Northstar).
5. **Run coverage analysis:** % of outcomes per move. Flag if Move 5 (new feature set) is >70% of the roadmap — usually means the team is overlooking fast borrows or partnerships.
6. **Emit Template-5 CSV and the defensible markdown.**

## Output — Template 5

```csv
outcome_id,opportunity_score,segment,move_number,move_name,release,mechanism
E-15,14.5,A,5,New feature set,v1.0,Integrated dust extraction port + LED cut-line indicator
E-12,14.2,A,5,New feature set,v1.0,Direct-line laser guide
P-05,13.0,A,1,Borrow features,v1.0,Single-lever bevel mechanism (borrowed from miter saw line)
E-08,12.7,"A,B",3,Partner or license,v1.1,License flex-grip cord material from category supplier
C-01,10.5,A,6,New subsystem,v1.1,Tether-clip on housing + matching belt-loop accessory
P-02,9.6,"A,B,C",2,Accelerate existing pipeline,v1.0,Already-in-progress quick-release base plate — pull forward 4 months
```

And the JSON:

```json
{
  "skill": "buildroadmap",
  "method_version": "ODI v2.4.2",
  "job_statement": "...",
  "target_segments": ["A", "B"],
  "outputs": {
    "csv": "roadmap-out/roadmap.csv",
    "markdown": "roadmap-out/roadmap.md"
  },
  "moves_coverage": {
    "Move 1 — Borrow":          {"count": 3, "pct": 0.15},
    "Move 2 — Accelerate":      {"count": 2, "pct": 0.10},
    "Move 3 — Partner":         {"count": 4, "pct": 0.20},
    "Move 4 — Acquire":         {"count": 1, "pct": 0.05},
    "Move 5 — New feature set": {"count": 8, "pct": 0.40},
    "Move 6 — New subsystem":   {"count": 1, "pct": 0.05},
    "Move 7 — Ultimate":        {"count": 1, "pct": 0.05}
  },
  "warnings": [],
  "next_step": "For each v1.0 outcome, run /outcometospec to produce the engineering spec."
}
```

## Hard rules

- Every roadmap line must trace to an outcome ID with an opportunity score.
- A feature without a corresponding underserved outcome ID **does not appear on the roadmap.** If the user insists ("regulatory requirement", "partner commitment"), add a separate `non_outcome_justified` block that surfaces what capacity it consumes.
- Don't slot more than 7 outcomes into v1.0. Engineering velocity is finite; ODI roadmaps that try to attack everything fail to attack anything.
- Don't use Move 5 (new feature set) for more than 60% of outcomes without explicit justification per slot.
