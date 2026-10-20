---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/review-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-review
status: done
wkind: capability
under: review
accepts: [review#r1-r5, review#r10, review#r12-r13]
blocked_by: [work-item/supervision-1]
risk: none
---

# review-1

## Observable
`bdd-task-reviewer` reviews one work-item's commits from a brief and writes graded, triaged findings to its result,
for `work run`'s review stage.

## Unknown
none

## What changes
`agents/bdd-task-reviewer.md` rewritten: the brief (the item, its plan, its commits), the findings and result files,
the triage; no Review:/Model: lines, no backlog, no lanes.

## Fixture cases
Each starts the reviewer on a done work-item with planted defects, with the fixture harness outside this repository
(formulation-1 is deferred).
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4, r5, r10, r12, r13 | task-review | commits that remove an unlisted test, contradict a line, edit a feature file, and report a setup-only change |

## Files, roughly
`agents/bdd-task-reviewer.md`, the fixture cases.

## Notes
r8 (the re-review of a fix work-item) left to review-2: the skeleton makes no fix work-items.
