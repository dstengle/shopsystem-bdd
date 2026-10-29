# research of w232

Work-item: .shop/work/i54/w232.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: a2a53b36c02b74d046b7a490d802403f3f1828a9
Worktree: /tmp/work-run-i54-dk9g6cqa/w232-1-research
Branch: none (a detached checkout)
Work-item branch: work/w232
Accepted scenarios:
- features/work-queue.feature: list prints each initiative and each work-item under .shop/work/ with its status
- features/work-queue.feature: list with --json prints each initiative and work-item with its status as one JSON object
- features/work-queue.feature: show of a request prints its status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution

Read (paths in your worktree):
- .shop/work/i54/w232.md
- spec/capabilities/work-queue.md

Run directory: /tmp/work-run-i54-dk9g6cqa/w232-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i54-dk9g6cqa/w232-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i54-dk9g6cqa/w232-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
