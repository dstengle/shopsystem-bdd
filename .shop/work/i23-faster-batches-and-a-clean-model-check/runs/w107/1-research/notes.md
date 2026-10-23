# w107 research notes

Work-item: w107, accepts analysis-tools#r7. Scenario: features/analysis-tools.feature:89 "a tool still missing after install is printed with the failed command". Node: tests/scenarios/test_analysis_tools.py::test_a_tool_still_missing_after_install_is_printed_with_the_failed_command
Method: `tools refs` (run), `python3 -m pytest --collect-only` (run), reads (`read`), a probe in scratch (`run`). No `tools map` run: it writes .shop/scratch/tools/coverage, outside my scratch dir. So `tests-of` / `untested` were not used; test lists below are `by search`.

## 1. Why each scenario is red today

Scenario: "a tool still missing after install is printed with the failed command"
- Alone: `python3 -m pytest -q "tests/scenarios/test_analysis_tools.py::test_a_tool_still_missing_after_install_is_printed_with_the_failed_command"` -> `1 passed` (run).
- Whole suite: failing at `assert "e1" not in stdout`, tests/scenarios/analysis_tools_probe_steps.py:220, Then "it prints the command that failed with the end of its error" (work-item, `read`; I did not run the whole suite).
- Cause: the Then's stdout includes the line `Tried: <python> -m pip install jedi`, and `<python>` is the stand-in interpreter under pytest's tmp dir. That dir is named from the test name cut to 30 characters plus a number: `test_a_tool_still_missing_afte<N>`. For N = 1 the path holds `e1`, so the assertion fails.
- Probe `probe_tmpname.py` + `probe_tmpname_b.py` (run, `-o python_files=probe_*.py`): two tests with that name in one session print `.../test_a_tool_still_missing_afte0` and `.../test_a_tool_still_missing_afte1`.
- Not explained: N = 1 in the whole suite. Collection of the whole suite (`pytest --collect-only -m "" tests`, run) finds one test with that 30-character prefix, so the `afte0` came from something I did not identify. The work-item reports the failure in w104–w106 whole-suite runs.
- Missing in code: nothing. `tools install` prints the r7 output (probe case 1 in part 2). The fault is the step's assertion: it looks for `e1` anywhere in stdout, and the path carries it.

## 2. What the system answers today

Probe `probe_install.py`, run as `python3 -m pytest -s -q -p no:cacheprovider -o addopts="" -o python_files="probe_*.py" .shop/scratch/w107-1-research/probe_install.py` (`-o addopts=""` drops pytest.ini's `-n auto`). Each case runs `scripts/tools --python <stand-in> install` in its own tmp project. Output trimmed.

Case 1 — the scenario's Givens and When: venv missing jedi, pip fails with `e1..e5` and `error: no matching distribution`:
```
jedi is missing.
  It is for: exact references to a name, through imports and aliases.
  Without it: where a change lands is counted by text search, and the count is a floor.
  Tried: /tmp/pytest-of-vscode/pytest-17491/test_scenario_case_pip_fails_i0/env/bin/python -m pip install jedi
  e3
  e4
  e5
  error: no matching distribution
```
rc=1. The last four stderr lines are kept (`tools_env.py:96`), so e1 and e2 are dropped. The `e1` test failure is only the path.

Case 2 — nearest: not a virtualenv, pip would fail (the r18 path):
```
jedi is missing.
  It is for: ...
  Without it: ...
  Tried: /tmp/.../env/bin/python is not a virtualenv (--python): nothing is installed into it
  
```
rc=1. The error line is empty, so a line of two spaces is printed.

Case 3 — nearest: pip exits 0, but jedi is still reported missing:
```
jedi installed
```
rc=0. Nothing re-probes after the install (see defect D1).

## 3. Old assumptions

r7 is not changed by w107; it is already in the spec and the scenario tests it. The one assumption is the test's:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| tests/scenarios/analysis_tools_probe_steps.py:failed_command (line 220) | asserts `"e1" not in stdout` as proof that the head of pip's error is dropped | nothing: r7 says "the end of its error", which the code gives; the check is path-dependent | the scenario (run alone: pass; whole suite: fails, per work-item) | grep `e1` in tests |
| tests/scenarios/analysis_tools_probe_steps.py:pip_fails (line 110) | the stub pip error `e1\ne2\ne3\ne4\ne5\n...` | none | the scenario | read |
| scripts/tools_env.py:cmd_install (lines 95–103) | prints the command, with the interpreter path, and the last 4 lines of pip's stderr | matches r7 | the scenario (run, case 1); tests/scripts/test_tools.py:test_install_refuses_an_interpreter_that_is_no_virtualenv (by search, read) | refs / read |

## 4. Tests the requirements make impossible to keep

- The work-item changes no behaviour, so no test becomes impossible to keep because of it.
- tests/scenarios/analysis_tools_probe_steps.py:failed_command (line 220): can fail in the whole suite (part 1). This is the accepted scenario itself, so the plan must decide.
- tests/scripts/test_tools.py:79–86 (read): asserts "is not a virtualenv" and the `Tried:` line shape. Case 2 matches it. Sound.
- Search of tests for `e1`, `Tried`, `installed` (by search): the hits are the step lines 110, 218, 220, 228 and test_tools.py:86. Only line 220 depends on the path.

## 5. A step the work-item skips

none. The work-item adds no path; it changes the test's assertion, if anything.

## 6. Defects

### D1: install reports success and exits 0 when pip exits 0 but the tool is still missing
Reproduction: probe_install.py case 3 (run). The stand-in still reports jedi missing after pip exits 0:
```
jedi installed
```
rc=0.
Code: scripts/tools_env.py:cmd_install (lines 92–98) checks only pip's return code and never re-probes. r7 says: "if a tool is still missing after `tools install`, then `tools` shall ... exit with an error". Reach in real use: unverified; the stand-in forces the case.

### D2 (minor): an empty pip error prints a line of two spaces
Reproduction: probe_install.py case 2 (run). The "outside a virtualenv" path prints `  ` as the last line. Cosmetic.

## 7. The file set

Changes the scenario may need (plan decides between them):
- tests/scenarios/analysis_tools_probe_steps.py (268 lines; room 32): line 220 `assert "e1" not in stdout` is the defect. Options: (a) check only the pip lines, e.g. no stdout line equal to `  e1`, which is independent of tmp paths; (b) keep the check and make the tmp path free of digits. Found by grep and run.
- tests/scenarios/analysis_tools_project.py (182 lines; room 118): the fixture helpers `fake`, `invoke`; touched only if (b) is chosen. Read.

Production files on the change's path (edited only if D1 is taken into the work-item):
- scripts/tools_env.py (104 lines; room 196): cmd_install lines 81–104. Found by refs (`cmd_install`: 0 references, defined at line 81; the dispatch is by name, not by a call site) and by read of scripts/tools.
- scripts/tools (118 lines; room 182): argument parsing and dispatch to cmd_install. Read of `--help`; not otherwise read.

Limit: CLAUDE.md, 300 lines.
