---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-44/review-2
kind: review
batch: batch-44
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/67
head: 163740cc5f3388a97cde6a32a85890efe90093b2
range: add4f211ceb99c7842182fc638f7b7d82cb5c9a5..163740cc5f3388a97cde6a32a85890efe90093b2
result: clean
---

# batch-44 review 2

## Verdict

The fix is good: f1 is fixed and the fix has no fault of its own. The fix commit 82ad9faf7 adds Implementation bullets to `spec/capabilities/readiness.md` and `spec/capabilities/batches.md`. Between them they name every behaviour f1 listed:
- `work chore` refuses a `--file` under `spec/`, `features/` or `.shop/`, or outside the repository.
- Run again, `work chore` replaces the chore.
- The readiness bar gives the reason `it holds a chore and requirement lines, which exclude each other: take one of them out`.
- `work batch resume` prints the chore's files and check in place of ids.
- The batch brief and `pr-reviewer`'s brief hold the chore's lines.

I checked each bullet against the code in the batch's worktree, and each says what the code does:
- `backlog_chore._path` refuses those files.
- `write` replaces the chore.
- `unlined` gives the reason text exactly as the bullet quotes it.
- `batch_tasks.resume_said` prints `said(item)[1:]`, which is the files line and the check line.
- `batch_driver` and `batch_brief._items` hold the chore's lines.
- `batch_tasks` line 192 runs the check after the tests, as the batches bullet says.

The change is two spec files and 10 added lines, well under the size limit. Every check in `## Runs` exited 0 at the head and at the base.

## Findings

None.

## Earlier findings
- f1: fixed
