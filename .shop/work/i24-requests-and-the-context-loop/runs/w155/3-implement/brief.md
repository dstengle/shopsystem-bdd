# implement of w155

Work-item: .shop/work/i24-requests-and-the-context-loop/w155.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w155
Branch: work/w155
Work-item branch: work/w155
Suite record: Suite: 828 passed, 2 failed at 39aa930 in 18 s; failing: tests/scenarios/test_supervision.py::test_when_a_session_started_under_a_delegation_to_answer_a_question_ends_at_its_turn_limit_the_question_is_left_unanswered_for_the_person, tests/scenarios/test_supervision.py::test_when_a_session_started_under_a_delegation_to_answer_a_question_ends_in_an_error_its_stage_directory_and_log_lines_are_committed; expected: tests/scenarios/test_supervision.py::test_when_a_round_work_run_started_for_a_capabilityproposal_ends_at_its_turn_limit_the_proposal_keeps_its_status, tests/scenarios/test_supervision.py::test_a_request_this_context_is_the_upstream_of_that_is_status_is_given_to_an_intake_round[awaiting-upstream], tests/scenarios/test_supervision.py::test_when_a_round_work_run_started_for_a_capabilityproposal_gives_an_outcome_other_than_done_no_transition_is_made_from_it, tests/scenarios/test_supervision.py::test_a_request_this_context_is_the_upstream_of_that_is_status_is_given_to_an_intake_round[open], tests/scenarios/test_supervision.py::test_when_a_round_work_run_started_for_a_capabilityproposal_leaves_no_result_it_can_read_work_run_exits_with_an_error_naming_the_round_and_how_it_ended

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w155.md
- spec/capabilities/supervision.md
- .shop/work/i24-requests-and-the-context-loop/runs/w155/1-research
- .shop/work/i24-requests-and-the-context-loop/runs/w155/2-plan

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w155/.shop/scratch/3-implement
Result file: /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w155/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w155: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
