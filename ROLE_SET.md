# The role set — one person per hat, and what each may decide without the founder

Founder, 2026-08-21: *"as fiuder i wear too nany hats, i need persons that cover all aspects of a
startup that can nake decisions autononously, strong oownership culture, roles clearly defined
enginerring to narketing to ux, etc"*, *"operations etc"*, *"sales ,finnace"*, *"legal"*,
*"all roles even ceo"*, *"ultra ultra specialised personas"*, *"always researching updating
knowledhe  being certain"*, *"not guess work"*.

**The measure of this set is hats removed, not files written.** A role earns its place when a
decision that used to reach the founder stops reaching him and still gets made correctly.

## Where they live and how they are graded

`~/.claude/agents/roles/*.md`. Claude Code scans `~/.claude/agents/` **recursively**
(code.claude.com/docs/en/sub-agents, checked 2026-08-21), so the subfolder is organisation only —
identity comes from the `name` field. That also means **any non-role file in that folder gets
loaded as a subagent**, which is why this document lives one level up. The guard caught exactly
that on the first run.

```
python3 ~/.claude/scripts/role-guard.py            # grade every role
python3 ~/.claude/scripts/role-guard.py --selftest # 15 checks
```

## Why these roles look nothing like a persona prompt

Three measurements, all recorded in `~/.claude/DECISIONS.jsonl` under decision `d9861f649fe4`:

1. **A persona label buys no accuracy.** *When "A Helpful Assistant" Is Not Really Helpful*
   (Findings of EMNLP 2024) tested 4 model families on 2,410 factual questions with 162 curated
   roles: adding a persona did not improve accuracy, and picking the best role per question beat
   random by nothing. Second angle, different authors and task (JMIR / PMC11467603): adding social
   identities dropped misinformation-detection accuracy from 68.1% to 29.3%.
2. **What a role actually needs** is Anthropic's own list: *"an objective, an output format,
   guidance on the tools and sources to use, and clear task boundaries."* Backstory is not on it.
3. **Role fidelity is not where agents fail.** MAST (arXiv 2503.13657, 150 annotated traces,
   kappa 0.88) puts "disobey role specification" at 1.5% of failures against 44.2% for system
   design and 32.3% for inter-agent misalignment. A framework that sells role fidelity fixes the
   smallest problem at roughly 15x the token cost.

So every file is: OBJECTIVE, DECIDES ALONE, ESCALATES, LOGS, SOURCES, OUTPUT, BOUNDARIES,
DONE WHEN. The character sketch is the one thing measured not to work, and the guard refuses it.

## The nine

| Role | Owns | Model | The escalation that defines it |
| --- | --- | --- | --- |
| `ceo` | what gets attention and what is dropped | opus | pivoting what the company sells |
| `engineering` | how it is built, tested, shipped | sonnet | a copyleft dependency; an irreversible migration |
| `ux` | what the person on the screen experiences | sonnet | collecting personal data; breaking a held link |
| `marketing` | how a stranger finds out and why they care | sonnet | any paid spend; a comparative claim |
| `sales` | interest to paid transaction | sonnet | a discount, a bespoke promise, a signature |
| `operations` | whether it is running right now | sonnet | a new paid resource; destroying unreplicated state |
| `finance` | what it costs and what it earns | opus | **every payment, in any amount** |
| `legal` | where the company is exposed | opus | **everything — this role never rules** |
| `inventor` | the hardest problems, and the option nobody else generated | opus | shipping an option nobody has costed |

## The two hard bounds, and where they come from

**Legal never gives advice.** Providing legal advice without a qualified lawyer is unauthorised
practice of law in over thirty US states and restricted in most jurisdictions this company would
sell into (NCSC UPL white paper; ABA Model Rule 5.5; WSBA advisory opinion 2025-05, recorded under
research `rb7bd31709f7`). The role drafts, quotes primary text, flags exposure and writes the
question for a lawyer. Every output carries a visible line saying it is unreviewed.

**Finance never pays.** It prepares the decision with the arithmetic shown. Money leaving the
account is the founder's, in any amount, with no exception — LAW 11, and the founder's own
standing rule.

