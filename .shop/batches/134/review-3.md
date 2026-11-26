---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-134/review-3
kind: review
batch: batch-134
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/157
head: 2d33a3099563c074674754d7e03ccf32865581f2
range: d45e833f9c16f1db615076b9ead1215d3d6581de..2d33a3099563c074674754d7e03ccf32865581f2
result: clean
---

# batch-134 review 3

## Verdict

The fix is right and f1 is fixed. b735 now has a line for the behaviour, decisions#r26 (group g26). The commit narrows `retired_history` to what that line says: only a decision whose status is `superseded` may name a requirement id that its capability retired. A `rejected` decision's retired id is again an unresolved reference, as it was before the batch. The test was changed to match: the `superseded` case still passes clean, and `rejected` was moved into the parametrized "unresolved" test next to `accepted`. That is a tighter assertion, not a weaker one. decisions#r26 is no longer in `unbuilt:` (`unbuilt: []`), and its scenario `@g26 @r26` is in features/decisions.feature. Every run in `## Runs` exits 0, as it did at the base. The change is 2 files, +11 -11, under the limit.

## Findings

None.

## Earlier findings
- f1: fixed
