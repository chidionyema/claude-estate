---
captured: 2026-09-06T15:55:01+00:00
session: 8d04d4f4-9226-4a98-ac41-37c887c03441
cwd: /Users/chidionyema/dev/code/idp
chars: 5780
source: founder prompt, verbatim (founder-doc-capture.py)
---

mumchimp.com is down because the edge gateway terminates TLS cleanly, but the upstream backend (prospector-store-web:3000 in the prospector namespace) never responds, resulting in Envoy timing out after 25 seconds (exit code 124).

The issue is isolated between the gateway and the prospector namespace.

Root Cause Breakdown
The Route Target: As shown in the HTTPRoute table, mumchimp.com and [www.mumchimp.com](https://www.mumchimp.com) route exclusively to:

Plaintext
prospector/prospector-store-web: ["mumchimp.com","www.mumchimp.com"] -> prospector-store-web:3000
Why it hangs instead of rejecting:

Network Fence / Allowances Drop: If a network policy or Calico rule was applied without an explicit allowance from the gateway namespace to prospector on port 3000, the packets are silently dropped (leading to a 25s timeout rather than an immediate 502 Connection Refused).

Pod Deadlock / Crashed Backend: The prospector-store-web pod is either in a CrashLoop, not scheduled, or blocked waiting on a deadlocked connection to prospector-store-api:8080 / external database.

Verification Commands
Run these in your shell to pinpoint the exact failure inside prospector:

Bash
# 1. Check if prospector-store-web pods exist and are Ready
kubectl get pods -n prospector -o wide

# 2. Check if the Service has healthy Endpoints
kubectl get endpoints -n prospector prospector-store-web

# 3. Check container logs for unhandled exceptions or blocked downstream connections
kubectl logs -n prospector deploy/prospector-store-web --tail=50

# 4. Check if the namespace has an active default-deny ingress policy
kubectl get netpol -n prospector
If endpoints is <none>: The pods failed their readiness probes or crashed.

If pods are Running but netpol exists: Traffic from the gateway to port 3000 is blocked by missing ingress rules in platform/ns-fences/allowances.yaml.

Note on the Terminal Hook Timeout
Plaintext
UserPromptSubmit hook timed out after 10s — output discarded. Raise the hook's "timeout" to allow more time.
Your Claude Code / agent runner ran a pre-submit validation hook (evaluating git state or waiting for background tasks) that stalled on the cluster or git locks.

The background PR creation (gh pr create ... wt-fence) is still running in the background.

Once the prompt releases or finishes "Infusing", confirm whether the PR was created with gh pr list --limit 3. 4. The 07:56 survivor will be terminated on the next roll because of rolling update defaults
If maxUnavailable is default (25% or 1) or if the deployment is patched, Kubernetes will eventually schedule a termination signal to the old pod if a rollout gets forced, or if the node experiences memory pressure. Furthermore, Node/Express defaults trust proxy to false—so even if the gateway sends X-Forwarded-For, Cyrus discards it and validates req.socket.remoteAddress (which is Envoy's internal pod IP 10.244.x.x), failing GitHub's CIDR check every time.

Emergency Triage Sequence
Do these in exact order: freeze the death loop first, unblock egress second, fix the webhook last.

Step 1: Freeze Reloader (Stop the 10-Minute Rolling Death Loop)
Strip the Reloader annotation from the cyrus deployment right now so the 10-minute secret rotation does not trigger revision 290 and kill your running survivor:

Bash
# Strip auto-reload annotations immediately
kubectl annotate deploy cyrus -n cyrus reloader.stakater.com/auto-
kubectl annotate deploy cyrus -n cyrus secret.reloader.stakater.com/reload-

# Verify revision churn has stopped
kubectl get deploy cyrus -n cyrus -o jsonpath='{.metadata.annotations}'
Verification: Wait 10 minutes past the next token re-mint. Confirm kubectl rollout history deploy/cyrus -n cyrus remains on revision 289.

Step 2: Unblock Egress to GitHub (Fix Item 2)
Replacement pods crash because git clone times out over port 443 / 22. Punch an explicit egress allowance for the cyrus namespace:

Bash
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-github-egress
  namespace: cyrus
spec:
  podSelector:
    matchLabels:
      app: cyrus
  policyTypes:
    - Egress
  egress:
    # Cluster DNS
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
    # GitHub HTTPS and SSH
    - to:
        - ipBlock:
            cidr: 0.0.0.0/0
      ports:
        - protocol: TCP
          port: 443
        - protocol: TCP
          port: 22
EOF
Verification: Exec into the survivor pod and test network reachability directly:

Bash
kubectl exec -n cyrus deploy/cyrus -c cyrus -- nc -zv github.com 443
# Must output: Connection to github.com 443 port [tcp/https] succeeded!
Once this exits 0, new replacement pods will successfully complete their startup clone.

Step 3: Neutralize the Webhook IP Check (Fix Item 1)
Because Cyrus is packaged as a Node/TypeScript distribution (dist/):

Check the upstream config file: Look at /var/lib/cyrus/config.json or whatever config volume is mounted. In Cyrus upstream, inspect if there is an explicit toggle:

JSON
{
  "webhooks": {
    "validate_ip": false,
    "trust_proxy": true
  }
}
If it is hardcoded in Node.js: If 0.2.71 runs Express without app.set('trust proxy', true):

In the Gateway/Envoy: Ensure Envoy is configured with use_remote_address: true and preserves client IP via X-Forwarded-For.

In the Entrypoint Wrapper (PR #1954): If the IP check is an inline function in dist/, set the environment variable TRUST_PROXY=true or patch the entrypoint wrapper to sed-replace the IP validation check to return true at runtime, leaving the HMAC X-Hub-Signature-256 as the sole cryptographic control.
