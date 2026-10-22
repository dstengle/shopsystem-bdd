---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-17-0-19-0-type-first-ids-fixture-scores
kind: measurement
about: [capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration, capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration]
date: 2026-10-17
---

# 0.19.0 type-first ids: fixture scores before the scorer fixes

Scores of the 0.19.0 type-first ids reruns (2026-10-17): T-integrate and T-migrate, three runs each, plugin B a detached worktree at `1a7b92a`. These are the scores before the two scorer fixes (a bold label with trailing text; the gate read from the last message holding `[rN]` under a label): T-integrate shows FAILs that the test log's "Type-first ids" section (`2026-10-16-requirement-ids-test-log.md`) reports as 7/7 after rescoring; the rescored output itself is not in scratch. The gate texts of these runs are in `2026-10-17-ids-integrate-gate-texts`.

Archived from git-ignored scratch; each file's text as it was.

## `/home/vscode/scratch/shopsystem-bdd/ids/scores-typefirst.txt`

~~~~~~
T-integrate-1 ok=6 FAIL=1 | cost $0.58, 4 turns (num_turns summed 5 
   FAIL the gate shows keep-items' removed title-by-id line as r4  [title-by-id line: ('4', 'added')]
T-integrate-2 ok=2 FAIL=5 | cost $0.53, 5 turns (num_turns summed 6 
   FAIL the gate shows keep-items' two added lines with ids  [empty title: (None, None), removal: (None, None)]
   FAIL the added lines are r6 and r7, never r3  [empty title: (None, None), removal: (None, None)]
   FAIL the changed count line keeps r3  [count line: (None, None)]
   FAIL the gate shows keep-items' removed title-by-id line as r4  [title-by-id line: (None, None)]
   FAIL the gate shows the new capability's lines with ids r1-r6  [lending; ids on added lending lines: []]
T-integrate-3 ok=6 FAIL=1 | cost $0.48, 4 turns (num_turns summed 5 
   FAIL the gate shows keep-items' removed title-by-id line as r4  [title-by-id line: ('4', 'added')]
T-migrate-1 ok=13 FAIL=0 | cost $0.18, 10 turns (num_turns summed 1
T-migrate-2 ok=13 FAIL=0 | cost $0.16, 8 turns (num_turns summed 9 
T-migrate-3 ok=13 FAIL=0 | cost $0.18, 10 turns (num_turns summed 1
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/rerun.log`

~~~~~~
== T-integrate-1 (integrate)
   cost $0.58, 4 turns (num_turns summed 5 over 2 results), 119 s wall, tokens all models: in 34, cache write 69581, cache read 272898, out 18727
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   FAIL the gate shows keep-items' removed title-by-id line as r4  [title-by-id line: ('4', 'added')]
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== T-integrate-2 (integrate)
   cost $0.53, 5 turns (num_turns summed 6 over 3 results), 104 s wall, tokens all models: in 36, cache write 60377, cache read 291529, out 16756
   ok   the gate text is the reply
   FAIL the gate shows keep-items' two added lines with ids  [empty title: (None, None), removal: (None, None)]
   FAIL the added lines are r6 and r7, never r3  [empty title: (None, None), removal: (None, None)]
   FAIL the changed count line keeps r3  [count line: (None, None)]
   FAIL the gate shows keep-items' removed title-by-id line as r4  [title-by-id line: (None, None)]
   FAIL the gate shows the new capability's lines with ids r1-r6  [lending; ids on added lending lines: []]
   ok   spec/ unchanged
== T-integrate-3 (integrate)
   cost $0.48, 4 turns (num_turns summed 5 over 2 results), 105 s wall, tokens all models: in 34, cache write 55248, cache read 280913, out 15774
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   FAIL the gate shows keep-items' removed title-by-id line as r4  [title-by-id line: ('4', 'added')]
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== T-migrate-1 (migrate)
   cost $0.18, 10 turns (num_turns summed 12 over 1 results), 27 s wall, tokens all models: in 20, cache write 28620, cache read 330071, out 3335
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is capability/<context path>/keep-items, retired: []
   ok   spec/index.md's id is bounded-context/<context path>
   ok   every decision/ reference and ledger heading rewritten to design-decision/
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   ok   model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)
   ok   spec/ and features/ committed in one commit
== T-migrate-2 (migrate)
   cost $0.16, 8 turns (num_turns summed 9 over 1 results), 24 s wall, tokens all models: in 16, cache write 26943, cache read 249775, out 2647
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is capability/<context path>/keep-items, retired: []
   ok   spec/index.md's id is bounded-context/<context path>
   ok   every decision/ reference and ledger heading rewritten to design-decision/
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   ok   model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)
   ok   spec/ and features/ committed in one commit
== T-migrate-3 (migrate)
   cost $0.18, 10 turns (num_turns summed 11 over 1 results), 28 s wall, tokens all models: in 20, cache write 28087, cache read 328447, out 3163
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is capability/<context path>/keep-items, retired: []
   ok   spec/index.md's id is bounded-context/<context path>
   ok   every decision/ reference and ledger heading rewritten to design-decision/
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   ok   model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)
   ok   spec/ and features/ committed in one commit
~~~~~~
