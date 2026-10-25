# implement of w186

Work-item: .shop/work/i25/w186.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i25-xl1rfpde/w186
Branch: work/w186
Work-item branch: work/w186
Suite record: Suite: 869 passed, 0 failed at 1f4a0731 in 43 s; expected: tests/scenarios/test_supervision.py::test_a_researcher_is_given_the_workitems_file_set_and_accepted_scenarios_and_a_limit_of_80_turns, tests/scenarios/test_supervision.py::test_a_capabilityproposal_whose_every_question_from_its_formulate_round_has_an_answer_is_given_to_a_formulate_round_with_the_answers, tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[gives BLOCKED, asking "Is a title given twice one book or two?"], tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[ends with no error and before its turn limit, having written no result file], tests/scenarios/test_supervision.py::test_when_the_workitem_drafted_for_a_kept_branch_reviews_findings_turns_green_the_next_branch_review_of_the_initiative_is_started_before_work_run_exits, tests/scenarios/test_supervision.py::test_an_initiative_that_a_workitems_transition_leaves_able_to_be_done_is_set_done_before_work_run_ends, tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[ends in an error], tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[ends at its turn limit], tests/scenarios/test_supervision.py::test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_gives_questions_each_is_written_under_the_proposals__questions, tests/scenarios/test_supervision.py::test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_gives_a_question_the_proposal_is_awaitinganswer, tests/scenarios/test_supervision.py::test_when_the_gate_round_work_run_started_for_a_capabilityproposal_gives_no_question_one_question_asking_for_the_approval_of_the_proposals_lines_as_drafted_is_written_under_its__questions, tests/scenarios/test_supervision.py::test_when_the_apply_round_work_run_started_for_a_capabilityproposal_ends_the_proposals_adds_changes_and_removes_are_written_from_the_change_list_the_round_applied, tests/scenarios/test_supervision.py::test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_ends_without_giving_a_question_the_proposal_is_formulated

Read (paths in your worktree):
- .shop/work/i25/w186.md
- spec/capabilities/work-queue.md
- .shop/work/i25/runs/w186/1-research
- .shop/work/i25/runs/w186/2-plan

Run directory: /tmp/work-run-i25-xl1rfpde/w186/.shop/scratch/3-implement
Result file: /tmp/work-run-i25-xl1rfpde/w186/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i25-xl1rfpde/w186: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
