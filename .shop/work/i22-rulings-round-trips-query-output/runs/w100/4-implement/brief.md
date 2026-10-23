# implement of w100

Work-item: .shop/work/i22-rulings-round-trips-query-output/w100.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-hi6aey0q/w100
Branch: work/w100
Work-item branch: work/w100
Suite record: Suite: 699 passed, 1 failed at 6865b9a in 14 s; failing: tests/scenarios/test_work_queue.py::test_answer_with_a_newline_in_it_is_refused_and_nothing_changes
Answers the person gave, each with the question it answers:
- Question: The work-item rules that the deprecated batch-measurement @r42 scenario and the deprecated work-queue @r9 outline are retired and listed under a `## Retires` section, and that gives_totals asserts every token column again afterwards. But the work-item has no Retires section, so this item cannot retire them. Reading A: the coordinator adds a `## Retires` section listing both scenarios. w100 then also retires them with `features retire` and makes gives_totals strict, and features/batch-measurement.feature, features/work-queue.feature and tests/scenarios/batch_measurement_then_steps.py join the file set. The person sees both deprecated scenarios gone from the suite, and the r42 totals scenario failing on any wrong token column. Reading B: w100 goes ahead without them, and a later work-item with a Retires section does M1, M2 and I2. Until then both deprecated scenarios stay in the suite and gives_totals stays lenient about token columns.
  Answer: 2026-10-23: Reading A: w100.md now has the Retires section naming both scenarios; retire them, make gives_totals strict, and add the two feature files and batch_measurement_then_steps.py to the file set.

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w100.md
- spec/capabilities/work-queue.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w100/1-research
- .shop/work/i22-rulings-round-trips-query-output/runs/w100/2-plan
- .shop/work/i22-rulings-round-trips-query-output/runs/w100/3-plan

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-hi6aey0q/w100/.shop/scratch/4-implement
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-hi6aey0q/w100/.shop/scratch/4-implement/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-hi6aey0q/w100: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
