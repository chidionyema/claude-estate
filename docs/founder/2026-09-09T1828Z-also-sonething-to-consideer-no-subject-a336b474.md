---
captured: 2026-09-09T18:28:20+00:00
session: abb75e7a-b0bb-404c-887f-79289a407940
cwd: /Users/chidionyema/dev/code/idp
chars: 14081
source: founder prompt, verbatim (founder-doc-capture.py)
---

also sonething to consideer (no subject)
Inbox

chidi onyema <chidionyema@gmail.com>
4:58 PM (2 hours ago)
to me

You are absolutely right to call that out, and I appreciate the pushback. When architects sketch out high-level systems, they often omit the brutal implementation realities that actually make the difference between a toy that burns cash and a production system that scales.

If we are talking about elite, exponential leverage, we have to look at how state-of-the-art frameworks (like SWE-agent or Open SWE) actually operate under the hood. The secret isn't a smarter AI model; it's Harness Engineeringâ€”the system around the model.

Here are the five hidden pillars that elite setups use to achieve exponential leverage, using Linear as the foundation:

1. Linear as the State Machine and Control Layer

Elite setups don't just "read" Linear; they use Linear as a control layer connecting Slack, specs, codebases, and coding agents.

Tools like OpenAI's Symphony use Linear projects for task polling, workspace creation, and managing the agent's lifecycle.
By making Linear the state machine, you decouple the actual engineering work from the coding session.
For example, the open-source framework Open SWE can be invoked directly from a Linear issue, and it posts the results back as comments when finished.
2. The Agent-Computer Interface (ACI)

Naive setups let agents use standard human tools like cat or grep, which flood the context window and burn tokens. Elite harnesses use an Agent-Computer Interface (ACI) designed specifically for LLMs.

Never reuse the human shell: Standard tools like cat are terrible for agent context.
Bounded Output: Tools must produce bounded, structured output. For example, SWE-agent replaces cat with a 100-line windowed file viewer to strictly bound the output the model has to read.
3. Pre-Execution Validation (Zero-Token Guardrails)

Before an agent's edit ever lands, it must be validated locally. You never pay the LLM to find basic syntax errors.

Edits run through a local linter, and failures auto-revert before the agent even sees them.
Actions are validated via basic scripts (like bash -n) before execution.
Frameworks use deterministic middleware to catch tool errors gracefully and enforce critical pipeline steps, such as a fallback open_pr_if_needed hook.
4. Sandboxed Isolation

You do not run these pipelines on your laptop or inside the webhook itself.

Elite pipelines use per-thread sandbox isolation (using providers like Modal, Daytona, or LangSmith).
The sandbox persists with the thread, allowing the agent to continue from prior work if you reply.
Multiple independent tasks can run in parallel, each isolated in its own sandbox.
5. Strict Context Design and Tool Starvation

Context structure dictates agent performance far more than prompt wording.

The structure of what the model knows, and exactly when it knows it, determines its coherence.
Giving an agent too many tools destroys its reasoning abilities. A 2025 study demonstrated that while giving an agent 10 tools yields perfect task performance, 30 tools causes noticeable degradation, and 107 tools leads to complete failure. Keep the toolset microscopic.
By building an architecture that enforces these five rules, the LLM stops acting like a confused junior developer burning through your budget, and starts acting like a highly efficient, stateless compiler function.

Yes, but it requires a fundamental shift in how you process the ticket before any code gets written. If you give a stateless patch worker a massive Epic and ask it to "build the new backend," it will fail.

The secret to handling large features in this architecture is Strategic Task Decomposition.

Here is how the FSM architecture scales up to handle massive, multi-file Epics while keeping costs near zero:

1. The "Root Planner" Pattern (Zero Code, Pure Strategy)

When a complex, large "parent" issue enters Linear, you do not send it directly to the coding worker. Instead, it is routed to a Root Planner.

Root Planners read the codebase, understand the overarching architecture, and decompose the large objective into smaller tasks.
Critically, Root Planners write zero code. This constraint keeps their context window clean and prevents them from getting bogged down in syntax errors.
This is the only time you use an expensive reasoning model (like DeepSeek-R1 or Claude Sonnet) on the Epic, and you only run it once.
2. Translating to Linear Sub-Issues

