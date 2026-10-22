---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-17-ids-harness-selftest
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-17
---

# Fixture harness self-test output (ids)

The fixture harness's self-test output (`selftest.sh`, no model), as last run on 2026-10-17 18:33 with the 0.20.0 consistency cases included: fresh fixtures fail what a run must achieve, hand-made correct results (`test-done-*`, `test-ok-*`) pass every check, and each mutation (`test-mut-*`) fails the check meant for it. The 0.19.0 test log cites its ok counts. The hand-made fixtures' run directories are listed in `2026-10-16-ids-runs/`.

Archived from `/home/vscode/scratch/shopsystem-bdd/ids/selftest.out` (git-ignored scratch), text as it was.

---

== test-fresh-integrate (integrate)
   cost: no result event in transcript.jsonl
   FAIL the gate text is the reply
   FAIL the gate shows keep-items' two added lines with ids  [empty title: (None, None), removal: (None, None)]
   FAIL the added lines are r6 and r7, never r3  [empty title: (None, None), removal: (None, None)]
   FAIL the changed count line keeps r3  [count line: (None, None)]
   FAIL the gate shows keep-items' removed title-by-id line as r4  [title-by-id line: (None, None)]
   FAIL the gate shows the new capability's lines with ids r1-r6  [lend-items; ids on added lending lines: []]
   ok   spec/ unchanged
== test-fresh-apply (apply)
   cost: no result event in transcript.jsonl
   FAIL spec/ committed alone  [no commit touches spec/]
   FAIL the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   FAIL the apply committed without restoring spec/
   FAIL no line renumbered  [r1: When the reader adds a book, the shelf h; r2: If the reader adds a book whose title th; r3: When the reader asks how many books ther; r4: When the reader asks for the title of a ]
   FAIL the removed line is gone, its id r4 in retired, r5 kept  [retired:  [r5]; r4: When the reader asks for the title of a book by its id, the shelf answers with the title.]
   FAIL model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit  [0 violations, 1 warnings, 0 unresolved references, 0 file problems]
   FAIL the drafts applied as written
