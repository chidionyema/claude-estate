---
captured: 2026-09-10T21:38:25+00:00
session: a941270d-843c-40b9-9481-9f198a8612f1
cwd: /Users/chidionyema/dev/code/idp
chars: 2645
source: founder prompt, verbatim (founder-doc-capture.py)
---

That is a brilliant, brutal catch by your builder bot.

You built a beautiful, fully tested memory retrieval engine (`otto/ingress/thread.py`), stored every single message in the database, and then accidentally hardcoded the router to ignore all of it. Otto literally has Alzheimer’s by design because of one hardcoded array.

The 112-second latency and the amnesia are the exact same bug. Because Otto has no short-term context window, it treats a one-word reply like "lol" as a brand new, context-less query. It is likely spinning up the heavy `hindsight` temporal memory, hitting the vector database, and doing a full RAG pipeline just to figure out what "lol" means in a vacuum.

Here is the one-shot elite fix to wire it up and drop the latency instantly.

### 1. Wire the Thread (The One-Shot Fix)

You need to open `otto/router/providers.py` and replace the hardcoded array with a call to the unwired thread builder.

Change this:

```python
messages: list[dict] = [{"role": "user", "content": payload}]

```

To this:

```python
from otto.ingress.thread import build_thread_messages

# Pull the last N turns from otto_turns, format them, and append the new payload
messages: list[dict] = build_thread_messages(session_id, limit=10)
messages.append({"role": "user", "content": payload})

```

*Boom.* Otto instantly has short-term memory, and the LLM can resolve conversational references (like "summarize this URL") natively in milliseconds without triggering massive background database scans.

### 2. The Leaked Protocol Errors

If the user sees "The reply protocol requires exactly one raw JSON object...", it means Otto's LLM failed to output valid JSON, and your router just dumped the raw stack trace or LLM apology straight to the frontend.

* **The Elite Fix:** Add a strict JSON validation middleware loop in `providers.py`. If the LLM outputs broken JSON, catch the `KeyError` or `JSONDecodeError` locally, append a system prompt saying `"Invalid JSON format. Output strictly valid JSON."`, and retry *under the hood*. The user should never see a prompt-engineering error.

### 3. The ⚠ Unverified Stamps

This means your asynchronous feed-guard or fact-checker is either failing silently or the background worker queue (like Celery or RQ) that processes message verification is offline or stalled.

**Tell the builder job to proceed with its exact proposed order:**

1. Wire `ingress/thread.py` into the router (Fixes memory + latency).
2. Catch and retry JSON protocol errors natively (Fixes UX bleed).
3. Debug the background verification workers (Fixes the ⚠ stamps).

Send the `Go` command to your builder to execute this.
