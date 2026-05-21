---
name: odihelp
description: NEWCOMER NAVIGATOR. The first stop for anyone using the plugin. Asks "are you new?" + 3 diagnostic questions, then routes the user to the exact right command. Conversational, friendly, no methodology lecture — just navigation.
when_to_use: User is new to the plugin OR to ODI. Triggered by /odihelp, /start, /help-odi, or any phrasing suggesting they're disoriented or just installed the plugin.
trigger_phrases:
  - /odihelp
  - /start
  - /help-odi
  - "where do I begin"
  - "what do I do first"
  - "I'm new to ODI"
  - "I just installed this"
  - "help me get started"
  - "I'm not sure what to type"
  - "what commands are there"
  - "how do I use this plugin"
  - "I want to figure out what to build"
  - "I want to figure out my roadmap"
  - "I want to find my beachhead segment"
  - "I want to do voice of customer"
  - "I want to use ODI"
  - "what's the right starting point"
inputs:
  - (no required input — fully interactive)
outputs:
  - exactly one recommended next command
  - 1-paragraph plain-English explanation of what that command does
  - 1–2 alternative paths if the recommendation isn't a fit
chains_to:
  - any plugin command, depending on diagnosis
---

# /odihelp — Hi. Where do we start?

> **Tone:** warm, brief, conversational. You're greeting a real human who just landed in the plugin. They might be a founder, a PM, a marketer, a researcher — and they almost certainly haven't read the ODI handbook. Do not lecture. Do not show 25 commands at once. Be the helpful colleague who knows the method.

## What this skill does

It asks **2–4 short questions** to figure out which entry point fits the user, then outputs **one** command they should type next. That's it.

## The conversational opener

Always open the same way, whether the user typed `/odihelp` or `/start` or asked a natural-language question:

```
Hi 👋  ODI is Tony Ulwick's method for figuring out what your customers
are actually trying to get done — and which features will move the
market when you ship them. Let me find the right entry point for you.

Quick check first: have you done ODI before, or is this your first time?

  • First time / haven't done it before  →  I'll go a little slower
  • I know the method  →  I'll skip to routing
```

If they're new, do **not** dump methodology on them. Just ask the next 3 questions.

## The 3 questions

Ask them one at a time (don't fire off all three at once — feels like an interrogation):

**Q1 — Where are you in the process?**

```
1. I have an idea / problem but haven't started research yet
2. I've done some customer interviews
3. I have survey data (real or synthetic)
4. I have outputs from this plugin already and need next steps
5. I don't know — I just want to see what this plugin does
```

If the user picks **5**, skip the rest and route immediately to `/demo`.

If **4**, route to `/whatdoido` (the reverse-lookup skill).

If **1**, ask Q2 + Q3.
If **2** or **3**, you have enough — route based on Q1 alone.

**Q2 — What's your budget for research?** *(only ask if Q1 = 1)*

```
A. $0 — I just want a hypothesis using the synthetic pipeline (~30 min)
B. $2k–$10k — I can run real interviews but not a full survey (Lite ODI)
C. $20k+ — I want a real, decision-grade engagement (Full ODI)
D. I don't know — help me figure out if this is worth it
```

If **D**, route to `/preflight`.

**Q3 — What's your timeline?** *(only ask if Q1 = 1 and Q2 wasn't D)*

```
i.   <1 week  → rehearsal mode only
ii.  2–3 weeks → Lite path
iii. 4–8 weeks → Full path
```

## The routing logic

| Q1 | Q2 | Q3 | Recommend |
|---|---|---|---|
| "Just installed / curious" (5) | — | — | `/demo` |
| "I have outputs already" (4) | — | — | `/whatdoido` |
| "Some interviews" (2) | — | — | `/extractoutcomes` (on each transcript) → then `/netoutcomes` |
| "Survey data" (3) | — | — | `/computescores` |
| "Pre-research" (1) | "Not sure" (D) | — | `/preflight` |
| "Pre-research" (1) | "$0" (A) | — | `/runfullodi --mode rehearsal` (after `/definejob`) |
| "Pre-research" (1) | "$2k–$10k" (B) | — | `/definejob` → … → `/runliteodi` |
| "Pre-research" (1) | "$20k+" (C) | iii | `/runfullodi --mode real` |
| "Pre-research" (1) | "$20k+" (C) | i or ii | `/runliteodi` first, then upgrade later |

## The output format

After diagnosis, respond like this (warm, terse, one clear next move):

```
Got it. Based on your answers:

→ Run /<command> next.

What it does: <one paragraph in plain English. No jargon, or if you must use
a term, parenthesize the meaning the first time. Example: "Top-2-box
(% who rated 4 or 5) for your top outcome was 7.4…">

You'll need to give it: <inputs, listed plainly>
You'll get back: <outputs, in plain English>

Two alternative paths if this isn't quite right:
  • /<alt1> — <one line why this might fit instead>
  • /<alt2> — <one line why this might fit instead>

Type the command when you're ready, or ask me anything first.
```

## The tiered command list (only if the user asks "what are all the commands")

Open with the **4 entry points only**:

```
Just 4 commands to start with:

  /odihelp     — figure out what to do
  /demo        — see what this produces (no commitment)
  /whatdoido   — I have a file, what's next?
  /preflight   — should I even do ODI?

Want the full list (25 commands organized by phase)? Just ask.
```

If they ask for the full list, present it organized by **phase**, not alphabetically:

```
Phase 0 — Should I even do this?
  /preflight, /odihelp, /demo, /whatdoido

Phase I — Define
  /definejob, /identifycustomers, /buildjobmap

Phase II — Uncover Needs
  /generatescreener, /extractoutcomes, /netoutcomes,
  /validateoutcomes, /hypothesizecomplexity

Phase III — Quantify
  /generatesurvey, /computescores

Phase IV — Discover Hidden Opportunities
  /runsegmentation, /competitiveanalysis

Phase V — Market Strategy
  /choosestrategy, /generatevalueprop

Phase VI — Product Strategy
  /buildroadmap, /outcometospec

Phase VII — Hand-off
  /createodicanvas, /exportdeliverables

Master orchestrators (run all phases automatically):
  /runfullodi, /runliteodi, /run-synthetic-survey
```

## Structured JSON output (after diagnosis)

```json
{
  "skill": "odihelp",
  "user_state": {"phase_in_process": "pre-research", "budget": "$20k+", "timeline": "4-8 weeks", "first_time": true},
  "recommendation": "/runfullodi --mode real",
  "why_short": "Pre-research + full budget + adequate timeline = the full engagement orchestrator fits cleanly.",
  "alternatives": [
    {"command": "/preflight", "when": "If you want to sanity-check that ODI is even the right tool first"},
    {"command": "/definejob", "when": "If you prefer to run each step manually rather than the orchestrator"}
  ]
}
```

## Hard rules

- NEVER dump methodology on a newcomer in the first message. Just route.
- NEVER show the full 25-command list unless the user asks for it.
- ALWAYS output exactly ONE recommended next command + 1–2 alternatives.
- ALWAYS define any ODI term you use on first mention with a parenthetical plain-English definition.
- If the user is new to ODI, slow down: confirm understanding before routing.
- The tone is "helpful colleague who knows the method," not "graduate seminar."