== test-fresh-formulate (formulate)
   cost: no result event in transcript.jsonl
   FAIL features committed
   ok   every scenario not @holding has one @r<n> tag
   FAIL lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7  [lend-items [], keep-items ['r1', 'r2', 'r3', 'r4']]
   FAIL model check: no v_s1, no v_s2  [features/keep-items.feature:The shelf answers with the title of a book asked for by its id]
   FAIL model check: no v_s3 for keep-items or lend-items  [capability/missingmass.io/demo/shelf/keep-items#r6; capability/missingmass.io/demo/shelf/keep-items#r7; capability/missingmass.io/demo/shelf/lend-items#r1; capability/missingmass.io/demo/shelf/lend-items#r2; capability/missingmass.io/demo/shelf/lend-items#r3; capability/missingmass.io/demo/shelf/len]
   FAIL the removed line's scenario (keep-items r4) is removed or held  [The shelf answers with the title of a book asked for by its id ['@slice-2', '@r4']]
   FAIL the held count scenario keeps @r3 and @holding  [The shelf answers with the number of books it holds ['@slice-1', '@r3']]
   ok   suite passes
== test-fresh-noclingo (noclingo)
   cost: no result event in transcript.jsonl
   FAIL features committed
   ok   every scenario not @holding has one @r<n> tag
   FAIL lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7  [lend-items [], keep-items ['r1', 'r2', 'r3', 'r4']]
   FAIL the removed line's scenario (keep-items r4) is removed or held  [The shelf answers with the title of a book asked for by its id ['@slice-2', '@r4']]
   FAIL the held count scenario keeps @r3 and @holding  [The shelf answers with the number of books it holds ['@slice-1', '@r3']]
   ok   suite passes
   FAIL the reply says model check did not run
== test-fresh-migrate (migrate)
   cost: no result event in transcript.jsonl
   FAIL every line has [r<n>] from r1 in order  [rNone rNone rNone rNone]
   ok   line text otherwise unchanged
   FAIL capability id is capability/<context path>/keep-items, retired: []  [id: capability/keep-items retired:None]
   FAIL spec/index.md's id is bounded-context/<context path>  [id: shelf]
   FAIL every decision/ reference and ledger heading rewritten to design-decision/  [spec/capabilities/keep-items.md: rests_on: [decision/books-kept-in-one-file]; spec/decisions.md: ## decision/books-kept-in-one-file]
   FAIL every scenario not @holding has one @r<n> tag  [A book added is held under an id made from its title; A book whose title is already held is refused as a duplicate; The shelf answers with the number of books it holds; The shelf answers with the title of a book asked for by its id]
   ok   no @r on a Feature: line
   FAIL the outline tagged once  [[('A book added is held under an id made from its title', ['@slice-1'], [])]]
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   FAIL model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)  [12 violations, 1 warnings, 1 unresolved references, 2 file problems]
   FAIL spec/ and features/ committed in one commit
== test-done-integrate (integrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== test-done-apply (apply)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   spec/ committed alone
   ok   the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   ok   the removed line is gone, its id r4 in retired, r5 kept
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== test-done-formulate (formulate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   model check: no v_s1, no v_s2
   ok   model check: no v_s3 for keep-items or lend-items
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== test-done-noclingo (noclingo)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
   ok   the reply says model check did not run
== test-done-migrate (migrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
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
== test-mut-noclingo-unformulated (noclingo)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   FAIL lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7  [lend-items [], keep-items ['r1', 'r2', 'r3', 'r6', 'r7']]
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
   ok   the reply says model check did not run
== test-mut-formulate-lend-v_s3 (formulate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   FAIL lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7  [lend-items ['r1', 'r2', 'r3', 'r4', 'r5'], keep-items ['r1', 'r2', 'r3', 'r6', 'r7']]
   ok   model check: no v_s1, no v_s2
   FAIL model check: no v_s3 for keep-items or lend-items  [capability/missingmass.io/demo/shelf/lend-items#r6]
   ok   the removed line's scenario (keep-items r4) is removed or held
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== test-mut-apply-message (apply)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   spec/ committed alone
   FAIL the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4  [spec: lending-design, lines approved 2026-10-16; adds lend-items#r1-r6, keep-items#r6-r7; changes lend-items#r3; removes keep-items#r4]
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   ok   the removed line is gone, its id r4 in retired, r5 kept
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== test-mut-apply-no-removes (apply)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   spec/ committed alone
   FAIL the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4  [spec: lending-design, lines approved 2026-10-16; adds lend-items#r1-r6, keep-items#r6-r7; changes keep-items#r3]
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   ok   the removed line is gone, its id r4 in retired, r5 kept
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== test-mut-apply-not-retired (apply)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   spec/ committed alone
   ok   the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   FAIL the removed line is gone, its id r4 in retired, r5 kept  [retired:  [r5]; r4: None]
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== test-mut-apply-line-kept (apply)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   spec/ committed alone
   ok   the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   ok   the apply committed without restoring spec/
   ok   no line renumbered
   FAIL the removed line is gone, its id r4 in retired, r5 kept  [retired:  [r5]; r4: When the reader asks for the title of a book by its id, the shelf answers with the title.]
   FAIL model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit  [8 violations, 2 warnings, 0 unresolved references, 0 file problems]
   FAIL the drafts applied as written
== test-mut-apply-restored (apply)
   cost $1.23, 2 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   spec/ committed alone
   ok   the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4
   FAIL the apply committed without restoring spec/  [git checkout -- spec/ && rm spec/capabilities/lend-items.md]
   ok   no line renumbered
   ok   the removed line is gone, its id r4 in retired, r5 kept
   ok   model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit
   ok   the drafts applied as written
== test-mut-formulate-r4-left (formulate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   features committed
   ok   every scenario not @holding has one @r<n> tag
   ok   lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7
   FAIL model check: no v_s1, no v_s2  [features/keep-items.feature:The shelf answers with the title of a book asked for by its id]
   ok   model check: no v_s3 for keep-items or lend-items
   FAIL the removed line's scenario (keep-items r4) is removed or held  [The shelf answers with the title of a book asked for by its id ['@slice-2', '@r4']]
   ok   the held count scenario keeps @r3 and @holding
   ok   suite passes
== test-mut-integrate-no-removal (integrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   FAIL the gate shows keep-items' removed title-by-id line as r4  [title-by-id line: (None, None)]
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
keep-items:
- r6 added (r5 is retired): If the reader adds a book whose title is empty, the shelf refuses the add because the title is empty.
### keep-items r7 (added)
When the reader removes a book the shelf holds, the shelf no longer holds it.

## Changed

keep-items:
- keep-items r3 changed, keeping its id: When the reader asks how many books there are, the shelf answers with the number of books on the shelf, leaving out any that are lent.
  was: When the reader asks how many books there are, the shelf answers with the number of books it holds.

## Removed
== test-ok-integrate-forms (integrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== test-mut-integrate-renumbered (integrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   FAIL the added lines are r6 and r7, never r3  [empty title: ('3', 'added'), removal: ('7', 'added')]
   FAIL the changed count line keeps r3  [count line: ('4', 'changed')]
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== test-mut-migrate-index (migrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is capability/<context path>/keep-items, retired: []
   FAIL spec/index.md's id is bounded-context/<context path>  [id: shelf]
   ok   every decision/ reference and ledger heading rewritten to design-decision/
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   FAIL model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)  [0 violations, 1 warnings, 0 unresolved references, 1 file problems]
   FAIL spec/ and features/ committed in one commit  [6e78fb7: spec/index.md; 663cf9b: features/keep-items.feature spec/capabilities/keep-items.md spec/decisions.md spec/index.md]
== test-mut-migrate-two-commits (migrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
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
   FAIL spec/ and features/ committed in one commit  [6a896f1: features/keep-items.feature; 0ecb9b1: spec/capabilities/keep-items.md spec/decisions.md spec/index.md]
== test-ok-integrate-wasnow (integrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== test-mut-integrate-wasnow-r8 (integrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   FAIL the changed count line keeps r3  [count line: ('8', 'changed')]
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== test-ok-integrate-labels (integrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== test-mut-migrate-old-decision (migrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   every line has [r<n>] from r1 in order
   ok   line text otherwise unchanged
   ok   capability id is capability/<context path>/keep-items, retired: []
   ok   spec/index.md's id is bounded-context/<context path>
   FAIL every decision/ reference and ledger heading rewritten to design-decision/  [spec/decisions.md: ## decision/books-kept-in-one-file]
   ok   every scenario not @holding has one @r<n> tag
   ok   no @r on a Feature: line
   ok   the outline tagged once
   ok   the held scenario keeps @holding and takes no @r<n>
   ok   features count --by-tag equals the baseline's but for r tags
   ok   the suite's summary unchanged
   FAIL model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem)  [0 violations, 1 warnings, 1 unresolved references, 1 file problems]
   FAIL spec/ and features/ committed in one commit  [a2fb60c: spec/decisions.md; 663cf9b: features/keep-items.feature spec/capabilities/keep-items.md spec/decisions.md spec/index.md]
== test-ok-integrate-bold-label (integrate)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== test-ok-integrate-late-message (integrate)
   cost $1.23, 2 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the gate text is the reply
   ok   the gate shows keep-items' two added lines with ids
   ok   the added lines are r6 and r7, never r3
   ok   the changed count line keeps r3
   ok   the gate shows keep-items' removed title-by-id line as r4
   ok   the gate shows the new capability's lines with ids r1-r6
   ok   spec/ unchanged
== test-fresh-consistency-report (consistency-report)
   cost: no result event in transcript.jsonl
   FAIL findings name volume and book together (one thing, two words)
   FAIL findings name keep-items' r3 scenario that drifts from its line
   FAIL findings name lend-items#r7, the line with two readings
   ok   spec/ and features/ unchanged
   ok   no commit
== test-fresh-consistency-fix (consistency-fix)
   cost: no result event in transcript.jsonl
   FAIL the glossary avoids volume under book  [- **book**: an item the shelf holds. Not: item.]
   FAIL no line or scenario says volume  [features/lend-items.feature: Scenario: Lending a volume the shelf does not hold is refused; features/lend-items.feature: When the reader lends the volume "Dune" to "Ann"; features/lend-items.feature: Then the loan is refused because the volume is not held; spec/capabilities/lend-items.md: - [r3] If ]
   ok   model check: no v_t row, 0 unresolved, 0 file problems, no new violation
   ok   line ids kept, no renumbering, no other line changed
   FAIL lend-items#r7 takes reading A, more than 3 books  [If the reader lends a book to a friend who has too many books, the shelf refuses the loan because the friend has too many books.]
   FAIL keep-items' r3 scenario reworded to its line (the number of books)  [The shelf answers with the titles of the books on the shelf]
   ok   suite passes
   FAIL the commits name the term change (volume)  [no commit]
== test-done-consistency-report (consistency-report)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   findings name volume and book together (one thing, two words)
   ok   findings name keep-items' r3 scenario that drifts from its line
   ok   findings name lend-items#r7, the line with two readings
   ok   spec/ and features/ unchanged
   ok   no commit
== test-mut-consistency-report-no-a (consistency-report)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   FAIL findings name volume and book together (one thing, two words)
   ok   findings name keep-items' r3 scenario that drifts from its line
   ok   findings name lend-items#r7, the line with two readings
   ok   spec/ and features/ unchanged
   ok   no commit
== test-mut-consistency-report-no-b (consistency-report)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   findings name volume and book together (one thing, two words)
   FAIL findings name keep-items' r3 scenario that drifts from its line
   ok   findings name lend-items#r7, the line with two readings
   ok   spec/ and features/ unchanged
   ok   no commit
== test-mut-consistency-report-no-c (consistency-report)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   findings name volume and book together (one thing, two words)
   ok   findings name keep-items' r3 scenario that drifts from its line
   FAIL findings name lend-items#r7, the line with two readings
   ok   spec/ and features/ unchanged
   ok   no commit
== test-mut-consistency-report-spec-edited (consistency-report)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   findings name volume and book together (one thing, two words)
   ok   findings name keep-items' r3 scenario that drifts from its line
   ok   findings name lend-items#r7, the line with two readings
   FAIL spec/ and features/ unchanged  [M spec/capabilities/lend-items.md]
   ok   no commit
== test-mut-consistency-report-committed (consistency-report)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   findings name volume and book together (one thing, two words)
   ok   findings name keep-items' r3 scenario that drifts from its line
   ok   findings name lend-items#r7, the line with two readings
   ok   spec/ and features/ unchanged
   FAIL no commit  [plan: findings noted]
== test-done-consistency-fix (consistency-fix)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the glossary avoids volume under book
   ok   no line or scenario says volume
   ok   model check: no v_t row, 0 unresolved, 0 file problems, no new violation
   ok   line ids kept, no renumbering, no other line changed
   ok   lend-items#r7 takes reading A, more than 3 books
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   ok   suite passes
   ok   the commits name the term change (volume)
== test-mut-consistency-fix-glossary (consistency-fix)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   FAIL the glossary avoids volume under book  [- **book**: an item the shelf holds. Not: item.]
   ok   no line or scenario says volume
   ok   model check: no v_t row, 0 unresolved, 0 file problems, no new violation
   ok   line ids kept, no renumbering, no other line changed
   ok   lend-items#r7 takes reading A, more than 3 books
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   ok   suite passes
   ok   the commits name the term change (volume)
== test-mut-consistency-fix-volume-left (consistency-fix)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the glossary avoids volume under book
   FAIL no line or scenario says volume  [features/lend-items.feature: Scenario: Lending a volume the shelf does not hold is refused]
   FAIL model check: no v_t row, 0 unresolved, 0 file problems, no new violation  [v_t1]
   ok   line ids kept, no renumbering, no other line changed
   ok   lend-items#r7 takes reading A, more than 3 books
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   ok   suite passes
   ok   the commits name the term change (volume)
== test-mut-consistency-fix-unresolved (consistency-fix)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the glossary avoids volume under book
   ok   no line or scenario says volume
   FAIL model check: no v_t row, 0 unresolved, 0 file problems, no new violation  [0 violations, 2 warnings, 1 unresolved references, 0 file problems]
   ok   line ids kept, no renumbering, no other line changed
   ok   lend-items#r7 takes reading A, more than 3 books
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   ok   suite passes
   ok   the commits name the term change (volume)
== test-mut-consistency-fix-renumbered (consistency-fix)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the glossary avoids volume under book
   ok   no line or scenario says volume
   FAIL model check: no v_t row, 0 unresolved, 0 file problems, no new violation  [v_s1: features/lend-items.feature:Lending to a friend who has more than 3 books is refused; v_s3: capability/missingmass.io/demo/shelf/lend-items#r8]
   FAIL line ids kept, no renumbering, no other line changed  [lend-items ids [1, 2, 3, 4, 5, 6, 8], were [1, 2, 3, 4, 5, 6, 7]; lend-items#r8 reworded]
   FAIL lend-items#r7 takes reading A, more than 3 books
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   ok   suite passes
   ok   the commits name the term change (volume)
== test-mut-consistency-fix-reading (consistency-fix)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the glossary avoids volume under book
   ok   no line or scenario says volume
   ok   model check: no v_t row, 0 unresolved, 0 file problems, no new violation
   ok   line ids kept, no renumbering, no other line changed
   FAIL lend-items#r7 takes reading A, more than 3 books  [If the reader lends a book to a friend who already has more than 5 books, the shelf refuses the loan because the friend has more than 5 books.]
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   ok   suite passes
   ok   the commits name the term change (volume)
== test-mut-consistency-fix-drift-kept (consistency-fix)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the glossary avoids volume under book
   ok   no line or scenario says volume
   ok   model check: no v_t row, 0 unresolved, 0 file problems, no new violation
   ok   line ids kept, no renumbering, no other line changed
   ok   lend-items#r7 takes reading A, more than 3 books
   FAIL keep-items' r3 scenario reworded to its line (the number of books)  [The shelf answers with the titles of the books on the shelf]
   ok   suite passes
   ok   the commits name the term change (volume)
== test-mut-consistency-fix-suite-red (consistency-fix)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the glossary avoids volume under book
   ok   no line or scenario says volume
   ok   model check: no v_t row, 0 unresolved, 0 file problems, no new violation
   ok   line ids kept, no renumbering, no other line changed
   ok   lend-items#r7 takes reading A, more than 3 books
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   FAIL suite passes  [1 failed, 1 passed in 0.11s]
   ok   the commits name the term change (volume)
== test-mut-consistency-fix-message (consistency-fix)
   cost $1.23, 1 turns (num_turns summed 10 over 2 results), 121 s wall, tokens all models: in 10, cache write 2000, cache read 50000, out 3000
   ok   the glossary avoids volume under book
   ok   no line or scenario says volume
   ok   model check: no v_t row, 0 unresolved, 0 file problems, no new violation
   ok   line ids kept, no renumbering, no other line changed
   ok   lend-items#r7 takes reading A, more than 3 books
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   ok   suite passes
   FAIL the commits name the term change (volume)  [spec, features: fix mode applied]
