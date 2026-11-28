---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-179/review-1
kind: review
batch: batch-179
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/201
head: 39d311b68a2a7e79e94f85b0fa48f62288038339
range: fa9de26e415d6dc3b54631179d69dabaa31f764c..39d311b68a2a7e79e94f85b0fa48f62288038339
result: fix-now
---

# batch-179 review 1

## Verdict

The batch builds b889's three lines: r203 at opening, r204 at an amend, and r205 at `work batch done`. Two findings must be fixed before merge. Commit aa44ac541 deleted most of the module map's `tests/` rows, and the batch's ruff check fails where it passed at the base.

## Findings

### f1 Important fix now: the module map loses about 90 rows of modules that still exist
- item: b889
- where: docs/reference/modules.md:373
Commit aa44ac541's hunk `@@ -372,95 +373,4 @@` replaces the table from `tests/scenarios/batches_handlers_rebuilt.py` to the end of the file with the single `batches_handlers_dependents.py` row. It also leaves the file with no newline at its end.

The rows deleted include `batches_handlers_rebuilt.py`, `batches_handlers_renumbered.py`, `batches_handlers_finding.py`, `batches_handlers_amended.py`, every `drafting_handlers_*`, `readiness_handlers_*`, `design_model_check_*`, `upgrades_handlers_*` and `codified2_*` row, `tests/toolchain.py`, `tests/scripts/`, `batch_templates.py`, `test_docs.py`, `cpu_budget.py` and `test_docs_truth.py`. None of these modules is removed by the change.

I checked this against the base: main's docs/reference/modules.md still holds them at lines 374-457, and none of them is in the Tree's modules.md. Commit 48fa58b1f had added the dependents row correctly, among the existing rows. CLAUDE.md makes the module map binding, so this is lost data, not a style point.

Fix: put back the base's rows from `batches_handlers_rebuilt.py` onward with the new `batches_handlers_dependents.py` row kept among them, and end the file with a newline.

### f2 Important fix now: `tools check` fails at Head and passed at the base (ruff)
- item: b889
- where: scripts/batch_amend.py:41
`python3 scripts/tools check` exits with `Exit code: 1 (base: 0)`:
```
scripts/batch_amend.py:41:32: RUF100 [*] Unused `noqa` directive (unused: `F401`)
scripts/batch_tasks.py:29:66: RUF100 [*] Unused `noqa` directive (unused: `F401`)
tests/scenarios/batches_handlers_dependents.py:30:10: ISC004 Unparenthesized implicit string concatenation in collection
tests/scenarios/batches_handlers_dependents.py:32:10: ISC004 ...
tests/scenarios/batches_handlers_dependents.py:34:10: ISC004 ...
tests/scenarios/batches_handlers_dependents.py:183:24: PERF102 When using only the values of a dict use the `values()` method
tests/scripts/test_batch_relay.py:4:1: I001 [*] Import block is un-sorted or un-formatted
```
`relay` is called in `amend`, and `touching_feature`, `uncited` and `under_shop` are all used in `batch_tasks.checked`, so neither `# noqa: F401` is needed.

Fix:
- Drop both `noqa` directives.
- Put each item of `LINES` in parentheses.
- Iterate `.values()` in `_touching`.
- Sort the imports of test_batch_relay.py.

### f3 Minor observation: a hand edit of a feature escapes r205 when its commit takes an amend's subject
- item: -
- where: scripts/batch_commits.py:36
`touching_feature` lets through any commit whose subject starts with `<batch>: the requirement lines of ` and ends with ` amended`. It tests the subject only, so a session that writes that subject on a hand edit of `features/` passes `work batch done`.

To reproduce, commit an edit of `features/work-queue.feature` on a running task's branch with the message `batch-1: the requirement lines of b1 "x" amended`, then run `work batch done` on the task: nothing is refused.

Keying the exception on the `Applied:` line, or on the commit's diff matching what the apply writes, would close this. No session does this today.

### f4 Minor observation: a dependent's relay applies its blockers' lines as main holds them, not as their tasks were applied
- item: -
- where: scripts/batch_relay.py:640
`relay` puts the workspace back to `batch.forked_from` and applies `blockers(...)` read from the backlog on main. Suppose a blocker's lines were changed with `work line` but not yet `work batch amend`ed. An amend of the dependent, or of another blocker, then applies the unamended change to the dependent's workspace, while the blocker's own task workspace still holds its old lines.

I found this by reading `relay` and `blockers`: both read items through `backlog_items.find(root, …)` and nothing compares them with the blocker's last `Applied:` commit. No line of the batch names this state.
