---
captured: 2026-09-06T20:37:04+00:00
session: dde713cc-8383-465a-908b-7e89c070bf22
cwd: /Users/chidionyema/dev/code/idp
chars: 2792
source: founder prompt, verbatim (founder-doc-capture.py)
---

The Gateway Timeout (504) confirms that Calico is now active and enforcing firewall rules:

Under Flannel, NetworkPolicy objects were completely ignored. Now that raw calico-node is running and Felix is active, Calico is actively enforcing the cluster's default-deny policies.

Because prospector has no entry in platform/ns-fences/allowances.yaml, Traefik (edge) is being firewalled from reaching prospector-store-web:3000. Traefik waits for the connection, gets dropped packets, and gives up with a Gateway Timeout.

1. The Root Cause: Active Policy Drops
Traefik Ingress: Runs in namespace edge.

Storefront: Runs in namespace prospector.

Policy state: The generated fence in platform/ns-fences/network/ applies an ingress default-deny on prospector. Because platform/ns-fences/allowances.yaml omits prospector, Felix drops every SYN packet from Traefik.

2. Immediate Unblock: Punch the Hole in allowances.yaml
In your working branch or repo root:

Open platform/ns-fences/allowances.yaml and add the allowance allowing edge to talk to prospector, and prospector-store-web to reach prospector-store-api:

YAML
# Add under the relevant ingress/egress blocks in platform/ns-fences/allowances.yaml:

prospector:
  ingress:
    - from:
        namespace: edge
      ports:
        - port: 3000
          protocol: TCP
    - from:
        pod: prospector-store-web
      ports:
        - port: 8080
          protocol: TCP
  egress:
    - to:
        dns: true
    - to:
        external: true  # Stripe/Postgres/storage

edge:
  egress:
    - to:
        namespace: prospector
      ports:
        - port: 3000
          protocol: TCP
Regenerate the network policies:

Bash
bin/idp-ns-fence-gen
If running via Flux / PR #2111:

Bash
git add platform/ns-fences/
git commit -m "feat(fences): allow edge ingress to prospector-store-web"
git push

# Force Flux to apply immediately
flux reconcile kustomization ns-fences --with-source
Verification: Check for Calico drop events or test Traefik connectivity immediately:

Bash
kubectl logs -n edge -l app.kubernetes.io/name=traefik --tail=20
3. Emergency Fast-Path (Test Instantly via kubectl)
If you want to verify this unblocks mumchimp.com before committing GitOps manifests, apply an emergency temporary allowance directly:

Bash
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: emergency-edge-to-prospector
  namespace: prospector
spec:
  podSelector: {}
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: edge
    ports:
    - protocol: TCP
      port: 3000
  policyTypes:
  - Ingress
EOF
Once applied, test mumchimp.com:

Bash
curl -Iv https://mumchimp.com/
Expected Result: HTTP 200 OK in under 150ms instead of a 30s 504 timeout.
