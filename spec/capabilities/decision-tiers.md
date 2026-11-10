---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/decision-tiers
title: Decision tiers
narrator: a person or session keeping the decisions
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r10, r11, r12]
---

# Decision tiers

## Purpose
Decisions return, in three tiers (design goal 7). A `check` decision names the test that enforces it, and the test
runs with the suite and at the pull request; a `requirement` decision names the requirement it is written as; a
`judgement` decision is read by the batch's plan and by the pull request's review. `model check` keeps each decision
to its tier, and keeps a superseded decision marked so.

## Terms
- **untiered** (adjective of design-decision): a design-decision that is not `superseded` or `rejected` and whose frontmatter gives no `tier`.
- **untested** (adjective of design-decision): A design-decision is untested when the design-decision is enforced by no test.
- **unrequired** (adjective of design-decision): A design-decision is unrequired when the design-decision is enforced by no requirement.

- **argument** (noun): an option a command is given on its command line, such as `--tier`.
- **absent** (adjective of argument): an argument that a command requires and that is not given.

- **unrouted** (adjective of universal condition): a universal condition that no design-decision's `verified_by` covers.
- **misrouted** (adjective of design-decision): a design-decision whose `verified_by` names a route other than `scenario`, `check`, `judgement` or `monitor`.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| design-decision | enforced by | requirement | |

## Behaviour

### [g1] A decision with no tier is a warning
- [r1] When the person runs `model check` on a design-decision that is untiered, `model` shall print `w_untiered`.

### [g2] A `check` decision names its test
- [r2] While a design-decision is `check` and the design-decision is untested, if the person runs `model check`, then
  `model` shall exit with an error naming `v_d6`.

### [g3] A `requirement` decision names its requirement
- [r3] While a design-decision is `requirement` and the design-decision is unrequired, if the person runs `model
  check`, then `model` shall exit with an error naming `v_d7`.

### [g4] `model decisions --check` runs the tests of the `check` decisions
- [r4] While a design-decision is `check` and the design-decision is enforced by a test, when the person runs `model
  decisions --check`, `model` shall use the test.

### [g5] `model decisions --check` names each failing decision
- [r5] While a design-decision is `check` and the design-decision is enforced by a test that is failing, if the person
  runs `model decisions --check`, then `model` shall exit with an error naming the design-decision.

### [g6] A superseded decision is `superseded`
- [r6] While a design-decision that is `accepted` supersedes a design-decision that is `accepted`, if the person runs `model check`, then
  `model` shall exit with an error naming `v_d8`.

### [g7] `work decision` writes and commits a decision
- [r7] When the person runs `work decision`, `work` shall write a design-decision, write the decisions index and commit the design-decision.

### [g8] `work decision` refuses a decision with no tier
- [r8] If the person runs `work decision` on a design-decision that is untiered, then `work` shall exit with an error naming `--tier` and change nothing.

### [g9] `work decision` names an absent argument
- [r9] If the person runs `work decision` on an argument that is absent, then `work` shall exit with an error naming the argument and change nothing.

### [g10] `work decision --verified-by` writes a route
- [r10] When the person runs `work decision --verified-by`, `work` shall write a design-decision and commit the design-decision.

### [g11] `model check` names a universal condition with no route
- [r11] When the person runs `model check` on a universal condition that is unrouted, `model` shall print the universal condition.

### [g12] `model check` refuses a route outside the four
- [r12] If the person runs `model check` on a design-decision that is misrouted, then `model` shall exit with an error naming the design-decision.

## Implementation, may change

- `w_untiered` is a warning; a decision gives its tier as `tier:` in its frontmatter.
- A decision gives its tier as `tier: check | requirement | judgement` and what enforces it as `enforced_by: [...]`:
  pytest node ids (`<path>.py` or `<path>.py::<name>`, relative to the root) for a `check` decision, requirement ids
  (an entry in the form `<capability>#r<n>` or `#r<a>-r<b>`, as `model why` reads them; any other entry, a
  parametrised test id holding `#` among them, is a test) for a `requirement` decision, and none for a `judgement` one. A tier
  outside the three, an entry of the wrong kind for its tier, `enforced_by` on a `judgement` decision and a test that is
  an option or whose file is not under the root are each a file problem; a requirement id that names nothing is an unresolved reference.
  History needs no tier: a `superseded` or `rejected` decision gives none, and `w_untiered` does not name it (plan 6,
  D2, D3).
- `model decisions --check` checks the index first and prints its line, then runs the tests of each `check` decision
  in force (not `superseded` or `rejected`), in file order and up to 4 at a time: one `<python> -B -m pytest -q -p
  no:cacheprovider -o addopts= <entries>` a decision, in the repository, with `PYTHONDONTWRITEBYTECODE=1` and a 600 s
  timeout, so a named test runs alone whatever the repository's own `addopts` deselect. `<python>` is the project's
  interpreter, found as `tools` finds it (`.venv/bin/python`, `venv/bin/python`, `$VIRTUAL_ENV`, else the one running
  `model`). It writes nothing of its own there (no `.pytest_cache`, no bytecode); what a decision's tests write is the
  tests'. It prints `holds    <path> (<id>): <entries>` or `failing  <path> (<id>): <entries>: <why>` with the last 20
  lines of pytest's output, then `<n> check decisions: <h> hold, <f> failing`. `<why>` is `exit <code>` for a pytest
  exit other than 0 (4: a test not found, 5: nothing collected), `timed out after <n> s`, `not run: <n> skipped` (or
  `xfailed`, `xpassed`, `deselected`) or `nothing passed` for an exit of 0 whose summary line shows a test that did not
  run, `not a test of this repository: <entry>` for an option or a file outside the root, which is never run, or
  `names no test`. It exits 1 when the index is stale or any decision fails (plan 6, D5; plan 6's review, S1-S3, M2).
- design-model-check r52 (`--check` on a decisions index exits successfully) and r5 here are both kept: r5 is an "If"
  line on r52's trigger (the person runs `model decisions` with `--check`), so it takes precedence by the rule of
  `spec/universal.md` ("An "If" line takes precedence", the person, 2026-11-04), as design-model-check r51 (a stale
  index) does (plan 6, D6; plan 6's rulings, Q1).

## Not yet
- None.
