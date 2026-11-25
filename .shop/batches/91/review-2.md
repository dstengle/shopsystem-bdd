---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-91/review-2
kind: review
batch: batch-91
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/114
head: 6bbeb842c103b48e13055880a324bc41af99d9f2
range: 449028e25550bac7ab7d1466c11315abaf1c00c6..6bbeb842c103b48e13055880a324bc41af99d9f2
result: clean
---

# batch-91 review 2

## Verdict

The fix for f1 is correct. The code no longer has its own refusal. Obtaining again over a contract kept at the same place now writes the upstream's bytes and commits them. When the bytes are the same, it changes nothing. The module map row and the `spec obtain` entry in `docs/reference/commands.md` now say the same thing. A new test, `tests/scripts/test_contract_obtain.py`, covers both cases, and no test was removed or weakened. Every run exits 0, as it did at the base, and the change is small (+67 -10). There are no new findings.

## Findings

None.

## Earlier findings
- f1: fixed
