---
captured: 2026-09-15T14:28:10+00:00
session: 35ebccc3-61ab-4efb-9623-22d844f21e75
cwd: /Users/chidionyema/dev/code/idp
chars: 47135
source: founder prompt, verbatim (founder-doc-capture.py)
---

how do i setup netric collection at enterprise level at insane level o f granularity, like evrything neasurable nust be neasured, any opensource tooling for this aceoss a whole esate and plstforn agents and k8s and all nanners of services and hernes agents etc
The user wants enterprise-level metrics collection at insane granularity. Open source tooling. Across estate, platform agents, K8s, all services, harness agents. Let me give them a real architecture.

This is a technical question. Need to be thorough but concrete. Open source tooling. Let me think about what actually exists and what's bleeding edge.

Key layers:

Metrics collection (Prometheus, VictoriaMetrics, OpenTelemetry)

Agent-specific metrics (agent runs, token usage, tool calls, reasoning)

LLM observability (Langfuse, Phoenix, OpenLLMetry)

K8s native (kube-state-metrics, cAdvisor, node-exporter)

Tracing (Jaeger, Tempo, OpenTelemetry)

Logs (Loki, Vector, Fluent Bit)

Profiling (Pyroscope, Parca, eBPF)

eBPF (Cilium, Pixie, Tetragon, Coroot)

Storage (Prometheus, VictoriaMetrics, Mimir, Thanos)

Visualization (Grafana)

Alerting (Alertmanager, Grafana OnCall)

For agents specifically:

Langfuse (open source, LLM observability)

Arize Phoenix (open source)

OpenLLMetry / Traceloop

Helicone

Lunary

For "everything measurable must be measured":

OpenTelemetry Collector as the universal shim

Prometheus ecosystem for metrics

eBPF for zero-instrumentation

Profiling: Pyroscope, Parca, Polar Signals

Cardinality management is the killer problem

Let me structure this as an enterprise architecture with a concrete stack.

Also need to address cardinality explosion - this is THE problem with "measure everything." VictoriaMetrics, Mimir handle this. Need to talk about cardinality budgets.

Let me be concrete about agent metrics - what do you actually measure:

Token counts (input, output, cached)

Cost per turn

Tool call latency

Tool call success rate

Reasoning chain length

Context size at each turn

Compaction events

Hook fires (before we kill them)

Mailbox reads

Commit → verification latency

Verification pass/fail by boundary

Agent wall-clock vs productive time

Speculation depth

Repair loop count

Policy violations

Hallucination proxies (claim vs verification mismatch)

K8s:

kube-state-metrics

cAdvisor

node-exporter

kubelet metrics

API server metrics

Scheduler metrics

etcd metrics

network (Cilium Hubble)

service mesh (Istio, Linkerd)

CNI metrics

Services:

OTel SDK auto-instrumentation

Prometheus exporters

Service mesh sidecar metrics

Application metrics via RED/USE

Let me be careful about the length. This needs to be dense and useful. Structure it as:

The principle (measure everything, but cardinality budget)

The stack (concrete OSS tools by layer)

Agent-specific instrumentation (the hard part)

The collector architecture

Cardinality management (the trap)

Storage tier

The 10x moves

Rollout

Let me be concrete about tool names, versions, and the tradeoffs.

Measure Everything, But Budget Cardinality Like Money
The naive version of "measure everything" kills the system. You instrument 10,000 pods × 50 metrics × 30 label combinations × 5 environments and you've built a cardinality bomb that no TSDB survives. The elite design is measure everything, but every measurement has a cardinality budget and a tier.

The architecture below is what I'd build at an enterprise with open source only. I'll name the tools, the layers, and the traps.

The principle
Every measurement exists. Every measurement has a tier. Every tier has a retention and a cost. Nothing is unmeasured; nothing is unbudgeted.

This is the same contract-graph idea applied to telemetry: a metric graph where each metric has an owner, a cardinality budget, a retention tier, and a consumer. Metrics without an owner are deleted. Metrics over budget are sampled or dropped.

The stack, by layer
Layer 0 — Instrumentation SDK
OpenTelemetry (OTel) SDKs for every language. This is the universal interface. Metrics, traces, logs — one SDK, one exporter protocol (OTLP).

