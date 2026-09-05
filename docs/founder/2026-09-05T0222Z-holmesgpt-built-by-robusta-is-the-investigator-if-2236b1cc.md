---
captured: 2026-09-05T02:22:01+00:00
session: cd5f2d7c-ebbe-44bb-890e-833699eb6631
cwd: /Users/chidionyema/dev/code/idp
chars: 3821
source: founder prompt, verbatim (founder-doc-capture.py)
---

HolmesGPT (built by Robusta) is the "Investigator." If K8sGPT is the smoke alarm that tells you a configuration is broken, Holmes is the senior SRE that pulls the logs, reads the events, and correlates why it broke.Because Holmes physically reads your pod logs (just like we did manually for otto-gateway), it requires slightly wider read permissions than K8sGPT. If your engineers failed to set this up, it is almost guaranteed they either choked on the RBAC log-reading permissions or the default-deny network policy.Here is the exact, fail-safe sequence to deploy HolmesGPT behind your internal LiteLLM router so data never leaves your cluster.1.Grant Log-Reading RBAC:Critical for Investigation.Holmes needs to be able to fetch pod logs and events to do its job. First, we create its namespace and give its ServiceAccount the exact read-only permissions it needs across the cluster.YAMLapiVersion: v1
kind: Namespace
metadata:
  name: holmes
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: holmes-investigator
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log", "events", "services", "nodes", "namespaces"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "statefulsets", "daemonsets", "replicasets"]
  verbs: ["get", "list", "watch"]
(Apply this and bind it to a ServiceAccount named holmes-sa in the holmes namespace).2.Punch the Network Fences:1 minute.Just like before, we must explicitly allow Holmes to reach both the Kubernetes API (to read the logs) and your internal LiteLLM router (to analyze them).YAMLapiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: holmes-allow-llm-and-api
  namespace: holmes
spec:
  podSelector:
    matchLabels:
      app: holmes
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: llm
    ports:
    - protocol: TCP
      port: 4000 # Your LiteLLM port
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0 # Scope this down to your specific K8s API server IP in production
    ports:
    - protocol: TCP
      port: 443
3.Store the Internal Token:API Fencing.Give Holmes the internal LiteLLM key so your billing stays centralized and fenced.Bashkubectl create secret generic holmes-llm-secret \
  --from-literal=OPENAI_API_KEY="YOUR_LITELLM_API_KEY" \
  -n holmes
4.Deploy the Holmes Application:Helm Configuration.We deploy Holmes using its official Helm chart, but we explicitly override its brain to use your internal router via standard environment variables. It will treat your LiteLLM instance exactly like OpenAI.Save this as holmes-values.yaml:YAMLimage:
  repository: robusta/holmes

serviceAccount:
  create: false
  name: holmes-sa # Matches the RBAC from Step 1

# Override standard OpenAI vars to point to your LiteLLM router
extraEnv:
  - name: OPENAI_API_BASE
    value: "http://litellm.llm.svc.cluster.local:4000/v1"
  - name: MODEL
    value: "gemini" # Your internal lane
  - name: OPENAI_API_KEY
    valueFrom:
      secretKeyRef:
        name: holmes-llm-secret
        key: OPENAI_API_KEY
Deploy it:Bashhelm repo add robusta https://robusta-charts.storage.googleapis.com
helm repo update
helm install holmes robusta/holmes -f holmes-values.yaml -n holmes
How this changes your Day-0 ProductIf you include this in your "Day-0 AI Infrastructure" SKU, your users don't have to scramble in the terminal when a pod crashes.Instead, when an alert fires in Prometheus or Alertmanager, Holmes intercepts it, automatically pulls the last 50 lines of logs from the crashing pod, sends it through your LiteLLM router, and attaches a plain-English explanation of the failure directly to the Slack alert or your UI portal.It completely removes the intimidation factor of Kubernetes for a lean startup team.
