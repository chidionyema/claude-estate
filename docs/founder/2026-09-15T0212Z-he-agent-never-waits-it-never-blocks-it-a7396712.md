---
captured: 2026-09-15T02:12:49+00:00
session: b47fc54c-5658-4c97-865c-a88fcc6b441e
cwd: /Users/chidionyema/dev/code/idp
chars: 4053
source: founder prompt, verbatim (founder-doc-capture.py)
---

he agent never waits. It never blocks. It produces claims in a tight loop, reading its mailbox at each step. When the budget expires, it emits its final state file and exits.

A separate system, watching the contract graph, sees def456: fail: boundary X and spawns a repair task with the failure context. That repair task might resume the same agent — or a fresh one — with the failure as input.

Enterprise rollout
Phase 1 — Remove the verb. Take run_tests out of the agent's toolset. Replace with commit + request_verification. This alone breaks the wait pattern in 80% of cases. The agent will fight it — it'll try to find other ways to wait — so this phase needs observability: log every attempt to block.

Phase 2 — Verification service. Stand up the queue and workers. Start with a single boundary type (HTTP proxy checks, since you already have probes). Results go to the contract graph.

Phase 3 — Mailbox protocol. Give agents the read_mailbox tool. Wire results from the graph to the mailbox. The agent can now see pass/fail without ever calling the verifier.

Phase 4 — Repair loop. Failed verification spawns a task. Start with "same agent, resumed from state file, failure appended." Measure repair latency and success rate.

Phase 5 — Speculative execution. Use the contract graph to decide what's safe to parallelize. Start conservative, loosen as confidence grows.

Phase 6 — Budgets and backpressure. Wall-clock budget per session. Queue-depth-aware rate limiting. This is the last piece because it requires trust in the rest of the system.

Each phase is independently useful. Phase 1 alone is a step change.

What can go wrong
Runaway producers. Agents commit faster than the system verifies. The queue deepens, latency grows, results become stale. Fix: commit budget per session, backpressure from queue depth.

Orphaned failures. Failures are detected but no one repairs them. Fix: repair loop must be a first-class service with SLA and ownership, not an afterthought.

Cold repair contexts. The repair agent doesn't have the context to fix the failure. Fix: every agent session must externalize state at checkpoints. The repair task loads the nearest checkpoint + the failure.

Silent divergence. A claim passes verification but the verification was wrong (or the contract was wrong). Fix: the contract graph is the ground truth. If a passing claim later fails, the contract is what gets audited, not the agent.

Speculation cascades. Task 2 speculates on task 1, task 3 on task 2, task 1 fails. Fix: speculative depth is bounded (e.g., 2 levels). The graph tells you which chains are safe.

What this changes structurally
The agent is no longer a "worker who does everything." It's a claim producer. Verification is a separate system. Repair is a separate system. Scheduling is a separate system. The contract graph is the scoreboard all three read from.

The agent's value is now purely in producing high-quality claims quickly. Its cost is bounded by the commit budget and wall-clock. Its failure mode is a claim that fails verification, which triggers a bounded repair cycle, not an infinite loop.

This is the same separation that made modern CPUs fast: cognition (branch prediction, OoO) is decoupled from computation (ALU), and the scoreboard handles the reconciliation. The agent is the front-end. Verification is the back-end. The graph is the reorder buffer.

The one-sentence version
Take the run_tests verb out of the agent's hands, make it produce unverified claims, run verification as a background service against the contract graph, spawn repairs on failure instead of blocking, and use the graph as the dependency oracle for speculative execution.

The wait disappears because the ability to wait disappears. The agent produces as fast as it can think. The system verifies as fast as it can compute. The graph reconciles. That's the enterprise design.

even runnong ci etc a lot of tine gets wated oull requests failues retrying, failed builds, red prs pilig up, wlite geniuls solve in additona salso for eterprise
