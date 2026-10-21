# implement of size-check

Work-item: .shop/work/i15-size-limit/size-check.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 2ea9b66fb6b40f0918de085a0ef8a4be38ac5130
Worktree: /tmp/work-run-i15-size-limit-l6t3hnm6/size-check
Branch: work/size-check
Suite record: Suite: 602 passed, 4 failed at b8bc20d in 7 s; failing: tests/scenarios/test_analysis_tools.py::test_size_prints_each_tracked_python_file_over_the_limit_in_the_working_tree_with_its_line_count, tests/scenarios/test_analysis_tools.py::test_size_fails_when_one_tracked_python_file_is_over_the_limit, tests/scenarios/test_analysis_tools.py::test_size_uses_the_limit_limit_gives_and_300_lines_without_it[--limit 250-250-251], tests/scenarios/test_analysis_tools.py::test_size_uses_the_limit_limit_gives_and_300_lines_without_it[-300-301]

Read (paths in your worktree):
- .shop/work/i15-size-limit/size-check.md
- spec/capabilities/analysis-tools.md
- .shop/work/i15-size-limit/runs/size-check/1-research
- .shop/work/i15-size-limit/runs/size-check/2-plan

Run directory: /tmp/work-run-i15-size-limit-l6t3hnm6/size-check/.shop/scratch/3-implement
Result file: /tmp/work-run-i15-size-limit-l6t3hnm6/size-check/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i15-size-limit-l6t3hnm6/size-check: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write your notes, plan, report or findings in the run directory and, last, the result file: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings).
