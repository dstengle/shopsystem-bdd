---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-182/review-1
kind: review
batch: batch-182
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/204
head: 3f8ca5c6d4181cf8c18dbd4f3a2d800362d56bc3
range: b40616d71ffec54592fda338221ce162d977957f..3f8ca5c6d4181cf8c18dbd4f3a2d800362d56bc3
result: clean
---

# batch-182 review 1

## Verdict

The batch builds b900: both laying modules are deleted, nothing in `scripts/` or `tests/` still imports `laying` or `laying_inprocess`, the `.importlinter` lists and the upgrades-apart name are updated, the three docstrings and the two phase names now say apply, and the docs and skills say apply/applied. Every run exits 0. One observation, and nothing to fix now.

## Findings

### f1 Minor observation: the module map still names a module that does not exist
- item: b900
- where: docs/reference/modules.md:350
Line 350 of the module map still says `laying_handlers and checking_handlers_apply build theirs by`, but there is no `laying_handlers` module: no file matches `tests/scenarios/laying*` in the tree. The row is older than this batch. It names neither the laying service nor `laying_inprocess`, so b900's notes do not ask for it to change and its check does not catch it. Still, the map is binding under CLAUDE.md, and a reader is sent to a missing module. Fix later: say which module builds those worlds now, probably an `applying_handlers*` module.

What I verified, so it needs no fix:
- Removing the modules leaves no importer behind: only docstring history mentions `laying` in `scripts/` or `tests/`.
- No code or spec reads the old phase strings `"lay"` or `"laid scenarios run"`. `batch_applied` uses `phases.LAY` and `phases.SCENARIOS` by name, and the `"lay"` strings in `tests/scripts/test_batch_timings.py`, `test_phases.py` and `test_measure_batch_show.py` are arbitrary data.
- The new `applying r46, r47` reference in `scripts/batch_reached.py:1` names lines that exist in `spec/capabilities/applying.md`.
