---
name: mineoutcomes
description: Autonomously mine public online sources (Reddit, X/Twitter, Amazon reviews, Trustpilot, app-store comments, niche forums, Quora) for a given core functional job, and convert real customer language into candidate outcome statements in strict Ulwick syntax. SYNTHETIC ACCELERATOR — never replaces real interviews.
when_to_use: User wants a fast hypothesis-pass before commissioning real interviews, or wants to supplement /extractoutcomes with public-data candidates. Triggered by "/mineoutcomes", "mine reddit for", "scrape outcomes from", "find outcomes online".
trigger_phrases:
  - /mineoutcomes
  - "mine outcomes from"
  - "scrape outcomes"
  - "find outcomes online"
inputs:
  - the locked job statement (and ideally job map)
  - target sources (defaults: reddit, twitter, amazon-reviews, app-store, trustpilot, quora, niche forums)
  - max items per source (default: 200)
  - language filter (default: en)
outputs:
  - mined-outcomes.csv — same shape as extractoutcomes output, with source URLs preserved
  - source-evidence.md — top quotes per outcome, attributable to original posts
  - SYNTHETIC banner stamped on every file
chains_to:
  - /netoutcomes (combines with /extractoutcomes output)
  - /hypothesizecomplexity
  - /sentimentlandscape
delegates_to:
  - agent: data-miner (does the actual fetching and clustering)
  - agent: outcome-formatter (converts mined quotes into strict syntax)
helpers:
  - scripts/mine_sources.py
---

# /mineoutcomes — Mine Public Data for Outcome Candidates

## Plain-English preamble (for newcomers)

> You want a hypothesis about what people are saying online before commissioning real interviews. This skill autonomously fetches public posts (Reddit, Amazon reviews, app-store reviews, Quora answers, StackExchange threads, specialty forums) and converts the customer language into outcome candidates in strict syntax.
>
> **Output is hypothesis-only.** Use it to (1) stress-test your draft outcome list, (2) generate complexity-factor hypotheses, (3) prioritize which real-customer interviews to commission first.
>
> **Cannot replace** 20–30 real interviews or the n=300–600 survey. Every output is stamped SYNTHETIC. When fed into `/netoutcomes`, mined candidates are capped at 60% of the total pool — real interview data always takes precedence.
>
> **ToS-respecting:** uses official Reddit JSON, StackExchange API, App Store RSS. Twitter/X requires user-supplied API credentials. The skill refuses to bypass ToS.

---

> ⚠️ **SYNTHETIC ACCELERATOR.** Outputs of this skill are hypothesis-generation only. They are intended to:
> 1. Stress-test your draft outcome list before fielding interviews,
> 2. Generate complexity-factor hypotheses,
> 3. Prioritize which real-customer interviews to commission first.
>
> They are **not** a substitute for the 20–30 real interviews or the n=300–600 survey required by the ODI handbook (Part III, Part IV, Chapter 16).

---

## Method

1. **Delegate to the `data-miner` subagent** with the job statement, the candidate source list, and the max-items quota.
2. The data-miner returns a JSON dump of raw posts with text, source, URL, timestamp, engagement metrics.
3. **Delegate each post (or batch) to the `outcome-formatter` subagent**, which converts the raw quote into outcome candidates using the same strict syntax as `/extractoutcomes`.
4. **Assign each candidate to a job-map step** (or to the buckets for related jobs, emotional/social, consumption-chain, financial).
5. **Stamp every output with the SYNTHETIC banner.**
6. **Cap mined candidates at 60% of the total candidate pool** when later fed into /netoutcomes — never let mined data outvote real interviews.

## Sources and what each is good for