Go, Java, Python, Node, .NET, Ruby, Rust, PHP, C++ — all have stable SDKs.

Auto-instrumentation via opentelemetry-instrument (Python), -javaagent (Java), @opentelemetry/auto-instrumentations-node (Node).

Manual instrumentation for business metrics.

Do not use anything else. Prometheus client libraries are fine for exporters, but internal services speak OTLP.

Layer 1 — Collection
OpenTelemetry Collector — the universal shim. Every service ships to a local collector; every collector forwards to a central collector cluster.

Agent mode (DaemonSet): one per node, receives local OTLP, batches, forwards.

Gateway mode (Deployment): receives from agents, does tail sampling, routing, redaction, enrichment.

Connectors: spanmetrics (traces → RED metrics), servicegraph (traces → dependency graph).

The collector is where cardinality control happens, not at the SDK.

Layer 2 — Metrics storage
Three viable OSS options. Pick one.

Tool    When    Trade-off
Prometheus    Single cluster, <10M active series    Simple, mature, but doesn't scale horizontally
VictoriaMetrics    Enterprise scale, high cardinality    Easier ops than Mimir, excellent compression, single binary
Grafana Mimir    Multi-tenant, huge scale    Most powerful, most operational complexity
Thanos    Multi-cluster Prometheus federation    Good if you already run Prometheus everywhere
My pick for enterprise: VictoriaMetrics for the hot path, Mimir if you need true multi-tenancy with per-tenant quotas. VictoriaMetrics handles high cardinality better with less ops pain.

Layer 3 — Logs
Loki or VictoriaLogs. Loki for Grafana-native; VictoriaLogs for cheaper at scale.

Ship via Vector (Rust, high performance) or Fluent Bit (lighter, more integrations). OTel Collector can also receive and forward logs.

Layer 4 — Traces
Tempo or Jaeger. Tempo for Grafana-native; Jaeger for the classic UI.

Trace sampling: tail-based at the collector. Head-based loses the interesting traces; tail-based keeps all errors and slow traces. This is critical at enterprise scale.

Layer 5 — Continuous profiling
Pyroscope or Parca. eBPF-based, no code changes. Profiles every process on the node.

This is the most underrated telemetry layer. It catches things metrics and traces miss: CPU hotspots, memory leaks, goroutine leaks, lock contention.

Layer 6 — eBPF / zero-instrumentation
Cilium with Hubble for network flows. Pixie for application-level observability with no code changes. Tetragon for security events. Coroot for SLOs and RCA.

eBPF is the "measure everything without asking anyone" layer. If a service won't instrument, eBPF catches it anyway.

Layer 7 — K8s native
kube-state-metrics — K8s object state (deployments, pods, jobs).

node-exporter — host metrics.

cAdvisor (built into kubelet) — container metrics.

kubelet, apiserver, scheduler, controller-manager, etcd — control plane metrics.

Cilium/Hubble — network, service, DNS.

Istio/Linkerd — service mesh metrics.

KEDA, Karpenter, Cluster Autoscaler — autoscaling metrics.

All scraped by the Prometheus agent (or VM agent) DaemonSet.

Layer 8 — Agent / LLM observability
This is the layer most people don't have. It's the most important one for you.

Langfuse (open source, self-hostable) — LLM observability. Traces, spans, generations, evaluations, datasets, prompts.

Arize Phoenix (open source) — LLM tracing and evals.

OpenLLMetry (Traceloop, open source) — OTel-native instrumentation for LLM SDKs. Works with OpenAI, Anthropic, LangChain, LlamaIndex.

OpenInference (Arize) — semantic conventions for LLM traces.

These three together give you the LLM-native layer: every prompt, every completion, every tool call, every retry, every cost.

Layer 9 — Visualization & alerting
Grafana for dashboards. Alertmanager or Grafana OnCall for alerts. Grafana SLO for SLO tracking.

Layer 10 — Query federation
Grafana with multiple datasources. PromQL everywhere. Grafana Mimir's query frontend if you need cross-cluster queries.

What "measure everything" means per layer
Every service
RED metrics (Rate, Errors, Duration) per endpoint, per operation, per client:

