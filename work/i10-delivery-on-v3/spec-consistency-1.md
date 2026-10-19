---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-spec-consistency
status: drafted
wkind: capability
under: spec-consistency
accepts: [spec-consistency#r1-r11]
blocked_by: [work-item/formulation-1]
risk: none
---

# spec-consistency-1

## Observable
The consistency check's scenarios run as fixture sessions and pass in every run.

## Unknown
none

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4 | consistency-report | the lending lines formulated, a glossary, three planted problems |
| r5, r6, r7, r8, r9, r10 | consistency-fix | as consistency-report; the prompt gives the answers |
| r11 | formulate, apply | their transcripts: no `spec-checker` is dispatched |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_spec_consistency.py`, `tests/workflow/checks/spec_consistency.py`.
