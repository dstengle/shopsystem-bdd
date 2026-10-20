---
name: bdd-red-green
description: Use when implementing a ready work-item in a project that has Gherkin feature files, before writing step definitions or production code; loaded by the bdd-implementer that work run starts in the work-item's worktree. Also use when a scenario already passes, when a Then line looks wrong, when tempted to "fix a typo" in a .feature file, or when several scenarios could be made green in one pass.
---

# BDD Red-Green

## Overview

The `.feature` files are the contract. Code exists to satisfy them, one scenario at a time, and nothing else. There is no unit-level red-green cycle, and unit tests are never written first.

You implement one work-item: the scenarios of the requirements it `accepts:` (the scenarios in `features/` whose tag lines carry those ids, `@r<n>`), or, for a work-item with a `check:` and no accepted requirements, its check. `work run` started you in the work-item's worktree, on its branch, with one brief; it reads your result file, rebases your branch, runs the tests itself and merges only if they pass. You never move the work-item.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Plan Is Intent, Not Code

The work-item's plan (`plan.md` in its plan run directory) says which scenarios go green, why they are red today, where the change lands (its file set), the decisions taken and the tests they break; it does not contain the code. You write the code, after the red run, from what the scenario asks. If the plan does contain code, do not paste it: run the scenario red first, write your own, and say in the report that the plan contained code and was not pasted. The work-item's `## Rulings`, if any, are decisions too.

## The Cycle

Work through the work-item's scenarios in the order the plan lists them. Where `python3 -m pytest --help` lists `--work-item`, `python3 -m pytest -q --work-item <name>` runs the work-item's scenarios; otherwise run them by title. For each scenario:

1. **Run that one scenario** by its test's node id (`python3 -m pytest -q "<node id>"`; `python3 -m pytest -q --collect-only` lists them). `-k` takes a name or an expression, not a title: a title with spaces is refused as a wrong expression. It must fail for the right reason: an undefined step, or the Then assertion on the outcome. Any other result is a stop condition (below).
2. **Write only the step definitions this scenario needs.** Given and When steps drive the system's real entry point. Then steps assert exactly what the line says, nothing more.
3. **Write the least production code that turns this scenario green.** Hard-coded values are fine inside a work-item.
4. **Run the work-item's scenarios** and the test module the scenario lives in. Everything previously green there stays green.
5. **Refactor** with them green, then commit, then the next scenario.

