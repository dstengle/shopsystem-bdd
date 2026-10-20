---
id: decision-argument/missingmass.io/shopsystem/shopsystem-bdd/2026-10-11-analysis-tools-design
kind: decision-argument
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-11
---

# Analysis Tools Design

Date: 2026-10-11
Status: Written while the person was away, at their instruction; not read by them. Unreleased, on branch
`0.15.0-analysis-tools`, stacked on 0.14.0.
Release: 0.15.0
Request: `docs/superpowers/requests/2026-10-11-predictable-batches-and-analysis-tools.md`, sections A, B and D, and
the fourth point of C
Baseline: `docs/superpowers/testing/2026-10-11-kb-baseline/`

## Purpose

Three things the workflow could not see become things a tool or a planned step sees: what else in the code a
decision changes; which tests execute a piece of code and which code none does; and the properties a reviewer
re-derives by hand each batch.

## Evidence

- Four tasks were added to batch 33 after its plan was written, each from a review that found a place still
  assuming the old thing. The branch reviewer found the whole class in one table: every place that still reads an
  artifact through its type's latest version.
- All four hand-backs of batches 33 to 35 were existing tests no task had listed. A scout searching for them names
  the tests that spell what changes; a test that reaches it through a helper or another module is not found by
  its name.
- `Lands:` was under the files touched in 15 of 23 slices (the baseline's facts).
- Reviewers found defects with probes they wrote and then deleted: a store exported, imported and read back; two
  changes released in each order; a set that changes a type twice.

### Measured on kb before this was written down

In a scratch clone of kb with its own virtualenv, at the commit before slice 163's hand-back (`149af5c`):

- **The map costs three suite runs.** 74 s against the suite's 24 s, 874 tests.
- **For code on every call's path the map narrows nothing.** The hand-back's commit changed 11 functions. `tests-of`
  gives 577 or 578 tests for four of them, 153 to 176 for four, and 16 to 29 for three. The lines it changed are
  executed by 577 tests in all. kb's tests drive the contract, so the entry path is everyone's.
- **For code off that path it narrows well.** `edits.py:_append` is executed by 29 tests, 18 of them in
  `tests/test_add_an_item_to_a_collection.py`, where five of the six tests that the commit broke are.
- **References are exact where a search is not.** `tools refs kb.changes.replacing` gives one reference,
  `servicer.py:81`. A search for the word gives 17 lines in 9 files: a test helper of the same name and prose. For
  three other names the two agree. A package under `src/` installed for development is invisible to jedi until
  `src` is given as a path, which `refs` now does.

So the request's row "coverage with per-test contexts replaces the scout's search for tests the decisions break"
holds for a change off the main path and not for one on it. The scout is told to say which it met.

## Changes
## Changes

### 1. `scripts/tools`: probe, install, report, and one interface to use them

New `scripts/tools`, `tests/scripts/test_tools.py`.

| command | does |
|---|---|
| `tools probe` | one line a tool in the project's own interpreter, present with its version or missing with what it is for; `--log` gives the one line for `plan log` |
| `tools install` | `pip install` of each missing tool into the project's virtualenv, and nothing else; for each still missing: the tool, what it is for, what the workflow does without it, the command and its error |
| `tools map` | the suite once under coverage with a context per test, kept under `.superpowers/tools/` |
| `tools tests-of <file>:<function>` | the tests that executed it in the map |
| `tools untested <file>...` | the functions no test executed |
| `tools refs <dotted name>` | every reference, through imports and aliases, with production and test file counts |
| `tools check [--base <commit>]` | ruff, vulture and import-linter over what changed, each under a heading; a missing tool named under its heading |

- **The tools, for Python:** coverage and pytest-cov (the map), jedi (references), ast-grep (search by shape), ruff,
  vulture, import-linter, hypothesis. A project in another language is told in one line that none are known, and
  agents search by text and say so.
- **Nothing is written to a project's dependency files.** `install` refuses an interpreter that is not a
  virtualenv. Whether a project records the tools as development dependencies is an enabling slice of its own.
- **Never silent.** Slicing probes first, installs, and tells the person in `install`'s words about anything still
  missing before any other step, then logs `Probe: tools -> …` in the plan.
- **Degrade openly.** The scout's notes say of every count and list how it was made: `refs`, `tests-of` or `by
  search`.
- **Not in the fast suite.** The map is its own run. `tests-of` and `untested` say the commit their map was made
  at.

The request listed nine tools. jedi is taken over pyright, which needs Node. mutmut and pytest-testmon are under
Not yet.

### 2. The scout uses them, and sweeps a decision's consequences

`agents/code-scout.md`.

- Tools before search, wherever the thing asked about is a name.
- **Task research:** "Tests the decisions break" begins from `tests-of` for each function or branch the decisions
  change. A few dozen tests are candidates to read. Most of the suite means the code is on every call's path and
  the map narrows nothing (below): the scout says so and searches by what the tests assert. "Where the change lands" says of each function it rewrites whether a
  test executes it.
- **Consequence sweep**, a third dispatch. Given one decision as an old assumption and what replaces it: every
  place in the code and tests that still embodies the old assumption, from the references of the functions that
  read or write the old form outward, with the tests that execute each. One table: place, what it does today, what
  the decision makes of it, the tests that execute it, how it was found. It names no slice.

### 3. Slicing owns the sweep

`skills/slicing-into-increments`.

- Step 0: probe, install, tell, log, map.
- In step 2, before slices are final: a sweep for each decision the batch applies that replaces something existing
  code assumes. Every row gets an owner: a slice, a `QUESTION FOR THE SPEC:`, or a deferral logged with its price
  and a reproduction. The planner assigns owners alone. A deferral that changes what a client can observe is a
  question for the person, as any contract decision already is.
- The request asked whether the person reviews the table at the gate. No: the gate stays the one on Behaviour
  lines. The table's questions and client-visible deferrals reach the person by the route they already have.

### 4. A guard names its test

The hand-off. A task may say that a test going red is a stop, about behaviour it must not change, only by naming
the passing test that executes it. Where none does, the task first writes that test, green on today's behaviour.
(Section C's fourth point, held from 0.14.0 for the map.)

### 5. Invariants, and probes that are kept

`skills/slicing-into-increments`, both reviewers, `skills/bdd-red-green`, `agents/bdd-implementer.md`.

- A project states its invariants in `CLAUDE.md` under `## Invariants`, each with the test that holds it. Where a
  line names no test, the release's first enabling slice writes them as property tests that run in the suite.
- A property test's failure is a red like any other.
- A reviewer's probe that finds a defect goes in the finding as `Keep as a test:`, and the fix round adds it to the
  suite and sees it red first. A probe that checks what should hold after any change is given under `Invariant
  proposed:`; whether it becomes a line of `CLAUDE.md` is the person's.
- Reviewers run `tools check` and read its output in place of reading for lint, dead code and import rules.

## Not yet

- **mutmut**, mutation on a slice's changed lines. It answers "went green on step definitions alone", which the
  scout's `steps only` line (0.13.0) and strict expected failures (0.14.0) now meet from two sides. Promoted if a
  review still finds an assertion that asserts nothing.
- **pytest-testmon.** It saves running the whole suite to compare two lists; 0.14.0 removes the comparison, and
  kb's suite runs in 25 s.
- **pyright.**
- **Languages other than Python.**
- **The implementer checking the map before it changes code.** The map is made at planning, and is stale by the
  second slice. Promoted if a cheap way to refresh it for one module is found.
- **The person reviewing the sweep's table.**

## What should move

On a batch of kb run on this version: tasks run less tasks planned, toward 0 (4 in batch 33); hand-backs for an
unlisted test, toward 0; `Lands:` at or above files touched in more slices (8 of 23); findings by the branch
review that a sweep row or an invariant would have held, in `analyzing-a-batch`'s findings table.

## Verification

- **The script:** unit tests against a real coverage and jedi where they are installed: a line a tool; the plan's
  line; a project in no known language; `install` refusing a system interpreter; the map and `tests-of` for a
  function reached directly, through an alias and in a class; `untested`; `refs` through an import and an alias;
  `check`'s headings.
- **Against kb's own hand-backs**, in a scratch clone with its own virtualenv: at the commit before each hand-back,
  whether `tests-of` for the functions that commit changed lists the tests the scout had missed, and how many
  tests it lists in all.
- **The scout**, headless on a fixture where two tests reach the changed function through a helper and through
  another module.
