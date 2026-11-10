---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/decision-tiers
title: Decision tiers
narrator: a person or session keeping the decisions
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10, g11, r11, g12, r12]
unbuilt: []
---

# Decision tiers

## Purpose
Decisions return, in three tiers (design goal 7). A `check` decision names the test that enforces it, and the test
runs with the suite and at the pull request; a `requirement` decision names the requirement it is written as; a
`judgement` decision is read by the batch's plan and by the pull request's review. `model check` keeps each decision
to its tier, and keeps a superseded decision marked so.

## Terms
- **enforce** (verb, state): a design-decision names a test or a requirement under its `enforced_by` as what holds it. Forms: enforces, enforced. Frame: test enforces design-decision. Frame: requirement enforces design-decision.
- **outcome** (attribute of test): Values: `passed`, `failed`.
- **supersede** (verb, state): a design-decision names another under its `supersedes` as the one it takes the place of. Forms: supersedes, superseded. Frame: design-decision supersedes design-decision.
- **route** (noun): a way a design-decision is verified, named under its `verified_by`. Kind of: text.
- **kind** (attribute of route): the word that names the route. Values: `scenario`, `check`, `judgement`, `monitor`.
- **verify** (verb, state): a design-decision names a universal condition under its `rests_on` and a route under its `verified_by`. Forms: verifies, verified. Frame: design-decision verifies universal condition.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| route | of | design-decision |  |

## Behaviour

### [g13] A decision in force with no tier is a warning
- [r13] While a design-decision is not `superseded` or `rejected` and the design-decision has no tier, when the person runs `model check`, `model` shall print `w_untiered`.

### [g14] A `check` decision names its test
- [r14] While a design-decision is `check` and no test enforces the design-decision, if the person runs `model check`, then `model` shall exit with an error naming `v_d6`.

### [g15] A `requirement` decision names its requirement
- [r15] While a design-decision is `requirement` and no requirement enforces the design-decision, if the person runs `model check`, then `model` shall exit with an error naming `v_d7`.

### [g16] `model decisions --check` runs the tests of the `check` decisions
- [r16] While a design-decision is `check` and a test enforces the design-decision, when the person runs `model decisions --check`, `model` shall run `pytest` on the test.

### [g17] `model decisions --check` names each failing decision
- [r17] While a design-decision is `check` and a test whose outcome is `failed` enforces the design-decision, if the person runs `model decisions --check`, then `model` shall exit with an error naming the design-decision.

### [g18] An accepted decision supersedes no accepted decision
- [r18] While a design-decision whose status is `accepted` supersedes a design-decision whose status is `accepted`, if the person runs `model check`, then `model` shall exit with an error naming `v_d8`.

### [g19] `work decision` writes and commits a decision and the decisions index
- [r19] When the person runs `work decision`, `work` shall write a design-decision and the decisions index and commit the design-decision and the decisions index.

### [g20] `work decision` refuses a decision with no tier
- [r20] If the person runs `work decision` without the `--tier` option, then `work` shall refuse the command and name `--tier`.

### [g24] `work decision` refuses a decision with no summary
- [r24] If the person runs `work decision` without the `--summary` option, then `work` shall refuse the command and name `--summary`.

### [g25] `work decision` refuses a decision with no text
- [r25] If the person runs `work decision` without the `--decision` option, then `work` shall refuse the command and name `--decision`.

### [g21] `work decision` with `--verified-by` writes a route
- [r21] When the person runs `work decision` with the `--verified-by` option, `work` shall write a design-decision that has a route and commit the design-decision.

### [g22] `model check` names a universal condition no decision verifies
- [r22] When the person runs `model check`, `model` shall print every universal condition that no design-decision verifies.

### [g23] `model check` refuses a route outside the four
- [r23] While a route of a design-decision is not `scenario`, `check`, `judgement` or `monitor`, if the person runs `model check`, then `model` shall exit with an error naming the design-decision.

## Implementation, may change

- `w_untiered` is a warning; a decision gives its tier as `tier:` in its frontmatter.
- A design-decision verifies a universal condition (r22) only while it is in force (not `superseded` or `rejected`),
  and only with a route of the four (`model check`'s `w_unrouted`); a route outside the four is `v_d9` (r23).
- `work decision` refuses a run without `--summary`, `--decision` or `--tier` (r20, r24, r25) in one error naming each
  one missing.
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
- design-model-check r52 (`--check` on a decisions index exits successfully) and r17 here are both kept: r17 is an "If"
  line on r52's trigger (the person runs `model decisions` with `--check`), so it takes precedence by the rule of
  `spec/universal.md` ("An "If" line takes precedence", the person, 2026-11-04), as design-model-check r51 (a stale
  index) does (plan 6, D6; plan 6's rulings, Q1).

## Not yet
- None.
