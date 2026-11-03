# Branch review of i62 (review 2, after w246)

**Verdict: DONE.** w246 fixes both fix-now findings of branch review 1:

- A refused merge's question now gives each scenario's first runs, as r220 asks (`scripts/supervise_merge.py:164-169`).
- The `rerun` line in `log.jsonl` is gone (`taken_back` at `supervise_merge.py:123-146` writes nothing to the log).

Nothing is Critical and nothing is triaged fix now. Every check has a run in the brief.

The whole suite at HEAD has **1 failure**: r214's scenario, which is i63's, not i62's. Its code is the same as at 0b306638, where the suite passed with 0 failed. It fails on a held `.git/index.lock`, so it is a flake. It is recorded below as an Important observation (finding 1).

## Range reviewed

- **Range:** `955ad466..215cf7c7` on `main`, the initiative branch.
- **w245** (`under: supervision`, accepts supervision#r219@0.29, r220, r222): green. Its commits:
  - b274fa52, 83e3b8ee, 58879782, f968f32a, 7f37149d, fa1b6eea
  - its `work:` transition commits
- **w246** (fix work-item for branch review 1, same accepts): green. Its commits:
  - 0b306638, "the refused merge's question gives each scenario's first runs; no rerun log line"
  - its `work:` transition commits
- **Commits the brief gives to no work-item:** every other commit in the range. See finding 3.

## Suite

`Suite: 1101 passed, 1 failed at 215cf7c in 33.90 s`

- The same run also gave: 1 skipped, 23 xfailed, 11 xpassed, 56 subtests passed. Command: `python3 -m pytest -q -n auto -rfEx -p work_items --work-item w245 --whole-suite`, exit 1.
- **The failure:** `tests/scenarios/test_supervision.py::test_what_changed_in_the_repositorys_own_checkout_while_a_session_of_one_initiative_worked_is_checked_without_the_paths_of_another_initiative_run_side_by_side` (@r214). See finding 1.
- **Parallel:** yes (`-n auto`).
- **In-process:** no. The supervision steps run `work run` as a subprocess.
- **Under 60 s,** so this is no finding.
- **Dry-run and real mode:** none to compare.
  - The only `--dry-run` in `scripts/` is `git push --dry-run`, used as a check before a push (`scripts/supervise_faults.py:71`, `scripts/supervise_review.py:55`).
  - That is not a dry-run mode of one of the system's own operations, so no agreement test is due.

## Checks

Every run was made at 215cf7c7.

- **w245's scenarios** (`pytest -q -n auto -p work_items --work-item w245`): exit 0. 195 passed, 1 skipped, 56 subtests passed, in 11.46 s.
- **w246's scenarios** (`pytest -q -n auto -p work_items --work-item w246`): exit 0. 195 passed, 1 skipped, 56 subtests passed, in 9.38 s.
- **`tools check --base 955ad466`:** exit 1.
  - **ruff:** 29 hits. None is in a file of i62's work:
    - `scripts/supervise_merge.py`, `scripts/work_items.py`, `tests/scripts/test_supervise_merge_rerun.py`, `tests/scenarios/supervision_rerun_steps.py`, `tests/scenarios/supervision_tests_steps.py` and `tests/scripts/test_work_items.py` have no hits.
    - `tests/scenarios/test_supervision.py:14` I001 is older than i62. w245's one import line (`supervision_rerun_steps`) is in order.
    - The other hits are in other initiatives' files: `scripts/supervise_change.py:83,103,130` B023 (i48 w238), `supervision_proposal_steps.py`, `supervision_reintegrate_steps.py`, `work_queue_list_steps.py`, `stub_claude.py`, `test_supervise_change.py`.
    - Some are in tracked round scratch scripts: `.shop/work/i55/.../splice.py`, `.shop/work/i60/.../splice.py`, `.shop/work/i63/.../mk.py`.
  - **vulture:** `tests/scenarios/work_queue_status_steps.py:100` unused variable `notes`. Not i62's.
  - **import-linter:** "the project states no import contracts". I read `CLAUDE.md` myself: it gives no import contract, only the module map. Nothing to check.
- **`tools size`:** exit 0, nothing printed. No file is over 300 lines; `scripts/supervise_merge.py` has 175.
- **`features deprecated`:** exit 0, 23 deprecated scenarios. None is i62's. One is reported as "no scenario has that title": the r209/r210 delegation scenario, "for: r209 and r210". That is not i62's.
- **`features bindings`:** exit 0, "every binding names a scenario".

## Removed and weakened tests

**What I searched the range's change for:**

- removed `def test_`
- removed or changed `assert` lines
- changed parametrize lists
- added `skip` or `xfail`
- changes under `features/`

**w245:** none.

**w246:** two assertions removed, both listed in w246's plan under "4. Tests the decisions break" (decision 2):

1. `tests/scripts/test_supervise_merge_rerun.py::test_a_scenario_failing_in_both_runs_gets_one_run_alone_and_a_pass_there_merges`
   - **Removed:** the assertion that a `rerun` line was logged for the run alone.
   - **What it proved:** that log line, which no line asks for (review 1, finding 2).
   - **What remains:** one run alone, `--whole-suite`, `-n 0` as the only `-n`, and the merge going ahead.
   - **Listed in the plan:** yes.
2. `tests/scenarios/supervision_rerun_steps.py::closes_run_alone`
   - **Removed:** the `rerun` log assertion (old lines 54-55).
   - **What it proved:** the same log line.
   - **What remains:** r219 is still pinned by `runs[-1:] == ["alone"]` (line 43 of the file as it now stands) and by `runs.count("alone") == 1` (`closes_run_no_other`).
   - **Listed in the plan:** yes.
   - **New pin:** `test_the_question_gives_the_first_run_of_a_scenario_that_failed_only_in_the_suite_run` asserts that no `rerun` line is logged.

Both files were first committed after Base, so the final diff shows them as new files.

**Other initiatives:** test changes in the range from other initiatives' commits, not graded against i62. Their own branch reviews are in the range.

- `test_supervise_change.py:37` (i48 w238)
- `test_workqueue_done.py:19` (i55)
- retired r9, r105, r23 and r14 scenarios (i55)

## Allowances

- **w246 3-implement, `test_supervise_merge_rerun.py::test_a_scenario_failing_in_both_runs_…`, row `interim`:** holds.
  - The file was first committed after Base (83e3b8ee and 58879782 are both after 955ad466).
  - The test now asserts what plan decision 2 says: no `rerun` line, and the merge goes ahead.
- **w246 3-implement, `supervision_rerun_steps.py::closes_run_alone`, "removed, as the plan lists":** holds.
  - The plan lists it in part 4.
  - The file was first added after Base (58879782).
  - The remaining assertions still show r219.
- **w245's rows** (3-, 4-, 6-, 8-, 9- and 11-implement): verified in branch review 1 and unchanged since. The final `test_supervise_merge_rerun.py` still asserts:
  - one run alone (line 70 of the new file)
  - `--whole-suite` and `-n 0` only
  - no `-n` where the command had none
  - an error refuses
  - a non-scenario refuses
  - an empty rerun refuses

## Cannot verify

None. Every check this review needs has a run in the brief.

## Findings

### 1. Important, no i62 work-item (r214's scenario, i63 w236/w237), observation: the whole suite at HEAD fails one scenario on a held `.git/index.lock`

- **Where:** `tests/scenarios/supervision_faults_steps.py:79` is the step that fails. The failing command is `work run`'s `git add` / `git commit` in the scenario's repository.
- **What is wrong:** `work run` ends with `w1 failed`. The failure is `git commit -q -m work: w1 drafted -> researched … failed: fatal: Unable to create '…/repo/.git/index.lock': File exists.`, so w1 is not green.
- **Why it is a flake and not i62's:**
  - HEAD 215cf7c7 differs from 0b306638 only by w246's `work:` transition commits.
  - The suite passed with 0 failed at 0b306638 (w246's review) and at 0b5e8470 (branch review 1).
  - i62 changed only `supervise_merge.py` and `work_items.py`, and neither is on this path.
- **What I verified (one look each):**
  - **Risk 1, work run's own threads colliding on the index:** they do not. `checkout_changes` runs under the shared `self.lock` (`supervise_worker.py:188-189`). `supervise_all.py:43-46` gives every run the same lock.
  - **Risk 2, a process outside work run holding the lock:**
    - The test double `tests/scripts/stub_claude.py:112-117` retries its own git while `index.lock` is held.
    - `work run`'s git (`supervise_worker.git`, `workqueue.git`) does not retry.
    - So a process outside work run's lock that holds `index.lock`, a session's git in the main checkout or git's own background maintenance, makes `work run` fail a work-item.
  - I could not tell from reading which process held the lock.
- **Why it matters:** this is i62's own subject, q41's "a scenario's git repository is changed by git after its step ends".
  - r219 and r222 tolerate such a flake at a merge.
  - They do not cover the branch review's suite run, or `work run`'s own commits in a scenario.
- **Fix:** find the process that holds the lock. Either have the r214/r218 stub sessions not touch git in the main checkout, or have `work run` retry a git command refused on `index.lock` (this would need a line).
- **The test that would show it (not run):** run that node 50 times alone and side by side: `python3 -m pytest -q -n 8 -p work_items --work-item w237 --whole-suite '<node>' --count 50` (pytest-repeat). Any failure shows the race.
- **Reproduction:** the suite run in the brief at 215cf7c7, its FAILURES section: `AssertionError: ("i1 started\n  w1 failed\n    - git commit … index.lock': File exists.`

### 2. Minor, w246, observation: a node id is matched as a substring (`scripts/supervise_merge.py:165`)

- **What is wrong:** the check is `"FAILED %s" % n in done.stdout + done.stderr`. A node `t.py::test_a` also matches a run whose only failure is `FAILED t.py::test_ab`.
- **Effect:** that run is then added to the question as a first run of `test_a`. The question gets an extra run. The merge is still refused, and nothing is lost.
- **Reproduction:** from reading. In Python, `"FAILED t.py::test_a" in "FAILED t.py::test_ab - x"` is True. (Carried from w246's review, finding 1.)
- **Fix:** parse whole `FAILED` lines as `taken_back` does at line 130, and test membership in `nodes`.

### 3. Minor, no work-item, observation: the range holds other initiatives' commits, all given as `none`

- **What is wrong:** Base 955ad466 predates the work of i48, i54, i55, i60, i61, i63 and i64 on the shared `main`.
  - Their work-item commits (w232, w233, w235-w243), formulate rounds, hand repairs and records are all in the range as `none`.
  - Examples: `20334492 none work: w232 claimed -> done`, `d8f57cc8 none supervision: a change under another run's initiative …`.
- **i62's own commits outside a work-item:**
  - `53c7d203` "i62: the proposal and w245 name r219 and r220 again", a hand repair recorded in w245's Answers (2026-11-02)
  - its formulate rounds (`ec876396`, `bddb538f`, `b6c51aa9`, `c933976`)
  - `19a1f906` "branch review 1 of i62"
- **What I graded against i62:** only w245's and w246's work. Every change under `features/` in the range comes from formulate rounds or from other initiatives' retires. None is in w245's or w246's commits.
- **Fix:** attribute other initiatives' work-item commits to their work-items in the brief, or start the range after the last kept branch review.

### 4. Minor, w245, observation (carried from review 1, findings 3-5)

- **Finding 3:** `has_error` reads after the first "short test summary info" (`supervise_merge.py:120`). A nested summary in captured output refuses a merge r222 would allow. It errs towards refusal.
- **Finding 4:** a node id holding `" - "`, and `-nauto` or `--numprocesses`, are not handled (`supervise_merge.py:130, 136-138`). Both err towards refusal.
- **Finding 5:** a delivery's own `[tests]` commands without the work_items plugin print no `SCENARIO` lines, so a failing scenario never gets r219's second run.
  - **The test that would show it (not run):** a `[tests]` override running plain pytest over a scenario that passes only alone; assert the merge goes ahead.
- **New in this review:** when `taken_back` refuses early, because a run also has a non-scenario failure or an error, a failing scenario of that run gets no second run (`supervise_merge.py:133-134`).
  - r219 says "run that scenario again once, alone, before it refuses the merge".
  - The person's ruling of 2026-11-02 ("a FAILED node that is not a scenario means the run is not taken back") governs whether the merge is taken back. It does not say to skip the scenario's rerun.
  - The merge is refused either way, so no answer is wrong, but r220's "both runs" is then not given.
  - **The test that would show it (not run):** a suite run failing on NODE (a scenario) and on `tests/scripts/test_y.py::test_y`; assert one run alone of NODE and both its runs in the question.

### 5. Minor, w246, drop: `taken_back`'s docstring line is about 190 characters (`supervise_merge.py:124`)

Rewrap it. Ruff does not flag it. Carried from w246's review.

## Feature files

- **Under `features/`:** w245 and w246 changed nothing.
  - r219, r220 and r222 were formulated by rounds ec876396 and bddb538f.
  - Their scenarios are at `features/supervision.feature` @r219, @r220, @r222, and all three pass in w245's and w246's runs.
- **Deprecated scenarios whose replacement's work-item is green:** none of i62's.
  - Outside i62, r28's scenario is deprecated "for removal" while r218, which takes its place, is green (i63 w236).
- **A deprecated scenario that names a replacement with no such title:** the r209/r210 delegation scenario. Not i62's.
- **Scenarios removed that were not deprecated, in i62's commits:** none.
- **Bindings naming no scenario:** none.

## Shape

- **Size:** every file is within 300 lines; `tools size` printed nothing. `supervise_merge.py` has 175 lines.
- **Module map:**
  - The `scripts/supervise*.py` row ("merging") holds the rerun and the question (`supervise_merge.py:116-169`). Met.
  - The `scripts/work_items.py` row ("the pytest plugin of `--work-item`") holds `pytest_runtest_setup` and `pytest_terminal_summary` (`work_items.py:156-170`). Met.
  - The `tests/scenarios/` row holds `supervision_rerun_steps.py`, one concern. Met.
  - The `tests/scripts/` row holds `test_supervise_merge_rerun.py`. Met.
- **Code no line asks for:** none left.
  - The `rerun` log write is removed.
  - The question header naming each first run's command serves r220 and r131.
  - The `SCENARIO <node>` lines serve r219's "a scenario" (the person's ruling of review 10).
- **Unreached code and step definitions:** none. `features bindings` is clean, and every step in `supervision_rerun_steps.py` and in the new part of `supervision_tests_steps.py` is used by @r219, @r220 or @r222.
- **Refactor (observation):** `ALWAYS_FEATURE` (`supervision_rerun_steps.py:9`) and `CLOSES_FEATURE` (`supervision_tests_steps.py:125`) are the same text. They could be one constant in `supervision_world.py`. A check that would show it done: `grep -c 'Scenario: it closes' tests/scenarios/*.py` totals 1.
- **Instance state:** `Merge.second_runs` is set in `merge()`. That is safe: `merge` runs only under the shared `self.lock` (`supervise_merge.py:104-106`, `supervise_all.py:43-46`).

## Coupling

The repository depends on pytest, pytest-bdd and pytest-xdist.

- **pytest's terminal text** is read by `taken_back`, `has_error` and the question (`supervise_merge.py:117-165`):
  - `FAILED <nodeid> - <msg>`
  - the `short test summary info` header
  - `N errors` in the last line
  - `N passed`

  This is display text, not a published interface. A change to it would leave runs not taken back, which errs towards refusal and is not a wrong merge. More stable: have work_items write the failed nodes, errors and scenario flags to a JSON file, and read that.
- **`report.user_properties`** carries the scenario flag from xdist workers to the controller. This is published pytest behaviour, and it shows in the suite run at HEAD (the `SCENARIO tests/scenarios/test_supervision.py::…` line). Stable.
- **pytest-bdd's `__scenario__`** (`work_items.scenario_of`, older than i62) is not published. If it were renamed, no failure would be a scenario, and every run would be refused rather than wrongly merged. More stable: pin pytest-bdd, or use its published marker or hooks.
- **`-n 0`** turns xdist off. That is published, and `pytest.ini`'s `addopts -n auto` is the repository's own.

## Observations

- index.lock flake at HEAD: from the suite run's output at 215cf7c7, `w1 failed … git commit … index.lock': File exists` in the @r214 scenario; the test to show it was not run (finding 1).
- Substring match of a node: from reading `supervise_merge.py:165`; `"FAILED t.py::test_a" in "FAILED t.py::test_ab - x"` is True (finding 2).
- Range attribution: from the brief's Commits, e.g. `20334492 none work: w232 claimed -> done` (finding 3).
- `has_error` reads the first summary header: from reading `supervise_merge.py:120` (finding 4).
- `" - "` in node ids, and `-nauto`/`--numprocesses`: from reading `supervise_merge.py:130, 136` (finding 4).
- `[tests]` commands without work_items never get a second run; test not run (finding 4).
- An early refusal skips the scenario's second run: from reading `supervise_merge.py:133-134`; test not run (finding 4).
