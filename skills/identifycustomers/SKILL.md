---
name: identifycustomers
description: Identify all three ODI customer types — the job executor, the lifecycle support person, and the purchase decision maker (Chapter 5). Each must be screened and interviewed separately. Mixing them is mistake #4 of the twelve most common. Skipping the buyer is how most B2B engagements fail — you build a great product nobody is willing to pay for.
when_to_use: Right after /definejob and before /generatescreener. Triggered by "/identifycustomers", "/customertypes", "who are the customers", "who do I interview", "who is the buyer". Also called by /runfullodi as Phase I step 2.
trigger_phrases:
  - /identifycustomers
  - /customertypes
  - "who are the customers"
  - "who do I interview"
  - "who is the buyer"
inputs:
  - locked job statement
  - market context (B2C or B2B; industry; rough revenue model)
outputs:
  - the three customer types named explicitly, with role title + how to recognize them
  - which types apply to this engagement (all three vs. just executor for simple B2C)
  - recruiting plan: n per type, screener variants
  - interview structure per type
chains_to:
  - /generatescreener (run once per type that applies)
  - /extractoutcomes (per type's transcript pool)
---

# /identifycustomers — Three customer types, never one

> **Plain English:** Most teams interview "customers" as if they were one group. ODI says no — there are usually **three** different people involved with any job, and they care about different things. Talk to all three. Mix them up in the same interview pool and your data turns to mush.

## The three types (Ch 5)

| Type | Who they are | What they care about |
|---|---|---|
| **Job executor** | The person who personally performs the functional job | Functional outcomes on the job (Minimize time / Minimize likelihood / etc.) |
| **Lifecycle support** | The person who installs, maintains, trains, repairs, or disposes of the solution | Consumption-chain outcomes (Ch 12) |
| **Purchase decision maker (buyer)** | The person who picks the solution and pays | **Financial outcomes (Ch 13)** — ROI, switching cost, capital cost, risk |

### Concrete examples

| Job | Executor | Lifecycle | Buyer |
|---|---|---|---|
| Cut a piece of wood in a straight line | Tradesman swinging the saw | The tradesman themselves (small tool) | Tradesman or shop owner |
| Monitor a patient's vital signs during anesthesia | Anesthesiologist | Hospital biomed engineer | Hospital procurement + clinical chief |
| Listen to music while on the go | The listener | The listener (small consumer item) | The listener |
| Deploy enterprise SaaS to a team | IT admin / power user | IT operations / support team | CIO / CFO / Procurement |

## When all three are the same person

In simple B2C ("listen to music"), the executor / lifecycle / buyer are often **all the same person**. You still interview them, but you don't need three separate recruits — you interview the same person about all three roles.

In B2B and complex B2C (medical devices, vehicles, expensive appliances), they're **different people** and need **separate** recruits and interviews. **Skipping the buyer is how most B2B engagements fail** — you build a great product and nobody is willing to pay for it because the buyer cares about ROI metrics you never captured.

## Recruiting plan (Ch 9 + Ch 13)

| Type | Recommended sample |
|---|---|
| Executor | 15–25 qualitative interviews; n=300–600 survey |
| Lifecycle support | 5–10 qualitative interviews; survey only if they're a distinct group |
| Buyer | 5–10 qualitative interviews; n=100+ survey if B2B with high-ticket purchase |

## Interview structure per type (Ch 10 + Ch 13)

| Type | Length | Anchor | What you ask |
|---|---|---|---|
| **Executor** | 60–90 min | The job map (walk every step) | "What slows you down here?" / "What's the measure of success?" |
| **Lifecycle support** | 45–60 min | The consumption chain | "What goes wrong in install / train / maintain / dispose?" |
| **Buyer** | 30–45 min | The purchase decision | "What metrics do you compare alternatives on?" / "What's the numerator and denominator of your ROI calc?" |

> ⚠️ **Common mistake** — letting the buyer drift into the user's hat mid-interview. If a hospital admin starts answering as if they were the surgeon, redirect them.

## How to run

1. **Read the locked job statement** from `/definejob` output.
2. **Ask the user (interactive)**:
   - Is this B2C, B2B, or hybrid?
   - Is the same person executing, maintaining, AND buying?
   - For B2B: who signs the check?
3. **Map the three types** for this engagement (each named explicitly with example titles).
4. **Mark which apply** as separate recruits — all three, two, or one (collapsed).
5. **Recommend a recruiting plan**: n per type + screener variant.
6. **Output a per-type interview brief** with the structure above.

## Output

```json
{
  "skill": "identifycustomers",
  "method_version": "ODI v2.4.2",
  "job_statement": "Monitor a patient's vital signs during anesthesia",
  "market_context": "B2B medical device, U.S. hospitals",
  "customer_types": [
    {
      "type": "job_executor",
      "role_titles": ["Anesthesiologist", "Nurse Anesthetist (CRNA)"],
      "how_to_recognize": "Personally administers anesthesia and reads the monitor in real time",
      "recruit_separately": true,
      "n_qualitative_target": 20,
      "n_survey_target": 300,
      "interview_anchor": "job_map_walkthrough",
      "screener_variant": "executor"
    },
    {
      "type": "lifecycle_support",
      "role_titles": ["Hospital biomed engineer", "Clinical-engineering technician"],
      "how_to_recognize": "Maintains and calibrates the monitor; manages firmware updates",
      "recruit_separately": true,
      "n_qualitative_target": 8,
      "n_survey_target": 80,
      "interview_anchor": "consumption_chain",
      "screener_variant": "lifecycle"
    },
    {
      "type": "purchase_decision_maker",
      "role_titles": ["Chief of anesthesia department", "Hospital procurement director", "VP of clinical operations"],
      "how_to_recognize": "Final approval on capital equipment purchases ≥ $20k",
      "recruit_separately": true,
      "n_qualitative_target": 8,
      "n_survey_target": 120,
      "interview_anchor": "purchase_decision_journey",
      "screener_variant": "buyer",
      "financial_outcomes_focus": ["per-procedure consumable cost", "training time on new equipment", "warranty claim risk", "5-year TCO"]
    }
  ],
  "collapsing_decision": "no_collapse — B2B medical device; three roles are three different people",
  "next_step": "Run /generatescreener three times — once per customer type. The screeners are NOT interchangeable."
}
```

## Hard rules

- For B2B, treat the three types as separate unless the user provides explicit evidence they're the same person.
- Always surface the **financial outcomes** focus for the buyer type — that's the thing teams most often skip.
- For simple B2C, collapse the roles explicitly and document the collapse in `collapsing_decision`.
- Refuse to skip the buyer for any B2B engagement with a purchase price >$5k. That's where the failure happens.
