# Estate LLM Cost Audit — 2026-08-06

**Status: AUDIT ONLY. Nothing has been fixed, changed, or enforced.**
No config was edited, no daemon touched, no provider rerouted. Every number below is
reproducible from the commands cited. Findings that are not yet proven are labelled
`HYPOTHESIS` with the exact check that would confirm or kill them.

Author: Claude (Opus 5). Method and raw scripts: `~/.claude/scripts/estate-cost.py`,
`~/.claude/scripts/cli-cache-experiment.py`.

---

## 0. The one-paragraph answer

The estate burned **$2,832.10 of Claude subscription value in 7 days**, and **$852.22 today
alone**. It is not spread across the estate — **99.4% of today's spend is Prospector**, and
Hermes, haworks, tie and signalengine together account for **$5.56**. The single largest line
item is **not model choice and not volume — it is cache transport waste**: the Prospector daemon
runs every `claude -p` call in a throwaway temp directory, so it re-writes a ~10,400-token
prompt cache at the 2.0x premium on every call and reads it back **0.72 times on average**.
A controlled experiment (§4) shows that reusing the directory makes an identical call
**8.6x cheaper with byte-identical output**. The second-largest item is **$264/day of
explicitly-non-critical work running on Opus** because the cheap provider is unfunded —
DeepSeek's balance is **−$0.22**. Meanwhile the spend guard that is supposed to be the
liability backstop can only see **4.4%** of what is actually being spent.

---

## 1. Method, and why these numbers can be trusted

Two independent accounting systems exist. This audit uses both and reconciles them.

| Source | What it is | Path |
|---|---|---|
| **Transcript reconstruction** | Cost recomputed from the `usage` block on every API response | `~/.claude/projects/*/*.jsonl` |
| **Prospector ledger** | The CLI's own self-reported `total_cost_usd` per call | `store/prospector.jsonl` |
| **Hermes telemetry** | Per-call cost rows written by the coordinator | `~/.hermes/coordinator.db` → `telemetry` |

Pricing constants for the reconstruction are taken verbatim from
`~/.claude/scripts/token-audit.py:33-43`, whose docstring documents that they reproduce Claude
Code's own ledger (`~/.claude.json` → `projects.<cwd>.lastModelUsage.costUSD`) to 7+ significant
figures for both Opus and Haiku. They are validated, not assumed:

```
input $5.00/MTok · cache_read 0.1x · cache_write 1.25x (5m TTL) / 2.0x (1h TTL) · output $25.00/MTok
```

Scope parsed: **84,369 transcripts / 2.4 GB / 24,260 deduped API requests**. Requests are
deduped per file by `message.id`, matching the validated tool's behaviour.

**Reproduce:** `python3 ~/.claude/scripts/estate-cost.py`

---

## 2. What was actually spent

### 2.1 Estate total — every dollar falls in 7 days

| day | $ |
|---|---|
| 2026-07-28 | 120.05 |
| 2026-07-29 | 283.55 |
| 2026-07-30 | 274.74 |
| 2026-07-31 | 611.98 |
| 2026-08-01 | 310.64 |
| 2026-08-05 | 396.18 |
| **2026-08-06 (today)** | **834.95** ¹ |
| **TOTAL** | **2,832.10** |

¹ $834.95 is the figure from the full-corpus pass; a later same-day pass measured $852.22 as
more calls landed during the audit. Both are cited where used; the drift is live spend, not
an error.

### 2.2 Today, by what is actually running

| group | sessions | requests | $ | % | $/session |
|---|---|---|---|---|---|
| **Prospector daemon** (`prospector_cli_cwd` temp dirs) | 1,926 | 1,936 | **510.98** | **60.0%** | 0.27 |
| **Prospector interactive** (coding sessions) | 40 | 3,587 | **335.68** | **39.4%** | 8.39 |
| haworks-platform | 3 | 17 | 3.22 | 0.4% | 1.07 |
| the-introduction-exchange | 1 | 13 | 1.34 | 0.2% | 1.34 |
| hermes-scripts | 24 | 24 | 0.78 | 0.1% | 0.03 |
| private-tmp | 2 | 2 | 0.22 | 0.0% | 0.11 |

**Prospector is 99.4% of today's estate spend.** Any cost programme that starts anywhere else
is optimising a rounding error.

