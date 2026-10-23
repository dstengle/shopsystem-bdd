# w98 research: tools check is clean

Accepted: analysis-tools#r16. Tools run as `python3 /home/vscode/shopsystem-bdd/scripts/tools` (the brief's Scripts). `tools map` never run (whole suite), so `tests-of` refused (no map); test coverage below is `by search`. Probes: `.shop/scratch/w98-1-research/` (git-ignored). Ruff and pytest caches written in the worktree (git-ignored; `git status --porcelain` clean).

## 1. Why each scenario is red today

None is red. All six accepted node ids pass (`python3 -m pytest -q <six node ids>` in `tests/scenarios/test_analysis_tools.py`: `6 passed`, run):
- `...runs_each_tool_under_its_own_heading...[ruff|vulture|import-linter]` (3 ids, outline)
- `...with_base_examines_the_changed_python_files...`
- `...with_no_file_to_examine_does_not_fail_for_ruff_and_vulture`
- `...without_import_contracts_does_not_run_importlinter`

The work-item's target is not a scenario: `tools check scripts tests` exits 1 (see 2, probe A). The scenarios use fake ruff, vulture and import-linter (`tests/scenarios/analysis_tools_project.py:61,72`), so they never see the real findings.

## 2. What the system answers today

Probe A: `python3 /home/vscode/shopsystem-bdd/scripts/tools check scripts tests`, run. Exit 1.
- ruff: `Found 690 errors`, 1 `[*]` line: 100 fixable.
- vulture: `tests/scenarios/feature_file_tools_given_steps.py:122: unused variable 'none' (100% confidence)`.
- import-linter: `the project states no import contracts`.

Probe B: ruff statistics, probe `.shop/scratch/w98-1-research/probe_ruff.py` (`ruff check --statistics scripts tests`, run):
UP031 522, PLW1510 49, RUF100 42, I001 29, FURB167 19, UP017 4, UP032 4, RUF015 3, BLE001 2, B023 2, PIE810 2, F401 2, one each: FURB162, PERF102, SIM115, F811, EXE001, FLY002, S110, RUF046, RUF059, RUF007. Sum 690. UP031 is 76% of them.

Probe C: vulture alone, `--min-confidence 80 scripts tests` (same probe): the one line above, RC 3.

Probe D: ruff settings source, probe `probe_ruff2.py` (`ruff check --show-settings`, run). The settings print no config path. Glob for `ruff.toml`, `.ruff.toml`, `pyproject.toml` under the worktree and its parent work-run directory: none (run). The rule set in use (UP, PLW, FURB, I, RUF...) is not ruff's default, so it comes from a config outside the checkout. I could not list `~/.config/ruff` (blocked), so the file is unidentified (read).

Probe E: `tools check --base HEAD` (no changed files), run. `== ruff == nothing to check`, `== vulture == nothing to check`, `== import-linter == the project states no import contracts`. Exit 0.

Probe F: `tools check --base nosuchref`, run. Exit 1: `tools: fatal: bad revision 'nosuchref'`.

Probe G: `tools check tests/scripts/stub_claude.py`, run. ruff: EXE001 (shebang, not executable), UP031 x3; vulture clean; exit 1.

Probe H: `tools size --limit 300`, run: no output, so no tracked Python file is over 300 lines.

Probe I: `tools tests-of scripts/tools_check.py:cmd_check --by-file`, run: `tools: no map: make one with tools map`, exit 1.

Probe J: `python3 -m pytest -q -o addopts="" tests/scripts/test_tools.py`, run: 3 passed, 2 failed, 1 skipped. The two failures are the map tests, `test_the_map_says_which_tests_execute_a_function` and `test_untested_names_each_function_no_test_executed`. The map's inner pytest prints `SystemExit: --work-item w98: no such work-item under .shop/work/`. Source of the work-item argument not identified (env of this session, read). See 6.

## 3. Old assumptions

No requirement changes. The one place that depends on the rule set:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/tools_check.py:cmd_check | runs `python -m ruff check --output-format=concise` with no config argument; ruff's config discovery sets the rules | a repo ruff config would set the rules of every run in this checkout; it must spell out the rules it keeps, or they change (read) | tests/scripts/test_tools.py:test_check_heads_each_tool_and_names_a_missing_one (run: not among the 2 failures) | by search (`ruff`, `vulture` in tests) |
| tests/scenarios/analysis_tools_project.py:72 | replaces ruff and vulture with fakes | unaffected by any ruff config | the six accepted scenarios (run: pass) | by search |

## 4. Tests the requirements make impossible to keep

`tests-of` unavailable (no map). By search: `tools check`, `cmd_check`, `ruff`, `vulture`, `import-linter` in `tests/`.

- tests/scripts/test_tools.py:test_check_heads_each_tool_and_names_a_missing_one (run: not failing): asserts the three headings and the import-linter line only. Survives every planned edit to `tools_check.py`.
- tests/scenarios/test_analysis_tools.py and analysis_tools_code_steps.py, analysis_tools_project.py (run: 6 pass): fake tools; survive. Lines 76 and 191 of `analysis_tools_code_steps.py` are PLW1510 targets; `check=` changes nothing.
- tests/scenarios/feature_file_tools_given_steps.py:121-122, the vulture `none` (by search, read): `@given(parsers.re(...(?P<none>no tag line)))` gives pytest-bdd a keyword `none`. Removing or renaming the parameter raises TypeError on the "no tag line" step. Its fix must keep the name, using it (e.g. `del none`), or the finding stays. Any test of "no tag line" fails if the parameter goes (read).
- tests/scenarios/analysis_tools_map_steps.py:140 and 180, `map_kept` defined twice (F811): only the definitions name it (by search). Renaming the second one is safe (read).
- tests/scripts/stub_claude.py (EXE001): run by `exec <python> <stub>` (tests/scenarios/supervision_given.py:34, by search), so the shebang and the executable bit are never used. Removing the shebang, or adding the bit, changes nothing (read).
- Other fixes (`check=`, `datetime.UTC`, `re.IGNORECASE`, f-strings, I001 import order, removing unused noqa, RUF059 unused `why` in tools_check.py:9): read as behaviour-neutral. Not searched for tests that assert the source text. I001 reorders imports in `tests/scenarios/*` and `conftest.py`, where pytest-bdd and the `work_items` plugin load modules: import order is a risk, unchecked (read).

