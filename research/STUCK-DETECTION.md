# Stuck detection — the spec

**Requirement R23.** Founder, 2026-08-21: *"sending alert to founder telegran when stck on
task/decisino that cant resolve or when console freeses or claude api tines out, need sone process
to page founder and be able to recover"*. And the constraint that shapes every number below:
*"that dot self heal"* — a condition that clears itself must never page.

**Implementation:** `~/.claude/scripts/stuck_detector.py` (stdlib only, python3).
**Status: it does not page.** `would_page` is a field in the output, not an action. Wiring it to
Telegram is a separate decision that has not been taken.

Prior research this builds on: [`PAGING-AND-REMOTE-CONTROL.md`](PAGING-AND-REMOTE-CONTROL.md).

---

## 1. Why the transcript is the signal

Every Claude Code hook event — PreToolUse, PostToolUse, Stop, SessionStart — is driven by the
session *doing something*. A wedged session emits no event, so **a hook can never be the
detector**. It has to fire on absence, and on a signal the stuck session does not have to
cooperate to produce.

Claude Code appends every session's records to `~/.claude/projects/<slug>/<session-id>.jsonl` in
real time, for its own purposes. `estate_spend.py` already leans on this for the same structural
reason: a meter fed by our own instrumentation goes blind exactly when our code breaks. So does a
pager.

**Corpus, measured 2026-08-21:**

```
ls ~/.claude/projects | wc -l                                        # 16,616 dirs
find ~/.claude/projects -maxdepth 2 -name '*.jsonl' | wc -l          # 89,418 transcripts
find ~/.claude/projects -maxdepth 2 -name '*.jsonl' -mmin -360 | wc -l   # 26 live (6h)
```

Scan cost: **50.2s cold, 13.2s warm** for the whole corpus (`time find ... -mmin -360`); the
detector end to end runs in **31.6s**. Transcripts are read by **seeking to the last 1 MB**, never
loaded — the largest live transcript measured is **96,151,013 B (96 MB)**.

---

## 2. The five classes

| # | Class | Implemented | Signal |
|---|-------|:---:|--------|
| 1 | **SILENT** | yes | idle past threshold with an unanswered tool call, or no clean turn end |
| 2 | **LOOPING** | yes | N identical consecutive tool calls, or the same error repeating with no success since |
| 3 | **BLOCKED_ON_HUMAN** | yes | interactive session, turn ended on a question, then nothing |
| 4 | **ERRORED** | yes | consecutive API-level errors with no successful call since |
| 5 | **BURNING** | **no — see §6** | cost climbing with no file edits |

### The discriminator that makes SILENT usable

Most idle sessions are not stuck. They finished a turn and are waiting for a human — the normal
resting state of every interactive session on this box. Paging on those is the cry-wolf failure.

The separator is the last assistant record's `stop_reason`. Measured over 101 transcripts,
803 assistant records carrying the field:

```
stop_reason = tool_use        606    asked for a tool, waiting on the result
stop_reason = end_turn        194    finished, handed back to the human
stop_reason = stop_sequence     3
```

A tail ending in `end_turn` is **at rest** and is never silent-stuck, however long it sits.
A tail ending in `tool_use` with **no matching `tool_result`** is a session that died mid-call —
the founder's *"console freeses"*. Measured: only **4 of 101** tails carry a dangling tool_use, so
this is a rare and therefore informative signal.

---

## 3. Every threshold, and the measurement that produced it

No number here was chosen because it sounded right.

### `SILENT_S = 900` (15 minutes)

Derived from the distribution of intra-session gaps **that later resumed**. A gap that resumed
was, by construction, not a stuck session, so the threshold must sit above them.

Measured over 101 transcripts, **134,362 resumed gaps**:

| percentile | gap |
|---|---|
| p50 | 2.2 s |
| p75 | 5.3 s |
| p90 | 12.1 s |
| p95 | 19.8 s |
| p99 | **93.2 s** |
| p99.5 | 149.3 s |
| p99.9 | **446.2 s** |

```
gaps > 300s (5m):  218 of 134,362  (0.162%)
gaps > 600s (10m):  93 of 134,362  (0.069%)
gaps > 900s (15m):  62 of 134,362  (0.046%)
```

900 s sits **~10x above p99** and **~2x above p99.9**. A normal working pause does not reach it.
Going tighter costs precision fast: 300 s would triple the candidate rate for no detection-time
benefit that matters on a pager a human reads.

