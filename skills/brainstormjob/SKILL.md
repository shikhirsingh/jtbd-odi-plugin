---
name: brainstormjob
description: Use when the user doesn't have a clear functional job yet — they have a business idea, a competitor URL, a market category, or are staring at a complex product they don't understand (e.g., a niche B2B SaaS, a hardware tool, an obscure platform) and need help figuring out what the underlying customer job actually IS. The skill does web research, proposes 3–5 candidate jobs at different abstraction levels, walks the user through picking one, and hands off to /definejob to lock it.
when_to_use: User typed /brainstormjob, OR said things like "I have an idea but I don't know the job", "what job does ProductX solve", "I'm looking at this market but I don't understand it", "help me figure out what customers are trying to do here". Always called BEFORE /definejob when the user isn't ready to draft a sentence yet.
trigger_phrases:
  - /brainstormjob
  - /exploretarget
  - /discoverjob
  - /whatjob
  - "I don't know what the job is"
  - "I have an idea but"
  - "help me figure out the job"
  - "what job does"
  - "I see this product but I don't understand"
  - "I'm exploring this market"
  - "what's the underlying job for"
  - "reverse engineer this product"
  - "what are customers trying to do with"
inputs:
  - free-form description of the idea, market, product name, competitor URL, or pasted product page
  - (optional) target customer description if known
  - (optional) the user's own product idea (so the proposals are framed around what they could build)
outputs:
  - 3–5 candidate job statements at different abstraction levels (too narrow / sweet spot / too broad)
  - a "category landscape" — competitors, workarounds, and how each frames the job
  - an interactive pick that hands off to /definejob with the chosen draft pre-loaded
chains_to:
  - /definejob (with the chosen candidate as the draft input)
  - /preflight (if the user wants to sanity-check first)
delegates_to:
  - WebSearch / WebFetch tools (for market research)
---

# /brainstormjob — "I see this market/product, what's the job?"

## Plain-English preamble

> Sometimes you don't have a draft job statement ready. You have a half-formed idea, a competitor URL, or you're staring at a complex product like a B2B SaaS tool and you don't really know what *underlying job* its users are getting done.
>
> `/definejob` assumes you can write a candidate sentence. This skill is what comes before that — it does light web research, proposes candidate jobs at different altitudes (narrow / sweet spot / broad), and lets you pick one. Then it hands off to `/definejob` to lock it through the formal validation.

## When to use this vs. /definejob

| Situation | Use |
|---|---|
| You can already write a draft like "Listen to music while on the go" | `/definejob` |
| You're staring at a competitor's website and don't know what job their users hire it for | **`/brainstormjob`** |
| You have a vague idea ("something for remote workers to feel less isolated") | **`/brainstormjob`** |
| You see a complex B2B product (Snowflake, Datadog, niche vertical tool) and don't know who hires it for what | **`/brainstormjob`** |
| You're entering a new market and don't know which "job" frame to attack from | **`/brainstormjob`** |

## How the skill works

### Step 1 — Gather context

Ask the user a few questions if they didn't already say:

```
Quick questions before I research:
  1. What are you looking at? (product URL, market category, your own idea, or a competitor name)
  2. Who do you think the user might be? (any guess is fine — "developers", "operations teams", "parents of toddlers")
  3. Why are you exploring this — entering the market, building against it, or just curious?
```

### Step 2 — Light web research

Use `WebSearch` and `WebFetch` to gather:

- **What the product/market actually does** — read the product's own page, the category Wikipedia entry, top "what is X" articles
- **What users say they use it for** — search Reddit / forums / G2 / Trustpilot for "how I use ProductX"
- **What workarounds existed before this product** — what people did to get the job done in a previous era
- **What adjacent products solve similar jobs** — to triangulate the right altitude

You're not doing a deep mine here (that's `/mineoutcomes`). Just enough to propose smart candidate jobs.

### Step 3 — Propose 3–5 candidates at different altitudes

For each candidate, present:

| Candidate | Altitude | What this would mean |
|---|---|---|
| Too narrow | "Boil water" | Your current product's literal job. Caps your ceiling. |
| Slightly narrow | "Make a cup of coffee" | The workflow your category typically frames |
| **Sweet spot** | **"Prepare a hot beverage for consumption"** | The job that includes the workflow + adjacent opportunities |
| Slightly broad | "Energize myself in the morning" | Crosses into other categories (energy drinks, supplements) |
| Too broad | "Maintain mental alertness throughout the day" | Not actionable — too many adjacent jobs |

