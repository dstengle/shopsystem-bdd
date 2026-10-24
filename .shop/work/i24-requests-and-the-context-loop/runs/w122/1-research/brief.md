# research of w122

Work-item: .shop/work/i24-requests-and-the-context-loop/w122.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w122-1-research
Branch: none (a detached checkout)
Work-item branch: work/w122
Accepted scenarios:
- features/batch-measurement.feature: --sessions gives the sessions that start inside the window and every session they dispatched (deprecated)
- features/batch-measurement.feature: --sessions gives the sessions active inside the window, starting inside it or before it with a message inside it, and every session they dispatched
- features/batch-measurement.feature: each session --sessions gives is given with its round trips, tool uses by tool name, dispatches and compactions
- features/batch-measurement.feature: show prints each session's round trips, tool uses by tool name, dispatches and compactions beside its tokens
- features/batch-measurement.feature: compare prints the totals over the sessions of round trips, tool uses and compactions side by side with the ratio of the second to the first

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w122.md
- spec/capabilities/batch-measurement.md

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w122-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w122-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w122-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
