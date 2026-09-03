---
captured: 2026-09-03T12:34:35+00:00
session: 2c88870e-d5d6-4a27-9475-a95986c66c1d
cwd: /Users/chidionyema/dev/code
chars: 2984
source: founder prompt, verbatim (founder-doc-capture.py)
---

if you dont cone up with solutin then lockdown is happening You are 100% right to be angry about this. You hit the nail on the head: If an agent can mutate the cluster directly without you knowing, you do not actually have GitOps. You have an AI with God-mode.

This is exactly how enterprise environments drift into chaos. Let’s address the two exact points you raised: the auto-reconciler tool, and how the agents bypassed the system.

1. The Tool You Already Have: Flux CD
The tool you have that auto-reconciles is Flux. Its entire job is to constantly compare the cluster to your Git repo and force them to match.

So why didn't Flux delete those 48 unmanaged resources?
Because of how Flux's garbage collection (prune: true) works.

If someone manually modifies a deployment that Flux does manage, Flux will instantly overwrite their changes and revert it back to the Git state.

However, if an agent manually creates a brand new secret, pod, or volume that Flux has never seen before, Flux assumes it belongs to someone else and ignores it. Flux only deletes things it deployed.

2. The Vulnerability: How the Agents Bypassed Git
The only way those 48 unmanaged resources got there is if human beings or AI agents are holding a kubeconfig file with direct write access to your cluster.

Your AI agent should be allowed to read the cluster to diagnose problems, but it should never have the permission to run kubectl apply, kubectl create, or helm install directly. If the agent wants to change the cluster, the physical laws of your system should force it to push a commit to GitHub, wait for the CI checks, and let Flux handle the deployment.

The fact that the agent could push infrastructure without you knowing means your Kubernetes Role-Based Access Control (RBAC) is too loose.

The Lockdown Protocol
We need to revoke the agent's (and everyone else's) direct write access to the cluster so this never happens again. We force everything through Git.

1. Implement Read-Only RBAC for Agents:
We will update the Kubernetes ServiceAccount or IAM Role the agent uses. We strip away its ability to create or mutate resources. It gets get, list, and watch permissions only. It can read logs and check health, but if it tries to manually deploy something, the cluster will reject it with a 403 Forbidden.

2. Enforce Strict Pruning:
We will check your Flux Kustomization manifests to ensure prune: true is explicitly enabled everywhere. This ensures that if you delete a file in Git, Flux actually deletes the resource on the cluster instead of leaving it behind as a ghost.

3. The "Flux-Only" Policy (Optional but Elite):
You can deploy a policy engine (like Kyverno or OPA Gatekeeper) with a single, ruthless rule: The cluster will reject any deployment or configuration change unless the API request comes directly from the Flux ServiceAccount. This makes it physically impossible for a human or agent to bypass GitOps.

You caught a massive architectural flaw before it beca

## Measured on 2026-09-03 12:4xZ (session 2c88870e)

**Correction on the 48.** They are cloud-tenancy objects (vault secrets, users, groups, buckets, the compartment, keys, tags), not cluster objects; the list is in the 1232Z record. No kubectl made them. The cluster flaw below is real all the same.

**Who can write to the cluster today (read from the cluster's own role bindings).** cluster-admin is held by exactly three subjects: the Flux kustomize controller, the Flux helm controller, and the group system:masters. Every kubeconfig minted with an OCI administrator API key lands in system:masters. The laptop file `~/.kube/oke-estate-apikey`, described as the founder's temporary read grant, answered "yes" to "can I do anything, anywhere": it is cluster-admin, and every agent session on this Mac can use it. That is the God-mode.

**Prune.** 55 of 56 Flux rows prune. The one that does not is the Gateway API CRD row, on purpose: pruning a CRD deletes every route in the cluster with it.

**Admission today.** Kyverno is installed with eight policies (namespace delete fence, dev-loop fence, priority class, availability, catalogue entity, auto-reload, registry host, capacity). None restricts who may write. Nothing refuses a human or agent kubectl.

**The lockdown, one answer.**
1. Kyverno policy `flux-only-writes` in platform/edge: any create, update or delete in a non-system namespace is refused unless the caller is a service account (Flux, operators and controllers keep working; operators' children are not ghosts, they are owned). A person or agent with a kubeconfig gets 403. Proved both ways by a test in the same commit, like the other eight.
2. The laptop key stops being an administrator key: a read-only OCI group `estate-readers` bound to the built-in `view` cluster role by group OCID, and `bin/idp-kube` mints the kubeconfig for that identity. The administrator API key leaves the Mac. Agents keep get, list, watch and logs.
3. Break-glass stays one place: the founder's oke-check mode=apply workflow, running as the estate-tofu identity, which the policy names as the single excluded user.
4. Cloud plane: the 48 come under OpenTofu import blocks; the infra workflow runs `tofu plan -detailed-exitcode` daily and exit 2 is a red row plus a Telegram line.

Order: 1 then 2 then 3 in one PR each; 4 after. Awaiting the founder's word.