### 2.3 By model, and by where the money goes (7 days)

| model | $ | % |
|---|---|---|
| claude-opus-5 | 2,581.36 | 91.1% |
| claude-fable-5 | 227.72 | 8.0% |
| claude-sonnet-5 | 23.03 | 0.8% |

| cost driver | $ | % |
|---|---|---|
| **cache_write** | **1,265.79** | **44.7%** |
| cache_read | 979.82 | 34.6% |
| output | 585.64 | 20.7% |
| raw_input | 0.85 | 0.0% |

**Only 20.7% of spend is the model generating anything.** 79.3% is moving context in and out.

---

## 3. FINDING 1 — The daemon pays a cold-cache penalty on every call (largest item)

Same model, same machine, same day:

| | daemon (fresh temp cwd) | interactive (stable cwd) |
|---|---|---|
| requests today | 1,936 | 3,594 |
| **$ per request** | **0.2650** | **0.0937** |
| cache_write share | **80.3%** ($412.19) | 23.9% ($80.53) |
| cache tokens **written** | 41,219,432 | 8,802,267 |
| cache tokens **read** | 29,643,830 | 377,527,835 |
| **cache reuse ratio** | **0.72x** | **42.89x** |

`$412.19 = 41,219,432 × $5.00 × 2.0 ÷ 1e6` **exactly** — so 100% of daemon cache writes are
1-hour-TTL writes at the **2.0x** premium, on a session that lives for seconds and is then
deleted. The daemon pays the *most expensive* cache tier for a cache it reads back **0.72
times**.

**Cause** — `prospector/claude_cli.py:119`:
```python
call_cwd = tempfile.mkdtemp(prefix="c_", dir=_NEUTRAL_CWD)
```
Claude Code derives its session identity from the cwd path, so a fresh directory means a cold
cache, every call, forever.

**This is not a mistake, and that matters for the fix.** The comment at
`claude_cli.py:113-118` records why it is there: concurrent `claude -p` processes sharing one
directory clobber each other's session state and degrade to non-JSON meta output — *"PROVEN
2026-07-02: parallel generation (concurrency=2) → 0/3 candidates, but serialized
(concurrency=1) → 2/3."* A correctness fix whose cost was never measured.

Note also `claude_cli.py:42` states the intent as *"Use a stable empty dir"* — the code at :119
does the opposite. The comment and the code disagree.

**Consequence beyond cost:** this minted **16,390 of the 16,479** directories under
`~/.claude/projects/` (3.0 GB), which is why every tool that walks that tree is slow.

---

## 4. EXPERIMENT — proving the cache penalty is recoverable

Hypothesis: reusing the cwd converts `cache_write` into `cache_read` with no output change.

Design: identical prompt, identical env-stripping, same binary, sequential calls. Arm A
reproduces `claude_cli.py:119` exactly (fresh `mkdtemp` per call). Arm B reuses one directory.
Measurement is the CLI's own `total_cost_usd`. Script: `~/.claude/scripts/cli-cache-experiment.py`.

**ARM A — fresh cwd per call (current daemon behaviour)**

| # | cost $ | cache_read | write_1h | out |
|---|---|---|---|---|
| 1 | 0.1121 | 15,273 | 10,422 | 10 |
| 2 | 0.1172 | 15,273 | 10,929 | 10 |
| 3 | 0.1172 | 15,273 | 10,933 | 10 |
| 4 | 0.1122 | 15,273 | 10,420 | 15 |

**ARM B — one stable cwd reused**

| # | cost $ | cache_read | write_1h | out |
|---|---|---|---|---|
| 1 | 0.1121 | 15,273 | 10,422 | 10 |
| 2 | 0.0899 | 18,147 | 8,057 | 10 |
| 3 | **0.0134** | 26,204 | **0** | 10 |
| 4 | **0.0132** | 25,695 | **0** | 15 |

**Result:** mean $0.1147 → $0.0572 (**2.01x**). At steady state, once warm,
**$0.1147 → $0.0133 — 8.6x cheaper, an 88% saving per call.** `write_1h` goes to zero and the
entire prefix is served from cache. Output was identical in every call.

**Quality risk: none.** Same model, same prompt, same output contract. This changes only where
the process runs.

