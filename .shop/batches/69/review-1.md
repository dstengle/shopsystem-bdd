---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-69/review-1
kind: review
batch: batch-69
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/93
head: 125d7669173167ef052376366540abecf75b7b26
range: 992f17437a4a45b19dd224ae5229da879dd711d9..125d7669173167ef052376366540abecf75b7b26
result: clean
---

# batch-69 review 1

## Verdict

The batch builds both items. b459's commits build items#r48-r52, and b474's chore meets its check while touching only the files the chore names. All five runs exited 0. No finding holds the merge; two observations are recorded.

## Findings

### f1 Minor observation: a split leaves the moved lines' capability declaration, terms, relations and model lines on the old item
- item: b459
- where: scripts/backlog_split.py:48
`_apart` builds the moved block with `terms=(), relations=(), new=None`. `split` gives `models`, `adapters`, `packs`, `universal` and `upstreams` to the kept item only. When the item declares the capability itself (`narrator:`/`group:`/`purpose:`), or the moved lines use a term, a relation row or a model line of the item, the new item holds lines with nothing under them, and `work ready` would refuse it. The old item keeps a declared block, and if every line of a new capability moves, that block has no lines left. r50 asks only that the new item hold the requirement, which it does, so this is hardening. Reproduction from the code: split the only line of an item whose `### <cap>` block carries `narrator:` and a term bullet. The new item's block has neither, and the old item keeps both with no group. A possible fix: move a new capability's declaration and its terms with the lines when every line of that capability moves, or refuse the split and name what stays behind.

### f2 Minor observation: the rerun files are never removed when a batch closes
- item: b474
- where: scripts/batch_rerun.py:26
`keep` writes `<git common dir>/shopsystem-bdd/rerun/batch-<n>-t<k>`, and only a passing `done` of that task deletes it. A task that is parked, or a batch that is abandoned or merged while its last `done` was refused, leaves the file behind. `batch_close` removes the worktrees, review folders and `batch-<n>-driver/`, but not this. Batch numbers are never reused, so a stale file is never read again; it just stays in the git dir. A possible fix: remove the batch's rerun files in `batch_close`'s merged and abandon paths.