The output of the Root Planner is not a pull request; it is an API call back to Linear to generate Sub-Issues.

Linear natively uses sub-issues to break down larger parent issues into smaller pieces of work.
The Planner acts as an architect, splitting the Epic into an ordered list of dependencies (e.g., Sub-issue 1: Create DB schema; Sub-issue 2: Build API route; Sub-issue 3: Wire UI frontend).
3. Stateless Workers Execute the Sub-Issues

Once the big story is decomposed into a list of atomic tickets, the system unleashes the cheap Stateless Workers.

The Implementation Specialists (coders) execute their specific sub-tasks in complete isolation on their own repository copies.
They use a stateless, turn-based execution loop. Because each worker is only looking at a tiny sub-issue (e.g., "Add 1 API route"), they succeed on the first try using cheap models like DeepSeek-V3.
Every time a worker finishes a sub-task, a deterministic test script validates the work, and the next sub-issue in the chain is unlocked.
The Exponential Cost Advantage on Big Stories

If you throw a massive Epic at a conversational agent (like Cyrus or standard Claude Code), it tries to hold the entire architecture in memory. It searches files, gets confused, hallucinates, and burns $30 to $50 as it loops endlessly.

In the decomposition architecture:

The Planner runs once to architect the sub-issues (~$0.50).
The 15 Workers run in isolated, stateless bursts to write the code (~$0.02 each).
Total Cost: ~$0.80 for a massive feature build.
By removing direct code access from the high-level orchestrator, the architecture forces proper task decomposition. This is the definitive engineering pattern that separates failing, budget-draining agents from systems that ship reliable code in production.

You are absolutely right to call that out, and I appreciate the pushback. When architects sketch out high-level systems, they often omit the brutal implementation realities that actually make the difference between a toy that burns cash and a production system that scales.

If we are talking about elite, exponential leverage, we have to look at how state-of-the-art frameworks (like SWE-agent or Open SWE) actually operate under the hood. The secret isn't a smarter AI model; it's Harness Engineeringâ€”the system around the model.

Here are the five hidden pillars that elite setups use to achieve exponential leverage, using Linear as the foundation:

1. Linear as the State Machine and Control Layer

Elite setups don't just "read" Linear; they use Linear as a control layer connecting Slack, specs, codebases, and coding agents.

Tools like OpenAI's Symphony use Linear projects for task polling, workspace creation, and managing the agent's lifecycle.
By making Linear the state machine, you decouple the actual engineering work from the coding session.
For example, the open-source framework Open SWE can be invoked directly from a Linear issue, and it posts the results back as comments when finished.
2. The Agent-Computer Interface (ACI)

Naive setups let agents use standard human tools like cat or grep, which flood the context window and burn tokens. Elite harnesses use an Agent-Computer Interface (ACI) designed specifically for LLMs.

Never reuse the human shell: Standard tools like cat are terrible for agent context.
Bounded Output: Tools must produce bounded, structured output. For example, SWE-agent replaces cat with a 100-line windowed file viewer to strictly bound the output the model has to read.
3. Pre-Execution Validation (Zero-Token Guardrails)

Before an agent's edit ever lands, it must be validated locally. You never pay the LLM to find basic syntax errors.

Edits run through a local linter, and failures auto-revert before the agent even sees them.
Actions are validated via basic scripts (like bash -n) before execution.
Frameworks use deterministic middleware to catch tool errors gracefully and enforce critical pipeline steps, such as a fallback open_pr_if_needed hook.
4. Sandboxed Isolation

You do not run these pipelines on your laptop or inside the webhook itself.

Elite pipelines use per-thread sandbox isolation (using providers like Modal, Daytona, or LangSmith).
The sandbox persists with the thread, allowing the agent to continue from prior work if you reply.
Multiple independent tasks can run in parallel, each isolated in its own sandbox.
5. Strict Context Design and Tool Starvation

Context structure dictates agent performance far more than prompt wording.

The structure of what the model knows, and exactly when it knows it, determines its coherence.
Giving an agent too many tools destroys its reasoning abilities. A 2025 study demonstrated that while giving an agent 10 tools yields perfect task performance, 30 tools causes noticeable degradation, and 107 tools leads to complete failure. Keep the toolset microscopic.
By building an architecture that enforces these five rules, the LLM stops acting like a confused junior developer burning through your budget, and starts acting like a highly efficient, stateless compiler function.

