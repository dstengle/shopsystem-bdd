# Plan of w95: the analysis tools answer in their output

Work-item `w95`, under `analysis-tools`, accepts `analysis-tools#r11` and `analysis-tools#r53`–`r57`. It has no Rulings and no Retires section. The capability rests on `design-decision/query-commands-answer-in-their-output` (0058) and `design-decision/plugin-takes-the-dependencies-it-needs` (0035). Everything below comes from `runs/w95/1-research/notes.md` unless it says otherwise.

## 1. What goes green

- **r11**, "tests-of says that no test of the map executed the target and exits successfully" (feature L138). It is red at its first Given: the map step with `5 tests made at commit abc1234` sets up no project and wires no commit label, and the `nothing executed` step's `{name}` pattern takes in `unused in src/cart.py` and then fails on a directory that is not a repository. The Then `tools prints that no test of the map executed it` has no step. The code prints `0 of the M tests … executed` and exits 1 (`tools_map.py:cmd_tests_of`).
- **r53**, "tests-of with --json prints the tests, their count and the map's commit as one JSON object" (L419). It is red at the Given: `executed_target` only matches targets that start with the FORMS prefixes, and this scenario says plain `src/cart.py`, so it raises StopIteration. The JSON Thens have no steps, and `--json` is refused with exit 2.
- **r54**, "untested with --json prints the functions, their count and the map's commit as one JSON object" (L428). It is red at the Given: no step matches `a map made at commit abc1234 in which no test executed the functions refund and export in src/cart.py`. The JSON Thens have no steps, and `--json` gives exit 2.
- **r55**, "refs with --json prints the references and the summary as one JSON object" (L436). It is red at `tools prints one JSON object`, which has no step, and `--json` gives exit 2.
- **r56**, "map with --json prints the map's commit and its test count as one JSON object" (L447). It is red at the Given: no step matches `… with the tests test_total and test_discount at commit def5678`. The JSON Thens have no steps, and `--json` gives exit 2.
- **r57**, "tests-of fails when the file has no function by the name given" (L455). `it exits with an error` passes. `it says the target cannot be read` has no step, and today's message says `has no function named missing` but not that the target cannot be read.
- **Retired:** the deprecated outline "tests-of fails when nothing executed the target or the function does not exist (deprecated)" (L124–136, `@r11 @deprecated`), both rows. See decision D1.

## 2. Where the change lands

- `scripts/tools`: the CONTRACT text no longer says tests-of exits 1 when no test executed the target. The map, tests-of, untested and refs subparsers each get a `--json` flag. The dispatch stays as it is.
- `scripts/tools_map.py`:
  - `cmd_tests_of`: the empty answer gets the r11 message and exit 0, the unknown function gets the r57 refusal, and `--json` gets its object (r53).
  - `cmd_untested`: `--json` object (r54).
  - `cmd_map`: `--json` object (r56).
- `scripts/tools_refs.py`: `cmd_refs` gets its `--json` object (r55).
- `tests/scenarios/analysis_tools_map_steps.py`:
  - The `a map of N tests made at commit <label>` Given sets up the project and the map, and records the label in `context["commits"]`.
  - The `nothing executed … in <file>` Given gets a pattern that keeps the function name and the file apart.
  - `executed_target` accepts a plain path.
  - New: the r11 Then `tools prints that no test of the map executed it`, and the r57 Then `it says the target cannot be read`.
  - The file has 268 lines, so anything that does not fit goes to the new module.
- `tests/scenarios/analysis_tools_json_steps.py` (new; the notes advise it because map_steps is near the limit):
  - `tools prints one JSON object`.
  - The `the object gives …` Thens of r53–r56.
  - The two `at commit` Givens of r54 and r56, unless they fit in map_steps.
  - It gets its own star import in `test_analysis_tools.py`, like the other step modules.
- `tests/scenarios/test_analysis_tools.py`: in `exits_with_error`, the `absent` branch is rewritten and the `unexecuted` branch removed (part 4), and the new module is imported.
- `tests/scenarios/analysis_tools_project.py`: `invoke` also removes `PYTEST_ADDOPTS` from the environment it gives `tools` (D6). A JSON parsing helper goes here only if the JSON module wants to share one.
- `tests/scripts/test_tools.py`: the `forgotten` assertions in `test_the_map_says_which_tests_execute_a_function` (part 4).
- `features/analysis-tools.feature`: the deprecated outline at L124–136 is taken out with `features retire` (D1).

Left out of the researcher's set: `tests/scenarios/analysis_tools_code_steps.py`. The JSON Thens for refs go in the new JSON module, so this file needs no change. Add it back only if a refs Given has to change.

## 3. Decisions

- **D1. Retire the deprecated outline, both rows.**
  - The row "unused" asserts exit 1 for a target no test executed. r11 and 0058 ("an empty answer exits successfully") say exit 0, so both cannot hold, and the outline's own `Deprecated for:` line names L138 as its replacement.
  - The row "missing" is covered by the r57 scenario at L455: same Given, same command, exits with an error.
  - Use `features retire` with the outline's title. This is the researcher's question, and it is settled: requirement r11 and design-decision 0058 decide what the narrator sees (exit 0), so it does not go to the person. It rests on `analysis-tools#r11`, `analysis-tools#r57` and 0058.
