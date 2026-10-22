# Review: migration-tools-1

**Verdict: DONE_WITH_CONCERNS.** The commit does what r15, r18-r20 and r22-r28 ask on the inputs the scenarios build, with no change under `features/`, no test removed or weakened and nothing outside the file set. One finding is triaged fix now: `migrate upgrade` refuses on a repository that has `.shop/` but no `.shop/work/`. That is the repository r19's own scenario builds, and the refusal leaves the hook offering the upgrade at every session start.

## Commits reviewed

The branch `work/migration-tools-1` is gone. On HEAD, between `b4a211e work: migration-tools-1 ready -> claimed` and `0a46dcb work: migration-tools-1 claimed -> done`, there is one commit:

- `ff22a77 migrate: status and upgrade, the SessionStart hook and the step work-items named by ids`. It is the commit the implementer's `result.json` lists. Its 8 files are those in the report's Budget and in the work-item's fileset. `scripts/migrate_write.py` is in the fileset but unchanged, as the plan allows.

## Removed and weakened tests

None. I checked:
- `git diff b4a211e 0a46dcb --stat -- features/ tests/`: no file under `features/`. `tests/` gets only additions: the new `tests/scenarios/migration_upgrade_steps.py` (+227) and one import line in `test_migration_tools.py`. Nothing was deleted, no parametrize case or assert changed, no skip or xfail added.
- The new Then "it exits with an error" asserts `returncode != 0`. It is a new step, not a weakened one.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test was changed.

## Cannot verify

- The report's suite figures (130 passed, 2 failed in `tests/scripts/test_tools.py` because `--work-item` leaks into a nested pytest). I did not run the suite, as instructed.
- The harness running `hooks/hooks.json`. The scenarios run its command with `shell=True`. This session's own start showed the installed 0.24.0 plugin's hook printing the r22 offer, which supports it, but that run used the installed plugin and not this commit.
- The coordinator's note that "after this work-item the skill delivering-an-initiative must say `work add <initiative> <title>`". It is not done here. Plan D8 sends it to the work-queue work-item that fixes `work add`. The coordinator should confirm it was routed there.

## Checks

- `tools check --base b4a211e`:
  - **ruff**: 44 findings, all style: UP031 percent-format, FURB167 `re.M` aliases, PLW1510 `subprocess.run` without `check`, RUF100 on the existing noqa lines. The same patterns are already in the existing migrate modules. Nothing is a defect.
  - **vulture**: clean.
  - **import-linter**: the project states no import contracts.
- `tools size --limit 300`: printed nothing. Of the touched files, `migration_upgrade_steps.py` is the largest at 227 lines.

## Findings

### F1. Important — fix now — `scripts/migrate_upgrade_ids.py:33` (`initiatives`)
- **What is wrong:** `initiatives` calls `(root / ".shop/work").iterdir()` without checking that the directory exists. On a repository with `.shop/` but no `.shop/work/`:
  - `migrate upgrade` raises FileNotFoundError and rolls back.
  - It prints "migrate put the repository back as it was; it could not make every change: [Errno 2] … .shop/work" and exits 1.
  - `.shop/plugin-version` is never written.
- **Why it matters:**
  - r20 says the pending steps apply. r25 then renumbers zero work-items, and the version should be recorded.
  - Because it never is, the hook (r22) keeps offering an upgrade that always fails.
  - This repository state is the one r19's scenario Given builds (`.shop/records/.keep` only). A repository that `migrate run` moved to the final layout without a `work/` would also be in it.
- **Fix:** have `initiatives` return `[]` when `.shop/work` is not a directory.
- **Reproduction:** probe `test_no_work_dir` with `spec/index.md` and `.shop/records/.keep` committed, then `migrate upgrade`. It returned RC 1 with the message above, and `git log` still shows only `base`.

