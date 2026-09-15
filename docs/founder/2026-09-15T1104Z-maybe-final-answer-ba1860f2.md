---
captured: 2026-09-15T11:04:19+00:00
session: 2c1fc7d2-ae84-470f-a8a6-24a80c8ea1a6
cwd: /Users/chidionyema/dev/code/idp/.claude/worktrees/fleetview-estate-map
chars: 4209
source: founder prompt, verbatim (founder-doc-capture.py)
---

Maybe final answer:

text
The high-tech enterprise solution is: make the vendor an adapter, not an architecture.

Concrete:
- `sovereign/engine/runners.py`: delete `_claude`. Define `Runner` protocol. `RunnerRegistry`. Product calls `registry.run(provider, task)`.
- `estate.db`: canonical `sessions`/`session_events`. All runners write there. No reading `~/.claude/...`. If no layer exists, that's the build item.
- Frontend: launchd plist with KeepAlive, same as backend. Chat session is not a supervisor.
- Executor: UDS sidecar (pod-local) or separate Deployment + NetworkPolicy + mTLS. No exposed port.
- CI: ban vendor names outside `adapters/`. Delete `.claude` from product tree.

That's it. The genius is refusing to let one vendor's dev tool become your product's control plane.
Then maybe "If you want, I can write the exact Runner interface and launchd plist." But we are assistant, can offer.

Need ensure no mention "I can't". We can provide.

Maybe include launchd snippet:

xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist ...>
<plist version="1.0">
<dict>
  <key>Label</key><string>com.idp.fleetview.frontend</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/env</string>
    <string>yarn</string>
    <string>start</string>
  </array>
  <key>WorkingDirectory</key><string>/Users/chidionyema/dev/code/idp/.../frontend</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>/tmp/fleetview-frontend.log</string>
  <key>StandardErrorPath</key><string>/tmp/fleetview-frontend.err</string>
</dict>
</plist>
Then command. But maybe too much.

Need answer "wwhat thigh tch genius enterpise soltion o t his" maybe they want "what's the high tech genius enterprise solution to this?" We can start: "There isn't a clever one. It's this:" Then list.

Let's craft final with moderate detail, no fluff. Ensure no "village" insult. Use direct tone.

We can also mention "MCP is not the product boundary; your estate's session/event store is." But maybe not.

Let's final.

There isn’t a clever one. The “high-tech enterprise solution” is boring architecture:

Make the vendor an adapter, not the control plane.

Kill _claude in sovereign/engine/runners.py.
Replace it with a Runner protocol + registry:

python
class Runner(Protocol):
    name: str
    async def run(self, task: Task, ctx: RunContext) -> AsyncIterator[Event]: ...
    async def cancel(self, run_id: str) -> None: ...
Product code calls registry.get(config.provider).run(...).
openai, anthropic, ollama, vllm, local_process, mock are just adapters. No product path imports a vendor binary.

Sessions are your own model-agnostic event store.
estate.db gets canonical tables:

sql
sessions(id, provider, model, created_at, metadata_json)
session_events(id, session_id, seq, type, payload_json, ts)
All runners emit into that. No reading ~/.claude/state/prompt-ledger/*.jsonl.
If the estate has no real session layer yet, that is the actual build item. Not a publisher shim.

Frontend and backend are supervised services.
A chat session is not a process manager. Put the frontend on launchd exactly like the backend:

xml
<key>Label</key><string>com.idp.fleetview.frontend</string>
<key>ProgramArguments</key>
<array><string>/usr/bin/env</string><string>yarn</string><string>start</string></array>
<key>WorkingDirectory</key><string>/path/to/frontend</string>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><true/>
Then launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.idp.fleetview.frontend.plist.

Dangerous executor: UDS sidecar or separate Deployment.
Pod-local sidecar over emptyDir UNIX socket is fine. Enterprise version: separate ServiceAccount, read-only rootfs, dropped caps, no network, only UDS. If it crosses a trust boundary, separate Deployment + NetworkPolicy + mTLS. No exposed laptop port.

CI gate.
rg -i 'claude|anthropic|\.claude' --glob '!adapters/**' --glob '!devtools/**' fails the build. Delete .claude from product paths. Keep dev tooling isolated.

That’s the genius enterprise move: hexagonal boundary + event-sourced sessions + process supervision + policy enforcement.
Everything else is a shim that will keep biting you.
