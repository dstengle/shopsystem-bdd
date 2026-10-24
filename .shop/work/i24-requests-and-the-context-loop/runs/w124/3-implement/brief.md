# implement of w124

Work-item: .shop/work/i24-requests-and-the-context-loop/w124.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w124
Branch: work/w124
Work-item branch: work/w124
Suite record: Suite: 738 passed, 4 failed at 1022a88 in 17 s; failing: tests/scenarios/test_migration_tools.py::test_a_session_about_to_be_compacted_in_a_repository_with_an_initiative_neither_done_nor_abandoned_is_told_to_write_its_handoff_with_work_note_and_end, tests/scenarios/test_migration_tools.py::test_a_session_starting_in_a_repository_on_the_plugins_version_whose_every_initiative_is_done_or_abandoned_is_told_nothing, tests/scenarios/test_migration_tools.py::test_a_session_starting_in_a_repository_with_initiatives_neither_done_nor_abandoned_is_given_what_work_status_prints_for_each_of_them, tests/scenarios/test_migration_tools.py::test_a_session_about_to_be_compacted_appends_compacted_with_the_time_to_the_ledger_of_each_initiative_neither_done_nor_abandoned; expected: tests/scenarios/test_supervision.py::test_a_workers_pytest_run_that_collects_scenarios_none_of_which_its_workitem_accepts_is_refused_when_a_requirement_the_workitem_accepts_is_not_of_a_guarantees_capability, tests/scenarios/test_supervision.py::test_a_workers_pytest_run_that_collects_scenarios_for_a_workitem_every_requirement_of_which_is_of_a_guarantees_capability_deselects_each_of_them, tests/scenarios/test_supervision.py::test_a_workers_pytest_run_for_a_workitem_every_requirement_of_which_is_of_a_guarantees_capability_left_with_no_test_exits_successfully

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w124.md
- spec/capabilities/migration-tools.md
- .shop/work/i24-requests-and-the-context-loop/runs/w124/1-research
- .shop/work/i24-requests-and-the-context-loop/runs/w124/2-plan

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w124/.shop/scratch/3-implement
Result file: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w124/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w124: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
