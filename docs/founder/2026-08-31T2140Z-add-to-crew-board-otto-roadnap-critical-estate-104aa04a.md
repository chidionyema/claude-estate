---
captured: 2026-08-31T21:40:23+00:00
session: ef0354ef-fa6b-4b6b-a5e2-5d6f7889b3b8
cwd: /Users/chidionyema/dev/code/.wt-agents-stack
chars: 9763
source: founder prompt, verbatim (founder-doc-capture.py)
---

add to crew board Otto roadnap critical estate project but not yet staerting 
chidi onyema <chidionyema@gmail.com>
10:38 PM (0 minutes ago)
to me

# Otto Roadmap — Platform to Embodiment, v1.0

**Date:** 31 August 2026 · **Companion to:** Otto Platform Build Spec v1.0
**Reading rule:** dates harden as they approach. 2026 items are commitments, 2027 items are plans, H4+ items are bets with explicit change-triggers. The Constitution (P1–P8) and the eval gate (P6) are invariant across every horizon — each new surface, sense, or body ships with its own eval slice and red-team slice, or it doesn't ship.

---

## The through-line

One brain, many skins, growing senses, then hands. Every horizon adds surfaces or capabilities to the *same* task plane behind the *same* gateway. Nothing at any horizon — not voice, not glasses, not a robot — ever gets a path around the tiers, the taint rules, or the Verification Plane. The platform is the appreciating asset; models, devices, and bodies are swappable engines proven by eval deltas.

---

## H0 — The Platform (Sept → mid-Dec 2026)

Build Spec v1 Phases 0–5, one senior engineer, ~12 weeks from start.

