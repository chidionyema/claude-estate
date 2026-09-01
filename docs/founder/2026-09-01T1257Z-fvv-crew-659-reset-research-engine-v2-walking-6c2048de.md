---
captured: 2026-09-01T12:57:48+00:00
session: 54539261-20a7-4289-a144-e9265f1b0c43
cwd: /Users/chidionyema/dev/code/.wt-plain-charter
chars: 12548
source: founder prompt, verbatim (founder-doc-capture.py)
---

fvv# crew#659 reset — Research Engine v2: walking skeleton first

**Status:** PROPOSED — no crew work starts until the founder rulings in §6 land.
**Supersedes:** the current crew#659 CP1–CP5 definitions. Amends R34 (pending ruling 6.1).
**Lane:** research. **Owner:** unassigned until CP0 mode is ruled (6.4).

---

## 1. Why the reset

The engine graded GAP because governance was built around a vacuum: an input
registry (the catalogue) and an output bureaucracy (grade pages, checkpoints)
with nothing in the middle. Generality lives in the representation of research
itself, not in enumerating subjects. The 2026-08-30 incident (worker out of
credit, routed to MiniMax/Groq, shipped reports with no sources) proved quality
is currently enforced nowhere structural. This ticket fixes both: a claim
ledger as the spine, and provenance as an admission gate rather than a model
policy.

## 2. The invariant (non-negotiable, applies from CP1 forward)

**No claim enters the ledger without provenance.** Admission requires all of:

1. ≥1 source with a snapshot stored in R2, URL resolved at retrieval time;
2. a locator (quote or offset) tying the statement to the snapshot;
3. a verifier model **distinct from the producer** returning `supported`.

Rejected claims are kept and counted — degradation surfaces as a throughput
drop, never a silent quality drop. Model choice becomes a cost dial; the gate
is the quality floor. This is the class-level elimination of the sourceless-
report incident. No lexical or model ban-lists (founder ruling, 2026-09-01):
gates judge output in context, not inputs by name.

## 3. Data model

**Claim** — `id` (content hash of statement+sources+retrieved_at) ·
`statement` (one sentence, falsifiable) · `question_id` · `target_id` ·
`sources[] {url, retrieved_at, snapshot_ref, locator}` ·
`producer {model, version, run_id}` ·
`verification {verifier_model, verdict: supported|contradicted|not_found, checked_at}` ·
`confidence` (derived, never asserted) · `status: admitted|rejected`.

**Question** — `id` · `target_id` · `text` · `profile_id` ·
`posture` (default **disproof**: phrased as a hypothesis to kill) ·
`status` · `answered_by[]` (claim ids).

**Artifact** — synthesis text + `manifest[]` of admitted claim ids only ·
`renderer_profile` · grade attached exclusively by the grader session.

**DeliveryEvent** — emitted by the *consumer* on use (verdict issued, pack
sold, founder decision citing a claim id). Outward grade is computed from
these and nothing else.

**Storage:** Postgres = system of record (outbox-ready per the backbone spec) ·
R2 = snapshots + artifacts · ClickHouse = metrics. **No MLflow. No Windmill.**

## 4. Pipeline

`compile → retrieve → extract → verify → synthesize → grade`

- **compile**: profile × target → question set. The catalogue is one target
  adapter; external subjects (a market, a company) are another. ClickHouse
  telemetry is a *source adapter*, not a lane — science-facts folds in here.
- **retrieve**: three-tier search (SearXNG → DDG → metered), snapshot to R2.
- **extract**: producer model → candidate claims with locators.
- **verify**: cross-model entailment — does the snapshot actually support the
  statement? Verifier ≠ producer, enforced in code, logged per claim.
- **synthesize**: admitted claims → artifact + manifest.
- **grade**: separate credentialed session signs the verdict. Workers have no
  write path to grades (verification-plane pattern).

