---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-120/review-2
kind: review
batch: batch-120
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/143
head: 53113d720bbab2b3e5b17eb96adbd8b6be75db77
range: fa28e0e42f4126c6001940c387698140f4532de0..53113d720bbab2b3e5b17eb96adbd8b6be75db77
result: clean
---

# batch-120 review 2

## Verdict

The fix closes f1: b701's unlay now puts an existing port area's own `imports:` back as the batch's base held them, and the new test shows the file coming back byte for byte. Nothing to fix now. Two observations follow on how the fix works.

## Findings

### f5 Minor observation: the port's imports are reset to the base whole, so another item's imports on the same port area are dropped
- item: b701
- where: scripts/backlog_port.py:93
The fix replaces the port's whole `imports:` list with the list at `base`. It does not take out only the names this item's lay added. Suppose two items of one batch place capabilities in the same existing port area, for example both use `work line --capability ... --area stock --port`, and each lay adds its own imports to `spec/model/stock.md`. When one item is parked or taken out by `work batch review`, the other item's imports are lost too. That other item's port lines then raise v_m1 on the batch branch.

The modules next to it keep what other items added. `backlog_area_move_unlay._imports` keeps every name that is not one of its targets (scripts/backlog_area_move_unlay.py:42). `backlog_model_elements` keeps another item's member lines (batches r119). No line names this case, so it is hardening.

Fix: take out only the names that are in the file now, not at `base`, and that this item's `lay` would add. That is the areas whose words `_text(into, port, blocks)` says, per `_says`.

### f6 Minor observation: with no base, as `work batch amend` calls it, the port's imports are not put back
- item: b701
- where: scripts/backlog_port.py:92
`batch_amend.py:112` calls `batch_start.unlay_lines(tree, [old], COMMAND)` with no base. `backlog_area_move_unlay.held(path, None)` then returns the latest committed version of the file. On the batch branch that is the version the lay committed, which already has the item's imports. So `was` equals what the file holds now, and nothing is put back.

The amend lays the item again straight after the unlay. A stale name stays only when the amended lines no longer say that area's words. `backlog_area_move_unlay._imports` has the same limit with no base, so this is not new to the fix.

What I verified: the callers of `unlay_lines`. `batch_parked.py:61` and `:93` and `batch_review.py:108` pass a base; `batch_amend.py:112` does not.

## Earlier findings
- f1: fixed
