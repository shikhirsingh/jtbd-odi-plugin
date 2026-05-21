---
name: hypothesizecomplexity
description: Generate hypothesized complexity factors for segmentation — situational, behavioral variables that explain why some job-executors struggle more than others — from mined online data and/or qualitative transcripts. Implements Chapter 17 + Strategyn's "complexity factors are the engine of segmentation" principle.
when_to_use: User is designing the survey and needs the profiling block, or wants a head-start on segmentation hypotheses before fielding. Triggered by "/hypothesizecomplexity", "what complexity factors", "what should I profile on", "what explains segmentation".
trigger_phrases:
  - /hypothesizecomplexity
  - "complexity factors"
  - "profiling questions"
  - "what should I profile on"
inputs:
  - the locked job statement (and job map)
  - one or more sources: mined-outcomes.csv (from /mineoutcomes), interview transcripts, or raw user description
outputs:
  - 8–15 candidate complexity factors with rationale
  - for each: proposed question wording, scale, why it might drive segmentation, what segment hypothesis it tests
  - explicit ranking by likely segmentation power (high / medium / low)
chains_to:
  - /generatesurvey (the profiling block uses these)
  - /run-synthetic-survey (used to define persona axes)
---

# /hypothesizecomplexity — Hypothesize Complexity Factors

## Plain-English preamble (for newcomers)

> Your survey will have a profiling section with ≤15 questions. Most teams fill it with demographics. **Demographics rarely drive segmentation in ODI.** What does is **complexity factors** — situational variables that make the job harder for some users than others.
>
> Examples: daily commute length, finish-cut frequency, herd size, wound severity, setting (hospital vs home), number of devices switched between per day.
>
> This skill proposes 8–15 candidate complexity factors, each grounded in your job map / mined data / interview transcripts, ranked by expected segmentation power.
>
> Plain-English alias: `/complexityfactors`.

---

> "The things that explain why executors struggle differently are not demographics. They are **complexity factors** — situational variables that make the job harder for some people than others." (Chapter 17)

A great segmentation depends on the right profiling questions. Without complexity factors, segmentation is uninterpretable — you can find clusters but can't tell anyone *why* they exist.

## Examples by job (Table 17.1)

| Job | Complexity factors that explain segments |
|---|---|
| Cut wood in a straight line | Frequency of finish cuts; frequency of bevel/angle cuts; cut length; presence of dust/debris in the work environment |
| Reach a destination on time | Number of destinations per day; familiarity with routes; consistency of traffic conditions |
| Treat a wound | Wound type and severity; setting (hospital vs. home care); patient compliance; comorbidities |
| Optimize dairy herd productivity | Herd size; feed sourcing model; geographic climate; nutritionist relationship |
| Listen to music while on the go | Daily commute length; commute mode (walk/transit/drive); noise environment; multi-device switching frequency; format mix (podcast/music/audiobook); offline-listening frequency |

## What makes a good complexity factor (Chapter 17)

1. **Situational, not preference-based.** Ask "How often do you make finish cuts?" not "Do you like finish cuts?" *Behavior > opinion.*
2. **Objective scale where possible.** Hours/week, % of the time, number of [thing], frequency band — avoid Likert preference scales.
3. **Plausibly explains variation in unmet outcomes.** Each candidate factor should have a story: *"if executors do X more often, we'd expect outcomes Y and Z to be more underserved for them."*
4. **Collectible in <30 seconds in a survey.** If the question requires a paragraph or document upload, it's too heavy.

## How to generate them

1. **From the job map**, walk each step and ask: *what makes this step easier or harder?* Variables that change difficulty are candidate factors.
2. **From mined outcomes or transcripts**, look for *qualifier phrases* the customer uses: "when I'm doing bevel cuts, the part that's hard is…" — the qualifier ("when I'm doing bevel cuts") is a complexity-factor candidate.
3. **From the industry / category**, list 2–4 known dimensions on which buyers differ (e.g., for B2B SaaS: company size, tech stack maturity, integration complexity).
4. **Rank** each candidate by likely segmentation power — high / medium / low — based on how much variance you expect across the executor population.

## What NOT to do

- Don't list demographics first. Age, gender, geography go in the survey for completeness but rarely drive innovation segmentation.
- Don't propose more than 15 complexity factors. Each one adds survey fatigue.
- Don't propose factors that aren't grounded in evidence — every candidate needs a 1-line rationale tied to either the job map, a mined quote, an interview, or a known industry dimension.

