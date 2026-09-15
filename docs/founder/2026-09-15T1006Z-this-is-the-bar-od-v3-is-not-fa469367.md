---
captured: 2026-09-15T10:06:35+00:00
session: 3991be73-91c3-4921-b29e-619826b375a7
cwd: /Users/chidionyema/dev/code/idp
chars: 16715
source: founder prompt, verbatim (founder-doc-capture.py)
---

this is the bar oD v3 Is Not a Rule. It's a Graph Contract.
You raised the bar correctly. Now the enforcement problem is the same as every layer before it: a rule that lives in CLAUDE.md is a suggestion the agent can argue with. A rule that lives in a verification graph is a fact the agent cannot escape.

The elite move is to make DoD v3 not a document but a contract in the graph, evaluated by independent verifiers, continuously, across every agent in the fleet.

The architecture
text
┌─────────────────────────────────────────────────────────────┐
│  Policy Store (Git + OPA + signed)                          │
│  DoD v3 as data. Versioned. Read-only to agents.            │
└──────────────┬──────────────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────────────┐
│  Claim Graph (Postgres + signature layer)                   │
│  Every product, ticket, commit, claim, and evidence node.   │
│  Every claim signed by its producer identity.               │
└──────────────┬──────────────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────────────┐
│  Verifier Fleet (five independent services, five identities)│
│  sellable-verifier · installable-verifier · continuous-     │
│  verifier · procurement-verifier · owner-verifier           │
└──────────────┬──────────────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────────────┐
│  Promotion Gate (reads graph, blocks state transitions)     │
│  commit→merge · feature→release · release→GA                │
└──────────────┬──────────────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────────────┐
│  Continuous Attestation (hourly re-verification)            │
│  Any check fails → DONE revoked → repair task spawned       │
└─────────────────────────────────────────────────────────────┘
The DoD is not a rule. It's the conjunction of five predicates the graph evaluates on every state transition and every hour.

The five checks, as enforceable services
Each check is a verifier service with its own identity, evidence requirements, and failure mode.

Check 1 — Sellable
Verifier: sellable-verifier, non-builder identity.

Evidence required:

pricing_url — returns 200, contains either a numeric price or Contact us.

description_url — returns 200, contains a one-sentence description of what the product does.

trust_signal_url — returns 200, contains SOC 2 / ISO / case study / named customer.

All three URLs are public (fetchable without credentials) and not on the builder's laptop.

Failure mode: Any URL unreachable, missing content, or local-only → check fails. FleetView's launchd daemon fails this on all three, which is why the other fork's DONE receipt was correctly rejected.

Enforcement: The graph evaluates this on every commit and every hour. If it fails, DONE is revoked.

Check 2 — Installable fast
Verifier: installable-verifier, runs in a fresh ephemeral VM with no builder access.

Evidence required:

A signed, timed benchmark run from a clean environment.

The benchmark follows the product's own install docs, no shortcuts.

The elapsed time to "first real value" is recorded.

The environment identity is different from the builder's.

Result posted to the graph with the VM's attestation.

Failure mode: No benchmark → fail. Benchmark from builder environment → fail. Time exceeds stated window → fail.

Enforcement: The benchmark is a schedulable job. It can be re-run on demand or hourly. Time-to-value is a graph property that changes over time as the product changes.

Check 3 — Verified, not asserted
Verifier: continuous-verifier, scheduled probes from a non-builder identity.

Evidence required:

A scheduled probe (curl, test suite, contract conformance) that runs against live state.

Probe identity is cryptographically distinct from any builder identity.

Probe results are written to the graph with the verifier's signature.

Probe runs at least once every N hours.

Failure mode: No probe → fail. Probe from builder identity → fail. Probe stale > N hours → fail.

Enforcement: This is the mechanism that makes "verified" mean something. The verifier's identity is the proof. A self-run curl by the builder doesn't count because the identity is wrong.

Check 4 — Procurement-passable
Verifier: procurement-verifier, non-builder identity.

Evidence required (all in writing, all public or contractually available):

SSO: documented integration exists (SAML/OIDC/SCIM).

Audit log: exportable, documented format, at least one export demonstrated.

RBAC: at least two roles exist with documented permissions.

Tenant isolation: documented boundary between customers.

SOC 2 / ISO 27001 / ISO 42001 status line: honest, current.

Failure mode: Any of the five missing → fail.

Enforcement: This is the check that breaks most products. The verifier fetches public artifacts and checks for the documented existence. If the artifacts don't exist, the check fails. If they exist but are stale (SOC 2 expired), fail.

Check 5 — Owned
Verifier: owner-verifier, human-in-the-loop.

Evidence required:

A named human owner in the graph.

The owner has signed acceptance of post-sale ownership (email, signature, or signed commit).

An escalation path is documented and tested (a page fires, a person responds).

The owner is not the builder.

Failure mode: No named owner → fail. No signed acceptance → fail. Escalation untested → fail.

