---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-155/review-3
kind: review
batch: batch-155
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/178
head: 96e8db869ab3dc9652c79b163d4f78b48e855522
range: 77413da58924c4226fd347f9d0b3b3f9d76c8d15..96e8db869ab3dc9652c79b163d4f78b48e855522
result: clean
---

# batch-155 review 3

## Verdict

The fix resolves f4: it takes the unused `capsys` parameter out of the test, and the test's assertions are unchanged. The `tools check` run now exits 0, and every other check exits 0 at `Head:` as it did at the base.

## Findings

None.

## Earlier findings
- f4: fixed
