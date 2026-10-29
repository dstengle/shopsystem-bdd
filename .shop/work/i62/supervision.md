---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i62-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i62
status: awaiting-answer
argues: [supervision]
adds: [supervision#r212, supervision#r213]
changes: []
removes: []
date: 2026-10-29
---

# supervision

The drafts of this proposal are in .shop/work/i62/runs/i62/1-integrate/drafts/round-2/.

## Questions
- r213, "its question". Line (added): [r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item. Readings: (a, recommended, as drafted) the question r131 writes under the work-item's `## Questions`; (b) a question of its own: "[r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall write under the work-item's `## Questions` a question that gives both runs of the scenario and transition the work-item to `awaiting-answer`."
- r213, what "both runs" give. Line (added): [r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item. Readings: (a, recommended, as drafted) both runs, without saying what each gives; (b) each run with its command, how it ended and its output: "... give both runs of the scenario, each with its command, how it ended and its output, in the question r131 writes for the work-item."
- After a passing second run. Lines (added): r212 and r213 (q41 does not say the merge goes ahead). Readings: (a, recommended, as drafted) add no line; (b) add a line: "[r214] **When** the second run of a scenario that r212 makes passes, `work run` shall take the scenario as passing for r4's merge."
- r212's condition. Line (added): [r212] **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge. Readings: (a, recommended, as drafted) every failure that would refuse the merge gets one more run; the rerun is how `work run` finds whether it repeats; (b) only failures `work run` can tell in advance are not the work-item's (q41 gives no list): "[r212] **If** a scenario fails in a run that `work run` makes before a merge, for a reason that `work run` takes as not caused by the work-item, **then** `work run` shall run that scenario again once, alone, before it refuses the merge."
- r212, "alone". Line (added): r212 as in the previous question. Readings: (a, recommended, as drafted) the second run is of that scenario by itself; (b) the same run is made again: "[r212] **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall make that run again once before it refuses the merge."
- r212, reach. Line (added): r212 as above. Readings: (a, recommended, as drafted) scenarios only, in both runs r4 makes; (b) a failing non-scenario test of the suite gets a second run too: "[r212] **If** a scenario or test fails in a run ..."
