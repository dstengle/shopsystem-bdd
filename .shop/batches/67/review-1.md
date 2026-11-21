---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-67/review-1
kind: review
batch: batch-67
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/91
head: 240af88660926fc828606ef736902f5548ac31cd
range: 03ba325de2dc5fdfb7b36d6a0771c81245dad7b5..240af88660926fc828606ef736902f5548ac31cd
result: clean
---

# batch-67 review 1

## Verdict

The batch builds all five requirement lines: reviews r7 and r8 (b491), and reviews r9, r10 and review-guarantees r10 (b492). No test was removed or weakened. `features generate --check` and every other run exit 0, and the change is within the size limit. No finding needs fixing before the merge. The observations below are hardening and polish. The most important one is that the new resubmit path skips the fix-loop check, so commits that were never reviewed can ride along with a base merge.

## Findings

### f1 Important observation: an awaiting-merge resubmit accepts any commits beside the base merge, and the brief tells the reviewer to ignore them
- item: b492
- where: scripts/batch_base_merge.py:351
`resubmit` only checks that the range since the last review holds at least one base merge (`merges`). It does not run `batch_fix.check` or anything like it, so other commits made on the batch branch after the clean review are pushed with the merge. Examples are a hand edit, or a fix that cites no finding. The normal `work batch review` path refuses such commits: each commit after a review must cite an open `fix now` finding.

`batch_brief` then sees no open finding and writes `## Base merges`. It sets `own = {}`, so no patch is written for those commits, and lists `--first-parent` commits. The section text says "Nothing else of the batch changed since that review", and pr-reviewer is told to "write no finding of it". So unreviewed code reaches a clean review and `awaiting-merge`.

Reproduction:
1. Take a batch `awaiting-merge` after a clean review.
2. In its worktree, commit any change to `scripts/`, then `git merge --no-ff main`.
3. Run `work batch review`, which succeeds.
4. Run `work batch brief`. The extra commit is in `change.diff`, but the brief says nothing else changed.

No line forbids this today, since r9 only asks for a base merge. Suggested hardening: in `resubmit`, refuse any first-parent commit since the last review that is not a base merge, naming it.

### f2 Minor observation: the pull request stays ready while the batch is in review again
- item: b492
- where: scripts/batch_base_merge.py:368
Decision 0100 says submitting opens a draft pull request and a clean review marks it ready. `resubmit` sets the batch to `in-review` but leaves the pull request ready, as the earlier clean review marked it. So the person can merge it on the host before the base merge has been re-reviewed. Calling `gh pr ready --undo` in `resubmit` would keep the pull request in line with the decision.

### f3 Minor observation: the items a conflict names depend on `git merge-tree --write-tree` (git 2.38 or later)
- item: b491
- where: scripts/batch_merge.py:509
`clashing` returns False whenever `merge-tree` does not exit 1. On an older git, the `--write-tree` call fails with a usage error, so every refusal names "the batch's branch" in place of the items that conflict. That silently stops meeting r8's "name ... every item". Paths are also read without `-z`, so a path git quotes (one with spaces or non-ASCII characters) never matches `path`, with the same effect. Suggested hardening: run with `-z`, and treat any exit code other than 0 or 1 as a git failure.

### f4 Minor observation: a comment in ADDED is now on the wrong entry
- item: b492
- where: tests/scenarios/requested.py:982
The trailing `# b370: the rule catalogue's checks` now sits after the b492 entry on the line below, not on the `checking#g52-57` comprehension it describes. Fix: move it back to line 981.

### f5 Minor observation: a missing comma in pr-reviewer's header list
- item: b492
- where: agents/pr-reviewer.md:14
The line reads "whether it is the first (the pull request is unreviewed) a re-review of the fix, or a re-review of the base merge". It needs a comma after "(the pull request is unreviewed)".
