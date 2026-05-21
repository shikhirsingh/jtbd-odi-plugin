---
name: generatesurvey
description: Build the full ODI survey instrument from a netted outcomes list — screener, profiling/complexity-factor questions, importance block, satisfaction block, optional WTP — ready to paste into Qualtrics, Typeform, SurveyMonkey, or a JSON survey schema. Implements Chapters 15, 16, 17, 18 + Template 4.
when_to_use: User has a netted outcomes CSV and says "/generatesurvey", "build the survey", "make the questionnaire", or arrives here from /netoutcomes.
trigger_phrases:
  - /generatesurvey
  - "build the survey"
  - "make the ODI survey"
  - "questionnaire"
inputs:
  - the netted outcomes CSV (from /netoutcomes)
  - the locked job statement
  - 8–15 candidate complexity factors (from /hypothesizecomplexity, or solicit interactively)
  - 2–4 named competitors (optional — for competitive satisfaction)
  - whether to include WTP (boolean)
outputs:
  - one full survey draft as Markdown (human-readable)
  - one machine-readable JSON survey schema
  - one Qualtrics-importable TXT (Advanced Format)
  - one Typeform-importable JSON
  - field-mapping documentation that ties every survey item back to the source outcome ID
chains_to:
  - "[field to 300–600 real humans via Qualtrics/Typeform/Prolific/Cint]"
  - /computescores (after fielding and cleaning the data)
helpers:
  - scripts/survey_generator.py (does the heavy lifting of writing Qualtrics .qsf-ish text)
---

# /generatesurvey — Build the ODI Survey Instrument

## Plain-English preamble (for newcomers)

> This is the most important deliverable of the project. The survey design determines whether your opportunity scores are real or noise.
>
> **What it produces:** a survey with 4–6 sections — screener, profiling (complexity factors), importance ratings, satisfaction ratings, optional competitive satisfaction, optional WTP — exported in Markdown, JSON, Qualtrics, and Typeform formats. Length budget: 25–40 min for 75–100 outcomes.
>
> **Why all the rules** (1 outcome per question; same scale throughout; importance first then satisfaction; matrix max 12 rows; group by job step; WTP at the very end)? Each one removes a known source of noise. Skip them and your data is unusable.
>
> **Hard gate:** this skill refuses to run until `/validateoutcomes` reports verdict ≠ `fail`. Bad outcomes can't be fixed downstream with statistics.

---

This is the most important deliverable of the entire project. **Its design determines whether your opportunity scores are real or noise.** (Chapter 15 opening.)

## The 4 (or 6) sections of the core survey (Chapter 15)

| # | Section | Notes |
|---|---|---|
| 1 | **Screener** | Filter out respondents who don't execute the job — frequency, role, use of a real solution. Disqualify in <90 seconds. |
| 2 | **Profiling** | ≤15 questions. Mostly **complexity factors**, not demographics. Behavioral & situational, not preference-based. |
| 3 | **Importance ratings** | Every outcome, rated 1–5. Grouped by job-map step. Asked first. |
| 4 | **Satisfaction ratings** | Same outcomes, same order, 1–5. Asked second (separately from importance to reduce anchoring). |
| 5 | **Competitive satisfaction** (optional) | Per-competitor. **Each respondent rates satisfaction against only the ONE product they currently use most** (Strategyn rule, Chapter 15). Don't ask everyone to rate every competitor — survey gets too long. |
| 6 | **Willingness-to-pay** (optional) | At the end only. Never before the I/S blocks. |

## Hard rules (Chapter 15 & 18)

1. **Same scale, same direction, throughout.** 5 = "extremely important"; 5 = "completely satisfied." Don't flip mid-survey "to test attention."
2. **Group outcomes by job step** in the I and S blocks. Don't shuffle the master order.
3. **Ask all importance ratings first, then all satisfaction ratings** with the same outcomes in the same order. No interleaving.
4. **One outcome per question.** No compound rows.
5. **Wrap each outcome in a context-setting prefix:**
   - Importance: *"When [job], how important is it to you that you can [outcome]?"*
   - Satisfaction: *"How satisfied are you with the [product/category] you currently use to [outcome]?"*
6. **Matrix questions: 8–12 rows max.** Break long blocks into multiple matrices, grouped by job step.
7. **Show a visible progress bar.** Reduces dropoff 10–20%.
8. **Attention check** every ~20 minutes of survey ("To confirm you're reading carefully, please select '4'").
9. **Mobile-test.** 40–60% of consumer respondents complete on phones.

## Sample plan (Chapter 16)

Default recommendation language: **target n = 300–600** (sweet spot). Note in the survey delivery doc:

| n | What you can do | What you can't |
|---|---|---|
| 180 | Overall opportunity scores | Reliably segment into 3+ groups |
| 400 | Scores + 2–3 segments at n≈120 each | Reliable WTP at segment level |
| 600–1000 | 3–5 segments + competitive on 3+ competitors | — |
| 1500–3000 | Multi-country / multi-vertical | — |

## Length budget (Chapter 15 & 18)

- 100 outcomes × 2 (importance + satisfaction) ≈ 25–40 minutes
- Cap at ~150 outcomes. Above that, rotate subsets (each respondent sees 80% randomized) and increase n accordingly.

## Incentives (Chapter 18, Table 18.2)

| Audience | Suggested |
|---|---|
| Consumer (general) | $5–25 |
| Professional B2B | $25–100 |
| Specialists (clinicians, executives) | $100–500 |

## Profiling that actually drives segmentation (Chapter 17)

