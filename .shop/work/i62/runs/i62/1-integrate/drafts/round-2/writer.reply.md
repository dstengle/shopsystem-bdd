/tmp/work-run-i62-8993uq31/i62-1-integrate/.shop/scratch/1-integrate/drafts/round-2/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| added | supervision | r212 | **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge. | q41 line 2: "**If** a scenario's run fails for a reason that a rerun of that scenario alone does not repeat, **then** `work run` shall run that scenario again once before it refuses the merge" (its first response; unchanged from round 1) |
| added | supervision | r213 | **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item. | q41 line 2: "... and give both runs in its question when the second also fails." (its second response) |

No lines changed or removed. No r214 drafted (see question 2). No glossary terms added, changed or removed. No decision files.

## Questions

1. supervision r213, "its question" (two readings).
   - (a, recommended, drafted) The question r131 writes under the work-item's `## Questions`: the merge refused, the implementer's output (r132: commits on which the scenarios and the suite pass) is missing. Line as drafted: "[r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item."
   - (b) A question of its own about the refused merge, written by `work run` in place of r131's. Line: "[r213] **If** the second run of a scenario that r212 makes also fails, **then** `work run` shall write under the work-item's `## Questions` a question that gives both runs of the scenario and transition the work-item to `awaiting-answer`."
   - Also open under either reading: whether "both runs" means each with its command, how it ended and its output (as r155 gives a branch reviewer). If yes, r213 ends "... give both runs of the scenario, each with its command, how it ended and its output, in ...".

2. supervision, what follows a second run that passes (round 1's question 4). q41 implies the merge is refused only after the second run, but does not say the merge goes ahead when it passes; the line is not drafted. If yes: "[r214] **When** the second run of a scenario that r212 makes passes, `work run` shall take the scenario as passing for r4's merge."

3. supervision r212, the condition (round 1's question 1): (a, recommended, drafted) every scenario failure that would refuse the merge gets one more run, the rerun being how `work run` finds whether it repeats; (b) only failures `work run` can tell in advance are not caused by the work-item, a list q41 does not give.

4. supervision r212, "alone" (round 1's question 2): (a, recommended, drafted) the second run is of that scenario by itself; (b) the same run (work-item's scenarios or whole suite) is made again: "... `work run` shall make that run again once before it refuses the merge."

5. supervision r212, its reach (round 1's question 5): scenarios only, in both runs r4 makes; should a failing non-scenario test of the suite get a second run too? If yes: "[r212] **If** a scenario or test fails in a run ...".

6. supervision, Not yet (round 1's question 6): keep "Retries, refused claims, ..." as it is, or narrow it to "Retries of a stage"?

## Cut sentences

- "A scenario's git repository is changed by git after its step ends" (q41's title; the observed cause, not a line).
- q41 line 1, "**When** a scenario's steps make a git repository for the scenario, the steps shall keep git from starting any maintenance of that repository that runs after the step that started it ends." Refused (Outcomes 1), so not drafted.