**What is proven vs. what is projected.** Proven: an *identical* prompt is 8.6x cheaper warm.
Projected: real daemon prompts vary per call, so only the *shared prefix* caches. The
conservative floor uses only the measured per-call prefix rewrite:

```
10,400 tok × $5.00 × (2.0 − 0.1) ÷ 1e6 = $0.0988 saved per call
$0.0988 × 1,936 calls today                = $191/day floor
```
Ceiling, if prompts share more prefix than the floor assumes, approaches the measured 88%
(~$450/day). **Proven range: $191–$450/day, at zero quality cost.**

`HYPOTHESIS` — a pool of *N* stable directories (N = the concurrency cap, currently 2) preserves
the 2026-07-02 collision fix while capturing the cache benefit, because each concurrent process
still gets a distinct slug. **Check that would confirm or kill it:** run the daemon's real
generation batch at `PROSPECTOR_CLAUDE_CONCURRENCY=2` against a 2-slot pool and assert both
(a) candidate JSON parse rate matches the serialized baseline (2026-07-02: 2/3), and (b) mean
`total_cost_usd`/call drops. Not yet run.

---

## 5. FINDING 2 — $264/day of explicitly-non-critical work is running on Opus

Today's daemon spend, split by pipeline phase (`store/prospector.jsonl`, `phase` field):

| phase | calls | $ | $/call |
|---|---|---|---|
| `main` — generate / prescreen / score | 775 | **264.16** | 0.341 |
| `vetting` — the moat | 784 | 142.44 | 0.182 |

`CLAUDE.md` states generation, prescreen and scoring are non-critical and **may** run on cheap
models; only verdicts require a MOAT_PRIMARY brain. They are on Opus because of a fallback, not
a decision: the 2026-08-06 directive put `claude_cli` at the head of `_NONCRITICAL_ORDER`
(`prospector/run.py:194`) after DeepSeek returned HTTP 402 and cursor_cli hit its usage limit.

**The cheap path is unfunded, and that is measurable:**
```
$ curl -H "Authorization: Bearer $DEEPSEEK_API_KEY" https://api.deepseek.com/user/balance
HTTP 200
{"is_available":false,"balance_infos":[{"currency":"USD","total_balance":"-0.22", ...}]}
```
DeepSeek is not broken or rate-limited. Its balance is **negative $0.22**. At DeepSeek's rate
($0.27/MTok in, $1.10 out — `config.py:208`) the same 775 calls cost roughly **$7/day**.

**Quality risk: real, and NOT yet measured.** A promotion gate already exists for exactly this
decision — `prospector/golden.py`, invoked as
`python -m prospector.golden --operator deepseek --fixtures fixtures/golden_fixtures.json --runs 3`,
requiring `discrimination == 1.0` on all 3 runs. **It cannot be run today** because the account
is unfunded. Note also the fixture set is **12 cases** (`fixtures/golden_fixtures.json`) — a thin
bar for a decision worth $264/day; widening it should precede any promotion.

**Zero-cost alternative available now:** `ollama` is installed at `/usr/local/bin/ollama` with
5 local models (`qwen2.5-coder:7b`, `gemma3:4b`, `gemma3:1b`, `gemma2:2b`, `llama3.2`), and
`config.yaml` already has an adapter priced at $0.00/$0.00. Its quality on structured routing
is unproven and would need the same golden gate.

---

## 6. FINDING 3 — The spend guard is blind to ~96% of spend, and to its own failures

**6a. The cap only counts metered money.** `scheduler/guard.py:164-166` sums only ledger rows
tagged `event: "spend"`, which by design excludes Claude CLI usage
(`prospector/claude_cli.py:84-90`). 30-day totals:

| | $ |
|---|---|
| metered (what `daily_cap_usd: 20.0` enforces) | **71.97** |
| subscription (uncapped) | **1,548.10** |