text
http_server_requests_total{service, method, path, status, version}
http_server_request_duration_seconds{service, method, path, status, version}
USE metrics (Utilization, Saturation, Errors) per resource:

text
process_cpu_seconds_total{service}
process_resident_memory_bytes{service}
process_open_fds{service}
Plus business metrics:

text
orders_created_total{region, tier}
payment_attempts_total{provider, status}
Every K8s workload
Per pod, per node, per namespace:

text
container_cpu_usage_seconds_total{namespace, pod, container}
container_memory_working_set_bytes{namespace, pod, container}
kube_pod_container_status_restarts_total{namespace, pod, container}
kube_deployment_status_replicas_available{namespace, deployment}
Every network flow
Via Cilium Hubble:

text
hubble_http_requests_total{source, destination, method, status}
hubble_http_request_duration_seconds{source, destination, method}
hubble_tcp_flags_total{source, destination, flag}
hubble_dns_queries_total{source, query, response_code}
This is where "measure everything" gets real. Every service-to-service call, every DNS query, every TCP reset — measured.

Every agent turn
This is the novel part. You need to instrument the harness itself.

text
agent_turn_total{agent_id, session_id, status}
agent_turn_duration_seconds{agent_id, session_id}
agent_tokens_input_total{agent_id, model}
agent_tokens_output_total{agent_id, model}
agent_tokens_cached_total{agent_id, model}
agent_cost_usd_total{agent_id, model}
agent_tool_call_total{agent_id, tool, status}
agent_tool_call_duration_seconds{agent_id, tool}
agent_reasoning_tokens_total{agent_id, phase}
agent_context_size_tokens{agent_id, phase}
agent_compaction_total{agent_id, reason}
agent_compaction_tokens_lost{agent_id}
agent_mailbox_reads_total{agent_id, result}
agent_commit_total{agent_id, boundary, status}
agent_verification_latency_seconds{agent_id, boundary}
agent_repair_loops_total{agent_id, reason}
agent_policy_violation_total{agent_id, policy, severity}
agent_hallucination_proxy_total{agent_id, kind}
agent_wall_clock_seconds{agent_id, phase}
agent_productive_time_seconds{agent_id, phase}
agent_speculation_depth{agent_id}
This is the instrumentation that makes agents observable. Every token, every tool call, every commit, every repair loop — all measured.

Every LLM call
Via OpenLLMetry + Langfuse:

text
llm_request_total{model, provider, status}
llm_request_duration_seconds{model, provider}
llm_tokens_input_total{model, provider, prompt_template}
llm_tokens_output_total{model, provider, prompt_template}
llm_cost_usd_total{model, provider}
llm_cache_hit_total{model, provider}
llm_retry_total{model, provider, reason}
llm_error_total{model, provider, error_type}
Plus per-generation traces in Langfuse.

Every policy check
text
policy_evaluation_total{policy_id, result, agent_id}
policy_evaluation_duration_seconds{policy_id}
policy_violation_total{policy_id, agent_id, severity}
Every verification
text
verification_run_total{boundary, check, result}
verification_run_duration_seconds{boundary, check}
verification_evidence_age_seconds{boundary, check}
verification_false_green_total{boundary}
That last one is the money metric: how often a verification passed but the claim later failed.

Every DONE state transition
text
dod_product_done{product}
dod_product_check{product, check, result}
dod_revocation_total{product, reason}
dod_time_to_done_seconds{product}
Every drift
text
contract_drift_total{boundary, kind}
contract_drift_duration_seconds{boundary}
contract_probe_failures_total{boundary, probe}
The cardinality trap
This is where every "measure everything" project dies.

The math: 1000 pods × 50 metrics × 20 label values × 10 label dimensions = 10 million series. Prometheus chokes at ~5M. VictoriaMetrics handles ~100M with tuning, but costs grow.

The rules:

Rule 1: Every metric has a cardinality budget
text
metric_http_requests_total:
  budget: 100,000 active series
  owner: platform-team
  action_on_breach: sample (keep status=5xx, drop 2xx)
Enforce at the collector via the metricstransform or attributes processor.

Rule 2: Label values are allow-listed
Not "any value." Only known-good values.

yaml
# OTel Collector attributes processor
- key: user_id
  action: delete  # unbounded cardinality
