# Divide and conquer — Part 1, the measured evidence

Measured 2026-08-21 on this estate. Every number below has the command that produced it.
This file is the evidence base for `DIVIDE-AND-CONQUER-PROTOCOL.md` (R34). It exists
separately because the measurement contradicted the premise the spec was going to be
built on, and that correction is worth more than the spec draft it replaced.

Founder's words (R34): *"and also critial an ultra efficient seanless divive and conqure/
parallel agent protocol , including taking raw pronp spec, distibute andc coordinate,
collision nanagennt, etc reviw-ship anything i niss, we have atteped this bitneeds
perfectin"*.

## 1. Cross-session duplicate discovery is ALREADY SOLVED. Do not build for it.

The premise was the founder's 2026-08-20 complaint: the peer channel *"keeps everyone
loppingevrt he sane issues"* — six sessions each finding the same wedge and each telling
the other five. `peer-loop-fence.py` was built to refuse that. **It worked.**

Two angles, sharing no mechanism, agree:

**Angle 1 — containment of significant tokens at 0.55**, the fence's own metric, applied to
every pair on the board:

    board rows          : 71        (6 distinct sessions)
    pairs compared      : 2485
    duplicate pairs     : 16
      cross-session     : 0
    rows in a cross-session dup: 0 of 71 = 0%

**Angle 2 — distinctive subject tokens** (PR numbers, file paths, script names) extracted by
regex and grouped by how many sessions named each. Shares no code and no threshold with
angle 1, so it fails differently:

    subjects named by >1 session: 6 of 32
    subjects named by >2 session: 0

Two sessions touching `live_checkout.py` is overlap, not a duplicate discovery, and nothing
at all is named by three.

**So the coordination half of R34 is not the gap.** A protocol that spends its effort on
"stop agents rediscovering each other's findings" would be building a second lock for a
door already locked.

## 2. What the 16 duplicates actually are: a session repeating ITSELF.

    9 of 16   pr-reactor / pr-reactor
    3 of 16   ...892de6 / ...892de6
    3 of 16   ...f9da7f / ...f9da7f
    1 of 16   ...ed46e4 / ...ed46e4

`pr-reactor` re-posts the same message on a timer — *"PR #544 is CONFLICT and needs a
person. CAUSE: STILL CONFLICT after 45 minutes"*, then after 49, then 162. The fence grades
a message against OTHER sessions' entries, so a session cannot be refused for repeating
itself. That is a real defect and it is a one-line fix, not a protocol.

The other 7 are honest re-raises: a session correcting a finding it had already sent, which
LAW 10's `Re-raising:` hatch explicitly permits.

## 3. The real throughput ceiling is a fence, and it is a deliberate cost decision.

`~/.claude/scripts/agent-fleet-fence.py` caps the estate at **3 live subagent leases**, four
agents including the main loop (founder directive 2026-08-20), each lease expiring 20
minutes after it is granted. Measured this turn: a fan-out of 4 independent tasks had its
fourth refused.

So on this estate "divide and conquer" has a hard width of 4, and the protocol must be
written for that width rather than for an unbounded fan-out. The interesting question is
therefore not *how do we parallelise more* but *which 3 tasks are worth a lease right now*,
and that is a prioritisation rule, not a coordination one.

## 4. What this leaves as the actual gaps in R34

Coordination: SOLVED (§1). The remaining five parts the founder named are open:

| Part | State | Why |
| --- | --- | --- |
| Raw prompt spec -> decomposition | OPEN | no rule exists for what is splittable; it is done by feel, badly — measured this turn: four independent items were worked serially until the founder said *"ur going slow"* |
| Distribute / assign | OPEN | no task-class -> model-tier map, against a standing rule to use the cheapest capable agent |
| Coordinate | **SOLVED** | `peer-loop-fence.py`, 0 cross-session duplicates in 2485 pairs |
| Collision management | PARTLY | `one-branch-fence.py` gives one branch + one worktree per session. Crude but effective; it is a lock, not a scheduler |
| Review -> ship | OPEN, and hard | an LLM grading another LLM's reasoning tracks fluency at rank correlation **+0.75** while causal importance sits at **-0.004**, i.e. chance (arXiv:2608.19760, in `RAW-reasoning-and-judgement.md`). So agent-reviews-agent is not a verification mechanism. Verification has to be an executable oracle — a test, a command, a diff |
| Abort / partial failure / visibility | OPEN | nothing tells the founder a fan-out is running or lets him stop it; his top standing complaint is visibility |

## 5. The one that is not in the founder's list and should be

A fan-out is billed. Five concurrent interactive sessions spent $515 of a $516.79 day
(measured 2026-08-21, `estate_spend.py --json`). Widening a fan-out is a spend decision, and
spend decisions are the founder's. The protocol needs a token/cost accounting rule per
fan-out, or it will optimise wall-clock into a bill nobody chose.