**The liability backstop governs 4.4% of the burn.** The exclusion has a documented rationale
(`guard.py:36-39`: folding it in "would halt the daemon within about two hours of every day for
spend that is never invoiced") — that rationale is about *invoicing*, and it is why the
subscription leg has no ceiling of any kind.

**6b. Failed calls cost money and are invisible.** Because the daemon uses one cwd per call,
transcript sessions and `claude -p` invocations are 1:1 — which makes this decisive:

| | today |
|---|---|
| daemon calls with costed API requests (transcripts) | **1,926** |
| daemon calls recorded in `store/prospector.jsonl` | **1,568** |
| **unrecorded** | **358 (18.6%)** |
| reconstructed cost | $513.09 |
| ledger-reported cost | $408.20 |
| **cost invisible to the ledger** | **$104.89** |

$104.89 ÷ 358 = $0.293/call, consistent with the $0.265 measured mean — these are real calls.
`HYPOTHESIS` for the mechanism: calls that exit non-zero *after* the API request bill normally
but raise before reaching `_record_claude_usage` (`claude_cli.py:127-137` documents exactly this
exit-1 path). **Check:** instrument the exception path to emit a ledger row and confirm the
18.6% gap closes. Not yet run.

---

## 7. FINDING 4 — Zero delegation, estate-wide

Of **24,260 API requests** across all 84,369 transcripts, **0.0% ran on a subagent** — every
request was main-loop. `~/.claude/settings.json:17` pins `"model": "opus[1m]"` and there is no
subagent model default anywhere under `~/.claude/`.

This compounds Finding 1 from the other direction: interactive sessions average **$8.39 per
session** and hold 100–120K resident context that is re-billed on every turn at `cache_read`.
`cache_read` is 56.1% of interactive spend ($188.76 today).

The existing controls are **advisory only**: `context-guard-hook.py` injects a ~70-token nudge
at 85K/140K resident and `CLAUDE_CODE_AUTO_COMPACT_WINDOW=200000` triggers compaction, but
nothing blocks or routes. No hard limit exists at the harness layer.

---

## 8. FINDING 5 — Hermes is armed but not firing, and cannot see its own Claude spend

The prior sub-audit reported "daemon not running / current risk NONE". **That is wrong.**

```
$ launchctl list | grep hermes
68291  0    ai.hermes.gateway
82738  -15  ai.hermes.coordinator
$ ps -o pid,etime,command -p 82738
82738 13:08:23 .../Python /Users/chidionyema/.hermes/scripts/coordinator.py daemon
```

The coordinator has been running for **13h08m**. It is not spending because its provider is
dead — last `telemetry` row is `2026-08-02 15:58:36`, and DeepSeek 402'd on 08-05. Its Claude
Code volume collapsed from **1,588 requests/day (07-29) to 24 today**.

**Structural blind spot:** `coordinator.db` records `claude-cli:unknown` at **$0.0000** for 143
calls. Hermes' `$25/day` cap (`~/.hermes/config.yaml:614-615`) therefore governs only its
metered providers — the same shape as Finding 6a. Hermes' lifetime *recorded* cost is
**$0.0567**; its actual Claude Code consumption over 07-28→07-30 was **$240.37**, a **4,240x**
under-report. It is quiet today because it is broken, not because it is cheap. **If DeepSeek is
funded to fix Prospector, Hermes resumes at the same time** — its route chain
(`~/.hermes/scripts/route.py:121-125`) puts `claude-cli` at the head for coordinator and
strategist.

---

## 9. Inventory — everything on a timer that can spend

| job | cadence | status | spends? |
|---|---|---|---|
| `com.prospector.scheduler` | `--daemon --interval 7200`, `KeepAlive` | **was pid 79003; died during this audit** | **yes — the main burn** |
| `ai.hermes.coordinator` | 60s tick | **live, pid 82738, 13h** | yes, when provider funded |
| `ai.hermes.gateway` | KeepAlive | **live, pid 68291** | indirect |
| `ai.hermes.rsi` | daily 04:30 | gated by `meta/OFF_SWITCH` (present) | yes if ungated |
| `ai.hermes.progress` | 3600s | live | no LLM calls |
| `ai.hermes.watchdog` | 300s | live | no LLM calls |
| `com.tie.ai-review` | daily 02:00 | loaded, not running | yes (`consensus/engine.py`) |
| `com.haworks.continuous-review` | 21600s | loaded, not running | yes |
| `com.haworks.test-coverage` | 21600s | loaded, not running | yes |
| `com.signalengine.daemon` | KeepAlive | live, pid 5751 (5h24m) | **no — see §9.1** |
| `com.prospector.control-center` | KeepAlive | live, pid 77927 | no (Streamlit UI) |
| `com.prospector.backup` | daily 03:40 | loaded | no |
| `ai.hermes.cockpit`, `ai.hermes.ngrok` | — | `Disabled: True` | no |

Two plists are **unparseable XML** and were skipped: `ai.hermes.gateway.plist` (line 39) and
`com.prospector.watchdog.plist` (line 8). They are loaded and running regardless.

### 9.1 signalengine — audited, and clean

It is the only estate component on a **separate billing rail**: it calls the metered Anthropic
API directly (`signal_engine/agents/llm_features.py:99,104` — `anthropic.Anthropic(api_key=...)`),
not the Claude Code subscription. Its exposure is currently **zero**, on four independent checks:

- Default model is already the cheap tier: `claude-3-5-haiku-20241022`
  (`llm_features.py:44`), priced in-repo at $0.80/$4.00 (`llm_features.py:35`).
- It has its own per-day spend tracking (`llm_features.py:47-50` → `signal_engine/costs/cost_model.py`).
- **No `ANTHROPIC_API_KEY` is configured for it** — no `.env` in the project root.
- `daemon.log` contains **0** lines matching `llm|anthropic|claude`, and its last entry is
  `2026-06-18` — 7 weeks stale, despite the process being up 5h24m.

It also has a Gemini fallback path (`llm_features.py:215,298`). **Verdict: not a cost risk today,
but it is a live daemon that would begin spending metered money the moment a key is supplied.**

---

## 10. Ranked way forward (nothing here has been done)

Ordered by **$ per unit of quality risk**, which is the only ranking that matters when the
constraint is "cut cost without losing quality".

| # | action | $/day | quality risk | blocked on |
|---|---|---|---|---|
| 1 | Pool of N stable CLI cwds (§4) | **191–450** | **none** — proven identical output | collision regression test |
| 2 | Instrument the failed-call path (§6b) | 0 (visibility) | none | — |
| 3 | Subscription-aware ceiling on the guard (§6a) | caps tail risk | none | choosing the ceiling |
| 4 | Route `main` phase off Opus (§5) | **~257** | **real, unmeasured** | funding DeepSeek; widening the 12-case golden set |
| 5 | Fix Hermes' `claude-cli = $0.00` accounting (§8) | 0 (visibility) | none | — |
| 6 | Subagent delegation for recon (§7) | unquantified | low | — |
| 7 | Garbage-collect 16,390 litter dirs / 3.0 GB | 0 | none | falls out of #1 |

**#1 is the whole programme's centre of gravity**: it is the largest single saving *and* the
only large one with zero quality risk. It should be proven and landed before anything touches a
model choice. **#4 is the one that can degrade the product** — it must not ship on anything less
than a widened golden set at `discrimination == 1.0`.

---

## 11. What this audit does NOT establish

- **The pool-of-N design (§4) is a hypothesis**, not a measured result. The collision-regression
  check is specified but has not been run.
- **The failed-call mechanism (§6b) is a hypothesis.** The 18.6% / $104.89 gap is measured; the
  explanation is not.
- **No cheap-model quality measurement exists.** DeepSeek and MiniMax have never been run
  through the golden gate because the account is unfunded. Any claim that they are "good enough"
  — or that they are not — is currently unprovable.
- **The 12-case golden set may itself be too thin** to detect regression at this stake.
- **The 7-day window may be an artifact of transcript retention**, not of when spending started.
  Nothing older than 2026-07-28 survives in `~/.claude/projects/`.
- **Two plists could not be parsed** (§9), so their schedules are unverified.
- **State changed mid-audit**: `store/scheduler/PAUSE` was removed and daemon pid 79003 exited
  while this was being written, by something outside this session. The repo working tree is also
  being modified concurrently. Nothing in this document was caused by it, but the live-state
  lines are a snapshot, not a steady state.

---

## 12. Reproducing this

```bash
python3 ~/.claude/scripts/estate-cost.py           # §2 estate roll-up
python3 ~/.claude/scripts/cli-cache-experiment.py 4  # §4 experiment (costs ~$0.70)
python3 ~/.claude/scripts/token-audit.py <slug>    # per-session detail
sqlite3 ~/.hermes/coordinator.db "select model,count(*),sum(cost) from telemetry group by 1;"
cd ~/Documents/code/prospector && .venv/bin/python tools/spend_today.py
```
