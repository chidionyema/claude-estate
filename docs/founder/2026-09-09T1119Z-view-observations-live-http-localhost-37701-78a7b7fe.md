---
captured: 2026-09-09T11:19:06+00:00
session: f4d67c6c-f2e7-45b3-aa66-d929ca80fca0
cwd: /Users/chidionyema/dev/code/idp
chars: 4757
source: founder prompt, verbatim (founder-doc-capture.py)
---

View Observations Live @ http://localhost:37701
✨ Get up to 100% more usage from your plan — memory runs off-plan, free for 30 days https://cmem.ai/pro?from=session-start&trial=30

Pinning the 504s to the LiteLLM chat-completion path now: reading the gateway timeout and the router's own log for those minutes.

  Ran 6 shell commands

Writing up the root cause now. No further probes needed.

INVENTORY: the 504s are the LLM router pod on node .221 hanging every request since 10:35Z, because that node lost pod-to-pod reach to the other node when OKE re-rolled flannel at 10:34Z on top of Calico's own VXLAN overlay.

Built: read-only root-cause read, nothing changed.
Use: nothing yet; a fix needs your go-ahead.
Expect: half of all llm.mumchimp.com calls (whichever land on pod litellm-77f5fbf88d-g7bq9) time out until that pod, or the double overlay, is
dealt with.
Not done: no fix applied, per your order. Why OKE rolled flannel to revision 3 is unverified.
Evidence: ~/.claude/docs/founder/2026-09-09T1054Z-memory-8393eaa7.md; log quotes below.

---

What your request hit. Traefik round-robins across two LiteLLM pods. The pod on node .197 served normally in the last 15 minutes. The pod on node
.221 answered zero completions and refused 379 requests with "No deployments available for selected model" for gemini, minimax, minimax_m27,
deepseek and default. Its Redis cache pod lives on .197 and has been unreachable since 10:35:02Z:

litellm-77f5fbf88d-g7bq9  redis-breaker  first 10:35:02  last 11:13:31
Exception: Redis circuit breaker is open — skipping async_batch_get_cache   (3423 times)

The other pod has none of those lines. A request that lands on the sick pod waits through LiteLLM's retries, Traefik gives up at 30s or 60s, and the friendly-errors middleware paints the "starting up" page. That is why it looks like a platform outage and why retries fail three times in a row.

Why .221 lost the other node. Two overlay networks are configured for the same pod range. Calico runs with CALICO_IPV4POOL_VXLAN=Always and FELIX_VXLANENABLED=true on 10.244.0.0/16, and OKE's flannel runs VXLAN on the same range. At 10:34:22Z and 10:34:28Z OKE recreated both flannel pods (DaemonSet revision 3, no change-cause). Node .221 flipped NetworkUnavailable at 10:34:32Z and the Redis breaker opened 30 seconds later. Two controllers writing cross-node routes for one CIDR is the class of defect; the flannel roll was the trigger.

What made it worse, not the cause. Both LiteLLM pods loggedfor two minutes, 10:30:23Z to 10:32:13Z, during the
preemption storm. Cron pods at platform-batch and infrastructure-critical priority preempted OKE's node agents, external-dns, kyverno and otherat 10:26 and 10:29 to 10:31; node .197 sits at 96 percent od internet works again from both nodes now: the fast lane
returned 200 34 and 36 times in four minutes on each pod.                                                                                      
Still failing, related. external-dns on .221 dies with dial tcp 104.19.192.176:443: i/o timeout to Cloudflare. external-secrets on .221 cannot reach Bitwarden. Flux is stuck on the edge → priority-classthing self-heals.
                                                                                                                                               What the killed runs were doing. Two pi headless runs of Desection 11 (OpenCode harness plugin) and section 12
(free-token pipeline). Section 12 changed nothing. Section 11 left six uncommitted files in the scratchpad worktree wt-ds11. Nothing was pushed
The one fix I would make, with your permission: delete the sick router pod for immediate relief, then put Calico in policy-only mode so flannelthe only overlay.
                                                                                                                                                 Worked for 20m 2s · done 12:15 · 1 monitor still running
                                                                                                                                                 Monitor event: "idp#2778 and claude-guards#264 checks compl
                                                                                                                                                 WAITING: nothing new from you yet. The check-monitor for clout; that pull request stays open and unmerged, and I am not
re-arming or acting on anything without your say-so.                                                                                           
The root-cause answer above stands. The next move is yours: allow the sick router pod delete plus the Calico policy-only change, or tell me to hold.

✻ Cooked for 24s · done 12:17 · 1 monitor still running
