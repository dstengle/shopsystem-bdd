# Gate: i62 (q41 line 2), round 2 drafts

Drafts: .shop/scratch/1-integrate/drafts/round-2/spec/capabilities/supervision.md (the Behaviour section, whole)

## supervision

Added:
- [r212] **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge.
  (q41 line 2, first response)
- [r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item.
  (q41 line 2, second response)

Changed: none. Removed: none. Glossary: none. Decisions: none.

## Questions

1. r213, "its question". (a, recommended, drafted) the question r131 writes under the work-item's `## Questions`. (b) a question of its own: "[r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall write under the work-item's `## Questions` a question that gives both runs of the scenario and transition the work-item to `awaiting-answer`." Also: should "both runs" each give command, how it ended and output? If yes, r213 ends "... give both runs of the scenario, each with its command, how it ended and its output, in ...".
2. After a passing second run. q41 does not say the merge goes ahead. If yes: "[r214] **When** the second run of a scenario that r212 makes passes, `work run` shall take the scenario as passing for r4's merge."
3. r212's condition ("a reason a rerun alone does not repeat"). (a, recommended, drafted) every failure that would refuse the merge gets one more run; the rerun is how `work run` finds whether it repeats. (b) only failures `work run` can tell in advance are not the work-item's (q41 gives no list): "[r212] **If** a scenario fails in a run that `work run` makes before a merge, for a reason that `work run` takes as not caused by the work-item, **then** `work run` shall run that scenario again once, alone, before it refuses the merge."
4. r212, "alone". (a, recommended, drafted) the second run is of that scenario by itself. (b) the same run is made again: "... `work run` shall make that run again once before it refuses the merge."
5. r212, reach. Scenarios only, in both runs r4 makes. Should a failing non-scenario test of the suite get a second run too? If yes: "[r212] **If** a scenario or test fails in a run ...".
6. Not yet. Keep "Retries, refused claims, ..." as it is, or narrow it to "Retries of a stage"?

## Cut sentences (2)
- q41's title (the observed cause, not a line).
- q41 line 1 (refused, Outcomes 1).
