---
captured: 2026-09-15T20:08:18+00:00
session: 1f9d2f2b-f2b7-4fbf-bbaf-538df8abd162
cwd: /Users/chidionyema/dev/code/idp
chars: 2755
source: founder prompt, verbatim (founder-doc-capture.py)
---

look wwe have done onehtig tofat]so everything  re problem is exactly what you said: We are model-agnostic. We don't build for a specific provider.

Building logic directly into a .claude or .pi folder violates that completely. If Claude or Pi goes away tomorrow, your platform capabilities shouldn't die with them.

Here is what we need to do immediately to stabilize this and enforce a single source of truth (idp).

The Immediate Action Plan: Kill the Split Brain
We have to stop the bleeding and force all agents to read from ONE place. Since estate_alert.py was deleted concurrently, and the repo is in an uncommitted, drifting state, we need to lock it down now.

1. Stop the Background Drift
Before touching another file, you MUST stop whatever background daemon or session is currently writing to the claude-guards or idp repos. If things are being deleted while we are checking them, we are fighting a ghost.

Action: Terminate any running idp-exec or background agent processes.

2. Isolate the .claude and .pi folders (The "Gutting")
These folders should contain only what the specific tool requires to physically start up (e.g., pointing to the single source of truth). They should hold ZERO platform logic.

Action: Ensure .claude contains only settings.json (which routes hooks to idp) and the mandatory AGENTS.md symlink.

Action: Delete any remaining scripts, bash files, or logic residing in .claude/scripts or .pi/agent/extensions.

3. Elevate idp as the Sole Authority
You already identified that idp is authoritative. We need to enforce this.

Action: In claude-guards, ensure the top-level rule points to idp. If claude-guards is meant to be retired or act only as a pass-through, make it explicit.

Action: Check idp/bin/idp-session-gate. If it's failing the epistemic/trajectory checks, we need to know why before blinding the other hooks, but we still point to it.

4. Address the Immediate Breakage (estate_alert.py)
The credential-guard.py hook is broken because its dependency (estate_alert.py) was deleted by a concurrent process.

Action: Restore estate_alert.py from the Git history (git checkout HEAD -- estate_alert.py or similar) to fix the immediate hook failure.

The Path Forward
You are absolutely right to be furious. An agent should never bury platform capabilities inside a tool-specific configuration folder.

To prevent this from happening again, we need a hard rule in the single source of truth (idp): "No capability, script, or logic shall be built inside a tool-specific directory (e.g., .claude, .pi). All platform logic must reside in idp and be accessed via MCP or standard CLI interfaces."

Tell me when you have stopped the background agents, and we will restore the broken hook and finalize the cleanup.