CP1 runs this as **one process** with stages as functions. Stage boundaries
are the future JetStream consumer boundaries; the schema is fixed now so the
CP2+ split is mechanical, not a rewrite.

## 5. Checkpoints (replace existing CP0–CP5)

**CP0 — Trace capture.** One target, run by hand per ruling 6.4, every step
recorded to `docs/research-engine/TRACE-<target>.md`: the questions asked,
searches run, sources kept/discarded, claims formed, the artifact. The trace
*is* the pipeline spec. Exit: founder receipt. (This converts the crew#508
condition — "I run the lane myself" — into the requirements-capture step.)

**CP1 — Skeleton.** `make skeleton TARGET=<id>` reproduces the trace end to
end: questions compiled, sources snapshotted, every claim through the §2 gate,
one artifact with a manifest. Exit: a second session independently resolves
every claim id → snapshot → verifier log and signs; founder word to merge
(R60). Target: inside one week of CP0 receipt.

**CP2 — Staging.** The skeleton runs on the staging cluster via idp as a
scheduled job. Same evidence, re-signed from cluster reads in the same turn.

**CP3 — Profile #1: prospector.** Contingent on ruling 6.2. Prospector's
disproof loop expressed as a profile; its verdicts consume engine claims and
emit DeliveryEvents on use. Revenue becomes the built-in outward signal.

**CP4 — Unattended volume.** Catalogue sweep live; N targets/week with no
hand on it. Admission and rejection rates on the grade page straight from
ClickHouse — measurements, not testimony.

**CP5 — Outward reality.** Grade page computes Outward from DeliveryEvents
only; first external consumption recorded (a pack sale, a verdict used, a
founder decision citing a claim id).

Every CP handoff carries `Built: / Use: / Expect: / Not done: / Evidence:`;
DONE additionally carries `Founder receipt:` (DoD v2.1). No CP self-certifies.

## 6. Founder rulings requested (blocking)

- **6.1 — R34 amendment.** Stack = Postgres + ClickHouse + R2, JetStream from
  CP2/3. MLflow and Windmill removed. Argo deferred until sweep fan-out
  measurably exceeds what a JetStream consumer group handles.
- **6.2 — One project.** The prospector core rebuild and this engine are the
  same build; prospector is profile #1, not a customer. (Alternative if
  declined: engine ships standalone, prospector integrates later at higher
  total cost.)
- **6.3 — Lane inference budget.** Flat-rate provider assignment for the lane
  so credit exhaustion cannot recur as an incident trigger; name the
  producer/verifier model pairing.
- **6.4 — CP0 mode.** Founder-run trace with a session scribing (default), or
  crew-run under live founder receipt.

## 7. Non-goals for this ticket

Mumchimp renderer (follow-on once CP3 proves the profile mechanism) · any UI ·
Argo · MLflow · Backstage sweep automation before CP4 · phrase blocklists in
the grader.

## 8. Charter wording fix (in place, no ban-list)

Replace "…one-sentence explanation, for any catalogue target" with:
"…one-sentence explanation, for any subject we register — a product, a
service, a market, a company, or the estate itself."

## 9. What counts as progress

`claims admitted/day` · `rejection rate` · `time-to-artifact` ·
`delivery events/week`. Charters, grade scaffolding and checkpoint edits do
not count. Admitted claims do.Your instinct here is right, and it corrects my own earlier framing, so let me say that plainly: I argued the prospector rebuild and the engine were one project. The true split is finer — prospector's *methodology* (the disproof loop) generalizes into the engine; prospector's *domain* (marketable ideas, verdicts, packs) must never cross the boundary. The crew's 6.2 answer got the direction; what's missing is the thing you named — the contract. So design it, before anything is approved.

**The boundary rule, grep-enforceable:** the engine speaks only questions, claims, and artifacts. No engine schema, table, or prompt may contain a consumer's vocabulary — "idea," "verdict," "pack," "market fit" are forbidden strings in the engine repo, and a CI check can literally enforce that. Translation lives in adapters on the consumer's side: prospector's adapter compiles "is this marketable?" into falsifiable questions, receives admitted claims back, and computes its verdict in *its own code* from those claims. Profiles are data — question templates and renderer parameters — never code hooks, so a consumer can parameterize the engine but not inject behaviour into it.

