---
name: whatdoido
description: Reverse lookup — the user describes what they currently have (files, data, prior outputs, current state) and this skill tells them exactly which command to run next. The "I'm holding something, what do I do with it?" navigator. Use when user says "I have X, what do I do?", "what should I run on this", "I'm stuck", "I have a CSV with [X] rows", etc.
when_to_use: User has SOMETHING (a file, partial outputs, a half-finished engagement, leftover data from somewhere else) and doesn't know what step they're on. Different from /odihelp (which routes from "I want to do X") — this routes from "I have X".
trigger_phrases:
  - /whatdoido
  - /whereami
  - "I have a CSV"
  - "what do I do with"
  - "I'm stuck"
  - "I'm not sure what's next"
  - "where am I in the process"
  - "I have this file"
  - "I have interview transcripts"
  - "I have survey data"
  - "what command should I run on"
  - "where am I"
  - "I finished the interviews"
  - "I have outcomes"
  - "I have a roadmap"
  - "I have segments"
  - "my survey is back"
  - "the panel results came in"
  - "what's the next step"
  - "what comes after"
inputs:
  - free-form description of what the user has OR the current working directory contents
outputs:
  - identifies the user's current phase (I through VII)
  - tells them the exact next command to run, with the file path argument filled in
  - flags any missing prerequisites
chains_to:
  - any plugin command, depending on diagnosis
---

# /whatdoido — "I have this, what's next?"

> **Plain English:** This skill is the *reverse* of `/odihelp`. `/odihelp` asks "what do you want to do?" — this skill asks "what do you currently have?" Use it when you've got a file or some output and you don't know which command to run on it.

## What it does

1. Looks at what the user describes (or scans the working directory for standard ODI files)
2. Figures out which phase of the engagement they're in
3. Tells them the **exact command** to run next, with the file path filled in
4. Flags any missing prerequisites and says how to fix them

## Phase detection logic

| If the user has… | They're in… | Run next |
|---|---|---|
| Just a problem in their head | Phase 0 | `/preflight` then `/definejob` |
| A locked job statement, no map yet | Phase I | `/identifycustomers` then `/buildjobmap` |
| Job map but no interviews/data | Pre-Phase II | `/generatescreener` (then go interview real people) |
| Interview transcripts (one file or many) | Phase II | `/extractoutcomes` on each transcript |
| Raw outcome CSV(s) from `/extractoutcomes` | Phase II late | `/netoutcomes` |
| A netted outcomes CSV, never validated | Phase II final gate | `/validateoutcomes` |
| A validated outcomes CSV, no survey yet | Phase II → III boundary | `/generatesurvey` |
| A survey instrument but no responses | Phase III mid | Field it; come back with the cleaned CSV |
| A survey response CSV (clean) | Phase III analysis | `/computescores` |
| `opportunity_scores.csv` but no segments | Phase IV | `/runsegmentation` |
| Segments + scores, no strategy yet | Phase V | `/competitiveanalysis` if competitor cols exist, then `/choosestrategy` |
| Strategy chosen, no value prop yet | Phase V mid | `/generatevalueprop --segment <id>` |
| Value prop + segment, no roadmap | Phase VI | `/buildroadmap` |
| Roadmap, but no engineering specs | Phase VII | `/outcometospec` per v1.0 outcome |
| All artifacts present but not bundled | Final | `/createodicanvas` then `/exportdeliverables` |
| Mixed / unclear / contradictory state | Diagnostic mode | Ask clarifying questions |

## Interaction pattern

1. **Read what the user said.** Look for filenames, file contents, mentions of files.
2. **Scan the working directory** if helpful: look for `netted-outcomes.csv`, `analysis-out/opportunity_scores.csv`, `roadmap-out/roadmap.csv`, etc.
3. **Identify the phase** using the table above.
4. **Output the exact next command** with the file path filled in.
5. **List the prerequisites** for that command. If any are missing, say so and offer the recovery command.
6. **If the state is ambiguous** (e.g., user has a CSV but it's not clear which kind), ask 1–2 clarifying questions.

## Output format

```json
{
  "skill": "whatdoido",
  "user_state_description": "I have a folder with 8 interview transcripts and a locked job statement.",
  "phase_detected": "Phase II — Uncover Needs",
  "next_command": "/extractoutcomes",
  "exact_command_with_args": "/extractoutcomes path/to/interview-01.txt   # run once per transcript",
  "prerequisites_met": ["locked job statement", "job map"],
  "prerequisites_missing": [],
  "after_this_step": "Combine the per-transcript outputs and run /netoutcomes",
  "alternative_paths": [
    "If you want a quick directional read instead of full analysis: /runliteodi <folder of transcripts>"
  ],
  "warning": null
}
```

## Few-shot examples

### Example A — User has interview transcripts

**User:** "I just finished 10 interviews about my product. I have transcripts. What do I do?"

**You:**
> You're in Phase II — Uncover Needs.
>
> Run `/extractoutcomes <path/to/transcript-01.txt>` once per transcript. That will pull candidate outcomes (in strict syntax) from each interview.
>
> After all 10 are extracted, combine the raw CSVs and run `/netoutcomes` to dedupe into 50–150 final outcomes.
>
> Prerequisites: you need the locked job statement and job map. Do you have those? If not, run `/definejob` first.

### Example B — User has survey data

**User:** "I have a CSV called survey-data.csv with about 400 rows."

**You:**
> Sounds like you're at the start of Phase III analysis.
>
> Before I send you to `/computescores`, two quick checks:
>
> 1. Does the CSV have columns named `imp_<outcome_id>` and `sat_<outcome_id>` for each outcome? (That's the schema `/computescores` expects.)
> 2. Has the data been cleaned (quality flags set, fraud filters applied)?
>
> If yes to both, run:
>
> `/computescores survey-data.csv`
>
> That will produce the ranked opportunity list + the Opportunity Landscape chart + WTP analysis. If the schema is different, tell me what columns you have and I'll help map them.

### Example C — Ambiguous state

**User:** "I have a CSV."

**You:**
> Cool — I just need a bit more context. Can you tell me:
>
> 1. **How many rows?** (under 50 → looks like outcomes; 200+ → looks like survey responses)
> 2. **What are the column names?** Or paste the first 2 rows.
> 3. **Where did it come from?** (Someone else handed it to you / output of a prior command / a panel provider export)
>
> Based on that I'll route you to the right command.

### Example D — User has everything except the engineering specs

**User:** "I've run computescores, runsegmentation, choosestrategy, generatevalueprop, and buildroadmap. What's next?"

**You:**
> You're one step from done. Phase VII.
>
> For each outcome in your `roadmap.csv` that ships in v1.0 (typically 5–12 outcomes), run:
>
> `/outcometospec <outcome_id_or_statement>`
>
> Each produces a 5-field engineering spec sheet (solution concept + acceptance criteria with the 20%-better target + success metric + engineering brief).
>
> Then close out with `/createodicanvas` (the one-page summary) and `/exportdeliverables` (the final bundle).

## Hard rules

- Always output the EXACT command the user should type, with the file path or argument filled in. Never make them guess.
- If prerequisites are missing, name them and the command to back up.
- If state is ambiguous, ask **at most 2** clarifying questions. Don't interrogate.
- If user is mid-engagement and clearly stuck, offer the alternative path (e.g., "if budget is the issue, switch to `/runliteodi`").
