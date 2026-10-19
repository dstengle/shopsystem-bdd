---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/delivery-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-delivery
status: drafted
wkind: capability
under: delivery
accepts: [delivery#r1-r12, delivery#r15]
blocked_by: [work-item/formulation-1, work-item/supervision-5]
risk: none
---

# delivery-1

## Observable
`delivering-an-initiative` drafts the work-items of an initiative's formulated proposals, commits them, shows them
and runs `work run` to the end; its scenarios pass in every run.

## Unknown
Whether a session waits on a background `work run` without reading its output (the reply-file wait of
initiative-round is the pattern), and how thin its drafted items come out on the lending fixture.

## What changes
New `skills/delivering-an-initiative/SKILL.md`: drafting by `work add` (one unknown, thin, risk, blocked_by,
Retires), routing a two-reading requirement to integration, the table, `work run` in the background, the end.

## Fixture cases
The session's `work run` uses the stub claude, whose script turns every item green.
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4, r5, r6, r7, r8, r10, r12, r15 | deliver | an initiative with two formulated proposals (lend-items, keep-items' changes with a held scenario), one merged proposal not formulated, a guarantees capability with a bound |
| r11 | deliver-unclean (two rows) | an uncommitted change; on the default branch |
| r9 | deliver-two-readings | a formulated requirement with two readings |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`skills/delivering-an-initiative/SKILL.md`, `tests/workflow/test_delivery.py`, `tests/workflow/checks/delivery.py`, fixtures.
