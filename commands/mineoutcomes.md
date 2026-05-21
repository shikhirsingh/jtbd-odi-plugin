---
description: SYNTHETIC ACCELERATOR — Mine Reddit, X/Twitter, Amazon/Trustpilot reviews, app-store reviews, Quora, and forums for candidate outcomes in strict Ulwick syntax. HYPOTHESIS-GENERATION ONLY — never replaces real interviews.
argument-hint: "<job statement>" [--sources reddit,amazon,quora,appstore] [--max-per-source 200]
---

# /mineoutcomes — Mine public data for outcome candidates

## What this is doing (plain English)

You want a hypothesis about what people are complaining about, before you commission real interviews. This skill autonomously fetches public posts (Reddit threads, Amazon reviews, app-store reviews, Quora answers, niche forums) about your job, then converts the customer language into properly-formatted outcome candidates.

**Output is hypothesis-only.** It can prepare your interview guide, stress-test your draft outcome list, or feed `/sentimentlandscape` for a pre-survey directional view. It cannot replace the 20–30 real interviews or the n=300+ survey.

## What you need before running this

- A locked job statement
- (Optional) source list (defaults: reddit, amazon-reviews, app-store, quora, stackexchange — twitter/X needs API credentials)
- (Optional) per-source quota (default 200)

## What you'll get back

- `mined-outcomes.csv` — candidates in strict syntax, with source URL + verbatim quote preserved per row
- `source-evidence.md` — top quotes per outcome, attributable to the original posts
- **SYNTHETIC banner** stamped on every file

When fed into `/netoutcomes`, mined candidates are capped at 60% of the total candidate pool — real interview data always takes precedence.

## Important constraints

- ToS-respecting: uses official Reddit JSON, StackExchange API, App Store RSS, etc. Twitter/X requires user API credentials. The skill refuses to bypass ToS.
- Public attribution preserved (source URL per row), no PII inference beyond public username.
- English-only by default.

## What runs after this

For hypothesis preparation: `/hypothesizecomplexity` (read complexity factors from the mined data) → `/sentimentlandscape` (pre-survey directional landscape).

For the full synthetic pipeline (mine + personas + simulated survey): `/run-synthetic-survey`.

Mined candidates should still pass through `/netoutcomes` + `/validateoutcomes` like any other raw outcome.

---

Invoke the `mineoutcomes` skill. Delegate to `data-miner` subagent for fetching, then to `outcome-formatter` subagent for syntax conversion. STAMP SYNTHETIC. Refuse to bypass ToS on any source.
