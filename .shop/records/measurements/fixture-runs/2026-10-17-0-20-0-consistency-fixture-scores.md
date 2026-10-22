---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-17-0-20-0-consistency-fixture-scores
kind: measurement
about: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency
date: 2026-10-17
---

# 0.20.0 consistency checking: fixture scores and costs

Scores and costs of the 0.20.0 consistency fixture runs (2026-10-17): U-consistency-report and U-consistency-fix, three runs each, plugin B at `73ee3fb`. `run-020.log` is the run output; `scores-020.txt` the summary. Fix-1's FAIL on r7 was a scorer error (it rejected any "too many"); the test log `2026-10-17-ubiquitous-language-test-log.md` reports fix-1 rescored ok after the fix, 3/3 report and 3/3 fix.

Archived from git-ignored scratch; each file's text as it was.

## `/home/vscode/scratch/shopsystem-bdd/ids/scores-020.txt`

~~~~~~
U-consistency-report-1 ok=5 FAIL=0 | cost $0.29, 8 turns (num_turns summed 11 over
U-consistency-report-2 ok=5 FAIL=0 | cost $0.29, 8 turns (num_turns summed 11 over
U-consistency-report-3 ok=5 FAIL=0 | cost $0.29, 8 turns (num_turns summed 11 over
U-consistency-fix-1 ok=7 FAIL=1 | cost $0.47, 20 turns (num_turns summed 23 ove
   FAIL lend-items#r7 takes reading A, more than 3 books  [If the reader lends a book to a friend who has more than 3 books, the shelf refuses the loan because the friend has too many books.]
U-consistency-fix-2 ok=8 FAIL=0 | cost $0.42, 16 turns (num_turns summed 19 ove
U-consistency-fix-3 ok=8 FAIL=0 | cost $0.54, 22 turns (num_turns summed 29 ove
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/run-020.log`

~~~~~~
== U-consistency-report-1 (consistency-report)
   cost $0.29, 8 turns (num_turns summed 11 over 1 results), 41 s wall, tokens all models: in 36, cache write 50127, cache read 304130, out 8954
   ok   findings name volume and book together (one thing, two words)
   ok   findings name keep-items' r3 scenario that drifts from its line
   ok   findings name lend-items#r7, the line with two readings
   ok   spec/ and features/ unchanged
   ok   no commit
== U-consistency-report-2 (consistency-report)
   cost $0.29, 8 turns (num_turns summed 11 over 1 results), 42 s wall, tokens all models: in 38, cache write 47056, cache read 317989, out 9364
   ok   findings name volume and book together (one thing, two words)
   ok   findings name keep-items' r3 scenario that drifts from its line
   ok   findings name lend-items#r7, the line with two readings
   ok   spec/ and features/ unchanged
   ok   no commit
== U-consistency-report-3 (consistency-report)
   cost $0.29, 8 turns (num_turns summed 11 over 1 results), 42 s wall, tokens all models: in 36, cache write 47312, cache read 308054, out 9730
   ok   findings name volume and book together (one thing, two words)
   ok   findings name keep-items' r3 scenario that drifts from its line
   ok   findings name lend-items#r7, the line with two readings
   ok   spec/ and features/ unchanged
   ok   no commit
== U-consistency-fix-1 (consistency-fix)
   cost $0.47, 20 turns (num_turns summed 23 over 1 results), 86 s wall, tokens all models: in 60, cache write 63972, cache read 952830, out 14373
   ok   the glossary avoids volume under book
   ok   no line or scenario says volume
   ok   model check: no v_t row, 0 unresolved, 0 file problems, no new violation
   ok   line ids kept, no renumbering, no other line changed
   FAIL lend-items#r7 takes reading A, more than 3 books  [If the reader lends a book to a friend who has more than 3 books, the shelf refuses the loan because the friend has too many books.]
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   ok   suite passes
   ok   the commits name the term change (volume)
== U-consistency-fix-2 (consistency-fix)
   cost $0.42, 16 turns (num_turns summed 19 over 1 results), 79 s wall, tokens all models: in 52, cache write 60884, cache read 722389, out 13084
   ok   the glossary avoids volume under book
   ok   no line or scenario says volume
   ok   model check: no v_t row, 0 unresolved, 0 file problems, no new violation
   ok   line ids kept, no renumbering, no other line changed
   ok   lend-items#r7 takes reading A, more than 3 books
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   ok   suite passes
   ok   the commits name the term change (volume)
== U-consistency-fix-3 (consistency-fix)
   cost $0.54, 22 turns (num_turns summed 29 over 1 results), 108 s wall, tokens all models: in 66, cache write 71198, cache read 1154294, out 16497
   ok   the glossary avoids volume under book
   ok   no line or scenario says volume
   ok   model check: no v_t row, 0 unresolved, 0 file problems, no new violation
   ok   line ids kept, no renumbering, no other line changed
   ok   lend-items#r7 takes reading A, more than 3 books
   ok   keep-items' r3 scenario reworded to its line (the number of books)
   ok   suite passes
   ok   the commits name the term change (volume)
~~~~~~
