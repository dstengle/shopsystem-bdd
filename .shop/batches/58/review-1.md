---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-58/review-1
kind: review
batch: batch-58
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/82
head: 63e1affa522e6df2ceb20b2a74e24385772b4826
range: bd0e7a572d2c31660130daf7efccc4a441c7e2ee..63e1affa522e6df2ceb20b2a74e24385772b4826
result: clean
---

# batch-58 review 1

## Verdict

The batch does what both chores ask. b439 compiles ContextSteps over grammar 4's compiled .gf and .gfo files, under a lock of the sha, and its test checks that the PGF is byte-identical to a compile from scratch. b430 makes the readiness bar faster. It holds the copy's state so the inputs are statted once and each line is parsed once. It keeps the result before the lay on disk, parses the lay's misses side by side, and runs no annotate, L2 or L8, as decision 0112 allows. I checked whether the bar's reasons could change. Removing L2 and L8 changes nothing it reports, because `_logic` only ever reported L0, L1 and L3. Excluding v_a5 and v_a6 matches the annotate it no longer runs. Every spec write inside the held scope goes through `lay_onto`, which drops the held state. The result kept on disk loses nothing on the way back, since violations are `(name, tuple(str))` and come back as the same tuples. No test was removed or weakened: the counts in test_decision_checks rise for decision 0112. No `.feature` file changed, every run exits 0, each commit touches only its chore's files, and the change is 819 lines against a limit of 1000. Nothing to fix now.

## Findings

### f1 Minor observation: the v_a5/v_a6 exclusion is written to hide from the rule catalogue's search
- item: b430
- where: scripts/readiness_bar.py:73
Commit c6cc73293 changed `"v_a5", "v_a6"` to `{"v_a%d" % n for n in (5, 6)}`. It did this only so that `spec rules --write` would not list readiness_bar.py as where those rules are implemented. The behaviour is the same, but now nobody who searches for `v_a5` finds that the bar skips it, and the catalogue's way of finding where a rule is implemented has been dodged rather than taught to tell an exclusion apart. A cleaner fix: let model_rules ignore a rule code that appears in an exclusion set, or name the exclusion in the catalogue's entry for v_a5 and v_a6.

### f2 Minor observation: the docs promise a timing that no test checks
- item: b430
- where: docs/recipes.md:81
The new text says `work ready` "answers in a second or two" after the first run, and takes "under a minute on a large" spec after a new word. test_readiness_speed.py checks stand-in measures (stat calls, parse calls, cache reads), not elapsed time, so nothing catches the claim if it stops being true. Either reword it without figures ("much faster after the first run") or back it with a timing guard like the one test_grammar4_guards.py uses.
