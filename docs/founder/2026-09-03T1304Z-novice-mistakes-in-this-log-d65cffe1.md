---
captured: 2026-09-03T13:04:18+00:00
session: a14fc078-4cf4-4882-8041-20d70d995c89
cwd: /Users/chidionyema/dev/code/idp
chars: 2837
source: founder prompt, verbatim (founder-doc-capture.py)
---

Novice Mistakes in this Log
1. The "Rerun and Pray" Anti-Pattern
The agent realized the failure was a "Tailscale API flake"—an external network timeout completely unrelated to the Superset code it was trying to ship. Its solution? Hit the "rerun jobs" button and wait another 5 to 10 minutes, hoping the third-party API feels like cooperating this time. This is how 2-minute tasks stretch into 40-minute deployment nightmares.

2. Live External APIs in the Critical Path
Your CI pipeline is making live network calls to the Tailscale API during a standard BDD test. That is an architectural sin. CI environments are ephemeral and noisy; if a pre-merge gate relies on a live external service, your pipeline will constantly randomly fail due to rate limits or network blips.

3. Zero Executive Judgment
The agent knows the Superset code works. It knows the failure is an unrelated flake. But because it lacks executive authority, it refuses to ship the code. It is prioritizing the bureaucracy of a green checkmark over the reality of a working feature.

How to Solve This (The Elite Fix)
You solve this by changing how both you and the agent treat flaky tests. You do not wait for them. You quarantine them or bypass them.

Step 1: The Immediate Override (Do this right now)
Since you know the code is good and the failure is a flake, do not let the agent sit there polling the CI.

Tell the agent: "The Tailscale failure is an unrelated flake. Execute an Admin Merge on PR 1263 immediately to bypass the CI block, then capture the Superset receipt."

Step 2: Quarantine the Flake (The Structural Fix)
A flaky test is worse than no test because it destroys trust in your CI pipeline and trains agents to ignore red lights.

After the merge, instruct the agent: "Open a new PR. Find the Tailscale token-exchange test that just flaked. Add a @pytest.mark.skip(reason='flaky live API call') decorator to it. We do not block deployments on third-party API weather." (Note: If you aren't using pytest, tell it to comment out the test or add the equivalent skip syntax for your framework).

Step 3: The "Flake Protocol" for AGENTS.md
To permanently stop the agent from doing the "rerun and pray" loop in the future, add this exact rule to your AGENTS.md file:

THE FLAKE PROTOCOL:
If a CI check fails, you must analyze the root cause. If the failure is 100% unrelated to your code changes (e.g., a known network flake, a third-party API timeout like Tailscale, or a random infrastructure blip), DO NOT just rerun the job and wait.
Instead, you will do two things:

Add a skip/quarantine flag to the flaky test in your current PR so it passes.

Proceed with the merge.
We prioritize velocity over broken tests.

Stop letting broken windows in your testing suite hold your deployments hostage. Force the merge, mute the bad test, and keep moving.
