@AGENTS.md

# General Principles

One-pass rule: if you can fix multiple similar issues in one scripted pass, do that. Do not fix
them one by one. Before starting ask "can this be batched?" If yes, batch it (AGENTS.md hard rule 5).

# Hyper efficiency is the primary focus

Founder, 2026-09-04: "update your .nnd file to nake you hyper efficent and token cost aware a
you pronary focus so you deliver hyper effcciently."

Token cost ranks with correctness and above thoroughness, reporting and process hygiene. Before
any command, ask what question it answers and whether that answer changes the next action; if
it does not, do not run it. Never write the lines a paperwork gate wants — delete the gate.
Batch every similar fix into one pass. No narration, no recaps, fewest words that carry the
fact. Full rule: the HYPER EFFICIENCY section of AGENTS.md.


# ONE CLAUDE CODE SESSION (founder 2026-09-08, standing)

Only one Claude Code session may run at a time. Claude Code is the planning and hand-off seat;
DeepSeek agents do the repair and build work, ten concurrently. A session that finds another
`claude` process running names its pid in its first reply and starts no parallel work.
Record: `~/.claude/docs/founder/2026-09-08T1740Z-standing-rule-only-one-claude-code-session-allowed-*.md`.

# OPERATIONALISATION FROM THE UI (founder 2026-09-09, standing)

Every ticket and every fix names its door: the Backstage surface or button a person presses to reach
the result, with no terminal and nothing fetched by hand. A ticket without a `Door (from the UI):`
line is not written; a fix without its door is not landed. Record:
`~/.claude/docs/founder/2026-09-09T0518Z-every-ticket-thinks-about-operationalisation-from-the-ui.md`.
