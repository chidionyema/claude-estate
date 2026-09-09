---
captured: 2026-09-09T03:21:02+00:00
session: e33563df-56c3-4b85-93c3-5a89cd6d949b
cwd: /Users/chidionyema/dev/code/idp
chars: 2283
source: founder prompt, verbatim (founder-doc-capture.py)
---

as you know the estate wants to get rid of claude code due to poor perfornance, the fonder has a soft spot for claude code ad would raher avod this but only on the condition that claude odes cost is slahed dratically s we nove off this harness Yes, this is true.

The post describes a real engineering solution published by Dimitri Mazmanov (a Principal Product Manager at Spotify) detailing how a custom Claude Code plugin called Shunt reduced token usage by roughly 90% on bulk file reads.

How It Works

Coding agents like Claude Code often burn massive amounts of expensive tokens simply doing heavy Input/Output (I/O) workâ€”such as reading multiple large source files into the context window just to answer a basic question. Spotifyâ€™s solution uses a three-layer routing approach:

The Hooks: A PreToolUse hook intercepts Claude's file-reading tools and automatically blocks/redirects any standard file reads that exceed a specific size threshold (e.g., over 350 lines).
The Worker Model: Instead of letting the expensive frontier model (Claude) digest thousands of lines of raw code, the plugin routes the files to a cheaper, faster worker modelâ€”specifically Google Gemini 2.5 Flash running via Spotify Portal's AiKA Modes.
The Summary: The worker model compresses the files into concise, structured bullet points and answers, which are then passed back to Claude. Claude keeps the core reasoning, editing, and debugging tasks, but avoids the costly overhead of raw data ingestion.
Important Caveats to Keep in Mind

While the 90% reduction figure is real based on Spotify's internal testing across specific Java monorepo scenarios, it comes with practical limitations:

Not for debugging or architecture: Cheaper worker models are used strictly for bulk-reading and predictable boilerplate generation; they lack the deep context needed for complex reasoning or tracking subtle bugs.
Ecosystem requirement: To use the exact setup shown in the screenshot, you need access to Portal by Spotify and its associated CLI/plugin infrastructure (though the architectural pattern of using hooks to route traffic to a cheaper model can be replicated independently).
Are you looking to implement a similar token-routing strategy for your own AI coding workflows?


 what do you htibk
