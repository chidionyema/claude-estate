---
captured: 2026-09-05T21:28:27+00:00
session: 2eb24bf7-c245-49bc-9398-b81dd0aaeb99
cwd: /Users/chidionyema/dev/code/idp
chars: 2401
source: founder prompt, verbatim (founder-doc-capture.py)
---

Assuming you want to lock in both the physical layout and the logical authorization, let's map out the Kubernetes namespace topology first to see where the walls go, and then drop the Policy-as-Code rules on the doors.1. The Kubernetes Topology (Physical Isolation)To ensure zero cross-contamination, we use a rigid namespace architecture.namespace: estate-control-plane: This is your Founder fortress. It runs the Envoy API Gateway, the OPA/Cedar policy engine, and the global Postgres estate-state. No tenant code is ever allowed to execute here.namespace: tenant-0-workspace: This is Customer 0's execution cell. All worker agents run here using gVisor to isolate the kernel. Customer 1 gets tenant-1-workspace, and so on.The Network Choke Point: A Cilium NetworkPolicy is applied to every tenant namespace with a strict Default Deny All. The only allowed egress route is directly to the estate-control-plane Envoy gateway. Agents cannot talk to the internet, or even to each other, without passing through the gateway.2. The Policy-as-Code (Logical Vault Doors)When a tenant agent hits the gateway, Envoy strips all client-provided identity headers and asks the policy engine for permission based only on the agent's cryptographic SPIFFE certificate.The Tenant Rule (Strict Confinement):Code snippetpermit (
    principal,
    action,
    resource
)
when {
    // The SPIFFE cert's tenant ID must perfectly match the target resource
    principal.tenant_id == resource.tenant_id 
};
The Founder Override (God Mode):Code snippetpermit (
    principal == Role::"Founder",
    action,
    resource
);
3. Tying It to the Memory DoorHere is how this architecture permanently solves the estate_memory.py ingestion problem without rewriting the Python app logic:Customer 0's agent (in tenant-0-workspace) calls the MCP recall tool.The request hits the Envoy Gateway. Envoy reads the agent's SPIFFE ID and identifies it as tenant-0.The Policy Engine runs the rule above and approves the read.Envoy forwards the request to the backend, securely injecting X-Verified-Tenant: tenant-0 into the headers.estate_memory.py requires zero authorization logic. It simply reads the header and executes SELECT * FROM memories WHERE tenant_id = 'tenant-0'.This is how you build a zero-regret platform. The python code just focuses on the business logic, while the infrastructure mathematically enforces the boundaries.
