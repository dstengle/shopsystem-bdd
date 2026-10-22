# Research of w1: upgrade step "work-items named by ids", migration-tools r26

Method: no map (`tools tests-of` answers "no map: make one with tools map"), so tests are found `by search`; `tools refs` not run. Checkout is HEAD 8014407 (the brief's Base 202c029 is older). Probes ran only in throwaway repos under `.shop/scratch/w1-1-research/`. `git status --porcelain` empty at the end.

Accepted scenarios (features/migration-tools.feature, @r26): S1 "renames a work-item's file and stage directories..." (line 483); S2 "rewrites a reference from another initiative and a for:..." (line 497).

## 1. Why each scenario is red today

- S1: `python3 -m pytest -q "tests/scenarios/test_migration_tools.py::test_the_upgrade_step_workitems_named_by_ids_renames_a_workitems_file_and_stage_directories_and_rewrites_its_name_where_its_initiative_names_it"` : passed (run). Not red.
- S2: `python3 -m pytest -q "tests/scenarios/test_migration_tools.py::test_the_upgrade_step_workitems_named_by_ids_rewrites_a_reference_from_another_initiative_and_a_for_to_the_id_of_the_workitem_they_name"` : fails (run) with `StepDefinitionNotFoundError: Given "work-items .shop/work/i1/delivery-1.md, .shop/work/i2/delivery-1.md and .shop/work/i2/size-check.md"` (feature line 500).
  - Missing steps (read): `tests/scenarios/migration_upgrade_steps.py` has only the literal `work-items .shop/work/i10/a.md, ...` (line 75). No step for feature line 501 ("a work-item whose blocked_by names size-check and whose for names size-check") nor line 502 ("a work-item whose depends_on names delivery-1"). pytest-bdd stops at the first undefined step, so 501 and 502 are read, not run.
  - Code behind it, even with steps (run, see §2 P1): `scripts/migrate_upgrade_ids.py` `plan` (lines 74-78) builds `names` per initiative; `rewrite_item` (lines 53-56) rewrites only `blocked_by`/`depends_on` lines, never `for:`.

## 2. What the system answers today (probes)

Probe file: `.shop/scratch/w1-1-research/probe_upgrade_refs.py`. Command: `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w1-1-research/probe_upgrade_refs.py` (run, 6 passed). Each builds a repo of the S2 shape, commits it, runs `python3 scripts/migrate upgrade` in it.

- P1 `test_scenario_2_as_written` (S2's Givens, built as the feature says). rc 0, "upgraded to 0.24.0". i1 delivery-1 -> w1; i2 delivery-1 -> w2, size-check -> w3; i2 tests `depends_on: [w2]` (correct, own initiative's name). i3 docs keeps `blocked_by: [size-check]` and `for: size-check`; S2 expects w3 in both. (run)
- P2 `test_name_held_by_two_others_not_own_refused_by_r7`: i1 and i2 hold delivery-1, i3 docs `blocked_by: [delivery-1]`. rc 0, no message, blocked_by unchanged. r7 says refuse naming the change, change no file. (run)
- P3 `test_name_held_only_by_other_initiative`: size-check only in i2, i3 docs `blocked_by: [size-check]`. rc 0, unchanged (dangling after upgrade). (run)
- P4 `test_for_as_block_list`: i1 docs `for:` with `  - size-check`, size-check in i1 -> w2. `for:` unchanged. (run)
- P5 `test_for_scalar_same_initiative`: `for: size-check` in i1, same. Unchanged. (run)
- P6 `test_qualified_work_item_form_in_blocked_by`: `blocked_by: [work-item/acme/shop/x/size-check]` -> `[work-item/acme/shop/x/w2]`. Correct. (run)
- Not probed, read: no `.shop/plugin-version` taken as 0.23.1 (`migrate_upgrade.py` `repository_version`, lines 26-28); no `.shop/work/` gives an empty plan (`migrate_upgrade_ids.py` `initiatives`, lines 32-33); uncommitted tree refused, naming the paths (`migrate_upgrade.py` `upgrade`, lines 81-85). The existing unit test `test_a_repository_with_shop_and_no_work_directory_records_the_version` (by search) covers the second.

## 3. Old assumptions

A bare name is unique within its initiative, and a reference resolves inside its own initiative. Places still making it:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/migrate_upgrade_ids.py:plan (74-78) | `names` built per initiative; a name resolves only in its own initiative | resolve own initiative first, else the one initiative holding it, else refuse (r26, r7) | S1 test and tests/scripts/test_migrate_upgrade_ids.py (by search) | read, run P1-P3 |
| scripts/migrate_upgrade_ids.py:rewrite_item (42-57), pattern at 48 | renames only names in `names` (own initiative) | must take the resolved name map of the referring item's initiative, across the context | S1 test (depends_on in own initiative) (by search) | run P1 |
| scripts/migrate_upgrade_ids.py:rewrite_item (53-56) | only `blocked_by:`/`depends_on:` lines | `for:` too, scalar and block list (r26) | none (no test has `for:`) | run P4, P5 |
| scripts/migrate_upgrade_ids.py:plan (no refusal path, returns Changes only) | never refuses; a name held by several initiatives is resolved silently | refuse naming each change, change no file (r7) | none | run P2 |
| scripts/migrate_upgrade_ids.py:rewrite_log (60-69) | renames `work-item` fields of the own initiative's log using the own map | keep; the map must be the global resolution (see row 1) | S1 test (by search) | read |
| scripts/model_work.py:read_work (178-197) | reads `for`, `blocked_by`, `depends_on` values through `qualify` | unchanged; after the step the values are `work-item/<ctx>/w<n>` | none searched | read |
| scripts/model_work.py:check_work_item_name (84-88) | file must be `w<n>.md`, id unique | the step makes it true; un-upgraded repos fail it | not searched | read |
| scripts/workqueue.py:highest (61-65), add (79) | next `w<n>` = highest `w<n>.md` under `.shop/work/` plus one | consistent with r25 numbering, nothing to change | by search: tests/scenarios/work_queue_add_steps.py | read |

## 4. Tests the requirements make impossible to keep

None found (by search, no map). Searched `tests/` for `blocked_by`, `depends_on`, `for:` and the step's names. Only two tests assert the step's behaviour, and both stay true under r26 (read):
- tests/scripts/test_migrate_upgrade_ids.py::UpgradeRecordsTheVersion::test_a_blocked_by_written_as_a_block_list_follows_the_rename: one initiative, asserts `  - work-item/w1` (r26 keeps this).
- tests/scenarios/migration_upgrade_steps.py: `depends_on: [size-check]` in the same initiative (lines 91-93), asserts `depends_on: [.../w2]` (r26 keeps this).
No test asserts that a cross-initiative or `for:` reference is left unchanged. S1's Then steps (migration_upgrade_steps.py 199-227) pass today and stay true.

## 5. A step the work-item skips

The upgrade path (`migrate_upgrade.py` `upgrade` -> `apply`) does not call `check_moves` (`migrate_write.py` line 47), which `migrate run` calls (`scripts/migrate` `cmd_run`). Only that check produces these refusals, all read:
- a move onto a file that exists, tracked or not (`check_moves` line 61), named;
- two sources to one destination, named;
- a write onto a file git does not hold, or through a symbolic link (line 50 in the docstring).
Under upgrade, a collision instead fails inside `git mv` (CalledProcessError), caught at `migrate_upgrade.py` lines 98-103: the repository is reset with `git reset --hard` and `git clean -fdq`, and the message does not name the change (r7 asks for it). Not probed (read).

## 6. Defects

Reproduce each with: `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w1-1-research/probe_upgrade_refs.py` (run).

- D1: a reference from another initiative is not rewritten. `test_scenario_2_as_written`: i3 `docs` keeps `blocked_by: [size-check]` and `for: size-check`; `size-check` is w3 in i2. Expected w3.
- D2: `for:` is never rewritten, scalar or block list. `test_for_scalar_same_initiative` (`for: size-check` stays; size-check is w2) and `test_for_as_block_list`.
- D3: a name held by several initiatives, none the naming item's own, is left as it is and the upgrade exits 0. `test_name_held_by_two_others_not_own_refused_by_r7`: `blocked_by: [delivery-1]` stays, "upgraded to 0.24.0". r7 says refuse.
- D4 (follows from D1, D3): a name held only elsewhere (`test_name_held_only_by_other_initiative`) is left dangling after a successful upgrade.

## 7. The file set

- scripts/migrate_upgrade_ids.py (93 lines; room 207): `plan` resolves names across the context (own initiative first, else the one holder, else refuse); `rewrite_item` also rewrites `for:` (scalar and list); plan returns failures (r7). Found: read, probes P1-P5.
- scripts/migrate_upgrade.py (119 lines; room 181): `upgrade` refuses and names plan failures and changes nothing (r7). Found: read `upgrade` lines 80-105.
- scripts/migrate_write.py (126 lines; room 174): may change, so upgrade can reuse `check_moves` (section 5). Found: read.
- tests/scenarios/migration_upgrade_steps.py (227 lines; room 73): three Givens for S2 (the literal lines, and the blocked_by/for and depends_on steps) and the Then for `blocked_by` and `for`. Found: feature lines 500-505, step file lines 75-100 (no matching step). Keep the file under 300.
- tests/scripts/test_migrate_upgrade_ids.py (53 lines; room 247): unit cases for cross-initiative, `for:`, and the refusal. Found: read.
- Not changed: scripts/migrate (71 lines; room 229), scripts/model_work.py, scripts/workqueue.py, tests/scenarios/test_migration_tools.py (226 lines), read: its scenario function already exists.

Size limit: `CLAUDE.md` gives 300 lines (`scripts/tools size --limit 300`). Room above is 300 minus the count.
