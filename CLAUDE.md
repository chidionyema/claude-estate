@AGENTS.md


## THE EMPIRICAL PROOF RULE (founder 2026-09-05, verbatim; record: `~/.claude/docs/founder/2026-09-05T1415Z-he-generalized-rule-empirical-proof-over-synthetic-probes-a79801e5.md`)

NEVER declare a system "WORKING" or "MEASURED_OK" based solely on synthetic probes, CI gates, or HTTP 200 health checks. Synthetic checks lie.

Before claiming a fix is successful, you MUST prove it empirically:
1. **Read live traffic:** Fetch the actual pod logs (`kubectl logs --tail=100`) and quote a real, end-to-end user transaction completing successfully.
2. **Check for silent failures:** Look at the most recent cluster events (`kubectl get events`) to ensure the pod isn't crashing or OOMing immediately after answering a probe.
3. **Verify the critical path:** If it's a bot, verify the upstream webhook and LLM generation path. If it's a database, verify a real row was written.

If you cannot quote a successful production log line, the system is NOT working.
