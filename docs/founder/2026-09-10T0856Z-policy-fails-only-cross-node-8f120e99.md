---
captured: 2026-09-10T08:56:17+00:00
session: a941270d-843c-40b9-9481-9f198a8612f1
cwd: /Users/chidionyema/dev/code/idp
chars: 1595
source: founder prompt, verbatim (founder-doc-capture.py)
---

Policy Fails Only Cross-Node
Since local policy works but cross-node policy dies, your agent is pulling exactly the right thread by checking Calico's ipset. There are only two reasons this happens in Kubernetes:

1. IP Set Desync (What the agent is checking now)
Calico enforces policies by constantly syncing lists of allowed Pod IPs (ipsets) to every node. If the Calico pod on .197 isn't receiving API updates from .221, it doesn't know the source pod's IP belongs to the allowed namespace. It defaults to DROP.

2. The SNAT Masking Bug (The Flannel Ghost returns)
If the agent's ipset dump shows the IPs are correctly synced, then the issue is Source NAT (SNAT).
When a packet leaves Node A, a misconfigured network (like having Flannel's cni0 bridge still alive) will masquerade the packet.

Node B expects the packet to come from Pod A's IP (10.244.x.x).

Instead, Flannel SNATs it, and the packet arrives looking like it came from Node A's physical IP (10.0.148.221).

Because the NetworkPolicy explicitly whitelists the Pod IP, it drops the Node IP.

What to tell the agent right now:
Wait for the agent's ipset dump to finish. Then feed it this exact prompt to close the trap:

"If the ipset contains the correct pod IPs, then the policy sync is fine, and we are dealing with SNAT masking. Check the iptables DROP logs or run a quick tcpdump on the receiving node to see if the cross-node packets are arriving with the Pod's IP or if they are being SNATted to the Node's physical IP. If they are arriving with the Node IP, Flannel's cni0 masquerade rules are assassinating our traffic."