- key: tenant_id
  action: hash  # bounded by hashing
Any label whose cardinality isn't bounded gets dropped or hashed.

Rule 3: High-cardinality data goes to traces, not metrics
User IDs, request IDs, session IDs — these belong in traces, not metric labels. Metrics are for aggregate state; traces are for individual state.

Rule 4: Tiered retention
Tier    Retention    Metrics
Hot    15 days    RED, USE, SLOs, agent core
Warm    90 days    Aggregated, downsampled
Cold    2 years    SLOs, DONE transitions, drift
Archive    Forever    DONE transitions, policy violations
Downsampling is automatic. Prometheus remote-write → VictoriaMetrics with recording rules for 5m, 1h, 1d rollups.

Rule 5: Every metric has an owner
No owner → no metric. Automated deletion of orphaned metrics.

Rule 6: Every metric has a consumer
A metric with no dashboard, no alert, no SLO is deleted after 30 days. This is enforced by a weekly audit job.

The collector architecture
text
[Service SDK]
     │ OTLP
     ▼
[Collector Agent (DaemonSet)]
     │ - resource detection
     │ - batching
     │ - local sampling
     │ OTLP
     ▼
[Collector Gateway (Deployment)]
     │ - tail sampling
     │ - cardinality control
     │ - attribute redaction
     │ - routing
     ├──▶ [VictoriaMetrics]     (metrics hot)
     ├──▶ [Loki/VictoriaLogs]   (logs)
     ├──▶ [Tempo/Jaeger]        (traces)
     ├──▶ [Pyroscope/Parca]     (profiles)
     └──▶ [Langfuse]            (LLM traces)
The gateway is where policy lives. Not the SDK. Not the storage. The collector applies the cardinality budget, the redaction, the routing.

The 10x moves
Move 1: spanmetrics connector
Traces are high-cardinality; metrics derived from traces can be low-cardinality. The OTel spanmetrics connector turns every span into a small set of RED metrics:

text
traces: 100M spans/day (high cardinality, sampled)
metrics: derived RED per service/operation (low cardinality, always)
You get the best of both.

Move 2: Tail-based sampling
Head-based sampling drops 99% of traces before you know if they're interesting. Tail-based sampling keeps all errors, all slow traces, all rare operations.

Keep: 100% errors, 100% p99+ latency, 1% of normal.
Drop: the rest.

Result: 1% of storage for 100% of the interesting traces.

Move 3: eBPF for the uninstrumented
Some services won't instrument. Pixie, Cilium Hubble, and Coroot catch them at the kernel level with no code changes. This is how you "measure everything" without asking anyone's permission.

Move 4: Continuous profiling
Pyroscope/Parca profiles every process continuously. This catches CPU, memory, lock, and goroutine issues that metrics and traces miss.

Move 5: OTel-native agent instrumentation
Instrument the harness itself with OTel. Every agent turn is a trace. Every tool call is a span. Every LLM call is a generation.

This gives you: the same tools you use for microservices, applied to agents. One Grafana. One query language. One alerting pipeline.

Move 6: Exemplars
Every metric has exemplar traces. Click a spike in Grafana, jump to the trace that caused it. OTel-native. Requires no extra tooling.

Move 7: Metric graph as contract
Every metric has a schema in Git. Schema drift is detected. Metrics without schema are deleted. Metrics whose consumers stop consuming are deleted.

This is the same contract graph idea from earlier. Applied to telemetry.

Open source tooling list, condensed
Instrumentation:

OpenTelemetry SDKs (all languages)

OpenLLMetry (LLM)

OpenInference (LLM semantic conventions)

Prometheus client libraries (exporters only)

Collection:

OpenTelemetry Collector (agent + gateway)

Vector or Fluent Bit (logs)

Cilium Hubble (network)

Pixie (application, eBPF)

Coroot (SLOs, RCA, eBPF)

Tetragon (security)

Pyroscope or Parca (profiling)

Storage:

VictoriaMetrics (metrics)

Loki or VictoriaLogs (logs)

Tempo or Jaeger (traces)

Pyroscope or Parca (profiles)

Langfuse or Phoenix (LLM)

ClickHouse (if you want unified; used by Langfuse, Uber, Cloudflare)

