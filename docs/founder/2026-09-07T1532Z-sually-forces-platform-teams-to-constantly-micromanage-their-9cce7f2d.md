---
captured: 2026-09-07T15:32:21+00:00
session: edea3807-332a-47d0-9ddc-1e9e05ad81fd
cwd: /Users/chidionyema/dev/code/idp
chars: 2791
source: founder prompt, verbatim (founder-doc-capture.py)
---

sually forces platform teams to constantly micromanage their AI.

Autonomy doesn't mean giving an agent raw root access to production so it can cowboy-code live infrastructure. True autonomy means the agent can complete the entire lifecycle of a problem—from detection to resolution—while you are asleep, without waking you up, and without breaking the system.

Here is how the agent works fully autonomously inside this framework:

The "Greenlane" (Automated Auto-Merge)
For 90% of daily operational toil, you configure your CI/CD pipeline with a Trust Threshold. If the agent's Pull Request meets the criteria, the system auto-merges it and deploys it immediately, with zero human intervention.

The agent is allowed to act autonomously if it satisfies the Proof Contract:

Scope Check: The change affects a low-risk layer (e.g., rotating a secret, increasing a pod memory limit, rolling back a single deployment, fixing a misconfigured ConfigMap).

Test Pass: The agent's PR includes a passing CI trace from the vcluster proving the fix worked and didn't crash the pod.

Autonomous Execution: A bot (like Renovate or a custom GitHub action) reads the proof, approves the PR, and merges it. Flux pulls it into production instantly.

Example: The 3:00 AM Memory Leak

Observation: Prometheus fires an OOMKill (Out of Memory) alert.

Action: The agent wakes up, clones the prod state into a vcluster, increases the memory limit for the failing pod, and verifies it starts successfully.

Handoff: The agent opens a PR labeled type: auto-remediation.

Autonomy: The CI pipeline sees the vcluster test passed, auto-merges the PR, and ArgoCD applies it to production. The pod is fixed. You sleep through the whole thing and just read a Slack summary in the morning.

The "Glass-Break" (Human-in-the-Loop)
The only time the agent loses autonomy and waits for you is when it tries to touch the Core Blast Radius.

If the agent decides it needs to upgrade the Kubernetes control plane, change a cluster-wide NetworkPolicy, or alter the core ingress routing, the system halts the auto-merge.

Even then, the agent is doing 99% of the work. It diagnosed the issue, tested the fix, and wrote the code. It is simply presenting you with the finished, proven solution. You don't have to SSH into anything or write any YAML; you just review the test logs and click "Approve."

Summary
By forcing the agent to output its work as Git Pull Requests accompanied by vcluster test proofs, you aren't removing its autonomy—you are weaponizing its autonomy. You are giving it a mathematically safe playground where it can move as fast as it wants, while the GitOps pipeline acts as the bouncer to production.

To turn this on, we just define the Trust Threshold. What is the agent allowed to auto-merge right now?
