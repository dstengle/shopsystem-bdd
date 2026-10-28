# research of w216

Work-item: .shop/work/i43/w216.md
Agent: code-scout
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.1/scripts
Base: ebbf1beaaa1fb5e4e3d29ffde673a5999a2cbd22
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w216-1-research
Branch: none (a detached checkout)
Work-item branch: work/w216
Accepted scenarios:
- features/supervision.feature: before the branch review starts, <run> is run at the initiative branch's head
- features/supervision.feature: the branch reviewer is given each run made before it, with its command, how it exited and its output, and the commit they ran at
- features/supervision.feature: the branch reviewer is given as files to read the work-items' capabilities, the design-decisions they rest on, and each work-item's plan, report and review findings
- features/supervision.feature: the branch reviewer is given the commits from the initiative branch's base to its head, each with the work-item it belongs to or none, and the change of that range less .shop/

Read (paths in your worktree):
- .shop/work/i43/w216.md
- spec/capabilities/supervision.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w216-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w216-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w216-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
