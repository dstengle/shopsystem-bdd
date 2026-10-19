---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/red-green-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-red-green
status: drafted
wkind: capability
under: red-green
accepts: [red-green#r1, red-green#r2, red-green#r6, red-green#r8-r11, red-green#r15, red-green#r16, red-green#r18, red-green#r19]
blocked_by: [work-item/formulation-1, work-item/supervision-2]
risk: none
---

# red-green-1

## Observable
The implementer takes a ready work-item in its worktree, goes green one scenario at a time and reports through its
result file; its scenarios pass in every run.

## Unknown
How much of `bdd-red-green` and `bdd-implementer.md` remains once plans, steps, lanes and the plan's log go (the
assessment counted 29k tokens of starting context against a 900-token brief).

## What changes
`skills/bdd-red-green/SKILL.md` and its `example/` rewritten: the cycle with `--work-item`, the suite record from the
brief, HAND-BACK as a result, the report's sections, `work claim`, Retires with `features retire`; no slice tags,
`plan log`, Steps or lanes. `agents/bdd-implementer.md` rewritten to match (brief, result file, worktree,
continuation, fix work-item; the 15-file budget kept). Rationalization and red-flag tables are cut to what a stop
condition needs.

## Fixture cases
Each runs `work step <item>` on a ready work-item with a plan.
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r6, r8, r10, r11, r16, r18, r19 | implement | lend-items-1 ready, its plan (one silent case, one code block in it), a held scenario to retire |
| r9 | implement-big | a plan whose file set has 18 files |
| r15 | implement-no-context | a brief with no scripts directory |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`skills/bdd-red-green/SKILL.md`, `skills/bdd-red-green/example/`, `agents/bdd-implementer.md`,
`tests/workflow/test_red_green.py`, `tests/workflow/checks/red_green.py`, fixtures.
