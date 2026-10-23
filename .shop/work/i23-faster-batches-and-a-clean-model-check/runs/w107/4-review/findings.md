# Review of w107: analysis-tools r7's scenario passes in the whole suite

**Verdict: DONE.** No finding is Critical, and none needs fixing now. The one commit changes one Then step, as the plan says (D-a). The plan lists that step under "Tests the decisions break".

## Commits reviewed

The branch `work/w107` no longer exists. The commits are the ones between `40e2c60 work: w107 ready -> claimed` and `dc4307c work: w107 claimed -> done` on the checked-out HEAD:

- `753c5a6` Check pip's error lines, not the whole stdout, in r7's Then. It changes `tests/scenarios/analysis_tools_probe_steps.py` (+3/−1).
- `dc4307c` is `work run`'s own `work:` commit and is not reviewed.

These match the implementer's `result.json` (`commits: ["753c5a6 …"]`).

## Removed and weakened tests

I looked for deleted test functions, dropped parametrize cases, removed or loosened asserts, added skip/xfail, and changes under `features/`. Commands: `git diff 40e2c60 HEAD --stat -- features/ tests/` and `git show 753c5a6`.

- `tests/scenarios/analysis_tools_probe_steps.py:220`, `failed_command` (the Then of r7's scenario):
  - **Before:** `assert "e1" not in stdout`. The substring `e1` appeared nowhere in stdout. That was meant as proof that the head of pip's error is dropped, but it also caught `e1` inside the interpreter path in the `Tried:` line.
  - **After:** `e1` and `e2` are not stripped lines of stdout, and `e3`, `e4`, `e5` are.
  - **Looser:** an `e1` that sits inside another line now passes. That is the intended fix.
  - **Stronger:** it now also checks that `e2` is absent and that the tail `e3`..`e5` is present.
  - **Listed in the plan:** yes, in part 4, "Tests the decisions break" (`failed_command`, D-a). Not a finding.

Nothing else changed. No change under `features/`.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds: the one test changed is listed in the plan.

## Cannot verify

- **Whole-suite green:** that the scenario now passes in the whole suite (`-n auto`), when pytest's tmp counter for it is 1. The implementer did not show it red either; the report says so. The reasoning holds: a stripped line `Tried: …/test_a_tool_still_missing_afte1/… -m pip install jedi` is never equal to `e1`. But I did not run the whole suite; `work run` runs it.
- **Report's suite counts:** "659 passed, 1 failed" at start, and "137 passed, 1 skipped" for `--work-item w107`. I did not re-run these.

## Findings

None at Critical, Important or Minor.

- **Behaviour:** no production code changed, so no behaviour contradicts r7 or the Purpose. The commit adds no code without a Behaviour line asking for it.
- **Not taken, by the plan's own decision:** the research notes' defects D1 (`tools install` exits 0 when pip exits 0 but the tool is still missing, which goes against r7's "exit with an error") and D2 (an empty pip error prints a blank indented line). The plan leaves both to the coordinator. They are not in w107's commits, so they are not findings against w107. D1 should still be filed as its own work-item, as the plan says.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w107 ready -> claimed$"` → `40e2c60`. Same for `claimed -> done` → `dc4307c`.
- `git log --stat 40e2c60..dc4307c` and `git show 753c5a6`.
- `git diff 40e2c60 HEAD --stat -- features/ tests/` → only the steps file.
- `python3 -m pytest -q -p no:cacheprovider -o addopts="" "tests/scenarios/test_analysis_tools.py::test_a_tool_still_missing_after_install_is_printed_with_the_failed_command"` → 1 passed.
- `python3 <Scripts>/tools check --base 40e2c60`:
  - ruff: All checks passed.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `python3 <Scripts>/tools size --limit 300` → nothing over the limit. `wc -l` on the steps file gives 270.
- `git status --short` → clean.