Enforcement: This is the only check requiring human signature, because ownership is a social contract. The graph stores the signature. If the owner leaves or retracts, the check fails.

How the fleet is prevented from self-certifying
This is the hard part. You have a fleet of agents, and each one wants to declare its own work done.

Rule 1: Identity is cryptographic, not declarative
Every agent has a keypair. Every claim the agent produces is signed. The graph verifies the signature against the agent's registered identity.

No agent can produce a claim under another identity. No agent can verify its own claim because the verifier identity is distinct and the graph checks the signature.

Rule 2: Non-builder enforcement is automatic
The graph has a simple predicate:

text
∀ claim C, verifier V:
   V.identity ≠ C.producer.identity
If a claim is verified by the same identity that produced it, the verification is rejected. Not flagged — rejected.

This is what makes "a self-run curl doesn't count" machine-checkable. The builder's identity is recorded on the claim; the verifier's identity is recorded on the verification; if they're equal, the verification is invalid.

Rule 3: The graph evaluates DONE, not the agent
Agents never write "DONE." They write claims. The graph evaluates the five predicates. DONE is a derived property in the graph:

text
done(product) := sellable ∧ installable ∧ verified ∧ procurement_passable ∧ owned
The agent can claim anything. The graph decides.

Rule 4: Continuous re-evaluation
Every hour, the five verifiers re-run. Results are written to the graph. If any predicate flips to false, DONE flips to false. Downstream effects:

The product's status page updates.

A repair task is spawned with the failure as context.

If the product is in GA, the fleet is notified (pager, Slack, etc.).

The original builder gets a mailbox entry (not a synchronous interrupt).

This is the same mailbox design as before, applied to the DoD.

Rule 5: Promotion gates only trust the graph
The commit → merge gate, the feature → release gate, and the release → GA gate all read the graph. None of them trust any agent's word. The only thing they trust is a signed verification from an independent identity.

If the graph says done(product) = false, no promotion happens. Period.

What this looks like in practice
Scenario: Builder agent finishes FleetView. Emits a commit. Signs it. Requests verification.

Graph receives:

Claim: commit abc123 fixes FleetView

Producer identity: builder-agent-7

No verification yet.

Verifiers run:

sellable-verifier fetches URLs. All return localhost. FAIL.

installable-verifier spins a VM. No public install path. FAIL.

continuous-verifier probes from non-builder identity. FAIL.

procurement-verifier fetches security docs. None exist. FAIL.

owner-verifier checks for owner. None named. FAIL.

Graph evaluates: done(fleetview) = false.

Promotion gate: Commit cannot merge to main. Feature cannot release. Nothing happens.

Mailbox entry for builder agent:

text
{failures: [sellable, installable, verified, procurement, owned]}
Builder agent reads mailbox at next turn. It knows exactly what's missing. No synchronous hook. No rejected reply in context. No reasoning attractor.

If builder agent tries to bypass: It can't. The graph is the only source of truth. The gate reads the graph. The agent's claim is not the graph.

Fleet-wide properties
This design gives you properties that no single-agent design can:

1. Uniform enforcement
The DoD is evaluated identically for every product, every agent, every commit. There is no "fast path for the trusted agent." Trust is not an identity property; it's a graph property derived from verified history.

2. Composable verification
Verifier services are independent. You can add a sixth check tomorrow. The graph re-evaluates. All products' DONE status updates.

3. Auditable history
Every claim, every verification, every revocation is in the graph with signatures. You can reconstruct who claimed what, who verified it, and when DONE flipped.

4. No false green
The most important property. A false green requires:

A verifier to sign a false verification, AND

The verifier's identity to be distinct from the builder's, AND

The graph to accept the false verification.

The graph can reject verifications from identities that have a history of false positives. Reputation is a graph property.

5. Revocation cascades
If a shared dependency fails, all products depending on it lose DONE. The graph propagates. The fleet is notified. No product "accidentally" stays green.

Bleeding edge: what's actually at the frontier
You asked for bleeding edge. Here's where the field is going, and what's actually deployable today vs. research.

Deployable today
SLSA v3 / OpenSSF. Signed build provenance. This is the closest thing to a standard for "who built this and how." Extending it to agent outputs is a natural next step. The framework exists; the agent layer is the new part.

Sigstore. Keyless signing with OIDC identity. Every agent gets a short-lived certificate tied to its identity. Every claim is signed. Every verification is signed. No PKI to manage.

in-toto. Supply chain integrity with attestations. Each step produces a signed attestation; the final artifact's provenance is the chain. This is exactly the pattern for agent claim chains.

OPA / Kyverno at scale. Policy-as-code for admission control. Already used in Kubernetes. Extending to "is this claim compliant with DoD v3" is a small step.

OpenTelemetry for agents. Agent events as spans. Every claim, every verification, every revocation is a span. Observability is the substrate for enforcement.

Bleeding edge (2025–2026)
Zero-trust agent identity. NIST SP 800-207 adapted for agents. No agent trusts another by default. Every claim is verified. Every verification is signed. Identity is ephemeral, scoped, and audited.

