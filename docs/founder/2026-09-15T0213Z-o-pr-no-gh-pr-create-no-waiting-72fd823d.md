---
captured: 2026-09-15T02:13:29+00:00
session: b47fc54c-5658-4c97-865c-a88fcc6b441e
cwd: /Users/chidionyema/dev/code/idp
chars: 4919
source: founder prompt, verbatim (founder-doc-capture.py)
---

o PR. No gh pr create. No waiting for CI. No "what's the status of my PR?"

The system around the agent:
Verification service watches shadow branches, runs tiered checks (fast → slow), classifies failures, writes results to mailbox and graph.

Promotion service promotes verified shadow commits to main via the merge queue.

Merge queue batches, bisects, lands.

Revert service detects broken main within minutes, auto-reverts, notifies repair loop.

Repair loop spawns a new task on the failed commit — with the failure context — from the externalized state file.

The human's job:
Review verified commits as documentation, not as a gate.

Own the contract graph for their boundaries.

Handle edge cases the classification can't.

Never wait for CI, never retry a flake, never bisect a batch manually.

What the enterprise looks like
Tiered verification
Every commit gets tier-0 (seconds), tier-1 (minutes), tier-2 (tens of minutes), tier-3 (hours, nightly).

Tier 0: lint, type-check, contract conformance for touched boundaries.

Tier 1: unit + contract tests for touched boundaries.

Tier 2: integration tests across boundaries in the graph neighborhood.

Tier 3: full system + soak tests.

The agent's commits only run tier 0 and 1 before promotion. Tier 2 and 3 run continuously against main. Failures in tier 2/3 spawn repair tasks or revert.

This is how big systems handle throughput: the fast path is fast, the slow path is continuous.

The contract graph is the scheduling oracle
Every decision above uses it:

Test impact analysis: which tests to run.

Speculative execution: which commits are safe to parallelize.

Blast radius: what to revert when something breaks.

Merge queue ordering: which commits can batch together.

Verification scope: which boundaries to verify for a given commit.

Without the graph, every layer reverts to "run everything, wait for everything." With it, every layer runs only what matters.

Auto-revert as policy
The single most important cultural and technical shift: revert first, investigate later.

Main breaks → auto-revert within minutes.

Revert is fast because the contract graph knows what to remove.

Investigation happens in a repair task, not on broken main.

No "don't merge, main is red" freezes.

This is Google's model. It's the reason main stays green even with thousands of commits per day.

For agents, this is non-negotiable. Agents don't have the judgment to be careful. The system has to be.

No PR pileup, because PRs don't gate
PRs become records of verified changes, not gates. The number of open PRs is a function of how many are being reviewed for documentation, not how many are waiting for CI or approval.

Rollout, in the right order
Phase 1 — Shadow branches. Agent commits to shadow/<agent>/<task>. Verification service watches. No PRs.

Phase 2 — Failure classification. Implement the classifier. Retries become one action among five. Instrument everything.

Phase 3 — Test impact analysis. Use the contract graph. Start with one boundary type. Measure reduction.

Phase 4 — Continuous merge with auto-revert. Trunk accepts verified commits. Reverts are automated. Main is never red for more than minutes.

Phase 5 — Merge queue with batching. Batch verified commits. Bisect on failure.

Phase 6 — Feature flags and trunk-based development. Land incomplete work behind flags. Kill long-lived PRs entirely.

Phase 7 — Tiered verification. Fast path, continuous slow path. Optimize for the agent's wall-clock.

Each phase is independently valuable. Each one removes a category of waste. Together they eliminate the PR backlog, the retry storm, the failed build pile, and the human bottleneck.

The pattern, named
Every layer of the pipeline has the same disease: a synchronous gate designed for humans, applied to a producer that doesn't need it.

Layer 1 (agent): run_tests gate → removed. Agent produces claims.

Layer 2 (pipeline): PR gate → remove. Agent produces commits to shadow.

Layer 3 (trunk): merge gate → remove. Continuous merge with auto-revert.

Layer 4 (review): human approval gate → remove. Review as documentation.

Layer 5 (release): deploy gate → remove. Feature flags.

At every layer, the fix is the same: decouple production from verification, make verification continuous and asynchronous, and let the contract graph decide what's safe to skip.

This is what elite enterprises do. It's not research. It's operations.

The one-sentence version
The PR is a synchronous gate for humans; agents don't need it — remove it, replace it with shadow commits, continuous verification, auto-revert, test impact analysis via the contract graph, and a batched merge queue, so the only thing in the critical path is the agent's own thinking.

The retry storm, the red PR pile, and the failed build waste are all symptoms of the same disease: verification coupled to production. Decouple them, and every one of those wastes disappears.
