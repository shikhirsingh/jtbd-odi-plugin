---
description: I have a business idea, see a market, or am staring at a complex product I don't understand — help me figure out what the customer's underlying functional job actually is. Uses light web research to propose 3–5 candidate jobs at different abstraction levels.
argument-hint: <a product name, competitor URL, market category, or your own idea OR no args for interactive>
---

# /brainstormjob — Discover the underlying job

Invoke the `brainstormjob` skill.

This is what to run when the user is NOT ready for `/definejob` yet — they don't have a draft sentence, just an idea or a product they're trying to understand.

The skill does light web research (WebSearch + WebFetch), proposes 3–5 candidate job statements at different altitudes (narrow / sweet spot / broad), walks the user through picking one, then hands off to `/definejob` to formally lock it.

If the user paste a URL, fetch it. If they mention a product name, search for context. If they have only a problem domain, search for the category and adjacent categories.
