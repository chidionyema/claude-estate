---
captured: 2026-09-09T22:47:43+00:00
session: a941270d-843c-40b9-9481-9f198a8612f1
cwd: /Users/chidionyema/dev/code/idp
chars: 1683
source: founder prompt, verbatim (founder-doc-capture.py)
---

We already know exactly what is causing the LiteLLM 504 epidemic: the router is configured to wait on a dead signoz-otel-collector before returning the LLM's response.

Let's kill the root cause right now so your primary data plane breathes again.

The Immediate LiteLLM Fix (Rip Out Tracing)
Because your estate runs on GitOps (Flux), you need to remove the otel callbacks from the configuration and push it, then bounce the pod so it picks up the clean config.

Run this exact sequence in your terminal to strip the observability blockers out of LiteLLM:

Bash
# 1. Remove the otel callbacks from the config file (macOS sed syntax)
sed -i '' '/success_callbacks: \[.*otel.*\]/d' platform/llm/config.yaml
sed -i '' '/failure_callbacks: \[.*otel.*\]/d' platform/llm/config.yaml
sed -i '' '/callbacks: \[.*otel.*\]/d' platform/llm/config.yaml

# 2. Commit and push to main so Flux sees it
git add platform/llm/config.yaml
git commit -m "fix(llm): emergency removal of blocking otel collector callbacks"
git push origin main

# 3. Force Flux to reconcile immediately (if you have the flux CLI)
# flux reconcile kustomization llm --with-source

# 4. Bounce the LiteLLM deployment to load the clean config
bin/idp-kube -n llm rollout restart deploy/litellm
What Happens Next
The moment that new LiteLLM pod spins up, it will stop trying to talk to the dead SigNoz collector. The 10-second blocking timeouts will vanish. The 504s will instantly drop to zero, and every agent in your estate (including Otto) will regain access to Anthropic and DeepSeek.

Run those commands, verify the router is returning 200s, and then we can talk about wiring the Mac fallback so it never happens again.
