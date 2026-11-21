---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-62/review-1
kind: review
batch: batch-62
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/86
head: 11b58a95c77582d1d4c6033ae9cfd8e6f6784812
range: 80349332f6fc0a5d31caebbd09d7ba017a3e59a5..11b58a95c77582d1d4c6033ae9cfd8e6f6784812
result: fix-now
---

# batch-62 review 1

## Verdict

The batch builds the lines of all six items. One finding needs fixing now: `tools check` fails at Head but passed at the base, because ruff finds an unused import in b367's new test module. The change is also over the size limit. The other two findings are hardening and do not hold the merge.

## Findings

### f1 Important fix now: tools check fails at Head on an unused import in b367's test
- item: b367
- where: tests/scripts/test_backlog_model_edit.py:6
`python3 scripts/tools check --base 80349332f` exits 1 at Head; it exited 0 at the base. The run's output:
```
tests/scripts/test_backlog_model_edit.py:6:47: F401 [*] `backlog_testing.write_item` imported but unused
```
The import line pulls in `write_item`, and no test in the module uses it. Fix: take `write_item` out of the `from backlog_testing import ...` line, so that `tools check` exits 0 again.

### f2 Minor observation: the change is over the review size limit
- item: -
- where: -
`## Size` gives 37 files, +1381 -57, against a limit of 1000 changed lines. Most of it is b367 (the new `scripts/backlog_model_edit.py`, its scenario handlers, its test module, eight corpus blocks and four contract tables) and b482/b479 (`adapter_tables.of`, the unlay against the base and their tests).

### f3 Minor observation: work batch start's rule check looks only at requirement ids, not the item's group ids
- item: b478
- where: scripts/batch_start.py:129
`violating` builds `mine` from `backlog_lines.ids(...)` only, so it holds requirement ids alone. The readiness bar's `_broken` also adds each group id `<cap>#g<n>` (readiness_bar.py:94). A model.lp rule of severity error that names only a group the lay brings (for example `v_s3`, "a group has no scenario", if a feature fails to generate) would therefore pass `work batch start`, and the batch would be laid broken. batches#r89 speaks of a requirement, so this is hardening. I checked that the lay writes features before the check (`lay_lines` calls `_generated`), so `v_s3` does not fire on a normal lay. Fix when convenient: add the item's group ids to `mine`, as `_broken` does.

### f4 Minor observation: --reword-model with the same text keeps the same model line
- item: b367
- where: scripts/backlog_model_edit.py:115
drafting#r45 says the drafting service keeps "a different model line". `reword_model` never compares the new lines with the element's current ones. Given the same text, it renders an unchanged item and calls `commit`. That falls to git's nothing-to-commit refusal rather than a refusal that names the model line, which is the same shape of problem b481 fixes for `work decision --amend`. To reproduce: `work line b1 --reword-model "object shelf" "object shelf\n  attributes: label (text)"` on an item holding exactly that element. `reword_term` behaves the same way.