- **D2. The empty answer of tests-of (r11).**
  - It prints one line saying that no test of the map executed the target, naming the target and the commit the map was made at (`no test of the map executed src/cart.py:unused (map made at <commit>)`), and exits 0.
  - The non-empty summary line (`N of the M tests …`) stays as it is (r9).
  - With `--by-file`, the empty answer is the same line.
  - Rests on `analysis-tools#r11` and 0058.
- **D3. The unknown function (r57).** The refusal stays exit 1 with nothing on stdout. Its stderr names the target and says it cannot be read, giving the reason after it, for example `tools: cannot read src/cart.py:missing: src/cart.py has no function named missing`. Other refusals keep their wording (`no map`, `is not a file`). Rests on `analysis-tools#r57` and `#r49`.
- **D4. The `--json` objects.** The keys are Implementation (0058). With `--json`, each command prints one JSON object on stdout and nothing else, and exits as it would without the flag. Refusals stay on stderr as text: 0058 says `--json` prints the result, and a refusal has none.
  - **tests-of (r53):** `tests`, the list of test node ids; `count`; `commit`, the stored commit, the same value the text line gives. The count of the map's tests can also be given as `of`, since the text line gives it. An empty answer is an empty list with count 0 and exit 0 (r11 with r53).
  - **untested (r54):** `functions`, each with its path, line and name; `count`; `commit`.
  - **refs (r55):** `references`, each with its path and line; `summary`, holding the number of references, the production file count, the test file count, and `defined`, the list of `path:line` places where the name is defined.
  - **map (r56):** `commit`, the commit written beside the data; `tests`, the number of tests in the map, counted from the map's test contexts as tests-of counts them. pytest's own output is not printed.
  - Rests on `analysis-tools#r53`–`r56` and 0058.
- **D5. Checks before output.** Every refusal (no map, a file that is not there, an unknown function, `map` that makes no map) runs before anything is printed, in text or JSON. Each JSON object is printed once, after it is complete, never line by line. Rests on `analysis-tools#r49` (change nothing; say why), and notes part 5.
- **D6. Scenario environment (the researcher's second question).**
  - `invoke` in `analysis_tools_project.py` removes `PYTEST_ADDOPTS` from the environment of the `tools` it runs. It already removes `VIRTUAL_ENV` there.
  - The scenario's temporary project is a project of its own. The `--work-item` that a worker's pytest gets through `PYTEST_ADDOPTS` (supervision's Implementation) is meant for this repository's run, not for the project being mapped. `tests/scripts/test_work_items.py` already removes it the same way.
  - The narrator sees nothing different. This is test harness only.
- **D7. The bare-name defect is out of scope.** The defect: `tests-of file:total` also matches the method `Cart.total`. No accepted requirement of w95 covers it, and changing it would change r9's answer. It is not fixed here. It is reported in part 5.

## 4. Tests the decisions break

- `features/analysis-tools.feature`, the deprecated outline at L124 (both rows): removed (D1). The row "unused" contradicts r11, and the row "missing" is covered by L455.
- `tests/scenarios/test_analysis_tools.py::exits_with_error`:
  - The `unexecuted` branch, which asserts `0 of the 1 tests in the map executed`, is removed. Under D1 and D2 no scenario reaches it, and its text is gone. Removing it also leaves no reader of the context key `unexecuted`; the implementer checks whether the `nothing executed` Given still needs to set it.
  - The `absent` branch is rewritten under D3. It still asserts that stdout is empty, asserts that stderr says the target `src/cart.py:<absent>` cannot be read, and keeps the check that `tests-of src/cart.py:total` exits 0. This branch may be what the new `it says the target cannot be read` Then asserts. It may stay in `exits_with_error` only if L455's Then does not repeat it.
- `tests/scripts/test_tools.py::test_the_map_says_which_tests_execute_a_function`, the `forgotten` assertions (L102–104): rewritten. `tests-of shelf/store.py:forgotten` now asserts return code 0 and the D2 line (that no test of the map executed it, with the commit). Its L105 (unknown function `nothing`, return code 1) holds under D3 and stays. A unit test of the `--json` objects' keys and of `--json` with refusals may go here, as 0058 places codes and keys in unit tests.
- Verified sound and kept (notes part 4):
  - `test_tools.py`: the positive tests-of cases, `--by-file`, `Shelf.count`, untested's default lines, refs' default lines and summary, probe and install, and `3 passed` in map's stdout. D4 changes only the `--json` path, so the text output stays as it is.
  - The r9, r10, r13 and r25 scenario steps.

## 5. Open cases

- `tests-of --by-file --json`: whether the object gives the counts per test file in place of `tests`. No scenario says.
- `tests-of --json` on a line range or a method: the same object as for a file is assumed, but no scenario pins it.
- `untested --json` over several files: each function carries its path. Whether the objects are also grouped by file is not said.
- `map --json` when the tests fail: r8 says the map exits successfully anyway. Whether the object also gives pytest's last line or a pass/fail count is not said.
- `refs --json` on a name defined in several places: `defined` is a list, but its order is not pinned.
- The JSON keys chosen under D4 are not yet in the capability's Implementation section, which 0058 says is where they belong. Writing them there is for whoever edits the spec, not this work.
- The bare-name defect (D7): a test of only `Cart().total` is listed for `tests-of src/cart.py:total`. Reported for its own work-item.
