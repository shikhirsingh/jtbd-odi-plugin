# GUIDE — How to use this plugin (for newcomers)

> If you've never done ODI before, read this once. It takes 10 minutes. After that you can use the plugin without re-reading.

---

## What ODI actually is, in three sentences

ODI (Outcome-Driven Innovation) is a research method, invented by Tony Ulwick in 1990. You **define the functional job** a customer is trying to get done, **collect 50–150 specific things they're trying to accomplish on that job** ("desired outcomes"), then **survey 300–600 of them** to score every outcome by **importance × satisfaction**. The math tells you which outcomes are most under-served — and therefore which features will move the market when you ship them.

If that sounds like a lot — it is. A full ODI engagement takes 4–8 weeks and costs $20k–$80k in panel/incentive fees. The payoff is a roadmap, value proposition, pricing band, and engineering specs that all trace to defensible data instead of opinion.

The plugin runs every step of the method for you. It doesn't replace the human research (real interviews, real survey respondents) — it replaces the *work* of running and analyzing them.

---

## The three paths

You almost certainly want one of these three. Pick the one that fits your reality before you start typing commands.

### Path A — Full ODI (`/runfullodi --mode real`)

For when you have budget and time:

- **Time:** 4–8 weeks
- **Budget:** $20k–$80k (panel/incentive fees + your team's time)
- **What you get:** decision-grade. Roadmap and pricing you can bet the company on.
- **When to use:** picking which v1 features to ship; finding a beachhead segment; re-pricing into a market with a new job-done quality; entering a new market.

### Path B — Lite ODI (`/runliteodi`, alias `/lite`)

For when you have less budget but real interviews are possible:

- **Time:** 2–3 weeks
- **Budget:** $2k–$10k (incentives for ~15 interviews; no panel survey)
- **What you get:** directional. Confidence to commit to interviews-only research; informs which questions a future survey should ask.
- **When to use:** seed-stage startups, pivots, new categories where panel providers don't have your audience yet.

### Path C — Rehearsal / Synthetic (`/run-synthetic-survey`, alias `/synthsurvey`)

For when you want a hypothesis before committing any money:

- **Time:** 30–60 minutes
- **Budget:** $0 (LLM cost only)
- **What you get:** a hypothesis. Stamped SYNTHETIC on every file. Cannot make decisions on it.
- **When to use:** stress-testing your survey instrument; deciding which interviews to commission first; team rehearsing the method before a real engagement.

> ⚠️ **The synthetic path is hypothesis-only.** It mines public posts (Reddit, Amazon reviews, app stores), synthesizes personas, has them "take" a survey, and outputs a CSV in the same shape a real survey would produce. The opportunity scores it produces will reflect LLM training-data biases, not market reality. Use it to prepare; never to decide.

---

## Not sure which path? Run `/preflight`

`/preflight` walks you through Ulwick's Ch 4 checklist (when ODI is right, when it isn't) and recommends one of the three paths above — or tells you ODI isn't the right method and points you somewhere else. Spend 5 minutes on it.

If you're really stuck, just type `/odihelp` (or `/start`). It asks three diagnostic questions and routes you.

---

## The journey, end to end

Here's the entire ODI process as the plugin runs it. Each row is one slash command. The arrows mean "produces what the next step needs."

