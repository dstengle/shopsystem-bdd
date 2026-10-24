# research of w123

Work-item: .shop/work/i24-requests-and-the-context-loop/w123.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w123-1-research
Branch: none (a detached checkout)
Work-item branch: work/w123
Accepted scenarios:
- features/work-queue.feature: status of an initiative prints where it stands, for a session to start from
- features/work-queue.feature: status with no initiative prints each initiative that is neither done nor abandoned
- features/work-queue.feature: status with --json prints its result as one JSON object
- features/work-queue.feature: note appends the line, with the date, to the initiative's ledger
- features/work-queue.feature: note commits the ledger on the current branch
- features/work-queue.feature: note with a line break in it is refused, and nothing changes

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w123.md
- spec/capabilities/work-queue.md

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w123-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w123-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w123-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