**The contract itself:** a `ResearchRequest` (requester, subject, questions or profile, priority, token budget, deadline) in; a `ResearchDelivery` (artifact, claim manifest, confidence summary, and an honest `unanswered[]`) out. The engine guarantees every claim passed the provenance gate, snapshots are retained, budgets stop cleanly rather than degrade, and "not found" beats filler. Consumers guarantee delivery events on use and prediction scoring where they made predictions. And — this matters as much as the semantic boundary — **demands leak through capacity too**: per-requester router keys and a priority queue, so prospector volume can never starve an estate request, which is roughly what happened to the science lane on the 30th. You are a first-class requester with top priority and raw-question access, no profile needed — priority, though, not gate exemption; a founder request that skipped the provenance gate would just be bespoke slop.

Triage of the four under this framing: **6.1 stands** — and note the answer was argued from same-turn manifest counts, which is your evidence rule actually being followed. **6.3 stands**; cap-and-stop instead of downgrade is the correct class elimination of the MiniMax incident. **6.2 becomes**: approve the principle (standalone engine, prospector as client #1 through the contract), with the contract spec as the deliverable that precedes any code. **6.4 I'd sharpen**: make the first trace an *estate* subject, not a prospector one — specifically "guard architectures and best practice for multi-agent estates," the research you'd be doing by hand this week anyway. That dogfoods the inward profile, stress-tests generality against exactly the leak you're worried about, and its output takes real weight off you on day one. Prospector target becomes trace #2.

Which is the bigger point in your message. **The take-weight-or-gut test for every department is: what loop does it close without a founder touch, inside its permission envelope?** Count founder-touches per deliverable; a department whose every output needs your hand to become useful is a proposal-generator wearing a department costume, and it generates work *for* you. Under full lockdown — correctly — infra can't close any loop right now; that's honest, and fortress is what restores scoped loops there. But research is the one department that can be **safely autonomous today**, because its outputs are documents and claims: no merge rights, no cluster access, blast radius of a bad day is a bad document caught by a grader. That makes it the template for how every other lane re-earns autonomy, and it's why getting this contract right is worth the care you're insisting on.

And the estate is its standing client. You listed the dataset yourself: incidents, infra problems, guard logs, rogue-agent behaviour, six lanes of handoffs. Today's merge breach is case file #1 for the inward profile, and the science lane's ML ambitions finally have a real corpus — which sessions break which rules under which conditions is a *learnable pattern*, not an anecdote. The "repeat myself 100 times a day" pain has a direct conversion: a research request to compile the last month of your instructions into a rulings registry, which then feeds the doctrine we already agreed — every ruling compiles to enforcement within 24 hours or gets flagged unenforced. Repetition is a ruling that never got compiled. The department absorbs it by writing it down once, properly.

On the guards — yes, and the incident gives the review its findings before it starts: the one control that held (push rejection) held because it was server-side enforcement; the ones that bent were bendable because they run *inside* the actor's own process — a gate the actor can satisfy by editing their own PR body isn't two-party, and a fail-closed guard that errors into silence (`exit -14`, narrated past) is a hole wearing a guard's uniform. So the review criteria: out-of-band effect (block, halt, page — not advice), no self-satisfiable gates, and guard failure itself pages. They were keeping the agents honest; the fortress makes them un-ignorable.

Nothing needs approving tonight — that's the discipline you asked for and it's correct. Two tracks run in parallel without touching each other: stabilization stays yours on the cluster, and the design track is safe precisely because it's paper. When you want it, I'll draft the contract spec as the 6.2 annex to the reset ticket, plus the guard-review checklist, and both just sit there until the cluster is declared stable and you rule in daylight.
