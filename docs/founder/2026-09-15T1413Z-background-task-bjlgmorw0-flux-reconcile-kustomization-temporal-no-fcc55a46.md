---
captured: 2026-09-15T14:13:00+00:00
session: 2c1fc7d2-ae84-470f-a8a6-24a80c8ea1a6
cwd: /Users/chidionyema/dev/code/idp/.claude/worktrees/fleetview-estate-map
chars: 2182
source: founder prompt, verbatim (founder-doc-capture.py)
---

Background task bjlgmorw0 (flux reconcile kustomization temporal, no --with-source, from /Users/chidionyema/dev/code/idp/.claude/worktrees/fleetview-estate-map) was launched after confirming estate-db-migrate is Ready:True and PR #3531 (unsuspend) is merged. The temporal HelmRelease has spec.upgrade.timeout: 45m (per platform/temporal/temporal.yaml comment: cold schema migrations run long). Check its output, then check current state:
- `bin/idp-kube get kustomization temporal -n flux-system -o jsonpath='{.status.conditions[?(@.type=="Ready")].status} {.status.conditions[?(@.type=="Ready")].reason} {.status.conditions[?(@.type=="Ready")].message}{"\n"}'`
- `bin/idp-kube get deploy sovereign-worker -n temporal -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'` (old tag was main-6721-339430bd8ed495f864bdacce9497edb8890c490c; any different tag means Flux applied the new kustomization.yaml)
- `bin/idp-kube get pods -n temporal` (confirm sovereign-worker pod Running/healthy, not CrashLoopBackOff; also check the HelmRelease's own pods -- temporal-frontend/history/matching/web/worker -- aren't crashing from a schema migration gone wrong)
- `bin/idp-kube get helmrelease temporal -n temporal -o jsonpath='{range .status.conditions[*]}{.type}: {.status} - {.reason} - {.message}{"\n"}{end}'`

STANDING RULE (user has repeatedly, furiously demanded this): absolutely NO intermediate chat messages. Only send ONE message when you reach a genuinely terminal state:
(a) SUCCESS: sovereign-worker's image tag changed from main-6721-339430bd... to something newer, pod is Running/healthy, Kustomization Ready:True. Report plainly as done, with the tag and pod status as evidence. This is what "fully operational" means here -- say so.
(b) BLOCKED: something genuinely failed (HelmRelease upgrade failed, pod CrashLoopBackOff, schema migration error) -- report the actual error plainly, no hedging.
If still reconciling within its normal timeout window and nothing has actually failed, stay completely silent and reschedule (noop:true if nothing changed since last check, noop:false if you learned something new like a condition transitioning even if not yet terminal).
