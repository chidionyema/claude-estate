# How the real world already solved the five things we keep failing at

Written 2026-08-21. Founder instruction, verbatim: *"we need to stop buildngaythig untill our
judgent inproves on what is wroth building and ewhat problens already solved out there in the
real wprld"*, and *"ny evidence is tha in repeaint gnyself and we keep naking the sane rookie
istakes"*.

This file contains **no proposal to build anything**. It is the outside evidence, per R37
(research means the internet, reputable sources, every source and search documented) and R39
(open-source and existing solutions are part of research).

Tags: `[PRIMARY]` = the originating work. `[SECONDARY]` = a summary of it that I read.
`[MEASURED]` = a number I produced on this estate today with the command shown.

---

## The five complaints, and what the established answer is

| Founder's words | The established name for it | The established answer | Is it code? |
| --- | --- | --- | --- |
| *"we clain our olutions work"* | documentation drift | make the status claim executable | no — a command |
| *"we dont retien any contents"* | theory loss (Naur, 1985) | the theory cannot be written down; keep continuity instead | **no — and this one says documents cannot fix it** |
| *"no sense of urgeny or what is priority"* | no ranking function | Cost of Delay ÷ Duration (CD3) | no — arithmetic |
| *"our spine is brroken"*, too much at once | WIP overload | a WIP limit, from Little's Law | no — a number that refuses |
| *"we keep naking the sane rookie istakes"* | decision amnesia | decision records, **read before deciding** | no — a habit |
| *"writing nnore ccode is not the solutio"* | build vs buy | build only at the differentiating edge | it is a gate |

**Every one of these is a constraint, not a system.** Not one of them is software you write. That
is the strongest single finding here and it agrees with the founder's instinct.

---

## 1. Claims without evidence — this is a named, solved problem

The mechanism, stated plainly by the documentation-drift literature `[SECONDARY]`:

> *"Code changes are continuously exercised by compilers, automated tests, and continuous
> integration, so drift is caught quickly. Documentation changes are not, so documentation is
> updated manually, opportunistically, and often incompletely."*

That is exactly what happened to us today. `[MEASURED]` `docs/REQUIREMENTS.md:65` asserts R32 is
*"3 of 8 governance pieces ported"*. Nothing exercises that sentence, so nobody noticed it was
wrong. Counting harness dependencies in the three named pieces:

    rg -c 'transcript|\.jsonl.*session|CLAUDE_SESSION_ID|settings\.json|hook' ~/.claude/scripts/<f>

| piece | lines | lines depending on Claude Code internals |
| --- | --- | --- |
| `prompt-ledger.py` | 633 | 34 — it parses Claude Code transcript JSONL |
| `goal-guard.py` | 668 | 15 |
| `decision-log.py` | 614 | 1 |

Only the decision log is genuinely harness-free. **The honest number is 1 of 8, not 3 of 8.**
And `[MEASURED]` the eight pieces are enumerated in no document at all, so R32 reports progress
toward a target that was never written down.

The arXiv work on AI verification contracts puts the same rule in one line `[SECONDARY]`:

> *"An AI verification contract is not real until the model-facing schema and the runtime
> validator can fail the same way."*

**We already have this rule and did not apply it.** `~/.claude/CLAUDE.md` says *"State is a
probe, not a paragraph"* and *"The live answer to 'is it done / deployed / working?' is a
command, never a sentence."* `REQUIREMENTS.md` is 55 sentences with a status column and no probe.

---

## 2. Context loss — the finding that contradicts our whole approach

Peter Naur, *Programming as Theory Building*, 1985 `[PRIMARY, read as [SECONDARY] — the PDF would
not extract on this machine; see Gaps]`.

Naur's argument: a program is not its text. It is a **theory** held in the minds of the people who
built it. The code and the documentation are lossy representations, and the theory *cannot be
rebuilt from them alone* once the people are gone. His term for the attempt is **revival**, and
his claim is that revival fails.

> *"The theory of the program cannot be rebuilt completely only from the code, documentation, and
> other artifacts, without the presence of developers who worked on the program."* `[SECONDARY]`

> *"Documentation and tests can support the reconstruction of theory, or at least prevent its
> rapid decay... But documentation is a finger, not the moon; it can orient, never replace. The
> more we confuse the finger with the moon, the more we sink into a paradox: we preserve the texts
> and lose the program."* `[SECONDARY]`

