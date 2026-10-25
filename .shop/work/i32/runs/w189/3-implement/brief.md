# implement of w189

Work-item: .shop/work/i32/w189.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: d3d3839d7347d73cc5e3d51f1761ba13875a4ae2
Worktree: /tmp/work-run-i32-_6c6pt8f/w189
Branch: work/w189
Work-item branch: work/w189
Suite record: Suite: 883 passed, 0 failed at 6fa7dc00 in 24 s; expected: tests/scenarios/test_supervision.py::test_an_initiative_that_a_workitems_transition_leaves_able_to_be_done_is_set_done_before_work_run_ends, tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[ends in an error], tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[ends at its turn limit], tests/scenarios/test_supervision.py::test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_gives_questions_each_is_written_under_the_proposals__questions, tests/scenarios/test_supervision.py::test_when_the_apply_round_work_run_started_for_a_capabilityproposal_ends_the_proposals_adds_changes_and_removes_are_written_from_the_change_list_the_round_applied, tests/scenarios/test_supervision.py::test_under_a_delegation_an_answer_to_a_reviewers_question_that_accepts_the_workitem_as_it_is_transitions_the_workitem_to_done, tests/scenarios/test_supervision.py::test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_gives_a_question_the_proposal_is_awaitinganswer, tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[ends with no error and before its turn limit, having written no result file], tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[gives BLOCKED, asking "Is a title given twice one book or two?"], tests/scenarios/test_supervision.py::test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_ends_without_giving_a_question_the_proposal_is_formulated, tests/scenarios/test_supervision.py::test_a_capabilityproposal_whose_every_question_from_its_formulate_round_has_an_answer_is_given_to_a_formulate_round_with_the_answers, tests/scenarios/test_supervision.py::test_under_a_delegation_an_answer_to_a_reviewers_question_that_asks_for_a_change_makes_the_workitem_ready_again

Read (paths in your worktree):
- .shop/work/i32/w189.md
- spec/capabilities/review.md
- .shop/work/i32/runs/w189/1-research
- .shop/work/i32/runs/w189/2-plan

Run directory: /tmp/work-run-i32-_6c6pt8f/w189/.shop/scratch/3-implement
Result file: /tmp/work-run-i32-_6c6pt8f/w189/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i32-_6c6pt8f/w189: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