```
                  PRE-FLIGHT
                       │
                  /preflight  ──→  go / lite / rehearsal / no-go
                       │
        ┌──────────────┴──────────────┐
        │                             │
   PHASE I — Define                   │
        │                             │
   /definejob      "Cut a piece of wood in a straight line"
        │
   /identifycustomers   executor + lifecycle + buyer
        │
   /buildjobmap         8 ideal steps: Define → Locate → Prepare …
        │
   PHASE II — Uncover Needs
        │
   /generatescreener    who you'll recruit + how
        │
   ─── recruit 20–30 real executors ───   (real mode pauses here)
        │
   /extractoutcomes     run on each transcript → ~400 raw outcomes
        │
   /netoutcomes         clean / dedupe to 50–150 outcomes
        │
   /validateoutcomes    Ch 11 hard gate — fix any failures
        │
   /hypothesizecomplexity   propose 8–15 complexity factors
        │
   PHASE III — Quantify
        │
   /generatesurvey      build the survey for Qualtrics/Typeform
        │
   ─── field to n=300–600 real respondents ───   (real mode pauses)
        │
   /computescores       opportunity scores + landscape + WTP
        │
   PHASE IV — Discover Hidden Opportunities
        │
   /runsegmentation     factor analysis + k-means
        │
   /competitiveanalysis where competitors win/lose per outcome
        │
   PHASE V — Market Strategy
        │
   /choosestrategy      Growth Matrix → Differentiated/Disruptive/etc.
        │
   /generatevalueprop   the 4-part value prop sentence
        │
   PHASE VI — Product Strategy
        │
   /buildroadmap        outcome-attack plan with the 7 product moves
        │
   PHASE VII — Execution
        │
   /outcometospec       per outcome → engineering spec sheet (×5–12)
        │
   /createodicanvas     the 1-page board-ready summary
        │
   /exportdeliverables  bundle the 6 Table 30.1 artifacts
        │
   ─── 6 months later ───
        │
   /computescores re-run to measure whether engineering moved the outcomes.
```

---

## The six artifacts you walk out with

The plugin guarantees you leave with these six things (Table 30.1 of the handbook). `/exportdeliverables` refuses to ship the bundle if any are missing.

| # | Artifact | What it is | Used by |
|---|---|---|---|
| 1 | **Ranked opportunity list** | 50–150 outcomes scored 0–20, sorted | PM — what to build first |
| 2 | **Outcome-based segments** | 2–5 customer groups defined by unmet-need patterns | Marketing + sales — targeting |
| 3 | **Strategic posture** | One of: Differentiated / Dominant / Disruptive / Discrete / Sustaining | Leadership — investment alignment |
| 4 | **Outcome-based value proposition** | A four-part sentence that traces to data | Marketing — copy + sales talk |
| 5 | **Outcome-attack roadmap** | Each outcome paired with one of the 7 product moves + a release | PM — planning |
| 6 | **Engineering specs** | Per outcome: solution concept + measurable acceptance criteria + success metric + engineering brief | Engineering — build |

Plus a **Canvas** (one-page summary), an **executive summary**, and a **coverage report** that proves all six artifacts are present.

---

## The 7 capabilities you walk out with

After running through, you'll be able to:

1. **Know what to build** — ranked opportunity list + per-segment landscapes.
2. **Identify the beachhead segment** — outcome-based segmentation.
3. **Price into the WTP band** — from the survey's WTP block + `/choosestrategy.pricing_band`.
4. **Hand engineering a measurable target** — `/outcometospec` with the 20%-better acceptance criteria.
5. **Write marketing copy that lands** — `/generatevalueprop` + marketing variants.
6. **Choose strategic posture with evidence** — Growth Strategy Matrix placement.
7. **Run it again, faster next time** — your outcome library and survey instrument export with the bundle and are reusable on the next engagement.

---

## A 90-second "what is each command for?" cheat-sheet

