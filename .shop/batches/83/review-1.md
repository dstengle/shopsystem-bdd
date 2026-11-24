---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-83/review-1
kind: review
batch: batch-83
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/106
head: 84a535e1b4451995eaceee024bb81b5326525d1f
range: 463fda72f7e5eb8cc5e6681424fc02087af4c5a7..84a535e1b4451995eaceee024bb81b5326525d1f
result: clean
---

# batch-83 review 1

## Verdict

The batch does what b563 asks. An observation in `.shop/records/observations.md` whose `about:` names an item or a batch this repository holds now passes v10c, the same way a record's `about:` does. Every run exits 0. The test changes add one test and raise counts; no test is removed or weakened. No findings.

- **The fix:** in `scripts/model_work.py`, the `held/1` fact that only records got is now produced by a shared helper, `about_held`. The observation reader calls it after writing its `about` fact. v10c is `v10c(R) :- about(R, A), not is_standing(A), not held(A).` in `scripts/model.lp`, so it now applies to observations as well. `model.lp` itself is unchanged.
- **The new test:** `test_an_observation_about_an_item_held_is_about_something_standing` checks both sides. The observation about the held item `b3` passes, and the one about `b9`, which is not held, is still the only v10c violation.
- **The count changes:** the commit to `tests/scripts/test_decision_checks.py` raises the totals from 124 to 126 decisions and from 39 to 41 judgements, for decisions 0126 and 0127. That matches the person's answer on b563, which also added this file to the chore.
- **Scope and rules:** every commit touches only paths in the chore's `Files:` list. `model_work.py` falls under the module map's `scripts/spec` with `scripts/model*.py` row. The size check passes, and the change is 23 added and 6 removed lines against a limit of 1000.
- **Judgement decisions:** none of them bear on this change.

## Findings

None.
