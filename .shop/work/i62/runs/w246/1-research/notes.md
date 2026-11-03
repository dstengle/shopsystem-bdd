# w246 research notes

Accepted: supervision#r219@0.29, r220, r222. Capability: spec/capabilities/supervision.md. Tools: `tools map` absent (no map), so `tests-of` and `untested` not used; test lists are `by search`. `refs` not run.

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q --work-item w246`. Result (run): 194 passed, 1 skipped, 56 subtests passed, exit 0, no failure line. The three scenarios are collected (named in the run's warnings); per-test outcome not listed.

- features/supervision.feature:2062 r219 "run again once, alone, before the merge is refused": green (run).
- features/supervision.feature:2072 r220 "both runs in the question": green (run).
- features/supervision.feature:2081 r222 "passes on its second run lets the merge go": green (run).

Nothing is missing for the three scenarios. What they do not pin is in parts 2 and 3: the findings of branch review 1 (.shop/work/i62/runs/branch-review/1/findings.md, read) name two gaps, and the fix is to be the work-item.

## 2. Old assumptions

The old form: a failing run refuses a merge, and the question shows one run. Tests found by search (no map).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_merge.py:Merge.merge (164-169) | question gives `failed[0]` output plus second runs only | r220: both runs of each rerun scenario; a suite-only failure's first run is dropped (finding 1) | by search: tests/scripts/test_supervise_merge_rerun.py:70-75 (asserts "boom" only) | read; branch review finding 1 |
| scripts/supervise_merge.py:Merge.suite_record (35-53) | returns the run's output; logs counts only | suite output of another failing scenario must reach the question (finding 1) | none (test file overrides it in Stubbed) | read; branch review finding 1 |
| scripts/supervise_merge.py:Merge.taken_back (145-147) | appends a `rerun` line to log.jsonl | no Behaviour or Implementation line asks for it (finding 2) | by search: tests/scripts/test_supervise_merge_rerun.py:67; tests/scenarios/supervision_rerun_steps.py:54-55 | read; branch review finding 2 |
| scripts/supervise_merge.py:Merge.has_error (117-121) | reads the first `short test summary info` header | r222 merges a passing rerun; a nested summary's ERROR refuses (finding 3, errs to refusal) | none (no test has a nested summary; 78-80 and 102-106 use a top-level one) | read; branch review finding 3 |
| scripts/work_items.py:pytest_terminal_summary (162-169) | prints `SCENARIO` lines under --work-item only | with a delivery `[tests]` override not loading the plugin, no failure is a scenario, so no rerun (finding 5; r219 against r29) | by search: tests/scripts/test_work_items.py:128-130 (asserts SCENARIO lines) | read; branch review finding 5 |

## 3. Tests the requirements make impossible to keep

By search (no map). Verified as sound: tests/scripts/test_supervise_merge_rerun.py:78-122 (error, non-scenario, no -n, error count, empty rerun) all pass in the run and touch neither the question header nor the log; they stay under either reading below.

- tests/scripts/test_supervise_merge_rerun.py::test_a_scenario_failing_in_both_runs_gets_one_run_alone_and_a_pass_there_merges, line 67: asserts the `rerun` log line. Impossible to keep if finding 2 is fixed by removing the log write. Kept if the fix adds an Implementation line.
- tests/scenarios/supervision_rerun_steps.py::closes_run_alone, lines 54-55: same; asserts the `rerun` line. Same condition.
- Nothing else: the r220 question test (supervision_rerun_steps.py:69-76) checks both commands and "it does not close" in the question, so a question with more runs still passes.

Readings for finding 2 (not decided here):
- (a) keep: add to supervision.md Implementation a line "and a `rerun` line for each second run before a merge"; no test breaks.
- (b) remove: drop the log write at merge line 147 and the assertion at rerun_steps 54-55 and test line 67.

## 4. The file set

Changed by the work-item:
- scripts/supervise_merge.py: merge() question gives both runs of each rerun scenario, including the suite run's output of another failing scenario (finding 1); reading (a) keeps taken_back's log line, reading (b) removes it (finding 2). Read of merge() and taken_back().
- tests/scripts/test_supervise_merge_rerun.py: new test for finding 1: stub suite output failing on NODE and OTHER; NODE's alone run passes, OTHER's fails; assert OTHER's suite-run FAILED line is in the question. Reading (b) drops line 67. Read of the file.
- tests/scenarios/supervision_rerun_steps.py: only under reading (b): drop lines 54-55. Read of the file.

Not changed, must keep passing: features/supervision.feature (r219, r220, r222 scenarios pass as they are); scripts/work_items.py (finding 5 not in the set; a reading "fix it" would touch it); tests/scripts/test_work_items.py.

Modules on the change's path (lines by wc; room under 300 per CLAUDE.md):
- scripts/supervise_merge.py: 175 lines, room 125 (edited).
- scripts/supervise.py: 295 lines, room 5 (Run.log at 94, Run.move at 113 used by merge; not edited).
- scripts/supervise_faults.py: 194 lines, room 106 (Fault, fault_of; not edited).
- scripts/supervise_worker.py: 259 lines, room 41 (git, with_scripts, worktree; not edited).
- scripts/workqueue.py: 294 lines, room 6 (move, agrees; not edited).
- scripts/work_items.py: 180 lines, room 120 (SCENARIO lines; not edited).
- tests/scripts/test_supervise_merge_rerun.py: 122 lines, room 178 (edited).
- tests/scenarios/supervision_rerun_steps.py: 76 lines, room 224 (edited under reading b).
- tests/scenarios/supervision_tests_steps.py: 252 lines, room 48 (r219/r220 steps; not edited).

Limits: `tools size --limit 300` printed nothing (run); all files above are within it.

Git: `git status --porcelain` clean at the end; `.shop/scratch/1-research/` is not listed.
