# JTBD ODI — The Outcome-Driven Innovation Plugin for Claude Code

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   👋  Welcome. You just installed the plugin.                        ║
║                                                                      ║
║   Type ONE of these — they're all safe first moves:                  ║
║                                                                      ║
║      /odihelp        ← I don't know what to do                       ║
║      /demo           ← Show me what this produces (no commitment)    ║
║      /whatdoido      ← I have a file/data, what do I run on it?     ║
║      /preflight      ← Is ODI even the right tool for me?            ║
║      /brainstormjob  ← I'm staring at a market/product and don't    ║
║                       even know what "the job" is yet                ║
║                                                                      ║
║   👉 If you only read one file, read QUICKSTART.md (2 min).          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

A toolkit for running an Outcome-Driven Innovation–style engagement inside Claude Code — from a one-sentence job statement all the way to a ranked opportunity landscape, segmented value proposition, and engineering specs.

It's built against my own practitioner guide, **[*JTBD: A Practical Guide*](https://shikhir.com/blog/jtbd-guide.html)** — a working write-up of how I execute the Ulwick / Strategyn Outcome-Driven Innovation method, with the consulting fluff stripped out. The plugin is one possible execution of that guide.

> ⚠️ **Not endorsed by Strategyn or Tony Ulwick** — independent, unaffiliated, inspired by their published work.

> **This plugin implements the Ulwick school of JTBD, not Christensen's narrative school.** Outputs are strict outcome statements, top-2-box scoring, and the opportunity algorithm `Imp + max(Imp - Sat, 0)`. If you want "jobs as stories," use a different tool.

---

## 🚀 New to this plugin or to ODI?

**Read these three short files first** (12 minutes total) — they're written for newcomers:

| File | Why | Time |
|---|---|---|
| **[QUICKSTART.md](QUICKSTART.md)** | The 4 entry-point commands, side by side. The 2-minute version. | 2 min |
| **[GUIDE.md](GUIDE.md)** | The full journey explained in plain English. The 3 paths (Full / Lite / Rehearsal), every command, every dependency. | 10 min |
| **[GLOSSARY.md](GLOSSARY.md)** | Every Ulwick term — top-2-box, opportunity, complexity factor, netting, etc. — translated into plain language. | reference |

Or just type **`/odihelp`** (or **`/start`**) inside Claude Code. The skill asks 3 diagnostic questions and routes you to the right entry point.

---

## What you can do with it

Commands are listed in **the order a newcomer would actually run them**. If you're not sure where to start, just type `/odihelp` — it routes you.

### 🟢 Step 0 — Figure out where to start (no methodology knowledge needed)

| Command | What it actually does |
|---|---|
| **`/odihelp`** | Asks you 3 short diagnostic questions ("are you new?", "where are you in the process?", "what's your budget?") and tells you the exact next command to type. Run this if you don't know what you're doing. |
| **`/demo`** | Walks you through what a finished ODI engagement *looks like* — using Tony Ulwick's own Bosch CS20 case study. Shows every artifact (ranked outcomes, landscape, segments, value prop, roadmap, engineering specs). No work, no commitment. Try this if you want to see what you'd actually get out. |
| **`/whatdoido`** | Reverse lookup: you tell it what files you have (a CSV, a folder of transcripts, partial outputs), and it tells you which command to run on it. Use when you're stuck mid-engagement. |
| **`/preflight`** | Ulwick's checklist of "should you even do ODI?" Asks 6 questions about your problem and gives you an honest go/no-go. Saves teams from spending 8 weeks on the wrong method. |

### 🔵 Step 1 — Figure out what the customer is actually trying to do