Before the last commit, run the whole suite once (`python3 -m pytest -q`, or the project's test command). Everything that passed in the starting record still passes. That run is the work-item's suite record, in the report.

**An invariant's test is a test like any other.** A property test that fails, on whatever example it found, is a previously green test that broke: the falsifying example it prints is the evidence.

**Code only what a scenario asserts.** Where the scenarios are silent, the code is silent. Do not choose semantics for cases no scenario covers, not as a "guard", not as "the forgiving option". Each such case goes in the report under `## Open questions`, with its behaviour left unchosen by the code.

## A Work-Item Verified by a Check

A work-item with a `check:` (a command and the result it must give) and no scenarios goes through the same cycle with the check in the scenario's place: run the check, which must fail for the reason the work-item exists (a check that passes before any work is a stop condition); do the least work that makes it give its stated result; run it again with the test modules the work touches; then the whole suite once, which is the record. No scenarios are written for it.

## The Suite Record

A suite record is one whole-suite run: `Suite: <N> passed, <M> failed at <short hash of the commit that was run> in <seconds> s`, with `; failing: <titles>` when M is not 0.

- You start from the record your brief gives. Where the brief gives none, run the whole suite once before your first edit: that run, at the commit you started from, is your starting record, and its failing list is what was already red.
- Do not run the whole suite at any other point but before your last commit.
- Both records go in the report. You write no log, no plan entry and no status anywhere: `work run` keeps its own record.

## Keep the Suite Fast

- Tests run in parallel (`pytest-xdist`, `-n auto` in the project's test command). Each test works in a directory of its own, so nothing they share needs a lock.
- The system's real entry point is driven in-process wherever the project allows: a command line is called through its `main` with its arguments and environment. One test per command runs it as a program.
- A test that waits does so for a signal, never for a fixed time.

A project whose suite cannot do one of these says why in its `CLAUDE.md`.

## Files You Do Not Commit

This skill never edits a `.feature` file. Not to fix a typo, not to correct arithmetic, not to align wording.

One command removes a scenario, and only one kind: `python3 <scripts>/features retire "<title> (deprecated)"` takes out a scenario tagged `@deprecated`. You run it for each scenario the work-item lists under Retires, in the commit that turns its replacement green, and remove with it its binding and the step definitions nothing else uses. It refuses any other scenario, and so do you.

Nothing under `.shop/work/` is yours to commit either: not the work-item, not its runs, not `log.jsonl`. Your report and your result go where the brief names, by the paths it gives, and are never added to a commit.

A scenario that is wrong is a **stop condition**, not a chore. Whether the contract changes is the person's ruling, and only `formulating-features` writes features.

## Existing Tests

A test that passed before your change and fails after it is information about the change. You may change what such a test asserts only when the plan lists it under "Tests the decisions break", and then only as the plan says. Two changes are allowed to a test the plan does not list, each named in the report under `## Tests changed under an allowance` (the test's file and name, `setup` or `interim`, what changed):

- **Its setup.** The lines that arrange the test. No `assert`, no expected value and no parametrize case is added, removed or changed.
- **A test this initiative wrote.** A test first committed after the initiative's base, the commit the brief names as `Base:`, rewritten to what a decision of the plan says. Where the brief names no base, no test counts as this initiative's.

Any other removal, loosening, skip, xfail or rewrite of an existing test is a stop: `BLOCKED` (below). Respelling a test (a renamed helper, an id written through a new function) is yours: a respelled test still passes against the code as it was.

## Stop Conditions

Each of these is observable. When one occurs, stop at once with the status its row gives:

| Observed | Status |
|---|---|
| A scenario the work-item accepts passes before you wrote any step definition or code for it | HAND-BACK |
| A scenario can't be made to fail on its Then line, only on setup or an undefined Given | HAND-BACK |
| The work-item's check passes before you did any work | HAND-BACK |
| A scenario of a work-item not yet claimed passes | HAND-BACK |
| A Then line can only pass through code that contradicts it | HAND-BACK |
| Going green needs work no scenario of the work-item describes and its plan does not name, beyond a trivial helper | HAND-BACK |
| An existing test could stay green only by being removed, loosened, skipped or rewritten to assert something else, and the plan does not list it and no allowance covers it | BLOCKED, naming the test and its failing assertion |
| A previously green scenario breaks and fixing it would change what a step means | BLOCKED, naming the step |
| The work needs a decision the plan, its rulings and the capability's Behaviour leave open | BLOCKED, naming the decision |
| A file would cross the repository's size limit and no rule in `CLAUDE.md` says where the code goes | BLOCKED, naming the file |

Where a rule in `CLAUDE.md` does say where the code goes (a new concern gets a new module and a row in the module map), make the split, add the row, and say so in the report.

A stop condition is triggered by a test-run result, never by reading. If a line looks wrong, run the cycle on it until a run shows the failure; the run output is the evidence.

**Stopping** means, in this order:
1. Commit everything that exists on the work-item's branch: green scenarios, and the step definitions and code written for the red one. The suite may be red at this commit; that is expected.
2. Write the report: the stop condition, its evidence verbatim (the failing assertion or observation), the scenarios green and the scenarios red.
3. Write the result with the status, the evidence in `questions`, and stop. Do not start the next scenario.

If the person asked for "green by the demo" and can't be reached, the answer is still a hand-back, because a green suite over an edited contract is worth less than a red one over the real contract.

## The 15-File Budget

One implementer touches at most 15 files. Before your first edit, write in the report, under `## Budget`, the files you will touch, by name. When the work needs more than 15, choose at most 15 whose change leaves everything passing that passes now, touch only those, commit at green (a whole-suite run shows nothing failing that passed in the starting record), say in the report what is done and what is left file by file, and give `PARTIAL`. The limit is not lifted by the plan naming more, nor by the work looking quick. `PARTIAL` is not for decisions: those are `BLOCKED`.

## When Done

When every scenario (or the check) is green and the whole-suite run fails nothing the starting record passed, the report says what someone can now do, what building it turned out to involve that the plan did not say, and the open questions; the result gives `DONE` and the commits.

## Rationalizations That Fail

| Excuse | Reality |
|---|---|
| "It's obviously a typo" | You don't know that. The same line reads as a typo to one person and a pricing rule to another. Hand back. |
| "The alternative is deliberately wrong arithmetic in production code" | No. The alternative is a red scenario and a hand-back. Those are the only two options. |
| "Nobody can answer questions now" | A hand-back isn't a question to you. It's a result; `work run` takes it to the person. |
| "I flagged the change in the commit message so it won't get lost" | A changed contract with a note is still a changed contract. The approval on that file is now void. |
| "I'll write all the steps now and fill the code in after" | That's batching. You lose the red on every scenario after the first. One scenario, then the next. |
| "It already passes, that's one less to do" | A scenario passing without code is a stop condition. It tells you the work-item is mis-cut. |
| "The capability's Behaviour is silent, so I had to pick something" | You didn't. Leave the case unhandled and name it as an open question. |
| "A raise is safer than silent clamping" | Choosing between them is choosing a contract. Neither is yours to choose. |
| "I can see from reading it that it can't pass" | Reading is not evidence. Run it. The failing assertion is what goes in the report. |
| "Nothing is green, so there's nothing to commit" | The honest code is the commit. Uncommitted work is lost with the worktree. |
| "The decisions make that test impossible, so I removed it and said so in the concerns" | A removed test with a note is still a removed test, and the behaviour it tested is gone unseen. Stop `BLOCKED` with the test named. |
| "Only the setup changed, and the expected value had to follow" | Then more than the setup changed. An expected value is what the test proves. Stop with the test named. |
| "The plan's code is right there" | Pasted code turns red into a performance. Write your own after the red run. |

## Red Flags

- Any diff touching a `.feature` file, other than `features retire` of a scenario the work-item lists under Retires
- `sed -i` or an editor on anything under `features/`, or a commit touching `.shop/work/`
- Writing a second step definition before the first scenario is green
- The phrase "typo", "obviously meant", or "arithmetically impossible" about a Then line
- A `try`, `raise`, `max(0, ...)`, or default branch no scenario exercises
- "already passes" said with relief
- A deleted test function or parametrize case, a loosened assertion, a new skip or xfail, or a test rewritten to assert something else, on a test the plan does not list
- A `git push`, `merge`, `rebase` or `reset`, or a `checkout` of another branch

**Any of these: stop, undo the edit, and stop as the table says.**

## pytest-bdd Notes

`scenarios("../features/x.feature")` binds every scenario of a file, `parsers.parse` captures step arguments, and `target_fixture` on a Given publishes the object later steps use. Run one scenario with `-k` and words of its title.
