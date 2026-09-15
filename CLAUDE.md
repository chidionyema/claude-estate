@AGENTS.md

# Standing rules

One-pass rule: batch every similar fix into one scripted pass — never fix issues one by one.

Every ticket and fix names its door: the exact Backstage surface or button a person presses, no
terminal, nothing fetched by hand. No `Door (from the UI):` line, no ticket. Record:
`~/.claude/docs/founder/2026-09-09T0518Z-every-ticket-thinks-about-operationalisation-from-the-ui.md`.

Definition of Done v3: no agent declares its own work "done" or "built" — only an independent,
non-builder check may. Done means five checks (sellable, installable fast, verified not asserted,
procurement-passable, owned), enforced zealously on all three `rules.yaml` planes, not just at
reply time. This is an idp estate law, not a Claude Code preference — full text and enforcement
status live in the idp repo: `docs/decisions/0029-definition-of-done-v3-is-five-checks-none-self-graded.md`.