**Why this matters more to us than to a normal team.** A human team loses its theory over years,
when people leave. Every agent session here loses it in hours, at every compaction and every
session death. We are the extreme case of Naur's problem.

**And our response has been the exact thing Naur says does not work.** `[MEASURED]` 99 markdown
files in `docs/`, 26 of them programme documents, plus 4,704 lines of tracking machinery
(`prompt-ledger.py` 633, `decision-log.py` 614, `action_items.py` 320, `founder_board.py` 1,134,
`pr-reactor.py` 548, `pr_triage.py` 281, `close-guard.py` 506, `goal-guard.py` 668). That is a
very large attempt to write the theory down. Naur's paper is the reason it keeps not being enough,
and it is why the founder still has to repeat himself.

What the literature says actually preserves theory: **continuity of the people**, and failing
that, deliberate handover *with the outgoing person present*. Documents orient a newcomer. They do
not carry the theory.

---

## 3. Priority — there is a standard arithmetic and we do not use it

Don Reinertsen, *Principles of Product Development Flow* `[PRIMARY, cited via [SECONDARY]]`.

**CD3 = Cost of Delay ÷ Duration.** Rank by the score, highest first. It is a scheduling rule from
queueing theory, and it maximises value delivered by a scarce capacity `[SECONDARY]`. SAFe
repackaged it as Weighted Shortest Job First.

`[MEASURED]` This estate has no ranking function anywhere. `docs/BACKLOG.md` is a hand-ordered
list. Nothing computes an ordering, so "what is most urgent" is answered by whoever is asking
loudest — usually the founder, in the same words as last time.

---

## 4. The broken spine — this is WIP overload, and it has a formula

**Little's Law**: `Lead Time = WIP ÷ Throughput` `[PRIMARY: Little, 1961; read via [SECONDARY]]`.

With throughput roughly fixed, the *only* way to shorten lead time is to reduce the number of
things in flight. The reported case studies `[SECONDARY]`:

- a team with **34 stories in progress** completing 11.3/week cut cycle time **47%** by limiting
  WIP to 18;
- mobile teams limiting parallel feature branches to three cut cycle times **20–30%**.

And the cost of the switching itself `[PRIMARY: Rubinstein, Meyer & Evans, 2001, *Journal of
Experimental Psychology*; read via [SECONDARY]]`: task-switching costs **20–40% of productive
capacity**, through the "resumption lag" of reloading context.

> *"High WIP doesn't just divide capacity — it shrinks it, as the capacity you're dividing becomes
> smaller because you divided it."* `[SECONDARY]`

`[MEASURED]` on this estate today:

    gh issue list --state open --limit 200 --json number,labels,createdAt,updatedAt

    open issues                : 71
    carrying the 'claimed' label: 0 of 71
    carrying no label at all    : 63 of 71
    closed in the last 24h      : 15
    closed in the last 7 days   : 31
    median idle                 : 1 day
    concurrent interactive sessions: 5, spending $515 of a $516.79 day

So the spine is **alive** — 31 closures a week is real throughput. What is absent is any limit on
how much is open at once, and any signal of who is on what. This is textbook WIP overload with
textbook symptoms: duplicate work, nothing feeling finished, and the founder repeating himself.

The relevant number is not "how many trackers do we have". It is **WIP**, and it is uncapped.

---

## 5. Repeating mistakes — we have the mechanism and do not read it

The decision-record literature `[SECONDARY]` names our exact failure:

> *"Organizations constantly re-solve the same problems in isolation, with one team debating
> build-vs-buy for a component while another team had the same debate six months ago and made a
> decision they now regret."*

Its term is **decision amnesia**, and the stated value of a decision record is *"preventing
re-litigation"*.

`[MEASURED]` We have the record: `~/.claude/DECISIONS.jsonl`, 86 rows, injected at every session
start. And here is today's failure inside it — research row **`r43ab013bc79`**, logged
2026-08-21T03:25:

    question: "What open-source and existing systems already implement role-specialised
               multi-agent teams, and should we adopt rather than build?"
    searches: []      sources: []      finding: None      status: open

**That is the founder's question, asked 14 hours before he asked it again.** It was captured and
never answered. The mechanism works; the closing does not. `prompt-ledger.py`'s own docstring says
the same thing about founder prompts: capture works, closing never happens.

The literature's answer is not a better tool. It is the habit of **reading the record before
deciding**, and the discipline of **closing a record with a finding**.

---

