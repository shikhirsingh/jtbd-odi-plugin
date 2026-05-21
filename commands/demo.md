---
description: Show what the plugin actually produces. Walks through a worked example (Bosch CS20 or "listen to music") and shows realistic outputs for every artifact — without running a real engagement. The "see before you commit" command.
argument-hint: "[saw|music|both] (default: ask the user)"
---

# /demo — See the outputs before committing

Invoke the `demo` skill. Walk the user through the 10 artifacts of a worked example (default: ask "Bosch CS20 — the canonical handbook case, OR listen-to-music — a familiar B2C example?"). Each artifact is stamped clearly as a DEMO so it's never mistaken for real engagement output.

End the demo with three clear "what to do next" options:
1. `/odihelp` — figure out which path fits the user's situation
2. `/preflight` — check if ODI is even the right tool
3. `/runfullodi --mode rehearsal` — try the synthetic pipeline on their own job
