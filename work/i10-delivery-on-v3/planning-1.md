---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/planning-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-planning
status: drafted
wkind: capability
under: planning
accepts: [planning#r1-r14]
blocked_by: [work-item/formulation-1, work-item/supervision-1]
risk: none
---

# planning-1

## Observable
`bdd-planner` plans a researched work-item from its notes; its scenarios pass in every run of `work step`.

## Unknown
Whether a planner limited to the notes and the file set writes the tests-the-decisions-break list as completely as
the planning session did with a scout re-run.

## What changes
New `agents/bdd-planner.md` (Read, Glob, Grep, Write; opus): the plan's sections, the question form with readings
and the plan under each, no code, the file set; the constraints of slicing's hand-off to writing-plans that still
hold, in work-item terms.

## Fixture cases
Each runs `work step <item>` on a researched work-item with prepared notes.
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4, r5, r6, r9, r13, r14 | plan | a researched lend-items item, notes with one `read` line and one broken test |
| r7, r8 | plan-question | notes where a broken test's fate is a contract decision |
| r10 | plan-defect | notes reporting a probe's defect, one on the item's path and one not |
| r11, r12 | plan-import | an import path that skips a stage, with a dry run beside it |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`agents/bdd-planner.md`, `tests/workflow/test_planning.py`, `tests/workflow/checks/planning.py`, fixtures.
