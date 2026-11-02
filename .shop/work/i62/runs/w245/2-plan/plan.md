# plan of w245: supervision#r222

## 1. What goes green

- **supervision#r222**: "a scenario that fails before a merge and passes on its second run, alone, lets the work-item branch be merged" (`features/supervision.feature:2081`).
  Red today (notes part 1): the Given at feature line 2086 has no step definition (`StepDefinitionNotFoundError`). The step at `supervision_given.py:147` ends in `branch$` and does not match it, and no fixture has an "it closes" scenario tagged @r1. Behind the missing step, `Merge.merge` in `scripts/supervise_merge.py` runs the scenarios and the suite once each and refuses on the first non-zero run. It has no second run, so the merge would still be refused once the step is bound. The Then ("the initiative branch has the implementer's commit of feature.txt") is already bound.
- No deprecated scenario is retired: the work-item has no `## Retires` and no `## Rulings`.
- The r219 and r220 scenarios (features:2062-2079) are not accepted by w245 and stay red. Their step "fails on the implementer's branch each time it is run" and the Then "was run once more, alone" are not part of this work.

## 2. Where the change lands

- `scripts/supervise_merge.py`: `Merge.merge` changes. After the suite run and the work-item's scenario run, it collects the scenarios each failing run names. It runs each distinct scenario once more, alone. A scenario whose second run passes counts as passing in that run (r222). The merge goes ahead only when every failure of both runs has been taken back this way. Otherwise it refuses as today. The second run gets its own log line (decision 4). `suite_record` keeps its present output. A small helper for the failing names, shared with `suite_record`'s `named`, may be split out. The file has 138 lines, so there is room.
- `tests/scenarios/supervision_tests_steps.py`: a new Given binding the step text of feature line 2086. It writes a real pytest-bdd fixture into the repository and removes `.shop/delivery.toml`, as `thing_waits` does, so that `work run`'s own commands run it. The fixture has "it answers" and "it closes", both tagged @r1. "it closes" fails when its run was not given its own node id and passes when it was (decision 5). This is a new fixture text, not an addition to `THING_FEATURE` (decision 6). The file has 218 lines, so there is room.
- `tests/scenarios/supervision_world.py` is **dropped** from the researcher's set. Its stub `tests.py` serves the `[tests]` override, and the r222 fixture runs through `work run`'s own pytest commands instead (decisions 5 and 6). The stub keeps failing on every run, which the r4 rows need.
- `tests/scenarios/supervision_given.py` is **dropped** from the researcher's set. The new Given goes in `supervision_tests_steps.py` with the other fixtures about the tests `work run` runs. `supervision_given.py` has only 41 lines of room. Its step at line 147 is anchored with `$` and does not clash with the new step text.
- Not edited: `scripts/supervise.py` (295 lines; the second run stays inside `Merge`), `scripts/work_items.py` (a node-id run under `--work-item w1` already keeps an accepted scenario, by the notes; see open case 3) and `tests/scenarios/test_supervision.py`.

## 3. Decisions

1. **Which runs give a second run.** Both of the runs `Merge.merge` makes before the merge can give one: the whole-suite run and the work-item's scenario run. The suite run the implement stage makes before the implementer starts does not, because it does not gate a merge. Rests on supervision#r219 ("a run that `work run` makes before a merge" whose failure "would keep r4 from merging") and supervision#r4.
2. **Once per scenario, not once per run.** A scenario that fails in both runs before the merge gets one second run, alone, not one for each run. Its result counts for both runs. Rests on supervision#r219 ("run that scenario again once") and supervision#r222.
3. **How a scenario is named and run alone.** The failing scenarios are the node ids in the `FAILED <node id>` lines of the failing run's output. `suite_record` already reads these lines; pytest prints them by default, and the suite command adds `-rfEx`. The second run is the work-item's scenario command (`tests["work_item"]`) with that node id appended. It runs without `-n auto`, since it runs one scenario. Under a `.shop/delivery.toml` `[tests]` override, it is the override's work-item command with the node id appended. A failing run whose output names no scenario gives no second run and is refused as today, because r219 concerns a scenario that `work run` can name. This keeps the r4 rows "the work-item's scenarios fail" and "the whole suite fails" refused: their stub prints `FAILED:`, not a node id. Rests on supervision#r219, supervision#r4 and the Implementation line on the commands and `[tests]`.
4. **The second run's record.** Each second run gets a `log.jsonl` line under its own event, not `suite`. The line names the work-item, the stage `merge`, the scenario and whether it passed. The suite record and the `merged` line keep naming the first run's failure. Rests on the Implementation line "a `suite` line for each whole-suite run before a merge": a second run is not a whole-suite run. This keeps `check_counted` at one `suite` line per stage.
5. **How the fixture tells "alone" from "with w1's scenarios".** The "it closes" step fails unless its pytest run was invoked with its own node id. The pass therefore follows from the second run being alone (r219's "alone"), not merely from it being second. Rests on supervision#r222 and the scenario's own words ("fails … in its run with w1's scenarios and passes there on its second run, alone").
6. **A fixture of its own, not `THING_FEATURE`.** "it closes" goes in a new fixture text written only by the new Given. If it were added to `THING_FEATURE`, it would also be w1's scenario and fail in every scenario that writes `THING_FEATURE` (features:452, 462, 472, 765, 785). That would break `pytest_deselected`, which requires "failed" to be absent from the implementer's `pytest -q`, and the r43 outlines. Rests on supervision#r4 and supervision#r43 staying green.

## 4. Tests the decisions break

None. I checked:
- r4 rows "the work-item's scenarios fail" and "the whole suite fails" (features:84-85) run the stub `tests.py` under `[tests]`. It prints `FAILED:` with no node id, so decision 3 gives no second run. The merge is refused as today, and `ran_delivery_tests` sees no extra argv.
- The `[tests]` scenario (features:583) passes both runs, so it makes no second run. `ran_delivery_tests` still sees only `["--work-item","w1"]` and `[]`.
- r43 outlines (features:761-800): "it waits" is xfail under `--whole-suite`, not a `FAILED` line, so it gets no second run. The second run's log line is not under the `suite` event (decision 4), so `check_counted` still finds exactly one record.
- `pytest_given_work_item` (features via `supervision_tests_steps.py:37-42`): a second run is a pytest call carrying `--work-item w1`. It is not `--whole-suite`, so `suites` stays non-empty and shorter than `ran`.
- `THING_FEATURE` is unchanged (decision 6), so `pytest_deselected`, `pytest_succeeded` and the r43 scenarios are untouched.
- The r5 outline is deprecated, and its stub still fails, so its merge stays refused.

## 5. Open cases

1. A failing node id that is a plain test, not a scenario, in the whole-suite run. r219 and r222 name scenarios only, so the implementer names how `Merge` tells a scenario's node id from another test's, or says it cannot.
2. A pytest-bdd parametrized scenario (an outline row): the node id carries `[...]`, which the second run must pass as one argument.
3. Whether a node-id run under `--work-item w1` that selects a scenario of another work-item's requirement is refused by `work_items.py`'s selection. The notes did not verify this (`tests/scripts/test_work_items.py` not read).
4. A `[tests]` override whose work-item command does not take a node id: the second run fails or runs more than the scenario.
5. The text of the question when a second run fails too. That is r220's, not this work-item's. The present question stays as it is.
