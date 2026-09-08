---
captured: 2026-09-08T00:59:38+00:00
session: 0290d925-df7f-451f-80bd-e401084880f4
cwd: /Users/chidionyema/dev/code/idp
chars: 7605
source: founder prompt, verbatim (founder-doc-capture.py)
---

what needs to be done ffor crosaplveurholding up crucisl work                                                                                                                                                                                                                                
 Original work I am tracking, not lost:                                                                                                                                                                                                       
                                                                                                                                                                                                                                              
 /Users/chidionyema/dev/code/agent-foundry on main, milestone per ORDER.md §5: order schema, one-call assembly stub, bus worker over estate NATS, price-alert army end-to-end with metering row. Eight commits in:                            
 - e602a3a Dual-Mode flip                                                                                                                                                                                                                     
 - ced3c63 foundry spine                                                                                                                                                                                                                      
 - 79d61d1 LoRA fit body (UNVERIFIED — needs HF Space run)                                                                                                                                                                                    
 - 21056ca HF Space runner config                                                                                                                                                                                                             
 - 35ed9a3 deploy_hf_space.py with audit-post + dry-run                                                                                                                                                                                       
 - d0125d5 metering merge                                                                                                                                                                                                                     
 - e567bc5 estate-DB audit post + Backstage dispatch                                                                                                                                                                                          
 - 169ac88 switch to ESO-mounted token on self-hosted runner                                                                                                                                                                                  
                                                                                                                                                                                                                                              
 Gap #3 (the live deploy): user creates HF Space, seeds Bitwarden/OCI Vault, Flux applies Kustomization, runner pod comes up, click Backstage tile. Verifies metrics.json lands in estate DB.                                                 
                                                                                                                                                                                                                                              
 Why bootstrap was the dependency: the runner pod holds the HF write token. Token must arrive as an ESO-mounted file from OCI Vault (LAW 50 + Kyverno forbid env.valueFrom.secretKeyRef). For the runner pod to mint/rotate that token        
 without a laptop, the bootstrap chain has to be one-click: bin/idp-bootstrap-estate lands agent_foundry_runner entry in OCI Vault, ESO reads it, runner pod starts. With WIF extended via Diamond Standard intent, that chain works          
 headlessly. Without it, every HF rotation is a laptop hand.                                                                                                                                                                                  
                                                                                                                                                                                                                                              
 What I will do once you decide:                                                                                                                                                                                                              
                                                                                                                                                                                                                                              
 1. Resolve the bootstrap dependency (your three questions). Lean toward extending Diamond Standard, not introducing Crossplane — the decision record closes that.                                                                            
 2. Feed the agent-foundry post: write the hf-fleet-train.yml workflow the same shape as estate-bootstrap.yml (OIDC + WIF), so HF Space deploys are one click. Verify metrics.json lands in task_executions (the metering table already       
    wired). Confirm agent_foundry_runner ESO secret survives a pod restart.                                                                                                                                                                   
 3. Checkpoint every dependency: runner pod health → ESO refresh → OCI Vault write → bin/idp-root-trust --check green → task_executions row. Kill switch if any leg goes red. Pull request against main, not a direct push.                   
 4. Verify the LoRA fit body end-to-end on the HF Space (79d61d1 is UNVERIFIED). The closed-vocabulary {none, aws_access_key, aws_secret_key, github_pat, google_api, slack_token} classifier must beat the majority baseline.                
                                                                                                                                                                                                                                              
 Three decisions I need from you, plain:                                                                                                                                                                                                      
                                                                                                                                                                                                                                              
 1. Diamond Standard extension stays the path, or revisit the 2026-09-01 decision and bring in Crossplane?                                                                                                                                    
 2. Bootstrap extension in scope this turn (intent schema + emitter + Tailscale proof), or defer?                                                                                                                                             
 3. estate-bootstrap.yml mode=estate-seed stays the OCI half while we wire WIF, or we block on all four vendor halves before any cloud-side live run?