| Command | What it actually does |
|---|---|
| **`/brainstormjob`** | You have an idea, a competitor URL, or you're staring at a complex product (Snowflake, Notion, some obscure B2B tool) and you don't even know what *job* its users hire it for. This skill does light web research, proposes 3–5 candidate jobs at different abstraction levels (too narrow / sweet spot / too broad), and hands off to `/definejob`. Use when you can't write a draft job sentence yet. |
| **`/definejob`** | You've got a draft sentence like "help people listen to music while on the go." This skill scores it against Ulwick's 5 rules (verb-first, no adjectives, no emotion, customer perspective, job-not-situation) and 3 stability checks (works in 20 years, across countries, regardless of solution). Iterates with you until the sentence is clean. Locked output becomes the anchor for every downstream step. |
| **`/identifycustomers`** | For B2B and complex B2C: identifies the THREE customer types — the executor (who actually does the job), the lifecycle support person (who installs/maintains/disposes), and the buyer (who signs the check). Each gets a separate screener and separate interviews. Skipping the buyer is how most B2B engagements ship products nobody pays for. |
| **`/buildjobmap`** | Breaks the locked job into the 8 universal steps (Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude). The map is what you'll hang outcomes on in the next phase. It's NOT a customer journey or a process map — those bake in today's solutions. The job map stays valid regardless of which product anyone uses. |

### 🟣 Step 2 — Discover what customers actually want (3 paths — pick one)

| Path | When to use it | Commands |
|---|---|---|
| **Real interviews** (the canonical way) | You can recruit 15–30 real customers and run 60-min interviews with each. Highest signal quality. | `/generatescreener` → recruit + interview → `/extractoutcomes <folder of transcripts>` → `/netoutcomes` → `/validateoutcomes` |
| **Online research** (skip interviews) | You can't recruit interviewees, but your category has an active online conversation (Reddit, app stores, forums). | `/mineoutcomes` → `/netoutcomes` → `/validateoutcomes` (or run `/researchpath` to orchestrate the whole thing) |
| **Pure rehearsal** (synthetic only) | Just want a hypothesis with zero budget. Output is NOT decision-grade. | `/run-synthetic-survey` does the full pipeline end-to-end |

| Command | What it actually does |
|---|---|
| **`/generatescreener`** | Builds the recruiting questionnaire your panel provider uses to filter for real job-executors. Includes incidence-rate estimate (so the provider can price), quota plan (so you get enough completes per likely segment), and an incentive recommendation ($5–500 depending on audience). For B2B, builds three separate screeners — one per customer type. |
| **`/extractoutcomes`** | Point it at ONE transcript file OR a WHOLE FOLDER of transcripts. The skill pulls 25–40 candidate outcome statements per transcript, in strict syntax (Minimize/Increase + metric + object + clarifier), groups them by job-map step, and surfaces a per-phase coverage histogram (so you can see which interviews under-covered which step). For 15 transcripts you'll get ~400 raw candidates. |
| **`/mineoutcomes`** | Autonomously mines Reddit, X/Twitter, Amazon reviews, app-store reviews, Quora, StackExchange, and forums for posts about your job. Converts customer language into outcome candidates with source URLs preserved. Output is hypothesis-only and capped at 60% of candidate pool when combined with real interview data. |
| **`/netoutcomes`** (alias `/refineoutcomes`) | Compresses 300–600 raw candidates into 50–150 clean, deduplicated, well-formed final outcomes. Runs embedding-based similarity clustering, splits compound statements, strips embedded product names, fixes non-canonical direction verbs. Logs every operation so the human reviewer can audit. |
| **`/validateoutcomes`** | The quality gate before the survey. Scores every netted outcome against Ulwick's 10 characteristics (Ch 11) — measurable, stable, solution-free, etc. Returns `pass / conditional / fail`. `/generatesurvey` refuses to run if verdict is `fail`. Better to catch a bad outcome here than in your $40k panel data. |
| **`/hypothesizecomplexity`** (alias `/complexityfactors`) | Proposes 8–15 "complexity factors" — the situational variables (commute length, finish-cut frequency, herd size, etc.) that will drive segmentation later. These are what go in your survey's profiling section. Demographics rarely segment ODI markets — complexity factors do. Ranked by expected segmentation power. |

### 🟠 Step 3 — Measure how customers actually rate everything (the survey)

