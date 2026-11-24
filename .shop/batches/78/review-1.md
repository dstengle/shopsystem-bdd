---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-78/review-1
kind: review
batch: batch-78
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/102
head: af7d978654a5368621866f19df43a6610a34d02d
range: 94fa6deca9b20dad6742b7688420029e499780f9..af7d978654a5368621866f19df43a6610a34d02d
result: clean
---

# batch-78 review 1

## Verdict

The batch does what b559's chore asks. v10c now passes a record whose about is an item or a batch the repository holds, using `shop_ids.held` as `check_refs` does. The records reader now skips a record folder's files below the folder's own level. Every run exits 0, as it did at the base. The change is 4 files and +63 -3 lines, well under the limit. All four touched paths are among the chore's files. Nothing is left to fix now; two minor observations follow.

## Findings

### f1 Minor observation: v10c's old passing example is still in model.lp but nothing checks it
- item: b559
- where: scripts/model.lp:191
model.lp now has two `% pass v10c:` lines. `scripts/model_rules.py:55` reads the examples into a dict keyed by `("pass", code)`, so only the last line is kept. So `about("r","c"). node("c","capability").` no longer appears in `grammar/rules.md` and is no longer run by `spec rules --check`. A reader of model.lp would take it for a checked example. No test was weakened: the catalogue only ever held one passing example per rule. Fix: either delete the old `% pass v10c` line, or let model_rules keep every example of a rule.

### f2 Minor observation: the module map's shop_ids row does not name its new reader
- item: -
- where: CLAUDE.md (row `scripts/shop_ids.py`)
That row says `held` is read by `work record`'s `--about` and by model_facts' `check_refs`. `scripts/model_work.py:114` now reads it too, to write `held/1` for v10c. The `scripts/spec with scripts/model*.py` row still covers model_work, so no rule of the map is broken. Fix: add model_work's `held` fact (v10c) to the shop_ids row.
