---
captured: 2026-09-01T11:17:17+00:00
session: a2aed3c9-7755-467b-aac8-1130e6034f41
cwd: /Users/chidionyema/dev/code
chars: 2737
source: founder prompt, verbatim (founder-doc-capture.py)
---

whats a clThe crew's read holds, and the ordering is right for a reason worth making explicit: mutate.kyverno.svc-fail is a fail-closed webhook, so with it returning EOF the API server rejects every matching apply — not just the scheduling dependency but almost certainly the cert re-issue too. Kyverno first isn't preference, it's the dependency graph.

The sequence I'd run:

Forensics before the restart — kubectl -n kyverno get pods, describe on anything restarting (OOMKilled is the usual culprit), logs --previous. If it's OOM, a bare restart buys you minutes and it'll die again mid-rollout; bump the memory limit in the same motion.
Restart the admission controller (kubectl -n kyverno rollout restart deploy/kyverno-admission-controller). If pods come up healthy and EOF persists, the caBundle in the webhook configs has gone stale across a cert rotation — delete the kyverno webhook configurations and let the controller regenerate them.
Prove admission works before trusting anything downstream: kubectl apply --dry-run=server on something trivial. Server-side dry-run exercises the webhooks; this is your same-turn measurement, not an inference.
Force Flux rather than waiting the interval: reconcile the scheduling kustomization, then hermes-agent. Gateway should roll to main-56-78e54b5.
The cert has a fork the report doesn't resolve: check whether otto.mumchimp.com is already in the Certificate's dnsNames in git (added with the Otto change, blocked from applying by Kyverno) or genuinely absent. If absent, that's a commit; if present, step 4 carries it. Force renewal with cmctl renew if cert-manager doesn't move, then verify the SAN directly: openssl s_client -servername otto.mumchimp.com -connect otto.mumchimp.com:443 </dev/null | openssl x509 -noout -ext subjectAltName.
Hand the door back to 54539261 once the leaf cert is real — clean getWebhookInfo, no last_error_message.

Break-glass, if Kyverno is properly wedged and you need the path open now: flip the webhooks to failurePolicy: Ignore or delete them. That's running the estate unguarded, which cuts against your whole lockdown posture — eyes open, revert immediately after.

By your own standard, the restart is the one-off, not the fix. The class-level question is whether a single fail-closed webhook should be able to freeze the entire apply path, cert issuance included. Either Kyverno earns that blast radius — PDB, adequate replicas, real resource headroom — or fail-closed gets scoped to the namespaces where enforcement actually matters. Worth a line in the incident record.

And the crew's still holding your marker: Control: none: at bin/idp-image-update-pr:28, or the next automated image bump fails the gate and someone hand-edits it again.
