---
captured: 2026-09-01T11:46:38+00:00
session: 54539261-20a7-4289-a144-e9265f1b0c43
cwd: /Users/chidionyema/dev/code/.wt-edge-dead-listeners
chars: 3357
source: founder prompt, verbatim (founder-doc-capture.py)
---

Count this as the third peer reply. The mechanism checks out: one Secret shared across listeners collapses into one Certificate whose dnsNames are the union of every hostname, and ACME orders are all-or-nothing — a single unresolvable name fails its authorization, the whole order dies, nobody gets a cert, otto included. Two dead names guarantees it. Stuck solvers on exactly the failing names is the classic signature, and the 08-27-cert-issued-after-the-08-24-redirect inference correctly eliminates the redirect. The session also named what would falsify it rather than certifying itself — which is the behaviour your rules exist to produce.

But it's convincing, not proven, and the proof lives in cluster reads only you can make:

kubectl -n <ns> get certificate prospector-edge-tls
kubectl -n <ns> get order,challenge
kubectl -n <ns> describe challenge

If the diagnosis holds, the Order is errored or pending and the challenges for the DNS-less names show lookup failures, while otto's own challenge is healthy but starved by the order. This read also settles the one loose thread in the report: it digs two names but counts three stuck solvers. If the third is otto's, expected — the whole order is wedged together. If it's a third DNS-less listener, the fix branch has to catch that one too, and nothing in the paste confirms it does.

The critical path runs through your hands twice and nobody else's: Kyverno first, if you haven't restarted it since this morning — the fix branch changes edge listeners, which is precisely the class of apply the fail-closed webhook is currently eating — then your merge word on 1b053318 under R60. After both, don't wait out cert-manager's retry backoff on the wedged Order: cmctl renew prospector-edge-tls or delete the failed Order to force a clean one with the corrected name set. Then the openssl SAN check, then 54539261 gets the Telegram door. Rate limits shouldn't bite — the failing identifiers are the ones being removed.

One decision before the merge: drop versus DNS. If alertmanager and prometheus were meant to be public, the honest fix is creating the records — though I'd push back on whether the monitoring plane belongs on the public edge at all rather than behind a port-forward or VPN. If they were speculative listeners, dropping is right and this outage did you a favour by forcing the question.

Class-level, this is the second incident in two days with the same shape: a shared control-plane object turning one bad input into estate-wide failure. Yesterday a fail-closed webhook froze every apply; today a shared-SAN certificate let two hostnames nobody uses take the Telegram money path hostage. The containment fix is splitting the edge cert — core serving names on their own Certificate, observability on another — so an experimental listener can never again poison the order that otto and prospector ride on. If the branch implements "no listener without a resolving record" as a standing rule rather than hand-deleting two names, that's the input-side class fix; worth confirming which it actually is before you bless it. And the failure ran silent from 08-30 to now — Certificate Ready=False needs to page. The two names that broke your cert were alertmanager and prometheus: the monitoring stack took down its own alarm wiring. That line belongs in the incident record verbatim.vv
