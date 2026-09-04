---
captured: 2026-09-04T17:14:35+00:00
session: 85f840c5-baf3-4598-9496-1b3eb9dd83e9
cwd: /Users/chidionyema/dev/code/idp
chars: 6799
source: founder prompt, verbatim (founder-doc-capture.py)
---

alldone deepseek is done too                                                                                                                                                                               
                                                                                                                                                                                                                        
 Done. Built CP2 — the runtime in the cluster:                                                                                                                                                                          
                                                                                                                                                                                                                        
 Files created in platform/cyrus/:                                                                                                                                                                                      
 - kustomization.yaml — Flux-managed Kustomization                                                                                                                                                                      
 - namespace.yaml — namespace with full fence (default-deny both ways, ResourceQuota, LimitRange, DNS egress)                                                                                                           
 - deployment.yaml — Deployment with ServiceAccount, Role (read-only), RoleBinding                                                                                                                                      
 - service.yaml — ClusterIP service on port 3456                                                                                                                                                                        
 - external-secret.yaml — GitHub token from vault, Claude env (empty for Max subscription)                                                                                                                              
 - configmap.yaml — Cyrus config with 5 engines, label-based routing                                                                                                                                                    
 - httproute.yaml — Gateway route for webhooks                                                                                                                                                                          
 - pull-secret.yaml — GHCR pull secret                                                                                                                                                                                  
 - Dockerfile — Node 20 base with git, gh, jq, cyrus CLI                                                                                                                                                                
                                                                                                                                                                                                                        
 Files modified:                                                                                                                                                                                                        
 - clusters/oke/platform.yaml — Added Flux row for cyrus                                                                                                                                                                
                                                                                                                                                                                                                        
 What's not yet done (noted in PR):                                                                                                                                                                                     
 - No upstream Docker image exists — needs image workflow                                                                                                                                                               
 - OpenCode needs to connect to estate router                                                                                                                                                                           
 - Image tag is placeholder (node:20-slim with sleep)                                                                                                                                                                   
                                                                                                                                                                                                                        
 PR: #1521 — auto-merge armed                                                                                                                                                                                           
                                                                                                                                                                                                                        
 CPs remaining:                                                                                                                                                                                                         
 - CP1 — Decision record (write last, from what actually ran)                                                                                                                                                           
 - CP3 — GitHub transport identity (already in external-secret.yaml)                                                                                                                                                    
 - CP4 — Engine proof (needs running cluster)                                                                                                                                                                           
 - CP5 — Guardrails (worktrees, tool permissions)                                                                                                                                                                       
 - CP6 — Cutover                                                                                                                                                                                                        

, witing for workspace to verify bank details, lets putput dns spec for deekseek now
