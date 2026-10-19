---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/red-green-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-red-green
status: drafted
wkind: capability
under: red-green
accepts: [red-green#r3-r5, red-green#r7, red-green#r12-r14, red-green#r17]
blocked_by: [work-item/red-green-1]
risk: none
---

# red-green-2

## Observable
Each stop condition of red-green stops the implementer with the right status and evidence, in every run.

## Unknown
Whether one fixture can plant each stop without the others firing first.

## Fixture cases
Each runs `work step <item>` on a ready work-item.
| requirements | case | what the fixture holds |
|---|---|---|
| r3, r7 | implement-passes-early | a scenario the code already satisfies |
| r4, r7 | implement-contradiction | a Then that only code contradicting it can pass |
| r5 | implement-breaks-test | a decision that breaks a test the plan does not list (and a setup-only change that is allowed) |
| r12 | implement-unnamed-work | going green needs a module the plan does not name |
| r13 | implement-meaning | a green scenario breaks unless a step's meaning changes |
| r14 | implement-open-decision | a case the plan, rulings and Behaviour leave open |
| r17 | implement-claim-refused | the work needs a file a claimed item holds |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_red_green.py`, `tests/workflow/checks/red_green.py`, fixtures; `skills/bdd-red-green/SKILL.md`
only where a run shows a stop is not followed.