| Command | Plain-English purpose |
|---|---|
| **`/odihelp`** (or `/start`, `/help-odi`) | Newcomer navigator — tells you which command to run |
| **`/preflight`** (or `/odicheck`) | Is ODI even right for your situation? |
| **`/definejob`** | Write the one-sentence functional job statement |
| **`/identifycustomers`** | Name the executor / lifecycle / buyer for B2B engagements |
| **`/buildjobmap`** | Break the job into the 8 universal steps |
| **`/extractoutcomes`** | Pull candidate outcomes from one interview transcript |
| **`/netoutcomes`** (or `/refineoutcomes`) | Dedupe + clean 300+ raw candidates → 50–150 final outcomes |
| **`/validateoutcomes`** | Confirm the outcomes are survey-ready (10 quality characteristics) |
| **`/generatescreener`** | Build the recruiting screener |
| **`/hypothesizecomplexity`** (or `/complexityfactors`) | Propose the situational variables that drive segmentation |
| **`/generatesurvey`** | Build the survey instrument for Qualtrics/Typeform |
| **`/computescores`** (or `/opportunitylandscape`) | The opportunity formula in action — ranks every outcome |
| **`/runsegmentation`** | Find segments using factor analysis + k-means |
| **`/competitiveanalysis`** | Compare against named competitors per outcome |
| **`/choosestrategy`** (or `/growthmatrix`) | Place yourself on the 5-cell Growth Strategy Matrix |
| **`/generatevalueprop`** | Write the 4-part value proposition |
| **`/buildroadmap`** | Pair each outcome with one of the 7 product moves |
| **`/outcometospec`** | Translate one outcome into an engineering spec sheet |
| **`/createodicanvas`** (or `/canvas`) | Render the one-page summary |
| **`/exportdeliverables`** (or `/ship`, `/packageproject`) | Bundle the six artifacts |
| **`/runfullodi`** (or `/fullodi`, `/start`) | End-to-end master orchestrator (real or rehearsal mode) |
| **`/runliteodi`** (or `/lite`) | Qualitative-only ODI (no survey) |
| **`/mineoutcomes`** | Mine public posts for candidate outcomes (SYNTHETIC) |
| **`/sentimentlandscape`** | Pre-survey hypothesis landscape from public data (SYNTHETIC) |
| **`/run-synthetic-survey`** (or `/synthsurvey`) | Full synthetic pipeline (SYNTHETIC) |

---

## What you need before each step

Most commands need outputs from prior commands. Here's the dependency tree in one place:

```
/preflight                    needs: a paragraph describing your situation
/odihelp                      needs: nothing
/definejob                    needs: a draft job, product description, or just a problem
/identifycustomers            needs: locked job statement from /definejob
/buildjobmap                  needs: locked job statement
/generatescreener             needs: job + (optional) competitor names
/extractoutcomes              needs: job + job map + interview transcript
/netoutcomes                  needs: ≥1 raw outcomes CSV from /extractoutcomes
/validateoutcomes             needs: netted outcomes CSV
/hypothesizecomplexity        needs: job + job map (+ optional mined data)
/generatesurvey               needs: netted outcomes CSV + complexity factors JSON
/computescores                needs: cleaned survey CSV (real or synthetic) + netted outcomes CSV
/runsegmentation              needs: cleaned survey CSV + netted outcomes CSV
/competitiveanalysis          needs: survey CSV with sat_<competitor>_<id> columns
/choosestrategy               needs: opportunity scores + segments (+ optional competitive + WTP)
/generatevalueprop            needs: chosen segment + segment's top outcomes + competitor + reason-to-believe
/buildroadmap                 needs: opportunity scores + chosen segment
/outcometospec                needs: outcome statement + opp score + competitor satisfaction
/createodicanvas              needs: any subset of the engagement outputs
/exportdeliverables           needs: all six Table 30.1 artifacts (will tell you which are missing)
/runfullodi                   needs: just an initial problem description
/runliteodi                   needs: 8–15 interview transcripts
/mineoutcomes                 needs: job statement
/sentimentlandscape           needs: mined-outcomes.csv
/run-synthetic-survey         needs: just a job statement
```

If you skip a prerequisite, the command will prompt you for the missing input. Nothing fails silently.

---

## Two final warnings

1. **Synthetic data is a hypothesis generator, not a substitute for the real survey.** Every output from the synthetic pipeline is stamped accordingly. The plugin refuses to chain `/generatevalueprop`, `/buildroadmap`, `/choosestrategy`, or `/outcometospec` off synthetic data.

2. **Leadership commitment is the silent killer of ODI projects.** Before you spend $40k on panel fees, get written commitment from the decision-maker that the data will be respected when it conflicts with their gut. `/preflight` flags this explicitly. If you can't get the commitment, run `/runliteodi` first as a pilot to demonstrate the method's value.

---

Now go run `/odihelp` (or just `/start`). It'll figure out where you actually want to land.
