---
captured: 2026-09-03T12:23:39+00:00
session: 54539261-20a7-4289-a144-e9265f1b0c43
cwd: /Users/chidionyema/dev/code/idp/.wt-purge
chars: 1620
source: founder prompt, verbatim (founder-doc-capture.py)
---

you are stil doingThe "Nuke the Maze" Mandate
Kill the agent's current background waiting task, open a fresh prompt with it, and drop this absolute mandate to gut the CI pipeline of all non-functional friction.

Copy and paste this directly to the agent:

Plaintext
FOUNDER MANDATE: THE CI PURGE

The CI pipeline is a toxic, brittle minefield that is destroying our deployment velocity. You just spent 34 minutes fixing capital letters after colons and hardcoded test counts. This ends today. 

Execute the following structural changes to the idp and crew repositories immediately:

1. NUKE VALE: Remove Vale entirely from GitHub Actions workflows. We do not run grammar linters on infrastructure repositories. Delete the `.vale.ini` file.
2. NUKE TEST COUNTS: Sweep the entire `bdd-suites` architecture. If any test asserts a hardcoded number of passed tests (e.g., "2 passed"), strip it out. Tests must only assert `returncode == 0`.
3. EXEMPT BOTS: Update the `fast-gate` and `spec-gate` workflow files. If the commit author is a bot/agent, these gates MUST automatically return exit 0 (skip). 

Do not ideate. Do not write a new testing framework. Delete the friction, commit the changes to a branch named `chore/nuke-ci-friction`, and push it.
Why this is the only way forward
Until you delete Vale and bypass the spec-gate for automated tools, every single code change you request will take 45 minutes of agent yak-shaving.

You told it to purge the test theatre, and it did—but it got caught in the CI theatre. Nuke the linters, and your agent will finally become the 1-minute deployment sniper you need it to be.
