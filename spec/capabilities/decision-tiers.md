---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/decision-tiers
title: Decision tiers
narrator: a person or session keeping the decisions
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10, g11, r11, g12, r12, g14, r14, g15, r15, g16, r16, g17, r17, g23, r23, g13, r13, g26, r26, g27, r27, g28, r28, g29, r29, g18, r18, g19, r19, g20, r20, g24, r24, g25, r25, g21, r21, g22, r22, g30, r30, g31, r31, g32, r32]
unbuilt: []
---

# Decision tiers

## Purpose
Decisions return, in three tiers (design goal 7). A `check` decision names the test that enforces it, and the test
runs with the suite and at the pull request; a `requirement` decision names the requirement it is written as; a
`judgement` decision is read by the batch's plan and by the pull request's review. `model check` keeps each decision
to its tier, and keeps a superseded decision marked so.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

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
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g13 | decisions#g1 |
| r13 | decisions#r1 |
| g26 | decisions#g2 |
| r26 | decisions#r2 |
| g27 | decisions#g3 |
| r27 | decisions#r3 |
| g28 | decisions#g4 |
| r28 | decisions#r4 |
| g29 | decisions#g5 |
| r29 | decisions#r5 |
| g18 | decisions#g6 |
| r18 | decisions#r6 |
| g19 | decisions#g7 |
| r19 | decisions#r7 |
| g20 | decisions#g8 |
| r20 | decisions#r8 |
| g24 | decisions#g9 |
| r24 | decisions#r9 |
| g25 | decisions#g10 |
| r25 | decisions#r10 |
| g21 | decisions#g11 |
| r21 | decisions#r11 |
| g22 | decisions#g12 |
| r22 | decisions#r12 |
| g30 | decisions#g13 |
| r30 | decisions#r13 |
| g31 | decisions#g14 |
| r31 | decisions#r14 |
| g32 | decisions#g15 |
| r32 | decisions#r15 |
