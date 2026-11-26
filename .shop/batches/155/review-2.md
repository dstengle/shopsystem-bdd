---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-155/review-2
kind: review
batch: batch-155
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/178
head: 77413da58924c4226fd347f9d0b3b3f9d76c8d15
range: c6330214e7448caf5306344423dfb90eb294fe66..77413da58924c4226fd347f9d0b3b3f9d76c8d15
result: fix-now
---

# batch-155 review 2

## Verdict

The fix closes f1: the four refusals of a drop of something the product does not hold are gone, and such a drop now completes without writing or committing anything. One problem came in with the fix: `tools check` fails at `Head:` but passed at the base, because the fix's new test has a fixture it never uses.

## Findings

### f4 Minor fix now: the fix's new test fails `tools check` (vulture: unused `capsys`)
- item: b795
- where: tests/scripts/test_product_drop.py:28
The run of `python3 scripts/tools check --base 8b4b7fe67f5d392ac0f9d4acfb9bcfc33c164369` exits 1 at `Head:` and exited 0 at the base. Its output names the one cause:

```
== vulture ==
tests/scripts/test_product_drop.py:28: unused variable 'capsys' (100% confidence)
```

Commit 3306df555 added `test_a_drop_of_what_the_product_does_not_hold_completes_unchanged(tmp_path, capsys, what, dest)`, but the test never reads `capsys`. The fix's own change therefore breaks a review check that passed before. Fix, on b795's branch: either drop the `capsys` parameter, or assert on the printed line (for example that `capsys.readouterr().out` holds `dropped`), so the fixture is used.

## Earlier findings
- f1: fixed