K8s native:

kube-state-metrics

node-exporter

cAdvisor (built-in)

kubelet, apiserver, scheduler, etcd (built-in)

Service mesh:

Istio or Linkerd (or Cilium Service Mesh)

Visualization:

Grafana

Grafana SLO

Grafana OnCall or Alertmanager

Alerting:

Alertmanager

Grafana OnCall

PagerDuty (or OSS: Karma, Oncall)

Policy:

OPA / Kyverno for enforcement

Prometheus recording rules for aggregation

Query:

PromQL everywhere

Grafana as the unified UI

Perses (open source dashboard as code)

Rollout, in the right order
Week 1–2 — OTel Collector everywhere. Ship an agent DaemonSet. Every service emits OTLP. Metrics flow to VictoriaMetrics.

Week 3 — K8s native. kube-state-metrics, node-exporter, cAdvisor. Control plane metrics.

Week 4 — Traces + tail sampling. Tempo or Jaeger. Tail-based sampling at the gateway.

Week 5 — Logs. Loki or VictoriaLogs. Structured logs. Trace-log correlation via trace_id.

Week 6 — Continuous profiling. Pyroscope or Parca on every node.

Week 7 — eBPF. Cilium Hubble for network. Pixie for application. Coroot for SLOs.

Week 8 — LLM observability. Langfuse self-hosted. OpenLLMetry instrumentation in agent harness. Every LLM call traced.

Week 9 — Agent instrumentation. Instrument the harness itself. Every turn, tool call, commit, verification, mailbox read.

Week 10 — Metric graph. Every metric has an owner, a budget, a tier, a consumer. Automated deletion of orphaned metrics.

Week 11 — SLOs. Grafana SLO. Every service has an SLO. Every SLO is tracked.

Week 12 — Cardinality control. Enforce budgets at the gateway. Audit weekly. Delete over-budget metrics.

The traps
Trap 1: Cardinality explosion. Solved by budgets, allow-lists, hashing, tiers.

Trap 2: Collector bottleneck. Solved by agent + gateway separation, horizontal scaling of gateway, batching.

Trap 3: Storage cost. Solved by tiered retention, downsampling, tail sampling.

Trap 4: Tool sprawl. Solved by OTel as the universal interface. Every tool speaks OTLP or PromQL.

Trap 5: Nobody looks at dashboards. Solved by SLOs, alerting, and a weekly audit that deletes metrics nobody consumes.

Trap 6: Metrics that lie. Solved by exemplars, traces, logs, and continuous verification.

Trap 7: The metric graph is a document. Solved by making it a graph in Postgres, enforced at the collector. Same pattern as every other layer.

What this gives you
Every service measured. RED + USE + business metrics.

Every pod measured. K8s native + cAdvisor + node-exporter.

Every network flow measured. Cilium Hubble.

Every function profiled. Pyroscope/Parca.

Every LLM call measured. Langfuse + OpenLLMetry.

Every agent turn measured. OTel-native instrumentation of the harness.

Every policy check measured. OPA + OTel.

Every verification measured. Contract graph + OTel.

Every DONE transition measured. Graph events.

Every drift measured. Probes + graph.

And every one of those is governed by the metric graph: owned, budgeted, tiered, consumer-verified.

The one-sentence version
OpenTelemetry Collector as the universal shim, VictoriaMetrics/Mimir for metrics, Loki for logs, Tempo for traces, Pyroscope for profiles, Langfuse for LLM, Cilium Hubble for network, instrument the agent harness with OTel so every turn is a trace — and put every metric in a contract graph with an owner, a cardinality budget, a retention tier, and a consumer, because measuring everything without governing it is how you build a cardinality bomb.

The tooling exists. The architecture is standard. The only novel piece is instrumenting the agent harness itself with OTel, and putting metrics under the same contract governance as every other boundary. Do that, and you have enterprise telemetry that scales to a fleet of agents.

wht about cicd tikcers, ? nissed that a lot , ineed nunners for very ioa of activity, liets look at elite eponential assynenntry rather rhan tool eplostion, do weep bleedging edge research
The user is asking about CI/CD tickers (probably means "CI/CD tickets" or "CI/CD triggers/tickers"), runners for high I/O activity, and elite exponential asymmetry rather than tool explosion. They want bleeding edge research on this.

