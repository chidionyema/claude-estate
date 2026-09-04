---
captured: 2026-09-04T08:42:47+00:00
session: 85f840c5-baf3-4598-9496-1b3eb9dd83e9
cwd: /Users/chidionyema/dev/code/idp
chars: 1592
source: founder prompt, verbatim (founder-doc-capture.py)
---

ca you explain what is going on 2. Clear the Distractions
Run this command in the Claude Code prompt to wipe its memory of the old task and start fresh:

Bash
/clear
3. Diagnose the Kimi / LiteLLM Issue
You confirmed Kimi (moonshot/kimi-k3) is in the LiteLLM console, but Claude told you it wasn't in the picker because it wasn't in config.yaml or the vault.

When a model is manually added to the LiteLLM UI (Database) but is not declared in your infrastructure as code (platform/llm/config.yaml), the GitOps sync will either overwrite it or ignore it, and your local CLI tools won't see it because they are reading the Git state, not the live LiteLLM database.

To fix this properly so Kimi shows up in your agent and survives cluster reloads, paste this exact prompt into Claude Code:

Plaintext
Do not read any files or think. Just execute these two commands:

1. Create a placeholder secret for Kimi in the vault directory (e.g. `estate-secrets/secrets/dev/`) so the lane can authenticate.
2. Add the 4-line row for `moonshot/kimi-k3` to `platform/llm/config.yaml` as the lane `kimi`.

Output only the file diffs or shell commands used to do this.
Why you couldn't see anything else in LiteLLM:
If you logged into the LiteLLM console and couldn't see your agents or other models, you are likely logged into the wrong LiteLLM instance/workspace, or you are logged in as a user without admin permissions to view the declarative models synced by Flux. The models listed in config.yaml are injected directly into the running container; they often won't show up in the manual "UI added" list.
