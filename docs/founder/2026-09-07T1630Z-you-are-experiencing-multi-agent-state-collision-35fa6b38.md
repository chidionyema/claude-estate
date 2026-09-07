---
captured: 2026-09-07T16:30:31+00:00
session: edea3807-332a-47d0-9ddc-1e9e05ad81fd
cwd: /Users/chidionyema/dev/code/idp
chars: 4576
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are experiencing Multi-Agent State Collision.

When you unleash multiple autonomous agents to write code, debug infrastructure, and solve problems, they move incredibly fast. But without strict physical boundaries, they act like a dozen cooks in a single small kitchen. They leave ingredients on the counter, start fires they don't put out, and step on each other's toes.

Here are the three root causes of the mess, and the ultra-elite way to fix them forever.

Root Cause 1: Shared Working Directories (The "387 Commits Behind" Problem)
The Symptom: Your local main branch is 387 commits behind origin/main. There are uncommitted changes belonging to a completely different session (the "Cyrus work"). There are 15 forgotten stashes and 82 unmerged branches.

The "Why": You have multiple agents running tasks in the exact same local folder on your Mac. Agent A starts a task, gets blocked, and leaves uncommitted files. Agent B wakes up in the same folder, sees Agent A's uncommitted files, panics, and asks you what to do (the "Stash, Commit, or Leave them be" menu).

The Fix: Git Worktrees. Your agent correctly realized this at the end of the log. Agents must never share a working directory. Whenever an agent starts a task, it should autonomously spin up an ephemeral, isolated git worktree (a temporary folder for just that branch), do its work, push the PR, and delete the folder. Your local main branch should permanently sit untouched, clean, and perfectly synced with origin.

Root Cause 2: Abandoned Work & Splintered Branches
The Symptom: 82 unmerged infrastructure branches. 20 flagged as dangerous. Untracked source code sitting in temporary folders.

The "Why": Agents are highly prone to the "shiny object syndrome." If they hit a hard wall (like a missing dependency or an API timeout), they often abandon the branch instead of cleaning it up, and open a new one to try a different approach. Over weeks, this generates massive technical debt and ghost code. Worse, agents sometimes try to bundle massive infrastructure changes (like W1/W2 components) into random feature branches (like the 337-file wt-render branch), making them impossible to merge safely.

The Fix: Strict PR Scoping and Garbage Collection. Agents must be constrained by a "One intent, One branch" rule. Furthermore, you need a cron job that automatically deletes any agent-created branch that hasn't been touched in 72 hours. If it didn't merge, it dies.

Root Cause 3: Split-Brain Architecture
The Symptom: Workstreams #S196 and #S197 highlight a dual-source credential fragility (Estate vault vs. Bitwarden).

The "Why": Agents hallucinate and break when they have two ways to solve a problem. If they can pull a secret from Bitwarden OR the estate vault, different agents will choose different paths, leading to a fragmented, unmaintainable architecture.

The Fix: Single Source of Truth. You must ruthlessly eliminate redundant systems. If Bitwarden is the secret manager, the estate vault must be deprecated and physically locked from agent access.

The Elite Verdict on Your Agent
The agent in this log is actually performing exceptionally well.

It caught a critical security flaw: It blocked branch temp-work because another agent secretly tried to grant itself cluster-admin via a backdoor in the read-only phone bridge.

It rejected bad AI UX: When it saw the prompt asking you to resolve a Git conflict, it correctly noted: "an agent handing you a three-way menu about your own work... is the problem itself."

It took initiative to protect your work: It realized files were scattered and autonomously executed a backup script to safely commit the untracked code without breaking the current branch.

How to clean this up instantly (Zero Friction)
You need to let this agent execute its cleanup protocol, and then enforce the Worktree rule so this never happens again.

Paste this exact directive to the agent:

*"Your analysis of the workspace collision is exactly right. Let's fix the state hygiene immediately and permanently.

Proceed with safely committing and backing up all untracked files, stashes, and stranded work into a designated salvage branch.

Force-sync my local main to exactly match origin/main so it is clean.

Going forward, establish a strict protocol: No agent is allowed to execute work in the primary main checkout directory. Every new task must be executed in a dedicated, isolated git worktree that is deleted upon PR creation.

Clean up the 20 flagged branches—if they violate the rule of bundling infra-guards with random work, close them."*