| Command | What it actually does |
|---|---|
| **`/generatesurvey`** | Builds the full ODI survey instrument from your validated outcomes. Includes screener, profiling (complexity factors + demographics), importance ratings, satisfaction ratings, optional per-competitor satisfaction, optional willingness-to-pay block. Exports to Qualtrics .qsf, Typeform JSON, Markdown for review, and a field-map CSV. Refuses to run if `/validateoutcomes` hasn't passed. |
| *(human step)* | **Field the survey to 300–600 real respondents.** No way to skip this and keep decision-grade output. Typical cost $5k–25k, timeline 2–3 weeks. The panel provider (Prolific, Cint, Dynata for B2C; ResearchNow, Schlesinger for B2B) sends you a CSV when done. |
| **`/run-synthetic-survey`** (alias `/synthsurvey`) | Alternative to the human step: mines public data, synthesizes 10 grounded personas (each anchored in ≥3 verbatim mined quotes), and simulates an ODI survey. **Output is HYPOTHESIS-ONLY** — statistical validity is bounded by persona count, not row count. Long-tail outcomes are systematically under-counted. Cannot drive roadmap or pricing decisions; downstream skills will refuse. |

### 🔴 Step 4 — Crunch the numbers (this is where ODI is famous)

| Command | What it actually does |
|---|---|
| **`/computescores`** (alias `/opportunitylandscape`) | The opportunity formula in action: `Opp = Importance + max(Importance − Satisfaction, 0)`, using top-2-box scoring (% rating 4 or 5). Every outcome ranked 0–20 and classified (extreme / low-hanging-fruit / worth-considering / appropriately-served / overserved). Produces the famous Opportunity Landscape scatter chart. If your survey had a WTP block, also computes the pricing band by segment. |
| **`/runsegmentation`** | Finds customer segments by **clustering on unmet outcomes**, not on demographics. Runs factor analysis on the differentiating outcomes, then k-means on the factor scores. Each segment gets its own opportunity landscape and is profiled by the complexity factors that explain it ("Finish-cut tradesmen", not "Men 30-55"). Typically surfaces 2–5 segments. |
| **`/competitiveanalysis`** | For every outcome, shows top-2-box satisfaction for each named competitor. Surfaces (a) where each competitor wins, (b) where the whole market collectively fails, (c) where you should attack (high importance, no competitor close to the ceiling), and (d) where to strip cost (over-served outcomes). Computes the 20%-better target you'd need to hit to win share on each underserved outcome. |

### ⭐ Step 5 — Decide what to do (strategy + positioning)

| Command | What it actually does |
|---|---|
| **`/choosestrategy`** (alias `/growthmatrix`) | Places your data on Ulwick's 5-cell Growth Strategy Matrix. Recommends one of Differentiated / Dominant / Disruptive / Discrete / Sustaining per target segment, with data justification per cell. Refuses to recommend Dominant unless you confirm a real cost breakthrough. Flags Discrete as a TRAP, not a celebration. If your survey had WTP, also outputs the pricing band. |
| **`/generatevalueprop`** | Writes the four-part outcome-based value proposition for your chosen segment: "For \[segment], who are trying to \[job], our \[product] helps them \[address these underserved outcomes], unlike \[next-best alternative], because of \[the specific tech/design reason it works]." Plus 3 marketing variants (long-form, one-liner, sales talk track). Every clause is traceable to data. Refuses on synthetic data. |
| **`/buildroadmap`** | Pairs every underserved outcome (opp ≥ 10) with one of Ulwick's 7 product moves: Borrow / Accelerate pipeline / Partner / Acquire / New feature set / New subsystem / Ultimate solution. Slots each into v1.0, v1.x, v2.0, or Northstar. Coverage check: flags if you're over-using "new feature set" — usually means you're missing faster paths (borrow, partner). |

### 🏗️ Step 6 — Hand off to engineering

