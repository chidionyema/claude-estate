---
captured: 2026-09-08T12:29:33+00:00
session: e5728c64-1db4-469c-9f91-941890812b9b
cwd: /Users/chidionyema/dev/code/idp
chars: 5670
source: founder prompt, verbatim (founder-doc-capture.py)
---

R0 — safety dumps (data protected before any change):                                                                                                                                                                                        
 - Estate CloudNativePG cluster: 623 MB pg_dumpall (all 15 app DBs) ✔                                                                                                                                                                         
 - Temporal: 527 KB pg_dumpall ✔                                                                                                                                                                                                              
 - Off-cluster at /Users/chidionyema/backups/estate-20260908-125420/, verified "dump complete" markers.                                                                                                                                       
                                                                                                                                                                                                                                              
 R1 — eradicate Cilium (both nodes): removed all CILIUM_* chains + cilium-feeder hooks across raw/mangle/filter/nat, deleted veths, deleted all 10 CRDs. Verified grep -ci cilium = 0 on both nodes. This was the highest-leverage step: it   
 was the cross-node/ClusterIP killer (NOTRACK), which means the work order's U1/U2 dataplane blockers are gone and R2 (open UDP 4789) is not needed. Flux reconciles recovered from 26 True toward green.                                     
                                                                                                                                                                                                                                              
 Bonus sign-in fix (F12's "no surface can be signed into"): root cause was a seed bug — put_raw stored python's trailing \n in the vault, so ESO rendered cookie_secret = "...Mo\n" = invalid TOML → oauth2-proxy CrashLoop. I re-stored the  
 trimmed vault value, forced resync, restarted, and verified oauth2-proxy 1/1 Running serving /ready 200. Durable code fix is up as PR #2574 (fix/oauth2-cookie-secret-newline), committed 91f32b29, mergeable.                               
                                                                                                                                                                                                                                              
 Tracked outstanding (per our "keep track of the other" agreement)                                                                                                                                                                            
                                                                                                                                                                                                                                              
 Recorded in the work-order file's session log:                                                                                                                                                                                               
 - R3 (flannel eradication): parked — no measured payoff while cluster works; restarting flannel-addressed stateful pods mid-recovery is risk without benefit right now.                                                                      
 - R4 (delete 47 fences): advise against — would lower security posture mid-recovery; fences now enforce correctly on Calico.                                                                                                                 
 - R5 (founder decision): you chose Option 1 (stabilize the live Calico overlay). Corrected against Oracle docs — "Calico-policy-over-flannel" is unsupported; current Calico-overlay is supported. Option 2 (VCN-native) verified as         
   cluster-creation-only → rebuild, too big for this fire; tracked as later follow-on.                                                                                                                                                        
 - R6 (guard): standing.                                                                                                                                                                                                                      
 - Current cluster state: 149/212 Running, 45 Succeeded, oauth2-proxy healthy, 1 CrashLoop = pre-existing nodesoftware-operator (the documented checkpoint bug, not caused here). Flux is in a dependency-reconcile tail; a handful of failed 
   cronjobs across dagster/otto/observability remain.                                                                                                                                                                                         
                                                                                                                                                                                                                                              
 Two PRs to merge: #2574 (seed fix, mergeable now). Want me to merge it, and then tackle the remaining dependency-cascade tail / the nodesoftware-operator pre-existing bug next?                                                             

Goal achieved (6.23M tokens)
prune: OFF (On agent message)
─────────────────────────────────────── uodate, net issut o triage is backsrage, why all work done is not shipping
