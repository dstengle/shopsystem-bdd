# review of w97

Work-item: .shop/work/i22-rulings-round-trips-query-output/w97.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w97-6-review
Branch: none (a detached checkout)
Work-item branch: work/w97
Answers the person gave, each with the question it answers:
- Question: Beside work-item .shop/work/i1/w1.md sits a plain note .shop/work/i1/w2.md (no work-item frontmatter); what does `work add i1 ...` do? Reading A (work-queue#r12 and r7 as written: one above the highest work-item is w2, whose file exists): work add exits with an error, writes nothing, and the refusal names .shop/work/i1/w2.md as a file that is not a work-item, instead of today's 'the work-item w2 already exists'. Reading B (the work-item's finding N9 F10, 'number it past every w<n>.md'): work add prints w3 and writes .shop/work/i1/w3.md as a drafted work-item with id w3, one above the highest w<n>.md file rather than one above the highest work-item.
  Answer: 2026-10-23: Reading A: work-queue r12 and r7 as written. work add refuses, writing nothing, naming .shop/work/<initiative>/w<n>.md as a file that is not a work-item.

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w97.md
- spec/capabilities/design-model-check.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/1-research
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/2-plan
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/3-plan
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/4-implement
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/5-review

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w97-6-review/.shop/scratch/6-review
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w97-6-review/.shop/scratch/6-review/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-aawfn3s_/w97-6-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
