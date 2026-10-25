# implement of w192

Work-item: .shop/work/i33/w192.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 1caef88132eda3084c4ef5d18d7c8deeeccaf483
Worktree: /tmp/work-run-i33-9vstbbh_/w192
Branch: work/w192
Work-item branch: work/w192
Suite record: Suite: 891 passed, 10 failed at ff6fe166 in 24 s; failing: tests/scenarios/test_supervision.py::test_a_kept_branch_review_whose_result_gives_outcome_and_no_question_is_taken_as_listing_nothing_to_fix_now[BLOCKED], tests/scenarios/test_supervision.py::test_a_kept_branch_review_whose_result_gives_outcome_and_no_question_is_taken_as_listing_nothing_to_fix_now[NEEDS_CONTEXT], tests/scenarios/test_supervision.py::test_an_initiative_whose_workitems_are_workitems_and_whose_kept_branch_review_lists_nothing_to_fix_now_measured[w1 is withdrawn and w2 is withdrawn-is not measured-ran no `measure initiative`], tests/scenarios/test_supervision.py::test_an_initiative_whose_workitems_are_workitems_its_delivery_otherwise_closed_set[w1 is green and w2 is withdrawn-is set done-is done], tests/scenarios/test_supervision.py::test_an_initiative_whose_workitems_are_workitems_its_delivery_otherwise_closed_set[w1 is withdrawn and w2 is withdrawn-is not set done-is not done], tests/scenarios/test_supervision.py::test_a_kept_branch_review_whose_result_gives_outcome_and_no_question_is_taken_as_listing_nothing_to_fix_now[DONE], tests/scenarios/test_supervision.py::test_a_kept_branch_review_whose_result_gives_outcome_and_no_question_is_taken_as_listing_nothing_to_fix_now[PARTIAL], tests/scenarios/test_work_queue.py::test_withdraw_that_leaves_every_workitem_of_an_initiative_withdrawn_leaves_the_initiatives_status_as_it_is, tests/scenarios/test_work_queue.py::test_add_given_an_initiative_that_is_status_is_refused_naming_its_status_and_changes_nothing[done], tests/scenarios/test_work_queue.py::test_add_given_an_initiative_that_is_status_is_refused_naming_its_status_and_changes_nothing[abandoned]

Read (paths in your worktree):
- .shop/work/i33/w192.md
- spec/capabilities/work-queue.md
- .shop/work/i33/runs/w192/1-research
- .shop/work/i33/runs/w192/2-plan

Run directory: /tmp/work-run-i33-9vstbbh_/w192/.shop/scratch/3-implement
Result file: /tmp/work-run-i33-9vstbbh_/w192/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i33-9vstbbh_/w192: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
