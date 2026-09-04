---
captured: 2026-09-04T16:02:39+00:00
session: 85f840c5-baf3-4598-9496-1b3eb9dd83e9
cwd: /Users/chidionyema/dev/code/idp
chars: 4202
source: founder prompt, verbatim (founder-doc-capture.py)
---

reviw Here is the complete, actionable Engineering Specification for deploying the zero-cost, self-hosted community version of the Cyrus orchestration framework.

This spec gives your engineers the exact commands and architecture needed to build the Coinbase-style software factory, leveraging their existing AI tools (like Claude Code or Cursor) directly on top of Linear and GitHub.

Engineering Specification: Cyrus Open-Source AI Orchestration

1. System Architecture Overview

Cyrus is a Node.js/TypeScript orchestration application that natively integrates Linearâ€™s issue tracking with AI coding agents. It acts as the state machine, managing Webhooks, isolated execution environments, and GitHub Pull Request generation.

Orchestrator: Cyrus EdgeWorker (Self-hosted on a machine you control).
Trigger Engine: Linear API & Webhooks.
Agent Engine: Claude Code, Cursor, Codex, or Gemini.
Version Control: Git + GitHub.
2. Host Machine Prerequisites

To achieve zero infrastructure cost, deploy this on an existing Linux VM, an unused Mac Mini, or an EC2 instance that runs 24/7. The host machine requires:

Node.js and a package manager (npm or pnpm).
Git configured with a GitHub App or Personal Access Token.
Your preferred AI CLI installed (e.g., Anthropic's @anthropic-ai/claude-code).
jq installed (required by Cyrus's internal parser packages).
3. Zero-Cost Deployment Steps

Do not use the paid managed service; use the End-to-End Self-Hosted (Community) option. This bypasses manual boilerplate by using an AI-guided setup.

Step 1: Install the Setup Skill Run this globally on the host machine to download the onboarding toolkit:

npx skills add ceedaragents/cyrus -g

Step 2: AI-Guided Configuration Open your terminal using your preferred AI agent (like Claude Code or Cursor) and run the setup command:

/cyrus-setup

Note: The AI will automatically handle installing dependencies, configuring your Linear OAuth/Webhooks, creating your GitHub integration apps, and connecting your target repositories.

Step 3: Persistent Execution To keep Cyrus listening to Linear webhooks securely in the background, wrap the process using pm2 or tmux.

# Using PM2

npm install -g pm2

pm2 start cyrus --name cyrus

4. The Orchestration Loop (Execution Flow)

Once running, Cyrus manages concurrency and the Plan -> Generate -> Evaluate loop natively without repository conflicts.

Trigger: A human assigns a Linear ticket to the Cyrus user. Cyrus detects the AgentSessionEvent webhook.
Git Isolation: Cyrus automatically creates an isolated Git worktree (e.g., /worktrees/DEF-1) cloned from origin/main. This allows multiple agents to work on different tickets in parallel.
Bootstrap (Optional): If a cyrus-setup.sh script exists in your repository root, Cyrus executes it within the worktree to prepare the specific environment.
Subroutine Execution: Cyrus delegates to the AI CLI, advancing through strict subroutines:
coding-activity: Implements the requested fix or feature.
verifications: The Evaluation Loop. The agent runs your local tests, type checks, and linters.
git-gh: The PR Handoff. It commits the changes and opens a GitHub Pull Request.
concise-summary: Generates a final summary and streams it back to the Linear ticket as a comment.
5. Security & Cost Guardrails

To prevent runaway API costs and infrastructure damage, enforce the following native Cyrus constraints:

Tool Restrictions: Configure Cyrus's tool permissions to sandbox the agent's shell access. Use strict patterns like "Bash(npm:*)", "Bash(git:*)", or "Bash(pytest:*)" to prevent the AI from executing unauthorized terminal commands.
Session Turn Limits: Hardcode turn-limit behaviors (e.g., maxTurns, maxSessionTurns) so the session fails gracefully and requests human help in the Linear thread rather than burning tokens in an infinite testing loop.
Enforce GitOps Read-Only: Ensure Cyrus creates separate worktrees and Pull Requests for human review. The agent must never be granted direct merge or push access to your protected main branch.
This setup provides the exact multi-agent factory infrastructure described by the Coinbase strategy, entirely on open-source rails and under your own compute control.