| Command | What it actually does |
|---|---|
| **`/outcometospec`** | For ONE outcome, produces SEVEN ship-ready artifacts in `spec-out/<outcome_id>/`: the 5-field engineering spec sheet (Ch 28), an Agile user story with INVEST acceptance criteria, a full PRD doc (Notion-ready), Linear-importable JSON, Jira REST API-compatible JSON, an ADR if there's a real tech choice, and a post-launch SQL telemetry query. All artifacts share the same outcome_id so PRs, tickets, and docs cross-link. Acceptance criteria use the 20%-better number from `/competitiveanalysis`. Run once per outcome shipping in v1.0 (typically 5–12 outcomes). |

### 📦 Step 7 — Ship the engagement

| Command | What it actually does |
|---|---|
| **`/createodicanvas`** (alias `/canvas`) | Renders the one-page ODI Canvas — a 9-cell board-ready summary showing the job, segment, job map, top outcomes, posture, value prop, roadmap, pricing band, and engineering acceptance criteria. Every cell footnoted to its source file. Exported as Markdown, HTML (printable), PNG, and JSON. This is what executives actually read. |
| **`/exportdeliverables`** (aliases `/packageproject`, `/ship`) | Bundles the engagement into a `deliverables/` folder containing EXACTLY the six Table 30.1 artifacts + Canvas + exec summary + coverage report. **Refuses to ship if any artifact is missing** — tells you which command to run to fill the gap. Coverage report proves all seven front-matter capabilities (know-what-to-build, identify-beachhead, WTP-pricing, engineering-measurable, marketing-lands, posture-with-evidence, repeatable) are enabled. |

### 🎯 Master orchestrators — pick one if you want it all coordinated

| Command | What it actually does | Wall-clock |
|---|---|---|
| **`/runfullodi`** (alias `/fullodi`, `/start`) | Walks every phase (Ch 29) from job definition through engineering spec, pausing at human checkpoints (recruiting, fielding, segment selection). Two modes: `real` (decision-grade, 4–8 weeks) and `rehearsal` (synthetic, 30–60 min). Guarantees all six Table 30.1 artifacts. | 4–8 weeks or 30–60 min |
| **`/researchpath`** (aliases `/onlinepath`, `/skipinterviews`) | Replaces interviews with thorough online research (5x heavier `/mineoutcomes` quotas), then fields a REAL n=300-600 survey on the mined outcomes. **Decision-grade** (because the survey is real). Shaves 2–3 weeks off vs. full path. Best for B2C / prosumer / developer-tool categories with active online communities. | 3–5 weeks |
| **`/runliteodi`** (alias `/lite`) | Qualitative-only path. Uses only interviews (no survey). Produces directional opportunity hypothesis + qualitative archetypes. NOT decision-grade. Use when budget < $10k or timeline < 3 weeks. | 2–3 weeks |
| **`/run-synthetic-survey`** (alias `/synthsurvey`) | Full synthetic pipeline. Mines public data, synthesizes 10 personas, simulates a survey. Hypothesis-only. Cannot chain to value-prop, roadmap, or engineering specs. | 30–60 min |
| **`/sentimentlandscape`** | Lighter than `/run-synthetic-survey` — produces only a pre-survey "hypothesis landscape" from public sentiment. Used to decide which outcomes to definitely include in the real survey. | 10–20 min |

---

## Installation

This repo ships as a Claude Code plugin (`.claude-plugin/marketplace.json` + `plugin.json`) and works in Cowork. Pick the install path that matches your setup — both end up with skills under `~/.claude/skills/`, which is what Claude Code and Cowork scan.

### Recommended — Claude Code marketplace

From inside Claude Code:

```
/plugin marketplace add shikhirsingh/jtbd-odi-plugin
/plugin install jtbd-odi@jtbd-odi
```

Commands are namespaced as `/jtbd-odi:odihelp`, etc. Update with `/plugin marketplace update jtbd-odi`. Then install the Python deps:

```bash
pip install -r ~/.claude/plugins/cache/jtbd-odi/jtbd-odi/*/scripts/requirements.txt
```

