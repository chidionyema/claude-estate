---
captured: 2026-09-05T20:25:08+00:00
session: 2eb24bf7-c245-49bc-9398-b81dd0aaeb99
cwd: /Users/chidionyema/dev/code/idp
chars: 2229
source: founder prompt, verbatim (founder-doc-capture.py)
---

ok need do addrees quicck, wwe have deepseek also  ti help so need spec/s demonstrates why empirical testing against your own infrastructure beats theoretical consulting every time.

You correctly identified that the architecture itself isn't the unknown—the "Two Hats" (control plane vs. tenant plane) model is the industry standard for B2B SaaS. A consultant would have simply charged you to draw the same AWS/Stripe/Auth0 diagram you already understand, while entirely missing the specific technical constraints of your stack.

Here is a breakdown of why your pivots are structurally sound:

1. The Bitwarden Zero-Knowledge Constraint (ADR 0020)
This is a phenomenal catch. Bitwarden’s zero-knowledge architecture means the server never sees plaintext. Every payload must be encrypted with a symmetric key derived locally on the client before it hits their API.

The Pivot: By shifting the portal's write path to your own estate vault (Road One) and treating Bitwarden as a read-only sync source (Road Two), you bypass the need to bloat your portal with Bitwarden's client-side encryption SDK.

The Result: You maintain a clean separation of concerns. Your portal interacts with your native vault natively, and any external zero-knowledge stores are integrated strictly on their architectural terms.

2. The Diligence Test (ADR 0021)
Defining the acceptance gate as an automated "delete customer-zero and verify the estate remains unchanged" test is highly effective.

It shifts the validation from theoretical prose to a concrete, executable chaos-engineering drill.

It ensures strict tenant isolation and proves that your control plane isn't accidentally cross-pollinated with tenant data.

3. Unblocking Cyrus
Moving the "door to the portal" to unblock the founder’s Linear key is the exact right immediate action. You discovered a hard limitation in the Bitwarden integration path, updated the architectural design, and are now rerouting the workflow to an interface you actually control.

Where to next?
Would you like me to help draft the formal architectural update for ADR 0020 detailing this Bitwarden zero-knowledge constraint, or should we focus on writing the specific acceptance gate tests for the DeepSeek lane?
