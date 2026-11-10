---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-21/review-2
kind: review
batch: batch-21
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/34
head: 37f9145dc1f8f874566b63310a4320219859b0b0
range: b5d907198c7c101fc24af6b501b0a86653c0ac58..37f9145dc1f8f874566b63310a4320219859b0b0
result: clean
---

# batch-21 review 2

## Verdict

Both fixes are right. Each one only adds parentheses around the joined strings or drops a `noqa`, so no string value changes. `tools check` now exits 0 at the head, and every other run exits 0 too. Nothing new to fix.

## Findings

None.

## Earlier findings
- f1: fixed
- f2: fixed
