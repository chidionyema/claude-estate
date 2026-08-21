# Consultant brief — why this estate repeats itself

**Prepared 2026-08-21. Every number carries the command that produced it. Nothing here is recalled.**

You are being asked one question: *why does a founder running an AI-agent software estate have to
say the same thing over and over, and what should change?* This document is the evidence. It does
not contain a recommendation, because the recommendation is what you are for.

---

## 1. What this is

A one-founder company. The product is `prospector`, a Python engine plus a storefront. The work is
done by five to six Claude Code agent sessions running concurrently on one laptop, sharing one git
checkout, one rules file, and one set of guard scripts under `~/.claude/scripts/`. There are no
human engineers. The founder is the only person in the loop.

Two constraints bind every option you might propose:

- **R32, portability.** *"Portability outside Claude Code is crucial, and portability also means
  model-agnostic"* (`docs/REQUIREMENTS.md:65`). Anything that only works inside one vendor's CLI is
  disqualified.
- **No funds.** Five sessions spent $515 of a $516.79 day on 2026-08-21. Every recurring cost is a
  threat to the business.

## 2. The complaint, in the founder's words

> *"we clain our olutions work yet in here always rpeaing nyself, we dont retien any contents, we
> have no sense of urgeny or what is priority, out spine is brroken and its getting super critical
> ... we are our own owrst eneny naking clins witout evidence. ny evidence is tha in repeaint
> gnyself and we keep naking the sane rookie istakes. and our code is not solving it and writing
> nnore ccode is not the solutio."*

> *"where is our board? i ave give you nany things to do this sssion, where os the traccking?"* —
> then, when answered: *"why do i need to ask?"* — then: *"i thought we solved thi already"*.

He is not describing a feeling. The estate measures him: **12 of the last 280 things he said were
complaints, and 8 of those 12 landed in the last 6 hours.** Source: `founder_board.py --json`.

## 3. The seven clusters

### A — Work is measured, and never delivered to the person who asked

The estate is full of instruments that report to nobody.

| Instrument | What it produces | Who receives it |
|---|---|---|
| `founder_board.py` + `com.founder.boardserve` | a full status page, served at `http://127.0.0.1:8787`, HTTP 200, up all day | **nobody — the URL appeared in no session-start hook, no doc, nowhere.** `rg '8787' ~/.claude/settings.json` returned nothing |
| `com.founder.stuckdetector` | 218 rows, some marked `"would_page": true` | **nobody.** `rg -l stuck-detector ~/.claude/scripts` returns only its own files |
| `prompt-ledger.py` | 3,670 + 865 + 73 captured founder asks | **nobody.** `--project-dir /Users/chidionyema --list open` returns `0 of 0`; the same data via `--ledger <path>` returns 45+ rows. Capture works, read-back is broken |
| `com.founder.board` (hourly builder) | the page above | last exit code **1**; it missed its 18:03 run and nothing alerted |
| 15 launchd background jobs | — | **6 are failing** (`ai.hermes.keepawake` 78, `com.prospector.offsite-backup` 2, `com.prospector.launchd-held` 1, `ai.hermes.idle-engine` 78, `com.estate.costsentinel` 1, `com.prospector-control.standby-sync` 1) |

This is the direct cause of *"why do i need to ask?"*. The answer existed, at a URL, hourly, all
day. Nothing put it in front of him.

### B — Written status and disk state disagree

| Document says | Disk says | Command |
|---|---|---|
| R32: "3 of 8 governance pieces ported" | **1 of 8.** Harness-dependent line counts: `prompt-ledger.py` 34, `goal-guard.py` 15, `decision-log.py` 1. The eight pieces are enumerated in no document at all | `rg -c 'transcript\|\.jsonl.*session\|CLAUDE_SESSION_ID\|settings\.json\|hook'` |
| W7: *"claim before the first edit"* with `--label claimed` | **0 of 71 open issues carry the label.** 63 carry no label at all | `gh issue list --label claimed` |
| 136 documents track deliverables | **510 deliverables sit in tables with no status column**, so nothing can ever mark them done. 55 more have a status word nothing recognises | `action_items.py --json` |

The founder's reaction to the first row: *"this is why i dont trutst our process"*. He is right to
distrust it. Code is exercised by compilers and tests; prose is exercised by nothing, so it drifts
the moment it is written and then gets believed because it is written down.

### C — Everything is open at once

| Measure | Value |
|---|---|
| Open GitHub issues | 71, **0 claimed** |
| Open action items across 136 docs | 317 open, 188 done — 37% finished |
| Requirements proven done | **10 of 53** |
| Concurrent agent sessions | 5–6, no cap |
| Spend | $515 of $516.79 in one day |
| Throughput | healthy — 21 PRs merged in 6 hours, 30 in 24 hours |
| Lead time | 0.7h median, 4.6h worst |

