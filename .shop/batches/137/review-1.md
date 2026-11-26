---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-137/review-1
kind: review
batch: batch-137
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/160
head: bb74f7cec8f04b7408ec5dc33267c485775f088b
range: 48c0c318d563ba5dcfe221c5671ad2eee7ca2208..bb74f7cec8f04b7408ec5dc33267c485775f088b
result: fix-now
---

# batch-137 review 1

## Verdict

The batch builds all five requirement lines. The size is within the limit (35 files, +528 -41 against 1000). One finding must be fixed: `tools check` fails at the head because of a test that b749 added, and it passed at the base. The rest are observations on paths no line names.

## Findings

### f1 Important fix now: vulture fails at the head on an unused `kwargs` in b749's new test
- item: b749
- where: tests/scripts/test_batch_generator.py:60
`python3 scripts/tools check --base 48c0c318d` exits 1 at the head and exited 0 at the base. The output shows why:

```
== vulture ==
tests/scripts/test_batch_generator.py:60: unused variable 'kwargs' (100% confidence)
```

The stub `def fail(*args, **kwargs)` in `test_a_generator_that_cannot_start_is_a_generate_error_naming_it` never uses `kwargs`. One of the review checks is red because of this batch. Fix: rename the parameters to `*_args, **_kwargs`, or something vulture accepts, so the check exits 0.

### f2 Minor observation: generate_all swallows a timeout and runs each capability again, so a stalled generator costs (N+1) time limits and refuses nothing
- item: b749
- where: scripts/batch_generator.py:73
If the one run for all paths times out, `generate_all` catches the GenerateError, sets `done = None` and falls back to running `generate` once for each path. Each of those runs times out again, and the loop turns that into `None`. batch_reached (scripts/batch_reached.py:40) then leaves those features as they were without a word. With the default limit of 600 s and N reached capabilities, one stalled generator holds the batch lock for (N+1)×600 s and ends with no refusal. That goes against this module's own docstring: "a GenerateError naming the feature generator, which those commands refuse with". What I checked: start, park and amend first write the laid capability's feature through `batch_start`'s per-capability `batch_generator.generate`, which does refuse (scripts/batch_start.py:93-95). So r175 and r176 hold today, and this path is only reached when the generator stalls after that first run succeeds. Hardening: let a timeout (as opposed to a refusal) in `generate_all` propagate.

### f3 Minor observation: park decides `fresh` before taking the lock, then on failure deletes the whole worktrees directory
- item: b749
- where: scripts/batch_tasks.py:263
`fresh = not trees_path(root).exists()` is read outside `locked(root)`. On a failed `take_out`, `shutil.rmtree(trees_path(root), ignore_errors=True)` removes the whole directory. Another batch command (`done`, `resume`) could create that directory and a worktree in it between the check and the lock. A park that then fails would delete that worktree and leave git's worktree record stale. Reproduction: two commands racing on a checkout with no `.shop/worktrees/`. Hardening: compute `fresh` inside the lock, and remove only what this park made (the `.gitignore` that `trees_dir` wrote, and the directory if it is empty) rather than calling `rmtree`.

### f4 Minor observation: take_out's `reset --hard` leaves untracked files and discards edits already in the batch worktree
- item: b749
- where: scripts/batch_parked.py:67
When the batch worktree already existed (`made` is False), a refusal resets it to `before` with `git reset -q --hard`. Two effects: any uncommitted changes in that worktree from before the park are thrown away, and untracked files the unlay wrote stay behind. So "change nothing" holds only for tracked files in a clean worktree. Hardening: refuse up front when the batch worktree has uncommitted changes (`uncommitted`), and add `git clean -fd` on the paths the unlay touched.

### f5 Minor observation: park now takes lines out before removing the task worktree, and a failed `remove_tree` is not put back
- item: b749
- where: scripts/batch_tasks.py:278
The change moves `batch_parked.take_out` ahead of `remove_tree(root, tree_of(...))`. Only `batch_plan.commit` is wrapped in `put_back`. If `remove_tree` fails (`git worktree remove --force` refused), the batch branch keeps the take-out commit while the item is still `in-batch` on the base. Hardening: wrap `remove_tree` in the same `put_back` guard.

### f6 Minor observation: a failed deregister during compensation hides the refusal of the register
- item: b743
- where: scripts/contract_obtain.py:516
`_compensate` runs before the `contract not registered` refusal is raised. If a deregister itself raises (for example a `Refused` from a failing git commit in `shop_files.committed`), the person gets that error instead of r140's refusal naming the adapter spec. The later contracts written in the loop also stay registered. The model gives deregister only a done outcome, so no line covers this. Hardening: run each deregister in its own try, and raise r140's refusal after all of them, naming any that failed.

### f7 Minor observation: the module map rows of batch_tasks and batch_parked do not mention the new refusal handling
- item: b749
- where: CLAUDE.md
The diff updates the `batch_generator.py` row for b749. The rows of `scripts/batch_tasks.py` (park: lines taken out before the task worktree is removed, the worktrees directory removed when park made it) and `scripts/batch_parked.py` (`take_out` resetting an existing worktree on a refusal) do not describe what this batch changed. CLAUDE.md says a concern belongs in its row. Fix: add a clause to each row.
