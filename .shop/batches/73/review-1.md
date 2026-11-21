---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-73/review-1
kind: review
batch: batch-73
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/97
head: 7a09a3c3bc8b7cd7afd460140f2bc54d2115392a
range: 8b5dc337f279768c4e8bee029d50d6796af3a7d9..7a09a3c3bc8b7cd7afd460140f2bc54d2115392a
result: fix-now
---

# batch-73 review 1

## Verdict

The batch builds b71's r56 and b475's r7, r4, r8 and r9. b60's U20 is not built for every service, so there is one finding to fix. The other findings are observations.

## Findings

### f1 Important fix now: `migrate upgrade` keeps a change on a task's branch, which U20 forbids
- item: b60
- where: scripts/migrate_upgrade.py:199
U20 says that while this repository is in the workspace of a task, any service that keeps a kept change shall refuse the request and name the task. The universal condition's Reading exempts only the batches service. b60's commit and test_task_branch.py rely on one claim: every command that keeps a change does so through `shop_files.committed`, which calls `refuse_task_branch` first.

That claim is false. I searched `scripts/` for `"commit"`. `migrate upgrade` commits with its own `subprocess.run(["git", "commit", ...])` at scripts/migrate_upgrade.py:199 and then calls `shop_files.pushed(root)` at line 207. `refuse_task_branch` is called only from shop_files.py:77. So `migrate upgrade` run on `batch-<n>-b<j>` commits the upgrade on the task's branch and pushes it. It neither refuses nor names the task. The other direct commits (batch_merge, batch_parked, batch_review, batch_amend, batch_start) belong to the batches service, which the Reading exempts.

Fix: before `migrate upgrade` applies any step, call `shop_files.refuse_task_branch(root)` and report the refusal the way the command reports its other refusals. Add the command to `COMMANDS` in tests/scripts/test_task_branch.py, so the test covers each command that keeps a change rather than only the ones that already go through `committed`.

### f2 Minor observation: `spec check` changes for v_t2 although no line of the batch asks for it
- item: b475
- where: scripts/model_spec.py:80
Before this change, two verb entries of one word were "senses" only when every entry of the word was a verb. Now they are senses whenever two or more of the entries are verbs, so a noun "file" beside the three "file" verbs no longer raises v_t2. This brings the code in line with the rule's label ("a term has two entries, other than the senses of one verb"), and test_model_spec_terms.py covers it. It is a change in what `spec check` reports, though, and no requirement line or decision records it. A decision or a checking line would make it traceable.

### f3 Minor observation: the plain `--design` flag swallows the next word
- item: b475
- where: scripts/record_write.py:520
`--design` takes `nargs="?"` with `const=True`, so it eats whatever follows it. `work record --design "Notes app" --summary s --body f` reads "Notes app" as the design to name. The command then fails with argparse's usage error for the missing title, or, if a title comes later, with "names a design only with --plan". The documented order (title first) works. Separate options would remove the ambiguity, for example `--plan --design X` versus a bare `--design-folder`. Also, with `--plan` the options `--summary`, `--kind`, `--about`, `--slug` and `--date` are accepted and silently ignored.

### f4 Minor observation: a single GitHub account for both sides still matches the other side's comment
- item: b71
- where: scripts/request_gh.py:600
`authored` keeps only comments with `viewerDidAuthor`. When the asker's and the upstream's repositories run gh as the same account, the other side's comments also carry `viewerDidAuthor: true`. A body that matches would then still be taken as this side's earlier post. That is the case b71's note describes, and in a single-person setup it is not ruled out. Reproduction: write a comment with `viewerDidAuthor: true` and the step's body into gh-issues.json and leave it out of the record. Then refuse the URL commit once and run `work turn` again, as in test_request_post_recovery.py. Nothing is posted.

### f5 Minor observation: the new records handler module has no row in the module map
- item: b475
- where: CLAUDE.md:263
tests/scenarios/records_handlers_files.py is a new concern (records' design, plan and observation). Its sibling, records_handlers_about.py, has its own row in the map, but this module has none. CLAUDE.md asks for a new module and a row for each new concern.
