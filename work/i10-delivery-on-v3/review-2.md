---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/review-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-review
status: withdrawn
wkind: capability
under: review
accepts: [review#r6, review#r7, review#r9, review#r11, review#r14]
blocked_by: [work-item/review-1]
risk: none
---

# review-2

## Observable
`bdd-branch-reviewer` reviews an initiative branch and `architecture-reviewer` gives refactors as observations; their
scenarios pass in every run.

## Unknown
none

## What changes
`agents/bdd-branch-reviewer.md` (Write added for its result and findings; no Edit) and `agents/architecture-reviewer.md`
rewritten in work-item terms: the initiative branch from its base, the work-items' checks, deprecated scenarios and
their replacements' items; a refactor as an observation with a check.

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r6, r7, r9, r11 | branch-review | an initiative branch with an unverifiable check, a dry-run pair, a deprecated scenario whose replacement is green, a removed scenario that was not deprecated, a dangling binding |
| r14 | architecture-review | a module past `CLAUDE.md`'s size limit |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`agents/bdd-branch-reviewer.md`, `agents/architecture-reviewer.md`, `tests/workflow/test_review.py`,
`tests/workflow/checks/review.py`, fixtures.

Withdrawn 2026-10-19: deferred until the skeleton runs (initiative notes)
