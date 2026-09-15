---
captured: 2026-09-15T02:12:25+00:00
session: b47fc54c-5658-4c97-865c-a88fcc6b441e
cwd: /Users/chidionyema/dev/code/idp
chars: 5526
source: founder prompt, verbatim (founder-doc-capture.py)
---

he Insight Is Correct. Here's the Elite Design.
You've identified the central inefficiency of every current agent harness: the most expensive resource in the system is synchronized with the slowest mechanical process.

An agent turn costs tokens, latency, and — critically — reasoning continuity. A test suite costs CPU. Currently they're locked together. The agent dispatches a test, blocks, waits, comes back with a cold context, resumes. Every wait is pure waste: the agent can't do anything useful, and the context it returns to is worse than the one it left.

Elite design doesn't make the wait shorter. It removes the wait entirely.

The principle
Agents produce claims. The system verifies them. The agent never blocks on verification.

This is the same shift as synchronous HTTP handlers → event-driven actors. The handler blocks on every I/O; the actor drains a mailbox. For LLMs the cost asymmetry is far worse: a 5-minute test suite burns a whole turn's worth of context and breaks the reasoning chain.

The agent's job is to emit proposed state. Verification is a separate service with its own SLA. The agent's turn ends when it has produced a commit — not when the commit passes.

The four moves
1. Remove the verb
Not "make it async." Remove the tool.

If run_tests() exists in the agent's toolset, the agent will call it and block. The strongest move is to delete it. The agent gets:

commit(branch, message) — produce a claim

request_verification(commit, boundaries[]) — fire and forget

read_mailbox() — non-blocking read of results

propose(state) — emit proposed next state

No run_tests. No wait_for_ci. No check_build. The agent literally cannot wait, because the tool to wait doesn't exist. If it wants verification results, it reads the mailbox — which is always instant and always non-blocking.

This is the "make the wrong thing impossible" principle. Don't add a rule that says "don't block on tests." Remove the ability to block.

2. Agent produces claims, not verified state
A commit is a claim: "I believe this state satisfies the contract."

The commit is not verified. It is not merged. It is not deployed. It's a proposal that enters the verification queue. The agent's job ends when the claim is emitted.

This reframes "done." Done ≠ tests pass. Done = commit emitted with a verification request attached. The agent's turn is complete when the claim exists, not when the claim is confirmed.

3. Verification is a service, not a tool call
Verification runs on its own infrastructure, at its own pace, on its own priorities:

Parallel workers. N machines, each capable of running any boundary's verification.

Queue with priorities. User-facing branches prioritized over background ones.

Contract-graph-driven. The verification spec for each commit comes from the contract graph — the same graph from the earlier discussion. This is where it pays off.

Results are durable. Every result is stored, queryable, timestamped.

Feedback is push, not pull. The agent doesn't ask "did it pass?" Results are delivered to a mailbox, or the graph, or a webhook.

This is closer to an SRE system than to CI. CI gates individual merges. This is a continuous verification fabric that produces a stream of pass/fail facts about the current state of every branch.

4. Failures spawn repair, not retries
The crux. If the agent doesn't wait, what happens when verification fails?

The wrong answer: retry the same agent. It has moved on; its context has shifted; it will re-derive the same failure.

The right answer: a failed verification is a new task with the failure as context. It gets routed to:

The same agent, resumed from its externalized state file (from the earlier discussion), now with the failure appended.

Or a fresh agent, with a compact context: the contract, the failure, the diff, the state file.

The repair loop is a first-class part of the system. It is not the agent's job to loop on tests. It is the system's job to route failures.

The speculation problem (and how the contract graph solves it)
If the agent commits task 1, moves to task 2, and task 1 fails verification, task 2 is built on a broken foundation. This is the classic speculative-execution hazard.

Two designs:

Conservative: task 2 cannot start until task 1's verification completes. Safe, but reintroduces the wait.

Speculative: task 2 starts immediately. If task 1 fails, task 2 is rolled back and re-issued.

Real systems use a hybrid, and the contract graph is the dependency oracle:

If task 2 touches boundaries that task 1 touched → serialize. Wait for verification.

If task 2 touches disjoint boundaries → speculate. Run in parallel. Rollback both if task 1 fails.

This is out-of-order execution with a reorder buffer. The contract graph is the scoreboard. Boundaries are registers. Commits are instructions. Failures are branch mispredicts.

Without the contract graph, you can't know what's safe to speculate on, and you're stuck with serialization. The graph is what unlocks parallelism.

Budgets and backpressure
Every agent session gets:

A wall-clock budget. Not tokens. Time. When it expires, whatever commits exist are the output.

A commit budget. N claims per session. After N, the agent stops and the system verifies.

A verification backlog signal. If the queue is deep, the agent's budget shrinks. If the queue is shallow, the agent can speculate more.

This is backpressure. The agent's rate of claim production is regulated by the system's rate of verification. No runaway. No queue blowup.
