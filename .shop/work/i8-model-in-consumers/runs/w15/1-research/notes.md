# migration-rebind-2 research (r6-r9, 12 scenarios)

**Checkout changed by my probe.** At 16:54:34-35 my probe `probe_migrate.py::test_outside_git` ran `scripts/migrate run` with its cwd outside any repo; git found the checkout's own repo and migrate rewrote and staged it. `git diff --cached --stat`: 150 files, 165+/165-, e.g. `spec/index.md` id now `bounded-context/example.org/acme/shop`. The checkout is not as it was at start. I did not undo it (reset/checkout/add are barred). It needs restoring to HEAD by an operator. Cause and defect: part 6.

Method: `scenario runs` = `python3 -m pytest -q tests/scenarios/test_migration_tools.py` (the --work-item filter collects 23 of 58). `refs`, `wc`, `read`, `search` as marked. `tests-of`: no map (`tools: no map`), so no test lists come from it; searches are marked `by search`.

## 1. Why each scenario is red today

Run: `python3 -m pytest -q --tb=line -rf tests/scenarios/test_migration_tools.py`. Result: 13 failed, 10 passed (run).

- 12 scenarios fail at the step `Then "it exits with an error"`: StepDefinitionNotFoundError (run). No step defines that text; `test_migration_tools.py:215` defines only `it exits non-zero`. Scenarios: feature lines 121 (2 Examples), 135 (4), 218, 229, 387 (3), 402.
- 1 scenario fails with FileNotFoundError at `spec/decisions/0001-x.md` (run): feature 355 (`gives a decision file whose id is decision/<nnnn>-<name>`). Its Given, `migration_safety_steps.py:56-59`, writes `decisions/0001-x.md` with no `old.commit()`. The file is untracked, so migrate refuses at its r15 check and moves nothing (read; probe 2 in part 2 confirms the refusal for an untracked file).
- The other 10 pass (run): r6 x4 (line 203), r8 (238), r9 type-first (258), r9 short form (273), r9 README x3 (280).
- Behind the missing step: migrate's refusal path is correct. Every message the Thens expect appears (part 2, run).

## 2. What the system answers today

Probes: `.shop/scratch/migration-rebind-2-1-research/probe_migrate.py` (run `python3 -m pytest -q -s -p no:xdist --whole-suite -o addopts= --confcutdir=.shop/scratch/migration-rebind-2-1-research <path>`; `--whole-suite` is needed because `--work-item` comes from the environment). Each repo is a throwaway git repo under the scratch dir. All rc and messages below are `run`.

1. finds before (`Notes on the ledger.` + entry): rc 1, `could not replace the ledger text "Notes on the ledger." outside its entries in spec/decisions.md`; no change. Matches the Then.
2. finds heading twice: rc 1, `could not replace the ledger entry `## decision/0007-a`, which is there twice`. Matches.
3. land on relocated `decisions/0007-a.md`: rc 1, `could not write spec/decisions/0007-a.md for the ledger entry `## decision/0007-a`: decisions/0007-a.md moves there`. Matches.
4. land on tracked `spec/decisions/0007-a.md`: rc 1, `... : a file is there`. Matches.
5. land on untracked `spec/decisions/0007-a.md`: rc 1, two lines: r15 `could not start from a tree with an uncommitted change: spec/decisions/0007-a.md` and the same `a file is there` line. Matches. Nearest case: r15 fires first, so the r7 line is not the only one.
6. land `decisions/0008-b.md` (ledger `## decision/b`, numbered 0008): rc 1, `could not write spec/decisions/0008-b.md for the ledger entry `## decision/b`: decisions/0008-b.md moves there`. Matches.
7. two changes (committed plans in `records/` and `docs/superpowers/`, untracked `.shop/work/i1/w1.md`): rc 1, three lines: r15, `could not move both docs/superpowers/plans/p1.md and records/archive/plans/p1.md to .shop/records/archive/plans/p1.md`, `could not move work/i1/w1.md onto .shop/work/i1/w1.md`. The Then regex matches. Nearest: the Given (`migration_*`: test_migration_tools.py:182-185) never commits, so r15 fires too (read; the probe commits the plans only).
8. relocate onto untracked `.shop/work/i1/w2.md`: rc 1, r15 line plus `could not move work/i1/w2.md onto .shop/work/i1/w2.md`. Matches.
9. outside git (in a true non-repo dir, `probe_outside.py`): rc 1, `could not find a git repository at <dir>`; nothing changed. Matches. The earlier run in `probe_migrate.py` that gave rc 0 was not outside a repo (see part 6).
10. decision file id, committed `decisions/0001-x.md`: rc 0, `R decisions/0001-x.md -> spec/decisions/0001-x.md`, id `design-decision/example.org/acme/shop/x`. Migrate is correct; the scenario failure is the uncommitted Given (part 1).
11. symlink plan (`docs/superpowers/plans/p1.md` tracked link out of repo): rc 1, `could not change docs/superpowers/plans/p1.md: it is a symbolic link`. Matches. Nothing changed.
12. ignored `spec/decisions/index.md`: rc 1, `could not write spec/decisions/index.md: a file git does not hold is there`. Matches.
13. ignored `.shop` file: rc 1, `could not move work/i1/w1.md to .shop/work/i1/w1.md: .shop is not a directory`. Matches.

The r6 scenarios and r8/r9 passing cases were run by pytest only (10 pass); I did not probe `model check` beyond that.

