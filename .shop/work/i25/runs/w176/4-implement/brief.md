# implement of w176

Work-item: .shop/work/i25/w176.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i25-inmctmii/w176
Branch: work/w176
Work-item branch: work/w176
Suite record: Suite: 868 passed, 3 failed at 9c79765c in 29 s; failing: tests/scenarios/test_work_queue.py::test_answer_that_accepts_the_workitem_as_it_is_to_a_reviewers_question_transitions_the_workitem_to_done, tests/scenarios/test_work_queue.py::test_answer_that_asks_for_a_change_to_a_reviewers_question_transitions_the_workitem_to_ready, tests/scenarios/test_work_queue.py::test_answer_to_a_reviewers_question_that_says_neither_whether_it_asks_for_a_change_nor_whether_it_accepts_the_workitem_is_refused_and_nothing_changes; expected: tests/scenarios/test_supervision.py::test_when_every_workitem_is_green_or_withdrawn_and_no_request_whose_asker_is_this_context_is_in_the_askers_turn_work_run_exits_successfully_printing_each_workitems_status, tests/scenarios/test_supervision.py::test_when_work_run_ends_while_a_request_whose_asker_is_this_context_is_in_the_askers_turn_it_exits_with_an_error_printing_the_request_with_its_open_questions, tests/scenarios/test_requests.py::test_request_with_an_empty_delegation_is_refused_and_nothing_changes, tests/scenarios/test_supervision.py::test_a_request_this_context_is_the_upstream_of_that_is_status_is_given_to_an_intake_round_that_writes_each_lines_line_outcome_or_a_question_on_it[open], tests/scenarios/test_supervision.py::test_a_request_this_context_is_the_upstream_of_that_is_status_is_given_to_an_intake_round_that_writes_each_lines_line_outcome_or_a_question_on_it[awaiting-upstream], tests/scenarios/test_supervision.py::test_a_question_an_intake_round_gives_on_a_line_of_a_request_is_written_in_the_request, tests/scenarios/test_supervision.py::test_a_field_of_a_workers_result_giving_a_sentence_longer_than_a_file_name_may_be_is_taken_as_no_file, tests/scenarios/test_supervision.py::test_work_run_started_with_no_initiative_ending_with_no_node_awaitinganswer_or_failed_and_no_request_whose_asker_is_this_context_in_the_askers_turn_exits_successfully_printing_the_status_of_each_initiative_it_took

Read (paths in your worktree):
- .shop/work/i25/w176.md
- spec/capabilities/work-queue.md
- .shop/work/i25/runs/w176/1-research
- .shop/work/i25/runs/w176/2-research
- .shop/work/i25/runs/w176/3-plan

Run directory: /tmp/work-run-i25-inmctmii/w176/.shop/scratch/4-implement
Result file: /tmp/work-run-i25-inmctmii/w176/.shop/scratch/4-implement/result.json

You start in your worktree, /tmp/work-run-i25-inmctmii/w176: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
