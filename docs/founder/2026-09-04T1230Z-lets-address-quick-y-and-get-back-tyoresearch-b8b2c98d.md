---
captured: 2026-09-04T12:30:03+00:00
session: 5f6f4e72-2af4-4aec-915f-678401bb6a68
cwd: /Users/chidionyema/dev/code/idp
chars: 1632
source: founder prompt, verbatim (founder-doc-capture.py)
---

lets address quick;y and get  back tyoresearch engine Outstanding Security Gaps (Not Best Practice)
Token Automounting: 130 of 180 pods unnecessarily auto-mount a kube API token. This requires an admission default setting automountServiceAccountToken: false with a specific opt-in policy.

Workload Identity: Cloud calls currently use the node's Instance Principal rather than fine-grained pod-identity federation. Migration to OKE Workload Identity is required to scope identity per service account.

ETCD Encryption: It is currently unknown whether the OKE control plane encrypts secrets in plaintext etcd with an OCI KMS key. This requires verification.

Database Consolidation Status (PR idp#1450)
PR idp#1450 contains the complete consolidation plan:

Credential Reuse: Every new cluster role retains the existing username, database name, and password read from the service's own vault entry. This eliminates new credential generation and prevents drift for seven of the ten services.

Data Migration: Seven copy Jobs handle the data transfer. These are guarded by marker tables (rather than emptiness checks) to prevent jobs from skipping real data if an application rebuilds its schema during the migration window.

Validation: Kyverno admission checks have passed (Pass: 525, Fail: 0).

Rollout Strategy: The old database servers and their volumes remain operational; their decommissioning is scheduled as a subsequent change.

Not Done: Dagster and Langfuse continue to run Postgres embedded within their Helm charts. These will be addressed in a follow-up action to move from nine servers down to three, and finally to one
