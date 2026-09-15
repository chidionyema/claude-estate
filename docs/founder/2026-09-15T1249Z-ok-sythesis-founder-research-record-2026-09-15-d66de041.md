---
captured: 2026-09-15T12:49:17+00:00
session: 1f9d2f2b-f2b7-4fbf-bbaf-538df8abd162
cwd: /Users/chidionyema/dev/code/idp
chars: 20974
source: founder prompt, verbatim (founder-doc-capture.py)
---

ok sythesis Founder research record — 2026-09-15

Asymmetric Compute Leverage
Every item in the buffet, extracted and checked — against a primary source where one exists, against the actual repository where the buffet claimed a mechanism, and tagged honestly where neither check has happened yet.

Legend: CONFIRMED checked this session against a primary source or the repo   UNVERIFIED founder-supplied only   GAP genuinely not built   CORRECTED an earlier claim was wrong, fixed here
1 — JIT / point-of-use compute
CONFIRMED Apple licensing forces a 24-hour minimum lease on Apple-Silicon-as-a-service (Scaleway, AWS both document it) — "point of use" cannot mean hourly for a Mac.

UNVERIFIED The buffet's flat-monthly Mac Mini figures (Hetzner ~£54/mo, Scaleway ~£68/mo) are a separate, monthly-committed lease that sidesteps the 24h floor — not the same offer as point-of-use rental, and the only one of the two that's actually cheap in practice.

2 — Small/efficient models
Model    Params    Claim    Status
GPT-OSS-120B    116.83B / 5.13B MoE    Near o4-mini parity; needs an 80GB GPU self-hosted — zero-GPU only via free API routing    CONFIRMED
Poolside Laguna S 2.1    118B / 8B MoE    Agentic coding, 256K ctx    CONFIRMED
Nanbeige4.1-3B    3B dense    Beats 30–32B class on most benchmarks    CONFIRMED — arXiv 2602.13367
Gemma 4 26B A4B    25.2B / 3.8B MoE    Near-31B quality, 4B-class cost    CONFIRMED
MiniMax M2.7    230B / 10B MoE    Near-Opus SWE-Pro — non-commercial license    CONFIRMED
Falcon-H1R 7B    7B hybrid    AIME-2025 83.1%, beats 15B/32B peers    CONFIRMED
TwiL-LM3    3B    96.4 rule-induction figure belongs to an unreleased TwiL-LM3* variant, not the shipping checkpoint    CORRECTED
TRM / VibeThinker / DeepSeek-Distill family / Qwen3.8-27B / DeepSeek V3.2/R1/V4 / Gemini 3/2.5 / o3-mini / Qwen3-32B    —    Founder buffet/email only    UNVERIFIED
3 — MoE economics
Total params = knowledge ceiling; active params = the real bill. The buffet's own pick of a dense 32B model for the rented Mac is the weaker choice once this is applied — Qwen3-Coder-Next (80B/3B active) fits the same 32GB box for less compute and more ceiling. Not yet benchmarked on real hardware.

4 — Buffet mechanisms vs. the actual repo
Mechanism    Status    Evidence
Pillar 1 — cheap/free routing + local gatekeeper    BUILT    platform/llm/config.base.yaml
Z3 / CEGIS symbolic verification    BUILT — more rigorous    sovereign/verifier.py, 3-stage pipeline
Semantic/intent routing    GAP    routing is price/health only, never intent
Pillar 2 — CPU sandbox (execute_python)    GAP    grepped, no match
Pillar 3 — Grind Tool CronJob    GAP    only "grind" hit is unrelated prose, broker.py:661
Pillar 4 — Darwin Machine    plausible, unconfirmed    sovereign/shadow/distill.py / branching.py
Differentiable execution graphs / do-calculus    real technique, not repo-checked    Pearl's do-calculus, established
Refinement types / proof-carrying actions    real technique, not repo-checked    repo's actual proof is runtime Z3+execution, not compile-time
CrewAI / LangGraph    not the repo's primitive    Temporal child workflows (branching.py) already fill this role
LLMRouter via ComfyUI    real tool, unused here    ulab-uiuc/LLMRouter, Feb 2026 ComfyUI front end
5 — Hosting cost matrix
Option    Spec    Cost
Oracle Ampere A1 free tier    2–4 OCPU / 12–24GB    $0
Vast.ai RTX 3090    24GB    $73–146/mo continuous, ~$9/mo @ 2hr/day
Vast.ai RTX 4090    24GB    $180–330/mo continuous
Vast.ai A100/H100    80GB    $600–1,400/mo continuous
Vast.ai storage    —    $0.10–0.20/GB/mo, billed even stopped
Hetzner Mac Mini M2 Pro    32GB unified    ~£54/mo UNVERIFIED
Scaleway Mac Mini M2 Pro    32GB unified    ~£68/mo UNVERIFIED
MacStadium fixed-rate    32GB unified    ~$80–100/mo UNVERIFIED
CORRECTED An earlier pass of this record said Vast.ai pricing "needs the founder's own email" — wrong, the email was already in the buffet; this was a failure to use material already provided, not a missing receipt.

