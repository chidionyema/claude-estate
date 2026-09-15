---
captured: 2026-09-15T11:28:13+00:00
session: 1f9d2f2b-f2b7-4fbf-bbaf-538df8abd162
cwd: /Users/chidionyema/dev/code/idp
chars: 5800
source: founder prompt, verbatim (founder-doc-capture.py)
---

The Local Swarm Architecture

To build a zero-cost, high-asymmetry pipeline, you don't need a massive monolithic framework; you need a lightweight router and specialized local agents. The goal is to inspect every prompt and route it dynamically so your local compute is never wasted.

1. The Traffic Cop: Semantic Routing

You cannot afford to run every query through a complex agent loop. You need a router sitting in front of your models to act as a traffic cop.

LiteLLM with Semantic Routing: This proxy sits between your client and your models. It uses a small, local embedding model (like nomic-embed-text running via Ollama) to analyze the intent of the incoming prompt. It compares the prompt against predefined utterances and automatically routes the request to the correct local backend based on meaning, rather than simple keyword matching.
RouteLLM: If you prefer a simpler binary approach, this framework uses a trained classifier to route queries strictly between a "weak" (fast/cheap) model and a "strong" (heavy/slow) model based on the predicted difficulty of the request.
vLLM Semantic Router: For a more advanced, system-level intelligence layer, this router classifies requests by intent, complexity, and safety, dispatching them across a custom "Mixture-of-Models".
2. The Brains: Orchestration & Execution

Once the request is routed, you need an orchestration layer to manage the state and handoffs between your tiny specialist models.

Ollama / llama.cpp: The foundational local execution engines. You use these to run your generalist model and your specialists (like TwiL-LM3 or TRM) entirely offline.
CrewAI: Ideal for role-based agent collaboration, where agents are given specific responsibilities and tools. You use this to define your "drafter," "logic checker," and "math solver" agents.
LangGraph: If you need hardcore control, LangGraph provides graph-based workflows that support complex branching, loops, and conditional execution across your agents.
3. The Visual Playground

LLMRouter via ComfyUI: If you hate writing YAML files, LLMRouter is an open-source routing system that plugs right into ComfyUI. You can literally drag, drop, and connect nodes to build your workflow and visualize your routing pipeline in real-time.
The Tactical Playbook: Spin up LiteLLM as your local proxy. Have it use a tiny embedding model to classify incoming requests. Standard chat goes to a quantized 8B model via Ollama. If the semantic vector matches "logic" or "math," LiteLLM instantly routes it to your specialized 3B or 7M models. Total cost: $0.

Which piece of the swarm should we set up firstâ€”the LiteLLM semantic router or the local Ollama backend?

Youâ€™re chasing exponential asymmetry, and this list is the absolute bleeding edge of it. If we are talking pure parameter-to-performance ratios in hyper-specific niches, this list is currently the final boss. We are witnessing a fundamental shift away from "bigger is better" toward hyper-efficient architectures.

Can we beat this list? To do that, we have to understand exactly how these models are breaking the rules and where they critically fail.

1. The Titans of Asymmetry

The models on your list aren't just small; they are structurally optimized for specific warfare.

Samsung TRM (7M Parameters): This is the most mind-bending model here. It scores an astonishing ~45% on the notoriously difficult ARC-AGI-1 benchmark, outperforming models thousands of times its size. It achieves this through "dynamic recursion"â€”iterating its reasoning in depth (looping 1-10 times) rather than relying on a massive parameter width.
TwiL-LM3 (3B Parameters): Developed by webAI, this model is ruthlessly optimized for formal logic and deductive reasoning. It obliterates the 40x larger gpt-oss-120b on rule induction (96.4 vs 65.2) and exact-format answering. It is designed to run locally on an iPhone or MacBook.
VibeThinker-3B (Weibo): A compact 3B model that scores a staggering 94.3 on the AIME 2026 math benchmark.
2. How We Actually Beat Them

We don't beat this list by finding a 5-million parameter model that does math better. We beat them by exploiting their fatal architectural flaws:

Zero General Intelligence: Samsung TRM is a puzzle solver, but it carries no broad world knowledge and cannot compete with generalist models on everyday reasoning.
Rigid Generative Limits: TRM operates in supervised settings; it cannot generate open-ended creative text or explore multiple valid solutions like a standard LLM.
The "Expert" Bottleneck: TwiL-LM3 is brilliant at verifying logic, but even its creators note it is best used as a specialized expert or an "auto-correct for AI" alongside other models, rather than a standalone generalist.
3. The Multi-Agent Swarm

To get the ultimate asymmetric advantage for zero dollars, you don't rely on one model. Because models like TwiL-LM3 run fast on consumer hardware, you build a local swarm. You use a general open-weight model to draft the output, route the logical checks through TwiL-LM3, and pass abstract spatial tasks to TRM.

Are you ready to look into frameworks for local model orchestration to link these together?

Here is the complete list of all AI models extracted from the screenshots provided:
TwiL-LM3 / TwiL-LM (by webAI Intelligence Lab)
VibeThinker-3B
VibeThinker-1.5B
Samsung TRM (7M)
Falcon-H1R 7B
Poolside Laguna S 2.1 (118B MoE, 8B active)
Qwen3-Coder-Next (80B MoE, 3B active)
Nanbei 4.1 3B
Qwen3.8-27B (27B dense)
Gemma 4 26B (also referenced as Gemma 4 26B A4B / 26B MoE)
MiniMax M2.7
GPT-OSS-120B (OpenAI)
DeepSeek Variants:
DeepSeek V3.2 (671B / 685B)
DeepSeek R1 (671B)
DeepSeek R1-0528 distilled Qwen3 8B
DeepSeek-V4-Pro-Max (1.6T)
DeepSeek V4 Flash (284B MoE)
Other Referenced Models:
Gemini 3 Pro
Gemini 2.5 Pro
o3-mini
Qwen3-32B
