---
name: extractoutcomes
description: Extract candidate desired-outcome statements (in strict Ulwick syntax) from interview transcripts. Accepts EITHER a single transcript file OR a directory containing many transcript files (.txt, .md, .vtt, .srt, .docx-extracted-text) — batch processes all of them and emits a combined raw-candidates CSV. Implements Ch 11 + Ch 14. Aliased as /interviewtooutcomes.
when_to_use: User has run real qualitative interviews and points the skill at either ONE transcript file OR a FOLDER of transcripts. Invoke when they say /extractoutcomes, /interviewtooutcomes, "pull outcomes from this interview", "process all my interview files", "I have a folder of transcripts".
trigger_phrases:
  - /extractoutcomes
  - /interviewtooutcomes
  - "pull outcomes from"
  - "extract outcomes"
  - "translate this transcript into outcomes"
  - "I have a folder of transcripts"
  - "process all my interviews"
  - "batch extract outcomes"
  - "all my interview files"
inputs:
  - EITHER a single transcript file path
  - OR a directory path containing 1..N transcript files (.txt, .md, .vtt, .srt, plain-text exports of .docx)
  - the locked job statement (from /definejob)
  - the job map (from /buildjobmap) — used to assign each outcome to a step
outputs:
  - ONE combined raw-candidates CSV across all transcripts processed
  - per-transcript breakdowns within the CSV (a `source_transcript` column lets you trace each candidate back)
  - per-transcript candidate-count summary surfaced at the end
  - the also-captured buckets: related jobs, emotional/social jobs, consumption-chain outcomes, financial outcomes
  - balance warning if any job-map step has 0 candidates after processing the whole batch (interview coverage gap)
chains_to:
  - /netoutcomes (combined output goes straight into netting)
---

# /extractoutcomes — Interview Transcript → Outcome Candidates

## Plain-English preamble (for newcomers)

> A 60-minute customer interview has 5–40 measurable pains buried in natural language. This skill mines them out and converts each into the strict 4-part outcome syntax: **Direction (Minimize|Increase) + Metric (time|likelihood|...) + Object + (optional) Clarifier**.
>
> Run this skill ONCE PER TRANSCRIPT. After all transcripts (typically 8–25), combine and run `/netoutcomes` to dedupe to 50–150 final outcomes.
>
> **Why strict syntax?** Survey respondents need to be rating the same thing, not your wording variations. Ulwick has documented that "reduce / prevent / eliminate" produce measurably different ratings even though they look synonymous. So we standardize on **Minimize** and **Increase** only.
>
> **You'll also separately capture:** related jobs (other jobs at the same time), emotional/social jobs, consumption-chain outcomes (install / maintain / dispose), and financial outcomes (for B2B buyer).

---

Your job is to translate raw customer language into well-formed **desired outcome statements** that will survive into the survey instrument unchanged.

You are not summarising. You are not paraphrasing for clarity. You are extracting the customer's measure of success and forcing it into the four-part syntax.

---

## The strict outcome syntax (Chapter 11)

```
direction of improvement + metric + object of control + (optional) contextual clarifier
```

| Part | Allowed values |
|---|---|
| Direction | **Minimize** or **Increase** (pick one verb per direction and use it everywhere — never "reduce / prevent / eliminate" as substitutes) |
| Metric | Almost always the **time** or the **likelihood**. Occasionally the number, the frequency, the amount. Covers ~90% of cases. |
| Object of control | The noun phrase the metric attaches to — the thing being measured. |
| Contextual clarifier | "…when X" / "…during Y" / "…e.g., from a ladder, rafter, etc." |

### Examples that pass

- *Minimize* the time it takes to *get the songs in the desired order for listening*
- *Minimize* the likelihood that *the music sounds distorted when played at high volume*
- *Minimize* the time it takes to *set the angle of the blade*, e.g., make a bevel adjustment
- *Minimize* the likelihood that *debris flies up into the user's face when guiding the blade along the cut line*
- *Increase* the likelihood that *the cut path is clear before initiating the cut*