6 — Choreography (design only, not built)
Matrix-as-data (§5) · branching.py Temporal workflows as choreographer, not CrewAI/LangGraph · one real hard-metering gap: request_ceiling.proxy_handler_instance currently warns on the 86,525,924-token/hour 2026-09-13 incident, it does not sever the router · visibility via a real Backstage catalog entity, not a bespoke dashboard.

7 — Open items
Mac-Mini hourly-vs-flat reconciliation for a real point-of-use plan
TRM / VibeThinker / DeepSeek-Distill family / remaining model-zoo entries — no primary source checked yet
No semantic-intent router exists — real gap, no ticket filed
No CPU-sandbox tool, no Grind Tool — real gaps, no tickets filed
Pillar 4's match to distill.py/branching.py — unconfirmed, not disproven
MoE-vs-dense-32B on a real 32GB rented Mac — not yet benchmarked
request_ceiling.proxy_handler_instance hard-metering fix — named, not built
Backstage catalog entity for the hosting-tier choreography — named, not builtStatus: PROPOSED — frozen on founder sign-off. After freeze, changes require
a version bump + diff against this file. Purpose: every instruction you repeated
this session is stated once here, made testable, and made complete by
construction (traceability coverage is a mechanical check, not a vibe).

Conventions: SHALL = mandatory, verifiable. Every REQ has: source (S#),
acceptance test, verification method. Nothing enters build without a REQ.

## S# — Sources

S1  Buffet verbatim (4 Pillars + CEGIS/Z3 + summary), pasted 2026-09-15
S2  Founder emails 2026-09-14 (TwIL-LM3 deploy, hardware table, Vast.ai pricing)
S3  Research record: docs/evidence/2026-09-15-asymmetric-compute-leverage-research.md
S4  Repository ground truth: platform/llm/*.yaml, sovereign/verifier.py,
sovereign/shadow/branching.py, AGENTS.md budget/capability blocks
S5  Session demand ledger (below)
S6  arXiv receipts: 2502.06703 (TTS volume beats size), 2505.04842,
2502.20379 (BoN-MAV multi-verifier), ROC-n-reroll (verifier ceiling)

## Demand ledger (your repeated instructions -> enforced rule)

D-LEDGER-1 "Don't drop a single ball / every iota" -> Traceability matrix
(§6): every S1 item maps to a REQ or an explicit OPEN/WONT. Coverage check
is mechanical: grep the matrix, count zero unmapped.
D-LEDGER-2 "Super synthesis = defined bar" -> Acceptance definition: a
deliverable is complete only if zero OPEN items remain unaddressed and every
claim carries a receipt grade (strong/weak/founder-supplied-unverified).
D-LEDGER-3 "No stupid questions" -> Decision register (§7): every open
question ships with a recorded DEFAULT so work proceeds; questions never
block dispatch.
D-LEDGER-4 "JIT / point of use, not 24h standing" -> REQ JIT-01/02.
D-LEDGER-5 "Infinite configurability, no corset" -> REQ ORCH-02 (axes as
config cells, no workflow rewrite).
D-LEDGER-6 "Asymmetric leverage without downside" -> §5 free-lunch invariants
only; everything else is costed with its tradeoff named.
D-LEDGER-7 "Metered hard and visible" -> REQ COST-01/02 + OBS-01. "Hard" is
false until the breaker severs; that is P0.
D-LEDGER-8 "No laptop dependency, not even optional" -> REQ GOV-01.
D-LEDGER-9 "Commercial-grade, day-0, no inches" -> every REQ has an
acceptance test; untestable requirements are rejected at intake.
D-LEDGER-10 "URL served from estate, not vendor" -> OBS-02: deliverables
render on the local founder board (127.0.0.1:8787 /look), never an external
host unless tagged # vendor-surface-intended with reason.

## 1. Cost & spend governance

COST-01 The system SHALL NOT exceed $150/month. The router budget enforcement
SHALL SEVER traffic at breach, not warn. (S4 86.5M-token/hour incident proved
warn-only is false security.)
ACCEPT: fault-injection: synthetic 2M tok/hr load -> breaker trips, traffic
degrades to declared local lane, audit event recorded. METHOD: integration test.
COST-02 Any action that provisions paid compute (tier activation, GPU rental,
cluster resize) SHALL require a hardware-rooted signature (Secure Enclave /
Touch ID) per spec §4.1, in addition to budget check. No signature path ->
the action is architecturally impossible, not just policy-blocked.
ACCEPT: attempting activation without signature yields no provisioning call;
with signature + quorum, provisioning proceeds. METHOD: integration test.
COST-03 The cost ladder (Rung 0-3) SHALL be versioned config data. Rung 2
(flat-rate rental) SHALL activate only when measured trace volume crosses the
breakeven band computed from real router token prices (~58M-233M tok/mo at
current rates). No pre-commitment. (S3 §5)
ACCEPT: with simulated traces below band -> no activation proposal; above ->
proposal with computed numbers. METHOD: trace-query test.
COST-04 Every hosting tier SHALL carry a receipt grade (vendor-doc / survey /
founder-supplied-unverified). Founder-supplied figures SHALL NOT enter the
cost model until cross-checked. (S3)
ACCEPT: cost table rows include grade column; ungraded row fails schema.
METHOD: config schema validation.

## 2. Compute provisioning (JIT)

JIT-01 All compute tiers SHALL be point-of-use: activatable on demand,
deactivatable when idle. Apple Silicon tiers SHALL honor the documented 24h
minimum per activation (Apple licensing term, not vendor policy); GPU tiers
SHALL be per-second with no floor. The two SHALL NOT be treated as
interchangeable on this axis. (S3 §1, verified)
ACCEPT: config declares activation_floor per tier; orchestrator refuses to
model Apple tiers below 24h granularity. METHOD: unit test + config review.
JIT-02 Cold start to first-token SHALL meet a declared latency budget per tier,
or the request SHALL degrade to the next declared lane with the degradation
marked in-trace. Silent stall is a defect.
ACCEPT: kill instance mid-flow -> trace shows DEGRADED marker, response
continues from fallback lane. METHOD: fault-injection test.

## 3. Routing & escalation

ROUTE-01 All model calls SHALL traverse the standardized model-agnostic router
with mandatory fallback chains. Direct provider calls are rogue per crew
policy. (S4, crew policy)
ACCEPT: network policy denies egress to provider APIs except router;
bypass attempt alerts. METHOD: infra test.
ROUTE-02 The working-method axes SHALL be independent config dimensions:
resource tier (Rung 0-3) x candidate volume N x selection method
(gate | weighted-vote | multi-verifier) x escalation pattern
(route | cascade | hybrid). Changing any cell SHALL be a config edit only.
(S5 D-LEDGER-5, S3 §6, S6)
ACCEPT: matrix run: same 50-task set executed against >= 4 config cells;
results queryable by config_id in Langfuse; no code change between cells.
METHOD: experiment harness test.
ROUTE-03 For domains with a real verifier (code/logic/math), escalation SHALL
be verifier-driven: cheapest lane first unconditionally, escalate ONLY on
verifier FAIL. No difficulty classifier gates execution. This makes misroute
risk zero by construction (nothing trusted unverified). (S3 creative leap #1)
ACCEPT: adversarial misroute suite: wrong-cheap-answer attempts escalate;
right-cheap-answer passes without touching expensive lanes. METHOD: eval suite.
ROUTE-04 For NL-judgment domains with no verifier, escalation SHALL be signaled
by disagreement between two cheap independent models. No classifier is built
for these domains. (S3 creative leap #1)
ACCEPT: seeded disagreement corpus -> escalate rate tracks disagreement;
agreement cases never escalate. METHOD: eval suite.
ROUTE-05 Semantic intent routing (buffet "Traffic Cop": LiteLLM semantic
router / RouteLLM / vLLM router) is a NAMED GAP (S3 §4). If adopted, it SHALL
exist as a filter_depth axis on ROUTE-02, default OFF, because
misclassification ships wrong answers on the cheap path (real cost, not free).
ACCEPT: gap recorded; axis present in config schema even when disabled.
METHOD: config schema review.
ROUTE-06 The fallback chain SHALL terminate at the always-on local tiny model
answering openly marked DEGRADED — never at a paid pool that can be
systemically down in the same event. Never silently fail. (S3 creative leap #4,
founder_board UNKNOWN-rule pattern)
ACCEPT: kill all external lanes -> local model answers with DEGRADED marker;
no request drops. METHOD: fault-injection test.

## 4. Verification & selection

VER-01 The existing three-stage gauntlet (structural compile / Z3 symbolic /
execution tests) SHALL grade all code/logic candidates. Attestation SHALL
remain bound to SHA-256 of verified bytes. (S4 sovereign/verifier.py)
ACCEPT: mutation of verified bytes invalidates attestation. METHOD: unit test.
VER-02 Selection method SHALL be a strategy slot per ROUTE-02. Where a real
verifier exists, weighted voting by verifier score or multi-verifier SHALL be
used; plain best-of-N with a noisy selector is disallowed there. (S6)
ACCEPT: config sets selection=weighted-vote for Z3-scored domains; harness
honors it; N-scaling on unverifiable domains is capped. METHOD: eval suite.
VER-03 The claim-graph mechanism (DoD v3) SHALL be pointed at NL output
candidates as the NL verifier (reuse, not new build). (S3 creative leap #3)
ACCEPT: claim-graph run over candidate outputs produces verdicts recorded in
trace. METHOD: integration test.
VER-04 The harness SHALL detect tasks with no real verifier and SHALL cap
candidate volume for them — volume scales noise, not accuracy, past the
verifier's ROC ceiling. (S6 ROC-n-reroll)
ACCEPT: unverifiable task class -> N capped at declared constant regardless
of config. METHOD: property test.

## 5. Offload, grind, darwin, orchestration

OFF-01 Deterministic operations (math/string/date/aggregation) SHALL execute on
CPU/REPL, never in a model call. (S1 Pillar 2, S3 Lane 0)
ACCEPT: static scan of traces shows zero model tokens attributable to
deterministic ops. METHOD: trace audit.
OFF-02 The CPU-sandbox execute_python tool (ephemeral container, result not raw
data returns) is a NAMED GAP. If built, raw data SHALL NOT enter the prompt
when the tool can compute the result. (S1 Pillar 2, S3 §4)
ACCEPT: gap recorded; when built, prompt payloads exclude offloadable data.
METHOD: integration test.
GRIND-01 The overnight grind worker (Pillar 3) SHALL be mathematically unable
to terminate before (a) its deterministic test passes, or (b) the 4h
wall-clock limit. Context compaction SHALL run every 20 turns. Status: NAMED
GAP pending confirmation against repo queue primitives. (S1, S3 §4)
ACCEPT: fault-injection: kill-signal at hour 2 -> worker resumes/rejects
termination until condition met. METHOD: fault-injection test.
DARWIN-01 The weekly meta-optimizer (generate variants -> CPU eval suite ->
auto-deploy winner via CI) SHALL be confirmed-or-built against
sovereign/shadow/distill.py + branching.py. Until confirmed as a match it is
a NAMED GAP, not existing capability. (S1 Pillar 4, S3 §4 — verified-not-asserted)
ACCEPT: file-level evidence that the weekly generate/eval/auto-deploy loop
exists, or the gap is scheduled. METHOD: code review record.
ORCH-01 Orchestration SHALL reuse Temporal child workflows (branching.py).
No second orchestration framework (CrewAI/LangGraph) without explicit REQ.
(S3 §6)
ACCEPT: dependency manifest contains no CrewAI/LangGraph. METHOD: config review.
ORCH-02 On flat-rate tiers, candidate volume SHALL be governed by a time
budget (generate as many as fit the time box), not a dollar-percentage.
branch.budget_pct is the wrong shape on those tiers. (S3)
ACCEPT: on flat-rate tier, budget_pct ignored, time-box honored; on metered
tier, dollar budget honored. METHOD: property test.
ORCH-03 Every routed call SHALL carry a config_id tag; experiment results
SHALL be answerable as a Langfuse query over existing traces. No new
dashboard. (S3 §6)
ACCEPT: run 2 configs, query returns per-config cost/pass/latency table.
METHOD: trace-query test.

## 5b. Free-lunch invariants (only true no-downside items)

FL-01 Speculative decoding SHALL use a draft model with identical output
distribution guarantee (rejection sampling) — faster, never different.
(S3)
FL-02 Exact-match cache SHALL retain its safeguards: TTL + per-call opt-out +
reuse marked in trace. Removing any safeguard voids the "free" claim.
(S4 litellm.yaml — already real)
FL-03 Trace tagging (config_id) is pure information gain on already-paid
infrastructure; zero new cost. (S3)
FL-04 Weighted verifier voting on Z3-scored branches: same generation cost,
strictly better selection, no added risk. (S6)
Any other "free lunch" claim SHALL be rejected at intake with its tradeoff
named. (S5 D-LEDGER-6)

## 6. Observability & delivery

OBS-01 Visibility SHALL live in the Backstage catalog via the existing
generator (bin/catalog-gen). The hosting matrix SHALL be a generated catalog
entity. No bespoke dashboard. (S3 §6, S4)
ACCEPT: catalog entity exists, generated, renders tier/cost/receipt-grade.
METHOD: render test.
OBS-02 Founder-facing deliverables SHALL render on the local board
(127.0.0.1:8787 /look) or a permanent collector page. External hosting only
with # vendor-surface-intended + reason. (S5 D-LEDGER-10, estate LAW 34/39)
ACCEPT: board serves the record; no external publish in trace. METHOD: check.
GOV-01 Zero laptop dependency in the production path: no config, lane, or
fallback may resolve to founder hardware. Dev-local convenience files not in
the routing path are exempt by classification record. (S5 D-LEDGER-8)
ACCEPT: dependency scan of routing path shows zero laptop-resolved targets.
METHOD: config audit.
GOV-02 Autonomous actions that spend money SHALL inherit the destructive
capability class: quorum + hardware signature (COST-02). No separately
invented authority. (S3 §6, S4 AGENTS.md [capabilities])
ACCEPT: capability classifier maps tier-activation to destructive class.
METHOD: config review.

## Traceability matrix (S1 buffet -> REQ) — mechanical coverage check

Pillar 1 Hollow Model (LiteLLM routing)      -> ROUTE-01 (real), ROUTE-05 (gap)
Pillar 1 Gatekeeper 1.5B local model         -> ROUTE-06, JIT-02 (real: ollama.yaml)
Pillar 2 execute_python CPU sandbox          -> OFF-02 (NAMED GAP)
Pillar 3 Grind Tool CronJob worker           -> GRIND-01 (NAMED GAP)
Pillar 4 Darwin Machines meta-optimizer      -> DARWIN-01 (UNCONFIRMED -> gap)
CEGIS/Z3 blocking clauses + SMT-LIB          -> VER-01 (real: verifier.py)
Differentiable execution graphs / do-calculus -> OPEN (see Decision register)
Refinement types / proof-carrying actions     -> OPEN (needs DSL decision)
Storage L3 (OCI object + Postgres)            -> covered by existing estate (S4)
Speculative decoding                          -> FL-01
KV-cache quantization / IQ3                    -> rejected at intake: real
precision loss (S3) — tradeoff named, not free
Semantic traffic cop                           -> ROUTE-05 (gap, axis only)
Flat-rate rented Apple Silicon                 -> COST-03, JIT-01 (breakeven-gated)
Vast.ai GPU burst                              -> COST-03 ladder Rung 3 (receipt-pending)
Local swarm (CrewAI/LangGraph)                -> ORCH-01 (Temporal instead)
TRL/TwiL-LM3/VibeThinker specialists           -> OPEN-3 (sources pending; see §7)
Coverage rule: any S1 line not in this matrix is a spec defect; count must be zero.

## 7. Decision register (defaults let work proceed; questions never block)

D1  Scaleway hourly vs flat-monthly: same product or two? DEFAULT: treat as
distinct product lines; check vendor pages before cost model. OWNER: founder.
D2  TRM 45% ARC-AGI / VibeThinker 94.3 AIME: need primary sources.
DEFAULT: excluded from all capability/cost decisions until sourced.
D3  MoE (Qwen3-Coder-Next class) vs dense 32B for rented node memory profile.
DEFAULT: re-evaluate when a node is actually procured; not before.
D4  Vast.ai figures are founder-supplied-unverified. DEFAULT: usable as upper
bound only; re-pull from marketplace before any activation.
D5  Do-calculus counterfactual repair / refinement-type DSL: unbuilt, unfunded
in this spec. DEFAULT: out of scope v0.1; revisit after DARWIN-01 lands.
D6  Demo boundary for first end-to-end run: DEFAULT fleetview (existing proxy
path, smallest surface) unless founder overrides.

## 8. Verification methods glossary

unit/property = code tests; integration = against real components;
fault-injection = kill/breach during flow; trace-query = Langfuse SQL;
eval suite = fixed task corpus with known answers; config audit/review =
static verification of the spec's own config rules.

## 9. P0 prerequisite (before any "hard-metered" claim is made)

P0-01 request_ceiling.proxy_handler_instance SHALL become a severing breaker.
Warn-only is proven false (86.5M-token/hour incident). Everything in
§1-8 depending on COST-01 is fiction until P0-01 lands.. TH ASEWR TO 99% percent of your questions is we need everything and the the seanless abiluty to enable , disbale eire fuly natri ocnfiguration and once oncfiged needs to be super inntelligent and , eeds unconnon and rare peoduct design and systenn engierring chops and skill
