# GLOSSARY — Every ODI term in plain English

A newcomer-friendly translation of the jargon you'll see in this plugin and in Ulwick's handbook.

If a term appears in a SKILL.md or command output and you don't recognize it, look it up here.

---

## Acceptance criteria
Measurable thresholds an engineer can build against, expressed in physical or behavioral units (not adjectives). "<5% of cuts produce face-zone debris" is acceptance criteria. "Make it feel safer" is not. Produced by `/outcometospec`.

## Appropriately served
An outcome the market satisfies adequately. Opportunity score < 10. Not an innovation target. Don't ignore it (still has to be at parity in your product) but don't over-invest.

## Beachhead segment
The first customer group you target — the one most underserved AND with the highest willingness to pay. Picked from `/runsegmentation` + `/choosestrategy`.

## Christensen JTBD vs. Ulwick JTBD
Two different methods sharing the name "Jobs to be Done." This plugin teaches the **Ulwick** school — quantitative, structured, opportunity-scored. The **Christensen** school is qualitative and narrative ("jobs as stories"). They're not interchangeable. If you came in expecting "milkshake-marketing" narratives, you're in the wrong tool.

## Complexity factor
A **situational** variable that explains why some job-executors struggle more than others. Examples: how often a tradesman makes finish cuts; herd size for a dairy farmer; wound severity for a clinician. Complexity factors drive segmentation in ODI — demographics rarely do. Captured in the survey's profiling block.

## Compound statement
An outcome that bundles two measurable things into one ("minimize the time AND effort to clean the device"). Forbidden — split into two outcomes. Caught by `/validateoutcomes`.

## Consumption-chain job
The lifecycle work surrounding the core job — research → purchase → install → set up → learn → use → store → transport → maintain → upgrade → repair → dispose. Captured by `/extractoutcomes` (separately from core-job outcomes). Often hidden gold in B2B (see Microsoft Software Assurance example, Ch 12).

## Contextual clarifier
The optional "when X" / "during Y" / "e.g., from a ladder" at the end of an outcome statement. Pins down the situation so survey respondents are rating the same thing.

## Desired outcome (or just "outcome")
The atomic unit of ODI. Strict 4-part syntax: **direction** + **metric** + **object of control** + **(optional) clarifier**. Example: "Minimize the time it takes to set the angle of the blade." You collect 50–150 of these per engagement.

## Differentiated strategy
The growth posture for "better job-done, premium price." Tesla, iPhone, Cordis stent. The default when the landscape is underserved and the segment has high willingness to pay. From `/choosestrategy`.

## Direction of improvement
The first word of an outcome statement. Always one of two: **Minimize** or **Increase**. Never "reduce," "prevent," "eliminate," "avoid," "improve" — those produce measurably different survey ratings even though they look synonymous.

## Discrete strategy
The trap cell of the Growth Matrix. "Worse job-done at higher price." Survives only on captive demand (airport food, prison phones). If `/choosestrategy` places you here, exit the cell — don't celebrate it.

## Disruptive strategy
The growth posture for "worse job-done, much lower price." Southwest, Vanguard, Canva. The right move when the landscape is overserved and you can bring in non-consumers.

## Dominant strategy
"Better job-done AND lower price." Rare — requires a real cost breakthrough (IP, manufacturing scale, supply-chain). `/choosestrategy` refuses to recommend this without a user-confirmed cost advantage.

## Extreme opportunity
An outcome scoring ≥ 15. Top priority. Often unlocks a Differentiated or Dominant posture.

## Factor analysis
A statistical technique that reduces many correlated outcomes to a smaller number of latent **factors**. Used in `/runsegmentation` (Appendix C) before k-means. The factors group outcomes that respondents tend to rate similarly.

## Financial outcome
An outcome the **purchase decision maker** (the buyer) uses to compare alternatives. Direction + metric + object + clarifier, but the object is a cost / ROI / risk metric rather than a functional one. "Minimize the per-procedure consumable cost." Captured by `/extractoutcomes` (separately) from buyer interviews (Ch 13).

