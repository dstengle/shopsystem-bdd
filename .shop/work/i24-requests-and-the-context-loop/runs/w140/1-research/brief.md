# research of w140

Work-item: .shop/work/i24-requests-and-the-context-loop/w140.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-4iuaa3m5/w140-1-research
Branch: none (a detached checkout)
Work-item branch: work/w140
Accepted scenarios:
- features/work-queue.feature: `work <command>` commits the change it makes to a work-item on the current branch (deprecated)
- features/work-queue.feature: `work <command>` commits the change it makes to a work-item or a capability-proposal on the current branch
- features/work-queue.feature: answer on an awaiting-answer capability-proposal writes the answer with the date under the proposal's Answers

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w140.md
- spec/capabilities/work-queue.md

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-4iuaa3m5/w140-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-4iuaa3m5/w140-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-4iuaa3m5/w140-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