### Common rewriting moves (Chapter 11, Table 11.3)

| Raw customer quote | Properly formatted outcome |
|---|---|
| "It takes forever to find the right setting" | Minimize the time it takes to identify the appropriate setting for the cut |
| "I hate when the cord gets caught on stuff" | Minimize the likelihood that the cord snags on the material when making a long cut |
| "I want to know if I'm bleeding too much" | Minimize the likelihood that excessive bleeding goes undetected during the procedure |
| "The thing should be lighter" | Minimize the physical effort required to position the saw before initiating the cut |

### The 10 characteristics of a perfect outcome (Table 11.2)

1. Stable over time (still meaningful in 20 years)
2. Reveals a metric (time, likelihood, etc.)
3. Devoid of solutions (no product names / technologies / features)
4. Measurable
5. Controllable
6. Actionable
7. One-dimensional (one direction, one metric, one object — no compound statements)
8. Mutually exclusive (does not duplicate another statement)
9. Customer-stated value
10. Useful across functions (PM, marketing, engineering, sales)

### Hidden sources of variability to strip (Table 11.4)

| Sin | Example | Fix |
|---|---|---|
| Interchangeable direction verbs | "reduce" / "prevent" / "eliminate" | Always use **Minimize** or **Increase** |
| Vague adjectives | "frequently", "significantly", "excessive" | Remove or replace with a contextual clarifier |
| Inconsistent nouns | "tool" / "instrument" / "device" | One name per object across the whole list |
| Compound statements | "Minimize the time AND effort to set the blade angle" | Split into two outcomes |
| Embedded solutions | "Minimize the likelihood that the laser guide drifts" | "Minimize the likelihood of moving off the cut line" |

---

## How to work

### A. Detect input mode — file or directory

The first thing to do is check whether the user pointed at a **file** or a **directory**:

```bash
# In your skill orchestration:
if path is a directory:
    find all *.txt, *.md, *.vtt, *.srt, *.transcript files inside (recursively, depth 2)
    for each file: run the extraction routine; tag each candidate with source_transcript = filename
    combine all candidates into one CSV
elif path is a single file:
    run the extraction routine once; source_transcript = filename
else:
    error → ask the user to provide a valid path
```

The user should be able to type either:

```
/extractoutcomes interviews/jane-2026-05-01.txt
```

OR

```
/extractoutcomes interviews/          # processes every file in the folder
```

For a directory with 15 transcripts, the skill produces ONE combined `raw-outcomes.csv` with ~400 candidates — ready for `/netoutcomes` without manual concatenation.

### B. Per-transcript extraction routine

For each transcript:

1. **Confirm you have the job statement and the job map.** If not, ask for them or invoke `/definejob` and `/buildjobmap` first.
2. **Read the transcript line by line.** Mark every phrase where the customer expresses:
   - A pain ("it takes forever…", "I hate when…", "what slows me down is…")
   - A measure of success ("I want to know when…", "I need it to…")
   - An anchor to a job step (referenced phase, e.g., "right before I start cutting…")
3. **For each marked phrase, propose an outcome candidate.** Convert verbatim → strict syntax using the rewriting moves above.
4. **Assign to a job-map step.** Use the job map you received. If a candidate doesn't fit any step on the map, flag it — it's either an emotional job, a related job, a consumption-chain outcome, or a financial outcome (Chapter 12, 13).
5. **Also capture, separately:**
   - **Related jobs** (other functional jobs at the same time): 5–20 expected
   - **Emotional/social jobs**: 5–25 expected
   - **Consumption-chain outcomes**: research → purchase → install → train → use → maintain → upgrade → repair → dispose
   - **Financial outcomes** (B2B, big-ticket B2C): cost, ROI, switching cost, risk
6. **Preserve the source.** Every candidate keeps the raw quote, its line/timestamp, AND its source_transcript filename so the human reviewer can verify.

