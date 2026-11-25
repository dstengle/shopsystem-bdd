---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-102/review-2
kind: review
batch: batch-102
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/125
head: c9e63ceb961b1fa65f2c70446685e162128f84bf
range: 0747dc91ccd73b229fe528fbcc5245c4213b1e73..c9e63ceb961b1fa65f2c70446685e162128f84bf
result: clean
---

# batch-102 review 2

## Verdict

The fix for f1 is correct. `_read` now collects a contract's terms in `own` and adds them to `taken` only after the whole contract is read. Several senses of one word in one contract are all kept, and a term is still a clash when it matches a pack's term, the adapter spec's own, or an earlier contract's. The new unit cases cover both: two `status (attribute of …)` lines kept, and a word of an earlier contract clashing with a later one. Every run exits 0, the size is within the limit, and no test was removed or weakened. No new findings.

## Findings

None.

## Earlier findings
- f1: fixed
