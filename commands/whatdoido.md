---
description: "Reverse lookup: tell me what you have (files, partial outputs, current state) and I'll tell you exactly which command to run next. The 'I'm stuck, where am I?' navigator."
argument-hint: <description of what you have OR no args for interactive prompts>
---

Invoke the `whatdoido` skill. This is the reverse of `/odihelp` — instead of asking "what do you want?", it asks "what do you have?" and routes accordingly.

If the user pasted a filename or described a file, look at the file (or ask for a sample) to detect which phase they're in. Always output the EXACT next command with the file path filled in.
