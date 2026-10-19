---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/review-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-review
status: drafted
wkind: capability
under: review
accepts: [review#r1-r5, review#r8, review#r10, review#r12, review#r13]
blocked_by: [work-item/formulation-1, work-item/supervision-5]
risk: none
---

# review-1

## Observable
`bdd-task-reviewer` reviews one work-item's commits from a brief and writes graded, triaged findings to its result;
its scenarios pass in every run.

## Unknown
none

## What changes
`agents/bdd-task-reviewer.md` rewritten: the brief (the item, its plan, its commits), the findings and result files,
the triage, the scoped re-review of a fix work-item; no Review:/Model: lines, no backlog, no lanes.

## Fixture cases
Each runs `work step <item>` on a done work-item with planted defects.
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4, r5, r10, r12, r13 | task-review | commits that remove an unlisted test, contradict a line, edit a feature file, and report a setup-only change |
| r8 | re-review | a fix work-item's commits leaving one hardening issue |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`agents/bdd-task-reviewer.md`, `tests/workflow/test_review.py`, `tests/workflow/checks/review.py`, fixtures.
