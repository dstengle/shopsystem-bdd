# supervision, formulate round 1: reply

## Coverage

| id | line | scenario |
|---|---|---|
| r219 | "**If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge." | a scenario whose failure before a merge would keep the work-item branch from being merged is run again once, alone, before the merge is refused |
| r222 | "**When** the second run of a scenario that r219 makes passes, `work run` shall take the scenario as passing in r4's merge of the work-item branch." | a scenario that fails before a merge and passes on its second run, alone, lets the work-item branch be merged |

r220 already has its scenario (@r220) in features/supervision.feature. It is left as it is and not drafted again. In the file, r219's scenario goes directly before @r220 and r222's directly after it, following the lines' order.

## Questions

None. Each line has one reading.

## Cases no line mentions (no scenario written)

- A scenario that fails both in the run of the work-item's scenarios and in the whole suite's run before the same merge: no line says whether it is run again once in all, or once for each failing run.
- A scenario that fails on its first run and passes on its second, alone, while a different scenario fails on both of its runs: by r4 the merge is still refused. No line says whether the question r131 writes also names the scenario that passed on its second run.
- Several scenarios that fail before one merge: no line says whether their second runs happen one after another or side by side. "alone" might mean each one is run apart from the others.
- A second run that cannot be made at all, for example because the run ends in an error before the scenario runs: no line says whether that counts as a failing second run under r220.
- The runs that r154 makes before a branch review: no line says whether a scenario failing there is run again too. r219 covers only the runs before r4's merge.

## Drafts

- /tmp/work-run-i62-cldtsv95/supervision-14-formulate/.shop/scratch/14-formulate/drafts/round-1/supervision.feature
