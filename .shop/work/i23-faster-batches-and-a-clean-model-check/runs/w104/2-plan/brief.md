# plan of w104

Work-item: .shop/work/i23-faster-batches-and-a-clean-model-check/w104.md
Agent: bdd-planner
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.24.0/scripts
Base: 1ad628182e2dd2eb91d1e0ed6e95ecb34f3bcc63
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w104-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w104
Questions the researcher gave with its DONE, for you to settle or ask:
- What is the accepts fact for a requirement: a scenario id as today, or a requirement id as well?
- D5: should a work-item accepting a requirement no capability has be an unresolved reference, or remain a file problem with a different message?
- The job guard for w_unserved_cap: this context never reads jobs, so 'no job' is always true here. Is r111 a guard on job nodes, or a fixed silence?
- tests/scripts/test_model_output.py::test_check_ends_with_the_four_counts expects the warning that r111 removes: change its expected count, or its setup?

Read (paths in your worktree):
- .shop/work/i23-faster-batches-and-a-clean-model-check/w104.md
- spec/capabilities/design-model-check.md
- .shop/work/i23-faster-batches-and-a-clean-model-check/runs/w104/1-research

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w104-2-plan/.shop/scratch/2-plan
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w104-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w104-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
