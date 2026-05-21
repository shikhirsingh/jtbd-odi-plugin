# Worked example — synthetic-survey pipeline for "Listen to music while on the go"

This walks through `/run-synthetic-survey` end-to-end, showing what the orchestrator produces and how it stays within its hypothesis-only guardrails.

```text
================================================================
⚠️  SYNTHETIC HYPOTHESIS REPORT — DIRECTIONAL ONLY — DO NOT SHIP
This walkthrough demonstrates the synthetic-survey pipeline. The
outputs are LLM-simulated and grounded in public online data. Treat
them as structured hypotheses, NOT decision-grade survey results.
Field n ≥ 300 real respondents before any roadmap / pricing /
value-prop decision (ODI v2.4.2, Chapter 16).
================================================================
```

## 0. The one-line invocation

```text
> /run-synthetic-survey "Listen to music while on the go"
```

## 1. Job + map (auto-runs because no prior context)

The orchestrator silently calls `/definejob` and `/buildjobmap` first:

- Job locked: **Listen to music while on the go** (passes all rules + stability checks)
- Job map: 8 steps from Define-what-to-listen-to → Conclude-the-session.

## 2. Mine public data → `data-miner` agent

Sources attempted: reddit, app-store-rss (iOS), amazon-reviews, quora, stackexchange. Twitter/X skipped (no API credential provided).

```text
[data-miner] reddit         — fetched 380 posts (r/headphones, r/audiophile, r/spotify, r/AppleMusic, r/AudioTechnica)
[data-miner] amazon_reviews — 412 reviews across AirPods Pro 2, Sony WF-1000XM5, Bose QC Earbuds II
[data-miner] app_store_rss  — 41 reviews (Spotify, Apple Music, YouTube Music)
[data-miner] quora          — 38 high-vote answers
[data-miner] stackexchange  — 22 superuser.com posts
[data-miner] total relevant after filter: 612 / 1240
```

## 3. Convert quotes → outcome candidates → `outcome-formatter` agent

`134` candidates extracted across all sources. Sample:

| Source | Verbatim (truncated) | Outcome candidate |
|---|---|---|
| reddit/headphones | "Every single time I walk into a meeting room, my AirPods re-pair to whatever my coworkers had…" | Minimize the likelihood that audio re-routes to an unintended device when entering an environment with other paired devices |
| amazon/sony | "Battery dies right when I'm on the back half of my commute home, every. single. day." | Minimize the likelihood that battery runs out before the end of a typical listening session |
| quora | "How do I make my Spotify queue actually keep the songs in the order I want?" | Minimize the time it takes to get the songs in the desired order for listening |

## 4. Net (auto-calls /netoutcomes)

134 candidates → **88 netted outcomes**. Heavy dedupe in Execute (audio quality, battery, signal drops) and Prepare (pairing, EQ).

## 5. Hypothesize complexity factors (auto-calls /hypothesizecomplexity)

9 candidate factors:

1. daily_commute_min (high)
2. primary_listening_environment (high)
3. multi_device_switch_frequency (high)
4. offline_listening_pct (medium)
5. content_mix_podcast_pct (medium)
6. hearing_assistance_used (medium)
7. household_size_with_audio (low)
8. device_age_months (low)
9. ear_anatomy_fit_difficulty (medium)

Top 8 fed into the survey profiling block.

## 6. Synthesize personas → `persona-synthesizer` agent

6 personas, each grounded in 2–5 verbatim quotes:

| ID | Label | Quotes | Archetype |
|---|---|---|---|
| P1 | Long-commute audiophile switcher | 4 (reddit ×3, amazon ×1) | Frustrated power user |
| P2 | Gym-first sweat-resistant fan | 3 (amazon ×2, quora ×1) | Active settled user |
| P3 | Driver who wants glanceable controls | 5 (reddit ×2, app-store ×2, quora ×1) | Pragmatic |
| P4 | Occasional walker, default-satisfied | 3 (amazon ×3) | Casual happy |
| P5 | Multi-device power user (laptop ↔ phone ↔ TV) | 4 (reddit ×2, stackexchange ×2) | Frustrated pro |
| P6 | Hearing-assistance user | 2 (reddit ×1, quora ×1) | Specialty / overlooked |

## 7. Build the survey (auto-calls /generatesurvey)

88 outcomes × 2 + 8 profiling + 3 WTP. Estimated length: 26 min. Length passes the <45-min hard rule.

## 8. Run virtual respondents → `virtual-respondent` agent

6 personas × 60 sampled rows = **360 synthetic rows**. Each row:

- Identical persona_id.
- Profiling values perturbed ±10%.
- Imp + Sat ratings drawn from per-bias distributions (very_high → 55% rate 5, etc.).
- Outcome-specific anchors override bias-by-step.
- 3% don't-knows, 5% drift noise.
- Completion time 25–35 min (logged).

## 9. Output schema (drop-in for /computescores)

```
synthetic-out/
├── personas.json
├── synthetic_survey.csv         ← 360 rows, schema identical to a real survey CSV
├── mined-outcomes.csv
├── source-evidence.md
└── hypothesis-summary.md        ← stamped SYNTHETIC, lists top hypothesized opportunities
```

## 10. Hypothesis landscape (run /computescores on the synthetic CSV)

```text
> /computescores synthetic-out/synthetic_survey.csv --synthetic
```

Top hypothesized opportunities (all classifications carry `_HYPOTHESIS`):

| ID | Outcome | Imp_h | Sat_h | Opp_h | Class |
|---|---|---|---|---|---|
| P-04 | Minimize likelihood that audio re-routes to unintended device | 8.7 | 1.9 | 15.5 | extreme_opportunity_HYPOTHESIS |
| E-08 | Minimize likelihood battery runs out before end of session | 8.9 | 3.1 | 14.7 | low_hanging_fruit_HYPOTHESIS |
| D-02 | Minimize time to get songs in desired order | 7.6 | 2.4 | 12.8 | low_hanging_fruit_HYPOTHESIS |

## 11. Hypothesis segments (run /runsegmentation)

3 hypothesis segments:

- Sx_A — Multi-device power users (combines P1 + P5) — underserved on pairing, queueing.
- Sx_B — In-motion specialists (P2 + P3) — underserved on glanceability, environmental fit.
- Sx_C — Settled / specialty (P4 + P6) — mostly table stakes.

## 12. What the orchestrator tells the user next

```text
✓ Synthetic pipeline complete.
✓ All outputs stamped SYNTHETIC — DO NOT SHIP.

Recommended next moves:
1. Refine the netted outcome list — see drop/add suggestions in hypothesis-summary.md.
2. Commission 8–12 real qualitative interviews. Prioritize: 4 from
   P1-profile (long-commute, multi-device), 2 each from P2, P3, P5.
3. Field the real survey to n=400–600 using P1..P6 as quota targets.
4. Re-run /computescores and /runsegmentation on the REAL data.

DO NOT run /generatevalueprop or /buildroadmap on this synthetic
output. These are decision-grade only against the real survey.
```

If the user attempts `/generatevalueprop` against the synthetic CSV anyway, the skill refuses:

```
✗ /generatevalueprop refused — input is SYNTHETIC.
Value propositions are decision-grade artifacts. Validate the
underlying opportunity scores with n ≥ 300 real respondents per
ODI v2.4.2 Chapter 16 before drafting a value prop.
```
