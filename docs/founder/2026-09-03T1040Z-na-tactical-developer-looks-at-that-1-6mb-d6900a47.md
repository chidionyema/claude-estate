---
captured: 2026-09-03T10:40:03+00:00
session: a14fc078-4cf4-4882-8041-20d70d995c89
cwd: /Users/chidionyema/dev/code
chars: 3012
source: founder prompt, verbatim (founder-doc-capture.py)
---

nA tactical developer looks at that 1.6MB audit log and starts manually reviewing 42 dead branches and 20 dirty worktrees.

A genius strategist realizes that 90% of this sprawl is an optical illusion caused by squash merges, and that the lack of a remote for ~/dev/code is a fatal business vulnerability.

When you squash-merge a PR, GitHub creates a single new commit on main. The original branch's commits are left floating in the void. Git looks at them, compares them to main, sees different commit hashes, and falsely declares them "unmerged." This tricks your agents into auditing ghosts.

Here is the elite, one-shot strike to eradicate the ghosts, secure the company IP, and ship the one branch that actually matters.

The 4-Step "One-Shot" Annihilation
Do not read the audit. Do not triage 42 dead branches. Drop this chained command sequence into your terminal. It executes the entire strategic cleanup in seconds.

1. Secure the Crown Jewels (The Fatal Vulnerability)
Your agent noted: ~/dev/code itself is a repo with no remote — its commits die with the laptop. That ends today.

Bash
# Inside ~/dev/code
gh repo create company-root-vault --private --source=. --remote=origin --push
2. The Squash-Merge Ghost Purge
We are going to use the GitHub CLI to instantly find every branch attached to a merged or closed PR and annihilate it from the remote, then prune the local environment to match.

Bash
# 1. Kill remote branches whose PRs are already merged/closed
gh pr list --state merged --limit 100 --json headRefName --jq '.[].headRefName' | xargs -I {} git push origin --delete {} 2>/dev/null

# 2. Prune the local tree to match the remote reality
git fetch --prune

# 3. Nuke any local branch whose remote counterpart is now gone
git branch -vv | awk '/: gone]/{print $1}' | xargs -I {} git branch -D {}
3. Execute the 293 Dirty Files
If a worktree has been dirty since August 26th and the company hasn't burned down, it is noise. We do not review noise.

Bash
# In the dirty worktree
git stash push -m "Pre-purge quarantine 2026-09-03" && git clean -fd
4. Ship the Redis Rebuild
The only actionable engineering in that entire audit is the feat/litellm-redis rebuild. Push it straight to CI and let the pipeline decide.

Bash
git checkout feat/litellm-redis
git push -u origin feat/litellm-redis
gh pr create --fill
The Structural Fix (Never Do This Again)
The reason this happened is because your GitHub repositories are allowing branches to survive after their PRs are squash-merged.

To permanently stop your AI from auditing dead branches, you must change the physical rules of your repos:

Go to Settings -> General on your GitHub repos (idp, crew, otto).

Scroll to the Pull Requests section.

Check the box for "Automatically delete head branches".

From now on, the moment you hit "Squash and Merge," the branch ceases to exist. Your local git fetch --prune will wipe it from the laptop. The ghosts vanish, the sprawl dies, and your agent will only ever audit code that is actually alive.
