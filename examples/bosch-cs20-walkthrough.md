# Worked example — Bosch CS20 circular saw

The canonical Ulwick case study, run end-to-end through this plugin. Every output below is what you'd actually see from the slash commands.

## 1. Define the job

```text
> /definejob "I want my customers — tradesmen who use power saws — to cut wood faster and safer"
```

Plugin response (excerpt):

> "Faster and safer" are outcomes, not part of the job. Strip them — they're captured later as desired outcomes. Also "use power saws" smuggles a solution. Let me propose a clean candidate.

Final locked statement: **Cut a piece of wood in a straight line**

Rules check: passes 5/5. Stability check: passes 3/3.

## 2. Build the job map

```text
> /buildjobmap "Cut a piece of wood in a straight line"
```

| Step | Phase | Statement |
|---|---|---|
| 1 | Define | Determine the appropriate cut path |
| 2 | Locate | Locate the right blade for the material |
| 3 | Prepare | Set the angle of the blade |
| 4 | Confirm | Confirm the cut path is clear |
| 5 | Execute | Guide the blade along the cut line |
| 6 | Monitor | Monitor the cut path during the cut |
| 7 | Modify | Adjust the blade or path mid-cut as needed |
| 8 | Conclude | Conclude the cut and store the tool |

Valid against: circular saw, table saw, hand saw, jigsaw.

## 3. Extract outcomes from 22 real interviews

```text
> /extractoutcomes interviews/cs20-01.txt
> /extractoutcomes interviews/cs20-02.txt
... (× 22)
```

After all 22 transcripts: **412 raw candidates**.

## 4. Net into the final 75 outcomes

```text
> /netoutcomes raw-outcomes.csv
```

Plugin response:

> 412 raw → 75 netted. 137 merges, 18 splits, 41 rewrites (mostly stripping "laser guide" / "DeWalt blade", consolidating "tool/instrument/device" into "saw"), 4 drops (preferences).

Sample of the final list:

| ID | Step | Outcome |
|---|---|---|
| P-05 | Prepare | Minimize the time it takes to set the angle of the blade |
| E-12 | Execute | Minimize the likelihood of moving off the cut line when guiding the blade |
| E-15 | Execute | Minimize the likelihood that debris flies up into the user's face when guiding the blade along the cut line |
| E-08 | Execute | Minimize the likelihood that the cord snags on the material when making a long cut |
| C-01 | Conclude | Minimize the likelihood of dropping the saw when lowering it from a ladder |
| … | … | … |

## 5. Generate the survey

```text
> /generatesurvey netted-outcomes.csv
```

Plugin prompts: "Competitors to include? Include WTP?"

User: "DeWalt, Makita. Yes to WTP."

Plugin produces:

- `survey-out/survey.md` — 30-min instrument, 75 outcomes × 2 + competitor sat (skip-logic per chosen brand) + 12 profiling items + 3 WTP.
- `survey-out/survey.qsf-import.txt` — Qualtrics import.
- `survey-out/field-map.csv`.

Recommended sample: n=400. Incentive: $80 trade-pro per completion. Pilot first with n=12.

## 6. Compute opportunity scores (n=413 after quality filters)

```text
> /computescores survey-data-clean.csv
```

Top hits:

| ID | Outcome | Imp | Sat | Opp | Classification |
|---|---|---|---|---|---|
| E-15 | Minimize debris into the user's face | 8.9 | 1.2 | 16.6 | extreme opportunity |
| E-12 | Minimize likelihood of moving off the cut line | 8.7 | 3.8 | 13.5 | low-hanging fruit |
| P-05 | Minimize time to set the blade angle | 8.6 | 4.1 | 13.0 | low-hanging fruit |
| E-08 | Minimize cord snags | 8.2 | 3.7 | 12.7 | low-hanging fruit |
| C-01 | Minimize likelihood of dropping when lowering from a ladder | 7.8 | 5.1 | 10.5 | worth considering |

14 outcomes scored ≥ 10. The landscape is clearly *underserved*. **Differentiated** or **Dominant** is on the table.

## 7. Run segmentation

```text
> /runsegmentation survey-data-clean.csv
```

Three segments emerge:

| Segment | Size | Defining complexity factors | Posture |
|---|---|---|---|
| A — Finish-cut tradesmen | 44% | High finish_cut_frequency, high bevel_cut_frequency | Differentiated — 14 unsatisfied outcomes |
| B — Quick-cut framers | 32% | High framing_cuts_per_week, low precision needs | Overserved — Disruptive candidate |
| C — Occasional DIYers | 24% | Low all-around frequency | Mostly table stakes |

## 8. Value prop for segment A

```text
> /generatevalueprop --segment A
```

> For tradesmen who frequently make finish cuts requiring bevel adjustments, who are trying to cut a piece of wood in a straight line, the Bosch CS20 helps them minimize the time to set the blade angle, minimize the likelihood of moving off the cut line, and minimize the likelihood of debris obscuring the cut path, unlike DeWalt or Makita circular saws, because of its direct-connect adjustment mechanism, integrated dust extraction port, and visible cut line indicator.

## 9. Build the roadmap

```text
> /buildroadmap --segment A
```

| Outcome | Opp | Move | Release | Mechanism |
|---|---|---|---|---|
| E-15 | 16.6 | 5 (new feature set) | v1.0 | Integrated dust port + LED cut-line indicator |
| E-12 | 13.5 | 5 (new feature set) | v1.0 | Direct-line laser guide |
| P-05 | 13.0 | 1 (borrow) | v1.0 | Single-lever bevel from miter saws |
| E-08 | 12.7 | 3 (partner) | v1.1 | License flex-grip cord material |
| C-01 | 10.5 | 6 (new subsystem) | v1.1 | Tether-clip + matching belt-loop |

## 10. Engineering spec for the top outcome

```text
> /outcometospec E-15
```

5-field spec includes:

- Solution concepts: (a) integrated dust port (shipping v1.0), (b) forward debris shield (shipping v1.0), (c) air-curtain (rejected — cost).
- Acceptance: "<5% of cuts produce face-zone debris in n=10 trials, pine 2x6, blade at 90°." Baseline 38%, competitor 31%, target ≤5% (20%+ better).
- Success metric: 6-month post-launch re-survey on outcome E-15, top-2-box satisfaction 1.2 → 6.0+.
- Engineering brief: 1.5" dust port + 4mm polycarbonate forward shield, ≤120g added mass, +$8 BOM at scale.

---

Result, historically: the Bosch CS20 became the #1 selling circular saw in North America for over a decade.
