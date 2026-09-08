---
captured: 2026-09-08T09:59:13+00:00
session: df632781-7339-41d3-b1d3-d2b55c6e63a2
cwd: /Users/chidionyema/dev/code/idp
chars: 11134
source: founder prompt, verbatim (founder-doc-capture.py)
---

reviw na dinvestigate what eeds to be done Brilliant. Since you already have LiteLLM as your routing layer, we’re going to turn it into a spend‑aware, multi‑provider, free‑first, never‑down money machine. The goal: extract every free token possible, then fall back to ultra‑cheap paid tiers, all within a hard £150/month, with zero downtime.

Here’s the full battle plan.

---

1. The Core Principles

· Free first, always – route to free providers until their rate limits are exhausted.
· Cheap paid second – use ultra‑cheap providers (SiliconFlow, DeepInfra, etc.) for overflow.
· Hard cap enforced at three levels – provider account, virtual card, LiteLLM budget.
· Graceful degradation – when all paid is gone, the factory keeps running on free tiers, even if slower.
· Prefix caching everywhere – identical system prompts and repo context across all agents to make input tokens nearly free.

---

2. Phase 1: Harvest Every Free Credit

2.1 Free API Providers with Frontier Open Models

Sign up for all of these. They’re free, no credit card required (unless noted). Each gives you a monthly/daily quota of requests or tokens.

Provider Free Tier Models (Frontier Open Weights) Free Limit (approx) API Endpoint Notes
Groq Llama 3.3 70B, Qwen2.5‑Coder‑32B, DeepSeek‑R1‑Distill‑Llama‑70B 14,400 requests/day, 30 req/min https://api.groq.com/openai/v1 Fastest free tier, but strict RPM.
Cerebras Llama 3.1 70B, Qwen2.5‑Coder‑32B 1M tokens/day (soft), 30 req/min https://api.cerebras.ai/v1 Very fast, generous tokens.
Cloudflare Workers AI Llama 3.1 8B/70B, Qwen2.5‑Coder‑7B/32B, DeepSeek‑R1‑Distill 10k neurons/day (≈1M tokens) https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/ Requires Cloudflare account, but free.
Google AI Studio Gemma 2 27B, Gemma 3 27B (open weights) 15 RPM, 1,500 requests/day https://generativelanguage.googleapis.com/v1beta/ Not Llama/Qwen, but open‑weights and capable.
Hugging Face Inference Many open models (Llama, Qwen, etc.) ~300 free credits/month (≈$0.10) https://api-inference.huggingface.co/models/ Limited, but useful for small tasks.
Together AI Llama 3.3 70B, Qwen2.5, DeepSeek‑R1‑Distill $1 free credit on signup https://api.together.xyz/v1 One‑time, but can add to pool.
Fireworks AI Llama 3.3 70B, Qwen2.5 $1 free credit https://api.fireworks.ai/inference/v1 One‑time.
DeepInfra Llama 3.3 70B, Qwen2.5‑Coder‑32B $1.50 free credit https://api.deepinfra.com/v1/openai One‑time.
OpenRouter Free models (Llama, Qwen, etc.) $1 free credit + some free models https://openrouter.ai/api/v1 Some models are marked “:free”.
Mistral (La Plateforme) Mistral 7B/8x7B/8x22B (open) Free tier with low rate limits https://api.mistral.ai/v1 Good for small tasks.
NVIDIA NIM Llama 3.1 70B, Qwen2.5 1,000 free API credits https://integrate.api.nvidia.com/v1 One‑time.

Action:
Create accounts, generate API keys, and store them securely. You’ll add them all to LiteLLM.

---

3. Phase 2: Cheap Paid Providers (Overflow)

These are pay‑per‑token but so cheap that £150 goes a long way. Order by cost for frontier open models.