Throughput is not the problem. **WIP is uncapped.** Little's Law says lead time equals WIP divided
by throughput, so with throughput fixed the only lever on how long anything takes is how much is
open. Nothing in this estate limits that number, and nothing decides which of the 71 goes first.

### D — The response to every process failure has been to write more governance code

This is the cluster the founder named himself: *"our code is not solving it and writing nnore ccode
is not the solutio."* The measurement supports him.

| Measure | Value | Command |
|---|---|---|
| Python scripts in `~/.claude/scripts` | **53** (plus 4 shell) | `ls -1 *.py \| wc -l` |
| Lines of governance Python | **19,715** | `cat *.py \| wc -l` |
| Scripts that REFUSE something (guards and fences) | **21** | `ls *fence*.py *guard*.py` |
| Hooks wired into `settings.json` | **37** across 5 events | parsed from `settings.json` |
| Written on 2026-08-21 alone | **33 of 53** | `stat` per file |
| Wired to no hook and no launchd job | **25 of 57 (43%)** | cross-reference of `settings.json` + `LaunchAgents` |
| Of those, called by no other script either — dead | **10 files, 2,457 lines** | `rg -l` per file |
| Guard selftests currently failing | 2 of 36 — `branch-pr-guard.py` (exit 124), `idle-guard.py` (exit 1) | board row |

Two thirds of this machinery was written in a single day, and nearly half of it is connected to
nothing that runs by itself.

**The clearest single example of the pattern, from today.** The laws file is injected into every
session by `memory-loop.py` under a fixed character cap. On 2026-08-20 the cap lagged and silently
deleted six laws, including the one the founder had just asked for; the fix was to raise the number
by "one law of headroom". On 2026-08-21 a seventeenth law was added, went 863 characters over the
same cap, and was dropped again — the founder's newest law reached no session. The guard caught it
and the fix was to raise the number again. **A law costs roughly 2,050 characters, so every second
or third new law will spend another founder turn on the same edit.** The mechanism is correct, it
is tested, it is guarded — and it still produces the same failure on a schedule.

### E — Nothing merged has ever been checked against production

| Measure | Value |
|---|---|
| Pushes that were wrong | **22 of 96 CI runs red (23%)** |
| Live smoke runs that ever concluded green | **zero, ever** |
| Therefore merges verified against the running product | **none of them** |

The pipeline proves that code compiles and that tests pass. It has never once proved that the thing
a customer touches still works. `mumchimp.com` answers HTTP 200 in 949ms, and that is the entire
production evidence base.

### F — Decisions are recorded, and the record leaks

A decision log exists: `~/.claude/DECISIONS.jsonl`, 13 research rows and 6 standing decisions, with
tiers of source quality and a confidence field that requires two publishers before anything may be
called proven. It is genuinely good and it is the estate's best-designed artefact.

It leaks in two measured ways:

1. **Six research rows written today show `ang=0 gap=0`.** The `--angle` and `--gap` content was
   supplied and silently not persisted. The reasoning behind six findings is gone.
2. **Reading the file naively gives the wrong answer.** It is append-only, so the first occurrence
   of an id is the creation record, not the current state. Earlier today I reported a decision as
   "open, never answered" when it was closed, proven, with two sources. Only `decision-log.py --show
   <id>` folds the record correctly.

Six rulings are currently parked waiting on the founder, including whether to buy model credit and
whether per-check grounding verification is an acceptable operational cost.

### G — Agent coordination, which is the thing everyone assumes is broken, is measurably fine

Do not spend here. Two independent angles agree:

- Containment scoring across all 2,485 pairs of the 71 shared-board entries: 16 duplicate pairs,
  **0 of them cross-session**.
- Distinctive-token grouping, sharing no code or threshold with the first method: 6 of 32 subjects
  named by more than one session, **0 named by more than two**.

All 16 duplicates are a session repeating *itself* — 9 of them one timer-driven reporter. Fan-out
width is capped at 3 concurrent subagents by `agent-fleet-fence.py`, which is a deliberate cost
decision. The gap in parallel work is not coordination; it is deciding *which three things* deserve
the slots, which is cluster C.

## 4. What has already been tried, and what happened

| Attempt | What it was | Outcome |
|---|---|---|
| **17 written laws** | `~/.claude/CLAUDE.md`, ordered, each paid for by a named incident, injected at every session start | Genuinely load-bearing. Also 53,007 characters, over the injection cap, so the newest law is the one that gets dropped |
| **21 guards and fences** | PreToolUse hooks that refuse a bad action outright | The good ones work: `peer-loop-fence.py` cut cross-session duplicate discovery to 0. 2 of 36 selftests currently fail |
| **The founder board** | `founder_board.py`, every row generated by a command, never hand-written, UNKNOWN never zero | The design is right. Delivery was missing for a full day |
| **The prompt ledger** | captures every founder ask to JSONL | Capture works, read-back returns 0 |
| **The decision log** | research and decision rows with source tiers and a two-publisher bar | Best artefact here. Loses angle and gap content silently |
| **GitHub Issues as the tracker** | declared in `docs/WAYS_OF_WORKING.md:142` as the one system, *"No new tool"* | 0 of 71 issues adopted the convention |
| **A duplicate of an existing tool** | `session-recorder.py`, ~330 lines, written today without checking | `prompt-ledger.py` already existed and handled cases the new one dropped |
| **Framework adoption** | assessed twice | Already ruled: `d9861f649fe4` refused a multi-agent framework on MAST evidence; `d9c32e050f27` allows LangGraph for new coordination work only, not the engine core. **Nothing is installed** — `pip list` finds no CrewAI, LangChain, LangGraph, AutoGen, Temporal, Prefect or Dagster in any venv on this machine |

