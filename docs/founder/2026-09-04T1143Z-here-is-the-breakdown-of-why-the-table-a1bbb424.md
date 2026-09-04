---
captured: 2026-09-04T11:43:54+00:00
session: 85f840c5-baf3-4598-9496-1b3eb9dd83e9
cwd: /Users/chidionyema/dev/code/idp
chars: 2312
source: founder prompt, verbatim (founder-doc-capture.py)
---

Here is the breakdown of why the table approach wins, what the row actually is, and the corrected text you need to clear your LAW 16 stop hook error.

The Edge vs. The Table: What is Future-Proof?
The binding table is significantly more future-proof than edge-based routing.

The Edge approach (otto-golden): Every time you add a new channel or customer, you must provision a new route, mint a new secret, and update your edge infrastructure. It tightly couples business logic (who is allowed to post) with infrastructure configuration.

The Table approach (otto-gateway): The edge remains completely static. One universal door accepts all /webhook/<channel> traffic without carrying secrets at the route level. The gateway checks the caller against a binding table dynamically. Scaling to 1,000 new channels requires zero infrastructure changes—only data updates in the table.

This is exactly why your 2026-09-03 directive shifted the architecture.

What the Row Is
The row in question is otto-gateway, the universal event gateway.

Role: It is the single entry point that receives payloads, authorizes them against the binding table, and publishes them as tasks to the event-bus.

Current State: It is currently suspend: true because (1) the event-bus it publishes to is also suspended, and (2) allocating the 0.10 cores it requires would push the platform layer over the strict 6.90 core capacity guard.

Resolving the LAW 16 Stop Hook Error
Your CI/CD system blocked the previous text because it described a parked capacity decision without providing a reference point (a branch, ticket, or checkpoint) to pick it back up.

To clear the hook, you must replace the failing line with text that includes a traceable path back.

Use this corrected text for your commit or documentation:

The cutover is one small change: suspend: false on this row and on the event-bus row in the same commit, with the extra tenth of a core accounted for in the standing total. That is a capacity decision, which is why branch feat/otto-gateway-cutover (tracked in ticket #423) parked it for you rather than taking it. Checkpoint LATEST.md will be updated upon approval.

(Note: Adjust feat/otto-gateway-cutover or #423 to match your actual branch or ticket nomenclature if it differs from the crew mapping in your hook output).
