# implement of w158

Work-item: .shop/work/i24-requests-and-the-context-loop/w158.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-tdnk4mdl/w158
Branch: work/w158
Work-item branch: work/w158
Suite record: Suite: 822 passed, 1 failed at e5a100c in 19 s; failing: tests/scenarios/test_supervision.py::test_a_proposed_initiative_that_fulfils_no_request_is_given_no_integrate_round_stays_proposed_and_leaves_nothing_behind; expected: tests/scenarios/test_batch_measurement.py::test_an_initiative_fulfilling_a_request_the_queue_does_not_hold_is_refused, tests/scenarios/test_batch_measurement.py::test_an_initiative_fulfilling_a_request_with_no_asker_is_refused, tests/scenarios/test_batch_measurement.py::test_an_initiative_fulfilling_more_than_one_request_is_refused, tests/scenarios/test_design_model_check.py::test_a_status_in_its_kinds_lifecycle_is_no_file_problem[a work directory .shop/work/i1 has the part p1.md with the kind capability-proposal and the status awaiting-answer-.shop/work/i1/p1.md], tests/scenarios/test_design_model_check.py::test_a_status_in_its_kinds_lifecycle_is_no_file_problem[a request in .shop/work/requests/q1.md, of the form `work request` writes, has the status withdrawn-.shop/work/requests/q1.md], tests/scenarios/test_supervision.py::test_under_a_delegation_a_workitem_with_two_questions_has_each_given_to_a_session_of_its_own_and_both_answers_stay_written_when_the_run_ends

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w158.md
- spec/capabilities/supervision.md
- .shop/work/i24-requests-and-the-context-loop/runs/w158/1-research
- .shop/work/i24-requests-and-the-context-loop/runs/w158/2-plan

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-tdnk4mdl/w158/.shop/scratch/3-implement
Result file: /tmp/work-run-i24-requests-and-the-context-loop-tdnk4mdl/w158/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-tdnk4mdl/w158: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