Show the user where each landing affects their roadmap ceiling:

> "If you pick 'make a cup of coffee,' you're competing with drip coffee makers. If you pick 'prepare a hot beverage,' you're competing with — and could become — Keurig."

### Step 4 — Walk the user through picking

Don't auto-pick. Ask:

```
Three considerations:
  • Where would your company's products actually live? (If you can't address the broader job
    end-to-end, even via partnerships, that's too broad.)
  • Where does competitive disruption come FROM? (Pick wide enough to see the threat.)
  • Where does the customer actually frame their goal? (Ask 2-3 of them if you can.)

Which candidate fits your company's reality?
```

### Step 5 — Hand off to /definejob

Once they pick:

```
Locked candidate: <picked sentence>

Now run /definejob "<picked sentence>" and we'll score it formally
against the 5 rules + 3 stability checks. It'll iterate until clean.
```

## Output format

```json
{
  "skill": "brainstormjob",
  "user_input": "I'm trying to understand what job Notion solves",
  "web_research_summary": {
    "category": "all-in-one workspace / docs+database+wiki",
    "competitors_examined": ["Notion", "Coda", "Confluence", "Airtable", "Roam"],
    "what_users_say": "Mostly: 'I use it to keep my team's institutional knowledge in one place' and 'I use it to plan my life'",
    "workarounds_before": "Google Docs + spreadsheets + a wiki + a project tool; lots of context-switching",
    "adjacent_jobs_solved": ["Document & share knowledge", "Track tasks & projects", "Build a personal database"]
  },
  "candidate_jobs": [
    {"label": "Too narrow", "statement": "Take notes during a meeting",
     "why_too_narrow": "Notion does this, but it's only 5% of why people use it. Caps you."},
    {"label": "Slightly narrow", "statement": "Document a team's internal processes",
     "tradeoffs": "Lives in confluence-like territory; clear category but limited TAM."},
    {"label": "Sweet spot", "statement": "Capture and organize a team's collective knowledge for ongoing reference",
     "why_sweet_spot": "Includes notes, docs, wikis, databases, and project tracking — the full workflow Notion users actually do."},
    {"label": "Slightly broad", "statement": "Coordinate a team's work and shared context",
     "tradeoffs": "Crosses into Slack/Linear territory; bigger TAM but harder positioning."},
    {"label": "Too broad", "statement": "Make a team more productive",
     "why_too_broad": "Every B2B SaaS could claim this. Not actionable."}
  ],
  "recommendation": {
    "candidate_id": "sweet_spot",
    "reason": "Sweet spot framing matches the actual cross-functional workflow Notion users describe in public threads. Narrower framings cap the ceiling; broader framings collide with too many adjacent categories."
  },
  "next_step": "Run /definejob \"Capture and organize a team's collective knowledge for ongoing reference\" — the chosen candidate goes through formal scoring."
}
```

## Worked example — exploring an unfamiliar product (Snowflake)

User input: *"I keep hearing about Snowflake but I don't really understand what it's for. What's the job?"*

You research and propose:

| Altitude | Candidate | Note |
|---|---|---|
| Too narrow | "Store query-able data in the cloud" | Cloud DB territory. Cap your ceiling. |
| Slightly narrow | "Run analytical queries on company data at scale" | Data warehouse category. Solid but limited. |
| **Sweet spot** | **"Make a company's data available for analysis across teams without engineering bottlenecks"** | Names what users actually buy Snowflake for — escaping the ETL/data-engineer queue. |
| Slightly broad | "Make a company data-driven" | True but too vague to act on. |
| Too broad | "Improve business decision-making" | Not actionable. |

User picks the sweet spot → you hand off to `/definejob`.

## Hard rules

- ALWAYS do at least light web research before proposing candidates. Don't make up market intel.
- ALWAYS propose 3–5 candidates at different altitudes — not just one.
- NEVER let the user pick a too-narrow framing without surfacing the disruption risk.
- ALWAYS hand off to `/definejob` after the user picks — never declare the job "locked" yourself.
- If the user is exploring a market they want to ENTER (vs. just understanding), recommend `/preflight` after `/definejob` to sanity-check ODI fits the situation.
