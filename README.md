# claude-estate

This repository is one machine's working brain: the laws every agent follows, the
scheduled jobs that keep the estate running, the guards that refuse bad changes,
and the record of what has been decided. `scripts/` is a submodule,
[claude-guards](https://github.com/chidionyema/claude-guards), and it holds the
code.

Both repositories are private and stay private. This one carries conversation
transcripts and project memory. A guard checks the visibility of both every hour
and says so on the board when one is wrong.

## If the laptop is gone, start here

```
git clone --recurse-submodules https://github.com/chidionyema/claude-estate ~/.claude
~/.claude/scripts/tracked.py --restore
~/.claude/scripts/jobs/render.py --write
```

That gets the files back. It does not get the credentials back, because none of
them are in here. `scripts/rebuild/PREREQUISITES.md` lists the fourteen things a
new machine needs, what each one holds, and the command that gets it. Five of
them are browser sign-ins that no agent may do for you.

The whole path is drilled rather than described. `scripts/drills/run.py --list`
says which recovery paths have been proved and when. The rebuild drill clones
both repositories into a throwaway home, restores from the manifest, renders the
jobs for that home, and asserts six things. It runs itself on Mondays at 04:30
and writes PASS or NOT-RUN to the board.

## What is in here

| directory | what it holds |
|---|---|
| `AGENTS.md` | the laws. `CLAUDE.md` includes it; the other agent tools symlink to it |
| `scripts/` | the submodule: guards, jobs, drills, docs |
| `scripts/jobs/` | every scheduled job, declared once, rendered per platform |
| `scripts/drills/` | the recovery paths, and which of them have been proved |
| `scripts/docs/onboarding/` | one page per feature: what it costs, and how to stop it |
| `scripts/rebuild/` | the drill, and what a new machine needs that git cannot hold |
| `projects/` | per-project memory and transcripts |
| `ESTATE_BOARD.jsonl` | the shared record. Every session is handed the last 12 hours |

## What is deliberately not in here

Credentials, keys and tokens. `scripts/hooks/pre-commit` reads the staged blob
of every commit and refuses one whose content looks like a secret. It reports
`file:line` only, so a refusal never prints the thing it stopped.
`tracked.py --pull` scans a file before it copies it, and excludes credential
stores such as `~/.ssh` and `~/.aws` by name as well.

## Windows

A Windows rebuild is not proved. `scripts/jobs/render_windows.py` turns all 29
jobs into Task Scheduler XML and reports, per job, what Windows does not keep.
Run it with `--check` for the current number. Until a rendered job has actually
run on Windows, that renderer is a file-format exercise, and the
`windows-rebuild` entry in the drill register says so.