Profiling questions are how you'll later *explain why* segments differ. The signal is in **complexity factors** — situational variables that make the job harder for some executors than others — **not** in demographics.

Examples of complexity factors:

| Job | Complexity factors |
|---|---|
| Cut wood in a straight line | Frequency of finish cuts; frequency of bevel/angle cuts; cut length; dust/debris environment |
| Reach a destination on time | Number of destinations per day; familiarity with routes; consistency of traffic conditions |
| Treat a wound | Wound type and severity; setting (hospital vs. home care); patient compliance; comorbidities |
| Optimize dairy herd productivity | Herd size; feed sourcing model; geographic climate; nutritionist relationship |

Demographic questions still go in (age, geography, role, company size) but **expect them not to drive segmentation**.

## Fraud and quality controls (Chapter 18) — bake into the survey, not after

- Attention checks (1 per ~20 min)
- Speed check (drop completions <40% of median time)
- Straight-line detection
- Consistency checks (screener vs. later answers)
- Open-text quality scan
- IP/device dedupe

Expect to drop 5–15% of responses. >25% means your panel source is bad — switch.

---

## How to run

1. **Load the netted outcomes CSV.** Validate every row has the four-part syntax.
2. **Ask the user (if missing):**
   - Named competitors (0–4) for competitive satisfaction
   - Whether to include WTP
   - Recruitment audience description (for the screener)
   - List of hypothesized complexity factors (or invoke `/hypothesizecomplexity`)
3. **Build screener questions.** 4–6 typical. Always include the "are you employed by [competitor] or in market research?" disqualifier.
4. **Build profiling questions.** ≤15. Behavioral/situational. Use objective scales ("hours per week," "% of the time") where possible.
5. **Build the importance block.** One matrix per job-map step, 8–12 rows per matrix, in netted-CSV order. Prefix: *"When [job], how important is it to you that you can [outcome]?"*
6. **Build the satisfaction block.** Same outcomes, same order. Prefix: *"How satisfied are you with the [product/category] you currently use to [outcome]?"*
7. **Build the competitive block.** Only the one product the respondent picked in profiling as their most-used. Skip-logic into a single per-product matrix.
8. **Build the WTP block (if requested).** Place at the very end. 2–4 questions: max price for "fully-satisfying solution", banded acceptable price range, hypothetical purchase intent.
9. **Pilot instructions.** Tell the user to pilot with n=10–15 before fielding to the full sample.
10. **Emit all three formats** (Markdown, JSON schema, Qualtrics TXT) by calling `scripts/survey_generator.py`.

---

## Output

Save to disk under `survey-out/`:

```
survey-out/
├── survey.md           ← human-readable, for review
├── survey.json         ← machine schema (the source of truth)
├── survey.qsf-import.txt   ← Qualtrics Advanced Import format
├── survey.typeform.json    ← Typeform import
└── field-map.csv       ← maps each survey item back to outcome ID + section
```

Then return:

```json
{
  "skill": "generatesurvey",
  "method_version": "ODI v2.4.2",
  "job_statement": "...",
  "outputs": {
    "markdown": "survey-out/survey.md",
    "json_schema": "survey-out/survey.json",
    "qualtrics_import": "survey-out/survey.qsf-import.txt",
    "typeform_import": "survey-out/survey.typeform.json",
    "field_map": "survey-out/field-map.csv"
  },
  "sections": {
    "screener": 5,
    "profiling": 12,
    "importance": 96,
    "satisfaction": 96,
    "competitive_satisfaction": 96,
    "wtp": 3
  },
  "length_estimate_minutes": 28,
  "recommended_sample_size": "n = 400-600 for 2-3 outcome-based segments",
  "incentive_recommendation": "$15-25 consumer / $75-150 B2B",
  "pilot_instruction": "Pilot with n=10-15 first. Watch them complete it. Cut any outcome that confuses them.",
  "next_step": "Field the survey. After cleaning, run /computescores on the response CSV."
}
```

---

## Sample survey skeleton (Template 4 — for your reference)

```
SECTION 1 — Screener
- Q1. How often do you [perform job]? (Disqualify if < threshold)
- Q2. Which of the following solutions do you currently use most often to [job]? (Disqualify if "none")
- Q3. Are you employed in market research or by [competitors]? (Disqualify if yes)
- Q4. Attention check: select "4"

SECTION 2 — Profiling (10–15 questions)
- Q5. [Complexity factor 1: hours/week]
- Q6. [Complexity factor 2: % of time in context X]
- …
- (then demographics: age, region, role, company size)

SECTION 3 — Importance (grouped by job step)
"When [job], how important is it to you that you can [outcome]?"
- I-D01: [outcome D-01]                                          1–5
- I-D02: [outcome D-02]                                          1–5
- …
- I-Cn: [outcome C-NN]                                           1–5

SECTION 4 — Satisfaction (same order)
"How satisfied are you with the [product] you currently use to [outcome]?"
- S-D01: …                                                       1–5
- …

SECTION 5 — Competitive satisfaction (skip-logic to the one product the respondent uses)
Same matrix as Section 4 but per-named-competitor.

SECTION 6 — Willingness to pay (optional, at the end)
- WTP1: How much would you pay for a solution that fully satisfies [top 3 outcomes]?
- WTP2: Acceptable price band (lo, hi)
- WTP3: Likelihood to purchase at midpoint (1–5)
```

## Hard refuses

- Never interleave importance and satisfaction questions.
- Never put WTP before the I/S blocks.
- Never let any outcome use a different surface phrasing than its locked netted form.
- Never produce a survey that takes >45 minutes — refuse and tell the user to cut outcomes or rotate subsets.
