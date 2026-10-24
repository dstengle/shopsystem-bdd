# Research of w121: --work-item and guarantees

Search method: `tools tests-of` has no map here (`tools: no map`), so every list of tests is `by search`. `tools refs accepted` ran. Probes ran the worktree's `scripts/work_items.py` (PYTHONPATH set to it), not the Scripts path. My shell inherited `PYTEST_ADDOPTS=--work-item w121` from work run, so probes clear it. Probe files: `.shop/scratch/w121-1-research/probe_work_items.py`, `probe_l.py`; `probe_more.py`, `probe_debug.py` are superseded. Scratch is git-ignored; `git status --porcelain` is clean.

## 1. Why each accepted scenario is red today

- r56 "refused when a requirement ... is not of a guarantees capability" (features/supervision.feature:470): `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_a_workers_pytest_run_that_collects_scenarios_none_of_which_its_workitem_accepts_is_refused_when_a_requirement_the_workitem_accepts_is_not_of_a_guarantees_capability"` -> run, FAILED: StepDefinitionNotFoundError Given "spec/capabilities/steady.md is a guarantees capability and spec/capabilities/other.md is not" (line 472). Missing: a step writing `spec/capabilities/<cap>.md` with `group: guarantees`, and "i1's work-item w1 is ready, accepting steady#r1 and other#r1" (tests/scenarios/supervision_tests_steps.py:99-147 match only thing#r1/other#r1 literals). Later steps are not reached. The Then "was refused ... accepts none of the scenarios it collected" exists (supervision_tests_steps.py:168). Code: scripts/work_items.py:105-107 refuses unconditionally.
- r64 "deselects each of them" (:480): run, FAILED at undefined Given "spec/capabilities/steady.md is a guarantees capability" (line 482). Also undefined: Given "i1's work-item w1 is ready, accepting steady#r1 and steady#r2" and Then "... was not refused, and deselected "it waits" without running it". Code: work_items.py:99-109 has no deselect path for guarantees and reads no capability group.
- r65 "left with no test, exits successfully" (:490): run, FAILED at undefined Given (line 492). Also undefined: Given "... and the repository holds no other test" (line 494) and Then "... exited successfully". Code: work_items.py:105-109 (refusal) and no exit-status handling (pytest exits 5, see section 2).
- Retired deprecated scenario (:460, @deprecated): run, PASSED today (`...is_refused_deprecated`). It is retired by w121, so it is not red.

## 2. What the system answers today

Probe command: `python3 -m pytest -q -s -n 0 .shop/scratch/w121-1-research/probe_work_items.py` and `... probe_l.py`. Each is `run`. Cases use a fresh repo; the scenario's capability is its feature stem (`thing`), so the failing `@r2` scenario is accepted only if a work-item accepts `thing#r2`.

| case | Givens | today's result |
|---|---|---|
| A (r64) | steady guarantees; w1 accepts steady#r1, steady#r2; thing @r2 failing | exit 3, refused "w1 accepts none of the scenarios it collected" |
| B (r65) | steady guarantees; w1 accepts steady#r1; thing @r2 failing; no other test | exit 3, refused (same text) |
| C (r56) | steady guarantees + other (no group); w1 accepts steady#r1, other#r1; thing @r2 | exit 3, refused |
| D (retired) | other (no group); w1 accepts other#r1; thing @r2 | exit 3, refused |
| E | steady guarantees; steady @r1 passing, thing @r2 failing; w1 accepts steady#r1 | exit 0 (@r1 kept, @r2 deselected) |
| F | other; w1 accepts other#r1; thing @r2; probe test; only the probe file given | exit 0, probe.ran written (r55) |
| F2 | as F, whole directory | exit 3, refused; probe.ran NOT written |
| G | steady guarantees; no scenario; probe test | exit 0, probe ran |
| H | steady guarantees; w1 accepts steady#r1; no test at all | exit 5, "no tests ran" |
| I | no spec file for other; w1 accepts other#r1; thing @r2 | exit 3, refused |
| J | steady guarantees; only passing steady @r1 | exit 0 |
| K | no --work-item; `-k nothing_matches` deselects all | exit 5 |
| L | w1.md with no `accepts:` line, `--work-item w1` | exit 3, "no such work-item under .shop/work/" |

Nearest cases: F2 (a probe next to an unaccepted scenario: refused, probe lost); I (capability missing: treated as not guarantees); H and K (every item deselected: pytest exits 5); L (see defect D2).

## 3. Old assumptions

Places that still assume the old form (no map, so `by search`):

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/work_items.py:pytest_collection_modifyitems (99-109) | refuses any run that collects scenarios and accepts none | refuses only for a non-guarantees requirement (r56); deselects for all-guarantees (r64) | tests/scripts/test_work_items.py:test_a_work_item_none_of_whose_scenarios_are_collected_is_refused, :test_a_non_scenario_does_not_save_a_run... ; tests/scenarios/test_supervision.py (deprecated, r56) | search (`grep "accepts none"`), tests/scripts/test_work_items.py:67,79 |
| scripts/work_items.py exit status | pytest's exit 5 when nothing runs | r65 needs exit 0 when the plugin deselects every item | none (H, K probed only) | probe H, K |
| scripts/supervise_merge.py:merge (128-130) | any non-zero exit from the work-item's test run fails the merge (awaiting-answer) | a guarantees-only work-item's run must exit 0 or every merge fails | none (no test merges a guarantees-only work-item) | read |
| scripts/work_items.py:accepted (47-53) | reads only `accepts:`; a missing line is "no such work-item" | the new guarantees read sits beside it; L shows the misleading message | tests/scripts/test_work_items.py:test_a_work_item_that_is_not_there_is_refused (w9 only) | search |
| scripts/work_items.py module docstring | "Standard library and pytest only"; no capability read | group read from spec/capabilities/<cap>.md | none | read |
| scripts/supervise_brief.py:accepted_scenarios (89-) | lists scenarios from features/<cap>.feature; none for guarantees | no change needed; empty list for guarantees | none found by search | read |
| scripts/model_work.py:191, scripts/model.lp:216-223 | already exempt guarantees requirements from scenarios (`group(C,"guarantees")`) | same notion of guarantees; the plugin should read `group: guarantees` the same way | model tests, not run | read |

## 4. Tests the requirements make impossible to keep

Searched by text (no map). Ran `python3 -m pytest -q -n 0 tests/scripts/test_work_items.py`: 8 passed.

- tests/scripts/test_work_items.py:test_a_work_item_none_of_whose_scenarios_are_collected_is_refused (67-69) and :test_a_non_scenario_does_not_save_a_run... (79-83): consumer repo has no spec/capabilities, so `other` is not guarantees: still refused. Sound, provided a missing capability file counts as not guarantees.
- tests/scenarios/test_supervision.py deprecated scenario: passes today; retired by w121 (Retires section). Not impossible to keep; removed.
- tests/scenarios/supervision_tests_steps.py:168 Then "was refused ... accepts none": still true for the r56 non-guarantees case.
- test_probe r55 scenario (:450): not run in my shell (PYTEST_ADDOPTS problem). Read: it collects no scenario, so the refusal does not apply; sound.
- None otherwise. Node-id runs of the accepted scenarios in my shell carry the inherited PYTEST_ADDOPTS; the first undefined step is reached before any plugin refusal, so their red reasons stand.

## 5. A step the work-item skips

The guarantees path skips the existing refusal step, `raise SystemExit` at scripts/work_items.py:106-107. Only that step produces these, all from probes:
- a refusal text "--work-item w1: w1 accepts none of the scenarios it collected" and exit 3 (INTERNALERROR, "mainloop: caught unexpected SystemExit!") — probes A, B, C, D, F2, I;
- no collected test runs at all: F2's probe.ran is not written.
The deselect path must still run the non-scenario tests and call `config.hook.pytest_deselected` as the normal path does (work_items.py:108), or the "deselected" text r64 wants does not appear. Read: no path in work_items.py reads a capability's group; the model reads it in scripts/model_facts.py:178-199.

## 6. Defects

D1. The refusal ends as an internal error. Reproduce: case D: `python3 -m pytest -q -p work_items --work-item w1` with w1 accepting other#r1 and only thing @r2 collected. Output: `INTERNALERROR> SystemExit: --work-item w1: w1 accepts none of the scenarios it collected`, `mainloop: caught unexpected SystemExit!`, exit 3. `run`.

D2. A work-item without an `accepts:` line gets a misleading refusal. Reproduce: probe L, `w1.md` with status drafted and no accepts line, `python3 -m pytest -q -p work_items --work-item w1`: "no such work-item under .shop/work/", exit 3. The file exists (work_items.py:50-52 skips it). `run`.

## 7. The file set

- scripts/work_items.py (109 lines; room 191). r56 conditional on capability group, r64 deselect, r65 exit 0 when none ran (a pytest hook must change exit 5). Read and probes A-L.
- tests/scenarios/supervision_tests_steps.py (172; room 128) or a new module tests/scenarios/supervision_guarantees_steps.py (new concern, so a new module and a row is the CLAUDE.md way). Needs: spec/capabilities writer with group, multi-accept Given, "holds no other test", the deselected and exit-0 Thens. Search: pytest-bdd undefined-step messages above.
- tests/scenarios/supervision_world.py (173; room 127): helper for writing a guarantees capability, if the new steps need it. Read.
- tests/scenarios/test_supervision.py (242; room 58): read only; the scenario bindings follow the feature file. Check whether it binds by `scenarios(...)`, so the retired one disappears. Read.
- features/supervision.feature (842; no limit): retire the deprecated scenario at :459-467 (the Retires section).
- tests/scripts/test_work_items.py (98; room 202): add cases for the guarantees path; the 8 existing ones keep passing (section 4).
- scripts/supervise_merge.py (135; room 165): on the path, no edit if the plugin exits 0 for a guarantees-only work-item (merge reads the exit at 128-130). Read.
- scripts/supervise_brief.py, scripts/model_work.py, scripts/model.lp: read only, no edit.
- spec/capabilities/supervision.md (109): r56, r64, r65 already written; no edit.

Plugin path lines are from `wc -l` and `Grep`; `tools size` was not run.

## Questions for the plan (not decided here)
1. F2: a probe test kept (r55) next to an unaccepted scenario of a non-guarantees capability: r56 literally refuses the run; r55 says keep the probe. Both readings are in the notes: refuse (today) or run the probe and deselect.
2. I: a missing capability file: "not of a guarantees capability" (refuse) or "unknown" (refuse). Both refuse today; reading it as guarantees would be wrong.