Aim for ~25–40 candidates per 60-minute interview transcript. Don't pre-dedupe — netting happens in /netoutcomes.

### C. After the batch, surface a summary

For a directory run, end with:

```
Processed 15 transcripts:
  jane-2026-05-01.txt       — 38 candidates
  amir-2026-05-02.txt       — 31 candidates
  ...
  Total raw candidates: 412
  Combined CSV: raw-outcomes.csv

Coverage check:
  Define     ████████████ 47
  Locate     ██████░░░░░░ 22
  Prepare    ██████████░░ 38
  Confirm    ███░░░░░░░░░ 11   ⚠️ thin — your interviews may have skipped this phase
  Execute    ████████████ 89
  Monitor    █████░░░░░░░ 18
  Modify     ███████░░░░░ 26
  Conclude   ███░░░░░░░░░ 9    ⚠️ thin

Suggested next step:
  /netoutcomes raw-outcomes.csv
```

---

## Output format

```json
{
  "skill": "extractoutcomes",
  "method_version": "ODI v2.4.2",
  "job_statement": "...",
  "transcript_source": "interview-01-2026-05-12.txt",
  "outcome_candidates": [
    {
      "candidate_id": "T01-D-001",
      "job_step": "Define",
      "direction": "Minimize",
      "metric": "time it takes to",
      "object_of_control": "determine the appropriate cut path",
      "clarifier": "before initiating any cut",
      "full_statement": "Minimize the time it takes to determine the appropriate cut path before initiating any cut",
      "source_quote": "I'll stand there for two minutes figuring out where I'm supposed to start the cut, even when I've done it a hundred times.",
      "source_locator": "line 42",
      "characteristics_check": {
        "stable": true, "metric_revealed": true, "solution_free": true,
        "measurable": true, "controllable": true, "actionable": true,
        "one_dimensional": true, "customer_stated": true
      }
    }
  ],
  "related_jobs": [
    {"statement": "Time the cut so it finishes before the cordless battery dies"}
  ],
  "emotional_social_jobs": [
    {"type": "emotional", "statement": "Avoid feeling rushed when making a finish cut on a client's project"},
    {"type": "social",    "statement": "Be perceived as a careful tradesman by the project supervisor"}
  ],
  "consumption_chain_outcomes": [
    {"phase": "maintain", "statement": "Minimize the time it takes to swap a worn blade"}
  ],
  "financial_outcomes": [
    {"statement": "Minimize the per-cut consumable cost when working on hardwoods"}
  ],
  "stats": {
    "total_candidates": 34,
    "candidates_per_step": {"Define": 6, "Locate": 3, "Prepare": 7, "Confirm": 2, "Execute": 8, "Monitor": 4, "Modify": 3, "Conclude": 1},
    "flagged_for_review": 2
  },
  "next_step": "Repeat for remaining transcripts, then run /netoutcomes on the combined raw set."
}
```

---

## Few-shot

**User pastes 3 lines of transcript:**
> R: "I always cut a little off the line because I can't see where the blade is going. Sometimes there's so much sawdust in the way I just have to guess. And then if I'm on a ladder I'm worried about dropping the thing."

**You produce:**

| ID | Step | Outcome |
|---|---|---|
| T01-E-001 | Execute | Minimize the likelihood of moving off the cut line when guiding the blade |
| T01-E-002 | Execute | Minimize the likelihood that debris obscures the cut line during the cut |
| T01-C-001 | Conclude | Minimize the likelihood of dropping the saw when lowering it from a ladder |

Note that "Sometimes I just have to guess" became *Minimize the likelihood that debris obscures the cut line*, not a compound "minimize the time and likelihood I have to guess." One direction, one metric, one object per row.

---

## Hard rules

- Never invent outcomes the transcript doesn't support. If you would have to fabricate the customer's intent, flag the line and leave it out.
- Never declare candidates "final" — only /netoutcomes does that.
- Never combine two raw quotes into one outcome unless they refer to the same direction, metric, and object — call out the alternative as a separate row.
