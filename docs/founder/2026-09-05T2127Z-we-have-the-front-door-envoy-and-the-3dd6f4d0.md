---
captured: 2026-09-05T21:27:37+00:00
session: 2eb24bf7-c245-49bc-9398-b81dd0aaeb99
cwd: /Users/chidionyema/dev/code/idp
chars: 2235
source: founder prompt, verbatim (founder-doc-capture.py)
---

We have the front door (Envoy) and the ID badges (SPIFFE) locked down. That gives you the mathematical certainty that nobody crosses the Founder/Tenant boundary at the network level.

To keep this ultra-elite and future-proof, we now need to secure the actual room where the agents do their work. If an enterprise customer asks, "What happens if an LLM writes malicious Python code and your agent executes it?", standard SaaS architecture doesn't have a good answer. Your platform will.

Here is how we physically isolate the agent compute layer so you never have to regret running untrusted AI code on your estate:

The Vault: Agent Compute Isolation
Kernel-Level Sandboxing (gVisor or Kata Containers): Standard Docker/Kubernetes namespaces share the host kernel. That is a massive vulnerability if an agent executes a malicious script. By wrapping the agent runtime in gVisor (what Google uses for Cloud Run) or Kata Containers, each agent gets its own lightweight, isolated kernel. Even if Customer 1's agent goes rogue, it is physically trapped; it cannot see the host node, the Founder control plane, or Customer 0's memory.

Zero-Trust Egress (Cilium/eBPF): By default, tenant agents should have no internet access and no lateral movement. We use Cilium network policies set to Default Deny. If a worker agent needs to reach out to an external API or hit the estate_memory MCP tool, it must route through the Envoy Gateway, where the policy engine verifies its SPIFFE identity first.

Dedicated Node Pools: For the ultimate enterprise guarantee, the platform orchestrates distinct Kubernetes node pools. The Founder's Control Plane (God Mode) runs on isolated hardware, while Customer 0 and Customer 1 run on tenant-specific compute nodes. A CPU spike from a runaway loop in Customer 1's environment will never degrade your overarching platform dashboards.

This combination guarantees that your platform is a fortress. You can confidently onboard enterprise clients knowing their code execution is entirely walled off from your proprietary estate state.

Would you like to map out the specific Kubernetes namespace design to support this, or should we define the OPA/Cedar rules that the gateway uses to authorize these agents?
