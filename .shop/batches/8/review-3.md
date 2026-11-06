---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-8/review-3
kind: review
batch: batch-8
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/23
head: 7fcab7523383b53b51f7458837c9e5e9330d5dc2
range: 5c046d75c0e50cff51ad747ca2b424f0e13d1c6d..7fcab7523383b53b51f7458837c9e5e9330d5dc2
result: clean
---

# batch-8 review 3

## Verdict

The fix for f6 removes the blank line between `import pytest` and `from shop_files import push_env` in `tests/scripts/test_push_env.py`. That puts the imports in one block, as ruff's I001 asks. `tools check` now exits 0 at the head, and every other run exits 0 too. The change is one line, it changes no test's behaviour, and no new finding comes from it.

## Findings

None.

## Earlier findings
- f6: fixed