### `LOOP_RUN = 3` — identical consecutive tool calls

Measured over a **14-day corpus, 14,471 transcripts >20 KB, 485 of them containing tool calls,
4,464 tool calls total**. Longest run of identical back-to-back calls (same tool, same arguments)
per session:

```
run length 1:  484 files
run length 2:    1 file
  >= 2:  1 of 485  (0.21%)
  >= 3:  0 of 485  (0.00%)
```

**No healthy session in the corpus ever reached 3.** The threshold sits directly above the
observed maximum. The run is counted at the **tail** of the call sequence, not anywhere in it: a
loop three calls ago that the session broke out of is a session that recovered.

### `API_ERR_RUN = 2`

`isApiErrorMessage` is Claude Code's own flag on a record; 4 occurrences across the live corpus.
One API error is retried and clears itself, and the founder's constraint forbids paging on that,
so one is never enough. Backed by the split already made in the engine's
`errors.classify_exhaustion`: a `429` carrying `retry-after` is backpressure and self-heals, a
`429` carrying `enforced_spend_limit_reached` does not.

### `LIVE_WINDOW_S = 21600` (6 hours)

A stuck session nobody is watching any more is archaeology, not a page. Also what keeps the scan
bounded — 26 files instead of 89,418.

### `DEBOUNCE_CHECKS = 2`

Prometheus' published batch-job guidance is a staleness threshold of **at least 2x the job
period**. Applied to a pager: a condition must survive a whole extra check interval before it is
allowed to wake anyone.

---

## 4. The debounce — "that dot self heal", mechanically

State lives in `~/.claude/state/stuck-detector.json`, written atomically (a pager whose own state
file is half-written pages on garbage).

Rules, each one pinned by a selftest case:

1. A class must hold for **2 consecutive checks** before `would_page` is true.
2. The streak is keyed on **session AND class**. A session that flips SILENT → LOOPING has two
   one-check conditions, not one two-check condition, and neither pages. A flapping session is a
   session that is still moving.
3. `OK` **drops the streak entirely**. A condition that clears itself between checks can never
   page, which is the founder's constraint stated as code.
4. `paged` **latches**, so a condition that persists for hours pages **once**, not every check.
   Google SRE's sustainable ceiling is 2 incidents per 12-hour shift; a repeating page burns it in
   minutes.

---

## 5. False-positive analysis

Two real false positives were found by running against live data, and both are fixed at source
with a regression test.

### FP-1: a filtered subsequence never moves on *(found live, session `74f4ed5c`)*

The first live run flagged `LOOPING` on a real session: the same tool error 4 times.
Verified genuine and not a re-emission artifact — 4 distinct `uuid`s, 4 distinct `tool_use_id`s,
timestamps 16–22 s apart. But then:

```
idx=336  09:23:54  is_error=1  'Agent fleet cap: 3 of 3 leases are live...'
idx=338  09:24:10  is_error=1  'Agent fleet cap: ...'
idx=340  09:24:31  is_error=1  'Agent fleet cap: ...'
idx=354  09:24:53  is_error=1  'Agent fleet cap: ...'
idx=362  09:25:27  is_error=0  <-- RECOVERED
idx=375  09:26:23  is_error=0
idx=381  09:26:32  is_error=0
```

The session recovered. The error list is a **filtered subsequence** of the transcript, so its
trailing run stayed at 4 forever. Counting a run over a filtered list answers *"did this ever
happen"*, not *"is this still happening"* — and only the second question may page.

**Fix:** every run is counted only over records **after the last successful tool result**.
Pinned by three selftest cases, including the inverse (the same 4 errors with nothing after them
must still fire).

### FP-2: a headless one-shot cannot be blocked on a human

After FP-1 was fixed, the only remaining live hit was `BLOCKED_ON_HUMAN` on a session whose answer
happened to end *"Does that help?"* — a rhetorical closing, not a decision request.

Measured over the 26 live transcripts:

```
entrypoint: sdk-cli  21     headless one-shot, no human attached
entrypoint: cli       5     interactive
```

An `sdk-cli` session has nobody waiting to answer anything; it has simply finished.
**Fix:** `BLOCKED_ON_HUMAN` applies only to `entrypoint == "cli"`. Pinned by a paired selftest —
the same question from `cli` fires, from `sdk-cli` does not.

### Known remaining weakness

