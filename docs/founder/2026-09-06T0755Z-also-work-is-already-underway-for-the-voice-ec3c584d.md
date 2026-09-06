---
captured: 2026-09-06T07:55:04+00:00
session: d6e854d8-9432-4f6e-9d3e-789cc41ae3ad
cwd: /Users/chidionyema/dev/code/idp
chars: 4107
source: founder prompt, verbatim (founder-doc-capture.py)
---

also work is already underway for the voice gate                                                                                                                                                  
 ────────────────────────────────────────────────────────────────────────────────                                                                                                                                                          
                                                                                                                                                                                                                                           
 Is the Rust work still relevant? Yes — here's the exact division:                                                                                                                                                                         
                                                                                                                                                                                                                                           
 - Python today = the bleed-stop and the oracle. The leak lives in a Python pipeline (Python export scripts, Python sanitizer, JSON data). You can't stop today's bleeding in Rust. And every behaviour I pinned today — EE rules, the     
   walker semantics, the cadence repair — is the reference the Rust gate must reproduce verdict-for-verdict. Nothing today is throwaway; it's the conformance suite.                                                                       
 - Rust = the product and the permanent gate. You can't sell a scattered Python module as an air-gapped enterprise sidecar. The Rust crate (already green in idp/platform/voice-gate) is what ships to clients at ~650 MB with their own   
   policy file. The Python deny module holds the line until the Rust gate matches it on all four greens, then the flag flips.                                                                                                              
                                                                                                                                                                                                                                           
 The plan from here, in order:                                                                                                                                                                                                             
 1. Merge voice-gate → deploy → the live site is clean (needs your merge or a nod to open the PR).                                                                                                                                         
 2. Phase 1 finish (hours): corpus match-set diff Python-vs-Rust + differential fuzz + golden sample vs oracle.                                                                                                                            
 3. Phase 2 (consultant-parallel): 100-string labelling + llama.cpp/candle benchmark on the OCI shape.                                                                                                                                     
 4. Phase 3: flip VOICE_GATE_IMPL=rust, delete Vale.                                                                                                                                                                                       
 5. Phase 4: GLiNER + Extism + multi-arch image — the sellable product.                                                                                                                                                                    
 6. Portal (crew#883): Lane 1 fires + your 15-minute sitting for the five, whenever you say go.                                                                                                                                            

                                                                                                 .. see update in case of any over lap,
