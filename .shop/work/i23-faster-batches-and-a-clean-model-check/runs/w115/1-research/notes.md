# w115 research notes

Method: `tools` from the plugin's Scripts path. `refs` ran (static). `tests-of` answered "no map" and no map was made, so tests were found by search (`by search`). Worktree HEAD is 44aff93; the brief's Base 1ad628 is its ancestor. The r57, r58, r59 and retired-r47 changes are already in HEAD (commits 5d88909, aecf1e7, 2e956ab), so the accepted scenarios pass today. Probe files: `.shop/scratch/w115-1-research/probe_measure.py`, `probe_show.py`, `probe_git.py`. Run each with `python3 -m pytest -q -s -n 0 -p no:cacheprovider <file>`; `-n 0` is needed because `pytest.ini` runs xdist and hides prints.

## 1. Why each scenario is red today

No accepted scenario is red. Command, run: `python3 -m pytest -q -p no:cacheprovider` with the 8 node ids from `--collect-only` on `tests/scenarios/test_batch_measurement.py` (run: "8 passed").
- r47, session.json row: pass (run).
- r47, transcript row: pass (run).
- r58, U+2028, U+2029, U+0085 rows: pass (run).
- r59, log.jsonl row and transcript row: pass (run).
- r57, empty session.json: pass (run).

The work-item's open gap is the w110 finding on r57. No accepted scenario covers it (see section 6, D1).

## 2. What the system answers today

Each probe is `run` unless marked `read`. Output below is trimmed.

