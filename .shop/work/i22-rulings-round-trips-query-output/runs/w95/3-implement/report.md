# Report w95 — HAND-BACK

## Budget
scripts/tools, scripts/tools_map.py, scripts/tools_refs.py, tests/scenarios/analysis_tools_map_steps.py, tests/scenarios/analysis_tools_json_steps.py (new), tests/scenarios/analysis_tools_project.py, tests/scenarios/test_analysis_tools.py, tests/scripts/test_tools.py, features/analysis-tools.feature (retire only)

## Stop condition
A Then line can only pass through code that contradicts it (r55, "refs with --json ...").
Scenario line: `the object gives the summary: 2 references, 1 production file, 1 test file, and src/cart.py as where total is defined`.
Evidence (run): `tools refs --json total` in that scenario's project printed
`... "summary": {"references": 4, "production_files": 1, "test_files": 1, "defined": ["src/cart.py:1"]}`;
the step fails on `(summary["references"], ...) == (2, 1, 1)` (analysis_tools_json_steps.py: gives_summary).
Why: `refs` counts each file's import line and its call line (src/checkout.py:1 and :5, tests/test_cart.py:1 and :5). Counting imports is existing, tested behaviour: tests/scripts/test_tools.py::test_refs_follow_imports_and_aliases expects `tests/test_store.py:2` (an import line) among the references. Getting 2 would mean excluding import lines, which changes existing text output and breaks that test. Alternatively the line's "2 references" is meant as something else (e.g. one per file). Either is the person's ruling on the scenario or the refs semantics. I did not choose.

## Scenarios
Green (5): r11 (tests-of says none executed, exit 0), r53, r54, r56, r57. Red (1): r55 at its last Then (above), the first Then steps of r55 pass.
Final run: `python3 -m pytest -q -n 0 tests/scenarios/test_analysis_tools.py --work-item w95` -> `1 failed, 5 passed, 58 deselected`.

## What changed
- scripts/tools: `--json` on map, tests-of, untested, refs; CONTRACT text (empty answer exits 0, --json); `map --json` re-runs under the project interpreter (it needs coverage to count tests).
- scripts/tools_map.py: tests-of empty answer line + exit 0 (r11), "cannot read <target>: ..." refusal (r57), JSON objects (tests-of: tests, count, of, commit; untested: functions[path,line,name], count, commit; map: commit, tests); `test_count` helper.
- scripts/tools_refs.py: JSON object: references[path,line], summary{references, production_files, test_files, defined}.
- features/analysis-tools.feature: `features retire` of the deprecated outline (D1), both rows.
- Tests: analysis_tools_map_steps.py (nothing_executed Given builds the planned map and labels the commit; plain-path target; r11 Then), new analysis_tools_json_steps.py, analysis_tools_project.py (`invoke` drops PYTEST_ADDOPTS, D6), test_analysis_tools.py (exits_with_error branches, new Then, import), tests/scripts/test_tools.py (`forgotten` assertions per plan).

## Red/green
Red runs: r11 failed first at the Given (`fatal: not a git repository`), then after the steps at the Then (exit code assertion, old exit 1). r57: red on stderr `tools: src/cart.py has no function named missing` vs the new Then. r53/r54/r56 were written with their code in the same step (flags were added to the parser with r11's change); their red state before any work is the research notes' (undefined steps, `--json` exit 2); I did not re-run them red — a deviation from one-at-a-time.

## Suite at start
Suite: 614 passed, 7 failed at 87a52bd (7 failures all in tests/scenarios/test_analysis_tools.py's w95 scenarios and supervision tests, per the brief's record).

## Tests changed under an allowance
none beyond the plan's list: the `forgotten` assertions in tests/scripts/test_tools.py::test_the_map_says_which_tests_execute_a_function and the `absent`/`unexecuted` branches of exits_with_error (both listed in plan part 4). Setup change: `invoke` drops PYTEST_ADDOPTS (plan D6).

## Notes
- tests/scripts/test_tools.py's tests that run `tools map` fail in this session (`PYTEST_ADDOPTS=--work-item w95` leaks into the mapped project's pytest: "no such work-item"). I could not unset it, so my edit to the `forgotten` assertions is unverified here; it should pass in work run's suite where the variable is absent.
- Size: `tools size --limit 300` printed nothing.

## Open questions
Plan part 5's open cases (by-file --json, line range --json, grouping, map --json on failing tests, defined order) are unchosen: code treats them uniformly. Plus the r55 question above.

## Outside the file set
none. The plan contained no code.
