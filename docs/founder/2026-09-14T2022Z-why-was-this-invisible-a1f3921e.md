---
captured: 2026-09-14T20:22:39+00:00
session: 3991be73-91c3-4921-b29e-619826b375a7
cwd: /Users/chidionyema/dev/code/idp
chars: 1925
source: founder prompt, verbatim (founder-doc-capture.py)
---

why was this invisible 
secret-store, rbac-identity and ~38 dependent Kustomizations have sat NotReady for days, all failing on the same error: the ValidatingWebhookConfiguration for ClusterSecretStore/ExternalSecret times out at 5s against a webhook call that occasionally takes longer due to a cross-node Calico SNAT hop.
Chart hardcodes timeoutSeconds: 5 with no values.yaml knob. Raised to 15s via a postRenderers kustomize patch on both ValidatingWebhookConfigurations. failurePolicy stays Fail.
Live proof before fix
$ bin/idp-kube get kustomization secret-store -n flux-system
NAME           AGE   READY   STATUS
secret-store   19d   False   ClusterSecretStore/estate-vault dry-run failed (InternalError): ...
failed calling webhook "validate.clustersecretstore.external-secrets.io": failed to call webhook: ...context deadline exceeded
Test plan
 bin/idp-ci green on this branch
 After merge/reconcile: bin/idp-kube get kustomization secret-store,rbac-identity -n flux-system shows Ready=True
 bin/idp-kube get clustersecretstore estate-vault Ready=True
🤖 Generated with Claude Code

https://claude.ai/code/session_014Q5w3d22zwWBUVJ9R4eU1M

estate-agents Bot and others added 4 commits 24 minutes ago
@estate-agents
@claude
fix(secrets): external-secrets webhook 5s timeout too tight for cross… 
cf7ba02
@estate-agents
Merge branch 'main' into fix/external-secrets-webhook-timeout
36b048a
@estate-agents
Merge branch 'main' into fix/external-secrets-webhook-timeout
2499ae0
@estate-agents
Merge branch 'main' into fix/external-secrets-webhook-timeout
6806b47
Merge info
Some checks haven't completed yet
1 in progress, 1 skipped, 16 successful checks


in progress checks
Loading
ci / offline-gate (pull_request)
ci / offline-gate (pull_request)Started 4 minutes ago — This check has started...
Required
skipped checks
build-multiarch / merge (pull_request)
build-multiarch / merge (pull_request)Skipped 3 minutes ago