- **A, two runs of one stage, the first empty (D1 reproduction).** `probe_measure.py::test_a_two_runs_of_one_stage_one_empty_one_with_figures`, run. The log has cart-1 research at 10:00 (session s-1) and at 11:00 (session s-3). `runs/cart-1/1-research/session.json` is empty and `runs/cart-1/2-research/session.json` has figures. Result, rc 0: both stages carry `"session_json": "empty"`. The s-3 stage also carries turns 14, cost 0.42. Totals: `sessions` 1.
- **B, session.json holding only "\n".** `test_b_session_json_with_only_a_newline`, run. rc 1, stderr: `.../runs/cart-1/1-research/session.json is not a session.json of a shape measure knows (no usage with input and output tokens)`. No measurement written. The file is not zero bytes, so `read_session_jsons` does not take the empty path (see D4).
- **C, stage with no session.json at all.** `test_c_stage_with_no_session_json_at_all`, run. rc 0. The stage has start, end and "12 minutes", with no figures and no `session_json` key. Nothing is named.
- **D, empty session.json, stage with a start and no end.** `test_d_empty_session_json_on_stage_with_start_and_no_end`, run. rc 0. The stage has `started` and `"session_json": "empty"`, with no took and no figures.
- **E, U+2028, U+2029, U+0085 in a user row and in assistant rows.** `test_e_unicode_line_breaks_in_user_and_assistant_rows`, run. rc 0. The stage has `round_trips` 3, which is the count of distinct requestIds.
- **F1, Z with a fraction, `2026-10-22T07:55:00.500Z` to `11:40+02:00`.** `test_f_z_with_fraction_and_lowercase_z`, run. rc 0. Window starts at `07:55:00.500000+00:00`, totals `time` "1 hour 45 minutes".
- **F2, lowercase `z`.** Same test, run. rc 1, stderr: `.../log.jsonl: '2026-10-22T07:55:00z' is not an ISO time`.
- **G, `measure show` of A and of D (r57's naming).** `probe_show.py`, run. Neither table shows `session_json`. In A the s-3 row shows figures and no mark. In D the plan row shows no mark. The naming exists only in the JSON block (`scripts/measure_show.py`: STAGES has no such column; grep for `session_json` finds only `measure_build.py:44`).
- **H, U+2028 in a commit subject, `probe_git.py`, run.** Commits: "start", "fix a b", "work: cart-1 claimed -> done". Result: rc 1, uncaught `ValueError: not enough values to unpack (expected 2, got 1)` at `scripts/measure_build.py:71` (D2).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/measure_read.py:read_session_jsons (68-78) | collects zero-byte session.json as `(work-item, stage name)` from the run directory name `<k>-<stage>`; no session id is available | must mark only the run whose file is empty, not every run of that stage | test_a_stage_whose_sessionjson_is_empty... (by search; run: pass) | read; grep; `refs` shows 0 uses, see note |
| scripts/measure_build.py:stages_of (32-44) | `(work-item, stage) in empty` marks every stage with that name; this is D1 | the mark must follow the run, not the name | same test (run: pass); probe A (run: fails the requirement) | read |
| scripts/measure_build.py:figures_of (111) | passes the `(work-item, stage)` set from read_session_jsons | changes with the key | same test | read |
| scripts/measure_build.py:figures_of (114) `sessions` = stages with turns | counts only stages with figures (ruling B) | must still count only those; probe A gives 1 | probe A (run) | read |
| scripts/measure_build.py:33-34 docstring | says `empty` is "its work-item and stage" | doc change only | none | read |
| tests/scenarios/batch_measurement_given_steps.py:88-91 | stores the empty stage under key `empty-<item>-<stage>` with text "" | no session id; a two-run fixture needs its own Given | the r57 scenario (run: pass) | read |
| tests/scenarios/batch_measurement_world.py:93-96 | numbers run directories by enumeration of the sessions dict | fixture works with two sessions of one stage | the r57 scenario (run: pass) | read |
| tests/scenarios/batch_measurement_then_steps.py:105-108 | asserts `session_json == "empty"` for the stage | still holds under per-run keying | r57 scenario (run: pass) | read |
| scripts/measure_build.py:69 `done.stdout.splitlines()` (merged_commits) | splits git log output on U+2028 and similar | not in r58's scope (transcripts), but a subject with U+2028 crashes (D2) | none run; r41 scenario by search (not run) | read; probe H (run) |
| scripts/measure_read.py:json_rows (22-35) | `split("\n")` since aecf1e7 (r58) | none; already done | r58 scenarios (run: pass) | read; git show aecf1e7 |

Note: `refs read_session_jsons` reports 0 references, but `measure_build.py:111` calls it and `refs read_transcripts` reports 0, but `measure_build.py:97` calls it. Names imported with `from measure_read import` are not counted. Use grep for those.

## 4. Tests the requirements make impossible to keep

None. `tests-of` had no map (`tools: no map: make one with tools map`); I did not make one. By search over `tests/` for session.json, empty, measure_read, measure_build and Z: only `batch_measurement_given_steps.py`, `batch_measurement_then_steps.py`, `batch_measurement_reading_steps.py` (TZ), `batch_measurement_world.py` and `test_batch_measurement.py`. None asserts the `(work-item, stage)` key or `splitlines`. The 8 accepted tests pass today (run). Under per-run keying they still pass, because each has one run per stage. No test in `tests/scripts/` concerns measure (`ls tests/scripts | grep measure` is empty).

## 5. A step the work-item skips

None. The work-item adds no path that skips a step. The r57 change only changes which stage receives the mark.

## 6. Defects

**D1. A stage's empty session.json names every run of that stage.** Command: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w115-1-research/probe_measure.py -k two_runs` (run). Came back: both stages `"session_json": "empty"`, and the figured run carries turns 14 and cost 0.42. Cause: `measure_build.py:43-44` (`stages_of`). Reading: the work-item's r57 says the stage is named "as a stage whose session.json is empty". The empty file has no session id, so the link to the log's start row (`session`, a uuid4 set at `supervise_worker.py:164`) has to come from the run directory name. `k` counts run directories per work-item (`supervise_worker.py:112-114`), and start rows carry no `k`. Two ways to link are open; see question Q5.

**D2. A commit subject with U+2028 makes `measure initiative` crash.** Command: `probe_git.py` (run). Came back: `ValueError: not enough values to unpack (expected 2, got 1)` at `scripts/measure_build.py:71`, rc 1, with a traceback and no `Refused`. Cause: `merged_commits`, `splitlines()` at line 69. Not an accepted requirement; see Q6.

**D3. Lowercase `z` is refused as not an ISO time (reading-dependent).** Command: F2 above (run). rc 1, names the file and value. r59 says "ends in `Z`". RFC 3339 allows lowercase `z`. Whether this is a refusal that should not be is open; see Q2.

**D4. A session.json holding only a newline is refused, not taken as empty (reading-dependent).** Command: B above (run). r57 says "empty"; the code tests `st_size == 0`. Whether a blank file is empty is open; see Q3.

**G1 (gap, not a defect).** `measure show` does not print the naming of an empty stage (G above, run). Open; see Q4.

## 7. The file set

Changes the work-item needs, for the accepted scenarios and the w110 finding:
- `scripts/measure_read.py` (141 lines; room 159): `read_session_jsons` keys its empty set per run directory, not per stage name. Found by read and by probe A.
- `scripts/measure_build.py` (126 lines; room 174): `stages_of` and `figures_of` match the mark per run. Found by read and by probe A. Also D2 at line 69, only if Q6 takes it in.

May change, depending on the plan:
- `features/batch-measurement.feature` (251 lines; not Python, no size limit): a scenario for two runs of one stage (Q1). Found by search: no accepted scenario covers D1.
- `tests/scenarios/batch_measurement_given_steps.py` (226 lines; room 74): a Given for two runs of a stage. Found by read.
- `tests/scenarios/batch_measurement_then_steps.py` (185 lines; room 115): a Then for the mark on a run. Found by read.

On the path, not changed (line count and room under 300):
- `scripts/measure` (90; room 210) and `scripts/measure_show.py` (87; room 213; G1 if Q4 changes it). Found by read.
- `scripts/measure_write.py` (41; room 259). Found by read.
- `tests/scenarios/batch_measurement_world.py` (140; room 160). Found by read.
- `tests/scenarios/batch_measurement_reading_steps.py` (50; room 250), `batch_measurement_transcripts.py` (39; room 261), `test_batch_measurement.py` (15; room 285). Found by read.
- Read, unchanged: `scripts/supervise_worker.py`, which writes the run directory names and the session uuid.

## Questions for the plan

- Q1. No accepted scenario covers D1 (two runs of one stage). Does the plan add a scenario, or accept r57 as it stands?
- Q2. Is lowercase `z` a time "ending in Z" (r59)? Refuse it, as now, or read it as UTC?
- Q3. Is a blank session.json "empty" (r57)? Zero bytes, as the code tests, or whitespace only?
- Q4. Should `measure show` print the stage named empty? r44 says show prints the figures as tables.
- Q5. How is an empty run directory matched to a log start row? The file has no session id, and the start row has no `k`. Either match by the order of starts and run directories for each stage (fragile), or have the run directory record its session id before dispatch (a change in `supervise_worker.py`, outside this work-item's file set). Both readings are open.
- Q6. D2 (a U+2028 commit subject crashes `measure initiative`) is not an accepted requirement. In scope or not?
- Q7. The brief's Base 1ad628 is older than HEAD 44aff93, which already holds the r57, r58, r59 and r47-retire commits. Should the plan work from HEAD?
