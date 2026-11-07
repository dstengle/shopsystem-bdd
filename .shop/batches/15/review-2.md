---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-15/review-2
kind: review
batch: batch-15
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/28
head: 159205468cbbfe99fc318786ab9bff1d4c803e00
range: 78041d895cea7ab340ff43436e91e0f6ca68ed51..159205468cbbfe99fc318786ab9bff1d4c803e00
result: clean
---

# batch-15 review 2

## Verdict

The fix commit bc57c44c resolves f1. It takes the storage path out of the gloss of `request` and makes `request` `Kind of: text`. Text sits above file in the glossary (spec/index.md:167-169), and `features generate --check` exits 0 at the head. There are no new findings.

## Findings

None.

## Earlier findings
- f1: fixed
