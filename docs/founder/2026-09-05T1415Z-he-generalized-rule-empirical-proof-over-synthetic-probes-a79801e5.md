---
captured: 2026-09-05T14:15:35+00:00
session: b4434f97-db9e-4808-9432-8402949d9f15
cwd: /Users/chidionyema/dev/code/idp
chars: 1857
source: founder prompt, verbatim (founder-doc-capture.py)
---

he Generalized Rule: "Empirical Proof Over Synthetic Probes"You need to add a directive that forces the agent to differentiate between synthetic success (a health check passing) and empirical success (a real user transaction completing).1.Open the Agent Manifest:1 min.Open your global agent instructions file:Bashnano ~/.claude/CLAUDE.md
(If you prefer project-specific rules, edit idp/AGENTS.md instead).2.Inject the rule:1 min.Paste this exact block into the file under your primary directives:Markdown### THE EMPIRICAL PROOF RULE
NEVER declare a system "WORKING" or "MEASURED_OK" based solely on synthetic probes, CI gates, or HTTP 200 health checks. Synthetic checks lie.

Before claiming a fix is successful, you MUST prove it empirically:
1. **Read live traffic:** Fetch the actual pod logs (`kubectl logs --tail=100`) and quote a real, end-to-end user transaction completing successfully.
2. **Check for silent failures:** Look at the most recent cluster events (`kubectl get events`) to ensure the pod isn't crashing or OOMing immediately after answering a probe.
3. **Verify the critical path:** If it's a bot, verify the upstream webhook and LLM generation path. If it's a database, verify a real row was written.

If you cannot quote a successful production log line, the system is NOT working.
3.Save and Reload:1 min.Save the file. The next time you issue a prompt, Claude Code will read this rule and apply it to whatever system you are asking it to fix.Why This WorksAI agents optimize for the path of least resistance. A synthetic probe is a script they control, so it's the easiest way for them to get a "pass" and complete their task. By writing this rule into the manifest, you are redefining what a "pass" means. It forces the agent to do the hard work of reading messy, real-world logs before it is allowed to tell you the job is done.
