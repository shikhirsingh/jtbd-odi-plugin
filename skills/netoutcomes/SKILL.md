---
name: netoutcomes
description: Net, deduplicate, and refine 300–600 raw outcome candidates into a final 50–150 clean, well-formed, mutually-exclusive desired-outcome statements ready for the survey. Implements Chapter 14 of the ODI handbook.
when_to_use: User has run /extractoutcomes on multiple interview transcripts (or pasted/uploaded a raw outcomes CSV) and now wants the netted, survey-ready list. Triggered by "/netoutcomes …", "net these outcomes", "dedupe", "clean up these outcomes", or after /extractoutcomes returns its candidate set.
trigger_phrases:
  - /netoutcomes
  - "net outcomes"
  - "dedupe outcomes"
  - "clean outcomes for survey"
inputs:
  - one or more files of raw outcome candidates from /extractoutcomes (or /mineoutcomes)
  - the locked job statement and job map
outputs:
  - 50–150 netted outcomes in Template-3 CSV shape
  - explicit log of every merge, split, and rewrite (so the human reviewer can audit)
  - a balance-check warning if any job-map step has <3 outcomes or >25 outcomes
chains_to:
  - /generatesurvey (next: build the survey instrument from the netted list)
helpers:
  - scripts/netting_helper.py (optional embedding-based dedupe + compound/direction-verb detector — Claude can call this for >500 raw candidates)
---

# /netoutcomes — Net & Refine the Outcome Set

## Plain-English preamble (for newcomers)

> "Netting" is Ulwick's term for **dedupe + clean**. After all your `/extractoutcomes` runs, you have 300–600 raw candidates. Most are near-duplicates with different wording, some are compound, some have product names embedded. This skill compresses the pile into 50–150 well-formed final outcomes that go into the survey.
>
> The plain-English alias is `/refineoutcomes` if "netting" feels too jargony.
>
> **What the 7-step process does:**
> 1. Groups candidates by job step
> 2. Reformats every outcome to strict syntax
> 3. Dedupes (same direction + metric + object = duplicate, regardless of wording)
> 4. Splits compound statements
> 5. Confirms one-dimensionality
> 6. Strips embedded solutions
> 7. Tests for stability over time
>
> **Every operation is logged** in an audit log so a human reviewer can verify.

---

This skill implements the *netting process* from Chapter 14 of the ODI handbook. After 20–30 interviews you'll have 300–600 raw candidate outcomes. Most are duplicates, malformed, compound, or solution-laden. Netting compresses them into a clean, deduped, well-formed set of 50–150.

**A single bad netted list breaks the survey, the opportunity scores, and the segmentation. So you are pedantic here.**

---

## The 7-step netting process (Chapter 14)

1. **Group by job-map step.** Sort all raw outcomes under the step they belong to. If any step has 50 candidates and others have three, the latter usually means an interview gap — flag it.
2. **Reformat every outcome to strict syntax.** Add missing direction-of-improvement words. Convert vague metrics ("affect," "improve") to time/likelihood. Add clarifiers where context is ambiguous.
3. **Deduplicate.** Two statements that share the same *direction*, *metric*, and *object* are duplicates regardless of surface wording. Keep the cleaner one; log the merge.
4. **Split compound statements.** "Minimize the time and effort required to clean the device" is two outcomes (time, effort). Split if both matter. Drop the weaker one if not.
5. **Test for one-dimensionality.** Each statement should describe one variable. If you can mentally answer "more important" and "less satisfied" separately, it's one-dimensional. If "I rate the same number for both," it's compound — split.
6. **Test for solution-freedom.** Scan for product names, technology references, feature words. Strip them and rewrite. "Minimize the likelihood that the laser guide drifts off the cut line" → "Minimize the likelihood of moving off the cut line."
7. **Test for stability.** Will this statement still make sense in 20 years? If it depends on a current technology ("…of the Bluetooth connection dropping"), generalize ("…of the wireless audio connection dropping" — even better, "…of audio dropouts during playback").

## Final target shape (Template 3)

```
ID | Job step | Direction | Metric | Object | Clarifier | Full statement
---+----------+-----------+--------+--------+-----------+---------------
D-01 | Define  | Minimize | the time it takes to | determine the appropriate cut path | before initiating any cut | Minimize the time…
```

IDs: two letters (job step) + two digits. Define → D-01..D-NN, Locate → L-01..L-NN, etc.

