## Coverage

| Line | Scenario |
|---|---|
| r218 | "a change to .shop/work/ in the repository's own checkout, less another initiative's path run side by side, that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file" |

Notes on the scenario:
- It covers both parts of r218 in one scenario. i1's file is put back and w1 is failed, naming it. i2's change is in the Given, and the check is that w1's record does not name i2's file. That check is r218's own "less ... naming each file" response.
- I did not assert that i2's file is left as i2 changed it. That is r215's response, and r215 already has its own scenario.
- Most of the step wording is reused from @r28 and @r214 to @r216. Three steps are new and need step code:
  - The combined Given, where two sessions change two files.
  - The Then "nothing recorded of w1 names .shop/work/i2/initiative.md". It is a standalone form of r214's trailing clause "nothing recorded of w1 naming ...".
  - "w1 is failed, naming .shop/work/i1/initiative.md". It is reused from @r28, which is deprecated, so its step code must outlive @r28's removal.

## Questions

None. I read r218 one way only:
- "the work-item" is the work-item of the worker that ended.
- "it" in "put it back" is the difference, less the excluded paths.

## Cases no line mentions

- No line says what happens when a worker of i1 changes a path under `.shop/work/i2/`. That path is excluded from i1's check by r214 and r218. r215 and r216 cover only a change made by a session of i2.
- No line says what happens when the difference under `.shop/work/` is committed rather than left uncommitted. "differs from its last commit" leaves out a change that was committed to the main checkout's branch.

## Drafts

- /tmp/work-run-i63-1aqx8f1u/supervision-18-formulate/.shop/scratch/18-formulate/drafts/round-1/supervision.feature.md