### Alternative — clone + run `fix-skills.sh`

```bash
git clone https://github.com/shikhirsingh/jtbd-odi-plugin.git
cd jtbd-odi-plugin
./fix-skills.sh
pip install -r scripts/requirements.txt
```

`fix-skills.sh` symlinks every skill, command, and agent into both `~/.claude/` (where Claude Code and Cowork look) and `~/.agents/` (where `npx skills add` writes), so the plugin is visible to all three. It's idempotent — re-run after `git pull` to pick up updates. If you previously ran `npx skills add shikhirsingh/jtbd-odi-plugin -a claude-code` and the skills didn't show up, run this script from the cloned repo to fix it.

### Verify

Restart Claude Code (or `:rebuild`), then:

```
/help
```

You should see `/odihelp`, `/demo`, `/runfullodi`, etc. Try `/odihelp` to confirm.

### Python dependencies

The analysis skills (`/computescores`, `/runsegmentation`, synthetic survey orchestrator) call scripts in `scripts/`:

```
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
matplotlib>=3.7
factor-analyzer>=0.4
```

A `requirements.txt` is included.

---

## A complete worked example — from blank slate to roadmap

```text
# 1. Define the job
/definejob "I want to help people listen to music while on the go"

# 2. Build the universal job map
/buildjobmap "Listen to music while on the go"

# 3. Run 10–20 real interviews, paste a transcript:
/extractoutcomes path/to/interview-01.txt

# 4. Net the raw outcomes into a clean list
/netoutcomes path/to/raw-outcomes.csv

# 5. Generate the survey ready for Qualtrics
/generatesurvey path/to/netted-outcomes.csv

# --- field the survey to 300-600 real humans, then: ---

# 6. Compute opportunity scores
/computescores path/to/survey-data.csv

# 7. Run outcome-based segmentation
/runsegmentation path/to/survey-data.csv

# 8. Write the value proposition for the chosen segment
/generatevalueprop --segment "Commuters with long routes"

# 9. Build the outcome-attack roadmap
/buildroadmap

# 10. Convert the top outcomes into engineering specs
/outcometospec "Minimize the time it takes to get the songs in the desired order for listening"
```

### Or, if you want a hypothesis BEFORE you commission interviews:

```text
/run-synthetic-survey "listen to music while on the go"
```

This single command:

1. Mines Reddit (r/headphones, r/audiophile, r/spotify, …), X/Twitter posts, Amazon-headphones reviews, app-store reviews, and forums for the job.
2. Synthesizes 5–8 grounded personas with complexity-factor profiles.
3. Has each persona "take" a synthetic ODI survey (importance + satisfaction 1–5).
4. Writes `synthetic_survey.csv` in the exact schema `/computescores` and `/runsegmentation` expect.
5. Stamps every output with a **SYNTHETIC — DO NOT SHIP** banner and an instruction to validate against n≥300 real respondents before any go/no-go decision.

---

## How the pieces talk to each other

```
                 ┌──────────────┐
                 │  /definejob  │
                 └──────┬───────┘
                        ▼
                 ┌──────────────┐
                 │ /buildjobmap │
                 └──────┬───────┘
        ┌───────────────┴────────────────┐
        ▼                                ▼
┌──────────────────┐         ┌────────────────────┐
│ /extractoutcomes │         │   /mineoutcomes    │  ← agent: data-miner
└──────┬───────────┘         └──────────┬─────────┘
       └──────────┬──────────────────────┘
                  ▼
           ┌──────────────┐
           │ /netoutcomes │  ← agent: outcome-formatter
           └──────┬───────┘
                  ▼
           ┌──────────────────┐
           │ /generatesurvey  │
           └──────┬───────────┘
        ┌─────────┴──────────────────────┐
        ▼                                ▼
[ field to real humans ]      ┌─────────────────────────┐
        │                     │  /run-synthetic-survey  │
        │                     │  ↳ data-miner           │
        │                     │  ↳ persona-synthesizer  │
        │                     │  ↳ virtual-respondent ×N│
        ▼                     └────────────┬────────────┘
        └────────────────┬─────────────────┘
                         ▼
              ┌─────────────────────┐
              │   /computescores    │
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │  /runsegmentation   │
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │ /generatevalueprop  │
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │   /buildroadmap     │
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │   /outcometospec    │  (one per shipping outcome)
              └─────────────────────┘
```

