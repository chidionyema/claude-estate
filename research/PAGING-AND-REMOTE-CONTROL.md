# Paging the founder, and driving the Mac from a phone

**Founder's words, 2026-08-21:** *"also for autonoyy , sending alert to founder telegran when
stck on task/decisino that cant resolve or when console freeses or claude api tines out , need
sone process to page founder and be able to recover , nsyber founder needs better tooling to be
able to connec to nacbook fron telegran renotly, do research and action, super inportant, need
thenost seanless and user fiendly setup an design, add to lisy of req"*

And the constraint that shapes every rule below: *"that dot self heal"* — a condition that clears
itself must never page.

**Method.** 19 web searches, 34 pages fetched, 2026-08-21. Sources are named inline. Where a claim
could not be confirmed it says so; there is one of those and it is flagged.

---

## 1. What decides whether something is allowed to page

**Google SRE, *Site Reliability Engineering*, ch. 6 "Monitoring Distributed Systems":**

> *"Every page should be actionable."*
> *"If a page merely merits a robotic response, it shouldn't be a page."*

That second sentence is the founder's *"that dot self heal"* in Google's words, and it is the
single rule that decides the whole design. It gives a mechanical test to apply to every candidate
alert: **if the correct response is something a machine could do, build the machine, do not send
the message.**

**The load ceiling is measured, not chosen.** Google's stated maximum sustainable on-call load is
**2 incidents per 12-hour shift**. Anything above that is not a busier operator; it is an operator
who stops reading.

**The four attributes of a good alert** (Google SRE Workbook, ch. 5 "Alerting on SLOs"):
precision, recall, detection time, and **reset time**. Reset time is the formal name for the
founder's complaint — how long an alert keeps firing after the condition has gone. The published
remedy is **multiwindow, multi-burn-rate alerting**: a long window establishes the condition is
real, a short window lets it clear quickly. Both windows must agree before it pages, and the short
window alone can silence it.

**Alert fatigue is measured and it is severe.** Published false-alarm rates for clinical alarm
systems run **72–99%**. The FDA's MAUDE database recorded **566 alarm-related patient deaths
between 2005 and 2008**. Interventions that pruned alarm sources cut the rate from **180 to 40
alarms per patient-day** without missing events. The lesson transfers exactly: the failure mode of
a noisy pager is not annoyance, it is that the real page is not read.

**Automation bias means a tap-to-approve button will be rubber-stamped.** Parasuraman & Manzey
(2010), *Complacency and Bias in Human Use of Automation*, concluded that automation bias
**"cannot be prevented by training or instructions"**. Design consequence, and it is not
negotiable: make approval requests **rare**, make each one carry the specific fact that decides it,
and make the **timeout default to DENY**, never to approve.

## 2. Detecting a stuck agent — it has to be external, and it has to fire on absence

**Nothing inside Claude Code can detect a wedged Claude Code session.** Every hook event —
PreToolUse, PostToolUse, Stop, SessionStart — is driven by the session *doing something*. A session
that is stuck emits no event at all, so a hook can never be the detector. Measured on this estate;
it is a property of the hook model, not a bug.

So the detector must live outside and must fire on **absence**:

- **Heartbeat out, not poll in.** The agent posts "I am alive" on a cadence; the *watcher* pages
  when the post does not arrive. Prometheus expresses this as `absent_over_time()`.
- **A liveness ping is not a progress signal.** An agent can loop forever and keep pinging. The
  second signal is a **monotonic progress counter** — steps completed, files touched, tokens spent
  on the named job — with the alert `increase(progress[30m]) == 0`. Alive-but-not-moving is the
  failure mode this estate actually has.
- **The watchdog must be inverted, and must not live on the dying laptop.** kube-prometheus ships
  a **Watchdog** alert that fires *constantly* on purpose, and Dead Man's Snitch pages when it
  *stops* arriving. A monitor running on the MacBook dies with the MacBook and reports nothing.

**The grace period has a published rule.** Prometheus' own batch-job guidance: set the staleness
threshold to **at least 2× the job period**. A job on a 300s `StartInterval` gets a 600s grace.
Anything tighter pages on one skipped firing.

## 3. macOS-specific facts, measured or cited

