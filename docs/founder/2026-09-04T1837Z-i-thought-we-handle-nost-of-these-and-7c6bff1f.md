---
captured: 2026-09-04T18:37:31+00:00
session: 85f840c5-baf3-4598-9496-1b3eb9dd83e9
cwd: /Users/chidionyema/dev/code/idp
chars: 3190
source: founder prompt, verbatim (founder-doc-capture.py)
---

i thought we handle nost of these and built in all the capabilities over the past 7 days This is a severe architectural failure for an infrastructure agent. Staging a high-risk network cutover (Flannel to Calico) with an auto-activation timer, only to lose session state and ask "What should I do?" when you reply "Go", combines multiple critical anti-patterns.

Root Causes of the Breakdown

Conversational Ephemeral State Instead of Durable State: The staged action lived solely in the LLM's conversation context window rather than an external, durable state machine (e.g., PostgreSQL, Redis, or an etcd key). When the state was wiped, the agent treated your message as an isolated prompt.
Context Amnesia Across Model Failovers: The gateway switched from kimi via custom to minimax via custom right before you sent "Go". During this failover (likely triggered by an API timeout or crash), the session context was completely dropped or not serialized to the fallback provider.
Underlying Gateway Crash Loops: The logs show recurring pod restarts (Crash Info.txt, Previous Container.txt, and rolling pod hashes for otto-gateway). If the pod restarted between the staged prompt and your reply, any in-memory state vanished.
Relying on LLM Inference for Deterministic Confirmation: Approving a production cutover should never depend on whether an LLM understands the conversational context of "Go". It requires a deterministic confirmation flow.
Catastrophic Failure Mode on Timers: The prompt stated: "Auto-activating in 60 minutes." If the agent forgets the context but a background timer or cron job still fires without health checks, it risks executing a half-configured network migration while blind to cluster state.
Critical Architecture Fixes

1. Decouple Approvals from LLM Reasoning

Replace free-text "Go" replies with deterministic Telegram Inline Keyboard Buttons containing a signed callback payload: action:cutover_calico|id:<uuid>|expires:<timestamp>.
The Telegram webhook should route this callback directly to an execution worker, completely bypassing the LLM.
2. Implement a Persistent State Machine

Every staged operation must generate an immutable, persistent record in a database:
Action ID
Staged Command / Flux Patch
Status (pending_approval, executed, cancelled, timed_out)
Pre-flight Cluster Hash
If the agent pod crashes or changes models, it can query the persistent record by ID rather than relying on prompt history.
3. Invert the Safety Default (Fail-Closed)

Never use auto-activation on destructive infrastructure mutations.
If no human confirmation is received, or if the session state corrupts, the default action must always be ABORT and alert, never auto-apply.
4. Isolate Chat Context from System Notification Streams

In the chat, system crash dumps (HIGH - Failed to pull image, Previous Container.txt) and human command-and-control share the same channel. This pollutes the model's token window with noisy telemetry, accelerating context degradation and token limit truncation.
Is your staging backend currently tracked via an external queue/orchestrator (like Temporal or Celery), or is the entire lifecycle managed inside the bot's runtime memory?
