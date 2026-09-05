---
captured: 2026-09-05T21:24:54+00:00
session: 2eb24bf7-c245-49bc-9398-b81dd0aaeb99
cwd: /Users/chidionyema/dev/code/idp
chars: 2941
source: founder prompt, verbatim (founder-doc-capture.py)
---

Got it. Zooming out entirely. You're talking about the fundamental topology of the platform—how the architecture itself separates the "Founder running the estate" from the "Enterprise Customer doing their work," across the entire stack.

If you are building the out-of-the-box platform for the AI age, the whole system has to be built on a Control Plane vs. Tenant Plane split from day one. You aren't just building features; you are building the boundaries.

Here is how that dual-identity shapes the overall architecture, far beyond just the memory door:

The Platform-in-a-Box Architecture
Every system you build has to answer to two masters: the overarching infrastructure (the Estate) and the isolated environments running on it (the Tenants).

Layer    Founder / Estate Owner (Control Plane)    Enterprise / Customer 0 (Tenant Plane)
Identity & Routing    "God Mode" access via the API Gateway. Can route requests to any tenant namespace to debug, observe, or deploy updates.    Strictly scoped token. The Gateway traps their requests and binds them entirely to their specific tenant ID.
Agent Compute    Orchestrator agents that monitor platform health, scale resources, and deploy new tenant instances (e.g., spinning up Customer 1).    Worker agents executing business logic (data analysis, coding, customer support) locked inside a specific namespace.
State & Storage    The estate-state database. Holds the global registry, cross-tenant telemetry, platform billing, and global configuration/constraints.    Isolated tenant databases or schemas. Customer 0's private documents, memory, and workarounds live here, physically or logically walled off.
Observability    The overarching Memory Dashboard (#1646) and Grafana/Superset views showing cross-cluster health, total token burn, and aggregate recall-counts.    A scoped dashboard showing only their specific agent performance, their token usage, and their isolated memory effectiveness.
MCP Integrations    Platform-level tools (e.g., managing GitOps pipelines, restarting pods, adjusting global rate limits).    Business-level tools (e.g., querying their specific CRM, reading their local GitHub repos, writing to their isolated DB).
The "Customer 0" Discipline
The genius of acting as both the Founder and Customer 0 is that it forces you to feel the pain of a bad boundary immediately.

If you, as Customer 0, have to use a Founder-level tool to fix a routine business problem, the platform isn't enterprise-ready yet. If your Customer 0 agents accidentally read an estate-state configuration file they shouldn't have access to, you've caught a tenant-isolation leak before Customer 1 ever signs up.

Every time you build a new feature—whether it's the MCP, a new dashboard, or a GitOps pipeline—the architectural reflex has to be: "Is this an Estate capability that manages the platform, or a Tenant capability that uses it?"

Want to look at the Gateway/Routing layer next?
