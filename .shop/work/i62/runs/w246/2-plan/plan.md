# Plan of w246: fix the findings of branch review 1 of i62

Work-item: .shop/work/i62/w246.md, under supervision, accepts supervision#r219@0.29, r220, r222, findings .shop/work/i62/runs/branch-review/1/findings.md. No `Retires` section, no `## Rulings`.

## 1. What goes green

All three scenarios already pass (research run: `python3 -m pytest -q --work-item w246`, 194 passed, exit 0). The work is the two findings triaged **fix now**: 1 and 2. Each gets a red test before its change.

- supervision#r219@0.29, "run again once, alone, before the merge is refused" (features/supervision.feature:2062): green today, and stays green. Its step stops reading the `rerun` log line (decision 2).
- supervision#r220@0.29, "both runs in the question" (features/supervision.feature:2072): green today. It covers only a scenario that fails in both first runs. The gap is finding 1: the question holds the output of `failed[0]` (the work-item's scenario run) and then the second runs. So a scenario that fails only in the whole-suite run, and fails again alone, has its first run missing from the question. That goes against r220. A new unit test shows this red (part 2).
- supervision#r222@0.29, "passes on its second run lets the merge go" (features/supervision.feature:2081): green today, and stays green.

Deprecated scenarios retired: none.

## 2. Where the change lands

- `scripts/supervise_merge.py` (175 lines):
  - In `Merge.merge`, the refusal's question gives both runs of each scenario whose second run failed (decision 1).
  - `Merge.suite_record` (or whatever `merge` gets from the suite run) keeps the suite run's output and command so the question can use them.
  - In `Merge.taken_back`, the append of the `rerun` line to `log.jsonl` is removed (decision 2).
- `tests/scripts/test_supervise_merge_rerun.py` (122 lines):
  - New test for finding 1. Stub the scenario run's output failing on NODE, and the suite run's output failing on NODE and OTHER, each with its `SCENARIO` line. NODE's run alone passes; OTHER's run alone fails. Assert the question holds OTHER's `FAILED` line from the suite run, the suite command, and OTHER's second run.
  - The `rerun` log assertion at line 67 goes (part 4).
- `tests/scenarios/supervision_rerun_steps.py` (76 lines): the `rerun` log assertion in `closes_run_alone` (lines 54-55) goes (part 4).

This is the researcher's set, taken under reading (b) of finding 2. No file is added or removed. These files stay as they are and must keep passing:
- `scripts/work_items.py` and `tests/scripts/test_work_items.py` (finding 5 is not fix-now)
- `features/supervision.feature`

All files stay under 300 lines.

## 3. Decisions

1. **The question of a refused merge (finding 1).**
   - For each scenario whose second run failed, the question gives:
     - every run before the merge that failed on that scenario (the work-item's scenario run, the whole-suite run, or both), each with its command and its output;
     - then that scenario's second run, with its command and output.
   - A run before the merge that names no such scenario is not added just for that.
   - The header no longer names only the first failing command.
   - Rests on supervision#r220@0.29 ("both runs of the scenario in the question r131 writes") and r131. A scenario's first run is whichever run before the merge failed on it, which can be the whole-suite run that r43 and r4 make.
2. **The `rerun` line in `log.jsonl` is removed (finding 2, reading b).**
   - The Behaviour lines that write to `log.jsonl` are r8 and r49. The Implementation section (supervision.md, "`log.jsonl` also gets a `push verified` line … and a `suite` line …") names only those lines, and no line names a `rerun` line.
   - Keeping the line would first need a new Implementation line through integrating-a-proposal. That is outside this work-item, which accepts only r219, r220 and r222 and can change no spec.
   - Removing it takes `work run` back to what the spec says it writes. Rests on the supervision Implementation line on `log.jsonl`, r7 (what a transition commits) and design-decision/workflow-capabilities-are-guarantees (behaviour only through a line).
3. **Findings 3, 4, 5, 6, 7 and the Range note are not fixed here.** The review marks them as observations or drop, not fix-now. `has_error`, the node-id and `-n` parsing, and `work_items.py` are left unchanged.

## 4. Tests the decisions break

- `tests/scripts/test_supervise_merge_rerun.py::test_a_scenario_failing_in_both_runs_gets_one_run_alone_and_a_pass_there_merges`, line 67, asserts the `rerun` log line.
  - Decision 2 breaks it.
  - The test is rewritten without that assertion. It keeps its other assertions: one run alone, `--whole-suite`, `-n 0` as the only `-n`, and the merge going ahead. A pass alone merging is still r222.
  - If the implementer wants to pin decision 2, the test may assert that `log.jsonl` has no `rerun` line.
- `tests/scenarios/supervision_rerun_steps.py::closes_run_alone`, lines 54-55, assert the `rerun` line.
  - Decision 2 breaks it.
  - Those lines are removed. r219 is still shown by line 53 (`runs[-1:] == ["alone"]`) and by the "run no other time" count of runs alone (findings.md, finding 2).
- Decision 1 breaks none:
  - The r220 step (supervision_rerun_steps.py:69-76) checks both commands and "it does not close" in the question. A question that holds more runs still passes.
  - test_supervise_merge_rerun.py:78-122 (error, non-scenario, no `-n`, error count, empty rerun) do not touch the question's runs or the log. The notes verified this.

## 5. Open cases

- **Shared runs.** When two scenarios fail again alone and share a first run, the implementer names whether that run's output appears once or once for each scenario.
- **Long suite output.** When the whole-suite output is long, the implementer names whether the question holds it whole or only the part that names the scenario. Either way it must hold the scenario's `FAILED` line and the run's command.
- **One scenario in both first runs.** When a scenario fails in both the work-item's run and the suite run, and again alone, the implementer names whether the question gives both first runs or one.
- **Mixed outcomes.** When some scenarios pass alone and others fail alone, the implementer names whether the question also lists the ones that passed alone.