## Certainty without asking the model how sure it is

The founder asked for roles that are *"always researching updating knowledhe  being certain"* and
*"not guess work"*. The mechanism is **not** telling the model to be sure of itself: verbalised
confidence is systematically overconfident and saturates near 0.9 (arXiv 2306.13063), so a role
that rates its own certainty produces a number that means nothing. The guard refuses that phrasing.

Certainty comes from the evidence rule instead — **two sources from two different publishers, or
the claim is marked unverified** — enforced where it can be checked, in `decision-log.py`. Two
readings from one publisher are one angle wearing two coats.

## What is deliberately not here yet

The founder wrote *"etc"* twice, which means derive rather than guess. These are the candidates,
not built, because a role with no decisions to make is another file to maintain:

- **data protection** — currently inside `legal` and `ux`. Splits out when the product holds
  personal data it does not hold today.
- **support** — currently inside `sales`. Splits out at the first paying customer.
- **product** — currently split between `ceo` (what) and `ux` (how). Splits out when more than one
  person is proposing features.
- **security** — currently inside `engineering` and `operations`. Splits out when the estate holds
  a credential a customer would care about losing.

Each of those is a two-way door: add the file, run the guard, and the overlap check will say
whether the decisions it claims were already owned.

## The model

`~/.claude/scripts/role-model.py` computes the role set rather than describing it. Structure is
measured from the nine files; the economics needs three numbers this estate has not measured, so
they are supplied on the command line and never invented.

Measured 2026-08-21 on the live set: 9 roles, 45 decisions owned, 35 escalated, **coverage 0.562**,
**0 overlapping decisions**, 36 pairwise interfaces.

The one result worth reading. Delegating a decision beats escalating it when

    q > 1 - A/(V + L)

for role correctness `q`, decision value `V`, loss from a wrong autonomous call `L`, and the cost
of the founder's attention `A`. As `L` grows the threshold rises past any achievable competence, so
an irreversible decision can never be delegated at any competence and any founder cost. **LAW 11 is
not a policy sitting on top of this system — it is what the arithmetic produces**, and it is why
`finance` and `legal` escalate more than the other seven rather than because they sound risky.

Two more consequences: the threshold FALLS as the founder's attention gets more expensive (the
busier the founder, the more should be delegated — his own complaint, as arithmetic), and it does
not contain a term for how impressive the role sounds, which agrees with the measurement that a
persona label buys no accuracy.

Coordination cost is quadratic — n roles have n(n-1)/2 interfaces, and 32.3% of multi-agent
failures sit on inter-agent misalignment — so net value has an interior maximum and more roles is
not monotonically better. That is why four roles are named below as deliberately not built.

    python3 ~/.claude/scripts/role-model.py                 # measure the live set
    python3 ~/.claude/scripts/role-model.py --delegate --value 200 --loss 400 --attention 150
    python3 ~/.claude/scripts/role-model.py --selftest      # 18 checks, mutation-proved

## Grading what a role PRODUCES, not just what it declares

`role-guard.py` grades the role FILES. It cannot see whether an answer met the contract, and the
first live `inventor` run showed why that gap matters: the role loaded, produced the right shape,
named three distant fields — and still failed two of its own four DONE WHEN conditions. It killed
no option, and it marked one option "Proven. Standard in mature suites." with no source. Nothing
noticed, because nothing was grading.

`~/.claude/scripts/inventor-grade.py` grades an answer against those conditions. 19/19 selftest,
mutation-proved. Its own test corpus is the real failing run, so the checks are pinned to a
failure that actually happened rather than to one I imagined.

    claude --agent inventor -p "<problem>" | python3 ~/.claude/scripts/inventor-grade.py

The role file was then changed rather than the grader: it now asks for at least five options with
the killed ones shown. Three generated and three kept is a set whose killer tests were never
applied; five generated and two killed makes the kill honest instead of forced. That also matches
the measured fix for mode collapse — ask for a spread and prune it, rather than asking for one
answer.
