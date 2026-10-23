# plan of w97

Work-item: .shop/work/i22-rulings-round-trips-query-output/w97.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w97-3-plan
Branch: none (a detached checkout)
Work-item branch: work/w97
Questions the researcher gave with its DONE, for you to settle or ask:
- Should 'one above the highest work-item' count only w<n>.md-named files (current) or every work-item's id? With fix-login.md holding id w7, the current code gives w2; the id reading gives w8.
- Should a plain note named w2.md (or a non-UTF-8 .md note) beside work-items block work add? Current code refuses both (D1, D2).
Answers the person gave, each with the question it answers:
- Question: Beside work-item .shop/work/i1/w1.md sits a plain note .shop/work/i1/w2.md (no work-item frontmatter); what does `work add i1 ...` do? Reading A (work-queue#r12 and r7 as written: one above the highest work-item is w2, whose file exists): work add exits with an error, writes nothing, and the refusal names .shop/work/i1/w2.md as a file that is not a work-item, instead of today's 'the work-item w2 already exists'. Reading B (the work-item's finding N9 F10, 'number it past every w<n>.md'): work add prints w3 and writes .shop/work/i1/w3.md as a drafted work-item with id w3, one above the highest w<n>.md file rather than one above the highest work-item.
  Answer: 2026-10-23: Reading A: work-queue r12 and r7 as written. work add refuses, writing nothing, naming .shop/work/<initiative>/w<n>.md as a file that is not a work-item.

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w97.md
- spec/capabilities/design-model-check.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/1-research
- .shop/work/i22-rulings-round-trips-query-output/runs/w97/2-plan

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w97-3-plan/.shop/scratch/3-plan
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w97-3-plan/.shop/scratch/3-plan/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w97-3-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
