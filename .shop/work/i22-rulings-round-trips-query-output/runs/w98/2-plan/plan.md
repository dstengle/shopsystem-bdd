# Plan of w98: tools check is clean

## 1. What goes green

analysis-tools#r16. Its accepted scenarios in `features/analysis-tools.feature`:
- Scenario Outline: `tools check` runs each tool under its own heading and fails when any finds something (ruff, vulture, import-linter)
- `tools check` with --base examines the changed Python files that remain, in place of the paths given
- `tools check` with no file to examine does not fail for ruff and vulture
- `tools check` without import contracts does not run import-linter

None is red today. All six node ids pass (notes 1), because the scenarios run fake ruff and vulture. The work-item's own target is red: running `python3 scripts/tools check scripts tests` in this repository exits 1. Ruff reports 690 findings (UP031 522, PLW1510 49, RUF100 42, I001 29, FURB167 19, and a tail of others; notes 2, probe B). Vulture reports one: the unused `none` in tests/scenarios/feature_file_tools_given_steps.py:122. Import-linter reports no contracts, which does not fail. The work is done when that command exits 0, the six scenarios still pass and no behaviour changes.

The work-item retires no scenarios.

## 2. Where the change lands

There are 92 files: the researcher's 91 Python files with findings (notes 7) and one new config file.

- `ruff.toml` (new, at the repository root): the project's ruff config. It spells out the rule set ruff applies today and ignores UP031 (decision D1).
- `tests/scripts/stub_claude.py`: the shebang is removed for EXE001 (D5), and its UP031 lines are left alone.
- `tests/scenarios/feature_file_tools_given_steps.py`: the `none` parameter is kept and used (D4), and the file's other findings are fixed.
- `tests/scenarios/analysis_tools_map_steps.py`: the second `map_kept` gets a new name (D6), and the file's other findings are fixed.
- `scripts/tools_check.py`: RUF059 (the unused `why`) and the other findings are fixed. `cmd_check` is unchanged: ruff finds the project config by its own discovery, so it needs no config argument.
- In every other file, the findings are fixed in a way that changes no behaviour (D2, D3):
  - scripts: workqueue, supervise_faults, supervise_worker, migrate_ledger, supervise, supervise_merge, migrate_upgrade_ids, supervise_brief, tools_map, migrate_upgrade, tools_env, migrate_write, migrate_layout, features_edit, features_bindings, measure_read, features_report, features_gherkin, migrate_spec, measure_show, measure_build, tools_refs, work_items, supervise_review, measure_write, tools_size, model_parse, model_facts, model_check (each `scripts/<name>.py`).
  - tests/scenarios: the other 43 modules of notes 7, including tests/scenarios/conftest.py (176 lines). The root conftest.py is not in the set.
  - tests/scripts: the other 15 modules of notes 7.

`scripts/tools` is not in the set, because no config path is passed (D1).

## 3. Decisions

- **D1. The config lives in the checkout and keeps today's rules except UP031.** Add a root `ruff.toml`. A project config replaces the outside config that sets the rules today, which the researcher could not identify (notes 2, probe D). So the new file must list the rules ruff runs today, which `ruff check --show-settings` prints, and add UP031 to the ignore list. It must not fall back to ruff's defaults. The work-item permits this ("configure ruff to leave it"). The report says UP031 is left by config and why: % formatting is the code's chosen style throughout. Rests on analysis-tools#r16 (ruff runs over the paths given, and whatever it finds fails) and on the work-item's own text.
- **D2. Every other ruff rule is fixed, not ignored.** Only UP031 meets the work-item's test of "a style the code keeps on purpose throughout". PLW1510 gets an explicit `check=False`, because the code reads return codes itself. RUF100 removes the unused noqa comments. I001, FURB167, UP017, UP032 and the rest of the tail are fixed in the form each rule suggests. Rests on the work-item ("Change no behaviour") and analysis-tools#r16.
- **D3. Where a fix would change behaviour, add a line-level noqa instead.** This applies to BLE001, S110 and SIM115, where narrowing an exception or moving a file into a with block could change what happens. Each noqa names its rule. Rests on the work-item ("Change no behaviour").
- **D4. The vulture `none` stays a parameter and is used.** pytest-bdd passes it as a keyword from the regex group, so removing or renaming it raises TypeError on the "no tag line" step (notes 4). The step body uses it (the researcher suggests `del none`). No vulture whitelist file is added. Rests on analysis-tools#r16.
- **D5. stub_claude.py loses its shebang rather than gaining the executable bit.** It is always run as `exec <python> <stub>` (notes 4), so the shebang is never used, and this is a plain file edit. It stays a Python file under r50 through its `.py` extension. Rests on analysis-tools#r50 and #r16.
- **D6. F811: the second `map_kept` (analysis_tools_map_steps.py:180) gets a name of its own.** Only the step decorators bind it to step text (notes 4). Rests on analysis-tools#r16.
- **D7. The size limit stays.** No file goes over 300 lines (CLAUDE.md). The tightest file is design_model_check_problems.py at 288 lines. Explicit `check=False` and noqa additions must not wrap lines past the limit.

## 4. Tests the decisions break

None. Here is what I checked against the notes (by search, since `tests-of` was refused without a map):
- tests/scripts/test_tools.py:test_check_heads_each_tool_and_names_a_missing_one asserts the headings and the import-linter line, not the rule set. It runs on its own project, outside this repository's ruff.toml, so D1 leaves it as it is.
- The six r16 scenarios use fake tools (analysis_tools_project.py:61,72), so D1 to D3 do not reach them. Adding `check=False` at analysis_tools_code_steps.py:76 and :191 changes nothing.
- The "no tag line" steps keep their `none` keyword under D4.
- `map_kept` is named only at its definitions, so D6 breaks no reference.
- stub_claude.py is run through the interpreter, so D5 leaves supervision_given.py:34 working.
- One known failure is not caused by this plan: the map tests in test_tools.py fail inside this work-run session with `--work-item w98: no such work-item` (notes 6, D1). That failure is in the environment, outside the work-item. It must not be counted against this change, and the change must not touch it.

## 5. Open cases

- I001 reorders imports in tests/scenarios modules and tests/scenarios/conftest.py, where pytest-bdd and the work_items plugin load modules. If a reorder changes how a module loads or registers steps, the implementer names the case and how it was kept.
- For each B023 (loop variable in a closure, 2 findings), the implementer says whether the closure runs after its loop iteration, which would make it a real defect and not a style point, and how it was handled without changing behaviour.
- RUF100 may flag a noqa that the outside config never used but that another ruff version would need. The implementer names any noqa removed that matters elsewhere.
- If `--show-settings` prints settings beyond the rule list (line length, target version), the implementer names which ones the new ruff.toml carries over.
