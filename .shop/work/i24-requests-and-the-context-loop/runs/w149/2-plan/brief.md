# plan of w149

Work-item: .shop/work/i24-requests-and-the-context-loop/w149.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-bowwvrlq/w149-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w149
Questions the researcher gave with its DONE, for you to settle or ask:
- D3: should work outcome refuse a line number beyond the request's Lines (today it is written and blocks the settled status)?
- D4: should a request with no lines be refused at work request, or turn to refused as it does now (vacuous r9)?

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w149.md
- spec/capabilities/requests.md
- .shop/work/i24-requests-and-the-context-loop/runs/w149/1-research

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-bowwvrlq/w149-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i24-requests-and-the-context-loop-bowwvrlq/w149-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-bowwvrlq/w149-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