`BLOCKED_ON_HUMAN` still keys on a trailing `?`, which cannot distinguish *"which do you want?"*
from a rhetorical sign-off. Restricting it to interactive sessions removed every observed instance,
but the heuristic is weak and this is the class most likely to produce the next false positive.
The debounce contains the damage rather than fixing it. If it proves noisy, the honest next step is
an explicit marker a blocked session writes, not a better regex.

### The ambiguity that is not resolved

From the prior research, restated because it still stands: **a sleeping MacBook is byte-identical
to a dead agent.** Both stop appending. This detector cannot tell them apart and does not try. It
is why the detector must not become the pager on its own — the thing that pages needs either a
sleep/wake marker or an alert window respecting the founder's hours.

---

## 6. BURNING — measured, and deliberately NOT implemented

The brief asked which classes could not be measured honestly. This is the one, and the reason is a
measurement rather than an opinion.

Cost **is** available: of 374 sessions with tool calls, **374 carry `message.usage`** (100%), so
the spend side is fully reconstructable exactly as `estate_spend.py` does it.

The problem is the other half of the definition. Measured over the same 374 sessions:

```
sessions with BOTH usage and a file edit in the tail:  48 of 374  (12.8%)
sessions that made ZERO file edits in the tail:       367 of 374  (98.1%)

longest run of consecutive NON-EDIT tool calls per session:
   p50 8 | p75 15 | p90 19 | p95 20 | p99 25 | max 29
```

**"Spending money with no file edits" describes 87% of normal work on this estate.** Research,
review, measurement, triage and reporting sessions legitimately never touch a file. A detector
keyed on that would fire on the overwhelming majority of healthy sessions — the precise failure the
founder pre-empted.

A real BURNING detector needs a progress signal that is not "files changed": a monotonic counter
the session itself advances against its named job. That does not exist yet, and inventing a
threshold over a signal this noisy would be exactly the guessing the estate's laws forbid.
**Deferred, with the measurement recorded so the next attempt starts here.**

---

## 7. What is deliberately not built

- **No paging.** `would_page` is a field. No Telegram, no Pushover, no side effects of any kind.
- **No recovery actions.** The detector never kills, resumes, or nudges a session. Detection and
  intervention are separate decisions, and the second one has not been taken.
- **No secret reading.** No `.env` parsing, no credential access, no token in the process.
- **No daemon.** It is a one-shot script. Scheduling it is a separate decision; the debounce
  assumes consecutive runs but does not care what invokes them.
- **No modification of any existing script.** New file only.

---

## 8. Interface

```
stuck_detector.py                 # human-readable table of non-OK sessions
stuck_detector.py --all           # include sessions classified OK
stuck_detector.py --json          # one JSON row per session
stuck_detector.py --selftest      # 24 cases; exits non-zero on any failure
stuck_detector.py --no-state      # classify without persisting the streak
stuck_detector.py --silent-s 60   # override a threshold (used to prove the probe is alive)
```

JSON row:

```json
{"session": "...", "slug": "...", "class": "SILENT", "idle_s": 176,
 "evidence": "idle 176s, last stop_reason='tool_use', no clean turn end",
 "would_page": false, "streak": 1, "cwd": "..."}
```

`--selftest` builds synthetic transcripts covering all four implemented classes plus healthy and
at-rest controls, both regression cases from §5, a mutation proof that each threshold is
load-bearing, six debounce cases, and four safety cases (a 4 MB transcript, a truncated line, a
file of garbage, an empty record list). **24 passed, 0 failed** as of 2026-08-21.

---

## 9. Live result, 2026-08-21

```
live sessions (transcript touched < 6h): 26
not OK: 0   would_page: 0
```

All 26 live sessions healthy: 25 at rest on a clean `end_turn`, 1 actively working. Re-run ten
minutes later: **31 live, 0 not OK, 0 would_page** — the population moves, the verdict did not.

A clean result and a dead probe look identical, so the probe was proved alive rather than assumed:
re-run with `--silent-s 60`, it correctly classified a real live session as
`SILENT — idle 176s, last stop_reason='tool_use', no clean turn end`. On the next run that same
session had moved on and the row was gone, which is the self-healing behaviour the debounce exists
to absorb, observed live.

The two conditions it did flag during development were both real events (a genuine 4x fleet-cap
retry loop, and a genuinely idle question) that both **self-healed**, and in both cases the
debounce held `would_page` at false. The design constraint held on its first contact with real
data.
