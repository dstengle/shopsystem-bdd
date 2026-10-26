# intake of q15

Request: .shop/work/requests/q15.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: intake
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/q15-1-intake
Branch: round/q15-1-intake
Lines of the request:
- 1. **When** the upstream ends its turn on a request and `work` sets the request to `accepted`, `work` shall keep the request's turn the upstream's.
- 2. **When** `work` sets a request to `delivered`, `work` shall pass the request's turn to its asker.

Read (paths in your worktree):
- .shop/work/requests/q15.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts/work outcome q15 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts/work turn q15`.

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/q15-1-intake/.shop/scratch/1-intake
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/q15-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/q15-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
