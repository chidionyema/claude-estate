---
captured: 2026-09-03T12:32:48+00:00
session: 2c88870e-d5d6-4a27-9475-a95986c66c1d
cwd: /Users/chidionyema/dev/code
chars: 2343
source: founder prompt, verbatim (founder-doc-capture.py)
---

we cant let thsi drift ever happen again, unless you have better suugestions t feels like a disaster, but take a breath—this is not a disaster. It is just the reality of building a startup fast.

Every single company that moves quickly accumulates "Infrastructure Drift." You aren't failing; you just finally got an automated system smart enough to measure the mess you left behind while sprinting.

Here is exactly how those 48 unmanaged resources and the Layer-0 drift happened:

1. The Layer-0 "Chicken and Egg" Problem
To use Infrastructure as Code (like Terraform/OpenTofu), you need a secure cloud bucket to store the "state" of your code. But how do you create that first bucket using code if you don't have a bucket to store the code yet?

Almost every founder solves this by logging into the Oracle Cloud web console, manually clicking "Create Compartment" and "Create Bucket," and then connecting their code to it. It’s a necessary evil to get started, but it leaves your foundation (Layer 0) unmanaged by Git.

2. The 2 AM Firefighting
Think about last night. You were tired, the cluster was stalled, and you were running manual kubectl commands, applying patches, and forcing webhooks to test if things worked.

Every time you (or an agent, or a consultant) use a manual command to fix a problem instead of writing a YAML file and pushing it to GitHub, Kubernetes creates that resource, but Git never learns about it. Those are "ghost resources."

3. Operator Exhaust
When you install complex tools like Ingress controllers, Cert-Manager, or databases via Helm, they often generate their own auxiliary resources on the fly—like dynamic secrets, temporary replica sets, or certificates. Git only tracks the "parent" instruction, so the cluster sees these dynamically generated children as "unmanaged."

Why You Shouldn't Panic
A disaster is when your cluster burns down and you don't know why you can't rebuild it.

You are in the opposite situation: your agent successfully audited the entire estate and gave you an exact count. You have exactly 48 pieces of tech debt. It's a bounded, solvable checklist, not a mystery.

Before we delete or import anything, we need to know exactly what those 48 things are. Most of them are likely just temporary garbage that can be safely nuked.

Want to see the exact list of the 48 items?

Yes

## Measured answer (session 2c88870e, 2026-09-03 12:4xZ)

**Where the 48 came from.** `bin/idp-estate-audit` on 2026-08-31 at 10:52Z, cloud tenancy only, recorded in idp `docs/audit/estate-inventory.md` under "The codify list". The exact 48: 27 vault secrets (authelia, authelia-users, backstage-env, cloudflare-api-token, flux-telegram, flux-writer, github-app, guacamole, hermes, hermes-agent-env, hermes-mac-run, hindsight, k8sgpt, laptop, litellm-ui, litellm-upstream, mcp-gateway, oauth2-proxy-cookie-secret, oke-autoscaler, prospector-engine-env, prospector-store-api-env, science, signoz-prover, sunshine-auth, tailscale-operator, temporal-db, plus DEFAULT which is pending deletion); 4 users (the founder, estate-ci, estate-drill, estate-tofu); 3 groups (All Domain Users, estate-operators, estate-provers); 2 policies (Tenant Admin Policy, estate-operators-manage-estate); 3 buckets (estate-drill-receipts, estate-shop-backups, estate-tofu-state); the compartment `estate`; 3 keys (two RSA wrapping keys, one pending deletion, and estate-secrets pending deletion); the old vault estate-secrets (pending deletion); the default route table of the cluster network; 3 tag objects (Oracle-Tags namespace, createdby, createdon). None is garbage except the four objects already pending deletion.

**What the daily drill says today.** The estate-inventory drill ran at 07:14Z (run 33726985140) and reported success, but it was blind on the cloud tenancy (its discovery step raised a code error), GitHub, Tailscale (token refused, 401) and the Mac. It read Kubernetes and Cloudflare only. Kubernetes: 1386 managed, 5 drifted (commerce, commerce-data, event-bus, notify, temporal not ready), 1465 "orphan" of which 1003 are Kyverno ephemeral reports, 71 IP addresses, 59 Cilium identities, 72 finished jobs, 82 cluster roles: operator exhaust graded as debt. Cloudflare: all 30 DNS records graded orphan, though the A and TXT records are written by external-dns from git routes. The drill goes red only when every plane is blind, so a run that measured nothing on the cloud plane read green.

**The one answer for "never again".** Drift is prevented by removing the ability to drift, not by counting it afterwards.
1. Cloud tenancy: the 48 come under OpenTofu with `import` blocks (the 24 Terraform-made secrets already are); then the existing infra workflow runs `tofu plan -detailed-exitcode` daily and any exit 2 is a red row on the Ops dashboard and a Telegram line. The plan is the drift detector; the hand-rolled OCI discovery that raised the code error is retired.
2. Cluster: nobody holds a write credential outside Flux. The founder's read-only kubeconfig stays; no agent has one. Kyverno, already installed, gets one validate policy: an object created in a Flux-owned namespace must carry the Flux owner label, or admission refuses it. A hand `kubectl apply` cannot create a ghost.
3. The inventory grader stops counting operator-made children (owner references, ephemeral reports, Cilium and IP objects) and external-dns records as debt, and goes red when any plane is blind, so the number the founder reads is real.
Layer 0 (compartment, state bucket, credential) is written as the bootstrap module with local state then migrated, exactly once.

Awaiting the founder's word before building (permission before building, 2026-08-31).
