---
description: ORCHESTRATOR — A complete ODI engagement that REPLACES interviews with thorough online research, then fields a REAL n=300-600 survey on the mined outcomes. Output is DECISION-GRADE (because the survey is real) and shaves 2-3 weeks off the timeline by skipping interview recruiting.
argument-hint: "\"<locked job statement>\" [--sources reddit,amazon,quora,appstore,...]"
---

# /researchpath — Skip interviews, keep rigor

Invoke the `researchpath` skill.

This is for users who:
- Can't recruit 20+ interviewees (timeline / target audience won't reply / etc.)
- Have an active online community discussing the category (B2C, prosumer, developer tools)
- Have budget + timeline for a real n=300-600 survey

This is NOT for:
- Enterprise / regulated industries (interviews are essential)
- B2B with no public discussion of the category
- Cases where the user wants to skip both interviews AND the survey (that's `/run-synthetic-survey`)

The orchestrator:
1. Runs Phase 0 eligibility checks; reroutes if mining won't work for this category
2. Does a HEAVY mining pass (5x normal quotas) instead of interviews
3. Nets and validates the candidates exactly like the full path
4. PAUSES for the user to field a real n=300-600 survey
5. Runs all decision-grade downstream analysis
6. Stamps `data_provenance: mixed_research_real_survey` on every artifact

For B2B engagements, explicitly recommends 5-8 buyer interviews alongside the mining (because buyers don't post publicly).