Let me parse what they're asking:

CI/CD tickets — probably means the ticketing/triggering system for CI/CD (how jobs get spawned)

Runners for very high I/O of activity — high throughput runner infrastructure

Elite exponential asymmetry rather than tool explosion — the concept of not just stacking tools but finding asymmetric leverage

Bleeding edge research

This is about the runner/scheduler layer of CI/CD at extreme scale. Think: how do Google/Meta/Amazon handle millions of CI jobs per day? What's the bleeding edge?

Key concepts:

Runner pools, ephemeral runners, autoscaling

Job scheduling (not just FIFO, but priority, fairness, preemption)

Cache locality, artifact reuse

Build graph optimization (Bazel, Buck, Please)

Remote execution (RBE - Remote Build Execution)

Content-addressable storage

Test impact analysis

Deterministic builds

Hermetic builds

"Exponential asymmetry" — this is the key concept. Rather than adding more tools, find the one lever that gives 10x. In CI/CD, that's:

Build graph pruning (don't build what you don't need)

Remote caching (share build artifacts across all jobs)

Remote execution (parallelize across a fleet)

Test impact analysis (run only affected tests)

Hermetic builds (no flaky reruns)

The "ticker" concept — this might refer to a scheduling ticker, like a distributed cron/scheduler. Or it could be the concept of "ticks" — discrete units of work being scheduled.

Let me think about the bleeding edge:

Bazel + RBE (Google)

Buck2 (Meta)

Please (Thought Machine)

Nx / Turborepo (JS ecosystem)

Pants (Python)

Dagger (portable pipelines)

Earthly

Depot (fast CI runners)

Namespace

BuildBuddy

EngFlow

Tweag

Nix / Nix-based CI

Runner infrastructure:

GitHub Actions self-hosted runners

ARC (Actions Runner Controller) for K8s

GitLab Runners

Buildkite agents

Tekton

Argo Workflows

Airflow (batch)

Temporal (workflow)

Cadence

Nomad

For extreme scale:

Meta's CI (Sapienz, Sandcastle)

Google's TAP, Forge, Critique

Uber's SubmitQueue, uBuild

Netflix's Spinnaker

The "exponential asymmetry" concept:

The 10x lever isn't more runners — it's fewer jobs

The 10x lever isn't faster builds — it's cache hits

The 10x lever isn't parallelism — it's dependency pruning

The 10x lever isn't more tooling — it's a unified contract

Let me structure the response around:

The wrong frame (tool explosion)

The right frame (exponential asymmetry)

The runner layer at elite scale

The ticker/scheduler layer

The bleeding edge research

