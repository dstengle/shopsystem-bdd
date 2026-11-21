---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-64/review-2
kind: review
batch: batch-64
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/88
head: fb3a223d704e5f1c51b949a1b842aa4f3f9a1c62
range: 3550423ee4888ed5da231a6dd02a29fd43622d72..fb3a223d704e5f1c51b949a1b842aa4f3f9a1c62
result: clean
---

# batch-64 review 2

## Verdict

The fix moves the review-limit check after the bar-alone check. An item that fails the bar alone now goes back to `shaped` whatever its estimate, as batches#r54 requires. The fix also adds a test that would have failed before it. Every run in `## Runs` exits 0, and the change is 3 files, +21 -6, well within the 1000-line limit. No new findings.

## Findings

None.

## Earlier findings
- f1: fixed
