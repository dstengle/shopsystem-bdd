# plan of w191

Work-item: .shop/work/i32/w191.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: d3d3839d7347d73cc5e3d51f1761ba13875a4ae2
Worktree: /tmp/work-run-i32-8o05wlcn/w191-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w191
Questions the researcher gave with its DONE, for you to settle or ask:
- The accepted scenarios already pass, so no requirement of w191 is red. Should the plan still take D1 (KeyError, findings finding 1), which no accepted requirement covers? Reading (a): add a requirement to the supervision capability for it. Reading (b): fix it as a defect with no new requirement.
- D1 readings: when no verdict comes from this run, leave the item awaiting-answer for the person (r77, r89), or refuse naming the item. The findings suggest keeping the verdict with the answer so a later run can move it. Both are open.
- D2: work answer --accept on a non-reviewer's question is accepted and the flag ignored. Refuse it, as the reviewer rule does, or leave it as it is?

Read (paths in your worktree):
- .shop/work/i32/w191.md
- spec/capabilities/supervision.md
- .shop/work/i32/runs/w191/1-research

Run directory: /tmp/work-run-i32-8o05wlcn/w191-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i32-8o05wlcn/w191-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i32-8o05wlcn/w191-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
