---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-0-19-0-ids-fixture-scores-and-costs
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-16
---

# 0.19.0 requirement ids: fixture scores and costs

Scores and costs of the 0.19.0 requirement-ids fixture runs (2026-10-16), from the harness in `/home/vscode/scratch/shopsystem-bdd/ids/`: B = branch `0.19.0-requirement-ids` at `8b61d65` (integrate, apply, formulate, noclingo, migrate, three runs each), A = 0.18.0 at `e3c846d` (integrate and formulate, two runs each, cost only). `run-all.log` is the first full run's output, with B-integrate-1 to 3 scored before the scorer's gate-parsing fixes; `scores.txt` and `scores-final.txt` are the rescored results and `costs-final.txt` the costs, all scored with B's model at `8b61d65`. The test log `2026-10-16-requirement-ids-test-log.md` reports them; the per-run inputs are in `2026-10-16-ids-runs/`.

Archived from git-ignored scratch; each file's text as it was.

## `/home/vscode/scratch/shopsystem-bdd/ids/scores-final.txt`

~~~~~~
A-formulate-1 ok=6 FAIL=2
   FAIL lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7  [lend-items ['r1', 'r2', 'r3', 'r5', 'r6'], keep-items ['r1', 'r2', 'r3', 'r6', 'r7']]
   FAIL model check: no v_s3 for keep-items or lend-items  [missingmass.io/demo/shelf/lend-items#r4]
A-formulate-2 ok=6 FAIL=2
   FAIL lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7  [lend-items ['r1', 'r2', 'r3', 'r4', 'r6'], keep-items ['r1', 'r2', 'r3', 'r6']]
   FAIL model check: no v_s3 for keep-items or lend-items  [missingmass.io/demo/shelf/keep-items#r7; missingmass.io/demo/shelf/lend-items#r5]
A-integrate-1 ok=7 FAIL=0
A-integrate-2 ok=7 FAIL=0
B-apply-1 ok=7 FAIL=0
B-apply-2 ok=7 FAIL=0
B-apply-3 ok=7 FAIL=0
B-formulate-1 ok=8 FAIL=0
B-formulate-2 ok=8 FAIL=0
B-formulate-3 ok=8 FAIL=0
B-integrate-1 ok=7 FAIL=0
B-integrate-2 ok=7 FAIL=0
B-integrate-3 ok=7 FAIL=0
B-migrate-1 ok=12 FAIL=0
B-migrate-2 ok=11 FAIL=1
   FAIL spec/ and features/ committed in one commit  [25ab91b: features/keep-items.feature; d57aa99: spec/capabilities/keep-items.md spec/index.md]
B-migrate-3 ok=12 FAIL=0
B-noclingo-1 ok=7 FAIL=0
B-noclingo-2 ok=7 FAIL=0
B-noclingo-3 ok=7 FAIL=0
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/costs-final.txt`

~~~~~~
A-formulate-1 cost $0.63, 5 turns (num_turns summed 6 over 2 results), 111 s wall, tokens all models: in 64, cache write 73048, cache read 551492, out 19334
A-formulate-2 cost $0.65, 5 turns (num_turns summed 6 over 2 results), 558 s wall, tokens all models: in 56, cache write 90755, cache read 482653, out 18145
A-integrate-1 cost $0.52, 4 turns (num_turns summed 5 over 2 results), 107 s wall, tokens all models: in 36, cache write 57026, cache read 282319, out 16691
A-integrate-2 cost $0.48, 4 turns (num_turns summed 5 over 2 results), 102 s wall, tokens all models: in 36, cache write 51769, cache read 285251, out 15947
B-apply-1 cost $0.20, 4 turns (num_turns summed 5 over 2 results), 30 s wall, tokens all models: in 22, cache write 41598, cache read 217539, out 3741
B-apply-2 cost $0.21, 4 turns (num_turns summed 5 over 2 results), 38 s wall, tokens all models: in 26, cache write 42261, cache read 265727, out 4173
B-apply-3 cost $0.19, 4 turns (num_turns summed 5 over 2 results), 29 s wall, tokens all models: in 22, cache write 40555, cache read 213812, out 3558
B-formulate-1 cost $0.59, 5 turns (num_turns summed 6 over 2 results), 583 s wall, tokens all models: in 58, cache write 90837, cache read 481038, out 15307
B-formulate-2 cost $0.57, 5 turns (num_turns summed 6 over 2 results), 97 s wall, tokens all models: in 54, cache write 72603, cache read 503593, out 16168
B-formulate-3 cost $0.56, 6 turns (num_turns summed 7 over 2 results), 90 s wall, tokens all models: in 62, cache write 71141, cache read 586530, out 15829
B-integrate-1 cost $0.57, 4 turns (num_turns summed 5 over 2 results), 121 s wall, tokens all models: in 34, cache write 72201, cache read 272243, out 17427
B-integrate-2 cost $0.49, 4 turns (num_turns summed 5 over 2 results), 99 s wall, tokens all models: in 34, cache write 54912, cache read 278346, out 15454
B-integrate-3 cost $0.52, 4 turns (num_turns summed 5 over 2 results), 114 s wall, tokens all models: in 36, cache write 56747, cache read 298354, out 17163
B-migrate-1 cost $0.17, 9 turns (num_turns summed 10 over 1 results), 25 s wall, tokens all models: in 18, cache write 27132, cache read 285100, out 2941
B-migrate-2 cost $0.17, 8 turns (num_turns summed 9 over 1 results), 25 s wall, tokens all models: in 16, cache write 28182, cache read 253081, out 2906
B-migrate-3 cost $0.15, 7 turns (num_turns summed 8 over 1 results), 21 s wall, tokens all models: in 14, cache write 26181, cache read 211286, out 2344
B-noclingo-1 cost $0.59, 6 turns (num_turns summed 7 over 2 results), 108 s wall, tokens all models: in 64, cache write 72566, cache read 593659, out 17389
B-noclingo-2 cost $0.53, 6 turns (num_turns summed 7 over 2 results), 110 s wall, tokens all models: in 62, cache write 67550, cache read 607836, out 15686
B-noclingo-3 cost $0.59, 5 turns (num_turns summed 6 over 2 results), 111 s wall, tokens all models: in 64, cache write 72016, cache read 568969, out 17250
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/scores.txt`

~~~~~~
== A-formulate-1 (formulate)
   cost $0.63, 5 turns (num_turns summed 6 over 2 results), 111 s wall, tokens all models: in 64, cache write 73048, cache read 551492, out 19334
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   FAIL lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7  [lend-items ['r1', 'r2', 'r3', 'r5', 'r6'], keep-items ['r1', 'r2', 'r3', 'r6', 'r7']]
   ok   model check: no v_s1, no v_s2
   FAIL model check: no v_s3 for keep-items or lend-items  [missingmass.io/demo/shelf/lend-items#r4]
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== A-formulate-2 (formulate)
   cost $0.65, 5 turns (num_turns summed 6 over 2 results), 558 s wall, tokens all models: in 56, cache write 90755, cache read 482653, out 18145
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   FAIL lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7  [lend-items ['r1', 'r2', 'r3', 'r4', 'r6'], keep-items ['r1', 'r2', 'r3', 'r6']]
   ok   model check: no v_s1, no v_s2
   FAIL model check: no v_s3 for keep-items or lend-items  [missingmass.io/demo/shelf/keep-items#r7; missingmass.io/demo/shelf/lend-items#r5]
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== A-integrate-1 (integrate)
   cost $0.52, 4 turns (num_turns summed 5 over 2 results), 107 s wall, tokens all models: in 36, cache write 57026, cache read 282319, out 16691
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== A-integrate-2 (integrate)
   cost $0.48, 4 turns (num_turns summed 5 over 2 results), 102 s wall, tokens all models: in 36, cache write 51769, cache read 285251, out 15947
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== B-apply-1 (apply)
   cost $0.20, 4 turns (num_turns summed 5 over 2 results), 30 s wall, tokens all models: in 22, cache write 41598, cache read 217539, out 3741
   ok   spec/ committed alone
   ok   the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   ok   the removed line is gone, its id r4 in retired, r5 kept
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== B-apply-2 (apply)
   cost $0.21, 4 turns (num_turns summed 5 over 2 results), 38 s wall, tokens all models: in 26, cache write 42261, cache read 265727, out 4173
   ok   spec/ committed alone
   ok   the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   ok   the removed line is gone, its id r4 in retired, r5 kept
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== B-apply-3 (apply)
   cost $0.19, 4 turns (num_turns summed 5 over 2 results), 29 s wall, tokens all models: in 22, cache write 40555, cache read 213812, out 3558
   ok   spec/ committed alone
   ok   the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   ok   the removed line is gone, its id r4 in retired, r5 kept
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== B-formulate-1 (formulate)
   cost $0.59, 5 turns (num_turns summed 6 over 2 results), 583 s wall, tokens all models: in 58, cache write 90837, cache read 481038, out 15307
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   model check: no v_s1, no v_s2
   ok   model check: no v_s3 for keep-items or lend-items
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== B-formulate-2 (formulate)
   cost $0.57, 5 turns (num_turns summed 6 over 2 results), 97 s wall, tokens all models: in 54, cache write 72603, cache read 503593, out 16168
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   model check: no v_s1, no v_s2
   ok   model check: no v_s3 for keep-items or lend-items
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== B-formulate-3 (formulate)
   cost $0.56, 6 turns (num_turns summed 7 over 2 results), 90 s wall, tokens all models: in 62, cache write 71141, cache read 586530, out 15829
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   model check: no v_s1, no v_s2
   ok   model check: no v_s3 for keep-items or lend-items
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== B-integrate-1 (integrate)
   cost $0.57, 4 turns (num_turns summed 5 over 2 results), 121 s wall, tokens all models: in 34, cache write 72201, cache read 272243, out 17427
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== B-integrate-2 (integrate)
   cost $0.49, 4 turns (num_turns summed 5 over 2 results), 99 s wall, tokens all models: in 34, cache write 54912, cache read 278346, out 15454
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== B-integrate-3 (integrate)
   cost $0.52, 4 turns (num_turns summed 5 over 2 results), 114 s wall, tokens all models: in 36, cache write 56747, cache read 298354, out 17163
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== B-migrate-1 (migrate)
   cost $0.17, 9 turns (num_turns summed 10 over 1 results), 25 s wall, tokens all models: in 18, cache write 27132, cache read 285100, out 2941
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is <context>/keep-items, retired: []
   ok   spec/index.md's id is the context id
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   ok   model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)
   ok   spec/ and features/ committed in one commit
== B-migrate-2 (migrate)
   cost $0.17, 8 turns (num_turns summed 9 over 1 results), 25 s wall, tokens all models: in 16, cache write 28182, cache read 253081, out 2906
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is <context>/keep-items, retired: []
   ok   spec/index.md's id is the context id
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   ok   model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)
   FAIL spec/ and features/ committed in one commit  [25ab91b: features/keep-items.feature; d57aa99: spec/capabilities/keep-items.md spec/index.md]
== B-migrate-3 (migrate)
   cost $0.15, 7 turns (num_turns summed 8 over 1 results), 21 s wall, tokens all models: in 14, cache write 26181, cache read 211286, out 2344
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is <context>/keep-items, retired: []
   ok   spec/index.md's id is the context id
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   ok   model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)
   ok   spec/ and features/ committed in one commit
== B-noclingo-1 (noclingo)
   cost $0.59, 6 turns (num_turns summed 7 over 2 results), 108 s wall, tokens all models: in 64, cache write 72566, cache read 593659, out 17389
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
   ok   the reply says model check did not run
== B-noclingo-2 (noclingo)
   cost $0.53, 6 turns (num_turns summed 7 over 2 results), 110 s wall, tokens all models: in 62, cache write 67550, cache read 607836, out 15686
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
   ok   the reply says model check did not run
== B-noclingo-3 (noclingo)
   cost $0.59, 5 turns (num_turns summed 6 over 2 results), 111 s wall, tokens all models: in 64, cache write 72016, cache read 568969, out 17250
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
   ok   the reply says model check did not run
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/run-all.log`

~~~~~~
Preparing worktree (detached HEAD e3c846d)
HEAD is now at e3c846d 0.18.0: spec-round, a controller for each round of integration and formulation; the session with the person keeps the gate; measure attributes spec dispatches; test log
Preparing worktree (detached HEAD 8b61d65)
HEAD is now at 8b61d65 test log: self-test counts from selftest.out, lines per capability
== B-integrate-1 (integrate)
   cost $0.57, 1 turns, 8 s, tokens in 4, cache write 2075, cache read 31972, out 1615
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   FAIL the changed count line keeps r3  [ids on the count line: ['8']]
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows lend-items' lines with ids r1-r6
   ok   spec/ unchanged
== B-integrate-2 (integrate)
   cost $0.49, 1 turns, 8 s, tokens in 4, cache write 1794, cache read 31908, out 1295
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows lend-items' lines with ids r1-r6
   ok   spec/ unchanged
== B-integrate-3 (integrate)
   cost $0.52, 4 turns (num_turns summed 5 over 2 results), 114 s wall, tokens all models: in 36, cache write 56747, cache read 298354, out 17163
   ok   the gate text is the reply
   FAIL the gate shows keep-items' two added lines with ids  [empty title: [], removal: []]
   FAIL the added lines are r6 and r7, never r3  [empty title: [], removal: []]
   FAIL the changed count line keeps r3  [ids on the count line: []]
   FAIL the gate shows keep-items' removed title-by-id line as r4  [ids on the title-by-id line: []]
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== B-apply-1 (apply)
   cost $0.20, 4 turns (num_turns summed 5 over 2 results), 30 s wall, tokens all models: in 22, cache write 41598, cache read 217539, out 3741
   ok   spec/ committed alone
   ok   the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   ok   the removed line is gone, its id r4 in retired, r5 kept
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== B-apply-2 (apply)
   cost $0.21, 4 turns (num_turns summed 5 over 2 results), 38 s wall, tokens all models: in 26, cache write 42261, cache read 265727, out 4173
   ok   spec/ committed alone
   ok   the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   ok   the removed line is gone, its id r4 in retired, r5 kept
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== B-apply-3 (apply)
   cost $0.19, 4 turns (num_turns summed 5 over 2 results), 29 s wall, tokens all models: in 22, cache write 40555, cache read 213812, out 3558
   ok   spec/ committed alone
   ok   the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   ok   the removed line is gone, its id r4 in retired, r5 kept
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== B-formulate-1 (formulate)
   cost $0.59, 5 turns (num_turns summed 6 over 2 results), 583 s wall, tokens all models: in 58, cache write 90837, cache read 481038, out 15307
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   model check: no v_s1, no v_s2
   ok   model check: no v_s3 for keep-items or lend-items
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== B-formulate-2 (formulate)
   cost $0.57, 5 turns (num_turns summed 6 over 2 results), 97 s wall, tokens all models: in 54, cache write 72603, cache read 503593, out 16168
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   model check: no v_s1, no v_s2
   ok   model check: no v_s3 for keep-items or lend-items
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== B-formulate-3 (formulate)
   cost $0.56, 6 turns (num_turns summed 7 over 2 results), 90 s wall, tokens all models: in 62, cache write 71141, cache read 586530, out 15829
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   model check: no v_s1, no v_s2
   ok   model check: no v_s3 for keep-items or lend-items
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== B-migrate-1 (migrate)
   cost $0.17, 9 turns (num_turns summed 10 over 1 results), 25 s wall, tokens all models: in 18, cache write 27132, cache read 285100, out 2941
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is <context>/keep-items, retired: []
   ok   spec/index.md's id is the context id
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   ok   model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)
   ok   spec/ and features/ committed in one commit
== B-migrate-2 (migrate)
   cost $0.17, 8 turns (num_turns summed 9 over 1 results), 25 s wall, tokens all models: in 16, cache write 28182, cache read 253081, out 2906
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is <context>/keep-items, retired: []
   ok   spec/index.md's id is the context id
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   ok   model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)
   FAIL spec/ and features/ committed in one commit  [25ab91b: features/keep-items.feature; d57aa99: spec/capabilities/keep-items.md spec/index.md]
== B-migrate-3 (migrate)
   cost $0.15, 7 turns (num_turns summed 8 over 1 results), 21 s wall, tokens all models: in 14, cache write 26181, cache read 211286, out 2344
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is <context>/keep-items, retired: []
   ok   spec/index.md's id is the context id
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   ok   model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)
   ok   spec/ and features/ committed in one commit
== B-noclingo-1 (noclingo)
   cost $0.59, 6 turns (num_turns summed 7 over 2 results), 108 s wall, tokens all models: in 64, cache write 72566, cache read 593659, out 17389
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
   ok   the reply says model check did not run
== B-noclingo-2 (noclingo)
   cost $0.53, 6 turns (num_turns summed 7 over 2 results), 110 s wall, tokens all models: in 62, cache write 67550, cache read 607836, out 15686
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
   ok   the reply says model check did not run
== B-noclingo-3 (noclingo)
   cost $0.59, 5 turns (num_turns summed 6 over 2 results), 111 s wall, tokens all models: in 64, cache write 72016, cache read 568969, out 17250
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
   ok   the reply says model check did not run
== A-integrate-1 (integrate)
   cost $0.52, 4 turns (num_turns summed 5 over 2 results), 107 s wall, tokens all models: in 36, cache write 57026, cache read 282319, out 16691
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== A-integrate-2 (integrate)
   cost $0.48, 4 turns (num_turns summed 5 over 2 results), 102 s wall, tokens all models: in 36, cache write 51769, cache read 285251, out 15947
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== A-formulate-1 (formulate)
   cost $0.63, 5 turns (num_turns summed 6 over 2 results), 111 s wall, tokens all models: in 64, cache write 73048, cache read 551492, out 19334
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   FAIL lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7  [lend-items ['r1', 'r2', 'r3', 'r5', 'r6'], keep-items ['r1', 'r2', 'r3', 'r6', 'r7']]
   ok   model check: no v_s1, no v_s2
   FAIL model check: no v_s3 for keep-items or lend-items  [missingmass.io/demo/shelf/lend-items#r4]
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== A-formulate-2 (formulate)
   cost $0.65, 5 turns (num_turns summed 6 over 2 results), 558 s wall, tokens all models: in 56, cache write 90755, cache read 482653, out 18145
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   FAIL lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7  [lend-items ['r1', 'r2', 'r3', 'r4', 'r6'], keep-items ['r1', 'r2', 'r3', 'r6']]
   ok   model check: no v_s1, no v_s2
   FAIL model check: no v_s3 for keep-items or lend-items  [missingmass.io/demo/shelf/keep-items#r7; missingmass.io/demo/shelf/lend-items#r5]
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
5
scores: /home/vscode/scratch/shopsystem-bdd/ids/scores.txt
~~~~~~
