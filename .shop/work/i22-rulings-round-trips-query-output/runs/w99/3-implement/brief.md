# implement of w99

Work-item: .shop/work/i22-rulings-round-trips-query-output/w99.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w99
Branch: work/w99
Work-item branch: work/w99
Suite record: Suite: 690 passed, 3 failed at 6941c6e in 15 s; failing: tests/scenarios/test_migration_tools.py::test_a_session_starting_in_a_repository_whose_shoppluginversion_holds_no_version_is_told_to_tell_the_person, tests/scenarios/test_migration_tools.py::test_migrate_command_on_a_shoppluginversion_that_holds_no_version_exits_with_an_error_naming_what_it_holds[status], tests/scenarios/test_migration_tools.py::test_migrate_command_on_a_shoppluginversion_that_holds_no_version_exits_with_an_error_naming_what_it_holds[upgrade]

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w99.md
- spec/capabilities/migration-tools.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w99/1-research
- .shop/work/i22-rulings-round-trips-query-output/runs/w99/2-plan

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w99/.shop/scratch/3-implement
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w99/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w99: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
