---
captured: 2026-09-15T15:15:15+00:00
session: 35ebccc3-61ab-4efb-9623-22d844f21e75
cwd: /Users/chidionyema/dev/code/idp
chars: 7332
source: founder prompt, verbatim (founder-doc-capture.py)
---

o k i gave u nay sprc, furst was netir and nubrrs, one is ment and Caladan for the frontier.

What the asymmetry actually looks like
Here's the arithmetic at enterprise scale.

Naive: 10,000 PRs/day × 30-min CI × 8 vCPU = 40,000 vCPU-hours/day.

With test impact analysis (TAP): 10% of tests run → 4,000 vCPU-hours/day. 10x.

With remote cache (Bazel + RBE): 80% cache hit → 800 vCPU-hours/day. 50x.

With batch merge queue (Rosie): 10 PRs verified per batch → 80 vCPU-hours/day. 500x.

With speculative execution + warm pools: latency drops from 30 min to 2 min. 15x on the developer's clock.

The 500x isn't from faster runners. It's from not running the job, or running it once for ten changes, or running it before anyone asked.

The minimal tool list (resist explosion)
You asked for exponential asymmetry, not tool explosion. Here's the minimum viable elite stack.

Layer    Tool    Why
Build graph    Bazel or Buck2    Content-addressed, hermetic, RBE-native
Remote cache    Bazel RBE + BuildBuddy/EngFlow    Share builds across all jobs
Remote execution    Bazel RBE    Parallelize actions, not jobs
Test impact    TAP or predictive test selection    Skip tests that can't fail
Merge queue    Rosie-style batching + bisect    10x throughput
Runner pool    K8s + Karpenter + Firecracker    Ephemeral, warm, cheap
Scheduler    Kueue (K8s-native) or Volcano    Batch, priority, preemption
Workflow    Temporal    Durable, resumable, auditable
Contract graph    Your own (from earlier)    Impact analysis, locality, policy
Observability    OTel + VictoriaMetrics    From the previous layer
That's 10 tools. Not 50. Each is load-bearing. Nothing is decorative.

What to refuse: five CI systems, four artifact registries, three scheduler philosophies, two cache strategies. Every tool must speak the same contract graph, the same OTel, the same policy store. Otherwise you've rebuilt the tool explosion.

Bleeding edge research (2024–2026)
Papers
"Firmament: Fast, Centralized Cluster Scheduling at Scale" (OSDI '16, Google)

"Caladan: Mitigating Interference at Microsecond Timescales" (OSDI '20, Google)

"TAP: Test Impact Analysis at Google Scale" (ICSE, Google)

"Predictive Test Selection" (Meta, ICSE '21)

"Rosie: Batch Merge Queues at Google Scale" (Google internal; summarized in SRE Book)

"Landcastle: Merge Queues at Meta" (Meta engineering blog)

"Hermetic Builds at Scale" (Bazel docs, Google)

"DICE: Incremental Computation at Meta" (Buck2 papers)

Projects
Bazel, Buck2, Please, Pants — build graphs

BuildBuddy, EngFlow, NativeLink — RBE as a service (some OSS)

Temporal, Cadence, Argo, Tekton — workflow engines

Kueue, Volcano, Firmament, Caladan — schedulers

Karpenter, Firecracker, Cloud Hypervisor, Kata — runner substrate

Depot, Namespace, Blacksmith — warmed runners (commercial)

Nix, Determinate Systems — content-addressed environments

People
Malte Schwarzkopf (Firmament, Caladan) — now at Brown

John Wilkes (Google cluster scheduling)

The Bazel team at Google

The Buck2 team at Meta

The Uber SubmitQueue team

The EngFlow / BuildBuddy founders

What's genuinely bleeding edge
Predictive test selection with LLMs. Meta's older model is classical ML. The frontier is using an LLM to reason about which tests a change affects. Early papers 2024–2025.

Content-addressed agents. Applying CAS to agent outputs: commit is a content hash, verification is a content hash, DONE is a content hash. The whole pipeline becomes a Merkle DAG.

Formal verification of CI policy. Using TLA+ or Alloy to prove the merge queue can't deadlock or land broken state.

eBPF-based build sandboxing. Sandbox builds at the syscall level without container overhead. This is what makes Nix-style hermeticity cheap.

Zero-copy artifact transfer. io_uring + RDMA for moving build artifacts between runners at line speed.

Distributed CAS with erasure coding. Content-addressed storage with Reed-Solomon across nodes. Cheaper than replication, same durability.

Speculative merge queues with rollback cost modeling. Not just "run it speculatively," but "run it speculatively if expected rollback cost < expected wait cost."

The design, in one diagram
text
                     ┌─────────────────────┐
                     │  Contract Graph     │  ← impact analysis
                     │  (from earlier)     │  ← locality hints
                     └──────────┬──────────┘
                                ▼
   ┌────────────────────────────────────────────────┐
   │  Admission                                     │
   │  - validate, prioritize, policy-check          │
   └──────────┬─────────────────────────────────────┘
              ▼
   ┌────────────────────────────────────────────────┐
   │  Impact Oracle                                 │
   │  - TAP / predictive selection                  │
   │  - prune work graph to must-run nodes          │
   └──────────┬─────────────────────────────────────┘
              ▼
   ┌────────────────────────────────────────────────┐
   │  Batch Merge Queue                             │
   │  - batch, verify, bisect on failure            │
   └──────────┬─────────────────────────────────────┘
              ▼
   ┌────────────────────────────────────────────────┐
   │  Scheduler (Firmament-style)                   │
   │  - place on hottest cache, cheapest pool       │
   │  - preempt lower-priority work                 │
   └──────────┬─────────────────────────────────────┘
              ▼
   ┌────────────────────────────────────────────────┐
   │  Runner Fleet                                  │
   │  - Firecracker microVMs, warm pools            │
   │  - tiered: hot / warm / cold / spot            │
   └──────────┬─────────────────────────────────────┘
              ▼
   ┌────────────────────────────────────────────────┐
   │  Remote Cache (CAS) + RBE                      │
   │  - share everything, execute remotely          │
   └────────────────────────────────────────────────┘
Each layer removes work before the next layer sees it. Runners are the last layer, not the first.

What to do this week
Measure your current curve. Jobs/day, cost/job, cache hit rate, test pass rate, flake rate. You can't improve what you don't measure.

Pick a build graph. Bazel or Buck2. This is a one-way door. Choose deliberately.

Stand up a remote cache. BuildBuddy or EngFlow as a service; or self-hosted Bazel RBE.

Implement TAP. Start with a coarse version: file → owning tests. Refine over time.

Add a batch merge queue. Rosie-style. Even a naive version is a 5–10x throughput win.

Add a runner pool on K8s. Karpenter + Firecracker. Start with warm pools; add hot pools for merge queue.

Add OTel tracing on the scheduler. Every scheduling decision is a span. Every placement decision is a span. Every cache hit/miss is a span.

Delete every other CI tool. One pipeline. One cache. One runner pool. One scheduler. Everything else is drift.

The one-sentence version
Stop adding runners. Add a build graph (Bazel/Buck2), a shared remote cache (RBE), test impact analysis (TAP), and a batch merge queue (Rosie) — those four omissions give 100–1000x more throughput than any runner fleet, and the runners you do run should be ephemeral Firecracker microVMs placed by a Firmament-style scheduler that puts work where the cache already is. nd the third one u nentioed
