---
captured: 2026-08-31T21:13:04+00:00
session: ef0354ef-fa6b-4b6b-a5e2-5d6f7889b3b8
cwd: /Users/chidionyema/dev/code/.wt-crew759-context
chars: 7732
source: founder prompt, verbatim (founder-doc-capture.py)
---

Assembly is a layer stack where each layer answers exactly one question and never restates the one above it. AGENTS.md: how work happens — universal. ENGINEER.md: what good building looks like — inherited by any department that builds, which is most of them; it's a craft file for an activity, not the property of an engineering department. The charter: what this department exists to produce, owns, and owes. Project CLAUDE.md: what this system is. The frame: what we're doing right now. Conflict rule same as before — the higher layer wins, and every charter says so in its first paragraph. A research session working inside idp therefore composes four layers automatically, and the charter is the only one that varies by department.

The wiring, verified against current docs: Claude Code reads CLAUDE.md, not AGENTS.md, but supports @path imports — so the universal pair loads via two import lines in user-scope memory at ~/.claude/CLAUDE.md, and department identity rides the launch: the CLI's system-prompt flags, including the append flags, work in both interactive and non-interactive modes, so one alias per department appends its charter without touching any repo. Department stays orthogonal to project — the same alias works whether the session is cwd'd into idp or prospector. 
Does Claude Code read AGENTS.md? No — it reads CLAUDE.md. The official @AGENTS.md import and symlink methods that actually work (the 'reads it as a fallback' claim is wrong), plus five operator-side patterns for keeping the two files in sync. For the #6235 cluster (5,200+ reactions). +3

~/.claude/CLAUDE.md          # two lines: @~/crew/AGENTS.md  @~/crew/ENGINEER.md
~/crew/depts/<dept>/CHARTER.md
alias crew-research='claude --append-system-prompt "$(cat ~/crew/depts/research/CHARTER.md)"'

Run /memory in a session once to confirm the stack actually loads — if the old 53-law file was sitting at ~/AGENTS.md without an import, part of your compliance history just explained itself. And two lines from the official memory docs vindicate the whole refactor: memory files are treated as context, not enforced configuration — to block an action regardless of what Claude decides, use a PreToolUse hook (your guards belong there), and files over 200 lines consume more context and may reduce adherence. Anthropic is telling you the 53 laws were self-defeating at the mechanical level, not just the stylistic one. 
Claude Code Docs
Claude Code Docs

Your inter-department obligations are the part to get right, because six departments is up to fifteen pairwise relationships, and if each obligation lives as prose in both charters you'll have rebuilt the 53 laws horizontally within a month. The fix is one you already know from your day job: departments are services, charters are their API docs. Every obligation is stated in full exactly once — in the producer's Provides section: artifact, shape (a schema or template path), cadence, and the guard that refuses a malformed handoff. The consumer's Consumes entry is a one-line pointer. Pointers can't drift; parallel prose always does. And your LAW 44 generalizes cleanly: an obligation with no checkable shape is a wish. Executive is the one department that isn't a peer in this graph — its outputs are decisions-with-reversal-conditions and ranked priorities, which enter everyone else's loop as interrupts and board items; its input is the status stream. It plugs into the interrupt slot of the algorithm, not into build work.

The "exceptional domain instinct" is the ENGINEER.md method applied per discipline — reference class plus decision procedures, zero adjectives. The register of it, one flavor per department:

Research: the literature search precedes the experiment — most of your ideas were tried in 2019, find the corpse first. Effect size before p-value; a result that won't replicate is a rumor.
Data: a schema is a contract and changing one is a breaking release, not an edit. Lineage or the number doesn't exist. A null is a decision, not an accident.
Science/ML: the embarrassingly simple baseline comes first; eval harness before training run; the default explanation for a great result is leakage until the ablation clears it.
Product: the spec states what won't be built; every feature ships with a kill criterion; user behavior outranks user opinion.
Executive: decisions are written with their reversal conditions; priorities are ranked, never listed; revisiting a decision without new information is a tax.

Here's the template to pour your existing charters into — same budget discipline, 400 words each:

Created a file, read a file

Full stack per session: two universal files, one charter, one project CLAUDE.md — under 1,500 words of instruction, all of it load-bearing, with everything enforceable living in hooks and schemas where it can actually refuse. Pour one of your existing charters into this and send it over; the first one will surface whatever the template gets wrong about your org before you convert the other five.

Charter template
Document·MD 

we are all using AGENTS.md, are you absolutely certain claude does ot reD FRON THEre, i think it does if CLAUDE.md isnt there

Fetched: https://code.claude.com/docs/en/memory

The docs answer directly — but given "absolutely certain" and a fast-moving CLI, let me check the shipped binary too, not just the page:

Ran 9 commands · 2 notes

No — and now it's verified from two angles rather than recalled, because you were right to push: I wasn't entitled to "certain" on a CLI that ships weekly.

Angle one, the docs, updated within the last day: Claude Code reads CLAUDE.md, not AGENTS.md. If your repository already uses AGENTS.md for other coding agents, create a CLAUDE.md that imports it so both tools read the same instructions — and a symlink also works if you don't need to add Claude-specific content. The docs' discovery section lists exactly two names walked up the directory tree: CLAUDE.md and CLAUDE.local.md.

Angle two, the shipped artifact: I pulled the actual v2.1.252 binary from npm and grepped it. AGENTS.md appears six times against CLAUDE.md's 184, and every occurrence sits inside two features: the /init codebase survey (reads it as source material when generating a CLAUDE.md) and the /import Codex adapter, which detects a Codex install by the file's presence and then copies AGENTS.md → CLAUDE.md and AGENTS.override.md → CLAUDE.local.md. Nothing in the session file-discovery path. And the copy operation is itself the proof: a migration that duplicates AGENTS.md into CLAUDE.md would be pointless if a fallback read existed.

Your observation was still real, though — here's the mechanism. Sessions frequently choose to open AGENTS.md mid-task: the model knows the ecosystem convention, sees the file in a listing, reads it, follows it. That's indistinguishable from native support right up until the session that doesn't bother. Discretionary reads produce exactly your compliance history — laws honored sometimes, ignored other times, the founder repeating himself five times. A file the model may elect to read is a wish; a file in the load path is a law. Your other tools reinforce the belief because for them it's true — Codex and friends do read AGENTS.md natively. And one clause of correction to my last message: /context is the command that shows what actually loaded; /memory lists and edits the locations.

The fix keeps your all-AGENTS.md convention intact: one ln -s AGENTS.md CLAUDE.md per repo root, ~/.claude/CLAUDE.md carrying the @~/crew/AGENTS.md import for the universal layer, then /context in a fresh session to confirm — deterministic load, no more relying on the model's curiosity. set this up  files in down load and we nneed claude.nd also
