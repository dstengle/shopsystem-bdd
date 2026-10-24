# plan of w129

Work-item: .shop/work/i24-requests-and-the-context-loop/w129.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w129-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w129
Questions the researcher gave with its DONE, for you to settle or ask:
- Requests r14 and work-queue r17 both govern work status with no initiative: does r14 add observations to the output (additive) or replace the initiative blocks? The SessionStart hook uses the same output.
- Should work show refuse (exit 1) when a request file under .shop/work/requests is not UTF-8, as it does for work-items today?

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w129.md
- spec/capabilities/requests.md
- .shop/work/i24-requests-and-the-context-loop/runs/w129/1-research

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w129-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w129-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w129-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
