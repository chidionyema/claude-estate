---
captured: 2026-09-10T09:01:26+00:00
session: a941270d-843c-40b9-9481-9f198a8612f1
cwd: /Users/chidionyema/dev/code/idp
chars: 1859
source: founder prompt, verbatim (founder-doc-capture.py)
---

n Flannel out of the root of your estate once and for all, permanently killing the bug.The Permanent Eradication SequenceGive your agent this exact remediation playbook to execute right now via break-glass:1. Purge the Flannel Iptables RulesYou must explicitly flush the leftover masquerade rules that Flannel injected into the host's kernel before it was uninstalled:Bash# Run on both nodes (.197 and .221)
iptables -t nat -D POSTROUTING -s 10.244.0.0/16 ! -d 10.244.0.0/16 -j MASQUERADE 2>/dev/null || true
iptables -t nat -D POSTROUTING -m comment --comment "flannel mask" -j MASQUERADE 2>/dev/null || true
2. Obliterate Dead Network InterfacesFlush the ghost bridges that Flannel left behind, which are actively hijacking the routing table:Bash# Run on both nodes
ip link set cni0 down 2>/dev/null || true
ip link delete cni0 type bridge 2>/dev/null || true
ip link set flannel.1 down 2>/dev/null || true
ip link delete flannel.1 type vxlan 2>/dev/null || true
3. Enforce Calico CNI OwnershipEnsure the Kubernetes kubelet on both nodes is strictly bound to Calico and cannot fallback or look for Flannel:Bash# Force the kubelet network plugin config to explicitly point to Calico
sed -i 's/networkPlugin: flannel/networkPlugin: cni/g' /var/lib/kubelet/config.yaml 2>/dev/null || true
systemctl restart kubelet
4. Hard-Reset the Calico DataplaneNow that the SNAT mask is gone and the ghost bridges are dead, bounce the Calico nodes so they re-establish a clean VXLAN tunnel without interference:Bashbin/idp-kube rollout restart daemonset -n kube-system calico-node
The Architectural TakeawayAdd this to your estate's immutable laws: Never run two CNI binaries on the same node. Even after a DaemonSet is deleted, CNI plugins leave kernel-level scars (iptables rules and bridge interfaces) that will silently assassinate your cross-node traffic weeks later.
