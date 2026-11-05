# research of w245: supervision#r222@0.29

Accepted: supervision#r222@0.29 (second run of a scenario that r219 makes passes, taken as passing in r4's merge). Depends on r219 (rerun once, alone), r4 (merge), r43. No `tools map` exists: every test list below is `by search`; `refs` and `wc` used where stated. No `Scripts:` tools run beyond `--help`.

## 1. Why each scenario is red today

Scenario: `features/supervision.feature:2081` "a scenario that fails before a merge and passes on its second run, alone, lets the work-item branch be merged".

Command (run): `python3 -m pytest -q -rfE --work-item w245 -p no:warnings`
Result (run): 1 failed, 181 passed, 1 skipped. Failing: `tests/scenarios/test_supervision.py::test_a_scenario_that_fails_before_a_merge_and_passes_on_its_second_run_alone_lets_the_workitem_branch_be_merged`.
Error (run): `StepDefinitionNotFoundError` for Given at feature line 2086: `the work-item's scenario "it closes", tagged @r1, fails on the implementer's branch in its run with w1's scenarios and passes there on its second run, alone`. pytest-bdd stops at the first undefined step, so the later When and Then were not reached.

Missing (read):
- Step: `tests/scenarios/supervision_given.py:147-150`, regex `(the work-item's scenarios|the whole suite) fails? on the implementer's branch$` does not match the trailing "in its run with ... passes there on its second run, alone" nor the "it closes" title.
- Fixture: `tests/scenarios/supervision_tests_steps.py:66-77` `THING_FEATURE` has "it answers" and "it waits" only, no "it closes" tagged @r1.
- Stub `tests/scenarios/supervision_world.py:19-22` fails on a marker file (`scenarios-fail`), in every run; it has no way to fail only in the run with w1's scenarios and pass alone.
- Code: `scripts/supervise_merge.py:126-132` (`Merge.merge`) runs the scenarios, then the suite, once each; the first non-zero run returns the question. No second run exists, so even with the step bound the merge would be refused. The Then "the initiative branch has the implementer's commit" is bound (`test_supervision.py:131`).

## 2. Old assumptions

Old form: one failing run of a work-item's scenario refuses its merge at once (r4). Search for the places that rely on it: `refs suite_record` (2 in `supervise_merge.py`), `refs TESTS` (1 production, 1 test file, unrelated fixture), `refs Merge` (0 references by name; `supervise.py:42` inherits it, `supervise.py:150` calls `implement`, `supervise_merge.py:106` calls `merge`; by read).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_merge.py:Merge.merge (126-132) | runs scenarios then suite once; any non-zero run returns the question | a failing scenario gets one run alone before refusal (r219); pass means merge (r222); the suite run's scenario failures too | `test_supervision.py` r4 outline (features:72-88), r5 deprecated (89-97), r43 outline (761-780); by search | read; refs |
| scripts/supervise_merge.py:Merge.merge question text (131-132) | names the failing run's output only | r220: both runs in the question (not w245's, same code) | r4 "work-item's scenarios fail" row executes it; by search | read |
| scripts/supervise_merge.py:Merge.suite_record (35-53) | names failing and XFAIL of the suite run; the record is logged | after a passing rerun the record still names the scenario as failing; no line for the rerun | `supervision_tests_steps.py:139-152` (`check_counted`), `supervision_then_workers.py:108-120`; by search | refs (2, both in merge); read |
| scripts/supervise_merge.py:Merge.merge scenario run (128) | takes `tests["work_item"]`'s return code; does not parse failing names | a rerun needs each failing scenario's node id, from pytest output; no node id for a `[tests]` override | none: none | read |
| tests/scenarios/supervision_world.py:19-22 (stub tests.py) | fails for every run while `scenarios-fail` or `suite-fail` exists | the r222 fixture must fail once with w1's scenarios and pass alone | r4 rows 2 and 3, r5 (by search) | read |
| scripts/work_items.py:128-145 (`--work-item` selection) | keeps the accepted scenarios and non-scenarios; refuses a set with none accepted | a rerun by node id must pass this filter for w1's requirement | unverified: `tests/scripts/test_work_items.py` not read | read |

## 3. Tests the requirements make impossible to keep

No test can no longer pass as its assertions stand, by search; two can break depending on the design choice in part 4.
- `tests/scenarios/supervision_tests_steps.py:23-27` (`ran_delivery_tests`): every `tests` argv must be `["--work-item","w1"]` or `[]`. A rerun through `[tests]` with a node id appended breaks it, if a scenario it binds reaches a failing run. Not read which feature scenario binds it: by search.
- `supervision_tests_steps.py:145-152` (`check_counted`): exactly one `event == "suite"` line per stage for w1. A rerun logged under event `suite` breaks the r43 scenarios (features:761-800). A rerun logged under another event does not.
- Sound by search: r4 row "the work-item's scenarios fail" (features:84) and row "the whole suite fails" (85): the stub keeps failing on the rerun, so still not merged. r5 (89-97) is deprecated and stays refused. `supervision_tests_steps.py:37-48` (`--work-item` on each pytest, the worker's `-q`) are unaffected: a rerun is an added pytest call that must carry `--work-item`.

## 4. The file set

Production (must change):
- `scripts/supervise_merge.py` — `Merge.merge`: rerun each failing scenario alone once, then merge or refuse (r219, r222); `suite_record` may need no change. Found by read and refs.

Tests (must change):
- `tests/scenarios/supervision_given.py` — new Given binding the r222 step text (regex at 147-150). Found by read and the run.
- `tests/scenarios/supervision_tests_steps.py` — "it closes" tagged @r1 in `THING_FEATURE` (66-77). Found by read.
- `tests/scenarios/supervision_world.py` — stub `tests.py` fails the first run with w1's scenarios only (19-22). Found by read.

Modules on the change path, edited or not (`wc -l`; room under the 300 limit from CLAUDE.md):
- `scripts/supervise_merge.py` 138 lines, room 162 (edited).
- `scripts/supervise.py` 295 lines, room 5 (composes `Merge`; keep the rerun out of it).
- `scripts/work_items.py` 164 lines, room 136 (node-id selection; read only).
- `tests/scenarios/supervision_given.py` 259 lines, room 41 (edited).
- `tests/scenarios/supervision_tests_steps.py` 218 lines, room 82 (edited).
- `tests/scenarios/supervision_world.py` 175 lines, room 125 (edited).
- `tests/scenarios/test_supervision.py` 269 lines, room 31 (binds the feature; no change expected).

## Readings for the planner

- Scenario rerun by node id (r219 "alone"): read as parsing pytest node ids from the failing run's output and running `python3 -m pytest -q -p work_items --work-item w1 <node id>`. A `[tests]` override has no node ids: either refuse the rerun, or rerun the whole work-item command once. Both readings are open.
- A scenario that fails only in the whole-suite run (second run of merge): read as covered by r219 ("a run that work run makes before a merge"). Not stated in r222.
- The merge record keeps the first run's failing name even after a passing rerun (part 2). Whether the rerun is logged, and under which event, is open (part 3).
- r219 and r220 scenarios (features:2062-2079) are also undefined and not accepted by w245: `It was run once more, alone` has no step. Not covered by w245.
