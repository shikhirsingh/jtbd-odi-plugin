---
description: PHASE II — Pull candidate desired-outcome statements (in strict Ulwick syntax) from interview transcripts. Accepts EITHER one file OR a directory of transcripts (.txt, .md, .vtt, .srt) — batches the whole folder into one combined raw-outcomes CSV. (Ch 11 + 14)
argument-hint: <single transcript file OR a directory containing transcript files>
---

# /extractoutcomes — Transcript(s) → candidate outcomes

## What this is doing (plain English)

Customer interviews are typically 60 minutes each and contain 25–40 measurable pain points buried in natural language. This skill mines them out and converts each into the strict 4-part outcome syntax: **Direction (Minimize/Increase) + Metric (time/likelihood/...) + Object + (optional) Clarifier**.

**Two ways to invoke it:**

```bash
# One transcript at a time
/extractoutcomes interviews/jane-2026-05-01.txt

# OR a whole folder at once (recommended)
/extractoutcomes interviews/
```

If you pass a directory, the skill batch-processes every transcript file in it (`.txt`, `.md`, `.vtt`, `.srt`, plain-text exports) and produces ONE combined `raw-outcomes.csv`. Every candidate has a `source_transcript` column so you can trace it back.

After the batch, the skill prints a per-phase coverage summary and flags any job-map step where interviews were thin.

## What you need before running this

- The **locked job statement** from `/definejob`
- The **job map** from `/buildjobmap`
- **One transcript file OR a folder of transcripts.** Otter, Whisper, Granola, Fireflies, Notta, Trint — all produce transcripts in supported formats.

If any of these is missing, the skill asks before extracting.

## What you'll get back

- **`raw-outcomes.csv`** — combined candidates across all transcripts, with `source_transcript` and source-line columns
- A per-transcript summary (how many candidates each interview yielded — useful for spotting weak interviews)
- A per-phase coverage histogram (which job-map steps were under-covered)
- Separate sections for related jobs / emotional-social / consumption-chain / financial outcomes

## What runs after this

Combine across all transcripts (already done if you used directory mode) → run `/netoutcomes` to dedupe to 50–150 final outcomes.

---

Invoke the `extractoutcomes` skill. If the user passed a directory, glob for transcript files inside it (`.txt`, `.md`, `.vtt`, `.srt`, plain-text exports) and process each one, tagging candidates with their source filename. If the locked job statement or job map isn't in conversation context, ask before extracting. End with a per-phase coverage histogram.
