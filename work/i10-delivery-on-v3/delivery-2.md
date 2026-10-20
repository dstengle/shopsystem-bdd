---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/delivery-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-delivery
status: withdrawn
wkind: capability
under: delivery
accepts: [delivery#r13, delivery#r14, delivery#r16, delivery#r17]
blocked_by: [work-item/delivery-1, work-item/supervision-4]
risk: none
---

# delivery-2

## Observable
The session relays `work run`'s questions, records the person's answers with `work rule` and runs again, and
handles a budget stop and a wrong-scenario question as the lines say; in every run.

## Unknown
How a headless fixture gives the person's answer before the question is asked (the prompt gives answers in
advance, as consistency-fix did).

## Fixture cases
Stub claude as in delivery-1.
| requirements | case | what the fixture holds |
|---|---|---|
| r13, r14 | deliver-question | the stub planner returns QUESTION on one item; the prompt gives the answer |
| r16 | deliver-budget | the stub reports costs that reach the run's budget |
| r17 | deliver-scenario-wrong | the stub implementer hands back saying a scenario is wrong |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`skills/delivering-an-initiative/SKILL.md`, `tests/workflow/test_delivery.py`, `tests/workflow/checks/delivery.py`, fixtures.

Withdrawn 2026-10-19: deferred until the skeleton runs (initiative notes)
