---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i47-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i47
status: awaiting-answer
argues: [supervision]
date: 2026-10-28
adds: [supervision#r188, supervision#r189, supervision#r190]
changes: []
removes: [supervision#r4]
---

# supervision

The drafts of this proposal are in .shop/work/i47/runs/supervision/3-integrate/drafts/round-1/.

## Questions
- supervision, r177 against r4. Lines: added [r177] **While** no work-item accepts a requirement that a scenario names, `work run` shall count a failure of that scenario in the whole-suite run of a work-item's branch as expected. r4 merges a work-item branch only if the whole suite passes "but for the failing scenarios r43 counts as expected"; as drafted, a failure r177 counts as expected still blocks the merge. Reading A (recommended): r177 lets the merge through: change r4 to "[r4] **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r177 count as expected." Reading B: r4 stays.
- supervision, Implementation note for r177. Line: added [r177] (as above). The existing note "r122: the checks are the whole-suite runs of r24 and r43" names the runs; r177 says only "the whole-suite run of a work-item's branch". Reading A (recommended): r177 covers both runs: add the Implementation line "r177: the whole-suite runs are those of r24 and r43; `--whole-suite` marks each such scenario as xfail." Reading B: only r43's run before a merge: "r177: the whole-suite run is r43's, before a merge."
- supervision, r188 (added, after r122). Line in full: [r188] **While** no work-item accepts a requirement that a scenario names, `work run` shall count a failure of that scenario in the whole-suite run of a work-item's branch as expected. Its Implementation note (answer Q2, 2026-10-28): "r188: the whole-suite runs are those of r24 and r43; `--whole-suite` marks each such scenario as xfail." Reading A (recommended): apply the line and the note as drafted. Reading B: do not apply r188.
- supervision, r189 (added, after r132). Line in full: [r189] **When** a work-item's researcher gives an empty file set and no question, `work run` shall take the empty file set as the researcher's output. Reading A (recommended): apply as drafted. Reading B: do not apply r189; an empty file set stays a missing output (r131, r132).
- supervision, r190 added and r4 removed (answer Q1, 2026-10-28: r4 changes, retired, new id). r4 was: [r4] **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 counts as expected. Drafted: [r190] **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r188 count as expected. Reading A (recommended): retire r4 and add r190 as drafted. Reading B: r4 stays and r190 is not added.

## Answers
- 2026-10-28: Q1, r177 against r4: reading A, r4 changes (retired, new id) so a failure r177 counts as expected does not block the merge (answered by the coordinator under the person's delegation, 2026-10-28)
- 2026-10-28: Q2, the Implementation note for r177: reading A, r177 covers the whole-suite runs of r24 and r43 (answered by the coordinator under the person's delegation, 2026-10-28)
