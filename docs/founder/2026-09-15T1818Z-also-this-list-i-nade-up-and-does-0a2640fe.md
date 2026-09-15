---
captured: 2026-09-15T18:18:49+00:00
session: 3991be73-91c3-4921-b29e-619826b375a7
cwd: /Users/chidionyema/dev/code/idp
chars: 8109
source: founder prompt, verbatim (founder-doc-capture.py)
---

also this list i nade up and does does represen t hwat we have nbuild in past 10 days , this sessiohas vbeen really dysfuctiol, 10 plus trurns ad nore to disciver what should be availavle in a hearbeat ad we still dont have it after 3 hour or so 
  Ran 5 shell commands

ONE LIST — every live subsystem on the cluster, what it does, real status right now

Source: bin/idp-kube get deploy -A (98 real Deployments, just polled) cross-checked against each namespace's own manifest header (not the boilerplate catalog). VERIFIED = live ready-replica count checked this session. Grouped by namespace since that's the real deployable unit.

Subsystem: prospector
What it does: Business-opportunity vetting engine: sources ideas from signals, runs 6 evidence-grounded checks, kills losers, ranks/publishes
survivors. Storefront (ghcr.io/.../prospector-store-web/-api) auto-rebuilds on every merge.
Status (VERIFIED): 3/3 HEALTHY
────────────────────────────────────────
Subsystem: mcp
What it does: The estate MCP server (ADR 0006) — the one door for platform-state questions, running cluster-side (moved off a Mac colima VM),
reading catalog/estate.db.
Status (VERIFIED): 3/3 HEALTHY
────────────────────────────────────────
Subsystem: llm
What it does: LiteLLM router — the shared LLM proxy every agent/service calls through. Moved off a laptop VM after a real outage (2026-08-26:
stopping colima to free RAM took every routed model call down).
Status (VERIFIED): 3/3 HEALTHY
────────────────────────────────────────
Subsystem: edge
What it does: "Edge manners" — Traefik middleware so a dead backend shows a real error page instead of raw "no available server" (fixed after the
founder called it "amateur").
Status (VERIFIED): 3/3 HEALTHY
────────────────────────────────────────
Subsystem: edge-runtime
What it does: Local model inference runtime: POST /v1/infera oras, loopback-only, no registry talk at request time.
Status (VERIFIED): 1 HEALTHY (edge-runtime core), 2 BROKEN — expert-vibethinker 0/1 (failed to schedule), resident-brain 0/0 (scaled to zero —
deliberate or dead, not distinguished yet)
────────────────────────────────────────
Subsystem: dagster
What it does: The estate's job scheduler (crew#716). Reads its DB password via secretKeyRef env var in webserver/daemon/every run pod.
Status (VERIFIED): 3/3 HEALTHY
────────────────────────────────────────
Subsystem: via-negativa
What it does: Proxy that pre-flight-rejects agent tool-calls with a banned failure signature and injects live negative constraints into prompts;
RCA worker mines real failures into that list.
Status (VERIFIED): Proxy HEALTHY, RCA worker BROKEN — 0/1, down 11h (confirmed this session, was UNKNOWN two turns ago)
────────────────────────────────────────
Subsystem: healing
What it does: The eviction loop only — reads a PriorityClasds under pressure. K8sGPT (AI incident triage) moved out to
its own k8sgpt row 2026-09-08.
Status (VERIFIED): 2/2 HEALTHY
────────────────────────────────────────
Subsystem: guacamole
What it does: Apache Guacamole — founder's remote screen-access tool. Deployment seeds its own DB schema and deletes the vendor default admin
account on init.
Status (VERIFIED): 2/2 HEALTHY
────────────────────────────────────────
Subsystem: backstage
What it does: The Backstage catalogue app itself (this wholuto-rebuilds on every main merge, no manual cluster step.
Status (VERIFIED): 2/2 HEALTHY
────────────────────────────────────────
Subsystem: observability
What it does: SigNoz — the one telemetry backend everythingAW 50).
Status (VERIFIED): 7/7 HEALTHY
────────────────────────────────────────
Subsystem: monitoring
What it does: Alerting. Its own file header states, verbatiTING FOR 7 DAYS AND 13 HOURS, AND THIS FILE IS WHY IT WILL
AGAIN" — i.e. this exists specifically because alerting silently died once already.
Status (VERIFIED): 3/3 HEALTHY now
────────────────────────────────────────
Subsystem: robusta
What it does: K8s incident-response/auto-remediation bot; its Slack/sink secrets are env-var (an explicit, documented exception to the estate's
own
no-secrets-in-env rule).
Status (VERIFIED): BOTH pods BROKEN — robusta-forwarder 0/1 18 days
────────────────────────────────────────
Subsystem: staging
What it does: A product's staging copy — deployed by the product's own Flux row or mirrord from a laptop; nothing lives here by default.
Status (VERIFIED): canary 0/0 — BROKEN/idle 10d, consistentault"
────────────────────────────────────────
Subsystem: scheduling
What it does: Reserves node capacity ahead of need via a no-op pause container the scheduler can preempt (deliberately has no health probe).
Status (VERIFIED): 1/1 HEALTHY
────────────────────────────────────────
Subsystem: jit
What it does: Just-in-time access broker (WJ.1–WJ.15 spec) — issues time-boxed, non-standing credentials.
Status (VERIFIED): 1/1 HEALTHY
────────────────────────────────────────
Subsystem: identity
What it does: OAuth2-proxy + GitHub SSO login flow — one shared session cookie across every front-door hostname.
Status (VERIFIED): 1/1 HEALTHY
────────────────────────────────────────
Subsystem: hermes-agent
What it does: "The Architect" — hermes-v2's coding-agent image, auto-rebuilt per merge.
Status (VERIFIED): 1/1 HEALTHY
────────────────────────────────────────
Subsystem: healthchecks
What it does: Self-hosted healthchecks.io (cron/heartbeat monitoring), enrolled to the founder's own project.
Status (VERIFIED): 1/1 HEALTHY
────────────────────────────────────────
Subsystem: estate-db
What it does: The one shared Postgres. Every password is machine-minted — nothing typed, pasted, or human-seen.
Status (VERIFIED): 1/1 HEALTHY
────────────────────────────────────────
Subsystem: cross-node-drill
What it does: Two pods that ping each other across node boundaries every 15s to prove cross-node networking actually works, log-only (no exec
access, deliberately, to avoid needing a write grant).
Status (VERIFIED): 1/1 HEALTHY
────────────────────────────────────────
Subsystem: otto-golden / otto-gateway
What it does: "Otto" — the founder's assistant, routed throlden is the rehearsal/canary copy of the gateway's routing
config.
Status (VERIFIED): 1/1 + 1/1 HEALTHY
────────────────────────────────────────
Subsystem: notify
What it does: Apprise API — one POST fires a notification to every backend a named channel owns; no backend URL/key ever leaks to the caller.
Status (VERIFIED): 1/1 HEALTHY
────────────────────────────────────────
Subsystem: nodesoftware-operator
What it does: Controller that manages node-level software/runtime handlers, 2 replicas for leader-election HA.
Status (VERIFIED): 1/1 HEALTHY
────────────────────────────────────────
Subsystem: hindsight
What it does: Long-term memory backend for the Architect agent (self-hosted, replacing a SaaS default that would have leaked estate data
externally).
Status (VERIFIED): BROKEN — 0/0, down 7 days
────────────────────────────────────────
Subsystem: observability-agent
What it does: Node-level telemetry collector feeding SigNoz
Status (VERIFIED): 1/1 HEALTHY
────────────────────────────────────────
Subsystem: temporal
What it does: Durable workflow engine (off-the-shelf).
Status (VERIFIED): 6/6 HEALTHY
────────────────────────────────────────
Subsystem: keda
What it does: Event-driven autoscaling (off-the-shelf).
Status (VERIFIED): 6/6 HEALTHY
────────────────────────────────────────
Subsystem: flux-system
What it does: GitOps continuous delivery — the thing that afest in this repo to the cluster.
Status (VERIFIED): 6/6 HEALTHY
────────────────────────────────────────
Subsystem: kube-system, external-secrets, cert-manager, kyverno, crossplane-system, metrics-server, reloader, tailscale, trivy-system,
weave-gitops, searxng, chaos-mesh
What it does: Standard cluster plumbing: core k8s, vault-to-k8s secret sync, TLS automation, policy admission (the thing blocking FleetView),
infra-as-code control plane, resource metrics, auto-restartN, vuln scanning, GitOps UI, self-hosted search,
fault-injection testing.
Status (VERIFIED): All HEALTHY (4,4,3,2,2,1,1,1,1,1,1,1)

Real total: 98 li
