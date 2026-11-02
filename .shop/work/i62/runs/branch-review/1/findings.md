# Branch review of i62

**Verdict: DONE_WITH_CONCERNS.** w245 delivers supervision r219, r220 and r222. All three scenarios are green in the whole suite and in w245's own run. No test or scenario was weakened by w245. I found two Important findings in w245's commits, both triaged **fix now**:

1. A refused merge's question can lack a scenario's first run, against r220.
2. The new `rerun` line in `log.jsonl` is written output that no Behaviour line and no Implementation line asks for.

Nothing is Critical. Every check has a run in the brief.

## Range reviewed

- **Range:** `955ad466..0b5e8470` on `main`, the initiative branch.
- **i62's work-item:** w245 (`under: supervision`, accepts supervision#r219, r220, r222), status green.
- **w245's commits:**
  - b274fa52: r222 rerun, first cut
  - 83e3b8ee: r219 and r220 bound; the question gives the second run
  - 58879782: one run alone, whatever number of runs failed
  - f968f32a: errors, non-scenarios and empty reruns are not taken back
  - 7f37149d: the rerun is built from the suite command
  - fa1b6eea: scenario-ness comes from work_items' `SCENARIO` lines; `-n 0` only where `-n` was given; errors read from the summary
  - the `work:` transition commits of w245
- **Commits for no work-item:** the brief attributes every other commit in the range to no work-item. The finding on this is under Range, below.

## Suite