---

## The critical guardrail

The plugin includes an autonomous "virtual respondent" layer. **It is a hypothesis generator, not a substitute for the survey.**

> Direct quote from the guide (Part IV, *What AI does NOT replace*):
> *"Do not use an LLM to simulate survey respondents. Synthetic survey data looks plausible and is dangerous: it tells you what the LLM thinks a customer would say, not what real customers actually rate. The opportunity scores from synthetic data will reflect training-data biases, not market reality."*

Every synthetic deliverable produced by this plugin is stamped:

```
================================================================
⚠️  SYNTHETIC DATA — DIRECTIONAL ONLY — DO NOT SHIP
This output was generated by LLM-simulated respondents grounded
in public online data. It is intended ONLY for hypothesis
generation, survey-question stress-testing, and prioritizing
which real-human interviews to commission first.

Before any roadmap, pricing, or value-prop decision, validate
against n ≥ 300 real respondents per ODI v2.4.2, Chapter 16.
================================================================
```

If you remove the banner, you are deliberately misusing the tool.

---

## Project structure

```
jtbd-odi-plugin/
├── .claude-plugin/
│   ├── marketplace.json     ← one-plugin marketplace catalog
│   ├── plugin.json          ← plugin manifest (method config + guardrails)
│   └── instructions.md      ← plugin-wide behavioral defaults
├── fix-skills.sh            ← post-clone installer (symlinks into ~/.claude/ and ~/.agents/)
├── README.md
├── commands/                ← thin slash-command entry points
│   ├── definejob.md
│   ├── buildjobmap.md
│   ├── …
│   └── run-synthetic-survey.md
├── skills/                  ← the actual prompts + JSON schemas
│   ├── definejob/SKILL.md
│   ├── buildjobmap/SKILL.md
│   ├── extractoutcomes/SKILL.md
│   ├── netoutcomes/SKILL.md
│   ├── generatesurvey/SKILL.md
│   ├── computescores/SKILL.md
│   ├── runsegmentation/SKILL.md
│   ├── generatevalueprop/SKILL.md
│   ├── buildroadmap/SKILL.md
│   ├── outcometospec/SKILL.md
│   ├── mineoutcomes/SKILL.md
│   ├── hypothesizecomplexity/SKILL.md
│   ├── sentimentlandscape/SKILL.md
│   └── run-synthetic-survey/SKILL.md
├── agents/                  ← subagents the skills delegate to
│   ├── data-miner.md
│   ├── persona-synthesizer.md
│   ├── virtual-respondent.md
│   └── outcome-formatter.md
├── scripts/                 ← Python helpers
│   ├── requirements.txt
│   ├── opportunity_scorer.py        (Ch 19 / Appendix B + WTP analysis)
│   ├── segmentation_engine.py       (Ch 21 / Appendix C)
│   ├── survey_generator.py
│   ├── synthetic_survey_generator.py
│   ├── netting_helper.py            (compound + direction-verb detection)
│   ├── mine_sources.py
│   ├── outcome_validator.py         (Ch 11 ten-characteristics gate)
│   ├── canvas_generator.py          (the one-page ODI Canvas)
│   └── deliverables_exporter.py     (the six Table 30.1 artifacts bundle)
└── examples/
    ├── bosch-cs20-walkthrough.md
    └── listen-to-music-synthetic.md
```

## The six Table 30.1 artifacts (always produced by `/exportdeliverables`)

