---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-84/review-1
kind: review
batch: batch-84
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/107
head: 63ec0fd0c025fd8b9ec4ad1e5eee56fcee6a5114
range: 2d0cab44b6059e5cd6fc1ce7464a04cda400ac96..63ec0fd0c025fd8b9ec4ad1e5eee56fcee6a5114
result: fix-now
---

# batch-84 review 1

## Verdict

The batch builds b573: the totals are gone from `test_decision_checks.py`, the sort test now checks what each tier implies, and every run exits 0. One finding to fix. In replacing the pinned judgement count, the brief test was loosened further than the item needed.

## Findings

### f1 Minor fix now: the brief test no longer catches a judgement decision listed that is not in force
- item: b573
- where: tests/scripts/test_decision_checks.py:86
The old `assert len(found) == 41` held only because the brief listed exactly the 41 accepted judgement decisions. So it also failed when the brief listed anything extra: a superseded decision that kept `tier: judgement`, or the same decision twice.

The new test only checks that the accepted judgement decisions are a subset of what the brief lists, and that each listed path has `tier == "judgement"`. A superseded judgement decision would now pass, and `batch_brief.judgement` (scripts/batch_brief.py:48-55) would list it, because it keeps every file whose frontmatter says `tier: judgement` whatever its status. The reviewer would then be told to check the change against a decision that is no longer in force.

That is an assertion loosened beyond what b573 asks: the item asks only that no count be pinned. I checked the tree at `Head:`: all 41 `tier: judgement` files there are accepted (none is among the 59 superseded ones), so the exact form holds today.

Fix: compare the two sets exactly, with no count:
```python
assert set(found) == judged and len(found) == len(set(found)), sorted(set(found) ^ judged)
```
This replaces lines 86-87.