### F2. Important — observation — `scripts/migrate_upgrade_ids.py:52` (`rewrite_item`)
- **What is wrong:** only a line that starts `blocked_by:` or `depends_on:` is rewritten. A `blocked_by` written as a block list (`blocked_by:` then `  - work-item/a`) keeps the old name, even when it names a work-item of the same initiative. That contradicts r26, and leaves a reference `model check` cannot resolve.
- **Why it is an observation:** `model_parse.frontmatter` accepts block lists, but no work-item in this repository uses one (grep `^(blocked_by|depends_on):\s*$` under `.shop/work`: 0). That makes it hardening.
- **Fix:** also rewrite the `- ` continuation lines that follow those keys.
- **Reproduction:** probe `test_multiline_list` (i1/a.md, and i1/b.md with a block-list `blocked_by: - work-item/a`, then `migrate upgrade`). It returned RC 0, and w2.md still has `  - work-item/a`.

### F3. Minor — observation — `scripts/migrate_upgrade.py:19` and `scripts/migrate_upgrade_ids.py:62`
- **What is wrong:** two inputs crash with a traceback where a refusal that names them belongs:
  - A `.shop/plugin-version` that is not a version: `migrate status --hook` raises ValueError and exits 1, so the hook prints a traceback at every session start, against D3's "always exits 0".
  - A non-JSON line in `log.jsonl`: `migrate upgrade` raises JSONDecodeError. Nothing is written, because the step's plan runs before any write.
- **Why it is an observation:** both are named open cases, and no client writes these inputs today.
- **Fix:**
  - Hook mode: catch the error and stay silent.
  - Upgrade: refuse, naming the file.
- **Reproduction:**
  - Probe `test_bad_version_hook` (`.shop/plugin-version` holding `next`): RC 1, `ValueError: invalid literal for int() … 'next'`.
  - Probe `test_bad_log_line`: RC 1, JSONDecodeError traceback.

### F4. Minor — observation — `scripts/migrate_upgrade_ids.py:71` (`plan`)
- **What is wrong:** a `blocked_by` that names a work-item of another initiative is left with the old name. r26 asks only for the item's own initiative, so this is not a contradiction. But after the upgrade, `model check` would find an unresolved `work-item/<old>`.
  - This repository has candidates for it, e.g. `i10…/feature-file-tools-1.md` `blocked_by: [… work-item/every-scenario-bound]`, which is not an i10 file.
- **Fix:** none needed under r26 as written. Flag it to the person: running the upgrade on this repository may show such references.
- **Reproduction:** probe `test_cross_initiative`. It returned RC 0, and i2/w2.md keeps `blocked_by: [work-item/a]` while `a` became w1.

### Risks checked and cleared
- **Rollback deleting user files:** the rollback is `git reset --hard HEAD` plus `git clean -fdq`. `uncommitted` (migrate_write.py:26) lists untracked files too (`--untracked-files=all`), so the upgrade starts only from a clean tree. The clean therefore removes only what the upgrade made, and ignored files are untouched (no `-x`). No data loss.
- **Renames into an existing `w<n>`:** two-phase `git mv` through `.upgrading-<i>` names, and single-pass regex substitution. No chained renames.
- **Code with no line behind it:**
  - `--hook` comes from the Implementation note and D3.
  - The "upgraded to …" message is a message's words.
  - `status`/`upgrade` refusing outside git follows `run`.
  - None of these is a finding.

## Commands run

- `git log --format=… --grep="^work: migration-tools-1 ready -> claimed$" work/migration-tools-1` (branch gone), then `git log -5 HEAD`
- `git show --stat ff22a77`, `git diff b4a211e ff22a77 -- …`, `git show ff22a77:<each new file>`
- `git diff b4a211e 0a46dcb --stat -- features/ tests/`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base b4a211e`, `… tools size --limit 300`
- grep of `scripts/migrate_write.py` (`uncommitted`), `scripts/model_work.py` (blocked_by), `scripts/model_parse.py` (block lists), `.gitignore`, `.shop/work` (blocked_by forms)
- `python3 -m pytest -q -s -n 0 … .shop/scratch/migration-tools-1-4-review/test_probe.py`: five probes on temp repositories (F1-F4)