## 4b. Already decided — do not re-litigate these

Six standing decisions are on record in `~/.claude/DECISIONS.jsonl`. Read each with
`decision-log.py --show <id>`; the file is append-only, so grepping it returns the creation record
and not the current state.

| id | Question | Ruling |
|---|---|---|
| `d9c32e050f27` | Adopt LangGraph to replace the hand-rolled orchestration? | No for the engine core. Yes as the default for NEW agent-coordination work, behind one bounded seam |
| `d9861f649fe4` | How to build the founder's specialised autonomous personas? | Claude Code native subagents in `~/.claude/agents/*.md`, each with a DECISION-RIGHTS block. A multi-agent framework was refused on MAST evidence |
| `db722515427f` | What is spending $521/day? | Not the daemon and not the engine. Five concurrent interactive Claude Code sessions spent $515 of $516.79 |
| `def4a2402617` | How should the board be built? | A generator that runs commands and renders JSON plus HTML — `founder_board.py`. No hand-written status |
| `d55c5a07c276` | Where do the 31 uncaptured founder requirements go? | Appended as R23–R53 to `docs/REQUIREMENTS.md`, PR #558, with his words verbatim |
| `d95b87d204c5` | Where do the governance requirements go? | Appended from R23 onward, supplied to the file's owner rather than edited in their worktree |

## 5. What the research already established

Recorded in `~/.claude/research/HOW-THE-REAL-WORLD-SOLVED-THIS.md` (263 lines) and six closed
research rows, most rated `proven` against two publishers.

- **Documentation drift** is structural, not sloppiness. Code is exercised by compilers, tests and
  CI. Prose is exercised by nothing. The industry answer is to generate status from the system,
  never to write it — which is exactly what `founder_board.py` already does.
- **Naur, *Programming as Theory Building* (1985):** a program is a theory held by people. Code and
  documents are lossy recordings of it; reviving a dead theory from artefacts does not work. Rated
  single-angle only — the source PDF would not extract on this machine.
- **Little's Law and WIP limits:** lead time equals WIP over throughput. Task-switching costs
  20–40% (Rubinstein, Meyer & Evans 2001).
- **CD3, cost of delay divided by duration** (Reinertsen; SAFe's WSJF) is the established method for
  choosing what goes next under scarce capacity.
- **Decision records (ADRs)** are the established answer to re-litigating settled questions.
- **MAST**, 150 multi-agent traces: role disobedience accounts for 1.5% of failures; specification
  and coordination account for 76.5%.

**The conclusion those six rows share: every one of these is a constraint or a habit. Not one of
them is software you write.** That is the finding that most contradicts what this estate has spent
its effort on, and it is the reason a building freeze is currently in force.

## 6. Questions for you

1. Cluster D says the estate builds governance faster than it fixes process. Is that a tooling
   problem, an operating-model problem, or a consequence of the founder being the only reviewer?
2. What is the correct WIP limit for one founder and five agent sessions, and what enforces it —
   given that a guard is exactly the response cluster D says is failing?
3. Cluster A is a delivery problem, not a measurement problem. What is the right channel to a
   founder who is already in a terminal all day?
4. Cluster E: is "merged" an acceptable definition of done for a live storefront when live smoke has
   never once passed?
5. Cluster B: `docs/WAYS_OF_WORKING.md` mandates a labelling convention with 0% adoption. Enforce it
   or delete it — and what is the general rule for a written process nobody follows?
6. The laws file is 17 laws and 53,007 characters, re-read by every session on every start and after
   every compaction. At what point does a rules file stop being an asset?

## 7. How to check anything in this document

Every number above came from a command on this machine. The board is at `http://127.0.0.1:8787` and
each of its rows prints the command that produced it, so any line can be re-run. The workload queue
is `~/.claude/projects/-Users-chidionyema/checkpoints/WORKLOAD.md`. The decision record is
`~/.claude/DECISIONS.jsonl`, read with `decision-log.py --show <id>` and never by grep.

**One caveat, in the spirit of the thing.** The complaint-rate figures in section 2 come from a
single instrument, `founder_board.py`. Every other number in this brief has two independent angles
behind it. That one does not, and should be treated as a reading rather than a proof.
