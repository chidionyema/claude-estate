---
captured: 2026-09-15T02:13:09+00:00
session: b47fc54c-5658-4c97-865c-a88fcc6b441e
cwd: /Users/chidionyema/dev/code/idp
chars: 11477
source: founder prompt, verbatim (founder-doc-capture.py)
---

The Waste Isn't CI. It's the PR Gate.
You've found the next layer of the same disease. Earlier we removed run_tests from the agent. Now we have to remove the merge gate from the pipeline.

The PR is a synchronous human-review artifact. It was designed when the producer was a human who needed a peer to look at their diff before it landed. Agents don't need peer review. They need verification. The PR conflates the two, and the conflation is where all the waste lives.

Red PRs pile up because verification is expensive and happens after the PR is opened.

Retries happen because failures aren't classified as flaky vs real.

Failed builds waste compute because the same build runs against every PR from scratch.

Merge is slow because every merge is a fresh full-CI run.

Humans become the bottleneck because they're the only ones who can approve.

Every one of these is caused by the gate. Elite systems removed the gate a decade ago for automated producers. We just have to apply the same lessons to agents.

The diagnosis, precisely
Waste 1: Verification-after-PR
The PR is opened. CI runs. It's red. The agent (or human) fixes. CI runs again. Red again. Three days pass. The PR rots. Meanwhile main has moved, so a rebase triggers full CI again.

Every retry is a full re-verification of a state that was already partly verified. The system has no memory of what was verified, only that a run happened.

Waste 2: No failure classification
A red build could mean:

Real bug in the change.

Flaky test.

Infra hiccup.

Race with a concurrent change.

Stale dependency.

Insufficient compute / timeout.

The system treats all six the same: retry. Retrying wastes compute, wastes time, and — worst — trains humans to ignore red. "It's flaky, just retry." Now real failures slip through because the signal has been diluted.

Waste 3: Per-PR full builds
Every PR runs the whole test suite. Two PRs touching disjoint modules still run each other's tests. The system can't tell which tests are affected because it doesn't have a contract graph to consult.

Waste 4: Synchronous merge
Merges are serialized. Each merge runs CI on the merged state. If merge N fails, merges N+1, N+2... all re-run. A single flake can cascade across the queue.

Waste 5: Human review as a required step
Even when CI is green, a human must approve. The human is slow. The queue backs up. The agent finishes its work and then waits — same disease as run_tests, one layer up.

Waste 6: No auto-revert
If a merge breaks main, the team investigates. Main stays broken for hours. Everything built on top of the break is contaminated. The break propagates.

Every one of these has a solved answer. None of them require new research.

The elite design
Six moves. Each is deployed at Google, Meta, or both, at scale, for over a decade.

Move 1: Remove the PR from the agent's path
The agent doesn't open PRs. The agent commits to a shadow branch. The verification service watches shadow branches continuously. Only verified states get promoted.

The PR — if it exists at all — is an artifact of a verified change, opened automatically at the end for humans to inspect. It is not a gate. It is a record.

This is what Google's internal system does: changes flow through a review system (Critique), but the review is decoupled from the build/verify pipeline. The agent's equivalent: commits are the unit of production; review is the unit of documentation.

Move 2: Continuous merge with auto-revert
The trunk (main) accepts commits continuously. Every commit is verified after landing. If a commit breaks the trunk, it is auto-reverted within minutes, before anything downstream depends on it.

This is Google's model. It sounds insane to teams used to PR gates. It works because:

Compute is cheap relative to human time.

Reverts are fast and automated.

The contract graph knows what depends on what.

The blast radius of a bad commit is bounded to minutes.

For agents, this is the natural fit. The agent produces commits at machine speed. The system reverts bad ones at machine speed. Humans are not in the critical path.

Move 3: Flake classification and quarantine
Every failure is classified automatically:

Class    Signal    Action
Real    Reproduces on retry, deterministic    Block, spawn repair
Flaky    Passes on retry, non-deterministic    Quarantine, notify owner
Infra    Specific error signature (network, timeout)    Retry with backoff
Contention    Different failure each run    Serialize with conflicting commits
Stale    Depends on outdated base    Rebase, re-verify only deltas
Once classified, retries are not the default. Retries are one action among five, chosen by classification.

This is Google's Flaky Test Handler and Meta's flake detection. It exists. It's deployable. The point is: don't retry blindly. Classify, then act.

Move 4: Test impact analysis
Only run tests affected by the change. This requires the contract graph — the same graph from the earlier discussion.

text
Commit touches boundary X
  → graph says boundaries A, B, C depend on X
  → run tests for X, A, B, C
  → skip everything else
Google's TAP does this at massive scale. The reduction is typically 80–95% of test executions. This is the single biggest compute win.

Without the contract graph, you can't do this. This is where the graph pays off at the CI layer.

Move 5: Merge queue with batching and bisection
Instead of merging PRs one at a time:

Batch: Take N verified commits, merge them together, verify the batch.

If batch passes: land all N at once.

If batch fails: bisect. Narrow to the failing commit in log₂(N) re-verifications.

If bisection is inconclusive: fall back to per-commit verification.

This is Meta's Landcastle and Google's Rosie. It transforms merge from "one at a time, full CI each" to "batch, bisect, land." Throughput scales with batch size.

Move 6: Trunk-based development with feature flags
Never block on incomplete work. Hide it behind a feature flag. Land incomplete code to main continuously. Flip the flag when the feature is ready.

This eliminates the long-lived PR entirely. The agent lands small commits continuously. The flag is the release gate, not the PR.

This is the standard at Google, Meta, Netflix, Amazon. It's the reason "PRs pile up" doesn't happen there — PRs are minutes-long, not days-long.

What changes for agents
Applied to an agent-first pipeline:

The agent's loop becomes:
text
1. produce commit (claim)
2. push to shadow branch
3. read mailbox (non-blocking)
4. produce next commit
5. read mailbox (non-blocking)
...
No PR. No gh pr create. No waiting for CI. No "what's the status of my PR?"

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
