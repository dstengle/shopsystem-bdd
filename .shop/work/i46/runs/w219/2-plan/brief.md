# plan of w219

Work-item: .shop/work/i46/w219.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 134745663cfa0a109b8564370c2464ef9ee9a7d5
Worktree: /tmp/work-run-i46-0i81ojqg/w219-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w219
Questions the researcher gave, for you to settle or ask:
- r54 vs supervision.feature:1479-1482 and supervision_integrate_steps.py:150: the term-in-capability-entry scenario conflicts with r54. Reading (a): move the term to a glossary entry and reword the scenario. Reading (b): keep it, which contradicts r54. Which does the owner want?
- The same conflict applies to features/supervision.feature:1700-1704 (gate brief listing term "ledger" under p1's adds).

Read (paths in your worktree):
- .shop/work/i46/w219.md
- spec/capabilities/spec-integration.md
- .shop/work/i46/runs/w219/1-research

Run directory: /tmp/work-run-i46-0i81ojqg/w219-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i46-0i81ojqg/w219-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i46-0i81ojqg/w219-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
