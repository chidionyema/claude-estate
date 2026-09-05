---
captured: 2026-09-05T03:34:39+00:00
session: cd5f2d7c-ebbe-44bb-890e-833699eb6631
cwd: /Users/chidionyema/dev/code/idp
chars: 2088
source: founder prompt, verbatim (founder-doc-capture.py)
---

also get this done as well
❯ no i would need to be able to aks it fron telegrn and backstage also

  Read 1 file, ran 23 shell commands

WORKING: One tool on the estate MCP server, then both doors get it.

What I measured just now:

- The estate already runs its own MCP server (estate-mcp, tools like get_estate_state, get_workload_logs) behind agentgateway at /estate/mcp. ADR 0006 says a question about the estate is one MCP tool call, and never a second server.
- Otto's agent is already an MCP client — it reads mcp_servers from its own config and supports HTTP servers with an auth header.
- Backstage already runs the proxy plugin (it uses it for the Ops page today), and it already carries our own in-house plugins.

So the road is one implementation and three callers, not three builds:

            ask_holmes  (mcp/plugins/estate_holmes.py)
                 |
                 +-- POST robusta-holmes.robusta/api/chat
                 |
   +-------------+-------------+---------------+
   |             |             |
Telegram      Backstage      Alertmanager
(Otto, as     (a page in     (the sensor
 an MCP        the portal,    that just
 tool)         via proxy)     merged)

I have recorded that a capability which only runs on its own is half delivered — you must be able to ask it from Telegram and Backstage too — so this does not need saying again.

---

Ask on Telegram becomes: "Otto, ask Holmes why the llm namespace is unhealthy" — Otto calls the tool, Holmes looks at the cluster, the answer comes back in the same chat. No new command to remember and no second bot.

In Backstage it becomes a page in the portal with a question box and the answer rendered, so it is not only yours — anyone with a login can ask.

The one thing I have not yet pi answers on Telegram in-cluster: the gateway pod runs python -m otto.ingress, which receives the message and puts it on the bus; the agent that repliesd I need to confirm it is theone holding the MCP client before I wire the config. That is the next thing I check, and it changes only where one confign.
, ok raise it