## 3. Old assumptions

Requirements r6-r9 are already what the code does (part 2). The rows are the old forms the code still reads or writes.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/migrate_spec.py:plan_capabilities (line 41) | strips `formulated_as:` before writing the capability | r6: model reads no `formulated_as`; the strip is what makes r6 hold | `tests/scenarios/design_model_check_problems.py:58-60` asserts model's problem for `formulated_as` (not via migrate); migrate's strip itself: `none` (no test of plan_capabilities found) | search (`grep formulated_as`) |
| scripts/model_facts.py:184-185 | flags `formulated_as` as a problem | r6 relies on migrate removing it; model still flags it, which is correct | design_model_check_problems.py:58-60 | search |
| scripts/model_facts.py:82-85 | accepts `capability/<name>`, `capability/<path>/<name>`, `<name>` | r9 writes only the full form; the short form is still read, so nothing breaks | not checked (no map) | search |
| scripts/model_facts.py:20 OLD_LAYOUT | model's list of what migrate moves: `spec/decisions.md`, `decisions/`, `work/`, `records/` | r8 adds `docs/superpowers/*` and `adrs/` to what migrate moves, not to this list; model check does not flag leftovers there | not checked (no map) | search |
| scripts/migrate_ledger.py:70-84 `REFERENCE`, `supersedes_of` | reads `decision/\S+` old ids in `supersedes` | r9/r13: renamed by `plan.renamed` before use; works today (scenario r5 passes via run of the Given) | `tests/scenarios/test_migration_tools.py` (ledger steps) — not run separately | read |
| scripts/migrate_layout.py:DIRECTORY_MOVES (8-16) | old dir -> final dir, including `docs/superpowers/*` and `adrs/` | r8/r14 requirement, already there | scenario r8 and r14 steps (r8 passes; r14 not accepted) | read |
| scripts/model_work.py, model.lp, workqueue.py, supervise_faults.py | `decision/`, `formulated_as`, `capability/` matches are comments or work-queue paths | none | none | search |

## 4. Tests the requirements make impossible to keep

- `tests-of` unavailable (no map). By search:
- `tests/scripts/test_migrate_write.py` (7 tests with layout, 7 passed run) and `test_migrate_layout.py`: the accepted r7/r9 behaviour is what they assert; they keep passing. Checked: all 7 pass (run, `--whole-suite`).
- `tests/scenarios/design_model_check_problems.py:58-60`: asserts model reports `formulated_as`; the requirement changes migrate, not model; keeps passing (read).
- Nothing else found that asserts the old behaviour of the accepted lines. None: I looked at the 10 green scenarios (run) and the step modules (read).

## 5. A step the work-item skips

- `migrate` refusal at line 34-35 of `scripts/migrate` (a tracked file that is gone): it returns before `plan_moves`, so the r7 names of the other changes are not printed (read). Only the r15 line is shown in that case.
- write() `git reset --hard HEAD` on failure (migrate_write.py:119) does not remove ignored files written by migrate (read). The r15 check excludes ignored files, so it would not refuse.

## 6. Defects

### D1 — migrate run outside a repository operates on the enclosing repository (run)

Repro: `probe_migrate.py::test_outside_git` (its `repo` ceiling set to the cwd itself, so git still finds the enclosing checkout). Command: `python3 scripts/migrate run --context example.org/acme/shop` with cwd = a dir in `.shop/scratch/.../nogit` under the checkout.
Came back: rc 0, no output. The checkout's `spec/index.md`, `spec/decisions/index.md` and 148 others were rewritten and staged (part 0, 16:54:34). Expected rc 1 `could not find a git repository` (as `probe_outside.py` shows when its dir really has no repo).

### D2 — r15 check and fixture commits (read, test-side)

The Givens at `test_migration_tools.py:182-185` and `migration_safety_steps.py:56-59` do not commit, so migrate refuses on r15 and the scenario's own subject is never moved. The `two changes` scenario still passes its Thens by substring; the r9 decision-id scenario fails (run).

## 7. The file set

Changes the scenarios need:
- `tests/scenarios/test_migration_tools.py` (225 lines; room 75): add `@then("it exits with an error")` asserting `returncode != 0`. Also commit after the Givens at 182-185.
- `tests/scenarios/migration_safety_steps.py` (120; room 180): commit after writing `decisions/0001-x.md` at 56-59.
- Production: none needed for the 12 scenarios (part 2: each passes its Then via the CLI).

Other file on the change path (read): `tests/scenarios/migration_old.py` (81; room 219) unchanged. `tests/scripts/test_migrate_write.py` (80) and `test_migrate_layout.py` (46) unchanged; they match no file-set glob but keep passing (7 passed, run).

Modules on the path, unchanged, with lines (`wc -l`) and room under 300:
- scripts/migrate: 63 (237)
- scripts/migrate_layout.py: 131 (169)
- scripts/migrate_ledger.py: 123 (177)
- scripts/migrate_spec.py: 132 (168)
- scripts/migrate_write.py: 126 (174)
- scripts/model (loaded by path): 132 (168)
- scripts/features (run by subprocess for `deprecate`): 143 (157)
- tests/scenarios/migration_ledger_steps.py: 227 (73); migration_spec_steps.py: 209 (91)

`tools size --limit 300` (run): over the limit, not on this path: `scripts/measure` 644, `tests/scripts/test_measure.py` 700.
