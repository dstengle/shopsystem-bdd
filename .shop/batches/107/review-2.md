---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-107/review-2
kind: review
batch: batch-107
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/130
head: 357d12417eeaa3f0b4daf5861ad519b96d3843de
range: 5d7fe97ceac464d5bf84e69872d7e0dd0b9f17d1..357d12417eeaa3f0b4daf5861ad519b96d3843de
result: fix-now
---

# batch-107 review 2

## Verdict

The fix takes the context id form check out of `work context keep` everywhere the finding named: the code, the model line's refusal reasons, the commands reference and the CLAUDE.md row. It also adds a test that an id the product id covers but that is out of the form is kept. One finding to fix: the new test brings in a `tools check` failure that the base does not have.

## Findings

### f4 Minor fix now: the fix's new test leaves `capsys` unused, and `tools check` now exits 1
- item: b576
- where: tests/scripts/test_shop_contexts.py:15
The run of `python3 scripts/tools check --base 14d07bc8777128d68d2a44b411ad1c3aed18e348` in `## Runs` exits 1 at Head, against 0 at the base. Its output shows why:

```
== vulture ==
tests/scripts/test_shop_contexts.py:15: unused variable 'capsys' (100% confidence)
```

This file is new in c24f64c8c, the commit that fixes f1. The test `test_an_id_the_product_id_covers_out_of_the_context_id_form_is_kept` takes the `capsys` fixture but never reads it, so the failure comes from the fix's own change. Fix: drop `capsys` from the test's parameters, or assert on `capsys.readouterr().out` (for example, that it is `kept bounded-context/example.org/home/A B\n`). Then the check exits 0 again.

## Earlier findings
- f1: fixed