| Fact | Source | Consequence |
| --- | --- | --- |
| **launchd has no `WatchdogSec` equivalent** (systemd has one) | launchd.plist(5) — no such key exists | A hung launchd job runs forever. Any timeout must be inside the job. `launchd_receipt.py` is this estate's answer. |
| `StartInterval` **misses** firings while the machine sleeps | launchd.plist(5), Apple | A 5-minute job is not a 5-minute job on a laptop. |
| `StartCalendarInterval` **coalesces** missed firings and fires on wake | launchd.plist(5), Apple | Use it where a missed run matters. (launchd.info contradicts Apple here; Apple's man page wins until this estate measures it.) |
| `ThrottleInterval` defaults to **10s** | launchd.plist(5) | A crash-looping job restarts at most ~6×/min — it will not melt the box, and it also will not self-heal fast. |
| `KeepAlive.SuccessfulExit` | launchd.plist(5) | The switch that separates "restart on crash" from "restart always". |
| `caffeinate -i -w <pid>` holds sleep off for a specific process | caffeinate(8) | The way to keep a long agent run alive. **`caffeinate -s` is void on battery** — it only works on AC. |
| TCC grants are **per binary**, and a Homebrew Python upgrade silently invalidates the grant | measured on this estate 2026-08-21 | Pin the interpreter path in every plist. See memory `a-launchd-job-dies-twice-under-tcc`. |
| Re-granting Full Disk Access is **GUI-only** | System Settings has no CLI equivalent | **It cannot be done over SSH.** A remote-recovery design must not depend on it. |

## 4. Telegram, as a control plane

Confirmed against the Telegram Bot API docs, 2026-08-21:

- **Rate limits:** 1 message/second per chat; ~20 messages/minute to a group; **4096 characters**
  per message.
- **`callback_data` is 1–64 bytes.** Anything bigger has to be an id into local state.
- **`answerCallbackQuery` is mandatory** after a button press, or the client spins.
- **Use `parse_mode=HTML`, never MarkdownV2.** MarkdownV2 requires escaping `.`, `-`, `(`, `!` and
  more; a single unescaped `.` in a file path fails the entire send. Every message this estate
  sends contains file paths.
- **Long polling needs no tunnel and no public URL.** `getUpdates` from behind the laptop's NAT is
  the whole transport. No webhook, no ngrok, no inbound port.
- **Updates are retained 24 hours.** A bot that is down for a day loses the commands sent to it.
- **The bot token is a bearer credential** — anyone holding it is the bot.
- **`from.id` must be allow-listed on every single update.** A bot with a public username can be
  messaged by anyone. This is the one security control that matters and it is per-update, not
  per-session.
- **Bot chats are not end-to-end encrypted.** Telegram can read them. Nothing secret goes in a
  message body.

**Critical alerts on iOS: UNVERIFIED.** Whether Telegram can break through Focus/Do Not Disturb
with a repeat-until-acknowledged alert could not be confirmed from any authoritative source. The
only channel with *documented* repeat-until-acknowledged behaviour is **Pushover priority 2**
($4.99 one-time, per platform). If a condition genuinely needs to wake the founder at 3am, that is
the mechanism; Telegram carries everything else.

## 5. Open-source components worth reusing rather than building

| Tool | Licence | Signal | What it gives us |
| --- | --- | --- | --- |
| **healthchecks.io** | BSD-3 | 20 free checks on the hosted tier; self-hostable | Exactly the inverted heartbeat in §2, with native Telegram delivery and a grace period per check. Least code of any option. |
| **Uptime Kuma** | MIT | 90.4k★ | Push monitors, self-hosted, a dashboard the founder can open on a phone. |
| **Gatus** | Apache-2.0 | — | Declarative YAML health checks; fits an estate that already keeps config in files. |
| **ntfy** | Apache-2.0 | — | Push with **up to 3 action buttons** per notification; self-hostable. |
| **alexei-led/ccgram** | MIT, 248★, pushed 2026-08-20 | actively maintained | Claude Code ↔ Telegram bridge over tmux. The most current of the bridges. |
| ~~RichardAtCT/claude-code-telegram~~ | **NO LICENCE** | 2761★ | **Not reusable.** No licence means no grant of rights. Read it for ideas, copy nothing. |

## 6. Phone → Mac, for recovery

**Tailscale SSH does not work on a normal Mac install.** The SSH *server* half is unavailable on
the standard macOS builds (Tailscale issues #4518, #18957). Do not design around it.

What does work: **Tailscale as the network layer** (so no port is exposed) + **macOS built-in
Remote Login** for SSH + **tmux** so a session survives the phone disconnecting + **Blink Shell**
as the client.

A practitioner's warning, and it is the honest limit of this approach:

> *"the phone still has to be a full terminal. That gets rough once the agent prints long output,
> diffs, or permission prompts."*

**Design consequence:** the phone is for **deciding**, not for **working**. Telegram carries the
decision — a short, specific question with buttons. SSH+tmux is the escape hatch for the times a
decision is not enough. Building a rich phone UI over a terminal is the trap.

## 7. Spend — the condition most likely to actually matter

- **Anthropic API spend caps are MONTHLY, not daily** (Start $500 / Build $1,000 / Scale $200,000).
  A **$120/day cap is not enforceable by the provider** and must be self-enforced by this estate.
  Measured 2026-08-21: **$483.05 spent against the $120 cap by 06:40**, with the halt cap
  **DISARMED** in `~/.claude/estate-budget.json`.
- **Two 429s that mean opposite things:**
  - `429` carrying `enforced_spend_limit_reached` has **no `retry-after`** and does **not**
    self-heal. **Page.**
  - A plain `429` with a `retry-after` header is backpressure and clears itself. **Never page.**
  This distinction is exactly the `errors.classify_exhaustion` split the engine already makes; the
  pager must make the same one or it will page on every busy minute.

## 8. What this says to build

In order, cheapest first:

1. **Heartbeat out to an external watcher**, grace = 2× the job period (§2, §3). The watcher is
   not on the laptop.
2. **A monotonic progress counter** beside the heartbeat, so alive-but-wedged is detectable (§2).
3. **Telegram for decisions**, HTML parse mode, `from.id` allow-listed on every update, timeout
   defaults to DENY (§1, §4).
4. **Pushover priority 2 for the wake-him conditions only** — and there should be about three
   (§4).
5. **A self-enforced daily spend kill**, because the provider will not enforce one (§7).
6. **`StartCalendarInterval` where a missed run matters**, and `caffeinate -i -w` around long runs
   (§3).
7. **Tailscale + Remote Login + tmux + Blink** as the escape hatch, not as the primary interface
   (§6).

**The biggest failure risk in the whole design, stated plainly: a sleeping MacBook is
byte-identical to a dead agent.** Both stop sending. Any watcher that cannot tell them apart will
either page every night or miss the real outage. Resolving that ambiguity — a sleep/wake marker the
agent writes, or an alert window that respects the founder's hours — is the first design decision,
not an afterthought.

---

*Related: [`REASONING-AND-JUDGEMENT.md`](REASONING-AND-JUDGEMENT.md) (pending),
[`HERMES.md`](HERMES.md), memory `a-launchd-job-dies-twice-under-tcc`.*
