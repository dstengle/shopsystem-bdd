---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/planning-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-planning
status: done
wkind: capability
under: planning
accepts: [planning#r1-r8]
blocked_by: [work-item/supervision-1]
risk: none
---

# planning-1

## Observable
`bdd-planner` plans a researched work-item from its notes into the plan file its brief names, with the open
decisions and the tests they break and no code; its result gives the status and the final file set.

## Unknown
Whether a planner limited to the notes and the file set lists the tests its decisions break as completely as the
planning session did with a scout re-run.

## What changes
New `agents/bdd-planner.md` (Read, Glob, Grep, Write; opus): the plan file, the open decisions with what they rest
on, the tests the decisions break, no code, the result file with the final file set, a `QUESTION` with its readings.

## Fixture cases
Each starts the planner on a researched work-item with prepared notes, with the fixture harness outside this
repository (formulation-1, which moves it in, is deferred).
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4, r5, r7 | plan | a researched lend-items item, notes with one broken test |
| r6 | plan-question | notes where a broken test's fate is a contract decision |
| r8 | plan-no-context | a brief whose notes file does not exist |

## Files, roughly
`agents/bdd-planner.md`, the fixture cases.
