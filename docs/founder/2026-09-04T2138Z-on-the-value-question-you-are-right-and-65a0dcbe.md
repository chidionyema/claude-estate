---
captured: 2026-09-04T21:38:52+00:00
session: 1790f775-dca6-49f9-9f54-76b1a679dd35
cwd: /Users/chidionyema/dev/code/idp
chars: 11258
source: founder prompt, verbatim (founder-doc-capture.py)
---

On the value question — you are right, and k8sgpt is the proof. It holds exactly 52 findings. Of those, 25 are ConfigMaps
flagged as "is empty", which is not a defect at all. 18 are Services, 5 are failed descheduler Jobs, and 4 are Pods. It
re-explains those same 52 things about 77 times a day, at ~1,950 output tokens each, because spec.analysis is unset and
noCache: true. Nobody has read them.

So roughly 39 million of the 176 million was a robot writing the same 52 essays over and over about a cluster that was
already broken. At MiniMax's real prices that is about $49 — the single biggest line, and the only one still spending.

One of those 4 Pod findings, incidentally, is the answer to why your agent is down: hermes-agent-gateway fails its startup   probe — connection refused on 10.244.1.243:9900, nothing listening.                                                       
I'm changing the k8sgpt CR now: an explicit analysis interval and a filter list that drops the ConfigMap noise. That takes
it from ~4,000 calls a day to a few hundred without losing a single real finding.                                                                                                                                                                       Crunched for 3m 4s · done 22:26

❯ what i this            who           │ calls  │ tokens in │ tokens out │ avg prompt │             where it ran
  │
    ├─────────────────────────┼────────┼───────────┼────────────┼────────────┼───────────────────────────────────────┤
    │ sovereign-kernel (KINI)

  Ran 2 shell commands

KINI is your own workflow engine. It's the estate's "durable job runner" — the thing that holds a long-running job and keeps
it alive across restarts. In docs/explanation/architecture/model-stack.md it's described as: "the durable workflow engine
(Temporal) that runs long jobs. When a job needs a model it asks the router with the login sovereign-kernel."

Where it runs: on your Mac, not in the cluster. Two processes, started by launchd, up for 1 day 8 hours right now:

- sb worker — pid 2430, ~/dev/code/idp/sovereign/.venv/bin/python -m sovereign.cli worker
- sb cockpit — pid 2402

That matches the ledger, which shows its calls arriving at the router through the public edge from outside the cluster.
                                                                                                                         What it actually spent: 91.4M tokens, but 69.5M of that was two days — 39.6M on 30 August and 29.9M on 31 August. Since then
it has fallen away: 9.2M, 5.9M, 4.7M, and 0.28M today. Its shape was ~28,500 tokens of prompt per call for a one-sentence
answer back, 3,145 times.

What I cannot tell you, and won't pretend to: what those jobs were. Its log file only contains Temporal connection retries —
the worker never logged a single job on 30 or 31 August, and the router doesn't store request bodies (messages is empty on
every row). So I can prove it was KINI's login, from your Mac, at that size and on those two days, and no further.                                                                                                                                 The honest summary of the three: KINI spent the most in total but has largely stopped. k8sgpt is the one still spending      today, and it's the one I'm cutting.

✻ Cooked for 3m 51s · done 22:29                                                                                                                                                                                                                    who isusing opencode on your Mac — 38.7M tokens. The key called laptop-... in the ledger is the file                      ~/.config/prospector/secrets.d/LITELLM_API_KEY, ane 73 of your ~/.zshrc, and ~/.config/opencode/opencode.json, whose default model is estate/minimax. It burned 20.6M on 1 September and 18.0M today,  and almost nothsorry this all sounds retared and need to be explined sinply                                                   Interrupted · What should Claude do instead?                                                                                                                           what jobs? we disocvered tody tenporal wast eve w                                                                                                                           Searched for 1 pattern, ran 6 shell commands, wro ⎿  Remembered founder 2026-09-04 — a credential's label names who it was minted for, never who used it; prove the calling  sorry if it running on laptio not sure how this adds anyvalues, we aaree using all these fnacy terns but id like to know  what aree thee thigs doing to be costinso nacu an                                                                                                                           WORKING: cutting the one that's still spending. H                                                                                                                           Three things spent the money. Only one of them I 's the worthless one.                                                                                                                           1. A coding assistant on your Mac — 38.7 million ode. It's the same kind of tool as Claude Code, but pointed at MiniMax instead. It spent almost nothing for days, then 20.6M on 1 September and 18.0M today. I confirmed  this properly: I asked the router which key that laptop-20260829T143252Z. Whether that was worth it depends on what got built in it — I can't see that, only you can.                                                          2. The thing I called "the sovereign kernel" — 91.4 million tokens. I was wrong and you caught it. You're right that      Temporal was never wired up, so it ran no jobs, ag days (30–31 August, 69.5M between them) contains nothing but failed connection attempts. All I actually know is that a key with that name made 3,145 very large calls from outside the cluster. I cannot tell you what progreral things on your Mac share that one key, so the
bill says the same name whichever one called. I'm not going to guess at it.