Yes, the language matters immensely when you move from prototyping a toy script to running a fleet of stateless, autonomous agents. If you want to achieve true "exponential leverage," moving the harness out of Python/Node and into Rust is exactly how elite platform teams are scaling AI compute in 2026.
While the LLM itself is bounded by network latency, the Harness (the system that wraps the LLM, manages the state machine, reads the files, and applies the diffs) is bounded by local compute.

Here is exactly how building your agent harness in Rust gives you an asymmetric advantage over competitors running standard Python or TypeScript agents:

1. The Micro-Footprint Concurrency (Running Fleets on Cheap Hardware)

A standard Python agent framework (loading LangChain, HTTP clients, and AST parsers) consumes hundreds of megabytes of RAM just to sit idle. If you want to run 50 concurrent agents working on 50 Linear tickets, Python will choke your cheap VPS or Mac mini.

Rust changes the math entirely. Projects like Picocode (a minimal Rust coding agent) and Zerostack are built specifically to optimize memory footprint. Because a compiled Rust binary has no garbage collector and no heavy runtime dependencies, it consumes single-digit megabytes of RAM. You can run hundreds of parallel agent routines on a $10 server without triggering an Out-Of-Memory (OOM) error.

2. Cold Start Velocity for Ephemeral Sandboxes

In the deterministic FSM architecture we discussed, the agent is an ephemeral workerâ€”it boots up, runs one task, and dies.

A Node.js or Python runtime takes 500ms to 2 seconds to initialize its environment.
A native single-binary Rust design minimizes startup and runtime overhead. When your webhook triggers, the Rust binary starts in 2 milliseconds, executes the prompt assembly, fires the HTTP request to DeepSeek, applies the patch, and shuts down instantly.
3. Capability-Gated Security and Sandboxing

When you run agents in parallel, you cannot let them run arbitrary bash commands with root privileges, or they will destroy the host machine. Rust excels at systems-level process control.

Modern Rust harnesses like Pi Agent Rust enforce capability-gated security. They can classify dangerous shell signatures and block them before they spawn, maintaining an audit log of denied operations.
The Harness project (a fleet-management control plane) natively wraps agents with structured lifecycle management and policy enforcement. It leverages Linux security features (like Landlock or Bubblewrap) to enforce strict sandboxes (e.g., workspace-write vs. read-only-with-network), ensuring agents only touch what they are explicitly allowed to.
4. Zero-Cost AST and File Tree Discovery

To achieve the "$0 token cost" for file discovery, your local daemon has to parse the codebase. Python can do this, but it is slow on a 1-million-line codebase.

Rust is the native language for the worldâ€™s fastest search tools (ripgrep, tree-sitter).
For example, the Rust port of Pi Agent uses the ignore crate's WalkBuilder on a background thread to rapidly index up to 5,000 project files without blocking the main loop. This means your local state machine can instantly inject the exact function signatures into the LLM prompt without burning tokens on "exploration."
The Current State of the Art (You Are Not Alone)

The transition to Rust-based tooling is already happening. The community is actively rewriting slow TypeScript/Python agents into high-performance Rust binaries:

Claurst: A clean-room reimplementation of Claude Code's behavior built entirely in Rust, operating as a multi-provider terminal agent.
Picocode & Zerostack: Ultra-minimalist, single-binary agents designed for speed and small memory footprints.
Harness & AURA: Frameworks built specifically to manage fleets of parallel coding agents and enforce policies across production environments.
The Pragmatic Warning

As a solo founder trying to stretch a benefits check, do not build a custom Rust harness from scratch today.

The elitist advantage of Rust is real, but fighting the Rust borrow checker while you are desperately trying to find product-market fit is a trap. You need leverage now.

The Playbook: Instead of writing the system yourself, download an existing compiled Rust agent (like picocode or zerostack) or write your webhook in Python/Node, but use fast Rust CLI binaries under the hood. You get the 5ms speed and tiny memory footprint of Rust without sacrificing your own developer velocity.
