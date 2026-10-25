# implement of w174

Work-item: .shop/work/i25/w174.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i25-_k05m4uy/w174
Branch: work/w174
Work-item branch: work/w174
Suite record: Suite: 870 passed, 8 failed at 125b2ad1 in 23 s; failing: tests/scenarios/test_requests.py::test_the_asker_answering_a_question_leaves_the_requests_questions_and_line_outcomes_as_they_were_and_writes_no_resolution, tests/scenarios/test_requests.py::test_the_upstream_asking_a_question_on_a_line_in_its_turn_writes_the_question_in_the_request, tests/scenarios/test_requests.py::test_the_asker_answering_a_question_in_its_turn_writes_the_answer_in_the_request, tests/scenarios/test_requests.py::test_outcome_writing_a_line_outcome_leaves_the_requests_lines_and_answers_as_the_asker_wrote_them, tests/scenarios/test_requests.py::test_a_change_to_a_request_commits_the_request_on_the_current_branch, tests/scenarios/test_work_queue.py::test_answer_that_asks_for_a_change_to_a_reviewers_question_transitions_the_workitem_to_ready, tests/scenarios/test_work_queue.py::test_answer_that_accepts_the_workitem_as_it_is_to_a_reviewers_question_transitions_the_workitem_to_done, tests/scenarios/test_work_queue.py::test_answer_to_a_reviewers_question_that_says_neither_whether_it_asks_for_a_change_nor_whether_it_accepts_the_workitem_is_refused_and_nothing_changes

Read (paths in your worktree):
- .shop/work/i25/w174.md
- spec/capabilities/work-queue.md
- .shop/work/i25/runs/w174/1-research
- .shop/work/i25/runs/w174/2-plan

Run directory: /tmp/work-run-i25-_k05m4uy/w174/.shop/scratch/3-implement
Result file: /tmp/work-run-i25-_k05m4uy/w174/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i25-_k05m4uy/w174: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
