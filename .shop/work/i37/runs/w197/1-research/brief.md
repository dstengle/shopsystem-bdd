# research of w197

Work-item: .shop/work/i37/w197.md
Agent: code-scout
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Base: 94be81b4c7efa16e4b751858da00db485be242d1
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w197-1-research
Branch: none (a detached checkout)
Work-item branch: work/w197
Accepted scenarios:
- features/requests.feature: turn passes the request's turn from the <side> to the <other side> (deprecated)
- features/requests.feature: turn on a request it does not set to accepted passes the request's turn from the <side> to the <other side>
- features/requests.feature: the upstream ending its turn on a request that turn sets to accepted keeps the request's turn the upstream's
- features/requests.feature: resolve setting a request's status to delivered passes the request's turn to its asker

Read (paths in your worktree):
- .shop/work/i37/w197.md
- spec/capabilities/requests.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w197-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w197-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w197-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
