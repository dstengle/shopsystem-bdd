# Review 10 of w245

**Verdict: DONE_WITH_CONCERNS.** I found two Important findings, both triaged fix now and both in w245's commits. (1) A failing test that is not a scenario is still taken back: `is_scenario` looks at a module's text, not at whether the module is under `tests/scenarios/`, which goes against the person's ruling (review 7, answer (2)). (2) The rerun always gets `-n 0`, so in a repository without pytest-xdist every rerun fails with "unrecognized arguments: -n", and r222 can never take a scenario back there.

## Commits reviewed

The brief's `Commits:` line, as `work run` merged them:
- f968f32a "a run with errors, a non-scenario failure, or a rerun that ran no test is not taken back (r219, r222)"
- 7f37149d "a scenario's rerun alone is built from the suite command, with --whole-suite and -n 0 (r222)"

The implementers' results list b99d5507 (8-implement) and ffb6d976 (9-implement). The branch work/w245 is gone. I compared each listed commit with the merged one (`git diff ffb6d976 7f37149d`): the only differences are under `.shop/`, so they are the same code change, rebased. Suite: the brief's record, 1097 passed, 0 failed at 7f37149d. I did not run the whole suite.

## Removed and weakened tests

What I searched for: in the diff of `tests/scripts/test_supervise_merge_rerun.py`, removed `def test_`, removed or changed `assert` lines, and added skip or xfail. Nothing changed under `features/`.

- No test function was removed. The helper `tmp_path_of` was removed and replaced inline by `stubbed.root`, which is the same value.
- `test_a_scenario_failing_in_both_runs_gets_one_run_alone_and_a_pass_there_merges`:
  - **Before:** it asserted `"-n" not in alone[0]`.
  - **Now:** it asserts `--whole-suite` is in the rerun and that the only `-n` value is `0`. This is what the person's answer (Fix the rerun command) asks for.
  - The plan does not list this change. It is covered by the interim allowance below.
- `NODE` moved from `tests/test_thing.py` to `tests/scenarios/test_thing.py`, and the fixture now writes scenario modules. This is setup only: no assertion changed.

## Allowances

- **8-implement, setup** (the test file's setup and lint respelled, its two tests keep their assertions): **holds.** f968f32 changes no `assert` in the two existing tests (only `tmp_path_of(stubbed)` became `stubbed.root`) and drops no parametrize case.
- **9-implement, interim** (the first test and the fixture's suite command): **holds.** The file was first committed in 58879782, after the base 955ad466. The new assertion is what the person's answer asks for: `--whole-suite`, and `-n 0` with no other `-n` value.

## Cannot verify

- 8-implement's report says the three new tests fail on the old code, and 9-implement's says its new assertion does. Neither ran them red. The claim is plausible from reading the code, but I did not run it.
- I did not reproduce the person's hand check (`-n 0 --whole-suite '<node>'` gives 1 passed on the rmtree scenario). That would mean running a scenario of another concern on the merged tree.

## Findings

### 1. Important, fix now: a test that is not a scenario is still taken back (scripts/supervise_merge.py:117-121)

- **What is wrong:** `is_scenario` counts a node as a scenario when its module's text matches `\bscenarios?\(`, wherever the module is. Four tests/scripts modules match:
  - `tests/scripts/test_work_items.py:21`: `scenarios("../features/thing.feature")` inside a string
  - `tests/scripts/test_features_scenarios.py:146`
  - `tests/scripts/test_features_deprecating.py:38,43`
  - `tests/scripts/test_supervise_merge_rerun.py:56`

  So a FAILED node in any of those modules is rerun alone and, if it passes, taken back and merged. One example is an order-dependent regression in `test_work_items.py`.
- **Why it matters:** the person's ruling (review 7, answer (2)) is "Rerun only scenarios (nodes under tests/scenarios/ that the suite collects from features/) ... a FAILED node that is not a scenario means the run is not taken back." r219 and r222 only cover scenarios, so taking back other tests is behaviour no line asks for.
- **Why it is this way:** 8-implement's report says it chose text detection because the r219/r222 scenarios' fixture writes `tests/test_thing.py` (`tests/scenarios/supervision_rerun_steps.py:39`).
- **Fix:** require the node's path to be under `tests/scenarios/`, as well as binding scenarios. Move the fixture module in `supervision_rerun_steps.py:39` to `tests/scenarios/test_thing.py`. Add a test with a FAILED node in a tests/scripts module that contains `scenarios(`.

### 2. Important, fix now: `-n 0` is added even where the command has no `-n` (scripts/supervise_merge.py:137)

- **What is wrong:** `alone = [...] + ["-n", "0"]` is added unconditionally.
  - `Merge.tests` (lines 31-32) leaves `-n` out when pytest-xdist is not installed. The capability's Implementation says to run "in one process where it has not".
  - The same happens when a delivery gives its own `tests` commands.
  - In those cases the rerun is `pytest ... -n 0 <node>`, which exits 4 with "unrecognized arguments: -n". It then counts as failed.
- **Why it matters:** wherever xdist is absent, a scenario that passes alone is never taken as passing. That is a wrong answer against r222, and the question then quotes a usage error as the "second run" (r220).
- **Reproduction:** `python3 -m pytest -q -p no:xdist -o addopts= -n 0 tests/scripts/test_supervise_merge_rerun.py` printed `ERROR: usage: ... error: unrecognized arguments: -n`.
- **Fix:** add `-n 0` only when the command had `-n` or the project has xdist. pytest.ini's addopts brings `-n auto` back only where xdist is loaded. Add a test with a suite command that has no `-n`.

### 3. Minor, observation: the error check matches captured test output (scripts/supervise_merge.py:134)

- **What is wrong:** `\b\d+ errors?\b` is searched across all of a failing run's output, including the captured output of the failing tests shown under `-rfEx`. A failing scenario whose output contains text such as ruff's "Found 2 errors." (as `tools check` printed in this review) is then not taken back.
- **Why it is only an observation:** this errs towards refusing a merge, never towards a wrong merge.
- **Fix:** match only the final summary line (the last `=+ ... in N s =+` line) and the `ERROR ` lines of the short summary.

### 4. Minor, drop: ruff findings in the touched file

`tools check` reports two hits:
- `scripts/supervise_merge.py:134:88` FURB167 (`re.M`)
- `scripts/supervise_merge.py:138:13` PLC0206

Both are in lines these commits added.

## Checks

- **ruff:** 2 errors, both in scripts/supervise_merge.py, both added by these commits (finding 4).
- **vulture:** clean.
- **import-linter:** the project states no import contracts.
- **size (limit 300):** nothing printed. supervise_merge.py has 172 lines and test_supervise_merge_rerun.py has 102.

## Commands run

- `git log --oneline -12`; `git log --stat f968f32~1..7f37149`; `git diff 8fd94a6a 7f37149d`
- `git show --stat ffb6d976 b99d5507`; `git diff ffb6d976 7f37149d --stat`
- `git log --diff-filter=A -- tests/scripts/test_supervise_merge_rerun.py`; `git log --oneline 955ad466..8fd94a6a -- <same>`
- `git diff 8fd94a6a 7f37149d --stat -- features/`: empty
- `grep -rln "scenarios\?(" tests/scripts`; `grep -n ...` on the four matches
- `python3 -m pytest -q -n 0 tests/scripts/test_supervise_merge_rerun.py`: 5 passed
- `python3 -m pytest -q -p no:xdist -o addopts= -n 0 tests/scripts/test_supervise_merge_rerun.py`: unrecognized arguments: -n
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 8fd94a6a`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`; `wc -l` on the two files
