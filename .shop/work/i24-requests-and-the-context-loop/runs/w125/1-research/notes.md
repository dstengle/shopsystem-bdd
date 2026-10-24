# Research of w125 (supervision r56, r64, r65)

Tool note: `tools tests-of` and `tools refs` ran; `tools tests-of` says "no map" (no `tools map` made), so every test list below is `by search`. `tools refs` counts are `refs`.

Probes: `.shop/scratch/w125-1-research/probe_guarantees.py` (cases 1-11) and `probe_refusal.py` (cases 12-15). Each consumer repo is built under `.shop/scratch/w125-1-research/consumers/` with its own `pytest.ini`. Run with `python3 -m pytest -q -s -n 0 <probe file>`.

## 1. Why each scenario is red today

None is red. All three pass on today's code.
- `python3 -m pytest -q -n 0 --tb=short -p no:warnings` with the three node ids of `tests/scenarios/test_supervision.py` (r56 "refused ...", r64 "deselects ...", r65 "left with no test ...`): `3 passed` (run).
- Default config (`pytest.ini` addopts `-n auto`): `tests/scripts/test_work_items.py` and the r65 node id: `12 passed` (run).
- Givens and Thens: `tests/scenarios/supervision_tests_steps.py:160-170` (capabilities), `:189-208` (Thens). Scenario test names are the three node ids above.

The gap is not in these scenarios. It is r65 under xdist (`-n 2`), which no scenario or test covers (part 6, D1).

## 2. What the system answers today (probes, run)

Command for each: `python3 -m pytest -q -p work_items [-n 2] --work-item w1` in the consumer. Scenario `it answers` is `@r1`, `it waits` is `@r2`, feature `thing`.

| case | accepts / capabilities | options | exit | output (last line) |
|---|---|---|---|---|
| 1 | other#r1; other guarantees | none | 0 | `2 deselected` |
| 2 | other#r1; other guarantees | `-n 2` | **5** | `4 warnings`, no test ran (D1) |
| 3 | other#r1; other guarantees; a non-scenario `test_probe.py` | `-n 2` | 0 | `1 passed` |
| 4 | other#r1, mixed#r1; other guarantees, mixed not | `-n 2` | 3 | INTERNALERROR, `SystemExit: w1 accepts none of the scenarios it collected` |
| 5 | as 4 | none | 3 | as 4 |
| 6 | other#r1; no capability file for other | none | 3 | refused, as 4 (read: `guarantees()` false) |
| 7 | thing#r1; thing guarantees (scenario requirement accepted) | none | 0 | `1 passed, 1 deselected` |
| 8 | thing#r1; thing guarantees | `-n 2` | 0 | `1 passed` |
| 9 | other#r1; other guarantees; repo holds no test | `-n 2` | **5** | `no tests ran` (D1) |
| 10 | other#r1; other guarantees; repo holds no test | none | 0 | `no tests ran` |
| 11 | other#r1, mixed#r1; repo holds no test | `-n 2` | 5 | `no tests ran` (not r65: mixed is not guarantees; exit 5 is today's) |
| 12 | work-item w9 missing | `-n 2` | 3 | `mainloop: caught unexpected SystemExit!` (message in the worker, not shown) |
| 13 | work-item w9 missing | none | 3 | `INTERNALERROR> SystemExit: --work-item w9: no such work-item under .shop/work/` |
| 14 | as 4 | `-n 2` | 3 | `SystemExit: --work-item w1: w1 accepts none of the scenarios it collected` in INTERNALERROR |
| 15 | as 4 | none | 3 | as 14 |

Nearest cases the scenarios do not give:
- Guarantees-only item with a non-scenario test left (case 3, and `tests/scripts/test_work_items.py:100`): run exits 0 under `-n 2`.
- Missing work-item, mixed item, and missing capability file are refused with exit 3 through an INTERNALERROR traceback, not exit 1. The message is there (cases 13-15). Observation only.
- Scenario requirement accepted from a guarantees capability (cases 7-8) runs its scenario; r65 does not apply.

## 3. Old assumptions

The old form is the stash `config.stash[GUARANTEES]`, set in collection and read at session end. It is set only where collection runs in-process, so the xdist controller does not hold it. Callers found by `tools refs GUARANTEES` (2 production, 0 test) and `tools refs guarantees` (3 refs: 1 production, 1 test); the rest by search.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/work_items.py:pytest_sessionfinish (128-131) | exit 5 becomes 0 when stash `GUARANTEES` is set | must decide from the work-item and spec alone, on the controller and on each worker: the stash is unset on the xdist controller (D1) | tests/scripts/test_work_items.py:93 (serial only); tests/scenarios/test_supervision.py r65 node (serial, via worker) | refs GUARANTEES; search |
| scripts/work_items.py:pytest_collection_modifyitems (112-113) | sets `GUARANTEES` when every accepted capability is guarantees | the only source of the decision today; replaced by a computation in sessionfinish | tests/scripts/test_work_items.py:93, 100, 108; r64 and r65 nodes (serial) | refs GUARANTEES; search |
| scripts/work_items.py:GUARANTEES (125) | the StashKey | removed with the stash | none (key is used only at 113 and 130) | refs GUARANTEES |
| scripts/work_items.py:guarantees (116-122) | reads `group: guarantees` from spec/capabilities/<cap>.md | callable from sessionfinish as is; no change needed | tests/scripts/test_work_items.py:93, 100, 108; r56/r64/r65 nodes | refs guarantees |
| scripts/work_items.py:accepted (49-55) | reads the work-item's accepts; SystemExit if no such work-item | sessionfinish would call it again; missing item already refused in collection | tests/scripts/test_work_items.py:62 (w9 refused) | search (refs not run) |
| scripts/supervise_merge.py:Merge.merge (128-132) | runs `tests["work_item"]` (`-n auto` where xdist is importable) and refuses the merge on nonzero exit | a guarantees-only item's merge gate exits 5 under xdist (D1); fixed once the exit is 0 | none (not traced; no map) | search |

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map, so this list is `by search` (all uses of `--work-item`, `guarantees`, exit 5 in tests/).
- tests/scripts/test_work_items.py:93, 100, 108 (r64, r65, r56 serial): keep. Run today, pass. The fix keeps exit 0 and the refusal.
- tests/scripts/test_work_items.py:62, 67, 79 (missing work-item, none accepted, non-scenario does not save a run): keep. Run today, pass; untouched by the fix.
- tests/scenarios/test_supervision.py r56, r64, r65 nodes: keep. Run today, pass. r65's Then (`supervision_tests_steps.py:198-201`) checks only the worker's pytest exit code, not w1's merge outcome; so the merge gate of D1 is not seen by it.
- No test asserts exit 5 (search for `returncode == 5`, `code == 5`): none.
- No test runs `-n 2` with `--work-item`: none. The new test in part 7 is the first.

## 5. A step the work-item skips

The collection-time step (modifyitems) does not run on the xdist controller; workers run it. The new sessionfinish path recomputes the accepted set from the option, so the controller does not depend on it. What only the collection step produces, and the new path does not:
- the deselection of scenarios (serial output `N deselected`; `-n 2` output shows none, probe 9): effect seen in case 1 and 10, read for the controller.
- refusal "no such work-item" (case 13) and "accepts none" (cases 4-5, 14-15): raised in collection; the controller reports INTERNALERROR and exit 3 (cases 12-15, run). The new path must not refuse twice; the work-item file is read again in sessionfinish, read.
Read: a guarantees-only run with no scenario collected has nothing for the refusals to say, so the new path skips no refusal for that case.

## 6. Defects

### D1: `--work-item` for a guarantees-only work-item with no test left exits 5 under xdist
Reproduction (run, probe 2 and 9): consumer with `pytest.ini` (`[pytest]`), `features/thing.feature` (`it answers` @r1, `it waits` @r2), `tests/test_thing.py`, `.shop/work/i1/w1.md` (`status: ready`, `accepts: [other#r1]`), `spec/capabilities/other.md` (`group: guarantees`).
- `python3 -m pytest -q -p work_items --work-item w1` → exit 0, `2 deselected` (case 1).
- `python3 -m pytest -q -p work_items -n 2 --work-item w1` → exit 5, `no tests ran` (case 2).
- Same with no scenario in the repo (case 9, exit 5) and `-n 2`, versus case 10 (exit 0).
- Mechanism (read): the stash is set in `pytest_collection_modifyitems` (work_items.py:112-113), which the xdist controller does not run; `pytest_sessionfinish` (130-131) sees no stash and keeps exit 5.
- Effect (read): `scripts/supervise_merge.py:128-130` treats exit 5 from `tests["work_item"]` as failure, and `tests()` adds `-n auto` where xdist imports; so a guarantees-only work-item's merge is refused in such a repository. Not run end to end.

## 7. The file set

Files the work-item must change (by read of the r65 path and probes):
- `scripts/work_items.py` (131 lines, room 169): `pytest_sessionfinish` computes "guarantees-only" from `config.getoption("--work-item")` through `accepted()` and `guarantees()`, not the stash; drop `GUARANTEES` (125) and the stash set (112-113). Shown by refs GUARANTEES and probe 2.
- `tests/scripts/test_work_items.py` (127 lines, room 173): new test runs `pytest(repo, "-n", "2", "--work-item", "w1")` on a guarantees-only consumer (as `test_a_guarantees_work_item_has_its_scenarios_deselected_and_exits_successfully`, line 93) and asserts returncode 0. Shown by probe 2.

Modules on the change's path, not edited (must keep passing):
- `scripts/supervise_merge.py` (135 lines, room 165): merge gate, consumer of exit code; read, unchanged.
- `conftest.py` (10 lines, room 290): loads the plugin in this repository; unchanged.
- `pytest.ini` (4 lines; not Python): `addopts = -n auto`, which makes every run here parallel; unchanged.
- `tests/scenarios/test_supervision.py` (246 lines, room 54) and `tests/scenarios/supervision_tests_steps.py` (208 lines, room 92): r56/r64/r65 scenarios; unchanged, must still pass.

`tools size --limit 300` printed nothing: no tracked Python file is over the limit.
