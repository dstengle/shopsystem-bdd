---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-59/review-1
kind: review
batch: batch-59
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/83
head: 8d1fb7cbaba5f656b55e9c3cb7e86b8171446675
range: bb88863e9daef9922018da6a6cdcbc889eaca0e4..8d1fb7cbaba5f656b55e9c3cb7e86b8171446675
result: fix-now
---

# batch-59 review 1

## Verdict

The batch builds every item's lines and chores. Three findings: one to fix now and two observations. The fix: the `tools check` run fails at Head (it passed at the base) on a ruff error in b451's test. I read every patch, all of `change.diff`, the handlers the new scenarios rely on, `move` in `backlog_moves.py`, `shop_files.committed` and `migrate_init.run`. No test was removed or weakened. The rewrite of b451's `--check` test is what b451 itself asks for: its notes call "`--check` exits 0" the bug. `features generate --check` passes, the size of 888 changed lines is under the 1000 limit, and no judgement decision is broken.

## Findings

### f1 Minor fix now: ruff FURB167 in b451's new test fails `tools check`
- item: b451
- where: tests/scripts/test_model_forms.py:41
The run of `python3 scripts/tools check --base bb88863e9` exits 1 at Head and 0 at the base. Its output:

```
tests/scripts/test_model_forms.py:41:84: FURB167 [*] Use of regular expression alias `re.M`
Found 1 error.
```

The new `test_each_item_it_names_is_open` passes `re.M` to `re.search`. The repository's lint gate is red on this branch until that changes. Fix: write `re.MULTILINE`. That file is one of b451's chore files.

### f2 Minor observation: module-map row and `spec` help text out of date
- item: -
- where: scripts/spec:199
Two pieces of text no longer match the code:

- CLAUDE.md's row for `scripts/backlog_moves.py` lists the commands it holds (`work idea`, `shape`, `refuse`, `withdraw`, `answer`, `rate`, `depend`, `ready`). It does not list `work reopen`, which b431 added to that module (`reopen`, `TRANSITIONS["work reopen"]`).
- `scripts/spec`'s help still says `--json prints {"forms": [{"name", "path", "writer"}]}`. After b451 each form also carries `kind`. b451's chore files leave `scripts/spec` out, so its task could not change that line.

Both are text only; behaviour is right.

### f3 Minor observation: `migrate init` rewrites and reports a `.gitignore` it does not change
- item: -
- where: scripts/migrate_init.py:181
`files[IGNORE] = ignore_text(root)` is set every time. So when the repository already has a `.gitignore` naming all four entries, the file is written back unchanged, named in the commit, and printed as `wrote .gitignore`.

A match is by exact line. An existing `.venv` (no slash) or `/.venv/` does not count, so `.venv/` is added beside it.

Reproduction:
1. Make a git repository whose committed `.gitignore` holds `.venv`.
2. Run `migrate init --id bounded-context/ex.org/x/y`.
3. The output says `wrote .gitignore`, and the file gains `.venv/` beside `.venv`.

Harmless today, since upgrades#r38 only asks that the ignore file is kept. Leaving the file out of `files` when `ignore_text` returns what is already there would make it exact.