**Chidi's parallel work (cannot be delegated):**
- Curate the eval corpus: 40–60 real tasks + the 10-task false-success set (Phase 0 dependency).
- Resolve the four DECISIONs: bulk-lane model, secrets backend, trace backend, gVisor availability.
- **Apply immediately for the Meta Wearables Device Access Toolkit developer preview** (H1 dependency — access approval is a queue you don't control; join it now).
- Order glasses hardware (see H1 risk R-G2).

**Exit gate:** all Phase 0–5 acceptance criteria green; platform operable from Telegram alone for a normal week.

---

## H1 — Voice, Companion App, Glasses (Oct → Dec 2026)

Overlaps H0: starts once the tool gateway and tiers exist (Phase 1 exit, ~mid-Oct). Goal: **Otto on your face before year end.**

### H1.1 Interaction plane (voice)
- LiveKit Agents self-hosted on the staging cluster; cascade STT → router → TTS.
- Latency budget: ≤ 800ms perceived end-to-end at launch, ≤ 500ms target; barge-in handled.
- Runs at **T0 read-only, no verdicts** — it converses and *proposes* tasks; anything above T0 becomes a task envelope through the normal gateway. Voice is a mouth and ears, never hands.
- SIP + phone number: Otto can take and place calls (outbound calls to third parties are T2 and disclose agent identity).
- Persona skill renders the voice register; same skill, same P1 rule — no spoken claim without a read behind it.

### H1.2 Otto companion app (the critical path to glasses)
Telegram cannot render on a lens. Meta's toolkit extends *your own* iOS/Android app onto the glasses — so a thin native companion app is the glasses gateway. Scope ruthlessly:
- Chat + voice session (WebRTC to the interaction plane).
- Push notifications for status, verdicts, digests.
- **Approval cards**: T2/T3 approve/deny with the untrusted-source list attached — this is the app's reason to exist.
- Passkey-bound session = a first-class authenticated principal in the identity plane.
No feature beyond these four in v1.

### H1.3 Glasses surface (Ray-Ban Display, dev preview)
- Extend the companion app via the Wearables Device Access Toolkit: glanceable cards (task status, verdicts, morning digest), voice loop through the glasses' mic/speakers, **T2 approvals via Neural Band gesture** (T3 remains phone-app tap only).
- All camera/mic capture enters as trust class `ambient`: observations, never instructions. Capture is push-to-talk/explicit at this horizon — no always-on.
- **No-voiceprint rule live from day one:** voice never authenticates; identity comes from the paired, passkey-bound phone.

### H1.4 Spec v1.1 (written during H1, from what we've brainstormed)
Channel plane (adapters → task envelope), identity plane (principal registry, device-bound approval, no-voiceprint), presence kernel (one conversation state across surfaces), `ambient` trust class formalized.

**Risks to "glasses this year":**
- **R-G1 — Dev preview access.** Approval queue is Meta's. *Mitigation:* apply now (H0 action); fallback = Brilliant Labs Halo (fully open source) so you are on *a* pair of glasses in 2026 regardless.
- **R-G2 — UK availability.** Ray-Ban Display launched US-first. *Mitigation:* confirm UK retail at time of order; if unavailable, US purchase/import or Halo fallback.
- **R-G3 — Companion app underestimated.** *Mitigation:* the four-feature scope cap above; everything else stays in Telegram.

**Exit gate:** you approve a real T2 action from the glasses; voice session survives a walk to the shops; red-team slice for voice + ambient passes (injection via spoken content, via a sign held to the camera).

---

## H2 — Every Surface + Twin Stage 1 (Q1–Q2 2027)

### H2.1 Channel plane rollout
Adapters, one at a time, each landing with its eval slice + red-team slice before the next begins: **email (in/out) → WhatsApp → Slack/Discord → iMessage (if bridging is viable then)**. Every non-Chidi sender on every channel is untrusted by default; the two-source rule caps accordingly. Sequencing rule: an adapter that fails its red-team slice blocks the queue — breadth never outruns hardening.

### H2.2 Presence kernel ships
Start a thread on glasses, continue at the desk, finish by voice in the kitchen — one conversation state, per-surface rendering. This is the single highest-"alive" feature on the roadmap.

### H2.3 Twin Stage 1 — *drafts as you* (T1 only)
- Style skill conditioned on your writing corpus (no fine-tuning; deferral triggers in Spec §16 stand).
- Otto drafts replies across all channels in your voice; **nothing sends without you**.
- Comms ledger live: every as-Chidi word on the stream, replayable.
- Eval: style-fidelity slice (blind you-vs-Otto drafts, scored by you weekly).

### H2.4 Vision Stage 1
Images/frames as first-class task inputs (envelope already supports it); glasses capture → described observations with provenance into memory. Printed-text injection attacks join the standing red-team suite.

---

## H3 — Twin Stage 2 + Ambient Otto (Q3–Q4 2027)

- **Twin Stage 2 — approved sends (T2):** batched approval cards; you tap, Otto sends as you.
- **Twin Stage 3 — disclosed autonomy (scoped T2):** for named low-stakes classes (scheduling threads, vendor follow-ups) after a 30-day clean approval record per class; every autonomous message carries agent disclosure (EU AI Act Art. 50 posture — the twin persuades no one it is you without your finger on the send).
- **Ambient Otto:** proactive rhythm — morning brief on the lens, context-aware nudges from `ambient` observations, end-of-day episode review. Proactivity is T1 (it may *tell* you anything; it *does* nothing new).
- **Second glasses platform:** Android XR display models as they land — the channel plane makes this an adapter, not a rewrite.
- **Capture ethics runbook:** consent norms, buffer retention, UK recording law for third parties in frame — written before always-on capture is ever enabled, and always-on remains a separate, explicit decision gated on it.

---

## H4 — Embodiment (2027–2028, provisional by design)

Robotics hardware and prices will change; the *staging* won't. Re-price and re-select hardware at horizon entry via a fresh landscape eval — never from this document.

- **R0 — Simulated & teleoperated:** Otto plans physical tasks, you (or sim) execute; robot-as-telepresence (a mobile camera/speaker is just another surface + `ambient` sensor). No actuation authority at all.
- **R1 — Constrained actuation:** one bounded environment (a room, a bench), reversible motions only, geofenced. **Every actuation begins T3.** Reversible motion classes may earn standing T2 within the geofence after an incident-free record — the same earn-down pattern as email sends.
- **R2 — The Verification Plane grows eyes:** prover gets independent cameras/sensors; physical completion claims ("the object is on the shelf") verified by the prover's *own* sensing, never the robot's self-report. P1, embodied.
- **Hard rules, permanent:** no actuation from a task containing untrusted or unreviewed ambient content; emergency stop is hardware, not software; humans and pets in frame = automatic pause class.

---

## H5 — Beyond (directional)

- **The compounding loop:** every industry model release = router YAML + eval run; upgrades land in days. Funding arrival = GPU node pool + local vLLM lane on the same cluster — a config change, reserved since day one.
- **Skill economy:** procedures → skills flywheel matures into Otto proposing, testing (in sandbox), and submitting new skills as PRs — self-improvement with you as merge authority, P7 forever.
- **Otto as chief of staff:** Otto fronting the estate's departmental crew — one verified interface over many working agents, charters as machine-readable contracts on the bus.
- **Interfaces watch-brief:** agent-interop protocols, neural-band-class input evolution, on-device inference on wearables. Watched, evaled on arrival, never pre-committed.

---

## What would change this roadmap (standing triggers)

| Trigger | Response |
|---|---|
| Frontier model leap (agentic or realtime multimodal) | Router lane swap + full eval run; roadmap dates may *compress* |
| Glasses platform shift (Meta closes/limits toolkit; Android XR opens agent-deep) | Channel-plane adapter swap; H1.3 fallback chain applies |
| GPU funds arrive | Local lane per H5; nothing else moves |
| Robotics capability/price inflection | H4 entry re-eval; may pull forward — staging order never changes |
| Any security incident on any surface | Freeze new-surface rollout; class-level fix (P8) ships first |

---

*One brain. Many skins. Growing senses. Earned hands. Verified always.*
