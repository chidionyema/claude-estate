---
captured: 2026-09-06T21:32:24+00:00
session: dde713cc-8383-465a-908b-7e89c070bf22
cwd: /Users/chidionyema/dev/code/idp
chars: 4700
source: founder prompt, verbatim (founder-doc-capture.py)
---

The jump from a static workflow runner to a bleeding-edge, System-2 reasoning agent requires moving from "prompt-and-pray" to Test-Time Compute (TTC) scaling combined with Process Verification.

Recent literature from late 2025 and 2026 (including the architectures behind OpenAI's o1, DeepSeek-R1, and models like Frontis-MA1) establishes that true autonomous coding capabilities rely heavily on Asymmetric Architectures and Process Reward Models (PRMs).

Here is the technical blueprint to build this on your OKE cluster.

1. The Core Architecture: Asymmetric Two-Stage Reasoning (A2R)
Instead of a single massive model trying to generate the perfect patch in one shot, SOTA implementations split the agent into two distinct roles to optimize compute efficiency and reasoning depth.

The Explorer (Generator): A smaller, faster model (e.g., Llama-3-8B or Qwen-2.5-Coder) deployed on OKE. Its job is purely divergent search. When given a ticket, it generates 5 to 10 different possible reasoning paths and code patches in parallel.

The Synthesizer (Judge/Refiner): A much larger, highly capable model (e.g., Claude 3.5 Sonnet or DeepSeek-Coder-V2) that acts as the "System 2" brain. It reviews the outputs of the Explorer, looks at the execution results (test passes/fails), and synthesizes the optimal final patch.

Why this works: It is an asymmetric scaling paradigm. Generating tokens is cheap; high-level reasoning is expensive. You scale test-time compute by parallelizing the cheap Explorer, then use the expensive Synthesizer only to judge and combine the best ideas.

2. The Search Algorithm: Monte Carlo Tree Search (MCTS)
A SOTA agent does not just iterate on a linear chain of thought. It builds a decision tree of code edits.

Node Representation: Each node in the tree is an intermediate state of the codebase.

Expansion: The Explorer model proposes multiple edits (branches) from the current state.

Simulation & Execution: Each branch is compiled and tested inside your isolated Kata Container sandboxes.

Backpropagation: If a branch fails a test suite or causes a syntax error, that failure is backpropagated up the tree. The agent learns that this path is dead and focuses its compute budget on the surviving branches.

3. The Verifier: Generative Process Reward Models (GenPRM)
Traditional agents use Outcome Reward Models (ORMs)—they only know if the final test passed or failed. If a 100-line script fails, the agent doesn't know which line caused the failure.

The bleeding edge uses Process Reward Models (PRMs). A PRM evaluates the agent's reasoning step-by-step.

How it works in practice: As your Explorer model generates pseudocode and intermediate logical steps, a PRM (trained specifically to verify reasoning traces) scores each step.

Code-grounded verification: The PRM doesn't just read English; it writes intermediate assertions to the Kata sandbox to verify its own logic mid-generation. If a step gets a low score, the MCTS algorithm immediately abandons that branch before wasting compute on generating the full code implementation.

4. Recursive Self-Improvement (Bounded RSI)
True "open-ended" RSI (a model rewriting its own weights) is not safely achievable or practical outside of frontier labs. However, Bounded RSI—where the agent improves its own scaffolding—is how systems like Anthropic's internal agents work today.

The Loop:

Inner Loop: The agent uses A2R + MCTS to solve standard Jira tickets.

Outer Loop: A dedicated "Meta-Agent" analyzes the execution traces of the Inner Loop. It identifies patterns where the Inner Loop struggles (e.g., "The agent wastes 3 loops parsing nested JSON").

Self-Modification: The Meta-Agent writes a new Python helper function or refines the system prompt for the Inner Loop, tests the new tool on a benchmark dataset (like SWE-bench), and automatically merges the PR into the agent's own repository if it improves the pass rate.

Bringing it Together on OKE
To implement this, your cluster needs:

A Job Orchestrator: (Like Temporal or an advanced Argo Workflows setup) to manage the parallel branching of the Explorer model.

Kata Containers: To instantly spin up isolated execution environments for every branch of the MCTS tree.

A PRM Service: A local endpoint running a specialized process verification model to score the tree nodes in milliseconds.

The jump from where you are to this SOTA architecture is massive. The most critical first step is decoupling reasoning from execution.

Are you ready to move away from the linear CrewAI script you are currently running and implement an asynchronous, tree-based orchestrator, or do you want to stick with a linear agent but upgrade its reasoning prompts?
