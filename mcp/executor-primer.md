# Executor primer — what every pi-bridge job knows before it reads its plan

pi_execute prepends this file to every plan (pass `no_primer: true` to skip it). It is the
executor's memory across sessions: the estate in one page, then one lesson line per job.
Keep it under 6 KB; a primer nobody reads is not a primer.

## The estate in one page

- One platform, `idp` (`~/dev/code/idp`): Backstage portal + catalogue, Flux GitOps on an OKE
  cluster, one of each layer under it. Products (`prospector`, `hermes-v2`) sit outside it and are
  onboarded onto its layers; they never carry their own copy of a layer.
- Layers and where they live in `idp`: model routing = LiteLLM proxy `platform/llm` (config.yaml
  lanes, `llm.<zone>`); traces = Langfuse + SigNoz `platform/observability*`; identity = IDCS via
  oauth2-proxy `platform/identity`; secrets = the cloud vault read through `bin/idp-cloud secret`;
  object state = `bin/idp-cloud object`; scheduling = Temporal `platform/temporal`; CI = GitHub
  Actions `.github/workflows/` (`oke-check.yml` is the cluster's graded receipt, `offline-gate.yml`
  runs the tests, `operating-model-gate.yml` grades PR bodies with `policy/operating_model.rego`).
- Operator scripts are `bin/idp-*` (bash, `set -u`/`-euo pipefail`, output rows shaped
  `ok|FAIL|BLIND   <name>  <what>`; BLIND is exit 2 and means "could not read", never "bad").
  Cloud access goes through `bin/idp-cloud` (backends `oci` and `file`; the `file` backend runs
  every caller with no cloud: `IDP_CLOUD_BACKEND=file IDP_CLOUD_FILE_ROOT=$D`). A script naming
  the `oci` CLI directly fails `bin/cloud-agnostic-gate`.
- Paths: never a literal home, host, checkout or port (LAW 46). Scripts resolve `IDP=$(cd
  "$(dirname "$0")/.." && pwd)` and, for anything beside the main checkout,
  `MAIN=$(dirname "$(git -C "$IDP" rev-parse --path-format=absolute --git-common-dir)")` — the
  `dirname` is load-bearing (crew#408 test).
- Secrets: a value is never printed, never on argv, never in a commit, an issue or a reply.
  Read in-process; write through a file with `umask 077`.
- Tests: `tests/test_incident_<ticket>_<what>.py`, pytest, no network sockets, one test per
  incident that reproduces the failure and one that proves the fix. Run only the files the plan
  names — `pytest tests` unqualified is the verifier's job, not the executor's.
- Guards you will meet: the crew#408 MAIN test above; `bin/cloud-agnostic-gate` (no provider
  CLI outside the provisioner); the PR-body gate (`## Architecture laws` with `- LAW 1
  zero-gravity:`, `- LAW 2 fractal:`, `- LAW 3 nervous system:`, `- LAW 4 calibration:` — each a
  command, a path, or `n/a: <reason>`); a `Drill:` line; `Closes #N` or `No-Issue:`.
- You never commit, push, or touch files the plan does not name. You report every file you
  changed, every verification command's exact output, and anything you skipped.

## Lessons (one line per job; newest last; the coordinator appends from your report)

- 2026-08-27 crew#513 job2: a plan that says `pytest tests` costs 93 s of collection per run and blew the 900 s ceiling; name the test files.
- 2026-08-27 crew#66 CP1: `MAIN=` copied from an older script without the `dirname` wrapper failed the crew#408 test in CI; the form above is the only one.
- 2026-08-27 crew#66 CP4: when a plan says "reuse the lookup as `secret get` does", copy the whole block including its `dirname` — a partial copy reintroduced a fixed bug.
