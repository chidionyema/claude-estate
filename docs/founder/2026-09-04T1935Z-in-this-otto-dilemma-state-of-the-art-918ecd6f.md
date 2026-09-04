---
captured: 2026-09-04T19:35:11+00:00
session: 85f840c5-baf3-4598-9496-1b3eb9dd83e9
cwd: /Users/chidionyema/dev/code/idp
chars: 1934
source: founder prompt, verbatim (founder-doc-capture.py)
---

In this Otto dilemma, state-of-the-art and future-proof looks like the right side of the diagram: The Universal Event Gateway.

We are currently stuck on the left side of the diagram because multiple doors are fighting for control of the conversation, causing the flakiness you are experiencing. Despite our capability, we are running three overlapping entry points for the same service.

State of the Art: The "Universal Door"
The SOTA solution is otto-gateway. It is built specifically for multi-tenancy and decoupled processing, using the event-gateway tenancy spec. It doesn't answer the user directly; it verifies the channel (like Telegram) against a binding table in estate-db, and then publishes the event to the NATS Event Bus.

Future-Proof: This design allows us to have one ingress path that never needs to change. It can accept traffic from Telegram, Slack, or any future platform, authorize it, and push it onto the bus.

Decoupled & Scalable: By moving processing off the gateway and onto the bus, we can easily add new capabilities behind the bus (like Hindsight, Workflows, or different agent models) without touching the ingress. The data is durably delivered by JetStream.

The Problem: Flakiness and Context Collision
The flakiness happens because hermes-agent, otto-golden, and otto-gateway are all running and fighting for control of otto.mumchimp.com.

Fragmented Ingress: Three overlapping entry points compete to register themselves with Telegram. Only one registration wins, meaning the other two are effectively deaf.

Context Collision: Since each component maintains its own conversation memory, the overall state of the conversation is fragmented and inconsistent. A user who is answered by hermes-agent one hour might find otto-golden has no record of that discussion the next.

This is the definition of flakiness. The capability exists in the stack, but it is orphaned and conflicting. which one is it