## Front end of innovation
The "what should we build?" decisions, before engineering. ODI lives here. ODI is the wrong tool for "how do we ship faster" (which is the back end).

## Functional job
The job statement that's purely about what the customer is trying to accomplish, stripped of emotional and social baggage. Verb + object + clarifier. "Cut a piece of wood in a straight line." (Emotional and social jobs are captured separately.)

## Gap analysis
The naive predecessor to the opportunity formula — just `Importance − Satisfaction`. ODI's formula re-adds Importance because important-but-unmet > unimportant-and-unmet at the same gap. See "opportunity formula."

## Growth Strategy Matrix
The 5-cell matrix that names the postures: Differentiated, Dominant, Disruptive, Discrete, Sustaining. Defined by two questions: does the product get the job done better/worse, and is it more/less expensive? Placement is data-driven — from `/choosestrategy`.

## Importance
In the formula: **the percentage of respondents who rated the outcome 4 or 5 (top-2-box) on the survey's importance question**, normalized to 0–10. So 74% → 7.4.

## Job executor
The person who personally performs the functional job. One of three customer types. Interviewed separately from the buyer and the lifecycle support staff. (Ch 5)

## Job map
The 8-step universal sequence: Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude. NOT a process map or customer journey — those bake in today's solutions. The job map is solution-agnostic.

## Job statement
The one-sentence formulation of what the customer is trying to accomplish. Verb + object + optional clarifier. The most important sentence in the project. Most teams get it wrong the first three tries.

## K-means
A clustering algorithm. In ODI, used in `/runsegmentation` on factor scores to group respondents into segments with similar unmet-need patterns.

## Lifecycle support
The customer type that installs, maintains, trains, repairs, or disposes of the solution. One of the three customer types. Their outcomes are mostly in the consumption chain.

## Lite ODI
Qualitative-only ODI (no survey). Produces directional opportunity hypotheses rather than statistically defensible scores. Use when budget < $10k or timeline < 3 weeks. (`/runliteodi`)

## Low-hanging fruit
An outcome scoring 12–15. Strong innovation candidate; the best fit for short-term roadmap moves.

## Netting
Ulwick's term for the process of deduping and refining 300–600 raw outcomes from interviews into 50–150 well-formed final outcomes. (Ch 14, `/netoutcomes` or `/refineoutcomes`)

## Object of control
The noun phrase the metric attaches to in an outcome statement. Example: in "Minimize the time it takes to set the angle of the blade," the object of control is "set the angle of the blade."

## One-dimensional
A characteristic of a well-formed outcome statement: one direction, one metric, one object. No compound statements.

## Opportunity formula
`Opportunity = Importance + max(Importance − Satisfaction, 0)`. The single equation at the heart of ODI. Importance is double-weighted (because important-but-unmet beats unimportant-and-unmet); the max() floor prevents over-served outcomes from going negative.

## Opportunity Landscape
The chart that plots every outcome by importance (y) and satisfaction (x). Four zones: Underserved, Table stakes, Appropriately served, Overserved. The diagonal divides served from overserved; the opp=10 line divides underserved from the rest. Produced by `/computescores`.

## Opportunity score
An outcome's value 0–20 from the formula. Higher = better innovation target. Thresholds:
- ≥ 15: Extreme opportunity
- 12–15: Low-hanging fruit
- 10–12: Worth considering
- < 10: Appropriately served
- Sat > Imp: Overserved

## Outcome-based segmentation
The ODI-specific way to find segments — cluster respondents on their **unmet-outcome** patterns (factor analysis → k-means) rather than on demographics or use cases. Then profile each cluster with complexity factors to explain *why* it exists.

## Outcome-based value proposition
A four-part sentence: "For [segment], who are trying to [job], our [product] helps them [address these underserved outcomes], unlike [next-best alternative], because of [reason to believe]." Every clause traces to data. (Ch 25)

## Overserved
An outcome where satisfaction exceeds importance. Disruption zone — strip cost; the market is paying for capability it doesn't value.

