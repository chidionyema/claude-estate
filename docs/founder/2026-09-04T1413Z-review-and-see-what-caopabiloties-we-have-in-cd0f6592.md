---
captured: 2026-09-04T14:13:21+00:00
session: 85f840c5-baf3-4598-9496-1b3eb9dd83e9
cwd: /Users/chidionyema/dev/code/idp
chars: 3392
source: founder prompt, verbatim (founder-doc-capture.py)
---

review and see what caopabiloties we have in place to support this as we have buuikt a lot of the ptiecss over past week 1. Seamless, One-Shot Ingestion (The UI is the New Road)
The command line is dead. We build an ingestion service (secret-provider) that powers the enterprise admin portal.

Enterprise Friction: A customer gets a new DeepSeek key.

The Seamless Solution: They open our Admin UI -> Settings -> Models. They paste the key once into a secure input field. They click "Activate."

Flexible Ingestion: For "bleed edge" customers, we provide a sync option (e.g., Bitwarden integration). They update the key in their enterprise vault, and our system programmatically fetches, proves, and syncs the new root without any manual pasting.

2. R52: Immediate Proving (Machine-Verified Trust)
Before the key is stored anywhere, the system must prove it is valid.

System Action: The secret-provider service makes an immediate test call directly to the vendor (e.g., [api.deepseek.com/v1/models](https://api.deepseek.com/v1/models)).

Validation: It must receive a 200 OK. If it gets a 401, the key is invalid. The UI provides immediate feedback: "DeepSeek key is invalid. Please check the vendor portal." The key is not stored. This is failing closed.

3. Secure storage: The "One Real Root"
Once the key is proved, it is written once to the ultimate truth.

System Action: The secret-provider writes the verified key into the single master entry in Vault (e.g., entry: litellm-upstream, field: DEEPSEEK_API_KEY). No repository secrets are used.

4. Distribution and Sync (Automated Refresh)
We leverage the built capability you mentioned to push the proven key across all products.

System Action: An ExternalSecret on the Kubernetes cluster is configured to pull the DEEPSEEK_API_KEY from the litellm-upstream Vault entry.

Mechanism: The ExternalSecret controller automatically refreshes and updates the corresponding Kubernetes secret every 10 minutes. Both the Router and the Prospector (and any future products) dynamically read from this Kubernetes secret. When Vault is updated, they all get the new key simultaneously in the next refresh cycle.

5. Proactive Monitoring (Ending the 401 Outage)
We don't wait for a 401 error to know a key is dead. The system actively monitors the health of the "R52 Road."

System Action: We implement a scheduled api-health-checker job. This is the proactive solution you need. It probes the router's /health endpoint and also makes a low-cost, vendor-specific validation call for every master key in Vault.

Flagging Expiry/Death: If a key starts to fail (401) or is flagged by the vendor as expiring, the system raises an alert before it impacts user traffic, allowing for rotation before an outage.

6. Automated Rotation (The Bleeding Edge)
This is the ultimate, seamless enterprise experience.

The Bleeding Edge Option: For vendors that support programmatic rotation (e.g., AWS, GCP), the api-health-checker detects an expiring key, generates a new one via the vendor's API, writes it to Vault, verifies it, and the system seamlessly updates.

The Assisted Option (Fallback): For vendors who do not support API-driven rotation (like DeepSeek, currently), the api-health-checker flags the key in the Admin UI. The customer is prompted to "Update DeepSeek key," which starts the automated Proving -> Storage -> Distribution cycle (Step 1).
