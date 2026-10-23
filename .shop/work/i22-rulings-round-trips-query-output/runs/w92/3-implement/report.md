# Report of w92 implement

## Budget
scripts/supervise.py, scripts/supervise_merge.py, scripts/supervise_brief.py, scripts/supervise_worker.py, scripts/workqueue.py, features/supervision.feature (retire only), tests/scenarios/test_supervision.py, tests/scenarios/supervision_given.py, tests/scenarios/supervision_faults_steps.py, tests/scenarios/supervision_answers_steps.py (new). Ten files, all touched.

## What changed
- work run writes awaiting-answer (supervise.py Run.stage, supervise_merge.py), prints open questions and exits 3 for it, and pairs `## Questions` with `## Answers`. workqueue STATUSES lists awaiting-answer (awaiting-ruling stays).
- Briefs.answer_lines: each worker's brief holds each answer beside its question (r57), paired by position.
- Workers.worktree: when work/<name> exists, the worktree is made on it, without `-b` (r58).
- Seven deprecated scenarios retired with `features retire` (plan part 1).
- Tests: the scenarios' `work run` env drops SHOPSYSTEM_WORK_RUN_WORKER (decision 5); the awaiting-ruling Then became awaiting-answer; the Rulings Givens became Answers Givens; new supervision_answers_steps.py holds the r57 Given/Then and the r58 Given/Then (the r58 Given has the stand-in watch the kept file; the Then checks the brief's Branch line and the file seen).
- Deviation from the plan: the Questions-then-Rulings Then step was rewritten to Answers, not removed, because the r36 replacement scenario's Then needs it.

## Red and green
- Red: `python3 -m pytest -q --work-item w92 -n0` before any edit: 23 failed (the 21 supervision scenarios, from the worker guard in the env and from missing steps; plus 2 tests/scripts/test_tools.py nested-map tests, which fail before and after for reasons outside w92). After the env fix, the r5 rows failed with `assert 'awaiting-ruling' == 'awaiting-answer'`, as expected (code wrote awaiting-ruling). r57 failed on its Then (brief held no answer), r58 on `git worktree add -b` with "a branch named 'work/w1' already exists".
- Green: final `python3 -m pytest -q -n0 --work-item w92`: 134 passed, 2 failed (test_tools.py::test_the_map_says_which_tests_execute_a_function and test_untested_names_each_function_no_test_executed: `tools: no map was made` / `--work-item w92: no such work-item under .shop/work/`, in a nested pytest run in a temp project; they failed before my first edit too and are not w92 scenarios). tests/scenarios/test_supervision.py: 14 passed (its w92 scenarios).
- Suite at start (brief): 627 passed, 11 failed at d9181a7 (supervision tests).

## Tests changed under an allowance
none beyond the plan's list ("Tests the decisions break"): test_supervision.py awaiting Then and env builder, the Questions/Answers Then, supervision_given.py item_with_sections, supervision_faults_steps.py awaiting_with_questions — each as the plan says.

## Open questions
- More answers than questions, an empty `## Questions`, bullets with continuation lines (answer_lines joins continuation lines with spaces; extra answers are not printed).
- The exact text of a pair in the brief beyond what r57 checks.
- Kept branch and r24 (pre-run on an unrebased branch) and under_work on a kept branch.
- Merge.failed_claimed's path to awaiting-answer: no scenario reaches it.
- `work retry` after a Fault in merge() reaching a kept branch: no scenario end to end.

The plan contained no code; nothing pasted.

## Completeness check
`tools size --limit 300` printed nothing.

## Now possible
`work run` moves a work-item to awaiting-answer, prints its open questions, tells every worker the answers beside their questions, and an implementer carries on from a kept work/<name> branch.

## Outside the file set
none.

## Commits
adf0d01, 79cc5a1.