`Suite: 1101 passed, 0 failed at 0b5e8470 in 35.33 s` (from the brief's run, which exited 0). The same run also gave 1 skipped, 23 xfailed, 11 xpassed and 56 subtests passed.

- **Parallel:** yes (`-n auto`).
- **In-process:** no. The supervision steps run `work run` as a subprocess (`tests/scenarios/test_supervision.py:81`).
- **No finding:** the suite is under 60 s.
- **Dry-run and real mode:** the system has no dry-run mode of one of its own operations. The only `--dry-run` is `git push --dry-run`, used as a push check (`scripts/supervise_review.py:55`, `scripts/supervise_faults.py:71`). So no agreement test is due.

## Checks

All runs below were made at 0b5e8470.

- **w245's scenarios** (`pytest -q -n auto -p work_items --work-item w245`): exit 0, 194 passed, 1 skipped, 56 subtests passed.
- **`tools check --base 955ad466`:** exit 1.
  - **ruff:** 29 hits, none in a file w245 touched except `tests/scenarios/test_supervision.py:14` I001. That hit is older than w245: the import block is already out of order at `supervision_branch_steps`/`supervision_answers_steps` (lines 27-28) and `supervision_review_steps`/`supervision_reintegrate_steps` (lines 41-42). w245's one import (line 44, `supervision_rerun_steps`) is in order.
  - **ruff, other initiatives:** the other hits are in other initiatives' files:
    - `scripts/supervise_change.py:83,103,130` B023 (i48 w238)
    - `tests/scenarios/supervision_proposal_steps.py`, `supervision_reintegrate_steps.py`, `work_queue_list_steps.py`
    - `tests/scripts/stub_claude.py`, `tests/scripts/test_supervise_change.py`
    - `.shop/work/*/runs/*/splice.py` and `mk.py` (round scratch scripts, tracked)
  - **vulture:** `tests/scenarios/work_queue_status_steps.py:100` unused variable `notes`. Not w245's.
  - **import-linter:** the project states no import contracts.
- **`tools size`:** exit 0, nothing printed. No file is over the limit, and none of w245's files is.
- **`features deprecated`:** exit 0, 23 deprecated scenarios listed. None is i62's. See Feature files.
- **`features bindings`:** exit 0, "every binding names a scenario".

## Removed and weakened tests

**w245: none.** I searched the range's change for:

- removed `def test_`
- removed or changed `assert` lines
- changed parametrize lists
- added `skip` or `xfail`
- changes under `features/`

What w245's commits did to tests:

- `tests/scripts/test_supervise_merge_rerun.py` is new in the range (first committed in 58879782, after Base). Its in-range rewrites are covered under Allowances.
- `tests/scripts/test_work_items.py`, `tests/scenarios/supervision_rerun_steps.py` and `tests/scenarios/supervision_tests_steps.py` only add code.
- `tests/scenarios/test_supervision.py` gains one import.

**Other initiatives:** these tests changed in the range in commits the brief gives to no i62 work-item. I did not assess them against their own plans; their initiatives' branch reviews are in the range.

- `tests/scripts/test_supervise_change.py:37`: the expected value changed from `adds: [thing#r5]` to `adds: [thing#r1, thing#r5]`. This is i48 w238, for r188.
- `tests/scripts/test_workqueue_done.py:19`: the parametrize case `("merged", True)` became `("merged", False)`. This is i55, for work-queue r62/r47.
- Deprecated scenarios were retired: r9, r105, r23, r14. That is i55's work (w239, w241).

## Allowances

The early reports had nothing to verify:

- **3-implement, 4-implement, 6-implement:** "none".
- **11-implement, `tests/scripts/test_supervise_merge_rerun.py` (setup/interim):** holds. The file was first committed after Base (in 58879782, per reviews 7, 10 and 12). The final file asserts what the person's answers say:
  - one run alone (line 70)
  - `--whole-suite`, and `-n 0` as the only `-n` value (lines 71-72)
  - no `-n` where the command had none (line 105)
  - an error refuses (lines 88-89 and 119-120)
  - a non-scenario refuses (lines 96-97)
  - an empty rerun refuses (lines 127-128)
- **8-implement, setup** (the file's setup and lint respelled; the two tests keep their asserts): holds, as review 10 verified on f968f32a.
- **9-implement, interim** (the first test's `-n`/`--whole-suite` assertion and the fixture's suite command): holds. The file was first committed after Base, and the new assertion is what the person's answer of 2026-11-02 asks for ("Add a test that the rerun command has --whole-suite and -n 0 and no other -n value").

## Cannot verify

None. Every check this review needs has a run in the brief.

## Findings

### 1. Important, w245, fix now: a refused merge's question can leave out a scenario's first run (scripts/supervise_merge.py:164-169)

- **What is wrong:** when both runs before the merge fail, the question holds the output of `failed[0]` only (the work-item's scenario run), followed by every failed second run.
- **When it bites:** a scenario S can fail only in the whole-suite run, for example another capability's scenario the implementer broke, while one of the work-item's own scenarios fails in both runs. If S's second run alone also fails, the question gives S's second run but not its first. The whole-suite output is not in the question.
- **Why it matters:**
  - r220 says: "If the second run of a scenario that r219 makes also fails, then `work run` shall give both runs of the scenario in the question r131 writes for the work-item."
  - The question is the only place the person reads the failure. `suite_record` logs a count, not the output.
  - The header also names only the first failing command.
  - The r220 scenario covers only the case where the scenario fails in both runs, so it does not catch this.
- **Fix:** give in the question the output of every failing run that names a scenario whose second run failed, or of both runs whenever both failed, with each run's command.
- **The test that would show it (not run):** in `tests/scripts/test_supervise_merge_rerun.py`, stub the scenario run's output as failing on `NODE` and the suite run's output as failing on `NODE` and on `OTHER` (each with its `SCENARIO` line). Let `NODE`'s run alone pass and `OTHER`'s fail. Assert that the question holds `OTHER`'s `FAILED` line from the suite run as well as its second run.

### 2. Important, w245, fix now: code no line asks for, the `rerun` line in `log.jsonl` (scripts/supervise_merge.py:147)

- **What is wrong:** each second run appends `{"event": "rerun", "scenario": …, "passed": …}` to the initiative's `log.jsonl`, which is a committed file.
- **Why it matters:** no Behaviour line asks for this line.
  - r8 and r49 cover workers and the branch reviewer.
  - The Implementation section (supervision.md:209) names only `push verified` and `suite` lines.
  - The plan's decision 4 rests on the `suite` line, but a rerun is not a whole-suite run, as the plan itself says.
  - Behaviour reaches code only through a line.
- **Where it is used:** the r219 step reads this log line (`tests/scenarios/supervision_rerun_steps.py:54-55`). The same step already counts the runs alone from `closes.runs` (line 53, `runs[-1:] == ["alone"]`; "run no other time" counts `alone == 1`). So the log assertion is not needed to show r219.
- **Fix:** either write the line first through integrating-a-proposal (for example an Implementation line: "and a `rerun` line for each second run of a scenario before a merge"), or remove the log write and the step's `reruns` assertion.

### 3. Minor, w245, observation: `has_error` reads after the first "short test summary info" (scripts/supervise_merge.py:120)

- **What is wrong:** `partition` takes the first header. A failing supervision scenario's captured output can hold a nested pytest summary, because these scenarios run `work run`, which runs pytest.
- **Effect:** an `ERROR ` line in that nested summary refuses a merge that r222 would allow. This errs towards refusal.
- **Reproduction:** from reading only, carried from review 12, finding 1.
- **Fix:** `rpartition`.

### 4. Minor, w245, observation: node ids and `-n` forms (scripts/supervise_merge.py:131, 137-139)

- A node id containing `" - "` (an outline row whose example holds it) is cut short. Its id then is not among the `SCENARIO` lines, so the run is refused.
- `-nauto` and `--numprocesses` are not stripped, so the rerun keeps xdist.
- Both err towards refusal, and no client sends them today.
- **Reproduction:** from reading only (review 5, finding 4).

### 5. Minor, w245, observation: a delivery's own `[tests]` commands never get a second run (scripts/supervise_merge.py:133-135; r29 with r219)

- **What is wrong:** `SCENARIO` lines come only from the work_items plugin under `--work-item`. Under a `.shop/delivery.toml` `[tests]` whose commands do not load it, every failing scenario counts as a non-scenario, so it gets no second run. That goes against r219 for such a repository.
- **Status:** no client is known to rely on it. 11-implement's report names it.
- **The test that would show it (not run):** a scenario with a `[tests]` override running plain `pytest` over a pytest-bdd fixture whose scenario fails unless it is run alone, then asserting that the merge goes ahead.

### 6. Minor, i62 (no work-item), observation: hand commit 53c7d203 "i62: the proposal and w245 name r219 and r220 again"

- It changes `w245.md`'s `accepts:` and the proposal's `adds:` outside any work-item.
- It is recorded as the person's session in w245's Answers (2026-11-02).
- Named here because it belongs to no work-item.

### 7. Minor, w245, drop: file set and duplication

- **File set:** w245's `fileset:` names `scripts/supervise_merge.py` and `tests/scenarios/supervision_tests_steps.py`. Its commits also touch:
  - `scripts/work_items.py`
  - `tests/scenarios/supervision_rerun_steps.py`
  - `tests/scenarios/test_supervision.py`
  - `tests/scripts/test_supervise_merge_rerun.py`
  - `tests/scripts/test_work_items.py`

  The reports and the person's answers widened the work.
- **Duplication:** `CLOSES_FEATURE` (`supervision_tests_steps.py`) and `ALWAYS_FEATURE` (`supervision_rerun_steps.py`) are the same text.
- **Instance attribute:** `Merge.second_runs` is set in `merge()`, not in `__init__`. I verified that this is safe: `merge` is only called under `self.lock` (`supervise_merge.py:104-106`), so two merges never share it at once.

### Range: commits the brief attributes to no work-item (Minor, observation)

- **What is wrong:** Base (955ad466) predates the work of i48, i54, i55, i60, i61, i63 and i64 on the shared `main`. The range therefore holds their code and feature commits:
  - work-items w232, w233, w235-w243
  - formulate rounds
  - hand repairs, for example 556cba3b, c0d2f0e2, 28ce4056, a411ea7a, ef8e1609, f7659913, 74132b41 and 9b453fd2
  - records: 60d88d6d, 3031e154

  The brief gives every one of these as `none`. Their own branch reviews are in the range (for example ff632c3a, ea0d0022, 583f7064, 212ee994, 52de5b39 and 89e0b98b).
- **What I reviewed:** I reviewed i62's work against w245. I read the rest of the change once and graded nothing in it against i62.
- **Features changes:** every change under `features/` in the range comes from formulate rounds or from other initiatives' retires. None of them is in w245's commits.
- **Fix:** attribute other initiatives' work-item commits to their work-items in the brief, or start the range at i62's first commit after the last kept branch review.

## Feature files

- **w245** changed nothing under `features/`. r219, r220 and r222 were formulated by rounds ec876396 and bddb538f.
- **Deprecated scenarios whose replacement's work-item is green:** none among i62's.
- **Outside i62:**
  - The deprecated r209/r210 scenario names a replacement "r209 and r210", which `features deprecated` reports as "no scenario has that title".
  - r28's scenario is deprecated "for removal" while r218, which takes its place, is green under i63's w236.
  - The scenarios of requests r39, r41 and r43 were rewritten in place as r56, r57 and r58 by i55's formulate round 627b4a71, with no deprecation step. Those lines were retired before Base.
- **Scenarios removed that were not deprecated, in w245's commits:** none.
- **Bindings naming no scenario:** none.

## Shape

- **Size:** all within 300 lines. `scripts/supervise_merge.py` has 175 lines; `tools size` printed nothing.
- **Module map:**
  - The `scripts/supervise*.py` row ("merging") holds the rerun. Met.
  - The `scripts/work_items.py` row ("the pytest plugin of `--work-item`") holds `pytest_runtest_setup` and `pytest_terminal_summary` (work_items.py:162-176). Met.
  - The `tests/scenarios/` row (one `<capability>_*_steps.py` module per concern) holds `supervision_rerun_steps.py`. Met.
  - The `tests/scripts/` row holds `test_supervise_merge_rerun.py`. Met.
- **The `SCENARIO <node>` lines:** work_items prints them under `--work-item`. That is output serving r219's "a scenario" (the person's ruling of review 10), not a line of its own.
- **Unreached code:** none. `is_scenario` was removed in fa1b6eea, and no step definition of w245 is left without a scenario (`features bindings` is clean).
- **Refactor (observation):** the two identical fixture texts (finding 7) could be one constant in `supervision_world.py`. A check that would show it done: `grep -c 'Scenario: it closes' tests/scenarios/*.py` gives 1.

## Coupling

The repository depends on pytest, pytest-bdd and pytest-xdist.

- **pytest's terminal text** (`FAILED <nodeid> - <msg>`, the `short test summary info` header, `N errors` in the last line, `N passed`) is read by `taken_back` and `has_error` (supervise_merge.py:120-143).
  - This is display text, not a published interface. A change in its wording would make runs not taken back (refusal side), or make an `N passed` match fail (refusal side).
  - **More stable:** have work_items write the failed nodes, errors and scenario-ness to a file (for example a JSON report via `pytest_terminal_summary` or `pytest_sessionfinish`) and read that.
- **`report.user_properties`** carries the scenario flag from xdist workers to the controller. This is published pytest behaviour, and it was seen working under `-n auto` (review 12, log.jsonl:125). Stable.
- **pytest-bdd's `__scenario__` attribute** (work_items.scenario_of, older than w245) is not a published attribute of pytest-bdd. A pytest-bdd release could rename it, and then no failure would be a scenario: every run would be refused, never wrongly merged. More stable: pin pytest-bdd, or tell scenarios by the `pytest_bdd` marker or hook that pytest-bdd publishes.
- **`-n 0`** turns xdist off (published), and `pytest.ini`'s `addopts -n auto` is the repository's own.

## Observations

- has_error reads the first summary header: from reading supervise_merge.py:120; an output quoting a nested `short test summary info\nERROR x::y` before the real summary gives True (finding 3).
- `" - "` in a node id, and `-nauto`/`--numprocesses`: from reading supervise_merge.py:131,137 (finding 4).
- `[tests]` commands without the work_items plugin: never taken back; test not run (finding 5).
- Range attribution: the brief's Commits list gives `none` for w232-w243's commits, for example `20334492 none work: w232 claimed -> done` (Range).
