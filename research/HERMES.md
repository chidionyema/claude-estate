# HERMES — audit, current state, and how to join it to the Claude Code estate

Requirement R28. Written 2026-08-21. Read-only audit: nothing was started, stopped or modified.

Every claim below carries the command or `file:line` that produced it. Anything I could not
measure is marked `unverifiable` rather than asserted.

## The requirement, in the founder's own words

> "eed to thik ehaustivelt about challenges founder ca face leaaving autononous workker s while
> renove and how not to lose connection to thwhts goig on, we have herness agebt also so needs
> tying tinto the borader project work also . this is an oversight and a nissing piece of the whole
> pule , hernes aget needs to be fully enbedded into the tean and project. look at the hernes
> project, deep researcj hernes online and see how o nake this a trie naster piece beause we can
> leverage it to really super chregae things , not an opportunity to be niseed , needs the biggest
> brains on this"

> "the hernes prohec needs cleanup and audiit current state and inprovenent also so jon the tiw
> tother into a super coherent systen"

> "a lot of kow legecan be shared bewennthen" / "skills and runboks sharing between then" /
> "super inprotant"

> "herhens has pernanent nennory also" / "dig ddp into how this work"

> "and rnenebr portblity outsidee of cloaud cod ei scrucial" / "portability also nneans nodel
> agnostic"

> "need to c=baseline everyhtig and conpare whgen proted" / "ti find gaps"

## The short version

Hermes is not a side project and it is not bespoke. It is **Nous Research's open-source Hermes
agent** (MIT, `hermes-agent/LICENSE:1-3` — "Copyright (c) 2025 Nous Research"), vendored as a git
submodule inside the founder's own private `hermes-config` repo. The founder is a contributor to
the upstream with 118 commits.

It already has, in production and on real traffic, four things the Claude Code governance layer
does not have at all: a real permanent memory store with full-text search, genuine model
agnosticism across four vendors, a scheduler, and multi-channel paging that reaches the founder
when he is away from the laptop. That last one is the literal answer to the founder's opening
sentence.

It is also **half-dead right now**: 10 of its 14 launchd jobs are not loaded, and it has not run an
agent session in over 2 days.

---

## 1. WHAT IT IS — measured

### Two repositories, one tree

**`~/.hermes` is a symlink.** The real directory is `~/Documents/code/hermes`, and the link was
created on 2026-08-20 18:23:

```
$ ls -ldi ~/.hermes
301421613 lrwxr-xr-x 1 chidionyema staff 40 20 Aug 18:23 /Users/chidionyema/.hermes
                                                          -> /Users/chidionyema/Documents/code/hermes
$ stat -f '%i %z %N' ~/.hermes/state.db ~/Documents/code/hermes/state.db
228279016 131833856 /Users/chidionyema/.hermes/state.db
228279016 131833856 /Users/chidionyema/Documents/code/hermes/state.db
```

Same inode, so this is one store reached by two paths — **not** the two-clone trap that bit the
prospector estate. Worth knowing anyway: every plist, every script and every `HERMES_HOME` default
resolves through that symlink, and anything deriving a path from `__file__` will report the
`Documents/code/hermes` side while config reports the `~/.hermes` side. The two are the same bytes
today; a tool that compares the two strings will still say they differ.

The real directory is a git repo.

```
$ git -C ~/.hermes remote -v
origin	https://github.com/chidionyema/hermes-config.git (fetch)
$ git -C ~/.hermes rev-list --count HEAD
605
```

Inside it, `hermes-agent/` is a submodule pointing at the public upstream:

```
$ git -C ~/.hermes/hermes-agent remote -v
origin	https://github.com/NousResearch/hermes-agent.git (fetch)
backup	https://github.com/chidionyema/hermes-agent.git (fetch)
$ git -C ~/.hermes/hermes-agent rev-list --count HEAD
11990
$ git -C ~/.hermes/hermes-agent log --format='%an' -2000 | sort | uniq -c | sort -rn | head -4
 424 Teknium
 211 Brooklyn Nicholson
 161 teknium1
 118 chidionyema
```

The upstream remote is live and reachable (`git ls-remote --exit-code origin HEAD` returns
`fc9cbc872d8050c22f1192b16bc5ff4aed471e10`).

So the split is: **`hermes-config` = the founder's estate automation** (605 commits, his own
scripts, cron jobs, policies, capability receipts). **`hermes-agent` = Nous Research's agent
framework** (11,990 commits, MIT, upstream-maintained).

That distinction matters for everything below. Improvements to `hermes-config` are ours to make.
Improvements to `hermes-agent` should go upstream as PRs or stay as a thin local layer, or every
`git submodule update` fights us.

### Size

| Component | Measure | Command |
|---|---|---|
| `hermes-config` tracked files | 10,966 | `git -C ~/.hermes ls-files \| wc -l` |
| `hermes-config` own Python (`scripts/`) | 46,775 LOC | `find ~/.hermes/scripts -name '*.py' \| xargs wc -l` |
| `hermes-agent` Python files | 11,498 | `find ~/.hermes/hermes-agent -name '*.py' -not -path '*/.venv/*' -not -path '*/__pycache__/*'` |
| `hermes-agent` Python LOC | 1,031,390 | same, piped to `xargs wc -l` |
| `state.db` (session store) | 131.8 MB | `ls -la ~/.hermes/state.db` |
| `capability_receipts.jsonl` | 9.25 MB, 22,682 lines | `wc -l ~/.hermes/state/capability_receipts.jsonl` |
| Skills (`~/.hermes/skills`) | 112 `SKILL.md` | `find ~/.hermes/skills -name SKILL.md \| wc -l` |
| Skills (`hermes-agent/skills`) | 73 | same pattern |
| Skills (`hermes-agent/optional-skills`) | 100 | same pattern |
| Cron jobs | 37 | `python3 -c` over `~/.hermes/cron/jobs.json` |

**285 skills in total.** The Claude Code side has 2 user skills (`~/.claude/skills/`: `graphify`,
`model-routing`).

### What upstream says it is

Fetched from https://github.com/NousResearch/hermes-agent on 2026-08-21:

> "The self-improving AI agent built by Nous Research. It's the only agent with a built-in learning
> loop."

