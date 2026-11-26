---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-120/review-1
kind: review
batch: batch-120
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/143
head: fa28e0e42f4126c6001940c387698140f4532de0
range: 5ea8203c7e6e95f443b4ce09ba8b9e8c958ef907..fa28e0e42f4126c6001940c387698140f4532de0
result: fix-now
---

# batch-120 review 1

## Verdict

The batch builds all five lines: b696 (r149), b698 (r150), b701 (drafting#r85, batches#r151) and b695 (r124). Every run exits 0. One finding to fix now. When a driven port's area already exists, the unlay of b701's port does not undo what the lay did. Three observations do not hold the merge.

## Findings

### f1 Important fix now: the unlay leaves imports the lay added to an existing port area's model file
- item: b701
- where: scripts/backlog_port.py:63
`work line --capability --area <a> --port` accepts an area that already exists in spec/model/ when its kind is `port` (`backlog_capability._port`). For such an area, `backlog_model_area.made` returns False. `backlog_port.lay` still writes the port's own imports into it: `_imports(into, port, [...])` adds each area whose words the port's lines say, for example `notes` to `spec/model/stock.md`.

`unlay` only calls `backlog_area_move_unlay._imports(into, set(made), base, files)`. That function takes the *port's name* out of other model files' imports. It keeps every name that is not in `targets`, so the `notes` the lay added to the port's own file stays there. `unmade` does not remove the file either, because the file existed before.

The result: when such an item is parked, or taken out by `work batch review`, the batch branch keeps a change from an item that is no longer in the batch. That goes against the module docstring and the CLAUDE.md row: "taken out by the unlay, each import the lay added out".

What I verified: `backlog_area_move_unlay._imports` (scripts/backlog_area_move_unlay.py:36-45) keeps `[n for n in names if n not in targets or n in before]`. The port's own added names are never in `targets`.

Fix: in `unlay`, also put each port's own `imports:` back to what the file held at `base` (else as git last held it), for example by passing the names the lay added to the port. Add a test where the port area already exists.

### f2 Minor observation: `fix task` is also given when no scenario of any item broke
- item: b696
- where: scripts/batch_broken.py:796
r149 asks for `fix task` with the task when "a scenario of the item breaks in the workspace of the batch". `task_of` also returns `tasks[0]` when the kept failed ids name no scenario of any item and no task's change reaches them, for example a `tests/scripts/` test only the base's code breaks. The poll then names a task that may have nothing to do with the failure.

This beats the endless `submit batch` the poll gave before, but no line states it. Either write a line for a refused submit that no item's scenario explains, or return no task in that case.

### f3 Minor observation: after a recorded review, the `fix task` step's report leads to a refused review
- item: b696
- where: scripts/batch_next.py:874
The report says "a commit on <branch> citing Item: <item>, then shop work batch review". Once a batch has a recorded review, `batch_fix.check` refuses a commit made since that review that cites no open finding.

So if every finding of a review is fixed and the next submit's whole-suite run fails, the poll gives `fix task`. The commit it asks for is then refused by `work batch review`.

Reproduction: record a review with one `fix now` finding, fix it, run `work batch review` with failing `[batch] tests`, then follow the step's report. No line covers this state yet.

### f4 Minor observation: CLAUDE.md's model_product row still says a malformed product file is a file problem
- item: b695
- where: CLAUDE.md:254
The change makes a product file that is not of the product form the fact `unformed_product`, which `w_unformed_product` reads (scripts/model_product.py:56). The module map row for `scripts/model_product.py` still ends with "a product file not of the product form a file problem", and it does not name the new warning. The module map is binding: update the row.
