/tmp/work-run-i62-8993uq31/i62-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| added | supervision | r212 | **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge. | q41 line 2: "**If** a scenario's run fails for a reason that a rerun of that scenario alone does not repeat, **then** `work run` shall run that scenario again once before it refuses the merge, and give both runs in its question when the second also fails." (its first response) |

No lines changed or removed. No glossary terms added, changed or removed. No decision files.

## Questions

1. supervision r212, the condition (two readings of "a reason that a rerun of that scenario alone does not repeat"). `work run` is a script and takes no judgment, and it cannot know before the second run whether a failure repeats.
   - (a, recommended, drafted) The rerun is how `work run` finds out. Every scenario failure that would refuse the merge gets one more run, and a failure the second run does not repeat is the kind the request means. r212 as drafted.
   - (b) Only failures whose reason `work run` can tell in advance will not repeat (for example a git error from outside the scenario) get another run. Any other failure refuses the merge at once. Line: "[r212] **If** a scenario fails in a run that `work run` makes before a merge, for a reason that `work run` takes as not caused by the work-item, **then** `work run` shall run that scenario again once, alone, before it refuses the merge." This reading needs a list of such reasons, which q41 does not give.

2. supervision r212, "alone" (two readings).
   - (a, recommended, drafted) The second run is a run of that scenario by itself, apart from the suite and the other scenarios.
   - (b) "alone" belongs only to the condition, and the second run is a repeat of the same run (the work-item's scenarios, or the whole suite). Line: "... `work run` shall make that run again once before it refuses the merge."

3. supervision, the second response "and give both runs in its question when the second also fails". It is a second response, so it needs a line of its own. q41 does not say which question "its question" is. In spec/ the only question that follows a refused merge is r131's question naming the missing output (r132: an implementer's output is commits on which the scenarios and the suite pass). If yes, the line would be: "[r<n>] **When** a scenario that `work run` ran again under r212 fails again, `work run` shall give both runs of the scenario, each with its command, how it ended and its output, in the question r131 writes for the work-item." The id is to be assigned above r212 and above every id other initiatives' drafts add on supervision. I did not draft it because the input prompt allows only r212 and I do not know which ids above r212 are free.

4. supervision, what follows a second run that passes. q41 implies that the merge goes ahead ("before it refuses the merge") but does not say so. r4 says the merge happens only if the scenarios and the suite pass. If yes, the line would be: "[r<n>] **When** a scenario that `work run` ran again under r212 passes, `work run` shall take the scenario as passing for r4's merge."

5. supervision r212, what it covers. As drafted, r212 covers both runs r4 makes before a merge (the work-item's scenarios and the whole suite), and only scenarios. It does not cover tests in the suite that are not scenarios, or the runs of r24 and r154. Should a failing non-scenario test of the whole suite also get a second run? If yes: "[r212] **If** a scenario or test fails in a run ... ".

6. supervision, Not yet. The entry "Retries, refused claims, ..." could be read as deferring what r212 now does. Keep it as it is, or narrow it to "Retries of a stage" (Not yet section changed)?

## Cut sentences

- "A scenario's git repository is changed by git after its step ends" (q41's title; it is the observed cause, not a line).
- q41 line 1, "**When** a scenario's steps make a git repository for the scenario, the steps shall keep git from starting any maintenance of that repository that runs after the step that started it ends." It was refused (Outcomes 1), so it is not drafted.
