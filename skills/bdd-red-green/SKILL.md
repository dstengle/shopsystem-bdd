---
name: bdd-red-green
description: Use when implementing any feature, bugfix, or plan slice in a project that has Gherkin feature files, before writing step definitions or production code. Also use when a scenario already passes, when a Then line looks wrong, when tempted to "fix a typo" in a .feature file, or when several scenarios could be made green in one pass.
---

# BDD Red-Green

## Overview

The `.feature` files are the contract. Code exists to satisfy them, one scenario at a time, and nothing else. This skill supersedes superpowers:test-driven-development wherever both apply: there is no unit-level red-green cycle, and unit tests are never written first.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Cycle

Work through the slice's scenarios in the order the plan lists them. The slice's scenarios carry a `@slice-<n>` tag, so `python -m pytest -q -m "slice-<n>"` runs the slice. For each scenario:

1. **Run that one scenario** (`python -m pytest -q -k "<scenario name>"`). It must fail for the right reason: an undefined step, or the Then assertion on the outcome. Any other result is a stop condition (below).
2. **Write only the step definitions this scenario needs.** Given and When steps drive the system's real entry point. Then steps assert exactly what the line says, nothing more.
3. **Write the least production code that turns this scenario green.** Hard-coded values are fine inside a slice.
4. **Run the whole feature suite.** Everything previously green stays green.
5. **Refactor** with the suite green, then commit, then the next scenario.

**Code only what a scenario asserts.** Where the scenarios are silent, the code is silent. Do not choose semantics for cases no scenario covers, not as a "guard", not as "the forgiving option". If the silence matters, it goes in the checkpoint entry as an open question.

## Slices Verified by a Check

An enabling or stack slice has a `Check:` line instead of scenarios: a command and the result it must give. The cycle is the same with the check in the scenario's place:

1. **Run the check.** It must fail, and for the reason the slice exists: the module isn't there, the stubs aren't generated, the bound isn't met. A check that passes before any work is a stop condition.
2. **Do the least work** that makes the check give its stated result.
3. **Run the check again**, then the whole feature suite. Everything previously green stays green.
4. Commit, then the checkpoint. The checkpoint's "someone can now" line says what the check proves.

No scenarios are written for a check slice, and no check is added to a capability slice.

## Feature Files Are Read-Only Here

This skill never edits a `.feature` file. Not to fix a typo, not to correct arithmetic, not to align wording. There is no step in the cycle that opens one for writing.

A scenario that is wrong is a **stop condition**, not a chore. Handling it is someone else's job: `slicing-into-increments` decides whether the contract changes, and only `formulating-features` writes features.

## Stop Conditions

Each of these is observable. When one occurs, hand back immediately:

| Observed | Meaning |
|---|---|
| A scenario passes before you wrote any step definition or code for it | The contract already covered it, or the scenario doesn't test what its tag claims. Slicing decides. |
| A slice's check passes before you did any work | The slice is already done or the check doesn't check what it says. Slicing decides. |
| A scenario can't be made to fail on its Then line, only on setup or an undefined Given | The Given describes a state the system can't represent yet. Slicing may need to re-order. |
| A Then line can only pass through code you'd be embarrassed to explain | The line is wrong or you've misread it. Either way, not yours to decide. |
| Going green needs work no scenario in the slice describes, beyond a trivial helper | Missing scenario or a mis-sized slice. |
| A previously green scenario breaks and the fix would change what a step means | Two scenarios contradict each other. |

A stop condition is triggered by a test-run result, never by reading. If a line looks wrong, run the cycle on it until a run shows the failure; the run output is the evidence.

**Hand back** means, in this order:
1. Append a `HAND-BACK` entry to the plan log (template below).
2. Commit everything scenario-driven that exists: green scenarios, the step definitions and code written for the red one, and the log entry. Commit message starts with `Hand-back slice <n>:`. The suite is red at this commit; that is expected.
3. Stop and report the trigger. Do not start the next scenario. Do not mark the slice done.

If the person asked for "green by the demo" and can't be reached, the answer is still a hand-back, because a green suite over an edited contract is worth less than a red one over the real contract.

Hand-back entry (all fields required):
```
- <date> HAND-BACK slice <n>, scenario "<name>": <which stop condition>.
  Evidence: <the failing assertion or observation, verbatim>.
  Green in this slice: <scenario names>. Red: <scenario names>.
```

## Checkpoint

When every scenario in the slice is green, set the slice's Status to `green`, append this entry to the plan log, and continue to the next slice without asking:
```
- <date> slice <n> green. Someone can now: <one sentence>.
  Surprised by: <what building it turned out to involve that the plan didn't say | nothing>.
  Open questions: <none | list>. Next: slice <n+1>.
```

## Rationalizations That Do Not Hold

| Excuse | Reality |
|---|---|
| "It's obviously a typo" | You don't know that. The same line reads as a typo to one person and a pricing rule to another. Hand back. |
| "The alternative is deliberately wrong arithmetic in production code" | No. The alternative is a red scenario and a hand-back entry. Those are the only two options. |
| "They said they couldn't answer questions" | Hand-back isn't a question. It's a report. The slicing skill handles it without them. |
| "I flagged the change in the commit message so it won't get lost" | A changed contract with a note is still a changed contract. The approval on that file is now void. |
| "It's a one-line revert if they disagree" | They approved the file. Reverting is their call to make in advance, not yours to make after. |
| "I'll write all the steps now and fill the code in after" | That's batching. You lose the red on every scenario after the first. One scenario, then the next. |
| "It already passes, that's one less to do" | A scenario passing without code is the first stop condition. It tells you the slice is mis-cut. |
| "The spec is silent, so I had to pick something" | You didn't. Leave the case unhandled and note it as an open question. |
| "A raise is safer than silent clamping" | Choosing between them is choosing a contract. Neither is yours to choose. |
| "The demo is in 20 minutes" | A demo of the wrong behaviour is the outcome you're paid to prevent. |
| "I can see from reading it that it can't pass" | Reading is not evidence. Run it. The failing assertion is what goes in the hand-back entry. |
| "Nothing is green, so there's nothing to commit" | The hand-back entry and the honest code are the commit. Uncommitted work is lost work in a hand-off. |

## Red Flags

- Any diff touching a `.feature` file
- `sed -i` or an editor on anything under `features/`
- Writing a second step definition before the first scenario is green
- The phrase "typo", "obviously meant", or "arithmetically impossible" about a Then line
- A `try`, `raise`, `max(0, ...)`, or default branch no scenario exercises
- "already passes" said with relief

**Any of these: stop, undo the edit, hand back.**

## pytest-bdd Notes

The example under `example/` shows the wiring: `scenarios("../features/x.feature")` binds every scenario, `parsers.parse` captures step arguments, and `target_fixture` on a Given publishes the object later steps use. Run one scenario with `-k` and the scenario name in snake case.
