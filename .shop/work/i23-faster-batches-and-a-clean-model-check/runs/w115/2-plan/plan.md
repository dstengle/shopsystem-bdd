# Plan of w115: measure reads what i22 left

Work from the worktree's HEAD. It already holds the r57, r58 and r59 commits and the r47 retirement (5d88909, aecf1e7, 2e956ab). This answers the notes' Q7.

## 1. What goes green

None of the accepted scenarios is red today. The researcher ran all 8 and they pass (notes §1).

- batch-measurement#r47: "a <file kind> of a shape measure does not know is refused, naming it", rows session.json and transcript. Green already.
- batch-measurement#r58: "a transcript line with <line break> inside a JSON string is read as one line", rows U+2028, U+2029 and U+0085. Green already.
- batch-measurement#r59: "a time ending in Z in <file> is read as a time in UTC", rows log.jsonl and a transcript. Green already.
- batch-measurement#r57: "a stage whose session.json is empty is given without its session's figures, named as such". Green already.

The work left is the w110 review's finding against r57, given in the work-item: an empty session.json marks every run of that stage with the same name. Probe A (notes §2, D1) shows it. Two research runs of cart-1 are in the log, the first with an empty session.json and the second with figures. Both stages come back with `session_json` "empty", and the second also carries turns 14 and cost 0.42. No accepted scenario has two runs of one stage, so the red test for this is a new script test (part 2 and decision 2).

Retired: "a <file kind> of a shape measure does not know is refused, naming it (deprecated)" (@r47). It is no longer in `features/batch-measurement.feature`: the scenario at line 23 carries no "(deprecated)" title. The implementer checks that no step or test is left that only that scenario used. If one is left, the implementer removes it.

## 2. Where the change lands

- `scripts/measure_read.py`: `read_session_jsons` stops naming an empty session.json by (work-item, stage name). It names the run instead: the work-item, the stage and the run's number `k` from the directory name `<k>-<stage>`. The number is compared as a number, because the sorted glob puts `10-` before `2-`. Its docstring changes with it.
- `scripts/measure_build.py`: `stages_of` puts the mark only on the start row that the empty run directory belongs to (decision 1). `figures_of` passes the new set through. The `stages_of` docstring changes with it. The `sessions` count in `figures_of` is unchanged (decision 3).
- `tests/scripts/test_measure_runs.py` (new): the red test for the finding (decision 2). It sets up an initiative whose log has two ended runs of one stage, the first with an empty session.json and the second with figures. It runs `measure initiative` and asserts four things: only the first stage is named empty, the second has its figures and no mark, and the totals' `sessions` is 1. It is red today (probe A).

Removed from the researcher's set:
- `features/batch-measurement.feature`, `tests/scenarios/batch_measurement_given_steps.py` and `tests/scenarios/batch_measurement_then_steps.py`. Adding a scenario means accepting a new behaviour scenario, and that is not the planner's or the implementer's job. A script test covers the finding without touching the accepted features (decision 2).

All files stay well under 300 lines (notes §7: measure_read 141, measure_build 126).

## 3. Decisions

1. **How an empty run directory is linked to its stage** (notes Q5). Rests on batch-measurement#r57 ("a stage's session.json is empty" names that stage) and on the work-item's ruling that the empty file is that run's alone.
   - Within each work-item and stage, pair the run directories `<k>-<stage>` (in ascending `k`) with that stage's start rows that have an end (in log order).
   - The empty directory's place in that order gives the start row, and through it the session, that is named empty.
   - Why this holds: `work run` creates a run directory and writes its session.json only just before it logs the stage's end, under one lock. A work-item's stages run one after another, so directories of one stage are made in the order their ends are logged (`supervise_worker.py` worker and run_dir, read).
   - The other reading in Q5, having `work run` record the session id in the run directory before dispatch, changes `supervise_worker.py`. That file belongs to another capability (supervision) and is outside this work-item, so it is not taken.
   - The narrator sees the same thing under either way of linking: the run whose file is empty is named, and no other run is.
2. **The red test is a script test, not a new scenario** (notes Q1). Rests on batch-measurement#r57 as accepted. The finding is a defect against an accepted requirement, not a new behaviour, so the accepted features are left as they are.
3. **`sessions` in the totals counts only sessions that gave figures.** This is the work-item's ruling (reading B, 2026-10-23) with batch-measurement#r42. Probe A already gives 1, and the new test pins it.
4. **Out of scope, unchanged:**
   - lowercase `z` (Q2, D3): r59 names only `Z`;
   - a session.json holding only whitespace (Q3, D4): r57's "empty" is left as the code reads it today, zero bytes;
   - `measure show` printing the empty naming (Q4, G1): r44, r54 and r56 say nothing of it;
   - a commit subject holding U+2028 (Q6, D2): r58 covers transcripts only.

   None of these is changed or decided here. They are passed on to the coordinator in the summary.

## 4. Tests the decisions break

None. The researcher searched `tests/` for session.json, empty, measure_read, measure_build and Z (notes §4). No test asserts the (work-item, stage) key. The accepted r57 scenario has a single run per stage, in a run directory whose number the world gives by enumeration (`batch_measurement_world.py`, read in the notes), with a start and an end. Under decision 1 that one run pairs with its own start, so the scenario's Then (`session_json` is "empty" for the stage) still holds. `tests/scripts/` has no measure test today.

## 5. Open cases

The implementer names each of these in its report. None of them may be resolved by putting the mark on a run whose file is not empty.

- The number of run directories for a work-item's stage differs from the number of that stage's start rows that have an end (a hand-edited log, a lost directory).
- An empty session.json for a stage that has a start and no end. Under `work run` this only happens if the session dies between writing session.json and logging the end. Probe D marks it today.
- A run directory name that is not `<k>-<stage>` with a whole-number `k`.