## 6. Build vs buy — the sentence that answers the founder directly

From the build-vs-buy discipline literature `[SECONDARY]`:

> *"If you do not have the discipline to deliver and operate it well, building it is not an asset
> you are creating — it is a liability you are signing up for."*

> *"The build vs buy decision is not a one-time choice but the start of a five-to-seven-year
> operational commitment that runs long after launch day."*

> COTS and SaaS deploy **40–60% faster** than custom alternatives (Altexsoft, 2024).

The standing guidance is: **build only at the differentiating edge**, buy or adopt everywhere
else. A workload tracker is not our differentiating edge. Neither is a session recorder.

`[MEASURED]` The build-first reflex, twice today, by me: I wrote `session-recorder.py` (~330
lines, now a live Stop hook) when `prompt-ledger.py` already existed and did the job better — it
reads the mid-turn `queue-operation` rows that mine drops. Then I started on a workload tracker
before checking. Both are the failure this section describes.

---

## The OSS survey the founder asked for, done

Two curated indexes read, ~74 orchestrators listed. Filtered on the estate's own rule (R32:
portable outside Claude Code, and model-agnostic):

| Tool | Licence | Runtime | agent-agnostic | tracker-agnostic |
| --- | --- | --- | --- | --- |
| Sortie | **not stated** | Go + SQLite | yes | yes |
| Cyrus | not stated | — | yes | Linear/GitHub/GitLab/Slack |
| Contrabass | not stated | — | yes | Linear/GitHub/local |
| Omnigent | Apache-2.0 | — | 7 harnesses | none |
| OMK | MIT | — | provider-neutral | none |
| Symphony | Apache-2.0 | Elixir | Codex only | yes |

Three of the six state **no licence**, and this estate has already rejected a tool on exactly that
ground (`claude-code-telegram`, R39).

**Everything returned by the "Claude Code skill/plugin" search fails R32 by construction** — the
backlog plugins, Task.md, the progress-tracker skill. They *are* the harness.

And a prior standing ruling already covers adopting a framework: **`d9861f649fe4`** refused
CrewAI/AutoGen-style adoption, because the MAST taxonomy of 150 real multi-agent traces puts
role-disobedience at 1.5% while design and coordination account for 76.5% — a framework selling
role fidelity fixes our smallest problem at 15x the token cost.

**The honest conclusion of the survey: the gap these tools fill is not the gap we have.**
`~/.claude/research/DIVIDE-AND-CONQUER-EVIDENCE.md` measured coordination as already solved — 2,485
board pairs compared, **0 cross-session duplicate discoveries**. Buying an orchestrator would be
buying a solution to a problem we do not have, which is the same error as building one.

---

## Gaps in this research — stated, not hidden

1. **Naur's paper was not read in the original.** The PDF downloaded but would not extract on this
   machine (no `Quartz`, no `pdftotext`). Every Naur quotation above is `[SECONDARY]`. The primary
   is at `pages.cs.wisc.edu/~remzi/Naur.pdf` and the argument is short — worth reading directly
   before anything is decided on it.
2. **Reinertsen and Little were read via summaries**, not the books.
3. **The WIP case-study numbers (47%, 20–30%) come from vendor blogs**, not peer-reviewed work.
   Treat them as directionally right, not as measurements.
4. **The six OSS tools were read from index listings, not from their repositories.** No licence
   was confirmed at source. Nothing should be adopted on this table alone.
5. **Rubinstein, Meyer & Evans (2001) is a real peer-reviewed paper**, but I read a summary of it.

## The searches that produced this

    "Claude Code skills marketplace task tracking backlog single source of truth plugin"
    "open source agent workload tracker GitHub issues sync multiple AI coding sessions 2026"
    "work in progress limits Little's Law evidence throughput too many parallel work items research"
    "build versus buy discipline software 'not invented here' why teams rebuild existing solutions"
    "institutional memory engineering organisations repeating same mistakes architecture decision records"
    "Peter Naur programming as theory building 1985 why documentation cannot preserve program knowledge"
    "Reinertsen cost of delay divided by duration CD3 prioritisation evidence single queue"
    "documentation drift status claims not verified executable specification continuous verification Google SRE"

Fetched in full: `github.com/bradAGI/awesome-cli-coding-agents`,
`github.com/andyrewlee/awesome-agent-orchestrators`, `pages.cs.wisc.edu/~remzi/Naur.pdf` (failed
to extract).