| Source | What it surfaces | Caveats |
|---|---|---|
| Reddit (job-relevant subreddits) | Pain points, workarounds, comparison threads | Skews young/online; tech-job overrepresented |
| X/Twitter | Real-time complaints, public reactions to launches | Heavy noise, hard to filter |
| Amazon / Best Buy / Sephora / industry-specific reviews | Concrete usage scenarios, defect modes, consumption-chain | Skews extreme reviewers (1-star and 5-star); fake-review risk |
| App-store reviews (iOS, Google Play) | Workflow friction, integration pain, "this should do X" | Limited length; mobile bias |
| Trustpilot / SiteJabber | Purchase + onboarding pain | B2C bias |
| Quora / StackExchange | "How do I…" — workaround patterns reveal unmet outcomes | Long form, more thoughtful, less venting |
| Specialist forums (audiophile, tradesman, clinician) | Highest signal-to-noise for niche jobs | Smaller volume, harder to discover |

## How to find the right subreddits / forums for a job

1. Search Google: `"<job verb> <object>" site:reddit.com`
2. Search Reddit's own search for the job verb and object separately
3. For B2B: search for trade-specific communities (e.g., `r/HVAC`, `r/finishcarpentry`)
4. Ask the user — they often know niche forums you can't find by search
5. Snowball — once you find one community, scan their sidebar/wiki for adjacent ones

## Per-post processing

For each raw post:

1. Mark whether the post contains a *pain*, a *workaround*, a *measure-of-success*, or none. Skip "none" posts.
2. Detect the underlying job-map phase.
3. Convert the raw quote → strict outcome syntax (delegate to outcome-formatter).
4. Record source URL, timestamp, upvotes/reactions (signal proxy), and the verbatim quote.

## Output

Every file is prepended with the SYNTHETIC banner:

```
================================================================
⚠️  SYNTHETIC DATA — DIRECTIONAL ONLY — DO NOT SHIP
This output was generated by LLM extraction from public online
data. It is intended ONLY for hypothesis generation and to inform
which real-human interviews to commission first.

Before any roadmap, pricing, or value-prop decision, validate
against n ≥ 300 real respondents per ODI v2.4.2, Chapter 16.
================================================================
```

CSV:

```csv
candidate_id,job_step,direction,metric,object_of_control,clarifier,full_statement,source,source_url,timestamp,engagement,verbatim_quote,confidence
M-D-001,Define,Minimize,the time it takes to,determine the right pair of headphones for the activity,,Minimize the time it takes to determine the right pair of headphones for the activity,reddit,https://reddit.com/r/headphones/comments/xyz,2026-04-12,87,"I spend more time choosing which earbuds to take than actually listening once I leave the house",0.82
```

JSON summary:

```json
{
  "skill": "mineoutcomes",
  "method_version": "ODI v2.4.2",
  "data_provenance": "SYNTHETIC — directional only, do not ship",
  "job_statement": "Listen to music while on the go",
  "sources_used": [
    {"name": "reddit", "subreddits": ["r/headphones", "r/audiophile", "r/spotify"], "posts_fetched": 380},
    {"name": "amazon-reviews", "products": ["AirPods Pro 2", "Sony WF-1000XM5", "Bose QC Earbuds II"], "reviews_fetched": 412},
    {"name": "twitter", "queries": ["airpods battery", "spotify offline broken"], "tweets_fetched": 220},
    {"name": "quora",  "questions": 38}
  ],
  "candidates_extracted": 134,
  "candidates_by_step": {"Define": 11, "Locate": 17, "Prepare": 22, "Confirm": 4, "Execute": 41, "Monitor": 14, "Modify": 13, "Conclude": 6, "consumption_chain": 6},
  "outputs": {
    "csv": "mined-outcomes.csv",
    "evidence_md": "source-evidence.md"
  },
  "guardrail_check": {
    "synthetic_banner_applied": true,
    "do_not_ship_marked": true,
    "validation_required": "n >= 300 real respondents"
  },
  "next_step": "Combine mined-outcomes.csv with output of /extractoutcomes (if any) and pass into /netoutcomes. Real interview candidates take precedence in dedupe."
}
```

## Hard rules

- Never strip the SYNTHETIC banner.
- Never use scraped posts that violate ToS — prefer official APIs (Reddit's API, X's API), or RSS-style endpoints. If the user requests bypass, refuse.
- Never present mined outcomes as having "respondents" or "respondent counts." They have *posts* and *posters*.
- Never feed mined outcomes into /computescores directly — they go through /netoutcomes first, capped at 60% of the total candidate pool.
