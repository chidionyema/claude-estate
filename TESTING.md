# How to test

Founder ruling, 2026-08-22. Binding in every repo. Referenced by LAW 6 in `~/AGENTS.md`,
which is where this lived until the laws were cut to 10 on 2026-08-23.

Most of a suite is implementation tests of orchestration that a redesign deletes anyway. The
invariant tests cost nothing to keep. Write only the rungs that survive a rewrite.

Always use the cheapest rung that can express the guarantee. Descend only when the rung above
genuinely cannot.

1. **Types — zero tests.** Every invariant that can be a type is a test you never write, run or
   maintain. Sealed enums, newtypes for units, a `Result` the caller must handle, a value that
   cannot be constructed without its evidence, config structs that lack the forbidden fields.
   Python: `pyright --strict`, frozen dataclasses, `NewType`, `Literal`, exhaustive `match`.
2. **Property tests — one test, thousands of cases.** A property describes behaviour, not
   structure, so it survives a refactor and ports across languages (`hypothesis` → `proptest` is
   near-mechanical). Seven properties beat several hundred example tests.
3. **Differential replay — the users already wrote these.** For any rewrite, the oracle is the
   current implementation. Run both over the recorded corpus and diff. One assertion, thousands of
   cases. A differential test is a migration tool, not a permanent test: delete it when the old
   implementation goes.
4. **Incident tests — one per bug, named for the bug.** `test_incident_0042_pool_saturation`.
   Written once, when it bites, asserting the rule and not the code. The only category where
   writing a test by hand is unambiguously worth an agent's time.
5. **Evals with deterministic graders.** For probabilistic output, prefer a mechanical grader over
   a model's opinion wherever the domain supplies one: substring containment, HTTP status, walking
   the IR, ordering in a table, ledger arithmetic, a diff against a golden set.
6. **LLM-as-judge — last resort, never gating.** Only for genuinely subjective quality. The judge
   is non-deterministic, so it produces flaky tests that cost money per run, and it drifts when the
   model updates. Sampled, reported, never blocking. Pin the model and version.
7. **Production oracles.** Deploy-and-verify with automatic rollback, health checks, canaries,
   alerts. The last line, and the cheapest, because it is already built.

**Before writing any test, ask in order.** Can this be a type? Make it unrepresentable instead. Can
this be a property? Write one property, not ten examples. Is this a rewrite? Write a differential
case against the old path. Is this a real bug that occurred? Write one incident test, named for it.
If none apply, the test is probably not worth writing — say so in the PR and move on.

**What you delete.** Example-based unit tests of orchestration and implementation detail. Any test
whose name describes a function rather than a rule. Mocks of your own internals — they test the
mock. Anything self-healing: a test that rewrites itself to match new code always agrees, which
removes the oracle. With agents writing the code as well, that is a closed loop with no external
check.

**Enforcement.** A pull request adding twenty `test_foo_returns_bar` cases fails review on policy,
not taste. Say which rung each new test is, in the PR body.

