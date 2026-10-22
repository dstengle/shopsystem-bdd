---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-ruling-returns-to-the-asking-stage
summary: "A ruling returns the work-item from `awaiting-ruling` to the status the stage that asked its question started from, not always to `planned`."
date: 2026-10-22
status: proposed
source: [observation/2026-10-22-release-0-24-0, design-decision/work-item-lifecycle-as-run]
by: "the person, 2026-10-22 (\"yes, do 1-6\"), delegating the drafting decisions to the coordinator; on the design note rulings, round trips and the analysis tools' query output"
---

# 0063. A ruling returns to the asking stage

## Decision

This replaces one row of decision 0039, "awaiting-ruling → planned | the person, `work rule`"; the rest of 0039 stands.

| from → to | made by | guard |
|---|---|---|
| awaiting-ruling → drafted | the person, `work rule` | the question was a researcher's |
| awaiting-ruling → researched | the person, `work rule` | the question was a planner's |
| awaiting-ruling → ready | the person, `work rule` | the question was an implementer's |
| awaiting-ruling → done | the person, `work rule` | the question was a reviewer's |

`work rule` writes the ruling, with the date, under the work-item's `## Rulings`. `work run` writes each of a
work-item's rulings, with the question it answers, in the brief of every worker it starts for it, and an implementer
started for a work-item whose work-item branch was kept works on that branch.
