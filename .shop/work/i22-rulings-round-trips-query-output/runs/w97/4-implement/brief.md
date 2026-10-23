# implement of w97

Work-item: .shop/work/i22-rulings-round-trips-query-output/w97.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w97
Branch: work/w97
Work-item branch: work/w97
Suite record: Suite: 657 passed, 0 failed at 8659d64 in 13 s; expected: tests/scenarios/test_analysis_tools.py::test_testsof_with_json_prints_the_tests_their_count_and_the_maps_commit_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_untested_with_json_prints_the_functions_their_count_and_the_maps_commit_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_refs_with_json_prints_the_references_and_the_summary_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_map_with_json_prints_the_maps_commit_and_its_test_count_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_testsof_fails_when_the_file_has_no_function_by_the_name_given, tests/scenarios/test_analysis_tools.py::test_testsof_says_that_no_test_of_the_map_executed_the_target_and_exits_successfully
Answers the person gave, each with the question it answers:
- Question: Beside work-item .shop/work/i1/w1.md sits a plain note .shop/work/i1/w2.md (no work-item frontmatter); what does `work add i1 ...` do? Reading A (work-queue#r12 and r7 as written: one above the highest work-item is w2, whose file exists): work add exits with an error, writes nothing, and the refusal names .shop/work/i1/w2.md as a file that is not a work-item, instead of today's 'the work-item w2 already exists'. Reading B (the work-item's finding N9 F10, 'number it past every w<n>.md'): work add prints w3 and writes .shop/work/i1/w3.md as a drafted work-item with id w3, one above the highest w<n>.md file rather than one above the highest work-item.
  Answer: 2026-10-23: Reading A: work-queue r12 and r7 as written. work add refuses, writing nothing, naming .shop/work/<initiative>/w<n>.md as a file that is not a work-item.

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w97.md
- spec/capabilities/design-model-check.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/1-research
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/2-plan
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/3-plan

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w97/.shop/scratch/4-implement
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w97/.shop/scratch/4-implement/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w97: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
