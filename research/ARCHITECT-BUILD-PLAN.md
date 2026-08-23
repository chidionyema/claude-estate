# ARCHITECT build plan — new Hermes agent to replace the existing one
Written 2026-08-21. Source spec: ~/.claude/research/THE-ARCHITECT-spec.md (sha 7aefd52f)

## 1. Measured state (all receipts from commands run 2026-08-21 23:53–23:57)

| fact | command | value |
|---|---|---|
| hermes home | `ls -la ~/.hermes` | symlink -> ~/Documents/code/hermes |
| config repo | `git -C ~/.hermes remote` | chidionyema/hermes-config, branch main, 68 dirty paths |
| agent repo | `git -C ~/.hermes/hermes-agent remote -v` | fork of NousResearch/hermes-agent |
| divergence | `git rev-list --count HEAD..origin/main` | **12,624 behind** |
| carried work | `git rev-list --count origin/main..HEAD` | **127 ahead**, 185 files, +43,791 lines |
| running version | `hermes --version` | v0.16.0 (2026.6.5), upstream base eca85e81 |
| upstream latest | `git tag --sort=-creatordate \| head -1` | **v2026.8.19** |
| agent processes | `ps aux \| grep hermes` | **none running** |
| launchagents | `launchctl list \| grep hermes` | only lease-guard + runaway-reaper; gateway/rsi/watchdog/progress are `.bak` (disabled) |
| carried hot files | `git log --name-only origin/main..HEAD` | gateway/operator_shell/estate.py 34, gateway/run.py 21, natural_ops.py 20, mission.py 18 |
| ledger | `prompt-ledger.py --list open` | 412 rows, **410 open** |

Two conclusions that drive everything:

1. **The old agent is not running.** Nothing is on fire; this is a build, not a rescue.
2. **The fork cannot be merged forward.** 12,624 commits behind, and upstream has
   restructured (new top-level `.coderabbit.yaml`, `.python-version`, `.nvmrc`,
   `CONTRIBUTING.es.md`; ours has `acp_registry`, `MANIFEST.in`, `cli.py` that upstream
   moved). A merge is a multi-week conflict grind on a codebase we do not own.
   The 127 carried commits are almost entirely OUR layer (`gateway/operator_shell/*`),
   not core-agent patches — that is what makes a clean rebase-onto-new-base feasible.

## 2. Decision

**Fresh build on a pinned upstream tag. Nothing is ported. The old estate stays frozen
and intact until the new one replaces it.** Not a merge, not a patch, not a port.

Rejected: (a) merge-forward — 12,624 commits, unbounded; (b) throw the 127 commits away
— they include the operator shell, cron budget ratchet, telegram fixes we paid for;
(c) upgrade in place — destroys the only working artifact we have if it goes wrong.

## 3. Phases (each ends with a command that proves it, per LAW 17)

### P0 — Requirement register (before any build)
Every requirement in THE ARCHITECT spec becomes a row in
`~/.hermes-v2/REQUIREMENTS.jsonl`: `{id, section, statement, acceptance_cmd, status}`.
Founder prompts stay in prompt-ledger; spec clauses live here; the two link by id.
Proof: `jq -s length REQUIREMENTS.jsonl` > 0 and every row has a non-empty
`acceptance_cmd`.

### P1 — Branch + worktree (the founder's literal ask)
```
git -C ~/.hermes fetch origin main
git -C ~/.hermes branch architect-v2 origin/main
git -C ~/.hermes worktree add ~/Documents/code/hermes-v2 architect-v2
```
New Hermes HOME is `~/Documents/code/hermes-v2`, never the live `~/.hermes`. One agent per home.
Proof: `git -C ~/.hermes worktree list` shows it; old home untouched
(`git -C ~/.hermes rev-parse --abbrev-ref HEAD` still `main`).

### P2 — Clean upstream agent at a pinned tag
Fresh clone of NousResearch/hermes-agent at `v2026.8.19` into `~/Documents/code/hermes-v2/hermes-agent`
(not a fetch into the old fork). Install into its own venv. `hermes doctor` clean before
anything else happens.
Proof: `hermes --version` reports 2026.8.19 with 0 carried commits, and `hermes doctor`
exits 0.

### P3 — The old fork is reference only (founder decision, 2026-08-22)
"This has nothing to do with the old one. It will eventually replace it."
The 127 carried commits are NOT ported. The new build starts empty and grows only
what the spec calls for. The old fork stays on disk, unread unless a specific need
names a specific commit — at which point that one commit is re-authored, not
cherry-picked.
Proof: `git -C ~/Documents/code/hermes-v2 ls-tree -r --name-only 2118344` is empty (the slate commit
has zero files), and the old home is still on `main`.

### P4 — Config + memory, spec §2/§3
`config.yaml` pinned: `agent.max_turns: 90`, `memory_enabled: true`,
`user_profile_enabled: true`, model lane per profile. Terse `MEMORY.md` + `USER.md`
including the restate-and-confirm line.
Proof: `hermes config get agent.max_turns` returns 90 on the new home.

### P5 — Profiles WATCH / WORK, spec §5/§6
Two separate homes, read-only creds on WATCH verified by attempting a write and
confirming it fails.
Proof: the failed-write output, quoted.

### P6 — Gates before hands, spec §7/§10
Evidence gate + static gates in CI; the five leash items. WORK gets write access only
after all five exist.
Proof: a deliberately evidence-free PR fails CI.

### P7 — Cutover
Old estate stays frozen and reversible: the `main` branch, the old home, the `.bak`
plists all stay where they are. Cutover is flipping the launchagents to the new home,
one at a time, with a documented one-command rollback.
Proof: gateway responds from the new home; `launchctl list` shows the new labels.

## 4. Explicitly NOT in this plan
Deleting anything from the old estate. Merging the fork. Touching prod. Auto-merge.
A third always-on profile. VPS migration (spec §1 says VPS; this build is local-first
and the VPS move is a later, separate item).

## 5. Open question for the founder (one)
Spec §1 puts WATCH and WORK on a VPS (£5–15/mo) so the laptop becomes optional.
ANSWERED 2026-08-22: laptop first, move to the VPS once it is proven.
