---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/formulation-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-formulation
status: drafted
wkind: capability
under: formulation
accepts: [formulation#r1-r14]
blocked_by: [work-item/formulation-1]
risk: none
---

# formulation-2

## Observable
Formulation's scenarios run as fixture sessions and pass in every run.

## Unknown
Whether a hand-back reaching formulation through a ruling (r10) can be set up as a fixture without a real
`work run` (an awaiting-ruling work-item written by the fixture with its evidence).

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r4, r5, r6, r7, r8, r11, r12, r13 | formulate | the lending lines applied, nothing formulated; the count scenario and removed r4's pass today |
| r13 (where it cannot) | noclingo | as formulate, clingo unimportable |
| r3 | formulate-two-readings | as formulate, one lend-items line with two readings |
| r9 | formulate-every-call | a line every call must keep, giving two reasons |
| r10 | formulate-hand-back | an awaiting-ruling work-item whose ruling sends a scenario back with its evidence |
| r14 | formulate-avoided-word | a scenario using a word the glossary avoids |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_formulation.py`, `tests/workflow/checks/formulation.py`, `tests/workflow/fixtures/shelf.py`.
