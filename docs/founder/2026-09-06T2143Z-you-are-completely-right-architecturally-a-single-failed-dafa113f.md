---
captured: 2026-09-06T21:43:51+00:00
session: dde713cc-8383-465a-908b-7e89c070bf22
cwd: /Users/chidionyema/dev/code/idp
chars: 3894
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are completely right. Architecturally, **a single failed data-copy or migration job should never take down or freeze your entire platform**.

Having observability, LLM routing, Dagster, and the research engine ground to a halt because a database copy failed is a classic **blast-radius anti-pattern**.

Here is why this design flaw happens in GitOps, why Flux behaved this way, and how to decouple it so a failed job never freezes your estate again.

---

### Why It Happened: The GitOps "Emergency Brake"

Flux operates under a strict **fail-closed, safety-first philosophy**:

1. **Overly Broad `dependsOn` Chaining:**
In your `clusters/oke/platform.yaml` (or kustomization definitions), the platform services were likely tied together in a single sequential pipeline:

$$\text{db-sync} \longrightarrow \text{llm} \longrightarrow \text{dagster} \longrightarrow \text{observability}$$


2. **The Terminal State of Kubernetes Jobs:**
When a Kubernetes `batch/v1 Job` fails its `backoffLimit` (usually 6 retries), Kubernetes marks it as permanently `Failed`. Unlike Deployments, Jobs do not self-heal or keep trying indefinitely.
3. **The Deadlock:**
Because the Job sits permanently in `Failed`, Flux marks the upstream Kustomization as `NotReady`. Downstream Kustomizations check `status.conditions[Ready] == True`. Because it is `False`, Flux triggers an emergency brake, assuming that letting downstream services start against an incomplete database will cause data corruption or crash-loops.

The problem? **Observability and LLM gateways don't care about a database copy.** Tying them to the same dependency gate violates basic fault isolation.

---

### How to Decouple This Permanently

To make your cluster resilient, non-critical background jobs must be decoupled from the core infrastructure path.

#### 1. Split Core Services from Data Workflows (Narrow the Blast Radius)

Observability, core networking, and foundation models should live in a **Level 0 / Foundation** tier that has zero dependencies on business data jobs.

```
[ Tier 0: Foundation ] (Never blocks on anything)
├── networking (calico / flannel / traefik)
├── observability (signoz / prometheus)
└── llm-gateway (litellm / vllm)

[ Tier 1: State & Storage ]
└── postgres / cnpg-cluster

[ Tier 2: Data Jobs & Apps ] (Only apps depend on this)
└── db-copy-job  ──(dependsOn)──> dagster / research-engine

```

#### 2. Don't Let One-Off Jobs Block GitOps Reconciliation

If a job is a data-sync, seed, or migration utility:

* **Remove `spec.wait: true**` on Kustomizations containing ad-hoc jobs, or omit the Job from health check evaluations so Flux doesn't wait for completion before proceeding.
* **Use Helm Hooks with Delete Policies:** If deployed via Helm, annotate with `helm.sh/hook-delete-policy: hook-succeeded,before-hook-creation` so failed relics don't deadlock the next reconciliation loop.
* **Run Syncs as Triggered Workflows, Not Gatekeeper Manifests:** Data copying belongs in an orchestrator (like a Dagster asset or Argo workflow) or a Kubernetes CronJob—not as a gating manifest in the root platform deployment repo.

---

### Immediate Fix to Unstick Your Cluster Right Now

If you want the agent to unblock everything immediately without waiting for the DB copy to be solved:

1. **Remove or bypass the dependency in Git:**
Edit the downstream Kustomizations (`llm`, `observability`, etc.) in `clusters/oke/` and temporarily delete or comment out the `dependsOn` block that points to the database sync.
2. **Push and reconcile:**
```bash
git commit -am "fix: decouple observability and llm from db sync job"
git push
flux reconcile kustomization platform --with-source

```


3. **Delete the stuck Job pod:**
```bash
kubectl delete job <failed-db-job> -n <namespace>

```



Flux will immediately ignore the database state and proceed to reconcile and boot `observability`, `llm`, and Otto.