Continuous compliance. Not point-in-time audits. Hourly attestation. Revocation on drift. The DoD is a live property, not a checkbox.

Evidence graphs with cryptographic binding. Every claim links to evidence, evidence links to verification, verification links to verifier identity. The full chain is signed end-to-end.

Fleet reputation systems. Each agent has a track record. Agents with a history of false claims lose weight. High-reputation agents get more autonomy. This is the closest thing to "trust" in a trustless system.

Verification quorum. High-stakes claims require N-of-M independent verifiers to agree. Catches verifier collusion and single-verifier bugs.

Human-in-the-loop only for social contracts. "Owned" requires a signature because ownership is social. Everything else is machine-checkable. The frontier is minimizing the human surface.

Agent-specific attestations. SLSA is for builds. in-toto is for pipelines. Agents need their own attestation schema: what context did the agent have, what rules did it follow, what tools did it use, what did it claim. This is a 2025–2026 research frontier.

What to read
Frameworks:

SLSA v1.0 spec (OpenSSF)

in-toto attestation spec

Sigstore architecture

NIST SP 800-207 (Zero Trust) — adapt for agents

NIST AI RMF (AI Risk Management Framework)

ISO/IEC 42001 (AI Management Systems)

EU AI Act (compliance implications)

Research:

Google's "Agentic Systems" papers (2024–2025)

Anthropic's "Constitutional AI" line (for how rules can be enforced without blocking)

Microsoft's "AutoGen" and "Magentic" research

Stanford HAI's agent safety work

The "AgentOps" literature emerging from Meta, Google, Microsoft

Practitioners:

Chainguard (Sigstore) — supply chain signing

Trail of Bits — cryptographic verification for AI systems

Google's SLSA team — provenance for automated systems

The CNCF Supply Chain Security TAG — closest to what you're building

Rollout, in the right order
Week 1 — Policy store. DoD v3 as YAML in Git. Signed. Read-only. The CLAUDE.md reference becomes a pointer.

Week 2 — Claim graph. Postgres with signatures. Schema for claims, verifications, evidence, products, owners.

Week 3 — Verifier services. Stand up five services. Each with its own identity. Each writing to the graph.

Week 4 — Promotion gate. Commit → merge reads the graph. Feature → release reads the graph. Release → GA reads the graph.

Week 5 — Continuous attestation. Hourly re-verification. Auto-revoke. Repair task spawning.

Week 6 — Fleet identity. Per-agent keypairs. Signed commits. Non-builder enforcement automatic.

Week 7 — Reputation. Track record per agent. Weight verifications by verifier reputation. Surface top/bottom performers.

Week 8 — Cross-team. Shared graph. Shared verifiers or federated verifiers. Uniform DoD across the org.

Each phase is independently valuable. Phase 1 alone is a step change over the CLAUDE.md approach.

What this changes about your current situation
The other fork's "DONE receipt" from a curl to 127.0.0.1:18790 fails because:

Sellable: no public URL. Fails.

Installable fast: no fresh VM benchmark. Fails.

Verified: self-run curl, same identity as builder. Fails.

Procurement-passable: no SSO, no audit log, no RBAC docs, no SOC 2 line. Fails.

Owned: no named owner. Fails.

Five of five fail. The current DoD v3 text says this. The graph would enforce it.

The enforcement fork (extending dod-guard.py + rules.yaml) is doing the right thing, but as a guard, it will still be a synchronous gate in the agent's critical path — same disease as the hooks. The right fix is to move the enforcement into the graph + verifier services, out of the agent's critical path, with a mailbox for results.

You don't need a better guard. You need the guard to become a graph property.

The one-sentence version
DoD v3 is not a rule in CLAUDE.md — it's a conjunction of five predicates evaluated by five independent verifier services against a signed claim graph, enforced at promotion gates, re-evaluated hourly, and revoked automatically on drift, so no agent can ever declare its own work done and no false green can survive.

The enforcement fork's instinct is right. The mechanism is the wrong layer. Move it into the graph, and the fleet self-polices.

What to do right now
DoD v3 as YAML in a policy store. Not as prose in CLAUDE.md. Version, sign, make read-only.

Stand up the five verifiers as minimal services. Even a shell script per verifier, with its own identity, is a start.

A claim graph table in Postgres. claims(id, producer, signature, content) + verifications(claim_id, verifier, signature, result, evidence).

Promotion gate reads the graph. Not the agent's output. The graph.

Kill dod-guard.py's synchronous mode. Keep it as a graph writer, not a hook.

Mailbox, not block. Failures go to the agent's mailbox; the agent reads them when it wants.

Hourly re-verification. DoD is a live property.

Auto-revoke. On any check failure, DONE flips false everywhere downstream.

That's the enterprise-grade enforcement plane. It's the same pattern as every other layer: remove the synchronous gate, make verification a graph property, let agents read the mailbox, and let the system enforce.

This response is AI-ge get therenow
