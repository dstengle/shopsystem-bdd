---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-101/review-2
kind: review
batch: batch-101
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/124
head: 3d3d74dde3fbfd7bdaefc95a1f5154765be71264
range: f707a216ded6885b49941d801d5b23fbc0aec519..3d3d74dde3fbfd7bdaefc95a1f5154765be71264
result: clean
---

# batch-101 review 2

## Verdict

The fix clears f1. In tests/scenarios/batches_handlers_added.py the two requirement texts are now bound to the names `ARCHIVED` and `FILED`. Each reads the same as its old implicit concatenation. The model line `HEADER` with `MEMBER` is now joined by an f-string, which gives the same string as the old static join. `tools check --base c399894e9` now exits 0, as it did at the base, and every other run exits 0 at `Head:` too. The change is one file, +4 -5, well under the limit. It adds no behaviour, removes no test and loosens no assertion.

## Findings

None.

## Earlier findings
- f1: fixed