Provider Example Models Input $/1M Output $/1M Notes
SiliconFlow DeepSeek‑V3, Qwen2.5‑Coder‑32B, Llama 3.3 70B $0.05 – $0.14 $0.20 – $0.40 Extremely low, good concurrency.
Novita AI Llama 3.3 70B, Qwen2.5 $0.10 – $0.20 $0.20 – $0.50 Cheap, reliable.
DeepInfra Llama 3.3 70B, Qwen2.5‑Coder‑32B $0.12 – $0.25 $0.30 – $0.60 Good performance, prefix caching.
Together AI Llama 3.3 70B, Qwen2.5, DeepSeek‑R1‑Distill $0.20 – $0.40 $0.60 – $1.00 Higher but still manageable.
Fireworks AI Llama 3.3 70B, Qwen2.5 $0.20 – $0.30 $0.40 – $0.80 Fast.
Groq (paid) Llama 3.3 70B, Qwen2.5 $0.59 – $0.79 $0.79 – $0.99 Very fast, but pricier.

Recommendation:
Use SiliconFlow as primary paid because it’s cheapest and supports prefix caching. Add DeepInfra as secondary paid.

---

4. Phase 3: LiteLLM Orchestration – The Ultimate Config

You’ll configure LiteLLM with:

· All free providers as high‑priority, limited models.
· Cheap paid providers as overflow.
· Budget routing to hard‑stop paid calls at £150.
· Automatic fallback to free when paid is exhausted.

4.1 Basic Model List

```yaml
model_list:
  # Free providers first (highest priority)
  - model_name: groq-free
    litellm_params:
      model: groq/llama-3.3-70b-versatile
      api_key: ${GROQ_API_KEY}
      rpm: 30
      tpm: 6000
  - model_name: cerebras-free
    litellm_params:
      model: cerebras/llama3.1-70b
      api_key: ${CEREBRAS_API_KEY}
      rpm: 30
      tpm: 1000000
  - model_name: cf-workers-free
    litellm_params:
      model: openai/llama-3.1-70b-instruct
      api_base: https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/v1
      api_key: ${CF_API_TOKEN}
      rpm: 100
      tpm: 1000000
  - model_name: gemini-free
    litellm_params:
      model: gemini/gemma-2-27b-it
      api_key: ${GOOGLE_AI_STUDIO_KEY}
      rpm: 15
      tpm: 1000000

  # Cheap paid providers (overflow)
  - model_name: siliconflow-paid
    litellm_params:
      model: openai/deepseek-v3
      api_base: https://api.siliconflow.cn/v1
      api_key: ${SILICONFLOW_API_KEY}
      rpm: 500
      tpm: 10000000
  - model_name: deepinfra-paid
    litellm_params:
      model: openai/meta-llama/Llama-3.3-70B-Instruct
      api_base: https://api.deepinfra.com/v1/openai
      api_key: ${DEEPINFRA_API_KEY}
      rpm: 200
      tpm: 5000000
```

4.2 Routing Strategy with Budget and Fallbacks

LiteLLM’s usage-based-routing-v2 can route based on cost and budget. But we need custom priority and fallback chain. Use router_settings with fallbacks and context_window_fallbacks.

```yaml
router_settings:
  routing_strategy: usage-based-routing-v2
  budget: 150                # £150 hard budget (LiteLLM uses USD; set 150 USD ~ £120, adjust)
  soft_budget: 0.9           # at 90% budget, start shifting to free
  fallbacks:
    - siliconflow-paid: [groq-free, cerebras-free, cf-workers-free, gemini-free]
    - deepinfra-paid: [groq-free, cerebras-free, cf-workers-free, gemini-free]
    - groq-free: [cerebras-free, cf-workers-free, gemini-free]
    - cerebras-free: [cf-workers-free, gemini-free]
  enable_pre_call_checks: true
  allowed_fails: 3
  cooldown_time: 30
```

Explanation:

· The router first tries the cheapest paid model (siliconflow‑paid).
· If the budget soft limit is reached, it will automatically route new requests to free models.
· If a free model rate limit hits, it falls back to the next free model.
· If all free models fail, it will go back to paid (if budget remains) or eventually error. To prevent total stop, we can set a catch‑all free provider last, but with many free providers, chance of all failing simultaneously is low.

Important:
LiteLLM’s budget tracking is in USD by default. Set budget: 150 and then multiply by exchange rate (approx $190 for £150). Or use a custom callback to track exact £.

4.3 Custom Spend Tracking in £

If you want exact £150, use LiteLLM’s callbacks or custom middleware to track cumulative spend in GBP. Simpler: set budget to 190 USD and accept slight over/under. Or use a virtual card with £150 limit as ultimate backstop.

