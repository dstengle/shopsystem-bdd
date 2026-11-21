---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-61/review-1
kind: review
batch: batch-61
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/85
head: de07e9c999357451db3bc9a934c1eb3c21184487
range: ca6d91134b7d2707022e8cbc3bf52650b2dd0e21..de07e9c999357451db3bc9a934c1eb3c21184487
result: fix-now
---

# batch-61 review 1

## Verdict

The batch builds the requirement lines of all seven items, and b473's chore meets its check. Two problems hold the merge. Widening the states `work line` accepts also lets `work chore` rewrite the chore of an `in-batch` item, which no line asks for. And `tools check` now fails where it passed at the base, in files from b460, b462 and b470.

## Findings

### f1 Important fix now: `work chore` now rewrites the chore of an in-batch item, which no line asks for
- item: b460
- where: scripts/backlog_section.py:30
`TAKES` is shared by every command that changes an item. Adding `in-batch` to it does more than drafting r38-r40 ask for: those lines only cover rewording, drafting a requirement into, and removing a requirement from an `in-batch` item. `backlog_chore.write` (scripts/backlog_chore.py:85) calls `takes(item, "work chore")`, so `work chore b<n>` on an `in-batch` item was refused before this change and now succeeds and commits.

This matters because `work batch done` checks a task's commits against the files its chore names and runs its check. A chore changed in the middle of a batch moves that boundary without the item going through the readiness bar again, and `work batch amend` lays nothing for a chore, so the batch branch never shows the change. Fix: keep `work chore` refusing an `in-batch` item, for example by passing `work chore` its own tuple of accepted states (`idea`, `shaped`), and keep `in-batch` only for the `work line` paths that `work batch amend` lays again.

### f2 Minor fix now: `tools check` fails on b460's files (it passed at the base)
- item: b460
- where: scripts/batch_amend.py:13
The check exits 1 at `Head:` and exited 0 at the base. Two of its lines are b460's:
```
scripts/batch_amend.py:13:1: I001 [*] Import block is un-sorted or un-formatted
tests/scripts/test_batch_amend.py:30:12: RUF015 Prefer `next(...)` over single element slice
```
Fix: sort the import block and use `next(...)` on line 30 of the test.

### f3 Minor fix now: `tools check` fails on b462's handlers (it passed at the base)
- item: b462
- where: tests/scenarios/checking_handlers_catalogue.py:79
These failures are b462's:
```
tests/scenarios/batches_handlers_settings.py:74:105: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
tests/scenarios/checking_handlers_catalogue.py:79:73: FURB167 [*] Use of regular expression alias `re.S`
tests/scenarios/checking_handlers_catalogue.py:79:80: FURB167 [*] Use of regular expression alias `re.M`
tests/scenarios/checking_handlers_catalogue.py:96:72: FURB167 [*] Use of regular expression alias `re.M`
```
Fix: remove the unused `noqa`, and write `re.DOTALL` and `re.MULTILINE` instead of `re.S` and `re.M`.

### f4 Minor fix now: vulture flags the ignore-file handler's import (it passed at the base)
- item: b470
- where: tests/scenarios/migration_tools_handlers_thens.py:13
At the base, `upgrades_handlers_conftest` was imported on its own line and vulture passed. b470 merged it into a parenthesised import with `upgrades_handlers_ignore`, and vulture now reports both:
```
tests/scenarios/migration_tools_handlers_thens.py:13: unused import 'upgrades_handlers_conftest' (90% confidence)
tests/scenarios/migration_tools_handlers_thens.py:13: unused import 'upgrades_handlers_ignore' (90% confidence)
```
vulture does not read `# noqa`. Fix: go back to one `from scenarios import X  # noqa: F401` line per module, the form that passed before, or add the two names to the vulture whitelist.

### f5 Minor observation: `/__pycache__/` counts as conforming, but git reads it as top-level only
- item: b470
- where: scripts/migrate_init.py:146
`ignore_text` strips the leading `/` before comparing, as the item's note and the ignore file form's vocabulary entry say it should. Git does not match lines that way: `/__pycache__/` ignores only a top-level `__pycache__`, while `__pycache__/` ignores one at any depth. Reproduction: start from g40's given `.gitignore` (`/__pycache__/`), run `migrate init`, then create `scripts/__pycache__/x.pyc`. `git status` lists it, though the ignore file entry's purpose is that "the caches are never committed". This is how the line itself is worded, not a fault in the build; the fix would be a retired line and a new one if the person wants git's real matching.

### f6 Minor observation: unlaying a restatement identical to the operation it restates deletes that operation
- item: b463
- where: scripts/backlog_model_ops.py:235
`restated` treats any operation the model already holds as the item writes it as restated. `held` then walks the file's git history for the latest version that does not hold those lines. If the item's operation line is the same as the existing one, that version is the one from before the operation existed. `unrestate` finds no such operation there and puts back nothing. Reproduction: an item with `### notes model` containing `service notes` / `  operation archive(note)  outcomes: done`, identical to the fixture's line. `work batch start`, then `work batch park`: `archive` is no longer in `spec/model/notes.md`. No client is known to send an identical restatement today.

### f7 Minor observation: a failed amend leaves the base's commit in place while the branches go back
- item: b460
- where: scripts/batch_amend.py:1518
`amend` commits the renumbered item and the task set back to `running` on the base (`batch_plan.commit`) before it lays on the task's branch. If `_task` then fails, the `except` block resets both branches but keeps the base commit. The base then holds the renumbered ids and a `running` task, while the branches hold the lines as last laid. Also, `lay_lines` reports a features-generate failure as `work batch start: ...` even when `amend` is the command that ran. A line reworded on an `in-batch` item also never passes the readiness bar before `amend` lays it.

### f8 Minor observation: the change is over the size limit
- item: -
- where: -
The change touches 66 files, +2881 -286 lines, against a limit of 1000 changed lines. Most of it is b460 (`batch_amend.py`, its handlers and tests), b462 (`delivery_settings.py`, `toml_edit.py`, `model_catalogue_write.py`, two handler modules, the `cli.toml` tables) and b463 (`backlog_model_ops.py`, two handler modules). Moving the `spec` contract into `model_contract.py` accounts for about 190 lines on each side.
