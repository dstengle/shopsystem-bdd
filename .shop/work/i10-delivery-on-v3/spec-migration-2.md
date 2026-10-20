---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/spec-migration-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-spec-migration
status: withdrawn
wkind: capability
under: spec-migration
accepts: [spec-migration#r9-r14]
blocked_by: [work-item/spec-migration-1]
risk: none
---

# spec-migration-2

## Observable
Migration to ids runs as fixture sessions and passes in every run.

## Unknown
none

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r9, r10, r11, r13, r14 | migrate | keep-items with no ids, the old `decision/` and `obs/` forms, a held scenario, an outline |
| r12 | migrate-ambiguous | as migrate, one scenario formulating two lines |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_spec_migration.py`, `tests/workflow/checks/spec_migration.py`, `tests/workflow/fixtures/shelf.py`.

Withdrawn 2026-10-19: deferred until the skeleton runs (initiative notes)