---

5. Phase 4: Optimization – Squeeze Every Token

5.1 Maximise Prefix Caching

· Keep system prompt, repo map, tool schemas identical across all agents.
· In LiteLLM, ensure caching: true is enabled for providers that support it (DeepSeek, SiliconFlow, DeepInfra).
· Place the static prefix at the very beginning of the prompt.

5.2 Split Workload by Complexity

Use different model tiers:

· High complexity (multi‑step reasoning, code generation): Llama 3.3 70B, DeepSeek‑R1‑Distill, Qwen2.5‑Coder‑32B.
· Low complexity (commit messages, file summaries, test names): Gemma 2 9B/27B, Llama 3.1 8B, Qwen2.5‑Coder‑7B.

In LiteLLM, define separate model names for simple tasks and route them to free small models first, e.g.:

```yaml
- model_name: simple-task
  litellm_params:
    model: groq/llama-3.1-8b-instant
    api_key: ${GROQ_API_KEY}
    rpm: 60
    tpm: 100000
```

5.3 Set Token Limits

Set max_tokens per request to avoid runaway output:

· For code generation: 2048–4096.
· For simple tasks: 256–512.

5.4 Use Streaming

Streaming reduces perceived latency and allows early stopping.

---

6. Phase 5: Hard Kill Switches (No Bill Shock)

Even with LiteLLM budget, enforce at lower levels:

1. Prepaid account with no auto‑reload on SiliconFlow/DeepInfra.
2. Virtual card (Revolut, Wise, Privacy.com) with exactly £150 monthly limit.
3. LiteLLM budget at $190 (or £150 equivalent) – stops paid calls.
4. Alerts at 70% and 90% via email/webhook.

LiteLLM config for alerts:

```yaml
general_settings:
  alerting: ["slack"]
  alerting_threshold: 0.7   # alert when budget 70% used
```

---

7. The Final Routing Flow

1. Agent calls your LiteLLM endpoint with a model like orchestrator.
2. LiteLLM checks remaining budget:
   · If budget > 90% remaining → route to siliconflow-paid (cheapest paid) for high complexity, simple-task for low.
   · If budget between 90% and 100% used → route high complexity to deepinfra-paid (slightly more expensive but still within cap) and low to free small models.
   · If budget exhausted (100%) → route all traffic to free providers (groq-free, cerebras-free, cf-workers-free, gemini-free) in order. Agents continue, just slower.
3. If a free provider hits rate limit, LiteLLM automatically falls to next free provider.
4. When the month resets, budget resets, and paid is available again.

---

8. Expected Performance

With 7 agents and efficient caching:

· Free tier capacity: Groq (14k req/day ≈ 600 req/hour) + Cerebras (1M tokens/day) + Cloudflare (1M tokens/day) + Gemini (1,500 req/day) can easily cover 30–50% of your traffic, especially low‑complexity tasks.
· Paid overflow: The remaining 50–70% of traffic uses SiliconFlow at ~3–5/day ≈ £90–150/month.
  With caching and small‑model offload, you can likely stay under £100.

Bottom line: You’ll extract every free token, keep total cost under £150, and never experience total downtime because free tiers act as an infinite (but rate‑limited) buffer.

---

9. Implementation Checklist

1. Sign up for all free providers and generate API keys.
2. Add cheap paid providers (SiliconFlow, DeepInfra) and deposit small amounts.
3. Set up virtual card with £150 limit for paid providers.
4. Configure LiteLLM with the YAML above, adjust model names and keys.
5. Enable prefix caching in your agents’ prompt structure.
6. Create a small‑model route for simple tasks.
7. Set alerts for budget usage.
8. Test failover by exhausting a free provider’s rate limit manually.
9. Monitor the first week; adjust RPM/TPM limits and model priorities.

---

This is the ultimate solution: free credits first, ultra‑cheap paid second, hard budget enforced, graceful degradation, and zero downtime. You now have a plan to run a 24/7 7‑agent software factory on frontier open models for less than £150/month, with no anxiety.

Want me to generate a complete config.yaml file with all the providers and model list ready to drop into your LiteLLM setup? I can also provide a Python script to auto‑rotate API keys if needed.