## Pre-flight check
Ulwick's Ch 4 checklist for "should you even do ODI?" Run via `/preflight` BEFORE you commit budget. It can save you 8 weeks on the wrong method.

## Profiling questions
The survey block (≤15 questions) that captures complexity factors + demographics. Used in `/runsegmentation` to explain *why* segments exist. Demographics-only profiling is a common mistake — complexity factors are the actual segmentation engine.

## Purchase decision maker (buyer)
The customer type who picks the solution and pays. One of the three. In B2B, almost always a different person from the executor. Skipping the buyer is how most B2B engagements fail. Their outcomes are mostly financial.

## Reason to believe
The fifth piece of the value proposition. The specific technology / design / IP / partnership / platform decision that lets your product satisfy underserved outcomes ≥20% better. "We work harder" is not a reason to believe.

## Related job
A different functional job the executor wants to do at the **same time** as the core job. "Time the cut so it finishes before the battery dies" is a related job to "Cut wood in a straight line." 5–20 per engagement. Captured by `/extractoutcomes`.

## Satisfaction
In the formula: the percentage of respondents who rated their satisfaction with the outcome 4 or 5 (top-2-box), normalized to 0–10. Optionally captured per competitor.

## Segment
A group of customers with similar unmet-outcome patterns. In ODI, defined by clustering on the outcomes themselves, not on demographics. Each segment is profiled by 1–3 complexity factors.

## Solution-agnostic
A property of well-formed job statements and outcome statements: they don't name any product, brand, technology, or feature. "Minimize the likelihood that the laser guide drifts" is NOT solution-agnostic; "Minimize the likelihood of moving off the cut line" is. `/validateoutcomes` flags violations.

## Sustaining strategy
The 5th cell of the Growth Matrix — slightly better, slightly cheaper. The incumbent's share-defense move. Maintenance, not growth.

## Synthetic data
Outputs from the plugin's mining / persona / virtual-respondent agents. **HYPOTHESIS-GENERATION ONLY.** Cannot replace real interviews or the n=300–600 survey. Every synthetic output is stamped accordingly. `/generatevalueprop`, `/buildroadmap`, `/choosestrategy`, `/outcometospec` refuse to chain off synthetic data.

## Table stakes
Outcomes with high importance AND high satisfaction. Opportunity score < 10 because the gap is small. Your product must satisfy them at parity (or better) or you lose anyway — but they're not innovation targets.

## Top-2-box
The percentage of respondents who picked 4 or 5 on a 5-point scale (or 9–10 on a 10-point scale). The scoring rule for both Importance and Satisfaction in ODI. Not the mean. Not the median. Specifically the top-2-box, normalized to 0–10.

## Twenty-percent rule
Strategyn's empirical switching threshold: to win meaningful share on an underserved outcome, your product must satisfy it ~20% better than the best competing solution. Under 5% better is "stuck in the middle" — customers won't switch. Used by `/competitiveanalysis` and `/outcometospec` to set acceptance criteria.

## Underserved
An outcome with high importance and low satisfaction — opportunity ≥ 10. Innovation target. Cluster of these in your data → Differentiated or Dominant posture is on the table.

## Universal job map
The 8 phases — Define / Locate / Prepare / Confirm / Execute / Monitor / Modify / Conclude — that almost every functional job decomposes into. From Bettencourt & Ulwick, HBR May 2008. Used as scaffolding for outcome capture.

## Variability strips
The Ch 11 Table 11.4 sins that practitioners introduce unconsciously and that wreck prioritization: non-canonical direction verbs (reduce/prevent/etc.), vague adjectives ("frequently"), inconsistent nouns for the same object, compound statements, embedded solutions. `/validateoutcomes` catches them.

## Willingness to pay (WTP)
The optional 3-question block at the end of the survey that surfaces the price band the target segment will actually pay. Computed by `opportunity_scorer.py` and consumed by `/choosestrategy.pricing_band`. Place at the very end of the survey — never before the importance/satisfaction blocks.
