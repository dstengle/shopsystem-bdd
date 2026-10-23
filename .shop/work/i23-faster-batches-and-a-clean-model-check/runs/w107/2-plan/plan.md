# Plan of w107: analysis-tools r7's scenario passes in the whole suite

## 1. What goes green

- analysis-tools#r7, scenario "a tool still missing after install is printed with the failed command" (features/analysis-tools.feature:89).
  - Red today only in the whole suite (`python3 -m pytest -q -n auto`). Alone it passes (notes part 1, run).
  - Cause (notes part 1): the Then "it prints the command that failed with the end of its error" (tests/scenarios/analysis_tools_probe_steps.py, `failed_command`) checks that the substring `e1` is nowhere in stdout. Stdout's `Tried:` line holds the stand-in interpreter's path. That path sits under pytest's tmp directory, whose name is the test name cut to 30 characters plus a counter (`test_a_tool_still_missing_afte<N>`). When N = 1 the path holds `e1` and the check fails. The production output already meets r7 (notes part 2, case 1): the four last lines of pip's error are printed, and `e1`/`e2` are dropped.
- Retired scenarios: none; the work-item has no Retires section.

## 2. Where the change lands

- tests/scenarios/analysis_tools_probe_steps.py: `failed_command` stops checking stdout as one string for `e1` and checks the printed lines of pip's error instead (see decision D-a). The file has 268 lines; the change keeps it at 300 or fewer.

Taken out of the researcher's set, and why:
- tests/scenarios/analysis_tools_project.py: this file changes only under option (b), tmp paths with no digits, which this plan does not take.
- scripts/tools_env.py and scripts/tools: production already gives r7's output for the scenario. Defect D1 (pip exits 0 but the tool is still missing) is not part of this work-item; see part 5.

## 3. Decisions

- **D-a. The step checks pip's error lines, not stdout as one string.** This is the researcher's option (a). The proof that only the end of pip's error is printed becomes: no stdout line is pip's dropped head line `e1` as printed (indented under the tool, like the kept lines `e3`..`e5` and `error: no matching distribution`). The path in the `Tried:` line can then hold any digits without changing the result. Optionally, the step also checks that the kept tail lines are present as lines of their own. The `Tried:` regex, the `error: no matching distribution` check and the pip-calls check stay as they are. Rests on analysis-tools#r7 ("the command that failed with the end of its error"): r7 is about the error's lines, not the interpreter's path.
  - Option (b), making pytest's tmp path free of digits, is rejected. It changes a fixture that many scenarios share, for a fault in one assertion. Any other test's tmp name could also collide with stub text.
- This plan changes nothing the narrator sees, so no question is needed.

## 4. Tests the decisions break

- tests/scenarios/analysis_tools_probe_steps.py `failed_command`, the Then of the accepted scenario. D-a rewrites it to assert that pip's dropped head (`e1`) is absent as a printed error line, and that the tail is present. The scenario then passes alone and in the whole suite, whatever tmp counter pytest picks.
- No other test breaks. The notes' search for `e1`, `Tried` and `installed` in the tests finds only step lines 110, 218, 220 and 228 and tests/scripts/test_tools.py:86, and only line 220 depends on the path. The r18 step (line 228) and test_tools.py:79–86 match `Tried:` with an escaped full path and are unaffected.

## 5. Open cases

- Seeing red: the fault shows only when pytest's tmp counter for this test is 1, and the notes could not say why that happens in the whole suite. The implementer names how the red was shown: a whole-suite run, or the step run against a stdout whose path holds `e1`.
- Defect D1 (notes part 6): `tools install` prints `<tool> installed` and exits 0 when pip exits 0 but the tool is still missing, because it does not probe again. That case falls under r7's "still missing after `tools install`", but this work-item does not accept it and no scenario covers it. It is left for the coordinator to file as its own work-item, not fixed here.
- Defect D2 (notes part 6): an empty pip error prints a line of two spaces. Cosmetic, outside r7's scenario, not taken.
