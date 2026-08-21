# Token framework — measured, not asserted

Written 2026-07-30. Every number here comes from
`python3 ~/.claude/scripts/token-audit.py -Users-chidionyema` (per-request ledger truth).
**Re-run it before trusting any figure below.** This file replaces the `TOKEN-PLAYBOOK.md`
citation in `~/.claude/CLAUDE.md`, which pointed at a file that does not exist.

## The measurement (8 sessions, $67.92 total)

| session | reqs | floor | median ctx | peak | cacheR | $ | **$/req** |
|---|---|---|---|---|---|---|---|
| e0a9eb3b | 17 | 35,507 | 57,098 | 62,604 | 868,635 | 1.18 | **0.069** |
| d5044ede | 42 | 35,832 | 64,679 | 98,765 | 2,597,832 | 2.95 | **0.070** |
| 02742eb3 | 9 | 36,931 | 47,467 | 53,350 | 384,875 | 1.75 | 0.194 |
| 0aa9f3bc | 85 | 36,035 | 95,889 | 151,462 | 8,153,526 | 8.25 | 0.097 |
| e1e931c3 | 102 | 36,527 | 98,281 | 164,247 | 9,491,153 | 9.81 | 0.096 |
| f2317195 | 138 | 35,486 | 95,273 | 164,145 | 13,575,494 | 12.06 | 0.087 |
| 5e24e317 | 55 | 36,393 | 105,108 | 277,374 | 4,881,374 | 9.04 | 0.164 |
| 288cc574 | 236 | 34,238 | 107,584 | 165,989 | 24,659,193 | 22.90 | 0.097 |

## Three findings that overturn the obvious moves

**1. Cost per request is roughly FLAT (~$0.09), not quadratic.** Median context plateaus near
95–107k rather than growing without bound, so total cost ≈ `requests × $0.09`. The lever is the
*number of requests*, which nothing in the old playbook targeted.

**2. Median context sets the per-request rate, and it is ~35% cheaper at half the size.**
57–65k median → $0.069–0.070/req. 95–107k median → $0.087–0.097/req.

**3. Trimming CLAUDE.md is a ~2.5% lever, NOT a headline one.** Both CLAUDE.md files total 14,459
chars ≈ 3.6k tokens. Against a 95k median that is 2.5% of each cached read ≈ **$0.17 on a $12
session**. Floor size looks big in isolation (35k) but is only ~37% of median context, and it is
cache-read at $0.50/MTok. *Do not spend a session optimising this.* Recorded because the intuition
"the floor is huge, cut the floor" is wrong here and will otherwise be re-derived every few weeks.

## The framework, ranked by measured impact

1. **Batch tool calls — up to ~50%.** Historical rate is ~1.00 tool_use/turn. Every independent
   call sent in the same message is a request not billed at ~$0.09. This is the single biggest
   lever and it costs nothing.
2. **Hold median context near 60k — ~30%.** Take `/clear` at safe points *early*, not when the
   session feels long. Compact costs $2.53; `/clear` costs $0.
3. **Keep tool output small — compounding.** Any large tool result is re-billed on every
   subsequent turn of the session. Pipe builds/tests through `tail`/`grep`; read files with
   offset/limit. A single 5k-token dump on turn 10 of a 100-turn session costs ~90 re-reads.
4. **Subagent recon — attacks growth, not output.** The raw file dump lands in the subagent's
   context and only the conclusion returns. Use `model: "haiku"` for search/recon.
5. **Delegation for BULK implementation only.** Spawning an agent adds a fresh ~35k floor plus the
   spec plus the return. Below roughly a few hundred lines of mechanical work it costs more than
   it saves. Do not delegate small edits.

Combined realistic target: `0.5 (batching) × 0.72 (context) ≈ 0.36` → **~64% reduction.**

## What model routing does and does not do

Driver split, measured (d5044ede, 42 reqs, $2.95): cache_read 44.1% / **output 30.0%** /
cache_write 25.9%. **~70% of spend is context, not reasoning output.** A plan-expensive /
execute-cheap ladder only attacks the 30% output slice, and adds context to do it. Route models
for *quality* reasons (the CLAUDE.md ladder stands); do not expect routing alone to be the saving.

## The 3-layer framework (founder's structure, magnitudes measured)

**Layer 1 — lean context floor.** Correct mechanism, small magnitude (see finding 3: ~2.5%).
Do it because it is permanent and cheap, NOT ahead of layers 2–3.
Verified against https://code.claude.com/docs/en/memory:
- *"CLAUDE.md files in the directory hierarchy above the working directory are loaded in full at
  launch. **Files in subdirectories load on demand when Claude reads files in those directories.**"*
  → moving project detail into a subdirectory CLAUDE.md removes it from unrelated sessions.
- **`.claude/rules/` with `paths:` frontmatter is the sharper tool** — path-scoped rules load only
  when Claude reads matching files, without requiring the content to live under that directory.
- **`@path` imports do NOT help**: *"imported files load at launch"*. Do not split with imports.
- **`/doctor` automates the trim** — it *"cuts content Claude can derive from the codebase, such as
  directory layouts, dependency lists, and architecture overviews."* `prospector/CLAUDE.md`'s
  `## Architecture` module list is exactly that; it is derivable and should go.
- Docs target: **under 200 lines per CLAUDE.md**; *"CLAUDE.md files are loaded in full regardless
  of length, though shorter files produce better adherence."* So the real Layer-1 win is
  **adherence**, with tokens as a bonus — worth saying plainly rather than overselling the tokens.

**Layer 2 — planner/executor routing.** Sound, with one measured caveat: a worker process pays a
fresh ~35k floor plus the spec plus its return. Below roughly a few hundred lines of mechanical
work that exceeds what it saves. Route bulk implementation out; never route small edits out.
Harness already exists, project-local to `the-introduction-exchange`
(`scripts/deepseek-run.sh`, `consensus/agents/{gemini,deepseek}_adapter.sh`). `gemini` CLI is
installed; **`deepseek` CLI is absent.**

**Layer 3 — session boundaries.** Strongest-supported layer. `/clear` costs $0, compact $2.53, and
per-request rate falls ~35% at half the median context. One feature = one session.

## File exclusion — settled 2026-07-30

`.claudeignore` **does not exist** in Claude Code (confirmed against
https://code.claude.com/docs/en/settings). The mechanisms are:

```json
{
  "permissions": { "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)"] },
  "claudeMdExcludes": ["**/vendor/**/CLAUDE.md"]
}
```

`permissions.deny` is a **security** control (stop secrets being read), not a token control — it
does not touch the floor. `claudeMdExcludes` skips CLAUDE.md files, which per finding 3 is a ~2.5%
lever. Neither belongs in the top three.

## Open, not yet measured

- **HYPOTHESIS:** batching to ~2.5 tool calls/turn cuts request count ~50% with no quality loss.
  **CHECK:** run one task deliberately batched, compare `$/req` and `reqs` against this table.
- **Floor decomposition is still unknown.** Floor is a stable 34–37k across all 8 sessions with
  zero MCP servers in settings and one skill (`graphify`), so it is system prompt + tool schemas +
  CLAUDE.md. **CHECK (free):** run `/context` in a fresh session.
- `02742eb3` at $0.194/req is a 3× outlier on only 9 requests — unexplained. Likely Fable 5 (2×
  Opus rates) plus cache-write amortised over few requests. **CHECK:** `--detail 02742eb3`, read
  the `model` column.