3. A robot called k8sgpt — 45.7 million tokens, and the only one still spending today. This one I can explain completely. It
watches the cluster, finds problems, and pays theation of each one in English. It has found 52
things. Twenty-five of them are "this ConfigMap is empty", which is not a problem. It re-asks for an explanation of the same
52 things about 77 times a day, every day, and noswers. That is roughly 39 million tokens and
about $49.

What the 176 million actually bought you: four real findings, buried in k8sgpt's output. One of them is hermes-agent-gateway
failing its startup probe — nothing listening on ur agent has been down for days, and it was
sitting there in the cluster the whole time, unread.

Two fixes, and I'm doing both now: throttle and filter k8sgpt so it stops re-explaining the same 52 things, and give each
program its own key so next time the bill names thared label.

✻ Worked for 1m 59s · done 22:32

❯ what dles tis do the sovereign kernel

  Ran 2 shell commands

The sovereign kernel is meant to be the safety neder for agent work. Reading its own command list,
that's what it's built to do:

- Records every action an agent takes as a signed receipt in a chain (verify-receipts, audit) — so afterwards you can prove
  exactly what was done and by whom, and nobody cry.
- Undo and rewind (undo, rewind, recover) — revert the commit an agent made, or roll the whole thing back to an earlier
  point and rebuild from there.
- A spending cap per session (start, refill) — a session gets a budget, and when it's gone the session halts until you top
  it up.
- A vote before anything destructive (consensus) — three different models have to agree before a delete or a force-push is
  allowed.
- A stop / approve / deny switch (stop, approve, deny, steer) — you can interrupt a running agent and point it somewhere
  else.

So the idea is: agents can work unattended, but epped, reversible, and you hold the stop button.

And here is the honest part. None of that has beeat actually runs the jobs — Temporal — was never
connected, which you found today. The two processes on your Mac have been sitting there polling a queue and failing to reach
it, for days. Their log has no jobs in it at all.

So it is a safety net that is built but not switcn tokens billed under its name did not come from
it doing any of the above. I still can't tell you what did spend them, because that key is shared between several programs,
and I'd rather say that than name the wrong one t

✻ Cooked for 38s · done 22:33

❯ ur not being clear at all,wh  is meant to be  wha

Right now it is doing nothing.

Two programs are running on your Mac — started 1 l running. Every few seconds they ask a queue "is
there any work for me?" The queue isn't there. They get a connection error, wait, and ask again. That is the entire contents
of their log file. No jobs. Not one, on any day.

It was built to be the safety net for agent work ent does so it can be proven and undone, cap what
a session can spend, and require a vote before anything destructive. It has never done any of that, because the part that
hands it work was never connected.

So: built, running, and idle. Burning electricity

✻ Baked for 24s · done 22:34

❯ ok lets disable

  Ran 3 shell commands

❯ and what of aiden and naestro , are theu using to

  Listed 1 directory, ran 2 shell commands

❯ are they adding value or can be diabled

  Ran 3 shell commands

WORKING: the sovereign kernel is stopped. launchci.estate.sovereign-worker or ai.estate.cockpit,
both processes are gone, and both are launchctl disabled so they won't come back on reboot.

On Aiden and Maestro — neither one costs you a single token. Two checks agree:

- Their code makes no model calls at all. Aiden's own file says so at line 5: "nothing in this program asks a model
  anything" — it reads your Claude Code session ltro has no model call in any of its Python.
- Neither has a login in the router's ledger. The complete list of who has ever called it is: sovereign-kernel, k8sgpt,
  laptop, science, founder-aider, otto-golden, anden, no Maestro.

So they are not part of the money problem.

On whether they earn their keep, they're differen

Aiden is already dormant — no launchd job, nothin August. It isn't running. Nothing to disable.

Maestro is running right now, every minute, and iase as k8sgpt — just for free. Today it ran 340
audit cycles. Each one reads 62 rows and produces 47 findings. Its log says 47 standing needs_human alarm(s) already open —
meaning 47 things it has flagged for a human, and at any of them. It logs the same incident as a
"Novel incident" 885 times. Its log file is 13.5 MB.

My read: disable Maestro. It costs no money, but 47 unread alarms and a 13.5 MB log is not value — it's the same
instrument-nobody-reads problem, and leaving it rt person who looks assumes something is watching
the estate when nothing is. Say the word and it goes the same way as the kernel.

✻ Cogitated for 1m 37s · done 22:36

❯ ok

  Previous task still in progress
  ⎿  $ cd /private/tmp/wt-k8sgpt && git push origin
