# plan of w221

Work-item: .shop/work/i46/w221.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 134745663cfa0a109b8564370c2464ef9ee9a7d5
Worktree: /tmp/work-run-i46-rhbgokrg/w221-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w221
Questions the researcher gave, for you to settle or ask:
- r122: is an approved glossary-proposal's removes excused across the whole context, or only within its own initiative? The scenario has one initiative; the spec is unscoped.
- A drafted glossary-proposal under a done initiative: model check's v_d1 blocks it, while workqueue_done.py ignores glossary-proposals. r123 names only the approved case; should the queue match model check?
- glossary-proposal lifecycle is read as drafted, awaiting-answer, approved, withdrawn (from the decision 0073 ledger and supervision r160, r169); the scenarios fix only drafted, approved and formulated. Confirm it.

Read (paths in your worktree):
- .shop/work/i46/w221.md
- spec/capabilities/design-model-check.md
- .shop/work/i46/runs/w221/1-research

Run directory: /tmp/work-run-i46-rhbgokrg/w221-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i46-rhbgokrg/w221-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i46-rhbgokrg/w221-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
