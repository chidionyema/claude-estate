---
captured: 2026-09-04T20:31:19+00:00
session: 85f840c5-baf3-4598-9496-1b3eb9dd83e9
cwd: /Users/chidionyema/dev/code/idp
chars: 2070
source: founder prompt, verbatim (founder-doc-capture.py)
---

thast was the deepseek spec imate, measured not scheduled. Four checkpoints, four pull requests, two repositories.

┌────────────────────────────────┬───────────┬───────────────┬───────────┐
│                                │   repo    │ files changed │ new files │
├────────────────────────────────┼───────────┼───────────────┼───────────┤
│ CP1 worker + reply address     │ hermes-v2 │ 6             │ 4         │
├────────────────────────────────┼───────────┼───────────────┼───────────┤
│ CP2 boot drops the webhook     │ hermes-v2 │ 3             │ 0         │
├────────────────────────────────┼───────────┼───────────────┼───────────┤
│ CP3 one door                   │ idp       │ 4             │ 0         │
├────────────────────────────────┼───────────┼───────────────┼───────────┤
│ CP4 registration receipt moves │ idp       │ 2             │ 0         │
└────────────────────────────────┴───────────┴───────────────┴───────────┘

One database column, one envelope field. Everything else wires code that already exists to code that already exists.

The blocking gap I found while writing it, which changes CP1's shape: a message arriving through otto-gateway today cannot be answered at all. otto/ingress/plugins.py builds TelegramBinding(chat_id_allowlist={}), an empty allowlist normalises every update to principal=None, and the envelope that reaches the bus carries no chat id anywhere — the envelope is frozen/extra="forbid", so nothing can be smuggled through it. So CP1 adds reply_to to the envelope and moves the chat allowlist into the channel_binding row, before the worker is worth building. Had DeepSeek started at "bind durable_pull", it would have shipped a worker that reads messages and can say nothing back.

---

Also in the spec, because both would otherwise be re-derived wrong: otto.boot's process_update already duplicates ingress/gateway.py::_mint almost line for line, which is exactly where the seam goes (process_envelope); and otto.boot's "answer" is a note tool, model="boot-deterministic-stub" — there is no model call to lose.

C