## 5. A step the work-item skips

none. The work-item adds no path; it edits lint findings and config.

## 6. Defects

D1. `tools map` inside a `work run` session fails its own tests.
Reproduce: `python3 -m pytest -q -o addopts="" tests/scripts/test_tools.py` (run). Output: `tools: no map was made by: .../python3 -m pytest -q -p no:cacheprovider -n 0 --cov=. --cov-context=test ...` then `SystemExit: --work-item w98: no such work-item under .shop/work/`. The worktree has `.shop/work/i22-rulings-round-trips-query-output/w98.md`, not `.shop/work/w98`. Cause: the work-item is set in this session's environment, which I did not inspect; not confirmed as a repository defect. Outside the work-item's scope; noted for the plan.

## 7. The file set

Changes (all 91 files with findings, probe A + B, by run; no finding in other files):

Config (new): a ruff config in the checkout that leaves UP031 (the work-item's own permission). The checkout has none today (Glob, read). It must spell out the rules kept, since a project config replaces the outside config (read).

Stub mode: tests/scripts/stub_claude.py (EXE001) needs a mode change or shebang removal; not writable from the research shell.

scripts (30): workqueue (27 findings), supervise_faults (20), supervise_worker (18), migrate_ledger (18), supervise (16), supervise_merge (15), migrate_upgrade_ids (15), supervise_brief (14), tools_map (13), migrate_upgrade (12), tools_env (11), migrate_write (10), migrate_layout (9), features_edit (9), features_bindings (9), measure_read (8), features_report (8), features_gherkin (8), migrate_spec (7), measure_show (7), measure_build (7), tools_refs (6), tools_check (6), work_items (5), supervise_review (4), measure_write (4), tools_size (2), model_parse (1), model_facts (1), model_check (1).
Lines and room (300 - lines): workqueue 255/45, supervise_faults 160/140, supervise_worker 210/90, migrate_ledger 123/177, supervise 263/37, supervise_merge 132/168, migrate_upgrade_ids 119/181, supervise_brief 97/203, tools_map 126/174, migrate_upgrade 137/163, tools_env 105/195, migrate_write 126/174, migrate_layout 131/169, features_edit 131/169, features_bindings 170/130, measure_read 109/191, features_report 116/184, features_gherkin 175/125, migrate_spec 132/168, measure_show 76/224, measure_build 112/188, tools_refs 50/250, tools_check 34/266, work_items 109/191, supervise_review 77/223, measure_write 41/259, tools_size 46/254, model_parse 271/29, model_facts 265/35, model_check 139/161.

tests/scenarios (45): analysis_tools_code_steps 223/77, analysis_tools_map_steps 268/32, analysis_tools_probe_steps 258/42, analysis_tools_project 183/117, analysis_tools_size_steps 68/232, batch_measurement_given_steps 177/123, batch_measurement_show_steps 68/232, batch_measurement_then_steps 158/142, batch_measurement_world 132/168, conftest 176/124, design_model_check_clingo 139/161, design_model_check_given 229/71, design_model_check_glossary 154/146, design_model_check_problems 288/12, design_model_check_reading 217/83, design_model_check_then 221/79, design_model_check_trace 244/56, feature_file_tools_check_steps 88/212, feature_file_tools_edit_steps 229/71, feature_file_tools_files 85/215, feature_file_tools_given_steps 208/92, feature_file_tools_json_steps 90/210, feature_file_tools_refusal_steps 155/145, feature_file_tools_tree_steps 163/137, migration_ledger_steps 227/73, migration_old 81/219, migration_safety_steps 120/180, migration_spec_steps 209/91, migration_upgrade_steps 269/31, supervision_faults_steps 186/114, supervision_given 232/68, supervision_review_steps 96/204, supervision_then_workers 276/24, supervision_tests_steps 163/137, supervision_world 172/128, test_analysis_tools 71/229, test_batch_measurement 14/286, test_design_model_check 53/247, test_feature_file_tools 109/191, test_migration_tools 226/74, test_supervision 236/64, test_work_queue 277/23, work_queue_add_steps 60/240, work_queue_git_steps 59/241, work_queue_withdraw_steps 64/236.

tests/scripts (16): stub_claude 206/94, test_agents 88/212, test_bound 32/268, test_features 178/122, test_features_deprecating 150/150, test_features_scenarios 172/128, test_migrate_layout 46/254, test_migrate_upgrade_ids 79/221, test_migrate_write 80/220, test_model 213/87, test_model_output 74/226, test_model_reading 247/53, test_tools 134/166, test_work_add_title 50/250, test_work_items 98/202, test_work_withdraw 32/268.

Module path, unchanged or changed: scripts/tools (112 lines, room 188; the dispatcher, edited only if a config path is added) -> scripts/tools_env.py (105/195, `probed`) -> scripts/tools_check.py (34/266, cmd_check).

Tightest room: design_model_check_problems.py 288/12, test_work_queue.py 277/23, supervision_then_workers.py 276/24, model_parse.py 271/29, migration_upgrade_steps.py 269/31. Nothing is over 300 (probe H).

File count: 91 Python files, from probe B's tally (`grep -o` of probe A, run).
