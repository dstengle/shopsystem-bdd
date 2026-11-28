---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-180/review-1
kind: review
batch: batch-180
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/202
head: 39126100446ae3643c918b15a9676a253cf89537
range: 0c6c5e95ba27c2ad31fb096daa7876f048b30eca..39126100446ae3643c918b15a9676a253cf89537
result: clean
---

# batch-180 review 1

## Verdict

The batch builds b875's chore. It deletes `batch_parked.py`, `backlog_area_move_unlay.py`, every `backlog_*` unlay half and their unlay-only helpers, `decision_successor.unlay` and `batch_start.cites`, with their tests and module-map rows. What remains is only lay code, so lay behaviour is unchanged. I found nothing to fix now. There are two observations: the change is over the size limit, and one module-map row is stale.

## Findings

### f1 Minor observation: the change is over the review size limit
- item: b875
- where: -
`## Size` gives 46 files, +110 -1556 changed lines, against a limit of 1000. All of it is b875, and almost all of it is deletion: the unlay functions in 22 `scripts/` modules, two whole modules and one whole test file. b875's notes allow splitting the work per module family if it goes over the limit; this batch kept it whole. Because the change only deletes, the review surface is small, so this does not hold the merge.

### f2 Minor observation: the laying_inprocess row of the module map still says its removal is b875's, and its lift now calls functions that are gone
- item: b875
- where: docs/reference/modules.md:242
The row still reads:
```
read by laying alone since b874, its removal b875's and b861's
```
b875 did not remove `laying_inprocess.py`. It only removed what the module's `lift` and `unlay_lines` call: `scripts/laying_inprocess.py:80` calls `backlog_lines.unlay` and `:85` calls `decision_successor.unlay`, and both are deleted. b875's notes say these calls stay unreached until b861 deletes the module. I checked with a grep of `scripts/` and `tests/`: nothing calls `laying.lift`, because `batch_parked.py` was its only caller and is gone. So nothing breaks today, and ruff and vulture both pass in `## Runs`. But the row now names the wrong item, and it does not say that `lift` is broken. Fix, now or in b861: say "its removal b861's", and note that `lift` and `unlay_lines` call removed functions.
