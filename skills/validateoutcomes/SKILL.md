---
name: validateoutcomes
description: Validate a list of outcome statements against the 10 characteristics from Chapter 11, the strict 4-part syntax, and the variability strips in Table 11.4. Returns a per-outcome pass/fail report, suggested rewrites, and a final go/no-go for survey readiness. Acts as the gate between /netoutcomes and /generatesurvey — refuses to allow a malformed list into the survey.
when_to_use: User has a netted outcomes CSV and wants to confirm survey-readiness, OR wants to QA an externally-provided outcome list. Triggered by "/validateoutcomes", "check these outcomes", "validate before survey", "are these survey-ready". Also auto-invoked by /generatesurvey as a precondition.
trigger_phrases:
  - /validateoutcomes
  - "validate outcomes"
  - "check outcome quality"
  - "are these survey-ready"
inputs:
  - netted outcomes CSV (or pasted list)
outputs:
  - validation_report.csv — one row per outcome, 10 boolean columns + suggestion + severity
  - validation_report.md — human-readable summary
  - go/no-go verdict for survey readiness
helpers:
  - scripts/outcome_validator.py
chains_to:
  - /netoutcomes (if validation fails — re-net)
  - /generatesurvey (if validation passes)
---

# /validateoutcomes — The Outcome-Quality Gate

This skill is a **hard gate**. If an outcome list fails validation, the survey will produce noisy and uninterpretable opportunity scores — you cannot fix that downstream with statistics. So this gate exists.

## The 10 characteristics (Ch 11, Table 11.2)

| # | Characteristic | What it means |
|---|---|---|
| 1 | **Stable over time** | Still meaningful in 20 years (no current tech, no current category) |
| 2 | **Reveals a metric** | Time / likelihood / frequency / number / amount |
| 3 | **Devoid of solutions** | No product names, technologies, or features |
| 4 | **Measurable** | You can imagine instrumenting it |
| 5 | **Controllable** | The executor (or product team) can plausibly influence it |
| 6 | **Actionable** | An engineer/designer reading it knows roughly what to attack |
| 7 | **One-dimensional** | One direction, one metric, one object — no compound statements |
| 8 | **Mutually exclusive** | Does not duplicate any other statement on the list |
| 9 | **Customer-stated value** | Reflects how the executor measures success |
| 10 | **Useful across functions** | Marketing, product, engineering, sales can all act on it |

## The variability strips (Ch 11, Table 11.4)

| Sin | Detection rule |
|---|---|
| Direction verb ≠ Minimize/Increase | Regex catches "reduce", "prevent", "eliminate", "avoid", "decrease", "limit", "improve" |
| Adjective/adverb in body | Catches "frequently", "significantly", "excessive", "quickly", "easily" |
| Inconsistent noun for same object | Cross-list scan for "tool" vs "instrument" vs "device" etc. |
| Compound statement | Substring " and " or "&" between two nouns — flag |
| Embedded solution | Catches product names, brand names, technology terms |

## How to run

1. Call `scripts/outcome_validator.py` over the netted CSV.
2. The script returns per-outcome:
   - 10 boolean columns (one per characteristic)
   - 5 boolean columns (one per variability sin)
   - `severity` ∈ {ok, warn, fail}
   - `suggestion` — proposed rewrite if applicable
3. Aggregate:
   - **Pass** if 100% are `ok`.
   - **Conditional pass** if <5% are `warn` and 0% are `fail`.
   - **Fail** if any outcome is `fail`.
4. Cross-list dedupe check: cosine similarity > 0.85 between two statements is a dedupe alert.
5. Emit `validation_report.csv`, `validation_report.md`, and the verdict.

## Output

```json
{
  "skill": "validateoutcomes",
  "method_version": "ODI v2.4.2",
  "input": "netted-outcomes.csv",
  "n_outcomes": 96,
  "summary": {
    "ok": 88,
    "warn": 6,
    "fail": 2
  },
  "verdict": "fail",
  "verdict_reason": "2 outcomes contain compound statements; 1 outcome embeds a product name.",
  "failing_outcomes": [
    {"id": "P-08", "statement": "Minimize the time and effort to clean the saw",
     "failures": ["one_dimensional"], "severity": "fail",
     "suggestion": "Split into two outcomes: 'Minimize the time it takes to clean the saw' and 'Minimize the physical effort required to clean the saw'"},
    {"id": "E-22", "statement": "Minimize the likelihood that the DeWalt blade overheats",
     "failures": ["devoid_of_solutions"], "severity": "fail",
     "suggestion": "Strip brand: 'Minimize the likelihood that the blade overheats during a long cut'"}
  ],
  "warning_outcomes": [
    {"id": "M-04", "statement": "Reduce the frequency that the queue is interrupted",
     "warnings": ["direction_verb_not_canonical"], "severity": "warn",
     "suggestion": "Replace 'Reduce' with 'Minimize': 'Minimize the frequency that the queue is interrupted'"}
  ],
  "duplicate_alerts": [
    {"pair": ["E-12", "E-19"], "cosine": 0.88,
     "reason": "Both express 'minimize the likelihood of moving off the cut line' — likely duplicates."}
  ],
  "outputs": {
    "csv": "validation-out/validation_report.csv",
    "markdown": "validation-out/validation_report.md"
  },
  "next_step": "Address the 2 failures and the duplicate pair, then re-run /validateoutcomes. /generatesurvey will refuse until verdict='pass'."
}
```

## Hard rules

- A list with even one `fail` outcome cannot pass. /generatesurvey will refuse.
- Suggestions are *suggestions* — the human reviewer accepts or modifies them.
- Cross-list cosine duplicate alerts are surfaced but not auto-merged.
- This skill is purely diagnostic. It does not modify the netted file directly.
