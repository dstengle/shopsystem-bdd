# implement of w165

Work-item: .shop/work/i27/w165.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 3cbd0c528b0bd62d10ca4b2453f47921f76c1c6e
Worktree: /tmp/work-run-i27-15a81p5x/w165
Branch: work/w165
Work-item branch: work/w165
Suite record: Suite: 849 passed, 1 failed at cc16fb45 in 23 s; failing: tests/scenarios/test_requests.py::test_request_with_delegation_writes_the_delegation_given_in_the_request; expected: tests/scenarios/test_supervision.py::test_an_initiative_with_no_workitem_gets_no_branch_review_though_its_branch_holds_a_commit_no_kept_branch_review_has_read, tests/scenarios/test_supervision.py::test_an_integrate_round_that_ends_done_without_a_change_list_ends_work_run_with_an_error_naming_the_round, tests/scenarios/test_supervision.py::test_an_initiative_with_no_workitem_is_not_measured, tests/scenarios/test_supervision.py::test_work_run_started_with_no_initiative_runs_the_integrate_apply_and_formulate_rounds_of_different_initiatives_one_at_a_time, tests/scenarios/test_supervision.py::test_the_drafts_of_an_integrate_round_that_ending_are_kept_on_the_initiative_branch[ends at its turn limit], tests/scenarios/test_supervision.py::test_an_integrate_rounds_change_list_gives_one_drafted_capabilityproposal_for_each_capability_it_names_with_what_it_adds_changes_and_removes_on_that_capability, tests/scenarios/test_supervision.py::test_the_drafts_of_an_integrate_round_that_ending_are_kept_on_the_initiative_branch[gives DONE with a change list naming thing], tests/scenarios/test_supervision.py::test_a_started_initiative_with_neither_a_capabilityproposal_nor_a_workitem_is_given_to_an_integrate_round_with_the_accepted_lines_of_the_request_it_fulfils, tests/scenarios/test_work_queue.py::test_start_commits_the_initiative_it_writes_on_the_current_branch

Read (paths in your worktree):
- .shop/work/i27/w165.md
- spec/capabilities/requests.md
- .shop/work/i27/runs/w165/1-research
- .shop/work/i27/runs/w165/2-plan

Run directory: /tmp/work-run-i27-15a81p5x/w165/.shop/scratch/3-implement
Result file: /tmp/work-run-i27-15a81p5x/w165/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i27-15a81p5x/w165: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