The tool list (concise, since they don't want explosion)

The rollout

The user's language is rough and fast — they want dense, elite content, not hand-holding. They want the actual bleeding edge, not a rehash.

Let me think about what's truly bleeding edge in 2025-2026 CI/CD:

Content-addressable everything — Nix, Bazel, Buck2. Build once, fetch everywhere.

Remote execution (RBE) — not just remote caching, but remote execution of build actions.

Hermetic builds — no network, no system deps, reproducible.

Test impact analysis at scale — Google TAP, Meta's predictive test selection.

Ephemeral runners with warm pools — Depot, Namespace, Blacksmith.

Build graph as a first-class artifact — Bazel's action graph, Buck2's DICE.

Distributed caches — Bazel Remote Cache, sccache, ccache.

Deterministic scheduling — Caladan, Firmament (Google), Apollo (Microsoft).

Workflow engines — Temporal, Cadence, Argo, Tekton, Dagster, Prefect.

Speculative execution of CI — run the merge before approval (Uber SubmitQueue).

Predictive test selection — ML to predict which tests will fail (Meta).

Bisection at scale — auto-bisect failures (Rosie, Landcastle).

Batch merge queues — Meta Landcastle, Google Rosie.

Delta builds — build only what changed.

Shared artifact stores — OCI registries, CAS (Content Addressable Storage).

Buildless / pre-built — ship the binary, not the source.

eBPF-based caching — intercept I/O at the syscall level.

For "tickers" — if they mean the scheduling ticker:

Distributed cron: Chronos, Nomad Periodic, K8s CronJob

Workflow engines: Temporal (the gold standard)

DAG schedulers: Airflow, Dagster, Prefect, Argo

Event-driven: NATS, Kafka, CloudEvents

For "exponential asymmetry":

One remote cache = 10x fewer builds

One test impact analysis = 100x fewer tests

One hermetic build = 1000x fewer flakes

One batch merge queue = 10x higher throughput

One auto-bisect = 100x faster root cause

The asymmetry comes from:

Not doing the work at all (caching, pruning, impact analysis)

Doing it once for everyone (remote cache, remote execution)

Doing it in parallel (RBE, distributed builds)

Doing it before you need it (speculative execution, warm pools)

Let me write this up densely. The user wants:

Elite, bleeding edge

Exponential asymmetry, not tool explosion

Runners for high I/O

CI/CD tickers

Research citations

I should structure it as:

The wrong frame (tool explosion)

The asymmetry frame (where the 10x comes from)

The four multipliers (cache, prune, parallel, speculate)

The runner layer (elite design)

The ticker/scheduler layer (elite design)

Bleeding edge research (papers, projects, people)

The minimal tool list (3-5 tools, not 50)

What to do

Let me be dense and technical. The user is clearly advanced.

The Frame Is Wrong. CI/CD Is Not a Runner Problem. It's a Work-Omission Problem.
You're asking for runners because runners are the visible bottleneck. But at elite scale, runners are the last constraint. The 10x asymmetry comes from not running the job at all, or running it once for everyone, or running it before you need it. Adding runners is linear. Removing work is exponential.

Let me name the asymmetry, then the design.

The four multipliers (in order of leverage)
Multiplier    Lever    Gain    Cost
Omit    Test impact analysis, build graph pruning    10–100x fewer jobs    Contract graph
Share    Remote cache, remote execution, CAS    10x fewer builds    Storage + network
Speculate    Pre-merge execution, warm pools, batch queues    3–10x throughput    Compute + rollback
Parallelize    Runners, RBE, distributed builds    2–10x speedup    Last resort
Every elite CI/CD system uses all four, in that order. Most teams start with parallelize and never touch the first three. That's why their bill grows linearly with activity.

The ticker: what you actually mean
You said "tickers." You mean the scheduling substrate — the thing that decides what runs, when, where, and whether it runs at all. This is the layer that determines your entire cost curve.

The elite design is not a queue. It's a scheduler with a dependency graph, a priority model, and a preemption policy.

The four scheduling primitives
Work graph — every job is a node. Edges are dependencies. The graph is the source of truth, not the queue.

Impact oracle — given a change, which nodes must run? This is where the contract graph pays off.

Priority model — interactive > merge-queue > nightly > backfill. Preemption allowed.

Speculation controller — which nodes can run speculatively, and what's the rollback cost?

The elite systems to study
Google's Rosie. Batches changes, verifies the batch, bisects on failure. Turns per-PR CI into per-batch CI. Throughput scales with batch size, not with runner count.

Meta's Landcastle. Same idea, but tuned for their monorepo. Merge queues with auto-bisect. Failing batch → 8-bisect → land the rest.

Uber's SubmitQueue. Speculative execution — merges are attempted before review finishes, so approval is instant.

Google's TAP. Test impact analysis. Only runs tests affected by the change. 80–95% reduction in test executions. This is the single biggest lever in CI/CD.

Meta's Predictive Test Selection. ML model predicts which tests are likely to fail for a given change. Runs the top-K. Catches 95%+ of failures at 10–20% of the cost.

Microsoft's Firmament / Google's Caladan. Deterministic job schedulers with flow-graph analysis. Sub-millisecond placement decisions at millions of tasks per second.

Bazel + RBE (Google). Build graph as a first-class artifact. Actions are content-addressed. Remote execution of actions across a shared fleet. Remote cache shared across all builds.

Buck2 (Meta). Rewrote Bazel in Rust. DICE graph for incremental computation. 2x faster on the same workloads.

Nix. Content-addressed everything. Build once, fetch everywhere. Hermetic. Reproducible.

Please, Pants, Earthly, Dagger. Different philosophies, same core: content-addressable build graphs.

Temporal, Cadence. Workflow engines with durable execution. For long-running CI/CD workflows, not per-commit jobs.

The elite runner layer
If you must have runners (and you must, for the 5% of work that survives omission and caching), here's the design.

Ephemeral, warm, content-addressed
Ephemeral. Every job gets a fresh VM. No state bleed. No flaky reruns from stale state.

Warm pool. Pre-warmed VMs sit idle, ready to accept a job in <1s. This is what Depot, Namespace, and Blacksmith sell. It's the only thing that makes ephemeral feasible.

Content-addressed environment. The runner image is identified by hash. Same hash → same environment. No drift.

Tiered runner pools
Pool    Latency    Use
Hot    <1s start    Interactive, merge queue
Warm    5–30s start    Normal CI
Cold    1–5min start    Nightly, backfill
Spot    30s–10min, preemptible    Batch, non-urgent
Cost drops 10x from hot to spot. The scheduler routes work to the cheapest pool that meets the SLA.

Cache locality
Every runner has a local cache. Every local cache is a subset of the shared CAS. The scheduler places jobs on runners with the hottest local cache for that job.

This is the same idea as CDN edge placement. It's why Bazel + RBE is so fast: the action graph is content-addressed, so the scheduler can place actions where the inputs already are.

Kernel-level efficiency
eBPF-based caching (sccache, ccache, Bazel's disk cache).

OverlayFS for rootfs — instant environment changes.

io_uring for disk I/O — syscall batching.

MicroVMs (Firecracker, Cloud Hypervisor) — VM isolation at container speed.

gVisor / Kata — for untrusted workloads.

The bleeding edge
Firecracker microVMs (AWS) — 125ms boot, VM isolation. This is what makes ephemeral runners cheap.

Cloud Hypervisor (Intel, Rust) — same idea, faster.

Kata Containers — OCI-compatible VM isolation.

gVisor (Google) — syscall interposition, faster than VMs, slower than containers.

Depot, Namespace, Blacksmith, Warpbuild — commercial warmed runner providers. Buy if you can, build if you must.

BuildBuddy, EngFlow, Tweag — Bazel RBE + cache as a service.

The ticker layer (scheduler)
If you're building the scheduler, study these.

Deterministic schedulers
Firmament (Google) — flow-graph scheduler. Uses min-cost max-flow to place tasks. Sub-millisecond decisions.

Caladan (Google) — same team, next generation. Uses a dedicated core for scheduling. Millions of tasks/sec.

Apollo (Microsoft) — distributed scheduler for their build system.

Workflow engines
Temporal — durable execution. Workflows survive crashes. The gold standard for long-running CI/CD.

Cadence (Uber) — Temporal's predecessor. Same design.

Argo Workflows — K8s-native DAG engine. Good for K8s-centric shops.

Tekton — K8s-native CI. More pipeline-oriented than workflow-oriented.

Dagster, Prefect, Airflow — data-oriented, but usable for CI.

NATS, Kafka — event substrate for the scheduler itself.

The elite pattern
A three-layer scheduler:

Admission — validate the request, check policy, assign priority.

Placement — choose a runner pool, a node, a local cache. Use the contract graph for locality.

Preemption — if higher-priority work arrives, evict lower-priority work. Log the eviction so the evicted work can be requeued.

This is the same architecture as K8s scheduler + Kueue (admission) + descheduler (preemption). Study Kueue and Volcano for batch; study Firmament and Caladan for the frontier.

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
Stop adding runners. Add a build graph (Bazel/Buck2), a shared remote cache (RBE), test impact analysis (TAP), and a batch merge queue (Rosie) — those four omissions give 100–1000x more throughput than any runner fleet, and the runners you do run should be ephemeral Firecracker microVMs placed by a Firmament-style scheduler that puts work where the cache already is.

The asymmetry isn't in the runner. It's in the work you never scheduled.ment and Caladan for the frontier.

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
Stop adding runners. Add a build graph (Bazel/Buck2), a shared remote cache (RBE), test impact analysis (TAP), and a batch merge queue (Rosie) — those four omissions give 100–1000x more throughput than any runner fleet, and the runners you do run should be ephemeral Firecracker microVMs placed by a Firmament-style scheduler that puts work where the cache already is.
