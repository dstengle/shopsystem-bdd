# w95 research: analysis tools answer in their output

Work-item `w95` under `analysis-tools`, accepts `analysis-tools#r11, r53-r57`.
Tools: `python3 /home/vscode/shopsystem-bdd/scripts/tools` (the brief's `Scripts:`); `tests-of`/`untested` have no map in the worktree, so their answers are by search and by probe.
Probe files: `.shop/scratch/w95-1-research/probe_tools.py`, `probe_refusals.py`, `probe_scenarios.py`.
Session env: `PYTEST_ADDOPTS=--work-item w95` (printed by a probe, run). It leaks into any `tools map` run.

Accepted scenarios (features/analysis-tools.feature): 7 scenarios, the deprecated outline counted once per row.
- L124 @r11 @deprecated outline (2 rows): tests-of fails when nothing executed / function missing (deprecated)
- L138 @r11: tests-of says no test executed it and exits successfully
- L419 @r53, L428 @r54, L436 @r55, L447 @r56: the four `--json` scenarios
- L455 @r57: tests-of fails when the file has no function by the name given

## 1. Why each scenario is red today

Run: `python3 -m pytest -q -n 0 <node id>` per scenario (probe_scenarios.py, PYTEST_ADDOPTS removed). Run.

- **deprecated outline, row "unused" (L124)**: PASSES today. Old behaviour: exit 1 with `0 of the 1 tests in the map executed src/cart.py:unused`. Conflicts with r11 (exit 0). See part 6/ruling note.
- **deprecated outline, row "missing" (L124)**: PASSES today (exit 1, stderr `has no function named missing`).
- **L138 "says that no test of the map executed the target and exits successfully"**: RED at the Given. `a map of 5 tests made at commit abc1234` (map_steps.py:20) only stores a plan; `no test in the map executed the function unused in src/cart.py` (map_steps.py:66, pattern `{name}`) captures `unused in src/cart.py` and calls `put` on a non-repo: `fatal: not a git repository` (project.py:93). Missing: a project set-up in that step, the 5-test map, the label `abc1234` wired into `context["commits"]`, and a step for `tools prints that no test of the map executed it` (undefined). Code: `tools_map.py:cmd_tests_of` lines 109-110 print `N of the M tests ... executed` and return 1 when nothing ran (`return 0 if tests else 1`).
- **L419 `--json` tests-of**: RED at the Given: `StopIteration` at map_steps.py:38: `executed_target` matches the target against FORMS prefixes (`the file`, `the function`...), and the scenario says `src/cart.py`. Then `tools prints one JSON object` and `the object gives ...` are undefined. Code: `scripts/tools` tests-of subparser (line 84-87) has no `--json`; `tools_map.py:cmd_tests_of` prints lines only.
- **L428 `--json` untested**: RED at the Given: StepDefinitionNotFound for `a map made at commit abc1234 in which no test executed the functions refund and export in src/cart.py` (L431); the existing step is `... executed {count:d} functions in src/cart.py` (map_steps.py:145). Then-step undefined. Code: `tools_map.py:cmd_untested` (L113-126) prints lines; `scripts/tools` untested subparser (L88-90) has no `--json`.
- **L436 `--json` refs**: RED at the Then `tools prints one JSON object` (undefined). Code: `tools_refs.py:cmd_refs` L43-49 prints lines and summary; `scripts/tools` refs subparser (L91-93) no `--json`.
- **L447 `--json` map**: RED at the Given `a Python project with the tests test_total and test_discount at commit def5678`: undefined (map_steps.py:13 has no `at commit` clause). Code: `tools_map.py:cmd_map` L42 prints pytest's last line and `map: ..., at ...`; `scripts/tools` map subparser (L81-83) no `--json`.
- **L455 tests-of unknown function (r57)**: the scenario's `it exits with an error` PASSES (exit 1), then `it says the target cannot be read` is undefined. Code: `tools_map.py:cmd_tests_of` L96 raises `has no function named`; the step module asserts that text (test_analysis_tools.py:48, via `exits_with_error`).

## 2. What the system answers today

Fixture projects in `.shop/scratch/w95-1-research/proj` and `nomap` (probe_tools.py, probe_refusals.py). Run. Fixture: src/cart.py with `refund`, `total`, `unused`, `class Cart.total`; test_cart.py has test_total (calls Cart().total and total); test_checkout calls only Cart().total.

- `tools map` -> exit 0; stdout `2 passed in 0.09s` then `map: .shop/scratch/tools/coverage, at 7db5716`.
- `tools tests-of src/cart.py:unused` (nothing executed it; nearest case to L138) -> exit 1; stdout `0 of the 2 tests in the map executed src/cart.py:unused (map made at 7db5716)`.
- `tools tests-of src/cart.py:missing` -> exit 1; stderr `tools: src/cart.py has no function named missing`; stdout empty.
- `tools tests-of src/cart.py` -> exit 0; `tests/test_cart.py::test_total`, `tests/test_checkout.py::test_checkout`, `2 of the 2 tests in the map executed src/cart.py (map made at 7db5716)`.
- `tools tests-of --by-file src/cart.py` -> `tests/test_cart.py 1`, `tests/test_checkout.py 1`, summary line.
- `tools untested src/cart.py src/other.py` -> `src/cart.py:1 refund`, `src/cart.py:9 unused`, `src/other.py:1 other`, `3 functions no test executed, in the map made at 7db5716`.
- `tools refs total` -> four `path:line` lines and `4 references to total, in 0 production and 2 test files; defined at src/cart.py:5, src/cart.py:14`.
- `tools map --json`, `tests-of --json src/cart.py`, `untested --json src/cart.py`, `refs --json total` -> exit 2, `unrecognized arguments: --json` (all four).
- Nearest refusal: no map (nomap project), `tests-of src/cart.py` and `untested src/cart.py` -> exit 1, stderr `tools: no map: make one with tools map`, stdout empty. Run.
- `untested src/cart.py src/gone.py` -> exit 1, stderr `tools: src/gone.py is not a file`, stdout EMPTY (the check runs before any line prints). Run.
- `tests-of src/gone.py` -> exit 1, `src/gone.py is not a file`. Run.
- `tests-of src/cart.py:Cart.total` and `src/cart.py:total` both list test_total AND test_checkout (see part 6). Run.
- Scenario's own data, empty: not probed; the nothing-executed case above is the empty answer.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/tools_map.py:cmd_tests_of L109-110 | prints `N of the M tests ... executed` and returns 1 when none ran | r11: print that no test of the map executed it, with the commit, exit 0; deprecated outline L124 still asserts exit 1 | test_tools.py::test_the_map_says_which_tests_execute_a_function (L102-104); test_analysis_tools.py exits_with_error branch L50-51 | tools refs (no callers, jedi skips the `scripts/tools` file, see note); read; search of tests |
| scripts/tools_map.py:cmd_tests_of L96 | `Refused: X has no function named N`, exit 1 | r57: say the target cannot be read, exit 1 | test_analysis_tools.py exits_with_error L48; test_tools.py L105 (returncode only) | read; search |
| scripts/tools_map.py:cmd_tests_of L104-108 | prints the tests, or per-file counts | r53: with --json one object: tests, count, commit | none (a JSON path does not exist) | read |
| scripts/tools_map.py:cmd_untested L124-126 | prints `path:line name` lines and count summary | r54: with --json one object: functions, count, commit | test_tools.py::test_untested_names_each_function_no_test_executed L110-112; analysis_tools_map_steps.py lost_functions/says_count L256-268 (keep: default output unchanged) | read; search |
| scripts/tools_refs.py:cmd_refs L43-49 | prints `path:line` lines and the summary | r55: with --json one object: references and summary | test_tools.py::test_refs_follow_imports_and_aliases L115-124 (keep: default output unchanged) | read; search |
| scripts/tools_map.py:cmd_map L42 | prints pytest's last line and `map: ..., at C` | r56: with --json one object: commit and test count | test_tools.py::test_the_map_says_which_tests_execute_a_function L90-92 (`3 passed` in stdout; default unchanged) | read; search |
| scripts/tools `CONTRACT` L35-41 | says tests-of exits 1 when none did | becomes wrong under r11; `--help` text | none | read |
| scripts/tools map/tests-of/untested/refs subparsers L81-93 | no --json flag (argparse exit 2) | each gets `--json`, as in the requirement | none | probe (exit 2) |
| tools_map.py:read_map L46-56 | refuses with no map, reads the commit from the .at file | shared by the text and JSON answers; the JSON path must keep the refusals | none (every refusal path) | read |
| features/analysis-tools.feature L124-136 (deprecated outline) | row "unused" asserts exit 1 | conflicts with L138 and r11 | run: passes today | run |
| agents/code-scout.md L39-43; spec/capabilities/code-research.md L32 | instruct tests-of/untested/refs; no reader of their line format or exit code | none change; no parser of output found | none | search (grep tests-of/untested/refs across skills/, agents/, spec/) |

Note: `tools refs` on the changed functions gives 0 references (`refs cmd_tests_of`, `refs cmd_untested`, `refs cmd_map`, `refs cmd_refs`): jedi reads only `.py` files and `scripts/tools` has no `.py` name. The callers are `scripts/tools` L98-106, found by read.

## 4. Tests the requirements make impossible to keep

`tests-of` lists none: no map in the worktree (`tools tests-of scripts/tools_map.py:cmd_tests_of` -> `no map: make one with tools map`). So this part is `by search` (tests asserting old behaviour, grep for `tests-of`, `untested`, `refs`, `executed`, `has no function`).

- **tests/scenarios/test_analysis_tools.py, the deprecated outline, row "unused"** (L124): r11 (exit 0). Passes today; cannot pass under the new r11 text. Accepted scenario that the requirement contradicts (see part 6/ruling note).
- **tests/scenarios/analysis_tools_*.py: `exits_with_error`, branch `unexecuted`** (test_analysis_tools.py L50-51, asserts `0 of the 1 tests in the map executed`): stops being reached under r11 (L138 says exit 0), and the old text it asserts changes.
- **tests/scenarios/test_analysis_tools.py `exits_with_error`, branch `absent`** (L46-49): asserts the stderr text `has no function named` (L48). r57 changes the text: this assertion can no longer pass as it is. Its L49 (`tests-of src/cart.py:total` exit 0) still holds.
- **tests/scripts/test_tools.py::test_the_map_says_which_tests_execute_a_function**, L102-104: `tests-of shelf/store.py:forgotten` asserts returncode 1 and `0 of the 3 tests in the map executed`. Under r11 the exit is 0 and the text is `no test of the map executed it`. Cannot pass as it is.
- **Sound (looked at, kept)**: test_tools.py L105 (missing function `nothing`: returncode 1, still true under r57); L93-101 (positive tests-of: lines, `--by-file`, `Shelf.count`: unchanged); L110-112 (untested default lines); L116-124 (refs default lines and summary); L69-86 (probe, install); L90-92 (`3 passed` in map's stdout).
- Scenario steps L186-199 (r9 positive, `says_share`, `gives_commit`), L203-212 (r10), L224-233 (r13), L256-268 (r25): read; they assert the default output, which stays. Sound.

## 5. A step the work-item skips

The new JSON path replaces the printing; it must keep the checks that run before printing. Each effect below comes from an existing step.

- `untested`: refuses a file that is not there before printing any line (`untested src/cart.py src/gone.py` -> stderr `src/gone.py is not a file`, stdout empty). Run. A JSON path that prints as it loops would print partial output. Keep the check first.
- `tests-of` and `untested`: refuse with no map, before any output (`no map: make one with tools map`, exit 1, stdout empty). Run.
- `tests-of` with a target function that does not exist: refuses before output (`has no function named`). Run. r57 keeps the refusal and changes its text.
- `map`: keeps the last map when pytest makes none: `cmd_map` raises `Refused` before `os.replace` (tools_map.py L34-39), and the stored commit is written after the replace (L40-41). Read. A `--json` map must print only the object; the pytest output is captured (L32), so none leaks. Read.
- The commit: `tests-of`/`untested` read the commit from `MAP.at` (L55-56); `map` writes `head()` (L14, L41). `--json` must print the same stored value. Read.

## 6. Defects

### tests-of: a bare function name also matches a method of that name (run)
Reproduction (probe_refusals.py, run):
```
tools tests-of src/cart.py:total   -> exit 0
tests/test_cart.py::test_total
tests/test_checkout.py::test_checkout
2 of the 2 tests in the map executed src/cart.py:total (map made at 7db5716)
tools tests-of src/cart.py:Cart.total -> the same two tests
```
test_checkout calls only `Cart().total([5])`, not the module function `total`. The filter is `found == name or found.endswith("." + name)` (tools_map.py L94). Read: this is the cause.

### `--json` is refused, not ignored (run)
`tools map --json` and the three others exit 2 with `unrecognized arguments: --json`. This is the requirement's gap, not a fault; listed so the plan sees today's refusal.

### Environment: `PYTEST_ADDOPTS=--work-item w95` breaks scenarios that run `tools map` (run)
Run of the deprecated rows and L455 in the session: `tools: no map was made by: .../python -m pytest -q ... --cov-report=` and `INTERNALERROR ... work_items.py line 53 ... --work-item w95: no such work-item under .shop/work/`. Removing the variable (probe_scenarios.py) makes the two deprecated rows and L455 reach their Then steps. Not a fault in the tools; the work run's env leaks into the mapped project's pytest.

## 7. The file set

Production (must change):
- `scripts/tools`: the CONTRACT text (L35-41, `Exit 1 when none did`); `--json` on the map, tests-of, untested and refs subparsers (L81-93); the dispatch is unchanged.
- `scripts/tools_map.py`: `cmd_tests_of` (r11 exit 0 and message, r57 text, r53 JSON, the bare-name match if the plan takes it); `cmd_untested` (r54 JSON); `cmd_map` (r56 JSON). Found by read and probes.
- `scripts/tools_refs.py`: `cmd_refs` (r55 JSON). Found by read.

Tests (must change, or keep passing):
- `tests/scenarios/analysis_tools_map_steps.py`: map_of wiring, nothing_executed, FORMS matching, the `at commit def5678` Given, the untested `in src/cart.py` Given, and the new Thens for r11/r57. Found by run.
- `tests/scenarios/test_analysis_tools.py`: `exits_with_error` (L46-51, the old absent and unexecuted branches); a new step module for the JSON Thens (`tools prints one JSON object`, `the object gives ...`) is advised (map_steps is 268 lines).
- `tests/scenarios/analysis_tools_project.py`: a JSON parse helper if it fits (183 lines).
- `tests/scripts/test_tools.py`: L102-104 (forgotten: exit and text) (134 lines).
- `features/analysis-tools.feature`: the deprecated outline L124-136 (retire or keep: a plan decision, see the conflict below).

Modules on the change's path, not edited, with line count and room under 300 (CLAUDE.md gives 300):
- scripts/tools: 112 lines, room 188 (edited)
- scripts/tools_map.py: 126 lines, room 174 (edited)
- scripts/tools_refs.py: 50 lines, room 250 (edited)
- scripts/tools_env.py: 105 lines, room 195 (interpreter lookup; not edited)
- tests/scenarios/analysis_tools_map_steps.py: 268 lines, room 32 (edited)
- tests/scenarios/analysis_tools_code_steps.py: 223 lines, room 77 (refs steps; edited for JSON if it fits)
- tests/scenarios/analysis_tools_probe_steps.py: 258 lines, room 42 (imports a_python_project; not edited)
- tests/scenarios/analysis_tools_project.py: 183 lines, room 117 (edited if a helper)
- tests/scenarios/test_analysis_tools.py: 71 lines, room 229 (edited)
- tests/scripts/test_tools.py: 134 lines, room 166 (edited)

Conflict for the plan (both readings, no choice made here):
- Reading A: the deprecated row "unused" (L124) is retired, as its own `Deprecated for:` line points at L138. Then r11 holds, and the step's unexecuted branch goes.
- Reading B: the deprecated row is kept as accepted; then r11 (exit 0) and that row (exit 1) cannot both hold for the same command and target.