Upstream's own feature list: persistent memory with periodic nudges and FTS5 session search;
agent-curated skill creation, "compatible with agentskills.io standard"; CLI plus Telegram,
Discord, Slack, WhatsApp, Signal and Email through a unified gateway; a built-in cron scheduler;
subagent spawning; and model support described as "any model you want".

### What actually runs

```
$ launchctl list | grep -i hermes
1713	0	ai.hermes.keepawake
13797	0	ai.hermes.lease-guard
1705	0	ai.hermes.idle-engine
-	0	ai.hermes.runaway-reaper
```

Two live daemons:

- `~/.hermes/scripts/idle_engine.py --daemon --interval 120` (pid 1705)
- `~/.hermes/scripts/launchd_receipt.py --label ai.hermes.lease-guard -- /bin/bash
  ~/.hermes/scripts/lease-guard.sh` (pid 13797)

Entry points worth knowing: `~/.local/bin/hermes` (the CLI), `hermes-agent/gateway/run.py` (the
multi-platform gateway), `hermes-agent/hermes_cli/` (subcommands), `~/.hermes/scripts/` (the
founder's 46k lines of estate automation).

---

## 2. CURRENT STATE / HEALTH

### 10 of 14 launchd jobs are not loaded

There are 14 non-backup `ai.hermes.*` plists in `~/Library/LaunchAgents/`. Only 4 are loaded:

| Job | State | Runs | Last exit |
|---|---|---|---|
| `ai.hermes.keepawake` | running | 1 | 0 |
| `ai.hermes.lease-guard` | running | 42 | 0 |
| `ai.hermes.idle-engine` | running | 1 | 0 |
| `ai.hermes.runaway-reaper` | running | 48 | 0 |
| `ai.hermes.coordinator` | **NOT LOADED** | — | — |
| `ai.hermes.gateway` | **NOT LOADED** | — | — |
| `ai.hermes.progress` | **NOT LOADED** | — | — |
| `ai.hermes.rsi` | **NOT LOADED** | — | — |
| `ai.hermes.selfcheck` | **NOT LOADED** | — | — |
| `ai.hermes.watchdog` | **NOT LOADED** | — | — |
| `ai.hermes.submodule-backup` | **NOT LOADED** | — | — |
| `ai.hermes.cockpit` | **NOT LOADED** | — | — |
| `ai.hermes.ngrok` | **NOT LOADED** | — | — |
| `ai.hermes.otto-server` | **NOT LOADED** | — | — |

Measured with `launchctl print gui/501/<label>` per job.

**The gateway is one of the dead ones.** That is the Telegram/Discord/Slack/WhatsApp/Signal/Email
delivery path — the exact mechanism that would keep the founder connected to autonomous workers
while he is away. It is installed, it is written, and it is switched off.

`ai.hermes.watchdog`, `ai.hermes.selfcheck` and `ai.hermes.rsi` being down means the system that is
supposed to notice Hermes is unhealthy is itself part of what is unhealthy.

I did not load any of them. That is a founder decision (LAW 11 — several of these send messages to
real channels, and `ngrok` opens a public tunnel).

### No agent session in over 2 days

```
$ sqlite3 'file:~/.hermes/state.db?mode=ro&immutable=1' \
    "select datetime(min(started_at),'unixepoch'), datetime(max(started_at),'unixepoch') from sessions;"
2026-06-18 10:54:54|2026-08-19 07:01:00
```

Last session started 2026-08-19 07:01. It is now 2026-08-21 10:27. The learning loop the upstream
tagline is built around has not turned in 51 hours.

### Why `ai.hermes.lease-guard` shows as failing

This one is subtle and the answer is not "it exits nonzero". It does not.

```
$ launchctl print gui/501/ai.hermes.lease-guard | grep -E 'state|runs|last exit'
	state = running
	runs = 42
	last exit code = 0
```

Three separate things are true, and only the third is what put it on the founder board.

**(a) It writes a shell parse error into stderr every 5 minutes.**

`~/.hermes/logs/lease-guard.err` is 27 identical lines plus two budget warnings:

```
/Users/chidionyema/.hermes/.env: line 467: Chrome.app/Contents/MacOS/Google: No such file or directory
```

Cause: `lease-guard.sh:18-20` sources the env file with bash —

```bash
set -a
[ -r "$HERMES/.env" ] && . "$HERMES/.env"
set +a
```

— and `.env:467` sets `AGENT_BROWSER_EXECUTABLE` to an **unquoted path containing spaces** (I read
only the key name and the line length, 91 bytes; I did not read the value). Bash word-splits it, so
`AGENT_BROWSER_EXECUTABLE=/Applications/Google` becomes an assignment prefix and
`Chrome.app/Contents/MacOS/Google` becomes the command it tries to run. Two consequences: the noise,
and `AGENT_BROWSER_EXECUTABLE` silently holds a truncated, wrong value for every process that
sources this file. The fix is one pair of quotes in `.env:467`.

**(b) It runs 4x to 16x over its time budget.**

`~/.hermes/state/capability_receipts.jsonl`, last two lease-guard records:

```json
{"script":"lease-guard.sh","duration_s":117.6,"exit_code":0,"budget_s":30.0,"over_budget":true}
{"script":"lease-guard.sh","duration_s":471.75,"exit_code":0,"budget_s":30.0,"over_budget":true}
```

`ai.hermes.lease-guard.plist` sets `StartInterval` 300, so a 471.8s run **overlaps the next run**.
The reason it hangs is visible in `~/.hermes/logs/lease-guard.log`, which is a tight poll loop:

```
HELD BY OTHER  fly (185e352b061638, pid 697, id b3624093), 292s left
HELD BY OTHER  fly (185e352b061638, pid 697, id b3624093), 348s left
...
```

Fly holds the leader lease — which is **correct and healthy**. `lease-guard.sh:28-36` documents
exactly that: exit 1 means "someone else holds it", and the script deliberately translates 0 and 1
both to exit 0 so launchd does not record a working fence as a failing job. But it sits there
polling for up to 8 minutes while doing so.

**(c) The actual board verdict is `UNDOCUMENTED`, not `FAILING`.**

From the alert text embedded in the `com.prospector.process-audit` receipt:

```
ai.hermes.lease-guard: UNDOCUMENTED, absent from PROCESS_INVENTORY.md
  -- declared, installed, loaded pid=-; exit=0; last receipt 0h ago
```

So the fix for the board entry is a documentation line in `PROCESS_INVENTORY.md`, and the fixes for
the real defects are the quoting in `.env:467` and either raising the receipt budget above 300s or
capping the poll in `lease-guard.sh`. Three different fixes for what looked like one red light.

### Other degradation found on the way

- The same process-audit alert reports `agent memory: PARTITIONED across 3 store(s): 454 memories
  in one, 1 in another` — that is the **Claude Code** side, not Hermes, but it is the same class of
  problem and is called out in §5.
- `~/.hermes/state/` holds ~1,000 entries, most of them `capability_receipts.jsonl.<ts>.gz`
  rotations from a single 45-minute window on 2026-08-19 (roughly 40 rotations, ~725 KB each). A
  rotation loop fired repeatedly. Low severity, but it is ~30 MB of near-identical archives.
- `~/.hermes/hooks/` is **empty** (`ls -la` shows only `.` and `..`). Hermes has no hook layer at
  all. See §5.
- `~/.hermes/cron/jobs.json` has 15 backup copies alongside it. There is no pruning.

---

## 3. PERMANENT MEMORY — how it actually works

This is the section the founder asked to dig deep into. There are **three separate layers**, and
they do not talk to each other.

### Layer 1 — the curated store: `~/.hermes/memories/`

Two flat markdown files, entries separated by a `§` on its own line
(`hermes-agent/tools/memory_tool.py:59`, `ENTRY_DELIMITER = "\n§\n"`).

| File | Purpose | Size now | Entries |
|---|---|---|---|
| `MEMORY.md` | agent's own notes: environment facts, project conventions, tool quirks | 4,157 chars | 13 |
| `USER.md` | what the agent knows about the founder: preferences, style, expectations | 2,580 chars | 4 |

**Backend:** plain files. No database, no vectors at this layer. Writes are atomic
(`utils.atomic_replace`) and take an `fcntl` lock — `memory_tool.py:29-47` imports `fcntl`, falling
back to `msvcrt` on Windows. Lock files exist on disk: `MEMORY.md.lock`, `USER.md.lock`.

**Scope:** profile-global, not per-project. `memory_tool.py:53-57`:

```python
def get_memory_dir() -> Path:
    """Return the profile-scoped memories directory."""
    return get_hermes_home() / "memories"
```

The scoping key is `HERMES_HOME`. Switch profile, get a different memory. There is no per-repo or
per-session partition — one store for everything Hermes knows.

**Char caps, and a correction.** `memory_tool.py:124` defaults to `memory_char_limit=3300,
user_char_limit=2750`. On those numbers `MEMORY.md` at 4,157 chars would be 857 over and every
`add()` would be refused at `memory_tool.py:328`.

That is **not** what is live. `agent_init.py:1129-1130` reads the limits from config:

```python
memory_char_limit=mem_config.get("memory_char_limit", 2200),
user_char_limit=mem_config.get("user_char_limit", 1375),
```

and `~/.hermes/config.yaml:354-360` sets:

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  write_approval: false
  memory_char_limit: 6000
  user_char_limit: 4000
  provider: ''
```

So the live caps are **6000 / 4000**. `MEMORY.md` is at 4,157/6,000 (69%, 1,843 chars headroom) and
`USER.md` at 2,580/4,000 (65%). Writes are **not** currently being refused. Two angles disagreed
here — the code default and the config — and the config wins; I nearly shipped the wrong one.

The overflow risk is real but historical, and Hermes has already written itself a memory about it,
`MEMORY.md` entry 7, verbatim:

> Memory writes stop SILENTLY at the char cap: add() refuses and the background review drops the
> lesson. Check headroom before blaming the writer.

**A live defect: the store is full of near-duplicates.** The last five entries of `MEMORY.md`, all
stamped `[verified: 2026-08-18]`, are the same lesson written five times:

> Before starting a new task, close or explicitly hand off every open loop from the current one...
> Every task must reach a named terminal state (done/blocked/escalated) with explicit handoff...
> Every opened loop must reach a named terminal (done/blocked/handed-off) before starting new work...
> Before ending a task, either close each open loop or explicitly flag it as blocked with an owner...
> Before ending a task, close every opened loop or state explicitly why it can't close...

Those five entries are ~40% of a 6,000-char budget spent on one idea. There is no dedup on the
write path. Given a hard char cap, a writer with no dedup will eventually evict real knowledge to
make room for paraphrases of one lesson. This is the single most valuable fix in the memory layer.

**How a memory is written.** Two paths.

1. *Automatic, and this is the interesting one.* `hermes-agent/agent/background_review.py` —
   after every turn, `AIAgent.run_conversation` may call `spawn_background_review`, which forks a
   daemon thread running a second `AIAgent` over the conversation snapshot and asks it "should any
   skill/memory be saved or updated?". From the module docstring:

   > The fork inherits the parent's live runtime (provider, model, base_url, credentials, cached
   > system prompt) so it hits the same prefix cache and uses the same auth. It runs with a tool
   > whitelist limited to memory and skill management tools; everything else is denied at runtime.

   That is a genuinely good design: the reflection step costs almost nothing because it reuses the
   prefix cache, it cannot do damage because the tool whitelist is enforced at runtime, and it
   never touches the main conversation. **Claude Code has no equivalent.** Memory here is written
   by a human deciding to write it.

2. *Manual.* A single `memory` tool with an `action` parameter — `add`, `replace`, `remove`, `read`
   (`memory_tool.py:297,349,414`). `replace`/`remove` match on a short unique substring rather than
   IDs, which is what makes it usable by a model.

`config.yaml:357` sets `write_approval: false`, so the background reviewer writes without asking.

**How a memory is recalled.** Also two paths, and they are different mechanisms.

1. *Frozen snapshot into the system prompt.* `memory_tool.py:11-14`:

   > Both are injected into the system prompt as a frozen snapshot at session start. Mid-session
   > writes update files on disk immediately (durable) but do NOT change the system prompt -- this
   > preserves the prefix cache for the entire session. The snapshot refreshes on the next session
   > start.

   This is why the char cap exists at all: the whole store goes into every prompt. The cap is a
   token-budget decision, stated in chars because `memory_tool.py:17` notes "char counts are
   model-independent" — a portability decision, and a correct one.

2. *Semantic retrieval, for cron and task injection.* `~/.hermes/scripts/retrieval/embedding_recall.py`
   (636 LOC) builds an embedding index over `MEMORY.md` entries **and** over `~/.hermes/policies/`:

   - Model: all-MiniLM-L6-v2, ONNX, 384-dim. `embedding_recall.py:26` points at
     `~/.hermes/models/miniLM-onnx`, and the model is present — `onnx/model.onnx`, 90,405,214
     bytes. `numpy 2.4.3` and `onnxruntime 1.23.2` both import in
     `~/.hermes/hermes-agent/venv/bin/python`, so this path is live, not falling back.
   - Cosine similarity, `top_k=5`, `threshold=0.25`–`0.3` (`embedding_recall.py:362-363,515`).
   - A TF-IDF encoder (`embedding_recall.py:182`) is the graceful fallback when onnx is missing.
   - **Self-query routing** (`embedding_recall.py:436`, `route_query`) decides whether a task needs
     memory, policies, or both, and adjusts the policy threshold by up to `-0.15` on a domain
     mismatch. That is smarter than anything on the Claude Code side.
   - Every retrieval is logged to `~/.hermes/logs/injection-log.jsonl` — 10,531 entries, 4.0 MB.
     Last record:

     ```json
     {"timestamp":"2026-08-20T16:53:41","task":"--query Create a new operator command 'otto audit'...",
      "routing":{"need_policies":true,"need_memory":true,"policy_threshold_boost":0.0},
      "retrieved_memory":5,"retrieved_policies":5,"embedding_threshold":0.25,"total_index_size":15}
     ```

   **`total_index_size: 15`.** The semantic index covers 15 items — 13 memory entries plus policies.
   The machinery is a 636-line embedding retriever with self-query routing, and the corpus it
   searches would fit on one screen. The engine is far larger than its fuel tank.

### Layer 2 — the session store: `~/.hermes/state.db`

This is where the real volume is, and it is a proper database.

```
$ ls -la ~/.hermes/state.db
-rw-r--r--@ 1 chidionyema staff 131833856 20 Aug 17:53 /Users/chidionyema/.hermes/state.db
```

Path is `DEFAULT_DB_PATH = get_hermes_home() / "state.db"` (`hermes-agent/hermes_state.py:108`).

> Measurement caveat, and it is worth recording: `find ~/.hermes -maxdepth 2 -name '*.db'` returned
> **nothing** while this 131 MB file sat at depth 1. A direct `[ -e ... ]` test found it. An earlier
> `ls ~/.hermes/*.db ~/.hermes/state/*.db ~/.hermes/cache/*.db` also returned nothing, because zsh
> aborts the entire command when any one glob fails to match. Two instruments said absent; the file
> is there. Do not conclude "no database" from a `find` on this tree.

Tables and live row counts, read with `sqlite3 'file:...?mode=ro&immutable=1'`:

| Table | Rows |
|---|---|
| `sessions` | 924 |
| `messages` | 9,595 |
| `messages_fts` | 9,595 |
| `state_meta` | 99 |
| `compression_locks` | 0 |
| `schema_version` | 1 |

Plus `messages_fts_trigram` and the FTS shadow tables.

`sessions` schema (`hermes_state.py:514`) carries far more than a transcript:

```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY, source TEXT NOT NULL, user_id TEXT, model TEXT, model_config TEXT,
    system_prompt TEXT, parent_session_id TEXT, started_at REAL NOT NULL, ended_at REAL,
    end_reason TEXT, message_count INTEGER, tool_call_count INTEGER,
    input_tokens INTEGER, output_tokens INTEGER, cache_read_tokens INTEGER,
    cache_write_tokens INTEGER, reasoning_tokens INTEGER, cwd TEXT,
    billing_provider TEXT, billing_base_url TEXT, billing_mode TEXT,
    estimated_cost_usd REAL, actual_cost_usd REAL, cost_status TEXT, ...
```

Note `parent_session_id` — subagent lineage is recorded in the schema. And per-session cost and
token accounting is a first-class column, not a bolt-on.

Full-text search: `messages_fts` is an FTS5 virtual table (`hermes_state.py:602`) kept in sync by
`AFTER INSERT` triggers on `messages` (`hermes_state.py` trigger `messages_fts_insert`). There is a
**second** trigram FTS table for CJK substring search (`hermes_state.py:626-631`) — the default
unicode61 tokenizer cannot do it. Failure is handled rather than silent:
`_is_fts5_unavailable_error` / `_warn_fts5_unavailable` (`hermes_state.py:773-783`) warn when the
SQLite build lacks FTS5 instead of quietly returning no results.

Lifetime totals across the 924 sessions:

```
input_tokens        15,249,677
output_tokens        1,194,269
cache_read_tokens  298,801,698
```

**Does it survive a restart?** Yes. Everything durable is on disk: `state.db` (SQLite, with a
documented WAL concern for network filesystems at `hermes_state.py:206`), `memories/*.md` (atomic
writes under `fcntl` locks), `state/capability_receipts.jsonl` (append-only). Nothing load-bearing
is RAM-only. The only in-process state is the frozen prompt snapshot, which by design is rebuilt
from disk at the next session start.

**Eviction / TTL / compaction:** there is a `compression_locks` table (0 rows) and
`agent/conversation_compression.py` / `agent/context_compressor.py` handle in-session context
compression. I found **no TTL or eviction on `state.db` itself** — it has grown to 131.8 MB over
two months and nothing prunes it. `unverifiable`: whether any cron job vacuums it (37 jobs, I did
not read all of them).

### Layer 3 — pluggable external providers (installed, not switched on)

`hermes-agent/agent/memory_provider.py` (296 LOC) is an ABC for swappable memory backends, with a
documented lifecycle:

```
initialize() / system_prompt_block() / prefetch(query) / sync_turn(user, asst)
get_tool_schemas() / handle_tool_call() / shutdown()
```

plus optional hooks including `on_session_end(messages)`, `on_pre_compress(messages)`,
`on_memory_write(...)` and `on_delegation(task, result, **kwargs)` — that last one is parent-side
observation of subagent work, i.e. a parent can remember what its subagents learned. Claude Code
has nothing like it; a subagent's findings die with the subagent unless the parent writes them down.

Five providers ship in `hermes-agent/plugins/memory/`: `supermemory`, `hindsight`, `retaindb`,
`openviking`, `holographic` (the last has its own `store.py`, `retrieval.py`, `holographic.py`).

`MemoryManager` enforces a **one-external-provider limit** "to prevent tool schema bloat and
conflicting memory backends" (`memory_provider.py:5-9`).

**Currently active: none.** `config.yaml:360` is `provider: ''`. The builtin file store is what
runs.

### Verdict on permanent memory

The architecture is genuinely good and better than what Claude Code has: automatic write via a
cheap forked reviewer, semantic recall with self-query routing, FTS5 over 9,595 real messages,
per-session cost accounting, a clean provider ABC with subagent-observation hooks.

The **content** is thin. 13 curated entries, five of which are the same lesson. 15 items in the
semantic index. Meanwhile the Claude Code side has 683 hand-written memory files across all
projects (457 in the prospector store alone) — real, hard-won, incident-derived knowledge, sitting
in a system with no semantic search, no automatic writer, and no dedup.

**Each side has exactly what the other is missing.** That is the whole opportunity.

---

## 4. SKILLS AND RUNBOOKS

### The good news: the formats are already compatible

A Hermes skill is a directory with `SKILL.md` carrying YAML frontmatter.
`~/.hermes/skills/supervised-process-contract/SKILL.md:1-5`:

```yaml
---
name: supervised-process-contract
description: How to supervise long-running daemons in Otto (launchd + thin wrapper, exit-cause
  captured by parent, circuit breaker, stderr split, OOM hypothesis first)
version: 1.1.0
---
```

A richer one, `~/.hermes/skills/external-audience-writing/SKILL.md:1-11`:

```yaml
---
name: external-audience-writing
description: "Write documents for audiences OUTSIDE the project ... Load when the user asks for
  help with a CV, cover letter, LinkedIn bio, ..."
version: 1.0.0
author: LUX Engine
license: MIT
metadata:
  hermes:
    tags: [writing, audience, cv, bio, linkedin, readme, pitch, vocabulary, translation]
---
```

A Claude Code skill is a directory with `SKILL.md` carrying YAML frontmatter.
`~/.claude/skills/graphify/SKILL.md:1-4`:

```yaml
---
name: graphify
description: "Use for any question about a codebase, its architecture, file relationships, ..."
---
```

**Same file name, same format, same two required keys.** Upstream confirms this is deliberate —
the GitHub page states skills are "compatible with agentskills.io standard".

### The mismatch is smaller than expected, and it is three things

1. **Extra keys.** Hermes adds `version`, `author`, `license`, and `metadata.hermes.tags`. Claude
   Code's loader ignores unknown frontmatter keys, so **a Hermes skill can be dropped into
   `~/.claude/skills/` as-is.** The reverse also works; the Hermes skill would simply have no
   version or tags.

2. **Directory nesting.** Hermes allows a category directory holding several skills —
   `~/.hermes/skills/apple/` contains `DESCRIPTION.md` and `apple-productivity/SKILL.md`, so the
   skill is at depth 2. Claude Code expects `<skills-root>/<name>/SKILL.md` at depth 1. A flatten
   step is needed one way; a category-index step the other way.

3. **Description semantics.** Claude Code descriptions are written as *load triggers* ("Use when
   the user asks..."). Hermes descriptions are often written as *summaries*. Both sides parse
   either, but a summary-style description loads badly in Claude Code because the router matches on
   it. Rewriting is a per-skill judgement, not a mechanical conversion.

**No bridge or converter exists on disk today.** The closest thing is
`hermes-agent/optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py`, which
migrates from a different agent entirely (it reads `memory_char_limit` / `user_char_limit` at
lines 770-771, so it does handle the memory store). It is a working precedent for the shape of a
converter, not a converter for our case.

### What each side actually has

**Hermes has that Claude Code does not:**

- 285 skills against 2. Named examples that map straight onto founder laws:
  `supervised-process-contract` (daemon supervision — LAW 12 territory),
  `dropped-ball-prevention` (explicitly "Otto's hard rules from the 16-dropped-balls session" —
  this is LAW 9 and LAW 16 written from the other side), `safe-commit-protocol`,
  `task-resilience`, `estate-ground-truth-probe` (this is the state-probe rule),
  `lux-proof-driven-development` (this is LAW 2), `skill-creator`, `mcp-builder`.
- **10 policies** in `~/.hermes/policies/` as machine-readable JSON — `pol-20260618-001.json`,
  `pol-auto-fix-coordinator.json`, `pol-shadow-gap-*.json`. These are enforceable rules with an
  escalation chain, checked automatically against every task by
  `policy_enforcer.check_and_fire_policies(task_text, context="injection")`
  (`scripts/memory_retrieval.py:63-69`). A policy is retrieved semantically alongside memory and
  *fires*. The Claude Code equivalent of a policy is a paragraph in `CLAUDE.md`.
- **37 cron jobs** (`~/.hermes/cron/jobs.json`) — named ones include `daily-self-reflection`,
  `daily-strategist-audit`, `ci-watchdog-daily`, `Otto daily digest (9am)`, "Run health check on
  all projects", "Summarize today's activity across all projects".
- `capabilities.json`, 43.8 KB — a registry of what the system claims it can do, graded against
  `capability_receipts.jsonl`. A capability that produces no receipt is raised as an alarm
  (`scripts/launchd_receipt.py:1-30` docstring, and `capability_audit.py:143-190` is the matcher).

**Claude Code has that Hermes does not:**

- **683 memory files** of incident-derived knowledge, one lesson per file with a `MEMORY.md` index.
- **46 guard scripts** in `~/.claude/scripts/` — `hang-guard.py`, `peer-loop-fence.py`,
  `jargon-guard.py`, `pr-freeze.py`, `agent-fleet-fence.py`, `one-branch-fence.py`,
  `dupe-work-fence.py`, `context-guard-hook.py`, `idle-guard.py`, `goal-guard.py`,
  `decision-log.py`, `founder_board.py`, `estate_spend.py`, and more. These are PreToolUse/Stop
  hooks that *refuse* an action. Hermes' `~/.hermes/hooks/` is empty.
- **16 numbered, ordered laws** with worked examples and explicit tie-breaks.
- `DECISIONS.jsonl` (85 entries) and `ESTATE_BOARD.jsonl` (73 entries) — a decision log and a
  cross-session board.

The single most shareable thing in each direction:
**Hermes → Claude Code: the 285 skills and the policy-fires-on-task mechanism.**
**Claude Code → Hermes: the 683 memories and the 46 refusing guards.**

---

## 5. OVERLAP WITH THE CLAUDE-CODE GOVERNANCE LAYER

### Where they duplicate each other

Both have independently built, and separately maintain:

| Concern | Claude Code | Hermes |
|---|---|---|
| Rules for the agent | 16 laws in `~/.claude/CLAUDE.md` | `SOUL.md`, `DEVELOPMENT_PHILOSOPHY.md`, `policies/*.json`, `INVARIANTS` in `scripts/memory_retrieval.py:26-32` |
| Cost metering | `~/.claude/scripts/estate_spend.py` | `sessions.actual_cost_usd` in `state.db`, `scripts/cost_policy_mgmt.py`, `scripts/claude_usage_limit.py` |
| Health probes | `.state-probe` per project | `scripts/self-audit.py`, `scripts/reliability_report.py`, `capabilities.json` + receipts |
| Exception / incident record | memory files | `EXCEPTIONS_LOG.md`, `AGENT_AUDIT_*.md` (4 dated audits) |
| Watchdogs | `hang-guard.py`, `idle-guard.py` | `scripts/estate_watchdog.py`, `ci-watchdog.py`, `reliability-watchdog.sh` |

The duplication is not free. `estate_spend.py:100-101` already treats Hermes as a separate owner:

```python
if "hermes" in slug:
    return "hermes"
```

— so the estate spend meter knows Hermes exists and bills it separately, but Hermes' own
per-session cost columns in `state.db` are a second, independent accounting of the same money. Two
ledgers, neither reconciled against the other. `unverifiable`: whether they agree.

The `estate_spend.py:15` comment records a known discrepancy already:

> Hermes' `coordinator.db` records `claude-cli` at $0.0000 for 143 calls

### Where Hermes lacks what Claude Code has

- **No hook layer.** `~/.hermes/hooks/` is empty. Everything in Hermes is advisory: a policy fires
  and *tells* the agent, it does not *refuse*. Claude Code's 46 guards refuse — the fleet cap
  refused two of my own subagent calls during this very audit, and `hang-guard.py` refused an
  unbounded `grep -r`. That is the difference between a documented trap and a guarded trap.
- **No ordered laws.** Hermes has invariants and policies but no tie-break. LAW ordering exists
  precisely because an unordered rule set fires the wrong rule at the wrong moment.
- **No cross-session peer board.** Hermes sessions do not appear to have an `ESTATE_BOARD.jsonl`
  equivalent. `unverifiable` — I did not exhaustively search `state_meta` (99 rows).
- **Thin memory content**, as measured in §3.

### Where Hermes is genuinely better — port these INTO Claude Code

Being honest about this, because it is the actionable half.

1. **Automatic memory write via a forked background reviewer**
   (`hermes-agent/agent/background_review.py`). Claude Code memory is written only when an agent
   remembers to write it, which means the lessons that get recorded are the ones from sessions that
   had spare attention — exactly the wrong sample. Hermes reflects after *every* turn, on the
   prefix cache, with a runtime-enforced tool whitelist. This is the single best idea in the
   codebase.

2. **Semantic recall with self-query routing** (`scripts/retrieval/embedding_recall.py:436`).
   Claude Code injects a flat `MEMORY.md` index of 457 one-line summaries and hopes the right one
   is noticed. Hermes embeds, routes, thresholds, and returns top-5 — and logs every retrieval to
   `injection-log.jsonl` so the retrieval quality is itself measurable. Claude Code cannot currently
   answer "was the right memory recalled?" at all.

3. **Capability receipts as a first-class contract**
   (`scripts/launchd_receipt.py`, `capabilities.json`, `capability_receipts.jsonl`, 22,682 rows).
   The docstring states the problem exactly:

   > a job that signs no receipt is invisible to the audit that decides what is broken

   It wraps any launchd job, passes stdout/stderr and the exit code through unchanged, and appends
   one signed receipt. It also grades **artifact count**, so a job that exits 0 and produced
   nothing is caught — the "exit-0-did-nothing" class. Claude Code has no equivalent, and the
   estate has repeatedly been bitten by exactly this.

4. **Policies as machine-readable JSON that fire on task text**, rather than prose in a rules file.
   A law that a machine can match against the current task is closer to a guard than a paragraph is.

5. **Per-session cost and token accounting in the schema** (`sessions.input_tokens`,
   `cache_read_tokens`, `actual_cost_usd`, `billing_provider`). LAW 14 asks for cost numbers;
   Hermes already has the table.

6. **Multi-channel delivery.** The gateway reaches Telegram, Discord, Slack, WhatsApp, Signal and
   Email. This is the direct answer to "how not to lose connection to what's going on" while away.
   Claude Code's reach ends at the terminal.

---

## 6. PORTABILITY AND MODEL AGNOSTICISM

**Hermes is not tied to Claude, and this is proven on real traffic rather than claimed.**

`~/.hermes/config.yaml:1-4`:

```yaml
model:
  provider: minimax
  base_url: https://api.minimax.io/anthropic
```

The live default is **MiniMax**, reached through an Anthropic-*compatible* endpoint. Anthropic here
is a wire protocol, not a vendor dependency.

29 provider plugins ship in `hermes-agent/plugins/model-providers/`:

```
alibaba  alibaba-coding-plan  anthropic  arcee  azure-foundry  bedrock  copilot  copilot-acp
custom  deepseek  gemini  gmi  huggingface  kilocode  kimi-coding  minimax  nous  novita
nvidia  ollama-cloud  openai-codex  opencode-zen  openrouter  qwen-oauth  stepfun  xai
xiaomi  zai
```

`anthropic` is one entry in that list. `ollama-cloud` and `custom` mean self-hosted is a
first-class option.

And the session store proves it has actually run on all of them:

```
$ sqlite3 'file:~/.hermes/state.db?mode=ro' "select model,count(*) from sessions group by 1 order by 2 desc;"
(null)|707
deepseek-v4-pro|68
MiniMax-M3|66
deepseek-chat|18
claude-haiku-4-5-20251001|16
standardcompute|13
anthropic/claude-opus-4-6|8
gpt-5.3-codex|7
gemini-2.5-flash|2
```

**Eight named models across five vendors, in one system, on real sessions.** Billing is tracked per
provider:

```
minimax|102 sessions|$0.7339
deepseek|22 sessions|$5.5206
custom|22|$0.00   openai-codex|7|$0.00   bedrock|4|$0.00
```

Design decisions that support portability, each with a citation:

- Memory limits are in **characters, not tokens**, "because char counts are model-independent"
  (`memory_tool.py:17`). A token cap would have to be retuned per tokenizer.
- The memory store is **markdown files**, not a vendor format. It ports by `cp`.
- The provider abstraction is a **plugin directory**, so adding a vendor is a directory, not a
  code change.
- `config.yaml` has dedicated `openrouter:`, `bedrock:` and `auxiliary:` blocks (lines 114, 118,
  129) — an auxiliary model (used for curator and background review) can be a *different, cheaper*
  provider than the main one.
- Deployment targets per upstream: local, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox.

**Conclusion for the pinned objective.** The founder's standing objective is porting the governance
layer off Claude Code. Hermes is not a candidate substrate to be evaluated — it is a substrate that
is already running, already model-agnostic, already multi-channel, already has the persistence
layer, and is MIT-licensed with the founder as an upstream contributor. The governance layer
(16 laws, 46 guards, 683 memories) is the part that is Claude-Code-shaped. Hermes is the part that
is not.

The port is therefore not "rebuild Hermes' capabilities in a portable way". It is **"move the laws,
guards and memories onto Hermes"**.

---

## 7. THE BASELINE TABLE

Capability matrix as of 2026-08-21. `~` means partial. Every cell is measured above.

| # | Capability | Claude Code | Hermes | Gap / who wins |
|---|---|---|---|---|
| 1 | **Permanent memory (content)** | 683 files, 457 in prospector store | 13 entries + 4 user entries | **CC wins 40x.** Hermes' store is nearly empty |
| 2 | **Permanent memory (mechanism)** | flat md + hand-written index | md store + FTS5 + 384-dim embeddings + provider ABC | **Hermes wins.** CC has no search at all |
| 3 | **Automatic memory write** | none — human writes it | forked background reviewer every turn, tool-whitelisted | **Hermes only.** Port to CC |
| 4 | **Semantic recall / routing** | none (flat index into prompt) | `embedding_recall.py`, self-query routing, top-5 @ 0.25 | **Hermes only** |
| 5 | **Memory dedup** | none | none — 5 duplicate entries measured | **Neither.** Real gap on both sides |
| 6 | **Session persistence + search** | JSONL transcripts, no index | `state.db` 131.8 MB, 924 sessions, 9,595 msgs, FTS5 + trigram | **Hermes only** |
| 7 | **Peer messaging / shared board** | `ESTATE_BOARD.jsonl` 73, `SendMessage`, `peer-loop-fence.py` | none found (`unverifiable`) | **CC only** |
| 8 | **Guards / hooks that REFUSE** | 46 scripts, PreToolUse/Stop | `hooks/` is **empty**; policies advise only | **CC wins decisively** |
| 9 | **Ordered laws with tie-break** | 16 numbered laws, lower wins | `SOUL.md` + 5 invariants, unordered | **CC only** |
| 10 | **Machine-readable policies firing on task** | none (prose in CLAUDE.md) | 10 JSON policies, `check_and_fire_policies()` | **Hermes only** |
| 11 | **Skills** | 2 user skills | 285 `SKILL.md` | **Hermes wins 140x.** Same format |
| 12 | **Runbooks / procedures** | laws + memories, prose | skills + `AGENT_AUDIT_*.md` ×4 + `EXCEPTIONS_LOG.md` | ~ both |
| 13 | **Scheduling / cron** | none native | 37 jobs, `cron/jobs.json` + 14 launchd plists | **Hermes only** |
| 14 | **Paging / multi-channel delivery** | terminal only | Telegram, Discord, Slack, WhatsApp, Signal, Email — **gateway NOT LOADED** | **Hermes only, switched off** |
| 15 | **Cost metering** | `estate_spend.py`, budget json | per-session cost/token columns in schema | ~ both, **unreconciled** |
| 16 | **Decision log** | `DECISIONS.jsonl` 85 | `EXCEPTIONS_LOG.md` (prose) | **CC only** (structured) |
| 17 | **Capability receipts / did-it-actually-work** | none | 22,682 receipts, artifact-count graded | **Hermes only.** Port to CC |
| 18 | **Model agnosticism** | Claude only | 29 provider plugins, 8 models used live | **Hermes wins decisively** |
| 19 | **Self-hosted / offline option** | no | `ollama-cloud`, `custom`, local ONNX embeddings | **Hermes only** |
| 20 | **Subagent lineage recorded** | none | `sessions.parent_session_id` + `on_delegation` hook | **Hermes only** |
| 21 | **Health self-audit** | `.state-probe` per project | `self-audit.py`, `reliability_report.py`, `capabilities.json` — **watchdog/selfcheck NOT LOADED** | **Hermes richer, currently off** |
| 22 | **Context compression** | `/compact`, 1200-word budget | `context_compressor.py`, `conversation_compression.py`, `compression_locks` | ~ both |

**Read the table this way.** Of 22 capabilities: Claude Code wins outright on 4 (memory content,
guards, ordered laws, decision log). Hermes wins outright on 10. Both are weak on 2 (dedup, cost
reconciliation). The two systems are close to complementary, which is why the founder's instinct
that this is "a missing piece of the whole puzzle" is correct.

**The gap that matters most for the port:** rows 8 and 9. Everything Claude Code uniquely has is
*enforcement* — guards that refuse, laws that order themselves. Everything Hermes uniquely has is
*substrate* — memory, persistence, scheduling, delivery, model choice. Enforcement is portable
(they are Python scripts reading stdin and exiting nonzero). Substrate is not (it took 11,990
commits). **Port the enforcement onto the substrate, not the other way round.**

---

## 8. TOP 5 IMPROVEMENTS, RANKED

Ranked by value per hour, with the measured reason for each.

### 1. Feed the 683 Claude Code memories into Hermes' retrieval layer
**Effort: ~half a day. Highest value on the page.**

Measured reason: Hermes has a 636-line semantic retriever with self-query routing, ONNX embeddings
and per-retrieval logging, and it is searching **15 items** (`injection-log.jsonl`, last record,
`total_index_size: 15`). Claude Code has **683 memory files** of incident-derived knowledge with no
search over them at all. The engine and the fuel are in different buildings.

Both are markdown. `embedding_recall.py:29` reads a single `MEMORY_FILE`; the change is to accept a
list of roots and index `~/.claude/projects/*/memory/*.md` alongside `~/.hermes/memories/MEMORY.md`.
This also fixes the `PARTITIONED across 3 store(s)` alarm the process audit is already raising,
because a single index over all roots makes the partitioning invisible to the reader.

Do this first because it is the one change that makes both systems immediately better and requires
no new mechanism on either side.

### 2. Fix `ai.hermes.lease-guard`, three separate defects
**Effort: under an hour. It is the live red light.**

- `.env:467` — quote the `AGENT_BROWSER_EXECUTABLE` value. Measured: 27 identical parse errors in
  `logs/lease-guard.err`, and the variable currently holds a truncated path for every process that
  sources that file.
- `lease-guard.sh` — bound the poll. Measured: runs of 117.6s and 471.8s against a `StartInterval`
  of 300, so runs overlap. Either cap the wait or raise the receipt budget above 300s; the current
  30s history budget guarantees an `over_budget` flag on every contended run.
- Add `ai.hermes.lease-guard` to `PROCESS_INVENTORY.md`. Measured: the board verdict is literally
  `UNDOCUMENTED, absent from PROCESS_INVENTORY.md`, not a failure.

Founder decision needed on nothing here — all three are safe, local edits.

### 3. Decide which of the 10 dead launchd jobs come back, starting with the gateway
**Effort: 1 hour to decide, minutes to apply. Founder decision required.**

Measured: 10 of 14 jobs are `NOT LOADED`, including `gateway`, `watchdog`, `selfcheck`, `rsi` and
`coordinator`. Hermes has run no agent session since 2026-08-19 07:01 — 51 hours.

The gateway is the one that answers the founder's opening question. Telegram/Discord/Slack/WhatsApp/
Signal/Email delivery is written, installed and switched off; while it is off, an autonomous worker
has no way to reach him when he is away from the laptop.

This is LAW 11 work — several of these jobs message real channels and `ngrok` opens a public
tunnel, so it is not mine to switch on. What is needed is a decision per job: back on, or delete
the plist. Ten plists sitting loaded-never make the health picture unreadable for whoever looks
next.

### 4. Port capability receipts into the Claude Code estate
**Effort: ~2 hours. It closes a class the estate keeps rediscovering.**

Measured: `scripts/launchd_receipt.py` wraps any job, passes exit code and streams through
unchanged, and appends one receipt carrying `exit_code` **and `artifact_count`** — so a job that
exits 0 and produced nothing is caught. 22,682 receipts exist. The docstring names the incident
that paid for it: `com.prospector.backup` with `runs = 9, last exit code = 1`, "Nine consecutive
failed runs, 237 dossiers never uploaded, and nothing raised".

The Claude Code side has no equivalent, and "a guard that grades a proxy grades nothing" and "an
audit that crashes reports nothing" are both already memory files there. Same class, already
solved on the other side of the machine.

### 5. Add dedup to the memory write path, then share the skills
**Effort: ~2 hours for dedup, ~half a day for the skill bridge.**

Dedup, measured: five entries in `MEMORY.md` stamped `2026-08-18` say the same thing about closing
open loops, consuming roughly 40% of a 6,000-char budget. The store is at 4,157/6,000. With a hard
cap and no dedup, a writer that paraphrases will eventually evict real knowledge. The embedding
index is already loaded in-process — a cosine check against existing entries before `add()` is a
few lines at `memory_tool.py:297`.

Skill sharing, measured: 285 Hermes skills against 2 Claude Code skills, and **the formats already
match** — both are `SKILL.md` with YAML frontmatter carrying `name` and `description`, and upstream
targets the agentskills.io standard. Claude Code ignores Hermes' extra `version`/`author`/`license`/
`metadata.hermes.tags` keys. The only real work is flattening the category directories (Hermes
allows `skills/apple/apple-productivity/SKILL.md` at depth 2; Claude Code wants depth 1) and
rewriting summary-style descriptions into load-trigger style. No converter exists today;
`optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py` is the nearest
precedent for its shape.

---

## Appendix — traps hit during this audit, recorded so the next reader does not pay again

- **`find` silently missed a 131 MB file.** `find ~/.hermes -maxdepth 2 -name '*.db'` returned
  nothing while `~/.hermes/state.db` sat at depth 1. `[ -e "$f" ]` found it immediately. Do not
  conclude "no database" from a `find` on this tree.
- **zsh aborts the whole command when any glob fails to match.**
  `ls ~/.hermes/*.db ~/.hermes/state/*.db ~/.hermes/cache/*.db` printed only
  `no matches found: .../cache/*.db` and evaluated *none* of the three. The first two would have
  matched.
- **`rg -r` is `--replace`, not recursive.** `rg -rn 'def add|MEMORY.md' <dir>` replaced every match
  with the literal string `n`, producing nonsense output that looked like real code
  (`n_provider(self, ...)`). ripgrep is recursive by default; there is no `-r` to add.
- **The code default and the config disagreed on the memory cap** (3300 vs 6000). The config wins
  via `agent_init.py:1129`. Checking only `memory_tool.py:124` would have produced a confident,
  wrong claim that memory writes are currently being refused.
- **`~/.hermes` is the symlink, not `~/Documents/code/hermes`.** I tested the direction that felt
  obvious (`ls -ld` on the `Documents` path, which is a real directory) and concluded they were the
  same directory. They are, but via a link pointing the other way. `ls -ldi` on *both* paths, or
  comparing inodes of a file inside, is the check that actually answers it.

## Sources

- [NousResearch/hermes-agent on GitHub](https://github.com/NousResearch/hermes-agent) — fetched
  2026-08-21 for the upstream description, license, feature list and model-agnosticism claim.

All other claims in this document are measured on this machine with the commands shown.
