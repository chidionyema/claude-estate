---
captured: 2026-09-03T10:54:40+00:00
session: 54539261-20a7-4289-a144-e9265f1b0c43
cwd: /Users/chidionyema/dev/code/idp/.wt-docs-keyintake
chars: 2778
source: founder prompt, verbatim (founder-doc-capture.py)
---

The Pathology of the Crash
The Bash Rookie Mistake: The agent ran pytest | tail. In standard Bash, a pipeline returns the exit code of the last command. pytest failed, but tail succeeded (exit code 0). The agent thought the tests passed.

The Panic: The agent realized its mistake ("the pipeline ate pytest's exit code") and tried to fix it by writing a nasty, chained command that redirected the entire output of 214 test files into a raw text log file in the /tmp directory.

The Death Spiral (20m 40s): The agent tried to read that raw text log. The output of 214 test files is massive. It flooded the agent's context window, choked the LLM's attention mechanism, and sent it into an infinite "Ideating..." loop trying to parse thousands of lines of raw text.

It didn't freeze because of the code. It froze because it tried to read a phone book.

The Elite Strategic Fix (Eradicating the Error Forever)
You do not fix this by telling the agent to be careful. You fix this by enforcing strict laws on how the agent is allowed to interact with the shell and test outputs.

Paste this into your AGENTS.md or system instructions to permanently ban the "Silent Green" trap and context-flooding loop:

Markdown
# ELITE SHELL & TESTING LAWS

## 1. THE PIPEFAIL MANDATE
You are strictly forbidden from running standard bash pipes (`|`) that swallow exit codes. Every shell command you write that includes a pipe MUST be prefixed with `set -eo pipefail;`. 
* BAD: `pytest | tail`
* GOOD: `set -eo pipefail; pytest | tail`

## 2. THE ANTI-FLOOD RULE (NO RAW LOG PARSING)
When executing test suites or bulk scripts, you are FORBIDDEN from reading massive raw `stdout` logs or dumping them to text files to read later. This destroys your context window.
If you need to run `pytest` on multiple files, you MUST use `--tb=no` and `--short` or output the summary strictly to JSON. You only care about the final pass/fail count and the names of the failing files.

## 3. NO COMPLEX BASH CHAINS
Do not write multi-line, inline bash scripts with custom exit code capturing (`rc=$?; echo $rc`). Keep commands atomic. Let the native environment handle the exit codes.
What to do right now:
Kill the frozen agent (Ctrl+C). It is braindead. It will never recover from that 20-minute context flood.

Run the pure command yourself. To see the actual pass/fail count of those 214 files without swallowing the exit code or flooding your terminal, run this exact command:

Bash
set -eo pipefail; pytest -q --tb=no $(cat /tmp/trimmed.txt | tr '\n' ' ') | awk '/===/ {print}'
This enforces pipefail, strips out the thousands of lines of noise, and prints only the final summary line (e.g., === 200 passed, 14 failed ===), returning the correct failure code.

That is how you execute without the theatre.
