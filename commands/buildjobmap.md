---
description: STEP 3 — Break the locked job statement into the 8 universal job-map steps (Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude). The job map becomes the scaffolding for collecting outcomes in the next phase. (Ch 7)
argument-hint: <locked job statement from /definejob, e.g., "Cut a piece of wood in a straight line">
---

# /buildjobmap — The 8-step job map

## What this is doing (plain English)

You've got the job. Now we break it into the steps any customer would walk through to get the job done — regardless of which product they use. This map is the *skeleton* your outcomes will hang on later.

Bettencourt & Ulwick (HBR, May 2008) showed that almost every functional job decomposes into the same 8 phases: **Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude**. Most jobs use 6–8 of them.

The map is solution-agnostic. The job of "listening to music" has the same map whether the customer uses a 1980 cassette walkman or Spotify in 2026.

## What you need before running this

- Your locked job statement from `/definejob`. If you don't have one yet, run `/definejob` first.

If you paste just a topic ("listening to music"), the skill will ask you to lock the job statement properly first.

## What you'll get back

- 6–8 steps in verb + object + clarifier syntax, in the ideal sequence
- Any of the 8 universal phases that genuinely don't apply to your job, marked explicitly (don't fabricate)
- 2–3 "today's reality" callouts where the ideal sequence diverges from how customers actually do it (those gaps become opportunities later)

## Jargon you'll see

- **Process map vs. job map** — a *process map* shows what the customer does with their current solution (bakes in today's tools). A *job map* shows what they're trying to accomplish (solution-agnostic). They look similar; they're not the same.
- **Ideal sequence** — the order the customer would do the steps if everything went smoothly. If today's products force re-work ("cut, realize the angle is wrong, re-cut"), order it as it *should* be — the rework is itself an opportunity captured later.

## What runs after this

- `/extractoutcomes` if you have real interview transcripts (real ODI)
- `/mineoutcomes` if you want a synthetic first pass

---

Invoke the `buildjobmap` skill with the locked job statement. If the user pasted something that isn't yet a proper job statement, route them back to `/definejob` first.
