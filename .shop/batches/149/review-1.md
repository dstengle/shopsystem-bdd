---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-149/review-1
kind: review
batch: batch-149
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/172
head: 3014605abe45103a0e37a3ad82cb403ed23ad302
range: 91f5a576e45db403e4f0a40e4eef4e935540f7c3..3014605abe45103a0e37a3ad82cb403ed23ad302
result: clean
---

# batch-149 review 1

## Verdict

The batch builds all six items. drafting#r91 (b768) and laying#r47 (b761) are built and have scenarios, and the four chores' checks pass. Every run exits 0, as it did at the base, and the change of 491 lines is within the limit. Nothing to fix now. Three observations follow: a chore's check runs with a different interpreter from the task's tests, module-map rows no longer describe the code, and b772's fixture change drops a coverage case.

## Findings

### f1 Minor observation: a chore's check runs with the tree's .venv only, not the fallbacks the task's tests get
- item: b771
- where: scripts/backlog_chore.py:139
The docstring says `run` uses "the environment a task's tests run in (batch_tasks' `run_tests`)". But `run_tests` picks its interpreter with `interpreter(tree, workspace, root)`, while `run` calls `interpreter(tree)` alone. `passes(item, tree, ...)` gets only the task's tree.
`.venv` is ignored by git, so a task worktree usually has none. The tests then run under the checkout's `.venv/bin/python` (b449), but the chore's check runs under the system `python3`. A check such as `python3 -m pytest -p work_items` can therefore still fail where the tests pass, for want of pytest or clingo.
What I read: `scripts/batch_tasks.py:95` (`python = interpreter(tree, workspace, root)`) and `scripts/batch_tasks.py:223` (`backlog_chore.passes(item, tree, ...)`). The item's note says "the tree's .venv python as batch_tasks gives the tests", so this matches its words but not what the docstring promises.
Hardening: pass the root, and the workspace where there is one, through `passes` to `run`, and call `interpreter(tree, workspace, root)` as `run_tests` does.

### f2 Minor observation: the module map's rows of the changed modules describe the code before this batch
- item: -
- where: CLAUDE.md:287
These rows no longer match the code:
- **`batch_parked` and `batch_amend` (lines 287-288):** still name `as_laid`, which b769 deleted. The idea b781 already records this.
- **`backlog_reword`:** says reinstating takes out "a pair with no line under `retires:`". Since b768, every pair naming the id goes and the item's own line is kept.
- **`spec_coupling_imports`:** says a name is resolved in "the importer's folder, else a dotted name under the root". It does not mention `folders` (b772).
- **`backlog_chore`:** does not say the check runs with the plugin's scripts on PYTHONPATH and the tree's `.venv` python (b771).
- **`laying`:** no row mentions the lift's `laid` commit or the `lifted` field of its reply (b769).

The chores' `Files:` lists leave out CLAUDE.md, so their tasks could not update the map. Fold these rows into b781, or into an item of their own.

### f3 Minor observation: b772's fixture change loses the case it tested
- item: b772
- where: tests/scripts/test_spec_coupling.py:68
The earlier test kept `a/store.py` as a file that `import store` in `b/` does not resolve to. Under b772, a name now resolves under each folder that holds an area's file, so that import would couple. The fixture now places the file at `a/pkg/store.py` instead, and the assertion is unchanged. This follows from the item's own change, and the new `test_an_import_resolves_through_an_area_folder` covers the positive case.
What drops out of the suite is a negative case: a bare name that matches a module in a folder of another area now resolves to it. For example, `import vocab` from anywhere would resolve to `tests/scenarios/vocab.py` whenever that file is in an area. That can report couplings that do not exist when two folders hold modules of the same stem. No test pins which one wins: `folders` is sorted, and the first base in that order is taken.
