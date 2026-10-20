---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/spec-integration-1
kind: work-item
part_of: capability-proposal/first-spec-spec-integration
status: withdrawn
wkind: capability
under: spec-integration
accepts: [spec-integration#r1-r7, spec-integration#r10]
blocked_by: [work-item/formulation-1]
risk: none
---

# spec-integration-1

## Observable
Spec integration's gate scenarios run as fixture sessions and pass in every run.

## Unknown
How to run r10's "this session brainstormed the note" headless: a first `claude -p` turn that brainstorms, then
`--resume` with the integration request.

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r3 | integrate | keep-items r1-r4, the approved lending note |
| r1 (questions), r2 | integrate-question | the note leaves "too many books" open and has a sentence no line can quote |
| r4 | answer | round-1 drafts and a gate with one question; the prompt answers it |
| r5, r6 | apply-reject | round-1 drafts; the answer approves all but one line |
| r7 | integrate-second-spec | a note that asks for a second spec |
| r10 | brainstormed-here | two turns in one session: brainstorm, then integrate |

Placed under i1's proposal: these requirements came from it, and i10 brings only their scenarios' harness.

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_spec_integration.py`, `tests/workflow/checks/spec_integration.py`, `tests/workflow/fixtures/shelf.py`.

Withdrawn 2026-10-19: deferred until the skeleton runs (initiative notes)
