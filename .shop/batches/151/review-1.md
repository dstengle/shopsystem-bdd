---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-151/review-1
kind: review
batch: batch-151
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/174
head: a32987b53afe2b9d691543517b7f9cca878530ff
range: a48f0c1038dc27e5b4d40def2c21f571bc2de50c..a32987b53afe2b9d691543517b7f9cca878530ff
result: clean
---

# batch-151 review 1

## Verdict

The batch builds all five chores as their items' technical calls describe, and every run exits 0, as it does at the base. Nothing needs fixing before the merge. There are two Minor observations.

## Findings

### f1 Minor observation: the module map rows of backlog_chore and spec_coupling_imports no longer say what the code does
- item: -
- where: CLAUDE.md:1
The b784 change makes `backlog_chore.run` pick its interpreter the same way `run_tests` does. It tries the tree's `.venv/bin/python` first, then the workspace's, then the checkout's (`interpreter(tree, workspace, root)`). The `scripts/backlog_chore.py` row of the module map still says only "the tree's `.venv/bin/python` when it holds one, b771". The b785 change makes a name that two area folders hold resolve to no file, so it couples nothing. The `scripts/spec_coupling_imports.py` row still describes the lookup without that case. CLAUDE.md calls its module map binding, and these two rows now describe less than the code does. Neither chore's `Files:` list allowed CLAUDE.md, so the tasks could not fix it. Fix: add "else the workspace's, else the checkout's (b784)" to the first row and "a name two area folders hold naming none (b785)" to the second, in a later item or chore.

### f2 Minor observation: a same-stem clash inside one area now drops a real coupling
- item: b785
- where: scripts/spec_coupling_imports.py:131
`imported` returns None whenever two or more `extra` folders hold a file for the name. It does not check whether those files belong to the same area. Suppose area `a` declares both `src/store.py` and `lib/store.py`, and `b/x.py` runs `import store`. Then b depends on a whichever file Python loads, but no `b -> a` import is reported. The item's wording only says such a name resolves to none of the files, and its test covers files of two different areas (`a/store.py`, `c/store.py`), so this edge is unspecified. Hardening: when every candidate's area (`area_of`) is the same, report the coupling to that area.
