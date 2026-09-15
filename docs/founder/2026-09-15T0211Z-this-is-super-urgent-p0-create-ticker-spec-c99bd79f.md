---
captured: 2026-09-15T02:11:57+00:00
session: b47fc54c-5658-4c97-865c-a88fcc6b441e
cwd: /Users/chidionyema/dev/code/idp
chars: 2525
source: founder prompt, verbatim (founder-doc-capture.py)
---

this is super urgent p0, create ticker  spec thpourugly incluug bdd, and use 2 parllen agents inclding urself to get it done faster and also ultra optinisne before diing the work for quick and effiecient build ve proof tonight; the catalog-drift builder is running in the background; two remain, deliberately not rushed.

Shipped, real cluster evidence, not committed:

1. K8s adapter gap (was: get_workload_state/get_workload_logs blind to the cluster despite it being live) — mcp/plugins/workload_state.py only ever read the launchd/colima assets table. The live cluster data was already there in estate.db's nodes table (bin/estate-twin-runtime's 15-min sweep) — it was just never queried. Added read_k8s_state() as a fallback. Live proof, run against the real db just now:
   get_workload_state("estate-mcp") → was found: false, empty state. Now returns real pod data: namespace: mcp, pods_total: 1, pods_running: 1, restarts_max: 5, state_source: "estate.db nodes (live k8s cluster sweep, ADR 0004)". (Pod count is stale — 1 vs the 2 live now — because the sweep hasn't run since; that's exactly why item 4, freshness, matters next.)
2. Bash-fallback telemetry — the rule-guard/claude-guards/policy/command.rego mechanism named in bin/idp-kube's own comment turned out to live in an external plugin, outside this repo's authority to edit. Scoped it down to what's actually mine to fix: bin/idp-kube already logged the rare break-glass escape hatch but nothing else. Every invocation now appends one line — timestamp, agent, identity used, full command — to $STATE/kube-calls.log. Live proof: ran bin/idp-kube auth whoami, confirmed the line landed:
   2026-09-15T00:15:34Z  unknown  kubeconfig-reader  auth whoami
   That's the visibility gap you flagged directly — "why is this whole thing not visible to me" now has an answer file.
3. Node-id bug fix (carried from earlier this session) — still staged, unchanged.

Running now, background: an engineering agent building get_catalog_drift() from scratch (confirmed it never existed anywhere in the codebase, despite ADR 0006 naming it) — briefed with the real Cilium/Hubble catalog lie as its acceptance test, required to prove it discriminates (flags the lie, doesn't flag a healthy entity) before reporting back.

Deliberately not touched yet, and I'm pushing back on rushing them:
- The typed multi-domain mutation ledger (code+manifest+SQL in one atomic proposal) — this extends estate_executor.py/estate_simulate.py, the live production mutation-safety gauntlet wi