## Balance check

Aim for **50–150 total outcomes**. Within that:

| Step | Typical count |
|---|---|
| Define | 5–15 |
| Locate | 3–10 |
| Prepare | 8–20 |
| Confirm | 3–10 |
| Execute | 15–35 |
| Monitor | 5–15 |
| Modify | 5–15 |
| Conclude | 3–10 |

Plus separate sections for:
- Related jobs: 5–20
- Emotional/social: 5–25
- Consumption-chain: 5–25
- Financial: 0–80 (mostly B2B)

If your final netted list has **fewer than 3 outcomes on any in-scope job-map step**, return a warning. The qualitative interviews probably under-covered that step.

---

## How to run

1. **Load every raw candidate** from the inputs (combine across transcripts).
2. **Group by job_step.**
3. **For each group:** apply steps 2–7 above. Iterate.
4. **Log every transformation** — merges, splits, rewrites, drops — with the candidate IDs involved and a short reason. This is the audit trail.
5. **Compute the balance check.**
6. **Emit the final CSV** (Template 3) plus the audit log.

If the raw set is **>500 candidates**, call `scripts/netting_helper.py` to do an embedding-based first-pass dedupe + compound/direction-verb sin detection, then review each cluster and pick the canonical statement. This is the recommended workflow for large engagements.

---

## Output format

Return two artifacts:

### 1. The netted CSV (Template 3 shape)

Write it to disk and tell the user the path. Use this exact header:

```csv
id,job_step,direction,metric,object_of_control,clarifier,full_statement
D-01,Define,Minimize,the time it takes to,determine the appropriate cut path,before initiating any cut,Minimize the time it takes to determine the appropriate cut path before initiating any cut
D-02,Define,Minimize,the likelihood of,selecting the wrong blade for the material,,Minimize the likelihood of selecting the wrong blade for the material
...
```

### 2. The structured JSON summary

```json
{
  "skill": "netoutcomes",
  "method_version": "ODI v2.4.2",
  "job_statement": "...",
  "input": {"raw_candidates": 421, "interviews_covered": 22},
  "output": {
    "path": "netted-outcomes.csv",
    "total_netted": 96,
    "by_step": {"Define": 9, "Locate": 6, "Prepare": 14, "Confirm": 5, "Execute": 28, "Monitor": 11, "Modify": 8, "Conclude": 4, "related_jobs": 8, "emotional_social": 12, "consumption_chain": 15, "financial": 3},
    "balance_warnings": ["Conclude has only 4 outcomes — interview coverage may have been thin here."]
  },
  "audit_log": [
    {"op": "merge", "kept": "E-07", "dropped": ["T03-E-002", "T11-E-014"], "reason": "Same direction (Minimize) + same metric (likelihood) + same object (moving off the cut line). Different surface phrasing only."},
    {"op": "split", "from": "T04-P-009 ('time and effort to clean')", "to": ["P-12 (time)", "P-13 (effort)"], "reason": "Compound; both directions matter in the transcripts."},
    {"op": "rewrite", "from": "Minimize the likelihood that the laser guide drifts", "to": "Minimize the likelihood of moving off the cut line", "reason": "Embedded solution (laser guide)."},
    {"op": "drop", "candidate": "T08-E-022 ('I prefer the blue color')", "reason": "Preference, not an outcome on the job."}
  ],
  "next_step": "Run /generatesurvey on netted-outcomes.csv"
}
```

---

## Few-shot — a merge decision

Raw candidates from three different interviews:

| ID | Phrase |
|---|---|
| T02-E-005 | Minimize the likelihood that the blade drifts off the marked line |
| T07-E-012 | Minimize the likelihood I have to re-cut because the line went crooked |
| T11-E-003 | Minimize the chance of straying from the cut line |

All three: direction = Minimize, metric = likelihood, object = moving off the cut line. **Merge into one canonical outcome:**

> **E-08 — Minimize the likelihood of moving off the cut line when guiding the blade**

Log the three source IDs in the audit log so the reviewer can verify.

---

## Hard refuses

- Never produce a netted list with compound statements ("time and likelihood") surviving.
- Never produce a list with two different nouns for the same object (e.g., "tool" and "instrument" both appearing as the object — pick one).
- Never drop a candidate without logging the reason in `audit_log`.
- Never return a "final" netted list with fewer than 40 or more than 180 entries — the survey logistics break down at those extremes. Flag and request human guidance.
