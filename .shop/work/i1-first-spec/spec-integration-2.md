---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/spec-integration-2
kind: work-item
part_of: capability-proposal/first-spec-spec-integration
status: withdrawn
wkind: capability
under: spec-integration
accepts: [spec-integration#r8, spec-integration#r9, spec-integration#r11-r19]
blocked_by: [work-item/spec-integration-1]
risk: none
---

# spec-integration-2

## Observable
Spec integration's apply, small-change and glossary scenarios run as fixture sessions and pass in every run.

## Unknown
none

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r11, r12, r13, r14, r15, r16, r18 | apply | round-1 drafts, the gate, the person's yes; a glossary entry added |
| r8 | small-change | a request to add one keep-items line, no note |
| r9 | apply-delegated | as apply, approved under the person's delegation |
| r17 | apply-with-work | as apply, in a repository with `.shop/work/` and a capability-proposal |
| r19 | glossary-no-work | a glossary change, no `.shop/work/` |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_spec_integration.py`, `tests/workflow/checks/spec_integration.py`, `tests/workflow/fixtures/shelf.py`.

Withdrawn 2026-10-19: deferred until the skeleton runs (initiative notes)