## Output

```json
{
  "skill": "hypothesizecomplexity",
  "method_version": "ODI v2.4.2",
  "job_statement": "Listen to music while on the go",
  "candidate_complexity_factors": [
    {
      "rank": 1,
      "name": "daily_commute_length_minutes",
      "question": "On a typical workday, roughly how many minutes do you spend listening to audio while traveling outside your home?",
      "scale": "open numeric (0–600 min)",
      "rationale": "Long-commute executors interact with every job-map phase more times per day; expected to have very different outcome priorities than short-commute executors. Mined outcomes from /r/audiophile cluster around 30+ min commuters reporting battery, glitch, and queueing pains; 5-min commuters do not.",
      "expected_segmentation_power": "high",
      "expected_segment_hypothesis": "Long-commute users → underserved on offline reliability, queue length, battery; Short-commute → mostly table-stakes."
    },
    {
      "rank": 2,
      "name": "primary_listening_environment",
      "question": "Which of the following best describes where you listen most often while on the go?",
      "scale": "single-select: quiet transit, busy street, gym/exercise, driving, open-plan office",
      "rationale": "Noise environment drives the Monitor and Modify phases of the job map significantly. Mined quotes from r/headphones repeatedly invoke 'gym vs. commute' as a switching context.",
      "expected_segmentation_power": "high",
      "expected_segment_hypothesis": "Gym/exercise → underserved on sweat resistance and fit; busy-street → underserved on environmental awareness; driving → underserved on glanceable control."
    },
    {
      "rank": 3,
      "name": "multi_device_switch_frequency",
      "question": "Across a typical day, how often do you switch your audio output between devices (phone ↔ laptop ↔ tablet ↔ TV)?",
      "scale": "Never / 1–2 times / 3–5 times / 6+ times",
      "rationale": "Switching is a Prepare/Locate phase pain. Many Reddit posts cite Bluetooth pairing reliability as the single biggest 'I switched away' driver.",
      "expected_segmentation_power": "high"
    },
    {
      "rank": 4,
      "name": "offline_listening_frequency",
      "question": "What percent of your listening time is offline (no internet connection)?",
      "scale": "0–100%",
      "rationale": "Offline executors have a fundamentally different Locate/Prepare pattern; they pre-stage content.",
      "expected_segmentation_power": "medium"
    },
    {
      "rank": 5,
      "name": "content_mix",
      "question": "Of your typical listening time, what percent is music vs. podcast vs. audiobook vs. other?",
      "scale": "four percents summing to 100",
      "rationale": "Different content types stress Define and Modify differently — podcasts are often returned to mid-episode; music is sequenced.",
      "expected_segmentation_power": "medium"
    },
    {
      "rank": 6,
      "name": "hearing_assistance_used",
      "question": "Do you use hearing aids, single-side headphones for medical reasons, or audio accommodations?",
      "scale": "yes / no",
      "rationale": "Single-side and amplification users may have an entirely different outcome profile; small but distinct segment.",
      "expected_segmentation_power": "medium"
    },
    {
      "rank": 7,
      "name": "household_size_with_audio",
      "question": "How many other people in your household share your audio devices or streaming account?",
      "scale": "0 / 1 / 2 / 3+",
      "rationale": "Account sharing impacts Define (recommendation pollution) and Conclude (queue cleanup).",
      "expected_segmentation_power": "low"
    },
    {
      "rank": 8,
      "name": "device_age_months",
      "question": "How old is the audio device you use most often while on the go?",
      "scale": "0–60 months",
      "rationale": "Older device users have different Monitor/Modify pains (battery degradation).",
      "expected_segmentation_power": "low"
    }
  ],
  "demographics_to_collect_anyway": ["age_band", "gender", "geo_country", "household_income_band"],
  "next_step": "Pass top 8–12 into /generatesurvey as the profiling block. After fielding, /runsegmentation will surface which actually explain segments."
}
```

## Hard rules

- Ground every candidate in the job map, a mined quote, an interview, or a known industry dimension. Pure speculation gets dropped.
- Never propose more than 15 factors.
- Always rank by expected segmentation power.
- If invoked from mined data only, stamp the output with the SYNTHETIC banner.
