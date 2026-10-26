## Budget
No file touched (stopped before any edit).

# Report of w200 implement: NEEDS_CONTEXT

Stop: the brief's answer says features/supervision.feature's r131 outline "now has a formulate round row on capability-proposal p1 (columns node and setup added)". It is not on this branch (HEAD cab55fa6, based on 50a40103).
Evidence: `grep -n "@r131" features/supervision.feature` gives line 909 only; the outline there (909-923) has columns `who | status | gives | missing`, rows researcher, planner, implementer, reviewer, and no formulate row, no `node` or `setup` column. `git log -- features/supervision.feature` last touches: a853a2ea. The work-item-only outline is not marked deprecated either.
Plan decision 4 forbids coding the formulate check without that red row, and I may not write the row.

Suite at start: 945 passed, 0 failed at cab55fa6. Finding 3's wording ("gave DONE") was already fixed by cab55fa6.
Scenarios green/red: nothing run or changed. Plan contained no code. Tests changed under an allowance: none. Open questions: the plan's part 5 cases remain.
Needed: the formulator's feature commit on this branch (rebase/merge), then run again.