1. **Ranked opportunity list** — `/computescores`
2. **Outcome-based segments** — `/runsegmentation`
3. **Strategic posture** — `/choosestrategy`
4. **Outcome-based value proposition** — `/generatevalueprop`
5. **Outcome-attack roadmap** — `/buildroadmap`
6. **Engineering specs** — `/outcometospec ×N` (each spec produces 7 ship-ready artifacts: 5-field sheet + user story + PRD + Linear JSON + Jira JSON + ADR + dashboard SQL)

`/exportdeliverables` refuses to ship if any are missing.

## Three valid data-provenance paths

The plugin enforces honesty about where your data came from:

| Path | Discovery | Quantify | Output stamp | Decision-grade? |
|---|---|---|---|---|
| `/runfullodi --mode real` | Real interviews (15–25) | Real survey (n=300–600) | `interviews_plus_survey` | ✅ Yes |
| `/researchpath` | Online research (heavy mining, 500+ posts) | Real survey (n=300–600) | `mixed_research_real_survey` | ✅ Yes |
| `/runliteodi` | Real interviews (8–15) | None | `qualitative_only_lite` | 🟡 Directional only |
| `/run-synthetic-survey` | Online mining | Synthetic personas (10 archetypes) | `synthetic` | ❌ Hypothesis only |

The decision-grade outputs (`/generatevalueprop`, `/buildroadmap`, `/choosestrategy`, `/outcometospec`) refuse to chain off `synthetic` or `qualitative_only_lite` provenance — they require real survey data.

---

## Versioning and provenance

- **Relationship to Strategyn / Tony Ulwick:** independent, unaffiliated, not endorsed. The plugin is inspired by Ulwick's published ODI work; it is not a Strategyn product and has not been reviewed by them. See the [practitioner guide](https://shikhir.com/blog/jtbd-guide.html) for the author's interpretation of the method.
- Method version: ODI v2.4.2 (May 2026) — refers to the author's own [practitioner guide](https://shikhir.com/blog/jtbd-guide.html), not a Strategyn release
- Plugin version: **1.4.2** — adds explicit "not endorsed by Strategyn / Ulwick" disclaimer and links the practitioner guide at shikhir.com/blog/jtbd-guide.html
- Plugin version: 1.4.1 — adopts the modern `.claude-plugin/` layout (marketplace.json + plugin.json), adds `fix-skills.sh` to reconcile `~/.claude/skills/` and `~/.agents/skills/` for `npx skills add` users, slimmed-down install section
- Plugin version: 1.4.0 — adds /brainstormjob (discover unclear job from an idea/competitor URL), /researchpath (online research → REAL survey workflow), /extractoutcomes now accepts a folder of transcripts, /outcometospec now produces 7 ship-ready artifacts (user story + PRD + Linear/Jira JSON + ADR + dashboard SQL), /run-synthetic-survey defaults to 10 personas with explicit sample-size honesty, README rewritten in newcomer-first order
- Plugin version: 1.3.0 — added /whatdoido (reverse lookup), /demo (worked-example tour), QUICKSTART.md, plugin-wide instructions, expanded natural-language triggers
- Plugin version: 1.2.0 — added /odihelp, /preflight, /identifycustomers, 7 plain-English aliases, GUIDE.md, GLOSSARY.md
- Plugin version: 1.1.0 — added /validateoutcomes, /generatescreener, /competitiveanalysis, /choosestrategy, /createodicanvas, /exportdeliverables, /runliteodi, /runfullodi + outcome_validator.py, canvas_generator.py, deliverables_exporter.py
- Method lineage: Tony Ulwick / Strategyn (original ODI framework — see strategyn.com)
- Practitioner handbook author: Shikhir Singh (independent interpretation — [shikhir.com/blog/jtbd-guide.html](https://shikhir.com/blog/jtbd-guide.html))
- This plugin author: Shikhir Singh (independent, unaffiliated with Strategyn)

Every output the plugin produces is stamped with the method version it was generated against so downstream artifacts remain traceable.

## License

MIT — see [LICENSE](LICENSE).

---

Thanks to Tony Ulwick for making the world a better place by helping smart people not waste time building products nobody wants.
