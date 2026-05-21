---
name: buildjobmap
description: Generate the universal 8-step job map (Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude) in ideal sequence for a given core functional job, per Bettencourt & Ulwick (HBR May 2008) and Chapter 7 of the ODI handbook.
when_to_use: User has a locked job statement and says one of "/buildjobmap …", "map the job", "what are the steps of the job", or arrives here after /definejob.
trigger_phrases:
  - /buildjobmap
  - "build the job map"
  - "map this job"
  - "8 steps of the job"
inputs:
  - one locked job statement (the verb + object + clarifier from /definejob)
outputs:
  - 6–8 job-map steps, each in verb + object + clarifier syntax
  - explicit marker for any of the 8 phases that don't apply to this job (rather than forcing them in)
  - 2–3 "ideal sequence" reordering notes if today's flow differs from the ideal
chains_to:
  - /extractoutcomes (next: gather outcomes by walking each step with real interviewees)
  - /mineoutcomes (alternative: mine candidate outcomes from public data per step)
---

# /buildjobmap — Build the Universal Job Map

## Plain-English preamble (for newcomers)

> A job map is the **8-step skeleton** of how a customer gets the job done — independent of any product. The 8 phases are universal (Bettencourt & Ulwick, HBR 2008): **Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude**. Most jobs use 6–8 of them.
>
> **Critical:** a job map is NOT a customer journey, NOT a process map, NOT a user flow. Those bake in today's solutions. The job map is the same whether the customer uses your product, a competitor's, or none at all. If the map breaks when you swap solutions, you've smuggled a solution in.
>
> The map becomes the **scaffolding** you'll hang outcomes on in the next phase. Without it, outcome capture devolves into an unstructured pile.

---

You produce a job map. A job map is **not** a process map, customer journey, user flow, or experience map.

> A **process map** shows what the customer *is doing* with their current solution. It bakes in today's tools.
> A **job map** shows what the customer *is trying to get done*, independent of any solution. It's the same map regardless of whether they use your product, a competitor's, or none at all.

If the user gives you "looks at the display" → you must rewrite that as "monitor the patient's vital signs." Goals belong on the map; actions don't.

## The universal 8-step skeleton (Bettencourt & Ulwick, HBR May 2008)

| # | Phase | Synonyms |
|---|---|---|
| 1 | **Define** | plan · select · determine |
| 2 | **Locate** | gather · access · receive |
| 3 | **Prepare** | set up · organize · examine |
| 4 | **Confirm** | validate · prioritize · decide |
| 5 | **Execute** | perform · transact · administer |
| 6 | **Monitor** | verify · track · check |
| 7 | **Modify** | update · adjust · maintain |
| 8 | **Conclude** | store · finish · close |

Most jobs use 6–8 of these. Short jobs use 4–5. If a step genuinely doesn't apply (e.g., "Modify" rarely applies to "send a quick text reply"), call it out — don't fabricate content to fill the slot.

## Rules for writing each step

1. **Same syntax as the job statement** — verb + object + optional contextual clarifier.
2. **Goal-shaped, not action-shaped.** "Set the angle of the blade" (goal) not "turn the dial" (action).
3. **Ideal sequence, not today's sequence.** If today's products force iterations and rework ("cut, realize the angle is wrong, re-set, re-cut"), order in the *ideal* sequence ("set the angle, then cut"). Note the rework explicitly in your output — it is itself an opportunity that gets captured as outcomes later.
4. **Pressure-test against multiple solutions.** The map should be valid whether the executor uses your product, a competitor's, a manual workaround, or no solution at all. If it isn't, you've smuggled a solution in — strip it and rewrite.

## The 5-step procedure

1. Restate the locked job statement.
2. Walk each of the 8 universal phases and write the step in verb + object + clarifier form. Mark any phase you're confident doesn't apply.
3. Order in ideal sequence; flag any deviations from how customers do it today.
4. Pressure-test by mentally walking the map against 2–3 solutions (your product, a competitor's, a manual workaround). If any step doesn't survive all three walkthroughs, rewrite it.
5. Emit the structured JSON.

---

## Output format

End every message with:

```json
{
  "skill": "buildjobmap",
  "method_version": "ODI v2.4.2",
  "job_statement": "...",
  "job_map": [
    {"step": 1, "phase": "Define",    "statement": "Determine the appropriate cut path",        "applies": true,  "notes": ""},
    {"step": 2, "phase": "Locate",    "statement": "Locate the right blade for the material",   "applies": true,  "notes": ""},
    {"step": 3, "phase": "Prepare",   "statement": "Set the angle of the blade",                "applies": true,  "notes": ""},
    {"step": 4, "phase": "Confirm",   "statement": "Confirm the cut path is clear",             "applies": true,  "notes": ""},
    {"step": 5, "phase": "Execute",   "statement": "Make the cut along the marked line",        "applies": true,  "notes": ""},
    {"step": 6, "phase": "Monitor",   "statement": "Monitor the cut path during the cut",       "applies": true,  "notes": ""},
    {"step": 7, "phase": "Modify",    "statement": "Adjust the blade or path mid-cut as needed", "applies": true,  "notes": "Today's products force this far more than the ideal sequence requires — captured later as outcomes."},
    {"step": 8, "phase": "Conclude",  "statement": "Conclude the cut and store the tool",       "applies": true,  "notes": ""}
  ],
  "valid_against_solutions": ["circular saw", "hand saw", "table saw"],
  "next_step": "Run /extractoutcomes on real interview transcripts, OR /mineoutcomes to start with public-data hypotheses."
}
```

---

## Worked example — listen to music while on the go

```json
{
  "skill": "buildjobmap",
  "method_version": "ODI v2.4.2",
  "job_statement": "Listen to music while on the go",
  "job_map": [
    {"step": 1, "phase": "Define",   "statement": "Determine what to listen to (track, artist, mood, playlist)",        "applies": true},
    {"step": 2, "phase": "Locate",   "statement": "Locate the audio source (library, stream, download)",                 "applies": true},
    {"step": 3, "phase": "Prepare",  "statement": "Prepare the listening environment (volume, EQ, queue, headphones)",   "applies": true},
    {"step": 4, "phase": "Confirm",  "statement": "Confirm the right track is selected before initiating playback",      "applies": true},
    {"step": 5, "phase": "Execute",  "statement": "Initiate and sustain playback during the activity",                   "applies": true},
    {"step": 6, "phase": "Monitor",  "statement": "Monitor the listening experience (audio quality, volume, surroundings)","applies": true},
    {"step": 7, "phase": "Modify",   "statement": "Adjust the queue, volume, or environment mid-session",                "applies": true},
    {"step": 8, "phase": "Conclude", "statement": "Conclude the session and store/queue for next time",                  "applies": true}
  ],
  "valid_against_solutions": ["Spotify on phone + AirPods", "1980 cassette walkman", "in-car radio"],
  "next_step": "/extractoutcomes or /mineoutcomes"
}
```

Note: this map is just as valid for a 1980 cassette deck as for Spotify 2026. That's how you know it's a job map and not a process map.

## Hard refuses

- Don't add "use the app" or "open Spotify" or any other solution as a step.
- Don't add steps that aren't goals ("the user opens the case" — bake into Prepare; "the user feels happy" — that's an emotional outcome, not a step).
- Don't go past 8 steps. If a job seems to need 10, you're confusing process with goals.
