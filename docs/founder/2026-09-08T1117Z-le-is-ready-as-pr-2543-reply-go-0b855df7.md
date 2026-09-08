---
captured: 2026-09-08T11:17:37+00:00
session: e5728c64-1db4-469c-9f91-941890812b9b
cwd: /Users/chidionyema/dev/code/idp
chars: 5344
source: founder prompt, verbatim (founder-doc-capture.py)
---

le is ready as PR #2543. Reply 'go' to merge immediately, 'hold' to review. Auto-activating in 60 minutes. Telegram 43317, pinned.

Root cause is filed as #2541 — the ten open P0: Flux cannot reconcile ... issues are one fault and none of them named it.

Also merged in the meantime: #2534, the cost work — 16 checks green, merged by estate-agents at 10:33Z. It cannot reach the cluster until the above clears.

---

The fault. Every failing Kustomization gives the same reason, a timeout to a ClusterIP:

dial tcp 10.96.202.29:80: i/o timeout      # source-controller

Not a Flux fault, and not cross-node — external-secrets and bitwarden-sdk-server sit on the same node and time out to each other identically. The Service NAT path itself is broken.

Why. Both nodes carry OKE's own marker, last-migration-failure=get_kubesvc_failure, and both CNIs are still installed and Running on both nodes — calico-node and kube-flannel-ds. Two dataplanes programming one node's rules.

What tipped it. The cni-cutover profile merged at 09:20Z (#2501) and worked: at ~10:10Z it evicted the flux-system, external-secrets and llm pods off flannel. They came back on the half-migrated dataplane and lost their Service path.

The premise that failed is in the profile's own comment — "every pod created since has come up on it, measured over the twenty youngest pods, all Calico." A pod holding a Calico address is not the same fact as a pod whose Service path works, and only the first was measured before 78 pods were moved. That sentence now sits in the file where the profile was.

Why only the profile goes. The three one-shot triggers from the same PR (spire, observability-collector, estate-db's restartedAt) are left alone on purpose: each is a fixed instant that rolls once, and removing one is itself a change that rolls it again. The profile is the only thing that keeps firing.

Why I did not just fix it. bin/idp-kube auth can-i delete pods -A, patch deployment -n kube-system and delete daemonset -n kube-system all answer no — and Flux cannot apply a git change while this is the fault, so the repository is not a road to the repair either. Finishing or reversing the CNI migration is a cluster-wide dataplane change, which is not a call a session makes alone.

One knock-on: bin/idp-set-root groq will set the repository secret fine, but the vault write and the ExternalSecret cannot land until secrets sync again. Worth doing after #2541, not before.
also 
  Ran 1 shell command

PR #2549 is merged — the generator fix is on main, so the fence regenerates with apiserver ingress from now on.

  Read 2 files, ran 7 shell commands

⏺ Background command "Watch Flux Ready count climb after the poke" completed (exit code 0)

Two real leaves left; everything else is waiting behind them. Getting the exact failure:

  Ran 2 shell commands

Fence is correct and the apiserver is 10.0.0.11. Probing the webhook directly to see whether it's policy or the pod:

  Ran 1 shell command

Kyverno's validating webhook just enforced on my probe — that path is live. Making the probe compliant:

  Ran 7 shell commands

Proven: 25 → 34 drops on the webhook pod's inbound chain during those five dry-runs. So the apiserver's real source is not 10.0.0.11. Capturing it:

  Ran 3 shell commands

No conntrack entry at all — dropped at SYN. Widening the fence briefly to learn the true source, then narrowing:

  Ran 2 shell commands

Root cause, proven: the apiserver's webhook call arrives sourced from the node's own address (src=10.0.159.197 → ClusterIP 10.96.7.232:443 → pod 10.244.3.23:10250), not from 10.0.0.11. Finding the node subnet so the fence can name it declaratively:

  Read 1 file, ran 6 shell commands

⏺ Background command "Read worker subnet lookup and search for a declared CIDR" completed (exit code 0)

Authoritative: workers subnet is 10.0.144.0/20 (workers-tiafzl). Fixing all eight namespaces live, and removing my temporary /16:

  Ran 5 shell commands

The rule is programmed but matches zero packets — so the source is in the VCN yet outside the worker subnet. Getting every subnet:

  Ran 1 shell command

cp-tiafzl = 10.0.0.8/29 — the control plane is a set of apiservers; .11 is only the service endpoint. Proving it:

  Ran 2 shell commands

Found it. src=10.244.117.0 — node A's Calico VXLAN tunnel address. The apiserver's call lands on node A, and because the single webhook replica lives on node B, Calico SNATs it across the overlay to the tunnel IP. Three observed sources, not one. Testing the exact set:

  Ran 1 shell command

Three for three. Rolling it to all eight and letting Flux run:

  Ran 1 shell command

While that runs, the durable fix in the generator:

  Ran 7 shell commands

⏺ Background command "Apply the fence fix to all eight namespaces and poke every Kustomization" completed

#2549 is on main. Building the follow-up in a clean worktree off main:

⏺ Searching for 1 pattern, running 4 shell commands…
  ⎿  $ set -o pipefail
     cd /Users/chidionyema/dev/code/idp
     WT=/private/tmp/claude-501/-Users-chidionyema-dev-code-idp/aafd9b47-da6f-44b6-a51a-b005607c8507/scratchpad/wt-webhook-callers
     git worktree add -b fix/the-fence-names-every-address-the-apiserver-arrives-as "$WT" origin/main 2>&1
     cp bin/i…

✽ Swooping… (35m 56s · ↓ 70.3k tokens) alsothis has bee onging for days noew
