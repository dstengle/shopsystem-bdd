---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i39-design-model-check
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i39
status: awaiting-answer
argues: [design-model-check]
adds: [design-model-check#r120, design-model-check#r121]
changes: []
removes: []
date: 2026-10-27
---

# design-model-check

The drafts of this proposal are in .shop/work/i39/runs/i39/1-integrate/drafts/round-1/.

## Questions
- design-model-check r120, r121 against table rows r115 (v17) and r117 (v18). Lines: [r120] **When** `model check` reads a request whose `part_of` names a job-thread kept in another repository, `model check` shall print no `v17` for the request. [r121] **When** `model check` reads a request raised for a request of another context, `model check` shall print neither `v17` nor `v18` for the request. Readings: (a) as drafted, standalone lines that override the rows for these requests (recommended, since the lines are what q14 accepted); (b) the rows change instead: "| [r115] | v17 | a request neither is part of a job-thread, cites an origin nor is raised for a request |" and "| [r117] | v18 | ... judged from the id alone, other than the request a request is raised for |", with lines 8 and 9 citing them.
