# implement of w96

Work-item: .shop/work/i22-rulings-round-trips-query-output/w96.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w96
Branch: work/w96
Work-item branch: work/w96
Suite record: Suite: 659 passed, 0 failed at bd55621 in 13 s; expected: tests/scenarios/test_analysis_tools.py::test_testsof_with_json_prints_the_tests_their_count_and_the_maps_commit_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_untested_with_json_prints_the_functions_their_count_and_the_maps_commit_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_refs_with_json_prints_the_references_and_the_summary_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_map_with_json_prints_the_maps_commit_and_its_test_count_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_testsof_fails_when_the_file_has_no_function_by_the_name_given, tests/scenarios/test_analysis_tools.py::test_testsof_says_that_no_test_of_the_map_executed_the_target_and_exits_successfully
Answers the person gave, each with the question it answers:
- Question: F7: when `.shop/plugin-version` holds no version (e.g. `next`, or nothing), what does `migrate status --hook`, the SessionStart hook, do? `--hook`'s help says it exits 0; the work-item says 'refuse, saying why'; no requirement settles which governs. Reading A, exit 0 with text: the hook prints to stdout a line saying the version file holds no version, naming what it holds and telling the session to tell the person. The session is told at its start and passes it on, and the hook keeps its exit-0 contract. Reading B, exit 1 as `migrate status` does: the hook prints the reason on stderr and exits 1. The session's context gets nothing; the person sees only the hook error that Claude Code reports, and the session never learns why.
  Answer: 2026-10-23: Reading A: migrate status --hook exits 0 and prints one line saying the version file holds no version, naming what it holds and telling the session to tell the person.

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w96.md
- spec/capabilities/migration-tools.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w96/1-research
- .shop/work/i22-rulings-round-trips-query-output/runs/w96/2-plan
- .shop/work/i22-rulings-round-trips-query-output/runs/w96/3-plan

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w96/.shop/scratch/4-implement
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w96/.shop/scratch/4-implement/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w96: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
